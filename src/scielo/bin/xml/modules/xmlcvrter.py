# coding=utf-8

import os
import shutil
import tempfile
from datetime import datetime

from isis_models import IssueRecord
import ftp_service
import email_service
import file_extractor
import serial_files
import reports
import pkg_checker
import xml_versions
import isis
import xmlcvter_cfg


html_report = reports.ReportHTML()
converter_report_lines = []
CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')


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
        if file_extractor.is_compressed_file(pkg_file):
            if not os.path.exists(pkg_work_path):
                os.makedirs(pkg_work_path)
            # delete content of destination path
            if os.path.exists(pkg_work_path):
                for item in os.listdir(pkg_work_path):
                    os.unlink(pkg_work_path + '/' + item)
            # create tempdir
            temp_dir = tempfile.mkdtemp().replace('\\', '/')

            # extract in tempdir
            if file_extractor.extract_file(pkg_file, temp_dir):
                # eliminate folders
                for item in os.listdir(temp_dir):
                    _file = temp_dir + '/' + item
                    if os.path.isfile(_file):
                        shutil.move(_file, pkg_work_path)
                    elif os.path.isdir(_file):
                        for f in os.listdir(_file):
                            if os.path.isfile(_file + '/' + f):
                                shutil.move(_file + '/' + f, pkg_work_path)
                        shutil.rmtree(_file)
                shutil.rmtree(temp_dir)
                r = True
    return r


def get_valid_article(articles):
    a = None
    for xml_name, article in articles.items():
        if article is not None:
            issue_label = article.issue_label
            print('issue_label')
            print(issue_label)
            if issue_label is not None:
                a = article
                break
    return a


def get_issue_record(db_issue, article):
    issue_record = None
    issues_records = db_issue.search(article.issue_label, article.print_issn, article.e_issn)
    if len(issues_records) > 0:
        issue_record = issues_records[0]
    return issue_record


def convert_package(serial_path, xml_path, report_path, web_path, db_issue, db_ahead, db_article, version='1.0'):
    old_report_path = report_path
    scilista_item = None
    issue_record = None
    issue_label = 'UNKNOWN'
    doc_files_info_list = []
    xml_filenames = sorted([xml_path + '/' + f for f in os.listdir(xml_path) if f.endswith('.xml') and not 'incorrect' in f])

    register_log('<h2>XML files</h2>')
    register_log('XML path: ' + xml_path)
    register_log('Total of XML files: ' + str(len(xml_filenames)))
    register_log(html_report.format_list('', 'ol', [os.path.basename(f) for f in xml_filenames]))

    for xml_filename in xml_filenames:
        doc_files_info = serial_files.DocumentFiles(xml_filename, report_path, None)
        doc_files_info.new_xml_filename = xml_filename
        doc_files_info_list.append(doc_files_info)

    dtd_files = xml_versions.DTDFiles('scielo', version)
    issues, toc_results, articles, articles_stats, article_results = pkg_checker.validate_package(doc_files_info_list, dtd_files, report_path, True, True)

    toc_stats_numbers, toc_stats_report = toc_results
    toc_f, toc_e, toc_w = toc_stats_numbers

    register_log('<h2>XML/Data/TOC Validations</h2>')
    register_log(articles_stats)
    register_log(toc_stats_report)
    if toc_f + toc_e + toc_w > 0:
        register_log(html_report.link('file:///' + report_path + '/toc.html', 'toc.html'))
    register_log(html_report.link('file:///' + report_path + '/authors.html', 'authors.html'))
    register_log(html_report.link('file:///' + report_path + '/sources.html', 'sources.html'))

    if toc_f > 0:
        register_log('FATAL ERROR: Unable to create "base" because of fatal errors in the Table of Contents data.')
    else:
        article = get_valid_article(articles)

        if article is not None:
            issue_label = article.issue_label
            issue_record = get_issue_record(db_issue, article)

        if issue_record is None:
            if issue_label == 'UNKNOWN':
                register_log('FATAL ERROR: Unable to identify the article\'s issue')
            else:
                register_log('FATAL ERROR: Issue ' + issue_label + ' is not registered in ' + db_issue.db_filename + '. (' + '/'.join([i for i in [article.print_issn, article.e_issn] if i is not None]) + ')')
        else:
            #register_log('Issue: ' + issue_label + '.')
            issue_isis = IssueRecord(issue_record)
            issue = issue_isis.issue
            journal_files = serial_files.JournalFiles(serial_path, issue.acron)
            scilista_item = issue.acron + ' ' + issue_label
            ahead_manager = serial_files.AheadManager(db_ahead, journal_files, db_issue, issue.issn_id)
            issue_files = serial_files.IssueFiles(journal_files, issue_label, xml_path, web_path)
            issue_files.move_reports(report_path)
            issue_files.save_source_files(xml_path)
            report_path = issue_files.base_reports_path
            convert_articles(ahead_manager, db_article, articles, article_results, issue_record, issue_files)

    html_report.title = 'XML Conversion (XML to Database) - ' + issue_label
    content = '\n'.join(converter_report_lines)
    content = content.replace(old_report_path, report_path)
    html_report.body = stats(content) + content
    converter_report_filename = report_path + '/xml_converter_result.html'
    html_report.save(converter_report_filename)
    print('\n\nXML Converter report:\n ' + converter_report_filename)
    pkg_checker.display_report(converter_report_filename)
    print('\n\n-- end --')
    return (report_path, scilista_item)


