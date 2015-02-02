# coding=utf-8

import os
import shutil
from datetime import datetime

from isis_models import IssueRecord
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


def get_issue(issue_data, db_issue):
    #print(issue_data)
    issue_label, p_issn, e_issn = issue_data
    i_record = None
    issue_record = None
    msg = None

    if issue_label is None:
        issue_label = 'UNKNOWN'
    else:
        i_record = get_i_record(db_issue, issue_label, p_issn, e_issn)

    if i_record is None:
        if issue_label == 'UNKNOWN':
            msg = html_reports.format_message('FATAL ERROR: Unable to identify the article\'s issue')
        else:
            msg = html_reports.format_message('FATAL ERROR: Issue ' + issue_label + ' is not registered in ' + db_issue.db_filename + '. (' + '/'.join([i for i in [p_issn, e_issn] if i is not None]) + ')')
    else:
        issue_record = IssueRecord(i_record)

    return (issue_record, msg)


def convert_package(serial_path, pkg_path, report_path, website_folders_path, db_issue, db_ahead, db_article, version):
    old_report_path = report_path
    scilista_item = None
    label = 'acron issue'
    issue_record = None
    dtd_files = xml_versions.DTDFiles('scielo', version)
    validate_order = True
    do_toc_report = True

    xml_filenames = sorted([pkg_path + '/' + f for f in os.listdir(pkg_path) if f.endswith('.xml') and not 'incorrect' in f])

    package_info = pkg_reports.get_package_info(xml_filenames, report_path)
    issue_data = pkg_reports.issue_in_package(package_info)

    toc_stats_and_report = pkg_reports.validate_toc(package_info, validate_order)
    toc_f, toc_e, toc_w, toc_report = toc_stats_and_report

    articles_stats, articles_reports, articles_sheets = pkg_reports.validate_articles(package_info, dtd_files, validate_order, False)

    validations_report = pkg_reports.package_validations_reports_text(articles_stats, articles_reports, articles_sheets, toc_stats_and_report, do_toc_report)

    issue_record, issue_error_msg = get_issue(issue_data, db_issue)
    issue_label = issue_data[0]

    conversion_report = ''

    if toc_f > 0:
        validations_report += html_reports.format_message('FATAL ERROR: Unable to create "base" because of fatal errors in the Table of Contents data.')

    issue = None
    if not issue_record is None:
        issue = issue_record.issue

    if issue is None:
        validations_report += issue_error_msg
    else:
        issue_label = issue.issue_label
        journal_files = serial_files.JournalFiles(serial_path, issue.acron)
        scilista_item = issue.acron + ' ' + issue_label
        label = scilista_item
        ahead_manager = serial_files.AheadManager(db_ahead, journal_files, db_issue, issue.issn_id)
        issue_files = serial_files.IssueFiles(journal_files, issue_label, pkg_path, website_folders_path)
        issue_files.move_reports(report_path)
        issue_files.save_source_files(pkg_path)
        report_path = issue_files.base_reports_path

        conversion_validation_result = check_data(ahead_manager, articles, issue_record)
        conversion_report = convert_articles(ahead_manager, db_article, issue_files, issue_record.record, articles, articles_stats, conversion_validation_result)

    filename = report_path + '/xml_converter.html'
    texts = []
    texts.append(pkg_reports.xml_list(pkg_path, xml_filenames))
    texts.append(validations_report)
    texts.append(conversion_report)
    texts.append(pkg_reports.processing_result_location(report_path))

    content = html_reports.join_texts(texts)

    if old_report_path in content:
        content = html_reports.get_unicode(content)
        content = content.replace(html_reports.get_unicode(old_report_path), html_reports.get_unicode(report_path))
    if isinstance(content, unicode):
        content = content.encode('utf-8')
    pkg_reports.save_report(filename, ['XML Conversion (XML to Database)', label], content)
    pkg_reports.display_report(filename)

    return (filename, report_path, scilista_item)


