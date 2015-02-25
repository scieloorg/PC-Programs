# coding=utf-8

import os
import shutil
from datetime import datetime

from isis_models import IssueRecord, ArticleRecords2Article
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
import xpmaker


converter_report_lines = []
CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')
CONFIG_PATH = CURRENT_PATH + '/../config/'


def register_log(message):
    if not '<' in message:
        message = html_reports.format_message(message)
    converter_report_lines.append(message)


def get_i_record(db_issue, issue_label, print_issn, e_issn):
    i_record = None
    issues_records = db_issue.search(issue_label, print_issn, e_issn)
    if len(issues_records) > 0:
        i_record = issues_records[0]
    return i_record


def get_issue_record(issue_label, p_issn, e_issn, db_issue):
    #print(issue_data)

    i_record = None
    issue_record = None
    msg = None

    if issue_label is None:
        msg = html_reports.format_message('FATAL ERROR: Unable to identify the article\'s issue')
    else:
        i_record = get_i_record(db_issue, issue_label, p_issn, e_issn)

        if i_record is None:
            msg = html_reports.format_message('FATAL ERROR: Issue ' + issue_label + ' is not registered in ' + db_issue.db_filename + '. (' + '/'.join([i for i in [p_issn, e_issn] if i is not None]) + ')')
        else:
            issue_record = IssueRecord(i_record)

    return (issue_record, msg)


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

    for name in os.listdir(whole_pkg_path):
        os.unlink(whole_pkg_path + '/' + name)

    return (new, update, xpmaker.get_articles(whole_pkg_path))


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


def convert_package(serial_path, src_path, website_folders_path, db_issue, db_ahead, db_article, version):
    display_title = False
    validate_order = True
    dtd_files = xml_versions.DTDFiles('scielo', version)
    conversion_report = ''
    msg = []

    result_path = src_path + '_xml_converter_result'
    wrk_path = result_path + '/work'
    pkg_path = result_path + '/scielo_package'
    report_path = result_path + '/errors'

    old_report_path = report_path
    acron_issue_label = 'acron issue label'
    xml_filenames = sorted([src_path + '/' + f for f in os.listdir(src_path) if f.endswith('.xml') and not 'incorrect' in f])
    scilista_item = None
    # normaliza os arquivos xml

    result_path = os.path.dirname(src_path)
    pkg_items = xpmaker.make_package(xml_filenames, report_path, wrk_path, pkg_path, version, 'acron')

    issue_label, p_issn, e_issn = xpmaker.package_issue(pkg_items)
    issue_record, issue_error_msg = get_issue_record(issue_label, p_issn, e_issn, db_issue)

    if issue_record is None:
        msg.append(issue_error_msg)
    else:
        issue = issue_record.issue
        journal_files = serial_files.JournalFiles(serial_path, issue.acron)
        issue_files = serial_files.IssueFiles(journal_files, issue.issue_label, pkg_path, website_folders_path)
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

            ahead_manager = serial_files.AheadManager(db_ahead, journal_files, db_issue, issue.issn_id)
            articles = {doc_file_info.xml_name: article for article, doc_file_info in pkg_items}
            scilista_item, conversion_report = convert_articles(ahead_manager, db_article, issue_files, issue_record, articles, articles_stats, inconsistent_orders)
            if scilista_item is not None:
                acron_issue_label = scilista_item

    filename = report_path + '/xml_converter.html'
    texts = []
    texts.append(pkg_reports.xml_list(pkg_path, xml_filenames))
    texts.append(html_reports.join_texts(msg))
    texts.append(conversion_report)
    texts.append(pkg_reports.processing_result_location(result_path))

    content = html_reports.join_texts(texts)

    if old_report_path in content:
        content = html_reports.get_unicode(content)
        content = content.replace(html_reports.get_unicode(old_report_path), html_reports.get_unicode(report_path))

    pkg_reports.save_report(filename, ['XML Conversion (XML to Database)', acron_issue_label], content)
    pkg_reports.display_report(filename)

    return (filename, report_path, scilista_item)