def stats(content=None):
    if content is None:
        content = ''.join(converter_report_lines)
    f, e, w = reports.statistics_numbers(content)
    return html_report.statistics_messages(f, e, w, 'Results of XML Conversion (XML to Database)')


def convert_articles(ahead_manager, db_article, articles, article_results, issue_record, issue_files):
    total_new_doc = []
    total_ex_aop = []
    total_ex_aop_unmatched = []
    total_ex_aop_invalid = []
    total_ex_aop_partially = []
    not_loaded = []
    loaded = []

    register_log('<h2>XML to Database</h2>')
    for xml_name, article in articles.items():
        #(xml_stats, data_stats, result)
        xml_stats, data_stats, result = article_results[xml_name]

        register_log('.'*80)
        register_log(result)
        print(xml_name)

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

        f, e, w, issue_validations, section_code = validate_issue_data(issue_record, article)
        article.section_code = section_code

        register_log(html_report.statistics_messages(f, e, w, '<h4>converter validations</h4>'))

        register_log(html_report.tag('h4', 'checking ex-ahead'))
        register_log(''.join([html_report.format_message(item) for item in ahead_msg]))
        register_log(''.join([html_report.tag('pre', item) for item in ahead_comparison]))

        register_log(html_report.tag('h4', 'checking section'))
        register_log(issue_validations)

        if f + xml_stats[0] + data_stats[0] == 0:
            article.section_code = section_code
            converted = convert_article(db_article, issue_record, issue_files, xml_name, article, valid_ahead)
        else:
            converted = False
            register_log('FATAL ERROR: Unable to create "base" for ' + xml_name + ', because it has fatal errors.')

        register_log(html_report.tag('h4', 'Result'))
        if converted:
            if valid_ahead is not None:
                done, msg = ahead_manager.manage_ex_ahead(valid_ahead)
                for item in msg:
                    register_log(item)
            loaded.append(xml_name)
            register_log('Result: converted')
        else:
            not_loaded.append(xml_name)
            register_log('ERROR: not converted')

    register_log('#'*80)

    register_log(html_report.tag('h2', 'SUMMARY'))
    register_log(stats())
    register_log(html_report.tag('h4', 'Converted/Not converted'))

    register_log(display_list('converted', loaded))
    register_log(display_list('not converted', not_loaded))

    register_log(html_report.tag('h4', 'New/Ex-ahead'))
    register_log(display_list('new documents', total_new_doc))
    register_log(display_list('previous version (ahead of print)', total_ex_aop))
    register_log(display_list('previous version (ahead of print) partially matched', total_ex_aop_partially))
    register_log(display_list('previous version (ahead of print) without PID', total_ex_aop_invalid))
    register_log(display_list('previous version (ahead of print) unmatched', total_ex_aop_unmatched))

    still_ahead = ahead_manager.finish_manage_ex_ahead()
    if len(still_ahead) > 0:
        register_log(display_list('ahead', still_ahead))

    if len(loaded) > 0:
        _loaded = db_article.finish_conversion(issue_record, issue_files)

        register_log(html_report.tag('h4', 'Processing result'))
        register_log(html_report.link('file:///' + issue_files.issue_path, issue_files.issue_path))

    if len(loaded) > 0:
        register_log(issue_files.copy_files_to_web())
    register_log('end')