def check_data(ahead_manager, articles, issue_record):
    print('\nMatching articles and issue data...')
    n = '/' + str(len(articles))
    index = 0
    result = {}
    for xml_name, article in articles.items():
        index += 1
        item_label = str(index) + n + ' - ' + xml_name
        print(item_label)

        valid_ahead, ahead_status, ahead_msg, ahead_comparison = ahead_manager.get_valid_ahead(article, xml_name)
        section_code, issue_validations_msg = validate_xml_issue_data(issue_record, article)

        msg = ''
        msg += html_reports.tag('h4', 'checking ex-ahead')
        msg += ''.join([html_reports.format_message(item) for item in ahead_msg])
        msg += ''.join([html_reports.tag('pre', item) for item in ahead_comparison])
        msg += html_reports.tag('h4', 'checking issue data')
        msg += issue_validations_msg
        conv_f, conv_e, conv_w = html_reports.statistics_numbers(msg)

        result[xml_name] = (conv_f, conv_e, conv_w, msg, valid_ahead, ahead_status, section_code)
    return result


def convert_articles(ahead_manager, db_article, issue_files, i_record, articles, articles_stats, conversion_report):
    loaded = []

    articles_by_status = {}
    status_text = ['converted', 'not converted', 'first version', 'previous version (aop)', 'previous version (aop) unmatched', 'previous version (aop) without PID', 'previous version (aop) partially matched', ]
    order = ['converted', 'not converted', 'new', 'matched', 'unmatched', 'invalid', 'partially matched']

    for item in order:
        articles_by_status[item] = []

    n = '/' + str(len(articles))
    i = 0

    print('\nGenerating database')
    text = html_reports.tag('h3', 'XML Conversion')

    for xml_name, data in conversion_report.items():
        conv_f, conv_e, conv_w, conv_messages, valid_ahead, ahead_status, section_code = data
        xml_stats, data_stats = articles_stats[xml_name]
        xml_f, xml_e, xml_w = xml_stats
        data_f, data_e, data_w = data_stats
        article = articles[xml_name]

        i += 1
        item_label = str(i) + n + ' - ' + xml_name
        print(item_label)

        text += html_reports.tag('h4', item_label)

        articles_by_status[ahead_status].append(xml_name)

        article.section_code = section_code

        converted = False
        if conv_f + xml_f + data_f == 0:
            converted = convert_article(db_article, i_record, issue_files, xml_name, article, valid_ahead)

            if converted:
                if valid_ahead is not None:
                    if ahead_status in ['matched', 'partially matched']:
                        done, ahead_msg = ahead_manager.manage_ex_ahead(valid_ahead)
                        conv_messages += ''.join([item for item in ahead_msg])
                articles_by_status['converted'].append(xml_name)
                conv_messages += html_reports.format_message('OK: converted')
            else:
                articles_by_status['not converted'].append(xml_name)
                conv_messages += html_reports.format_message('FATAL ERROR: not converted')
                conv_f += 1
        title = html_reports.statistics_display(conv_f, conv_e, conv_w, True)
        text += html_reports.collapsible_block(xml_name + 'conv', title, conv_messages)

    summary = '#'*80
    i = 0
    for status in order:
        summary += display_list(status_text[i], articles_by_status[status])
        i += 1

    still_ahead = ahead_manager.finish_manage_ex_ahead()
    if len(still_ahead) > 0:
        still_ahead = [still_ahead[k][0] + still_ahead[k][1] + still_ahead[k][2] for k in sorted(still_ahead.keys(), reverse=True)]
        summary += display_list('ahead list', still_ahead)

    if len(loaded) > 0:
        _loaded = db_article.finish_conversion(i_record, issue_files)

        summary += html_reports.tag('h4', 'Resulting folders/files:')
        summary += html_reports.link('file:///' + issue_files.issue_path, issue_files.issue_path)

    if len(loaded) > 0:
        summary += issue_files.copy_files_to_web()
    summary += html_reports.tag('p', 'Finished.')

    return text + summary


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


def convert_article(db_article, i_record, issue_files, xml_name, article, ahead):
    r = False
    if article is not None:
        if ahead is not None:
            article._ahead_pid = ahead.ahead_pid
        article_files = serial_files.ArticleFiles(issue_files, article.order, xml_name)
        r = db_article.create_id_file(i_record, article, article_files)
    return r


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
                report_path = pkg_path + '_base_reports'
                converter_report, report_path, scilista_item = convert_package(config.serial_path, pkg_path, report_path, config.website_folders_path, issue_dao, isis_dao, article_dao, version)
                messages.append('*'*80)

                if scilista_item is not None:
                    scilista_items.append(scilista_item)

                    if email is not None:
                        email_text = open(converter_report, 'r').read()
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
