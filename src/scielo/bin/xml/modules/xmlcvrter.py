# coding=utf-8

import os
import shutil
from datetime import datetime

from isis_models import IssueModels, ArticleRecords2Article
import ftp_service
import email_service
import serial_files
import html_reports
import pkg_reports
import xml_versions
import isis
import xmlcvrter_cfg
import article_utils
import fs_utils
import xml_utils
import xpmaker


converter_report_lines = []
CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')
CONFIG_PATH = CURRENT_PATH + '/../config/'
converter_env = None


class ConverterEnv(object):

    def __init__(self):
        self.version = None
        self.db_issue = None
        self.db_article = None
        self.db_isis = None
        self.website_folders_path = None
        self.serial_path = None
        self.is_windows = None


def register_log(message):
    if not '<' in message:
        message = html_reports.format_message(message)
    converter_report_lines.append(message)


def find_i_record(issue_label, print_issn, e_issn):
    i_record = None
    issues_records = converter_env.db_issue.search(issue_label, print_issn, e_issn)
    if len(issues_records) > 0:
        i_record = issues_records[0]
    return i_record


def find_issue_models(issue_label, p_issn, e_issn):
    #print(issue_data)

    i_record = None
    issue_models = None
    msg = None

    if issue_label is None:
        msg = html_reports.format_message('FATAL ERROR: Unable to identify the article\'s issue')
    else:
        i_record = find_i_record(issue_label, p_issn, e_issn)

        if i_record is None:
            msg = html_reports.format_message('FATAL ERROR: Issue ' + issue_label + ' is not registered in ' + db_issue.db_filename + '. (' + '/'.join([i for i in [p_issn, e_issn] if i is not None]) + ')')
        else:
            issue_models = IssueModels(i_record)

    return (issue_models, msg)


def get_creation_date(id_filename):
    previous_creation_date = None
    if os.path.isfile(id_filename):
        records = isis.IDFile().read(id_filename)
        previous_article = ArticleRecords2Article(records)
        previous_creation_date = previous_article.creation_date
    return previous_creation_date


def check_previous_articles_order(previous_articles, articles):
    inconsistent_orders = {}
    for name, article in articles.items():
        previous = previous_articles.get(name)

        if previous is not None:
            if previous.order != article.order:
                inconsistent_orders[name] = (previous.order, article.order)
    return inconsistent_orders


def previous_and_current_package(issue_files, pkg_path, previous_articles, current_articles):

    whole_pkg_path = pkg_path + '_complete'
    if not os.path.isdir(whole_pkg_path):
        os.makedirs(whole_pkg_path)

    for name in os.listdir(whole_pkg_path):
        os.unlink(whole_pkg_path + '/' + name)

    for name in previous_articles.keys():
        if not name in current_articles.keys():
            shutil.copyfile(issue_files.base_source_path + '/' + name, whole_pkg_path + '/' + name)

    update = []
    new = []
    for name, article in current_articles.items():
        shutil.copyfile(pkg_path + '/' + name, whole_pkg_path + '/' + name)
        if name in previous_articles.keys():
            update.append(name)
        else:
            new.append(name)

    complete_package = xpmaker.get_articles(whole_pkg_path)
    for name in os.listdir(whole_pkg_path):
        os.unlink(whole_pkg_path + '/' + name)

    return (new, update, complete_package)


def validate_previous_and_current_package(issue_files, pkg_path):
    print('issue_files.base_source_path')
    print(issue_files.base_source_path)
    print('pkg_path')
    print(pkg_path)

    msg = ''

    previous_articles = xpmaker.get_articles(issue_files.base_source_path)
    current_articles = xpmaker.get_articles(pkg_path)

    inconsistent_orders = check_previous_articles_order(previous_articles, current_articles)
    if len(inconsistent_orders) > 0:
        msg += html_reports.tag('h4', 'checking order of previous version')
    for name, orders in inconsistent_orders.items():
        msg += html_reports.format_message('WARNING: Found inconsistence: previous ' + name + ' has order=' + orders[0])
        msg += html_reports.format_message('WARNING: Found inconsistence: current  ' + name + ' has order=' + orders[1])

    new, update, complete_package = previous_and_current_package(issue_files, pkg_path, previous_articles, current_articles)

    previous = [name for name in previous_articles.keys() if not name in new and not name in update]

    toc_f, toc_e, toc_w, toc_report = pkg_reports.validate_package(complete_package, validate_order=True)

    toc_w += len(inconsistent_orders)
    toc_report = pkg_reports.get_toc_report_text(toc_f, toc_e, toc_w, msg + toc_report)

    status_report = ''
    for status, items in {'new': new, 'previous': previous, 'update': update}.items():
        status_report += html_reports.format_list(status, 'ol', items, 'label')

    return (toc_f, status_report + toc_report, inconsistent_orders)