def display_list(title, items):
    messages = []
    messages.append('\n<p>' + title + ': ' + str(len(items)) + '</p>')
    messages.append('<ul>' + '\n'.join(['<li>' + item + '</li>' for item in items]) + '</ul>')
    return '\n'.join(messages)


def validate_issue_data(issue_record, article):
    f = 0
    e = 0
    w = 0
    msg = []
    if article is not None:
        section_code, matched_rate, similar_section_title = IssueRecord(issue_record).section_code(article.toc_section)
        if section_code is None:
            if not article.is_ahead:
                f += 1
                msg.append('ERROR: ' + article.toc_section + ' is not a registered section.')
                msg.append('Registered sections:\n' + '; '.join(IssueRecord(issue_record).section_titles))
        else:
            if matched_rate != 1:
                w += 1
                msg.append('WARNING: section replaced: "' + similar_section_title + '" (instead of "' + article.toc_section + '")')
            else:
                msg.append('section: ' + article.toc_section + '.')
        msg.append('@article-type: ' + article.article_type)

    msg = ''.join([html_report.format_message(item) for item in msg])
    return (f, e, w, msg, section_code)


def convert_article(db_article, issue_record, issue_files, xml_name, article, ahead):
    r = False
    if article is not None:
        if ahead is not None:
            article._ahead_pid = ahead.ahead_pid
        article_files = serial_files.ArticleFiles(issue_files, article.order, xml_name)
        r = db_article.create_id_file(issue_record, article, article_files)
    return r


def delete_folder(folder):
    if os.path.isdir(folder):
        for item in os.listdir(folder):
            if os.path.isfile(folder + '/' + item):
                os.unlink(folder + '/' + item)
            else:
                delete_folder(folder + '/' + item)
                shutil.rmtree(folder + '/' + item)


def execute_download_packages(ftp, ftp_dir, download_path, email, email_to, email_subject, email_header):
    r = []
    log = ''
    if ftp is not None:
        if ftp_dir is not None and download_path is not None:
            r = ftp.download_files(ftp_dir, download_path)
            log = ftp.registered_actions()
            if email is not None:
                email_header = ''
                if os.path.isfile(email_header):
                    email_header = open(email_header, 'r').read()
                email.send(email_to, email_subject, email_header + log)
    return (r, log)


def queue_packages(download_path, temp_path, queue_path, email, email_to, email_subject, email_header):
    invalid_pkg_files = []
    proc_id = datetime.now().isoformat()[5:10].replace('-', '')
    temp_path = temp_path + '/' + proc_id
    queue_path = queue_path + '/' + proc_id

    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)

    for pkg_file in os.listdir(download_path):
        shutil.move(download_path + '/' + pkg_file, temp_path)

    for pkg_file in os.listdir(temp_path):
        pkg_name = os.path.basename(pkg_file)
        pkg_path = queue_path + '/' + pkg_name
        os.makedirs(pkg_path)

        if not extract_package(temp_path + '/' + pkg_file, pkg_path):
            invalid_pkg_files.append(pkg_file)
            delete_folder(pkg_path)
        os.unlink(temp_path + '/' + pkg_file)
    delete_folder(temp_path)

    if len(invalid_pkg_files) > 0 and email is not None:
        email_header = ''
        if os.path.isfile(email_header):
            email_header = open(email_header, 'r').read()
        email.send(email_to, email_subject, email_header + '\n'.join(invalid_pkg_files))
    return queue_path


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


def xml_converter_read_configuration(filename):
    r = None
    if os.path.isfile(filename):
        r = xmlcvter_cfg.XMLConverterConfiguration(filename)
        if not r.valid():
            r = None
    return r


