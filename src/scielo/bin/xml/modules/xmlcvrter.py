# coding=utf-8

import os
import shutil
import tempfile
from datetime import datetime

from isis_models import IssueRecord
import ftp_service
import email_service
import files_extractor
import serial_files
import reports
import pkg_checker
import xml_versions
import isis
import xmlcvrter_cfg
import article_utils

html_report = reports.ReportHTML()
converter_report_lines = []
CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')
CONFIG_PATH = CURRENT_PATH + '/../config/'


def register_log(message):
    if not '<' in message:
        message = html_report.format_message(message)
    converter_report_lines.append(message)


def extract_package(pkg_file, pkg_work_path):
    """
    Extract files to pkg_work_path from compressed files that are in compressed_path
    """
    r = False

    if os.path.isfile(pkg_file):
        if files_extractor.is_compressed_file(pkg_file):
            if not os.path.exists(pkg_work_path):
                os.makedirs(pkg_work_path)
            # delete content of destination path
            if os.path.exists(pkg_work_path):
                for item in os.listdir(pkg_work_path):
                    delete_item(pkg_work_path + '/' + item)
            # create tempdir
            temp_dir = tempfile.mkdtemp().replace('\\', '/')

            # extract in tempdir
            if files_extractor.extract_file(pkg_file, temp_dir):
                # eliminate folders
                for item in os.listdir(temp_dir):
                    _file = temp_dir + '/' + item
                    if os.path.isfile(_file):
                        shutil.copyfile(_file, pkg_work_path + '/' + item)
                        delete_item(_file)
                    elif os.path.isdir(_file):
                        for f in os.listdir(_file):
                            if os.path.isfile(_file + '/' + f):
                                shutil.copyfile(_file + '/' + f, pkg_work_path + '/' + f)
                                delete_item(_file + '/' + f)
                        shutil.rmtree(_file)
                shutil.rmtree(temp_dir)
                r = True
    return r


def get_i_record(db_issue, issue_label, print_issn, e_issn):
    i_record = None
    issues_records = db_issue.search(issue_label, print_issn, e_issn)
    if len(issues_records) > 0:
        i_record = issues_records[0]
    return i_record


def get_issue(issue_data, db_issue):
    print(issue_data)
    issue_label, p_issn, e_issn = issue_data
    i_record = None
    issue_record = None
    msg = None

    if issue_label is None:
        issue_label = 'UNKNOWN'
    else:
        i_record = get_i_record(db_issue, issue_label, p_issn, e_issn)
    print(i_record)
    if i_record is None:
        if issue_label == 'UNKNOWN':
            msg = html_report.format_message('FATAL ERROR: Unable to identify the article\'s issue')
        else:
            msg = html_report.format_message('FATAL ERROR: Issue ' + issue_label + ' is not registered in ' + db_issue.db_filename + '. (' + '/'.join([i for i in [p_issn, e_issn] if i is not None]) + ')')
    else:
        issue_record = IssueRecord(i_record)

    print(type(issue_record))
    return (issue_record, msg)