def normalized_package(src_path, report_path, wrk_path, pkg_path, version):
    xml_filenames = sorted([src_path + '/' + f for f in os.listdir(src_path) if f.endswith('.xml') and not 'incorrect' in f])
    pkg_items = xpmaker.make_package(xml_filenames, report_path, wrk_path, pkg_path, version, 'acron')
    return (xml_filenames, pkg_items)


def get_issue_models(pkg_items):
    issue_label, p_issn, e_issn = xpmaker.package_issue(pkg_items)
    return find_issue_models(issue_label, p_issn, e_issn)


def get_issue_files(issue_models, pkg_path):
    journal_files = serial_files.JournalFiles(converter_env.serial_path, issue_models.issue.acron)
    return serial_files.IssueFiles(journal_files, issue_models.issue.issue_label, pkg_path, converter_env.website_folders_path)


def convert_package(src_path):
    display_title = False
    validate_order = True
    conversion_report = ''
    msg = []
    acron_issue_label = 'acron issue label'
    scilista_item = None

    dtd_files = xml_versions.DTDFiles('scielo', converter_env.version)
    result_path = src_path + '_xml_converter_result'
    wrk_path = result_path + '/work'
    pkg_path = result_path + '/scielo_package'
    report_path = result_path + '/errors'
    old_report_path = report_path

    xml_filenames, pkg_items = normalized_package(src_path, report_path, wrk_path, pkg_path, converter_env.version)
    issue_models, issue_error_msg = get_issue_models(pkg_items)

    if issue_models is None:
        msg.append(issue_error_msg)
    else:
        issue_files = get_issue_files(issue_models, pkg_path)
        result_path = issue_files.issue_path

        toc_f, toc_report, inconsistent_orders = validate_previous_and_current_package(issue_files, pkg_path)

        msg.append(toc_report)

        if toc_f == 0 and len(pkg_items) > 0:
            articles_stats, articles_reports, articles_sheets = pkg_reports.validate_pkg_items(pkg_items, dtd_files, validate_order, display_title)
            msg.append(pkg_reports.get_articles_report_text(articles_reports, articles_stats))
            msg.append(pkg_reports.get_lists_report_text(articles_reports, articles_sheets))

            issue_files.move_reports(report_path)
            issue_files.save_source_files(pkg_path)
            report_path = issue_files.base_reports_path

            articles = {doc_file_info.xml_name: article for article, doc_file_info in pkg_items}
            scilista_item, conversion_report = convert_articles(issue_files, issue_models, articles, articles_stats, inconsistent_orders)
            if scilista_item is not None:
                acron_issue_label = scilista_item

    report_filename = report_path + '/xml_converter.html'
    texts = []
    texts.append(pkg_reports.xml_list(pkg_path, xml_filenames))
    texts.append(html_reports.join_texts(msg))
    texts.append(conversion_report)
    texts.append(pkg_reports.processing_result_location(result_path))

    content = html_reports.join_texts(texts)

    if old_report_path in content:
        content = html_reports.get_unicode(content)
        content = content.replace(html_reports.get_unicode(old_report_path), html_reports.get_unicode(report_path))

    pkg_reports.save_report(report_filename, ['XML Conversion (XML to Database)', acron_issue_label], content)
    pkg_reports.display_report(report_filename)

    return (report_filename, report_path, scilista_item)