def xml_converter_read_inputs(args):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    messages = []
    xml_paths = None
    script = None
    param = None

    if len(args) == 2:
        script, param = args
        if os.path.isdir(param):
            param = param.replace('\\', '/')
            if os.path.isdir(param):
                xml_paths = find_xml_source_paths(param)
            configuration_filename = CURRENT_PATH + '/../../cfg/scielo_paths.ini'

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
        messages.append('python xml_converter <collection_acron>')
        messages.append('where:')
        messages.append('  <collection_acron> = collection acron')

    else:
        if xml_paths is not None:
            if len(xml_paths) == 0:
                messages.append('ERROR: Missing <xml folder>')
    error_messages = '\n'.join(messages)

    return (xml_paths, configuration_filename, error_messages)


def update_issue_copy(issue_db, issue_db_copy):
    d = os.path.dirname(issue_db_copy)
    if not os.path.isdir(d):
        os.makedirs(d)

    if open(CURRENT_PATH + '/issue.fst', 'r').read() != open(issue_db_copy + '.fst', 'r').read():
        shutil.copyfile(CURRENT_PATH + '/issue.fst', issue_db_copy + '.fst')
    shutil.copyfile(issue_db + '.mst', issue_db_copy + '.mst')
    shutil.copyfile(issue_db + '.xrf', issue_db_copy + '.xrf')


def call_converter(args, version='1.0'):
    messages = []
    xml_paths, configuration_filename, error_messages = xml_converter_read_inputs(args)
    if len(error_messages) > 0:
        messages.append(error_messages)
    else:
        config = xml_converter_read_configuration(configuration_filename)

        serial_path = config.serial_path
        web_path = config.serial_path

        isis_dao = isis.IsisDAO(isis.UCISIS(isis.CISIS(config.cisis1030), isis.CISIS(config.cisis1660)))

        update_issue_copy(config.issue_db, config.issue_db_copy)
        isis_dao.update_indexes(config.issue_db_copy, config.issue_db_copy + '.fst')
        issue_dao = serial_files.IssueDAO(isis_dao, config.issue_db_copy)

        article_dao = serial_files.ArticleDAO(isis_dao)

        email_header = ''
        if os.path.isfile(config.data.get('EMAIL_TEXT')):
            email_header = open(config.data.get('EMAIL_TEXT'), 'r').read()

        email = None
        if xml_paths is None:
            ftp = ftp_service.FTPService(config.data.get('FTP_SERVER'), config.data.get('FTP_USER'), config.data.get('FTP_PASSWORD'))
            if config.data.get('EMAIL_SERVICE') == 'on':
                email = email_service.EmailService(config.data.get('SENDER_NAME'), config.data.get('SENDER_EMAIL'))

            execute_download_packages(ftp, config.data.get('FTP_DIR'), config.data.get('DOWNLOAD_PATH'), email, config.data.get('EMAIL_TO'), config.data.get('EMAIL_SUBJECT_DOWNLOAD'), config.data.get('EMAIL_TEXT_DOWNLOAD'))
            queue_path = queue_packages(config.data.get('DOWNLOAD_PATH'), config.data.get('TEMP_PATH'), config.data.get('QUEUE_PATH'), email, config.data.get('EMAIL_TO'), config.data.get('EMAIL_SUBJECT_NOT_PROCESSED'), config.data.get('EMAIL_TEXT_NOT_PROCESSED'))
            xml_paths = [item for item in os.listdir(queue_path)]

        scilista_items = []
        for xml_path in xml_paths:
            messages.append('*'*80)
            messages.append(xml_path + '\n')
            report_path = xml_path + '_base_reports'
            report_path, scilista_item = convert_package(serial_path, xml_path, report_path, web_path, issue_dao, isis_dao, article_dao, version)
            messages.append('*'*80)

            scilista_items.append(scilista_item)

            if email is not None:
                email_text = open(report_path + '/xml_converter_report.html', 'r').read()
                email.send(config.data.get('EMAIL_TO'), config.data.get('EMAIL_SUBJECT'), email_header + email_text, attaches=os.listdir(report_path))

        if config.data.get('SCILISTA') is not None:
            open(config.data.get('SCILISTA'), 'a+').write('\n'.join(scilista_items))
