# coding=utf-8

import os
import shutil
from datetime import datetime

from configuration import Configuration
from isis_models import IssueRecord

import files_manager
import reports


msg_list = []


def register_log(text):
    msg_list.append('\n' + text)
    print('\n' + text)


def get_valid_article(validation_results):
    a = None
    for xml_name, data in validation_results.items():
        results, article = data
        if article is not None:
            issue_label = article.issue_label
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


def display_statistic(f, e, w):
    msg = []
    msg.append('fatal errors: ' + str(f))
    msg.append('errors: ' + str(e))
    msg.append('warnings: ' + str(w))
    return '\n'.join(msg)


def evaluate_package(xml_path, report_path):
    register_log('Validating the package...')

    if not os.path.isdir(report_path):
        os.makedirs(report_path)
    xml_names = {f.replace('.xml', ''):f.replace('.xml', '') for f in os.listdir(xml_path) if f.endswith('.xml')}

    toc_statistic, package_statistic, validation_results, issues = reports.generate_package_reports(xml_path, xml_names, report_path)
    toc_f, toc_e, toc_w = toc_statistic
    package_f, package_e, package_w = package_statistic

    register_log('Table of Contents Validations')
    register_log(display_statistic(toc_f, toc_e, toc_w))
    register_log('Articles validations')
    register_log(display_statistic(package_f, package_e, package_w))

    return (toc_f == 0, validation_results)


def convert_package(serial_path, xml_path, report_path, web_path, db_issue, db_ahead, db_article):
    register_log('XML Converter')

    register_log('XML files: ' + xml_path)
    register_log('serial path: ' + serial_path)

    is_valid_package, validation_results = evaluate_package(xml_path, report_path)

    if not is_valid_package:
        register_log('FATAL ERROR: Unable to create "base" because of fatal errors in the Table of Contents data. Check toc.html report.')
    else:
        article = get_valid_article(validation_results)
        issue_record = get_issue_record(db_issue, article)
        if issue_record is None:
            register_log('FATAL ERROR: ' + article.issue_label + ' is not registered.')
        else:
            register_log('Issue: ' + article.issue_label + '.')
            issue_isis = IssueRecord(issue_record)
            issue = issue_isis.issue
            journal_files = files_manager.JournalFiles(serial_path, issue.acron)
            ahead_manager = files_manager.AheadManager(db_ahead, journal_files)
            issue_files = files_manager.IssueFiles(journal_files, article.issue_label, xml_path, web_path)
            issue_files.move_reports(report_path)
            issue_files.save_source_files(xml_path)
            report_path = issue_files.base_reports_path
            convert_articles(ahead_manager, db_article, validation_results, issue_record, issue_files)

    register_log('XML Converter reports of each document: ' + report_path)
    register_log('\n'.join(sorted(os.listdir(report_path))))

    content = '\n'.join(msg_list)

    f, e, w = reports.statistics_numbers(content)
    register_log(display_statistic(f, e, w))

    open(report_path + '/xml_converter.log', 'w').write(content)
    print('\n\nXML Converter report: ' + report_path + '/xml_converter.log')
    print('\n\n-- end --')


def convert_articles(ahead_manager, db_article, validation_results, issue_record, issue_files):
    total_new_doc = []
    total_ex_aop = []
    total_ex_aop_unmatched = []
    total_ex_aop_invalid = []
    total_ex_aop_partially = []
    not_loaded = []
    loaded = []

    register_log('Total of documents in the package: ' + str(len(validation_results)))

    for xml_name, data in validation_results.items():
        
        results, article = data

        register_log('.'*80)
        register_log('' + xml_name + '\n')

        label = xml_name

        valid_ahead, ahead_status, ahead_msg = ahead_manager.get_valid_ahead(article, xml_name)
        if valid_ahead is None:
            if ahead_status == 'new':
                total_new_doc.append(label)
            elif ahead_status == 'unmatched':
                total_ex_aop_unmatched.append(label)
            elif ahead_status == 'not valid':
                total_ex_aop_invalid.append(label)
        else:
            total_ex_aop.append(label)
            if ahead_status == 'partially matched':
                total_ex_aop_partially.append(label)

        register_log(ahead_msg)

        converted = convert_article(db_article, issue_record, issue_files, xml_name, article, results, valid_ahead)

        if converted:
            if valid_ahead is not None:
                done, msg = ahead_manager.manage_ex_ahead(valid_ahead)
                register_log(msg)
            loaded.append(xml_name)
            register_log('RESULT: converted')
        else:
            not_loaded.append(xml_name)
            register_log('ERROR: not converted')

    register_log('.'*80)

    register_log(display_list('converted', loaded))
    register_log(display_list('not converted', not_loaded))
    register_log(display_list('new documents', total_new_doc))
    register_log(display_list('ex-aheads', total_ex_aop))
    register_log(display_list('ex-aheads partially matched', total_ex_aop_partially))
    register_log(display_list('ex-aheads without PID', total_ex_aop_invalid))
    register_log(display_list('ex-aheads unmatched', total_ex_aop_unmatched))

    if len(loaded) > 0:
        _loaded = db_article.finish_conversion(issue_record, issue_files)
        register_log('Created database: ' + issue_files.base_path)
        register_log('Other products: ' + issue_files.base_path)

    if len(total_ex_aop) > 0:
        register_log(ahead_manager.finish_manage_ex_ahead())
    if len(loaded) > 0:
        register_log(issue_files.copy_files_to_web())