def convert_articles(ahead_manager, db_article, issue_files, issue_record, articles, articles_stats, inconsistent_orders):
    index = 0
    status_text = ['converted', 'not converted', 'first version', 'previous version (aop)', 'previous version (aop) unmatched', 'previous version (aop) without PID', 'previous version (aop) partially matched', ]
    order = ['converted', 'not converted', 'new', 'matched', 'unmatched', 'invalid', 'partially matched']

    articles_by_status = {}
    for k in order:
        articles_by_status[k] = []

    ex_ahead = 0
    article_id_created = 0
    n = '/' + str(len(articles))

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

        section_code, issue_validations_msg = validate_xml_issue_data(issue_record, article)

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

            done = db_article.create_id_file(issue_record.record, article, article_files, creation_date)
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
        if db_article.finish_conversion(issue_record.record, issue_files):
            scilista_item = issue_record.issue.acron + ' ' + issue_record.issue.issue_label

    if scilista_item:
        summary += issue_files.copy_files_to_web()
    else:
        summary += html_reports.format_message('FATAL ERROR: ' + issue_record.issue.issue_label + ' will not be updated or published in the website.')

    summary += html_reports.tag('h4', 'Resulting folders/files:')
    summary += html_reports.link('file:///' + issue_files.issue_path, issue_files.issue_path)
    summary += html_reports.tag('p', 'Finished.')

    return (scilista_item, text + summary)


def display_list(title, items):
    messages = []
    messages.append('\n<p>' + title + ': ' + str(len(items)) + '</p>')
    messages.append('<ul>' + '\n'.join(['<li>' + item + '</li>' for item in items]) + '</ul>')
    return '\n'.join(messages)


def validate_xml_issue_data(issue_record, article):
    msg = []
    if article is not None:

        # issue date
        if article.issue_pub_dateiso != issue_record.issue.dateiso:
            msg.append(html_reports.tag('h5', 'publication date'))
            msg.append('ERROR: Invalid value of publication date: ' + article.issue_pub_dateiso + '. Expected value: ' + issue_record.issue.dateiso)

        # section
        msg.append(html_reports.tag('h5', 'section'))
        msg.append('section: ' + article.toc_section + '.')
        section_code, matched_rate, most_similar = issue_record.most_similar_section_code(article.toc_section)
        if matched_rate != 1:
            msg.append('Registered sections:\n' + '; '.join(issue_record.section_titles))
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

    if not os.path.isdir(archive_path):
        os.makedirs(archive_path)

    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)

    for pkg_file in os.listdir(download_path):
        if is_valid_pkg_file(download_path + '/' + pkg_file):
            shutil.copyfile(download_path + '/' + pkg_file, temp_path + '/' + pkg_file)
        fs_utils.delete_file_or_folder(download_path + '/' + pkg_file)

    for pkg_file in os.listdir(temp_path):
        if is_valid_pkg_file(temp_path + '/' + pkg_file):
            pkg_name = os.path.basename(pkg_file)
            queue_pkg_path = queue_path + '/' + pkg_name
            if not os.path.isdir(queue_pkg_path):
                os.makedirs(queue_pkg_path)

            if fs_utils.extract_package(temp_path + '/' + pkg_file, queue_pkg_path):
                shutil.copyfile(temp_path + '/' + pkg_file, archive_path + '/' + pkg_file)
            else:
                invalid_pkg_files.append(pkg_file)
                fs_utils.delete_file_or_folder(queue_pkg_path)
            fs_utils.delete_file_or_folder(temp_path + '/' + pkg_file)
        else:
            invalid_pkg_files.append(pkg_file)
            if os.path.isfile(temp_path + '/' + pkg_file):
                fs_utils.delete_file_or_folder(temp_path + '/' + pkg_file)
    fs_utils.delete_file_or_folder(temp_path)

    return (queue_path, invalid_pkg_files)


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