def convert_articles(issue_files, issue_models, articles, articles_stats, inconsistent_orders):
    index = 0
    status_text = ['converted', 'not converted', 'first version', 'previous version (aop)', 'previous version (aop) unmatched', 'previous version (aop) without PID', 'previous version (aop) partially matched', ]
    order = ['converted', 'not converted', 'new', 'matched', 'unmatched', 'invalid', 'partially matched']

    articles_by_status = {}
    for k in order:
        articles_by_status[k] = []

    ex_ahead = 0
    article_id_created = 0
    n = '/' + str(len(articles))

    ahead_manager = serial_files.AheadManager(converter_env.db_isis, converter_env.db_issue, issue_files.journal_files, issue_models.issue.issn_id)

    text = ''
    for xml_name, article in articles.items():
        index += 1
        item_label = str(index) + n + ' - ' + xml_name
        print(item_label)

        msg = ''
        xml_stats, data_stats = articles_stats[xml_name]
        xml_f, xml_e, xml_w = xml_stats
        data_f, data_e, data_w = data_stats

        valid_ahead, ahead_status, ahead_msg, ahead_comparison = ahead_manager.get_valid_ahead(article, xml_name)
        articles_by_status[ahead_status].append(xml_name)

        section_code, issue_validations_msg = validate_xml_issue_data(issue_models, article)

        msg += html_reports.tag('h4', 'checking ex-ahead')
        msg += ''.join([html_reports.format_message(item) for item in ahead_msg])
        msg += ''.join([html_reports.tag('pre', item) for item in ahead_comparison])
        msg += html_reports.tag('h4', 'checking issue data')
        msg += issue_validations_msg

        conv_f, conv_e, conv_w = html_reports.statistics_numbers(msg)

        if conv_f + xml_f + data_f == 0:
            article.section_code = section_code
            if valid_ahead is not None:
                article._ahead_pid = valid_ahead.ahead_pid

            article_files = serial_files.ArticleFiles(issue_files, article.order, xml_name)

            creation_date = get_creation_date(article_files.id_filename)

            done = converter_env.db_article.create_id_file(issue_models.record, article, article_files, creation_date)
            if done:
                if xml_name in inconsistent_orders.keys():
                    prev_order, curr_order = inconsistent_orders[xml_name]
                    prev_article_files = serial_files.ArticleFiles(issue_files, prev_order, xml_name)
                    os.unlink(prev_article_files.id_filename)

                article_id_created += 1
                if valid_ahead is not None:
                    if ahead_status in ['matched', 'partially matched']:
                        done, ahead_msg = ahead_manager.manage_ex_ahead(valid_ahead)
                        msg += ''.join([item for item in ahead_msg])
                        if done:
                            ex_ahead += 1
                articles_by_status['converted'].append(xml_name)
                msg += html_reports.format_message('OK: converted')
            else:
                articles_by_status['not converted'].append(xml_name)
                msg += html_reports.format_message('FATAL ERROR: not converted')
                conv_f += 1
        title = html_reports.statistics_display(conv_f, conv_e, conv_w, True)
        text += html_reports.collapsible_block(xml_name + 'conv', title, msg)

    summary = '#'*80
    i = 0
    for status in order:
        summary += display_list(status_text[i], articles_by_status[status])
        i += 1

    if ex_ahead > 0:
        still_ahead = ahead_manager.finish_manage_ex_ahead()
        if len(still_ahead) > 0:
            still_ahead = [still_ahead[k][0] + still_ahead[k][1] + still_ahead[k][2] for k in sorted(still_ahead.keys(), reverse=True)]
            summary += display_list('ahead list', still_ahead)

    scilista_item = None
    if article_id_created == len(articles):
        if converter_env.db_article.finish_conversion(issue_models.record, issue_files) > 0:
            scilista_item = issue_models.issue.acron + ' ' + issue_models.issue.issue_label
            if not converter_env.is_windows:
                converter_env.db_article.generate_windows_version(issue_files)

    if scilista_item is None:
        summary += html_reports.format_message('FATAL ERROR: ' + issue_models.issue.issue_label + ' will not be updated or published in the website.')
    else:
        summary += issue_files.copy_files_to_web()

    summary += html_reports.tag('h4', 'Resulting folders/files:')
    summary += html_reports.link('file:///' + issue_files.issue_path, issue_files.issue_path)
    summary += html_reports.tag('p', 'Finished.')

    return (scilista_item, text + summary)


def display_list(title, items):
    messages = []
    messages.append('\n<p>' + title + ': ' + str(len(items)) + '</p>')
    messages.append('<ul>' + '\n'.join(['<li>' + item + '</li>' for item in items]) + '</ul>')
    return '\n'.join(messages)