def convert_package(serial_path, pkg_path, report_path, website_folders_path, db_issue, db_ahead, db_article, version='1.0'):
    old_report_path = report_path
    scilista_item = None
    issue_record = None
    dtd_files = xml_versions.DTDFiles('scielo', version)

    xml_filenames = sorted([pkg_path + '/' + f for f in os.listdir(pkg_path) if f.endswith('.xml') and not 'incorrect' in f])
    doc_files_info_list = []
    for xml_filename in xml_filenames:
        doc_files_info = serial_files.DocumentFiles(xml_filename, report_path, None)
        doc_files_info.new_xml_filename = xml_filename
        doc_files_info_list.append(doc_files_info)

    validate_order = True
    do_toc_report = True

    articles, issue_data = pkg_checker.articles_and_issues(doc_files_info_list)

    issue_record, issue_error_msg = get_issue(issue_data, db_issue)
    issue_label = issue_data[0]

    toc_stats_and_report, articles_stats_and_reports, lists = pkg_checker.package_validations_data(articles, doc_files_info_list, dtd_files, report_path, validate_order, do_toc_report)

    toc_stats, toc_report = toc_stats_and_report
    toc_f, toc_e, toc_w = toc_stats

    conversion_report = ''
    validations_report = pkg_checker.package_validation_report_content(toc_stats_and_report, articles_stats_and_reports, lists)

    if toc_f > 0:
        validations_report += html_report.format_message('FATAL ERROR: Unable to create "base" because of fatal errors in the Table of Contents data.')

    issue = None
    if not issue_record is None:
        issue = issue_record.issue

    if issue is None:
        validations_report += issue_error_msg
    else:
        issue_label = issue.issue_label
        journal_files = serial_files.JournalFiles(serial_path, issue.acron)
        scilista_item = issue.acron + ' ' + issue_label
        ahead_manager = serial_files.AheadManager(db_ahead, journal_files, db_issue, issue.issn_id)
        issue_files = serial_files.IssueFiles(journal_files, issue_label, pkg_path, website_folders_path)
        issue_files.move_reports(report_path)
        issue_files.save_source_files(pkg_path)
        report_path = issue_files.base_reports_path

        summary, articles_conversion_result = convert_articles(ahead_manager, db_article, articles, articles_stats_and_reports, issue_record, issue_files)

        articles_conversion_results = ''.join([html_report.tag('h4', k) + item[1] for k, item in articles_conversion_result.items()])
        f, e, w = reports.statistics_numbers(articles_conversion_results)

        conversion_report = ''
        conversion_report += html_report.statistics_messages(f, e, w, 'conversion')
        conversion_report += articles_conversion_results
        conversion_report += summary

    filename = report_path + '/xml_converter.html'
    content = ''
    content += normalize_coding(pkg_checker.xml_list(pkg_path, xml_filenames))
    content += normalize_coding(validations_report)
    content += normalize_coding(conversion_report)
    content += normalize_coding(pkg_checker.processing_result_location(report_path))

    if old_report_path in content:
        content = content.replace(old_report_path, report_path)

    pkg_checker.save_report(filename, ['XML Conversion (XML to Database)', issue_label], content)
    pkg_checker.display_report(filename)

    return (filename, report_path, scilista_item)


def normalize_coding(text):
    if isinstance(text, str):
        text = text.decode('utf-8', 'xmlcharrefreplace')
    return text