def display_list(title, items):
    messages = []
    messages.append('\n' + title + ': ' + str(len(items)))
    messages.append('\n'.join(items))
    return '\n'.join(messages)


def convert_article(db_article, issue_record, issue_files, xml_name, article, results, ahead):
    r = False

    if article is None:
        register_log('FATAL ERROR: Unable to load XML')
    else:
        f, e, w = results

        section_code, matched_rate, similar_section_title = IssueRecord(issue_record).section_code(article.toc_section)
        if section_code is None:
            if not article.is_ahead:
                f += 1
                register_log('FATAL ERROR: ' + article.toc_section + ' is not a registered section.')
                register_log('Registered sections:\n' + '\n'.join(IssueRecord(issue_record).section_titles))
        else:
            if matched_rate != 1:
                register_log('WARNING: section replaced: "' + similar_section_title + '" (instead of "' + article.toc_section + '")')
            else:
                register_log('section: ' + article.toc_section + '.')
        register_log('@article-type: ' + article.article_type)
        register_log(display_statistic(f, e, w))

        if f > 0:
            register_log('FATAL ERROR: Unable to create "base". Fix all the fatal errors.')
        else:
            if ahead is not None:
                article._ahead_pid = ahead.ahead_pid
            article_files = files_manager.ArticleFiles(issue_files, article.order, xml_name)
            r = db_article.create_id_file(issue_record, article, section_code, article_files)
    return r


def has_xml_files(path):
    files = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f) and f.endswith('.xml')]
    return len(files) > 0


def find_xml_paths(path):
    r = []
    if has_xml_files(path):
        r.append(path)
    else:
        for d in os.listdir(path):
            if os.path.isdir(path + '/' + d):
                if has_xml_files(path + '/' + d):
                    r.append(path + '/' + d)
    return r


def convert(path, config):
    #FIXME
    xml_paths = find_xml_paths(path)
    if len(xml_paths) == 0:
        print('XML files not found in ' + path + '\n')
    elif len(xml_paths) > 0:
        web_path = config.serial_path.replace('serial', '4web') if config.web_path is None else config.web_path
        serial_path = config.serial_path
        issue_dao = files_manager.IssueDAO(config.isis_dao, config.issue_db)
        article_dao = files_manager.ArticleDAO(config.isis_dao)

        for xml_path in xml_paths:
            print('*'*80)
            print(xml_path + '\n')
            report_path = xml_path + '_base_reports'
            convert_package(serial_path, xml_path, report_path, web_path, issue_dao, config.isis_dao, article_dao)
            print('*'*80)


def read_configuration():
    curr_path = os.getcwd().replace('\\', '/')
    filename = curr_path + '/./../scielo_paths.ini'
    if os.path.isfile(filename):
        r = Configuration(filename)
        if r is not None:
            if not r.valid():
                r = None
    else:
        r = None
    return r


def read_inputs(args):
    path = None
    error_messages = ''
    if len(args) == 2:
        script, path = args
        path = path.replace('\\', '/')
        if not os.path.isdir(path):
            path = None

    if path is None:
        messages = []
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python ' + script + ' <xml_src>')
        messages.append('where:')
        messages.append('  <xml_src> = XML filenames folder')
        error_messages = '\n'.join(messages)

    return (path, error_messages)


def call_converter(args):
    config = read_configuration()
    if config is None:
        print('ERROR: Unable to configure XML Converter.')
    else:
        path, error_messages = read_inputs(args)
        if path is None:
            print(error_messages)
        else:
            convert(path, config)
