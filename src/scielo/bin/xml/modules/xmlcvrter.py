# coding=utf-8

import os
import shutil

from configuration import Configuration
from isis_models import IssueISIS

import files_manager
import reports


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
    if not os.path.isdir(report_path):
        os.makedirs(report_path)
    xml_names = {f.replace('.xml', ''):f.replace('.xml', '') for f in os.listdir(xml_path) if f.endswith('.xml')}

    toc_statistic, package_statistic, validation_results, issues = reports.generate_package_reports(xml_path, xml_names, report_path)
    toc_f, toc_e, toc_w = toc_statistic
    package_f, package_e, package_w = package_statistic

    msg = []
    msg.append('Validations reports in ' + report_path)
    msg.append('\nTable of Contents Validations')
    msg += display_statistic(toc_f, toc_e, toc_w)
    msg.append('\nArticles validations')
    msg += display_statistic(package_f, package_e, package_w)

    return (toc_f == 0, validation_results, '\n'.join(msg))


def convert_package(serial_path, xml_path, report_path, web_path, db_issue, db_ahead, db_article):
    msg_list = []
    is_valid_package, validation_results, msg = evaluate_package(xml_path, report_path)

    msg_list.append(msg)
    if not is_valid_package:
        msg_list.append('\nFATAL ERROR: Unable to generate base because of fatal errors in the Table of Contents.')
    else:
        article = get_valid_article(validation_results)
        issue_record = get_issue_record(db_issue, article)
        if issue_record is None:
            msg_list.append('\nFATAL ERROR: ' + article.issue_label + ' is not registered.')
        else:
            issue = IssueISIS(issue_record).issue
            journal_files = files_manager.JournalFiles(serial_path, issue.acron)
            ahead_manager = files_manager.AheadManager(db_ahead, journal_files)
            issue_files = files_manager.IssueFiles(journal_files, article.issue_label, xml_path, web_path)
            issue_files.move_reports(report_path)
            report_path = issue_files.base_reports_path
            msg = convert_articles(ahead_manager, db_article, validation_results, issue_record, issue_files)
            msg_list.append(msg)
    msg_list.append('Check all the reports: ' + report_path)
    open(report_path + '/conversion.log', 'w').write('\n'.join(msg_list))
    print('Check the report: ' + report_path + '/conversion.log')
    print('-- end --')


def convert_articles(ahead_manager, db_article, validation_results, issue_record, issue_files):
    total_new_articles = []
    total_ex_aheads = []
    not_loaded = []
    msg_list = []
    msg_list.append('\nTotal of articles in the package: ' + str(len(validation_results)))

    for xml_name, data in validation_results.items():
        results, article = data
        converted, msg = convert_article(db_article, issue_record, issue_files, xml_name, article, results)
        msg_list.append(msg)
        if converted:
            article_title = xml_name if article.title is None else xml_name + ' ' + article.title
            if article.number != 'ahead':
                xml_filename = xml_name + '.xml'
                ex_ahead, msg = ahead_manager.manage_ex_ahead(article.doi, xml_filename)
                msg_list.append(msg)
            else:
                ex_ahead = None
            if ex_ahead is None:
                total_new_articles.append(article_title)
            else:
                total_ex_aheads.append(article_title)
        else:
            not_loaded.append(xml_name)

    msg_list.append('.'*80)

    msg_list.append(display_list('ex-aheads', total_ex_aheads))
    msg_list.append(display_list('new articles', total_new_articles))
    msg_list.append(display_list('converted', loaded))
    msg_list.append(display_list('not converted', not_loaded))

    if len(total_ex_aheads) > 0:
        msg_list += ahead_manager.finish_manage_ex_ahead()

    msg_list += issue_files.copy_files_to_web()
    return '\n'.join(msg_list)


def display_list(title, items):
    msg_list = []
    msg_list.append(title + ': ' + str(len(items)))
    msg_list.append('\n'.join(items))
    return '\n'.join(msg_list)


def convert_article(db_article, issue_record, issue_files, xml_name, article, results):
    r = False
    msg_list = []
    msg_list.append('.'*80)
    msg_list.append(xml_name)

    if article is None:
        msg.append('FATAL ERROR: Unable to load XML')
    else:
        f, e, w = results

        section_code = issue_record.section_code(article.toc_section)
        if section_code is None:
            f += 1
            msg_list.append('FATAL ERROR: ' + article.toc_section + ' is not a valid section.')

        display_statistic(f, e, w)

        if f > 0:
            msg_list.append('FATAL ERROR: Unable to generate its base because of fatal errors in XML.')
        else:
            article_files = files_manager.ArticleFiles(issue_files, article.order, xml_name)
            if db_article.create_id_file(issue_record, article, section_code, article_files):
                msg_list.append('converted')
                r = True
            else:
                msg_list.append('FATAL ERROR: Unable to generate ' + article_files.id_filename)
    return (r, '\n'.join(msg_list))


def validate_path(path):
    xml_path = None
    if path is not None:
        path = path.replace('\\', '/')
        if path.endswith('/'):
            path = path[0:-1]
        if len(path) > 0:
            if os.path.isdir(path):
                xml_files = [path + '/' + f for f in os.listdir(path) if f.endswith('.xml')]
                if len(xml_files) > 0:
                    xml_path = path
    return xml_path


def convert(path, acron, config):
    #FIXME
    xml_path = validate_path(path)
    if xml_path is None:
        print('There is nothing to convert.\n')
        print(' must be an XML file or a folder which contains XML files.')
    else:
        web_path = config.serial_path.replace('serial', '4web') if config.web_path is None else config.web_path
        report_path = os.path.dirname(xml_path) + '/base_reports'
        serial_path = config.serial_path
        issue_dao = files_manager.IssueDAO(config.isis_dao, config.issue_db)
        article_dao = files_manager.ArticleDAO(config.isis_dao)
        convert_package(serial_path, xml_path, report_path, web_path, issue_dao, config.isis_dao, article_dao)


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
    acron = ''
    if len(args) == 3:
        script, path, acron = args
        path = path.replace('\\', '/')
        if not os.path.isfile(path) and not os.path.isdir(path):
            path = None

    if path is None:
        messages = []
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python ' + script + ' <xml_src> <acron>')
        messages.append('where:')
        messages.append('  <xml_src> = XML filename or path which contains XML files')
        messages.append('  <acron> = journal acronym')
        acron = '\n'.join(messages)

    return (path, acron)


def call_converter(args):
    config = read_configuration()
    if config is None:
        print('ERROR: Unable to configure XML Converter.')
    else:
        path, acron = read_inputs(args)
        if path is None:
            print(acron)
        else:
            convert(path, acron, config)