def validate_xml_issue_data(issue_models, article):
    msg = []
    if article is not None:

        # issue date
        if article.issue_pub_dateiso != issue_models.issue.dateiso:
            msg.append(html_reports.tag('h5', 'publication date'))
            msg.append('ERROR: Invalid value of publication date: ' + article.issue_pub_dateiso + '. Expected value: ' + issue_models.issue.dateiso)

        # section
        msg.append(html_reports.tag('h5', 'section'))
        msg.append('section: ' + article.toc_section + '.')
        section_code, matched_rate, most_similar = issue_models.most_similar_section_code(article.toc_section)
        if matched_rate != 1:
            msg.append('Registered sections:\n' + '; '.join(issue_models.section_titles))
            if section_code is None:
                if not article.is_ahead:
                    msg.append('ERROR: ' + article.toc_section + ' is not a registered section.')
            else:
                msg.append('WARNING: section replaced: "' + most_similar + '" (instead of "' + article.toc_section + '")')

        # @article-type
        msg.append(html_reports.tag('h5', 'article-type'))
        msg.append('@article-type: ' + article.article_type)
        if most_similar is not None:
            section_title = most_similar
        else:
            section_title = article.toc_section
        rate = compare_article_type_and_section(section_title, article.article_type)
        if rate < 0.5:
            msg.append('WARNING: Check if ' + article.article_type + ' is a valid value for @article-type.')

    msg = ''.join([html_reports.format_message(item) for item in msg])
    return (section_code, msg)


def compare_article_type_and_section(article_section, article_type):
    rate = 0
    max_rate = 0
    for type_item in article_type.split('-'):
        for part_item in article_section.lower():
            rate = article_utils.how_similar(type_item, part_item)
            if rate > max_rate:
                max_rate = rate
    return max_rate


def download_packages(ftp, ftp_dir, download_path):
    files = []
    log = ''
    if ftp is not None:
        if ftp_dir is not None and download_path is not None:
            if not os.path.isdir(download_path):
                os.makedirs(download_path)
            files = ftp.download_files(download_path, ftp_dir)
            log = ftp.registered_actions()
    return (files, log)


def send_email(email, email_to, email_subject, email_header, message):
    if os.path.isfile(email_header):
        email_header = open(email_header, 'r').read()
    if email_header is None:
        email_header = ''
    print([email_to, email_subject, email_header + message])
    email.send(email_to, email_subject, email_header + message)


def queue_packages(download_path, temp_path, queue_path, archive_path):
    invalid_pkg_files = []
    proc_id = datetime.now().isoformat()[11:16].replace(':', '')
    temp_path = temp_path + '/' + proc_id
    queue_path = queue_path + '/' + proc_id
    pkg_paths = []

    if not os.path.isdir(archive_path):
        os.makedirs(archive_path)

    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)

    for pkg_name in os.listdir(download_path):
        if is_valid_pkg_file(download_path + '/' + pkg_name):
            shutil.copyfile(download_path + '/' + pkg_name, temp_path + '/' + pkg_name)
        else:
            pkg_paths.append(pkg_name)
        fs_utils.delete_file_or_folder(download_path + '/' + pkg_name)

    for pkg_name in os.listdir(temp_path):
        queued_pkg_path = queue_path + '/' + pkg_name
        if not os.path.isdir(queued_pkg_path):
            os.makedirs(queued_pkg_path)

        if fs_utils.extract_package(temp_path + '/' + pkg_name, queued_pkg_path):
            shutil.copyfile(temp_path + '/' + pkg_name, archive_path + '/' + pkg_name)
            pkg_paths.append(queued_pkg_path)
        else:
            invalid_pkg_files.append(pkg_name)
            fs_utils.delete_file_or_folder(queued_pkg_path)
        fs_utils.delete_file_or_folder(temp_path + '/' + pkg_name)
    fs_utils.delete_file_or_folder(temp_path)

    return (pkg_paths, invalid_pkg_files)


def find_xml_source_paths(path):
    r = []
    if os.path.isdir(path):
        files = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f) and f.endswith('.xml')]
        folders = [f for f in os.listdir(path) if os.path.isdir(path + '/' + f)]

        if len(folders) > 0:
            for item in folders:
                r += find_xml_source_paths(path + '/' + item)
        elif len(files) > 0:
            r.append(path)
    return r


def run_remote_mkdirs(user, server, path):
    os.system('ssh ' + user + '@' + server + ' "mkdir -p ' + path + '"')


def run_rsync(source, user, server, dest):
    os.system('nohup rsync -CrvK ' + source + '/* ' + user + '@' + server + ':' + dest + '&')


def transfer_website_files(acron, issue_id, website_folders_path, user, server, destination):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    issue_id_path = acron + '/' + issue_id

    folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']

    for folder in folders:
        dest_path = destination + folder + issue_id_path
        source_path = website_folders_path + folder + issue_id_path
        run_remote_mkdirs(user, server, dest_path)
        run_rsync(source_path, user, server, dest_path)