def convert_articles(ahead_manager, db_article, articles, articles_stats_and_reports, issue_record, issue_files):
    total_new_doc = []
    total_ex_aop = []
    total_ex_aop_unmatched = []
    total_ex_aop_invalid = []
    total_ex_aop_partially = []
    not_loaded = []
    loaded = []

    i = 0
    summary = u''
    articles_conversion_result = {}
    for xml_name, article in articles.items():
        print(xml_name)
        i += 1
        xml_validation_result, data_validation_result = articles_stats_and_reports[xml_name]
        xml_stats, xml_validation_report = xml_validation_result
        data_stats, data_validation_report = data_validation_result

        valid_ahead, ahead_status, ahead_msg, ahead_comparison = ahead_manager.get_valid_ahead(article, xml_name)
        if valid_ahead is None:
            if ahead_status == 'new':
                total_new_doc.append(xml_name)
            elif ahead_status == 'unmatched':
                total_ex_aop_unmatched.append(xml_name)
            elif ahead_status == 'not valid':
                total_ex_aop_invalid.append(xml_name)
        else:
            total_ex_aop.append(xml_name)
            if ahead_status == 'partially matched':
                total_ex_aop_partially.append(xml_name)

        section_code, issue_validations_msg = validate_xml_issue_data(issue_record, article)
        article.section_code = section_code

        msg = u''
        msg += html_report.tag('h4', 'checking ex-ahead')
        msg += ''.join([html_report.format_message(item) for item in ahead_msg])
        msg += ''.join([html_report.tag('pre', item) for item in ahead_comparison])
        msg += html_report.tag('h4', 'checking issue data')
        msg += issue_validations_msg

        article.section_code = section_code

        f, e, w = pkg_checker.sum_stats([xml_stats, data_stats])
        conv_f, conv_e, conv_w = reports.statistics_numbers(msg)

        converted = False
        if f + conv_f == 0:
            converted = convert_article(db_article, issue_record.record, issue_files, xml_name, article, valid_ahead)

        msg += html_report.tag('h4', 'Conversion result')
        if converted:
            if valid_ahead is not None:
                done, msg = ahead_manager.manage_ex_ahead(valid_ahead)
                msg += ''.join([item for item in msg])
            loaded.append(xml_name)
            msg += '<p>converted</p>'
        else:
            not_loaded.append(xml_name)
            msg += html_report.format_message('FATAL ERROR: not converted')

        articles_conversion_result[xml_name] = ((conv_f, conv_e, conv_w), msg)

    summary += '#'*80
    summary += display_list('converted', loaded)
    summary += display_list('not converted', not_loaded)
    summary += display_list('new documents', total_new_doc)
    summary += display_list('previous version (ahead of print)', total_ex_aop)
    summary += display_list('previous version (ahead of print) partially matched', total_ex_aop_partially)
    summary += display_list('previous version (ahead of print) without PID', total_ex_aop_invalid)
    summary += display_list('previous version (ahead of print) unmatched', total_ex_aop_unmatched)

    still_ahead = ahead_manager.finish_manage_ex_ahead()
    if len(still_ahead) > 0:
        summary += display_list('ahead', still_ahead)

    if len(loaded) > 0:
        _loaded = db_article.finish_conversion(issue_record.record, issue_files)

        summary += html_report.tag('h4', 'Resulting folders/files:')
        summary += html_report.link('file:///' + issue_files.issue_path, issue_files.issue_path)

    if len(loaded) > 0:
        summary += issue_files.copy_files_to_web()
    summary += 'Finished.'
    return (summary, articles_conversion_result)


def display_list(title, items):
    messages = []
    messages.append('\n<p>' + title + ': ' + str(len(items)) + '</p>')
    messages.append('<ul>' + '\n'.join(['<li>' + item + '</li>' for item in items]) + '</ul>')
    return '\n'.join(messages)


def validate_xml_issue_data(issue_record, article):
    msg = []
    if article is not None:

        # issue date
        msg.append(html_report.tag('h5', 'publication date'))
        if article.issue_pub_dateiso != issue_record.issue.dateiso:
            msg.append('ERROR: Invalid value of publication date: ' + article.issue_pub_dateiso + '. Expected value: ' + issue_record.issue.dateiso)

        # section
        msg.append(html_report.tag('h5', 'section'))
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
        msg.append(html_report.tag('h5', 'article-type'))
        msg.append('@article-type: ' + article.article_type)
        if most_similar is not None:
            section_title = most_similar
        else:
            section_title = article.toc_section
        rate = compare_article_type_and_section(section_title, article.article_type)
        if rate < 0.5:
            msg.append('WARNING: Check if ' + article.article_type + ' is a valid value for @article-type.')

    msg = ''.join([html_report.format_message(item) for item in msg])
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


def delete_item(path):
    if os.path.isdir(path):
        for item in os.listdir(path):
            delete_item(path + '/' + item)
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.unlink(path)


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
        delete_item(download_path + '/' + pkg_file)

    for pkg_file in os.listdir(temp_path):
        if is_valid_pkg_file(temp_path + '/' + pkg_file):
            pkg_name = os.path.basename(pkg_file)
            queue_pkg_path = queue_path + '/' + pkg_name
            if not os.path.isdir(queue_pkg_path):
                os.makedirs(queue_pkg_path)

            if extract_package(temp_path + '/' + pkg_file, queue_pkg_path):
                shutil.copyfile(temp_path + '/' + pkg_file, archive_path + '/' + pkg_file)
            else:
                invalid_pkg_files.append(pkg_file)
                delete_item(queue_pkg_path)
            delete_item(temp_path + '/' + pkg_file)
        else:
            invalid_pkg_files.append(pkg_file)
            if os.path.isfile(temp_path + '/' + pkg_file):
                delete_item
    delete_item(temp_path)

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
            delete_item(col_scilista)
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
