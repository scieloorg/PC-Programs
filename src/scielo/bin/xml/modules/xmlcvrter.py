# coding=utf-8

import os
import shutil

from configuration import Configuration
from isis_models import IssueRecord

import files_manager
import reports
import pkg_checker
import xml_versions
import article_utils


curr_path = os.path.dirname(__file__).replace('\\', '/')

html_report = reports.ReportHTML()
converter_report_lines = []


def register_log(message):
    if not '<' in message:
        message = html_report.format_message(message)
    converter_report_lines.append(message)


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

    issue_record = None
    issue_label = 'UNKNOWN'
    doc_files_info_list = []
    xml_filenames = sorted([xml_path + '/' + f for f in os.listdir(xml_path) if f.endswith('.xml') and not 'incorrect' in f])

    register_log('<h2>XML files</h2>')
    register_log('XML path: ' + xml_path)
    register_log('Total of XML files: ' + str(len(xml_filenames)))
    register_log(html_report.format_list('', 'ol', [os.path.basename(f) for f in xml_filenames]))

    for xml_filename in xml_filenames:
        doc_files_info = files_manager.DocumentFiles(xml_filename, report_path, None)
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
            journal_files = files_manager.JournalFiles(serial_path, issue.acron)
            ahead_manager = files_manager.AheadManager(db_ahead, journal_files, db_issue, issue.issn_id)
            issue_files = files_manager.IssueFiles(journal_files, issue_label, xml_path, web_path)
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
        # subject
        msg.append('section: ' + article.toc_section + '.')
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

        # @article-type
        section_title = article.toc_section
        if similar_section_title != article.toc_section:
            section_title = similar_section_title
        msg.append('@article-type: ' + article.article_type)
        rate = 0
        max_rate = 0
        for item in article.article_type.split('-'):
            rate = article_utils.how_similar(section_title, item)
            if rate > max_rate:
                max_rate = rate
        if max_rate < 0.7:
            msg.append('WARNING: Check if ' + article.article_type + ' is a valid value for @article-type. (' + str(max_rate) + ')')

    msg = ''.join([html_report.format_message(item) for item in msg])
    return (f, e, w, msg, section_code)


def convert_article(db_article, issue_record, issue_files, xml_name, article, ahead):
    r = False
    if article is not None:
        if ahead is not None:
            article._ahead_pid = ahead.ahead_pid
        article_files = files_manager.ArticleFiles(issue_files, article.order, xml_name)
        r = db_article.create_id_file(issue_record, article, article_files)
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


def convert(path, config, version):
    #FIXME
    xml_paths = find_xml_paths(path)
    if len(xml_paths) == 0:
        print('XML files not found in ' + path + '\n')
    elif len(xml_paths) > 0:
        web_path = config.serial_path.replace('serial', '4web') if config.web_path is None else config.web_path
        serial_path = config.serial_path

        if open(curr_path + '/issue.fst', 'r').read() != open(config.issue_db + '.fst', 'r').read():
            shutil.copyfile(curr_path + '/issue.fst', config.issue_db + '.fst')
            config.isis_dao.update_indexes(config.issue_db, config.issue_db + '.fst')
        issue_dao = files_manager.IssueDAO(config.isis_dao, config.issue_db)
        article_dao = files_manager.ArticleDAO(config.isis_dao)

        for xml_path in xml_paths:
            print('*'*80)
            print(xml_path + '\n')
            report_path = xml_path + '_base_reports'
            convert_package(serial_path, xml_path, report_path, web_path, issue_dao, config.isis_dao, article_dao, version)
            print('*'*80)


def read_configuration():
    filename = curr_path + '/../../scielo_paths.ini'

    if os.path.isfile(filename):
        r = Configuration(filename)
        if r is not None:
            if not r.valid():
                r = None
    else:
        r = None
    if r is None:
        print(filename)
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
        messages.append('python xml_converter.py <xml_src>')
        messages.append('where:')
        messages.append('  <xml_src> = XML filenames folder')
        error_messages = '\n'.join(messages)

    return (path, error_messages)


def call_converter(args, version='1.0'):
    config = read_configuration()
    if config is None:
        print('ERROR: Unable to configure XML Converter.')
    else:
        path, error_messages = read_inputs(args)
        if path is None:
            print(error_messages)
        else:
            convert(path, config, version)