def transfer_website_bases(bases_path, user, server, dest_path):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    folders = ['artigo', 'issue', 'newissue', 'title']

    for folder in folders:
        run_remote_mkdirs(user, server, dest_path)
        run_rsync(bases_path + '/' + folder, user, server, dest_path)


def gera_padrao_command(proc_path, gerapadrao_status_filename):
    return 'cd ' + proc_path + ';./GeraPadrao.bat;echo FINISHED> ' + gerapadrao_status_filename


def gera_padrao(gerapadrao_status_filename, source_path, col_scilista, proc_serial_path, proc_path):
    status = open(gerapadrao_status_filename, 'r').read()
    path = os.path.dirname(gerapadrao_status_filename)

    if 'FINISHED' in status:
        gerapadrao_cmd = gera_padrao_command(proc_path, gerapadrao_status_filename)
        open(gerapadrao_status_filename, 'w').write('RUNNING')

        for item in ['title', 'issue']:
            for ext in ['.mst', '.xrf']:
                if os.path.isfile(source_path + '/' + item + '/' + item + ext):
                    if not os.path.isdir(proc_serial_path + '/' + item):
                        os.makedirs(proc_serial_path + '/' + item)
                    shutil.copyfile(source_path + '/' + item + '/' + item + ext, proc_serial_path + '/' + item + '/' + item + ext)

        scilista_items = list(set([f.strip() for f in open(col_scilista, 'r').readlines()]))
        if len(scilista_items) > 0:
            fs_utils.delete_file_or_folder(col_scilista)
            sorted_scilista_items = [f for f in scilista_items if ' pr' in f] + [f for f in scilista_items if not ' pr' in f]

            proc_scilista = proc_serial_path + '/scilista.lst'
            open(proc_scilista, 'w').write('\n'.join(sorted_scilista_items))

            now = datetime.now().isoformat()[11:16].replace(':', '')

            open(path + '/' + now, 'w').write(datetime.now().isoformat())
            os.system(gerapadrao_cmd)
            open(path + '/' + now, 'a+').write(datetime.now().isoformat())


def xml_converter_read_configuration(filename):
    r = None
    if os.path.isfile(filename):
        r = xmlcvrter_cfg.XMLConverterConfiguration(filename)
        if not r.valid():
            r = None
    return r


def xml_converter_get_inputs(args):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    package_path = None
    script = None
    collection_acron = None
    if len(args) == 2:
        script, param = args
        if os.path.isfile(param) or os.path.isdir(param):
            package_path = param
        else:
            collection_acron = param

    return (script, package_path, collection_acron)


def xml_converter_validate_inputs(package_path, collection_acron):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    messages = []
    errors = []
    if package_path is None:
        if collection_acron is None:
            errors.append('Missing collection acronym')
    else:
        errors = xml_utils.is_valid_xml_path(package_path)
    return errors


def xml_config_filename(collection_acron):
    filename = configuration_filename = CURRENT_PATH + '/../../scielo_paths.ini'

    if not os.path.isfile(filename):
        if not collection_acron is None:
            filename = CURRENT_PATH + '/../config/' + collection_acron + '.xc.ini'
    return filename


def is_valid_configuration_file(configuration_filename):
    messages = []
    if configuration_filename is None:
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: No configuration file was informed')
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: unable to read XML Converter configuration file: ' + configuration_filename)
    return messages


def is_valid_pkg_file(filename):
    return os.path.isfile(filename) and (filename.endswith('.zip') or filename.endswith('.tgz'))


def update_issue_copy(issue_db, issue_db_copy):
    d = os.path.dirname(issue_db_copy)
    if not os.path.isdir(d):
        os.makedirs(d)
    if not os.path.isfile(issue_db_copy + '.fst'):
        shutil.copyfile(CURRENT_PATH + '/issue.fst', issue_db_copy + '.fst')
    if open(CURRENT_PATH + '/issue.fst', 'r').read() != open(issue_db_copy + '.fst', 'r').read():
        shutil.copyfile(CURRENT_PATH + '/issue.fst', issue_db_copy + '.fst')
    shutil.copyfile(issue_db + '.mst', issue_db_copy + '.mst')
    shutil.copyfile(issue_db + '.xrf', issue_db_copy + '.xrf')