def xml_converter_read_inputs(args):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    messages = []
    package_paths = None
    script = None
    param = None

    if len(args) == 2:
        script, param = args
        if os.path.isdir(param):
            param = param.replace('\\', '/')
            if os.path.isdir(param):
                package_paths = find_xml_source_paths(param)
            configuration_filename = CURRENT_PATH + '/../../scielo_paths.ini'

        else:
            configuration_filename = CURRENT_PATH + '/../config/' + param + '.xmlproc.ini'

        if not os.path.isfile(configuration_filename):
            messages.append('\n===== ATTENTION =====\n')
            messages.append('ERROR: unable to read XML Converter configuration file: ' + configuration_filename)
            param = None

    if param is None:
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsages:')
        messages.append('python xml_converter.py <xml_folder>')
        messages.append('where:')
        messages.append('  <xml_folder> = path of folder which contains')
        messages.append('or')
        messages.append('python xml_converter.py <collection_acron>')
        messages.append('where:')
        messages.append('  <collection_acron> = collection acron')

    else:
        if package_paths is not None:
            if len(package_paths) == 0:
                messages.append('ERROR: Missing <xml folder>')
    error_messages = '\n'.join(messages)

    return (package_paths, configuration_filename, error_messages)


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
    messages = []
    package_paths, configuration_filename, error_messages = xml_converter_read_inputs(args)
    if len(error_messages) > 0:
        messages.append(error_messages)
    else:
        config = xml_converter_read_configuration(configuration_filename)

        isis_dao = isis.IsisDAO(isis.UCISIS(isis.CISIS(config.cisis1030), isis.CISIS(config.cisis1660)))

        update_issue_copy(config.issue_db, config.issue_db_copy)
        isis_dao.update_indexes(config.issue_db_copy, config.issue_db_copy + '.fst')
        issue_dao = serial_files.IssueDAO(isis_dao, config.issue_db_copy)

        article_dao = serial_files.ArticleDAO(isis_dao)

        email = None
        email_header = ''
        if config.data('EMAIL_SERVICE') == 'on':
            email = email_service.EmailService(config.data('SENDER_NAME'), config.data('SENDER_EMAIL'))
            if os.path.isfile(CONFIG_PATH + '/' + config.data('EMAIL_HEADER')):
                email_header = open(CONFIG_PATH + '/' + config.data('EMAIL_HEADER'), 'r').read()

        if package_paths is None:
            package_paths = call_download_packages(config, email)

        print(package_paths)
        if package_paths is not None:
            scilista_items = []
            for pkg_path in package_paths:
                pkg_name = os.path.basename(pkg_path)
                messages.append('*'*80)
                messages.append(pkg_name + '\n')
                report_filename, report_path, scilista_item = convert_package(config.serial_path, pkg_path, config.website_folders_path, issue_dao, isis_dao, article_dao, version)
                messages.append('*'*80)

                if scilista_item is not None:
                    scilista_items.append(scilista_item)

                    if email is not None:
                        email_text = open(report_filename, 'r').read()
                        email.send(config.data('EMAIL_TO'), config.data('EMAIL_SUBJECT') + ' ' + pkg_name, email_header + email_text, attaches=[report_path + '/' + f for f in os.listdir(report_path)])
            if config.data('COL_SCILISTA') is not None and len(scilista_items) > 0:
                if not os.path.isdir(os.path.dirname(config.data('COL_SCILISTA'))):
                    os.makedirs(os.path.dirname(config.data('COL_SCILISTA')))
                open(config.data('COL_SCILISTA'), 'a+').write('\n'.join(scilista_items))

            if len(scilista_items) > 0:
                if config.data('GERAPADRAO_PROC_PATH') is not None:
                    gera_padrao(config.data('GERAPADRAO_STATUS'), config.data('SOURCE_PATH'), config.data('COL_SCILISTA'), config.serial_path, config.data('GERAPADRAO_PROC_PATH'))
                    if email is not None:
                        email_header = open(CONFIG_PATH + '/' + config.data('EMAIL_HEADER_GERAPADRAO'), 'r').read()
                        email_text = '\n'.join(scilista_items)
                        email.send(config.data('EMAIL_TO'), config.data('EMAIL_SUBJECT_GERAPADRAO'), email_header + email_text)

                if config.data('TRANSFER_DESTINATION') is not None:
                    transfer_website_bases(config.website_folders_path + '/bases', config.data('TRANSFER_USER'), config.data('TRANSFER_SERVER'), config.data('TRANSFER_DESTINATION') + '/bases')

                    for scilista_item in scilista_items:
                        acron, issue_id = scilista_item.split(' ')
                        if os.path.isdir(config.website_folders_path):
                            transfer_website_files(acron, issue_id, config.website_folders_path, config.data('TRANSFER_USER'), config.data('TRANSFER_SERVER'), config.data('TRANSFER_DESTINATION'))
    print('\n'.join(messages))