def call_download_packages(config, email):
    package_paths = []
    ftp = ftp_service.FTPService(config.data('FTP_SERVER'), config.data('FTP_USER'), config.data('FTP_PSWD'))

    files, messages = download_packages(ftp, config.data('FTP_DIR'), config.data('DOWNLOAD_PATH'))

    queue_path, invalid_pkg_files = queue_packages(config.data('DOWNLOAD_PATH'), config.data('TEMP_PATH'), config.data('QUEUE_PATH'), config.data('ARCHIVE_PATH'))
    if len(invalid_pkg_files) > 0:
        send_email(email, config.data('EMAIL_TO'), config.data('EMAIL_SUBJECT_NOT_PROCESSED'), CONFIG_PATH + '/' + config.data('EMAIL_HEADER_NOT_PROCESSED'), '\n'.join(invalid_pkg_files))
    if os.path.isdir(queue_path):
        package_paths = [queue_path + '/' + item for item in os.listdir(queue_path) if item.endswith('.zip') or item.endswith('.tgz')]
    if len(package_paths) == 0:
        package_paths = None

    return package_paths


def call_converter(args, version='1.0'):
    script, package_path, collection_acron = xml_converter_get_inputs(args)
    if package_path is None and collection_acron is None:
        # GUI
        import xml_gui
        xml_gui.open_main_window(True, None)

    elif package_path is not None and collection_acron is not None:
        errors = xml_converter_validate_inputs(package_path, collection_acron)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ATTENTION =====\n')
            messages.append('ERROR: Incorrect parameters')
            messages.append('\nUsages:')
            messages.append('python xml_converter.py <xml_folder> | <collection_acron>')
            messages.append('where:')
            messages.append('  <xml_folder> = path of folder which contains')
            messages.append('  <collection_acron> = collection acron')

            messages.append('\n'.join(errors))
            print('\n'.join(messages))
        else:
            execute_converter(package_path, collection_acron)
    elif collection_acron is not None:
        execute_converter(package_path, collection_acron)


def execute_converter(package_path, collection_name=None):
    #collection_names = {'Brasil': 'scl', u'Salud Pública': 'spa'}
    collection_names = {}
    collection_acron = collection_names.get(collection_name)
    configuration_filename = xml_config_filename(collection_acron)
    error = is_valid_configuration_file(configuration_filename)
    if len(error) > 0:
        print('\n'.join(error))
    else:
        config = xml_converter_read_configuration(configuration_filename)
        prepare_converter(config)
        invalid_pkg_files = []
        scilista = []
        if package_path is None:
            package_paths, invalid_pkg_files = queue_packages(config.download_path, config.temp_path, config.queue_path, config.archive_path)
            #FIXME
            #if len(invalid_pkg_files) > 0:
            #    send_email(email, config.data('EMAIL_TO'), config.data('EMAIL_SUBJECT_NOT_PROCESSED'), CONFIG_PATH + '/' + config.data('EMAIL_HEADER_NOT_PROCESSED'), '\n'.join(invalid_pkg_files))
        if package_path is None:
            package_path = []
        if not isinstance(package_path, list):
            package_paths = [package_path]

        for package_path in package_paths:
            try:
                report_filename, report_path, scilista_item = convert_package(package_path)
            except Exception as e:
                invalid_pkg_files.append(os.path.basename(package_path))
                report_filename, report_path, scilista_item = [None, None, None]
            if scilista_item is not None:
                scilista.append(scilista_item)
                #email result
        if len(invalid_pkg_files) > 0:
            #email invalid packages

        if len(scilista) > 0:
            open(config.scilista_path, 'a+').write('\n'.join(scilista))
        print('finished')


def prepare_converter(config):
    global converter_env

    if converter_env is None:
        converter_env = ConverterEnv()

    converter_env.db_isis = isis.IsisDAO(isis.UCISIS(isis.CISIS(config.cisis1030), isis.CISIS(config.cisis1660)))

    update_issue_copy(config.issue_db, config.issue_db_copy)
    converter_env.db_isis.update_indexes(config.issue_db_copy, config.issue_db_copy + '.fst')
    converter_env.db_issue = serial_files.IssueDAO(converter_env.db_isis, config.issue_db_copy)

    converter_env.db_article = serial_files.ArticleDAO(converter_env.db_isis)

    converter_env.website_folders_path = config.website_folders_path
    converter_env.serial_path = config.serial_path
    converter_env.version = '1.0'
    converter_env.is_windows = config.is_windows
    #converter_env.email_service = 
