# coding=utf-8

import os
import shutil
from datetime import datetime

import serial_files
import fs_utils
import utils
import html_reports
import dbm_isis

import xc_models
import pkg_reports
import xml_utils
import xml_versions
import xpmaker
import xc
import xc_config

import attributes


converter_report_lines = []
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

CONFIG_PATH = CURRENT_PATH + '/../config/'
converter_env = None


categories_messages = {
    'converted': 'converted', 
    'not converted': 'not converted', 
    'skept': 'skept conversion', 
    'deleted ex-aop': 'deleted ex-aop', 
    'deleted incorrect order': 'deleted incorrect order', 
    'not deleted ex-aop': 'not deleted ex-aop', 
    'new aop': 'aop version', 
    'new doc': 'doc has no aop', 
    'ex aop': 'aop is published in an issue', 
    'matched aop': 'doc has aop version', 
    'partially matched aop': 'doc has aop version partially matched (title/author are similar)', 
    'aop missing PID': 'doc has aop version which has no PID', 
    'unmatched aop': 'doc has an invalid aop version (title/author are not the same)', 
}


class ConverterEnv(object):

    def __init__(self):
        self.version = None
        self.db_issue = None
        self.db_article = None
        self.db_isis = None
        self.local_web_app_path = None
        self.serial_path = None
        self.is_windows = None
        self.org_manager = None


def register_log(message):
    if not '<' in message:
        message = html_reports.p_message(message)
    converter_report_lines.append(message)


def find_i_record(issue_label, print_issn, e_issn):
    i_record = None
    print('debug: find_i_record')
    print([issue_label, print_issn, e_issn])
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
        msg = html_reports.p_message('FATAL ERROR: Unable to identify the article\'s issue')
    else:
        i_record = find_i_record(issue_label, p_issn, e_issn)

        if i_record is None:
            msg = html_reports.p_message('FATAL ERROR: Issue ' + issue_label + ' is not registered in ' + converter_env.db_issue.db_filename + '. (' + '/'.join([i for i in [p_issn, e_issn] if i is not None]) + ')')
        else:
            issue_models = xc_models.IssueModels(i_record)

    return (issue_models, msg)


def get_complete_issue_items(issue_files, pkg_path, registered_articles, pkg_articles):
    #actions = {'add': [], 'skip-update': [], 'update': [], '-': [], 'changed order': []}
    xml_articles_status = {}
    complete_issue_items = {}
    for name in registered_articles.keys():
        if not name in pkg_articles.keys():
            xml_articles_status[name] = '-'
            complete_issue_items[name] = registered_articles[name]
    changed_orders = {}
    for name, article in pkg_articles.items():
        status = 'add'
        if name in registered_articles.keys():
            status = 'update'
            if converter_env.skip_identical_xml:
                if open(issue_files.base_source_path + '/' + name + '.xml', 'r').read() == open(pkg_path + '/' + name + '.xml', 'r').read():
                    status = 'skip-update'
            if status == 'update':
                if registered_articles[name].order != pkg_articles[name].order:
                    changed_orders[name] = (registered_articles[name].order, pkg_articles[name].order)
        xml_articles_status[name] = status
        if status == 'skip-update':
            complete_issue_items[name] = registered_articles[name]
        else:
            complete_issue_items[name] = pkg_articles[name]
    return (complete_issue_items, xml_articles_status, changed_orders)


def complete_issue_items_row(article, status, creation_date, source, other_order=None):
    values = []
    values.append(status)
    values.append(article.order)
    values.append(article.xml_name)
    if other_order is None:
        values.append('')
    else:
        values.append(other_order)
    values.append(source)
    values.append(creation_date)
    values.append(article.previous_pid)
    values.append(article.toc_section)
    values.append(article.article_type)
    values.append(article.title)
    return values


def display_status_before_conversion(registered_articles, pkg_articles, xml_articles_status, status_column_label='action'):
    labels = [status_column_label, 'order', 'name', 'notes', 'source', 'registration date', 'aop PID', 'toc section', '@article-type', 'article title']
    orders = [article.order for article in registered_articles.values()] + [article.order if article.tree is not None else 'None' for article in pkg_articles.values()]

    orders = sorted(list(set([order for order in orders if order is not None])))

    sorted_registered = pkg_reports.articles_sorted_by_order(registered_articles)
    print('sorted_registered')
    print(sorted_registered)

    sorted_package = pkg_reports.articles_sorted_by_order(pkg_articles)
    print('sorted_package')
    print(sorted_package)

    items = []
    print('orders')
    print(orders)
    for order in orders:
        status = ''
        print('order')
        print(order)
        if order in sorted_registered.keys():
            for article in sorted_registered[order]:
                status = xml_articles_status[article.xml_name]
                _notes = ''
                if status == 'update':
                    if registered_articles[article.xml_name].order != pkg_articles[article.xml_name].order:
                        status = 'delete'
                        _notes = 'new order=' + pkg_articles[article.xml_name].order
                values = complete_issue_items_row(article, status, article.creation_date[0], 'registered', _notes)
                items.append(pkg_reports.label_values(labels, values))

        if order in sorted_package.keys():
            for article in sorted_package[order]:
                status = xml_articles_status[article.xml_name]
                _notes = ''
                if registered_articles.get(article.xml_name) is not None:
                    if registered_articles[article.xml_name].order != pkg_articles[article.xml_name].order:
                        _notes = 'replacing ' + registered_articles[article.xml_name].order
                values = complete_issue_items_row(article, status, '', 'package', _notes)
                items.append(pkg_reports.label_values(labels, values))
    return html_reports.sheet(labels, None, items, None, 'dbstatus', status_column_label)


def display_status_after_conversion(registered_articles, pkg_articles, xml_articles_status, unmatched_orders):
    labels = ['action', 'order', 'name', 'notes', 'source', 'registration date', 'aop PID', 'toc section', '@article-type', 'article title']
    status_labels = {'update': 'updated', 'add': 'added', '-': '-', 'skip-update': 'skept', 'order changed': 'order changed'}
    orders = sorted(list(set([article.order for article in registered_articles.values()] + [article.order if article.tree is not None else 'None' for article in pkg_articles.values()])))

    print('display_status_after_conversion')
    sorted_registered = pkg_reports.articles_sorted_by_order(registered_articles)
    print(sorted_registered)

    sorted_package = pkg_reports.articles_sorted_by_order(pkg_articles)
    print(sorted_package)
    items = []

    for order in orders:
        if order in sorted_registered.keys():
            for article in sorted_registered[order]:
                status = xml_articles_status[article.xml_name]
                _notes = ''
                if status == 'update':
                    name = article.xml_name
                    if name in unmatched_orders.keys():
                        previous_order, new_order = unmatched_orders[name]
                        _notes = previous_order + '=>' + new_order

                values = complete_issue_items_row(article, status_labels[status], article.creation_date[0], 'registered', _notes)
                items.append(pkg_reports.label_values(labels, values))
        else:
            if order in sorted_package.keys():
                for article in sorted_package[order]:
                    status = xml_articles_status[article.xml_name]
                    _notes = ''

                    if status in ['update', 'add']:
                        if status == 'update':
                            name = article.xml_name
                            if name in unmatched_orders.keys():
                                previous_order, new_order = unmatched_orders[name]
                                _notes = 'unable to replace ' + previous_order + ' by ' + new_order
                        status = 'ERROR: unable to ' + status
                    values = complete_issue_items_row(article, 'error', '', 'package', _notes)
                    items.append(pkg_reports.label_values(labels, values))
            else:
                values = []
                values.append('deleted')
                values.append(order)
                for k in range(0, len(labels)-2):
                    values.append('')
                items.append(pkg_reports.label_values(labels, values))

    return html_reports.sheet(labels, None, items, None, 'dbstatus', 'action')


def complete_issue_items_report(complete_issue_items, unmatched_orders):
    unmatched_orders_errors = ''
    if len(unmatched_orders) > 0:
        unmatched_orders_errors = ''.join([html_reports.p_message('WARNING: ' + name + "'s orders: " + ' -> '.join(list(order))) for name, order in unmatched_orders.items()])

    toc_f, toc_e, toc_w, toc_report = pkg_reports.validate_package(complete_issue_items, validate_order=True)
    toc_report = pkg_reports.get_toc_report_text(toc_f, toc_e, toc_w, unmatched_orders_errors + toc_report)

    return (toc_f, toc_report)


def normalized_package(src_path, report_path, wrk_path, pkg_path, version):
    xml_filenames = sorted([src_path + '/' + f for f in os.listdir(src_path) if f.endswith('.xml') and not 'incorrect' in f])
    articles, doc_file_info_items = xpmaker.make_package(xml_filenames, report_path, wrk_path, pkg_path, version, 'acron')
    return (xml_filenames, articles, doc_file_info_items)


def get_issue_models(articles):
    issue_label, p_issn, e_issn = xpmaker.package_issue(articles)
    return find_issue_models(issue_label, p_issn, e_issn)


def get_issue_files(issue_models, pkg_path):
    journal_files = serial_files.JournalFiles(converter_env.serial_path, issue_models.issue.acron)
    return serial_files.IssueFiles(journal_files, issue_models.issue.issue_label, pkg_path, converter_env.local_web_app_path)


def convert_package(src_path):
    display_title = False
    validate_order = True

    validations_report = ''
    toc_report = ''
    sheets = ''
    conclusion_msg = ''

    conversion_status_summary_report = ''
    aop_status_summary_report = ''
    before_conversion = ''
    after_conversion = ''
    acron_issue_label = 'unidentified issue'
    scilista_item = None
    issue_files = None

    dtd_files = xml_versions.DTDFiles('scielo', converter_env.version)
    result_path = src_path + '_xml_converter_result'
    wrk_path = result_path + '/work'
    pkg_path = result_path + '/scielo_package'
    report_path = result_path + '/errors'
    old_report_path = report_path
    old_result_path = result_path

    for path in [result_path, wrk_path, pkg_path, report_path]:
        if not os.path.isdir(path):
            os.makedirs(path)

    xml_filenames, pkg_articles, doc_file_info_items = normalized_package(src_path, report_path, wrk_path, pkg_path, converter_env.version)
    issue_models, issue_error_msg = get_issue_models(pkg_articles)

    skip = False
    if not issue_models is None:
        issue_files = get_issue_files(issue_models, pkg_path)
        result_path = issue_files.issue_path
        acron_issue_label = issue_models.issue.acron + ' ' + issue_models.issue.issue_label

        registered_articles = get_registered_articles(issue_files)

        complete_issue_items, xml_articles_status, unmatched_orders = get_complete_issue_items(issue_files, pkg_path, registered_articles, pkg_articles)

        before_conversion = html_reports.tag('h3', 'Documents status in the package/database - before conversion')
        before_conversion += display_status_before_conversion(registered_articles, pkg_articles, xml_articles_status)

        toc_f, toc_report = complete_issue_items_report(complete_issue_items, unmatched_orders)

        selected_articles = {}
        if toc_f == 0:
            for xml_name, article in pkg_articles.items():
                if xml_articles_status[xml_name] in ['add', 'update']:
                    selected_articles[xml_name] = article

        if len(selected_articles) > 0:
            fatal_errors, articles_stats, articles_reports, articles_sheets = pkg_reports.validate_pkg_items(converter_env.db_article.org_manager, selected_articles, doc_file_info_items, dtd_files, validate_order, display_title, xml_articles_status)

            scilista_item, conversion_stats_and_reports, conversion_status, aop_status = convert_articles(issue_files, issue_models, pkg_articles, articles_stats, xml_articles_status, registered_articles, unmatched_orders)

            validations_report = html_reports.tag('h2', 'Detail Report')
            validations_report += pkg_reports.get_articles_report_text(articles_reports, articles_stats, conversion_stats_and_reports)

            conclusion_msg = html_reports.tag('h2', 'Summary Report')
            conclusion_msg += report_conclusion_message(scilista_item, acron_issue_label, len(conversion_status['converted']), len(conversion_status['not converted']), len(selected_articles))

            after_conversion = html_reports.tag('h3', 'Documents status in the package/database - after conversion')
            after_conversion += display_status_after_conversion(get_registered_articles(issue_files), pkg_articles, xml_articles_status, unmatched_orders)

            conversion_status_summary_report = html_reports.tag('h3', 'Conversion results') + report_status(conversion_status)
            aop_status_summary_report = html_reports.tag('h3', 'aop information')
            if aop_status is None:
                aop_status_summary_report += 'this journal has no aop.'
            else:
                aop_status_summary_report += report_status(aop_status)

            sheets = pkg_reports.get_lists_report_text(articles_sheets)

            issue_files.save_reports(report_path)
            issue_files.save_source_files(pkg_path)
            report_path = issue_files.base_reports_path

            if scilista_item is not None:
                issue_files.copy_files_to_local_web_app()
        else:
            conclusion_msg = html_reports.tag('h2', 'Summary Report')
            conclusion_msg += report_conclusion_message(scilista_item, acron_issue_label, 0, len(pkg_articles), len(selected_articles))
            skip = True

    report_location = report_path + '/xml_converter.html'

    texts = []
    texts.append(html_reports.section('Package: XML list', pkg_reports.xml_list(pkg_path, xml_filenames)))
    texts.append(issue_error_msg)
    texts.append(toc_report)
    texts.append(conclusion_msg)
    texts.append(conversion_status_summary_report)
    texts.append(aop_status_summary_report)
    texts.append(before_conversion)
    texts.append(after_conversion)
    texts.append(validations_report)
    texts.append(sheets)

    if converter_env.is_windows:
        texts.append(pkg_reports.processing_result_location(issue_files.issue_path))

    texts.append(html_reports.tag('p', 'Finished.'))

    content = html_reports.join_texts(texts)

    if old_report_path in content:
        content = content.replace(old_report_path, report_path)

    f, e, w = html_reports.statistics_numbers(content)

    header_status = ''
    subject_stats = ''
    subject_results = 'APPROVED ' if scilista_item is not None else 'REJECTED'
    if skip:
        header_status = html_reports.p_message('WARNING: Package was ignored because it is already published and package content is unchanged.')
        subject_stats = ''
        subject_results = 'IGNORED'
    else:
        subject_stats = '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(f)), ('errors', str(e)), ('warnings', str(w))]]) + ']'
        header_status = html_reports.statistics_display(f, e, w, False)

    pkg_reports.save_report(report_location, ['XML Conversion (XML to Database)', acron_issue_label], header_status + content)
    subject_results += subject_stats

    if not converter_env.is_windows:
        format_reports_for_web(report_path, pkg_path, acron_issue_label.replace(' ', '/'))
        fs_utils.delete_file_or_folder(src_path)

    if old_result_path != result_path:
        fs_utils.delete_file_or_folder(old_result_path)

    return (report_location, scilista_item, acron_issue_label, subject_results)


def format_reports_for_web(report_path, pkg_path, issue_path):
    if not os.path.isdir(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path):
        os.makedirs(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path)

    for f in os.listdir(report_path):
        if f.endswith('.zip') or f == 'xml_converter.txt':
            os.unlink(report_path + '/' + f)
        else:
            content = open(report_path + '/' + f).read()
            if not isinstance(content, unicode):
                try:
                    content = content.decode('utf-8')
                except:
                    content = content.decode('iso-8859-1')
            content = content.replace('file:///' + pkg_path, '/img/revistas/' + issue_path)
            content = content.replace('file:///' + report_path, '/reports/' + issue_path)
            if isinstance(content, unicode):
                content = content.encode('utf-8')
            open(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path + '/' + f, 'w').write(content)


def convert_articles(issue_files, issue_models, pkg_articles, articles_stats, xml_articles_status, registered_articles, unmatched_orders):
    index = 0
    conversion_stats_and_reports = {}
    conversion_status = {}

    for k in ['converted', 'not converted', 'skept', 'deleted incorrect order']:
        conversion_status[k] = []

    n = '/' + str(len(pkg_articles))

    i_ahead_records = {}
    for db_filename in issue_files.journal_files.ahead_bases:
        year = os.path.basename(db_filename)[0:4]
        i_ahead_records[year] = find_i_record(year + 'nahead', issue_models.issue.issn_id, None)

    ahead_manager = xc_models.AheadManager(converter_env.db_isis, issue_files.journal_files, i_ahead_records)
    aop_status = None
    if ahead_manager.journal_has_aop():
        aop_status = {'deleted ex-aop': [], 'not deleted ex-aop': []}
    for xml_name in pkg_reports.sorted_xml_name_by_order(pkg_articles):
        article = pkg_articles[xml_name]
        index += 1

        item_label = str(index) + n + ' - ' + xml_name
        print(item_label)

        msg = ''

        if not xml_articles_status[xml_name] in ['add', 'update']:
            msg += html_reports.tag('p', 'skept')
            conversion_status['skept'].append(xml_name)
            conv_stats = ''
        else:
            xml_stats, data_stats = articles_stats[xml_name]
            xml_f, xml_e, xml_w = xml_stats
            data_f, data_e, data_w = data_stats

            valid_ahead = None
            if aop_status is not None:
                valid_ahead, doc_ahead_status = ahead_manager.get_valid_ahead(article)
                if not doc_ahead_status in aop_status.keys():
                    aop_status[doc_ahead_status] = []
                aop_status[doc_ahead_status].append(xml_name)
                msg += aop_message(article, valid_ahead, doc_ahead_status)

                if valid_ahead is not None:
                    if doc_ahead_status in ['unmatched aop', 'aop missing PID']:
                        valid_ahead = None

            section_code, issue_validations_msg = validate_xml_issue_data(issue_models, article)
            msg += html_reports.tag('h4', 'checking issue data')
            msg += issue_validations_msg
            conv_f, conv_e, conv_w = html_reports.statistics_numbers(msg)

            if conv_f + xml_f + data_f == 0:
                article.section_code = section_code
                if valid_ahead is not None:
                    article._ahead_pid = valid_ahead.ahead_pid

                article_files = serial_files.ArticleFiles(issue_files, article.order, xml_name)

                creation_date = None if not xml_name in registered_articles else registered_articles[xml_name].creation_date

                saved = converter_env.db_article.create_id_file(issue_models.record, article, article_files, creation_date)
                if saved:
                    if xml_name in unmatched_orders.keys():
                        prev_order, curr_order = unmatched_orders[xml_name]
                        msg += html_reports.p_message('WARNING: Replacing orders: ' + prev_order + ' by ' + curr_order)
                        prev_article_files = serial_files.ArticleFiles(issue_files, prev_order, xml_name)
                        msg += html_reports.p_message('WARNING: Deleting ' + os.path.basename(prev_article_files.id_filename))
                        os.unlink(prev_article_files.id_filename)
                        conversion_status['deleted incorrect order'].append(prev_order)

                    if aop_status is not None:
                        if doc_ahead_status in ['matched aop', 'partially matched aop']:
                            saved, ahead_msg = ahead_manager.manage_ex_ahead(valid_ahead)
                            msg += ''.join([item for item in ahead_msg])
                            if saved:
                                aop_status['deleted ex-aop'].append(xml_name)
                                msg += html_reports.p_message('INFO: ex aop was deleted')
                            else:
                                aop_status['not deleted ex-aop'].append(xml_name)
                                msg += html_reports.p_message('ERROR: Unable to delete ex aop')
                    conversion_status['converted'].append(xml_name)
                    msg += html_reports.p_message('OK: converted')
                else:
                    conversion_status['not converted'].append(xml_name)
                    msg += html_reports.p_message('FATAL ERROR: not converted')
            else:
                conversion_status['not converted'].append(xml_name)
                #msg += html_reports.p_message('FATAL ERROR: not converted')

        conv_f, conv_e, conv_w = html_reports.statistics_numbers(msg)
        title = html_reports.statistics_display(conv_f, conv_e, conv_w, True)
        conv_stats = html_reports.get_stats_numbers_style(conv_f, conv_e, conv_w)
        conversion_stats_and_reports[xml_name] = (conv_f, conv_e, conv_w, html_reports.collapsible_block(xml_name + 'conv', 'Converter validations: ' + title, msg, conv_stats))

    if ahead_manager.journal_has_aop():
        if len(aop_status['deleted ex-aop']) > 0:
            updated = ahead_manager.finish_manage_ex_ahead()
            if len(updated) > 0:
                aop_status['updated bases'] = updated
        aop_status['still aop'] = ahead_manager.still_ahead_items()
    scilista_item = None
    if len(conversion_status['not converted']) == 0:
        saved = converter_env.db_article.finish_conversion(issue_models.record, issue_files)
        if saved > 0:
            scilista_item = issue_models.issue.acron + ' ' + issue_models.issue.issue_label
            if not converter_env.is_windows:
                converter_env.db_article.generate_windows_version(issue_files)

    return (scilista_item, conversion_stats_and_reports, conversion_status, aop_status)


def aop_message(article, ahead, status):
    data = []
    msg_list = []
    if status == 'new aop':
        msg_list.append('This document is an "aop".')
    else:
        msg_list.append('Checking if ' + article.xml_name + ' has an "aop version"')
        if article.doi is not None:
            msg_list.append('Checking if ' + article.doi + ' has an "aop version"')

        if status == 'new doc':
            msg_list.append('WARNING: Not found an "aop version" of this document.')
        else:
            msg_list.append('WARNING: Found: "aop version"')
            if status == 'partially matched aop':
                msg_list.append('WARNING: the title/author of article and its "aop version" are similar.')
            elif status == 'aop missing PID':
                msg_list.append('ERROR: the "aop version" has no PID')
            elif status == 'unmatched aop':
                status = 'unmatched aop'
                msg_list.append('FATAL ERROR: the title/author of article and "aop version" are different.')

                data.append('doc title:' + article.title)
                data.append('aop title:' + ahead.article_title)
                data.append('doc first author:' + article.first_author_surname)
                data.append('aop first author:' + ahead.first_author_surname)
    msg = ''
    msg += html_reports.tag('h4', 'checking existence of aop version')
    msg += ''.join([html_reports.p_message(item) for item in msg_list])
    msg += ''.join([html_reports.tag('pre', item) for item in data])
    return msg


def get_registered_articles(issue_files):
    registered_issue_models, registered_articles_list = converter_env.db_article.registered_items(issue_files)
    registered_articles = {}
    for article in registered_articles_list:
        registered_articles[article.xml_name] = article
    return registered_articles


def report_status(status):
    text = ''
    for category in sorted(status.keys()):
        if len(status[category]) == 0:
            ltype = 'ul'
            list_items = ['None']
        else:
            ltype = 'ol'
            list_items = status[category]
        text += html_reports.format_list(categories_messages.get(category, category), ltype, list_items)

    return text


def report_conclusion_message(scilista_item, issue_label, converted, not_converted, selected_articles):
    text = ''
    text += html_reports.p_message('converted: ' + str(converted) + '/' + str(selected_articles))
    if scilista_item is None:
        if selected_articles == 0 and converted == 0:
            text += html_reports.p_message('WARNING: ' + issue_label + ' will not be updated/published on ' + converter_env.web_app_site + ' because nothing was changed.')
        else:
            text += html_reports.p_message('FATAL ERROR: ' + issue_label + ' is not complete (' + str(not_converted) + ' were not converted), so ' + issue_label + ' will not be updated/published on ' + converter_env.web_app_site + '.')
    else:
        text += html_reports.p_message('OK: ' + issue_label + ' will be updated/published on ' + converter_env.web_app_site + '.')

    return text


def transfer_website_files(acron, issue_id, local_web_app_path, user, server, remote_web_app_path):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    issue_id_path = acron + '/' + issue_id

    folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']

    for folder in folders:
        dest_path = remote_web_app_path + folder + issue_id_path
        source_path = local_web_app_path + folder + issue_id_path
        xc.run_remote_mkdirs(user, server, dest_path)
        xc.run_rsync(source_path, user, server, dest_path)


def transfer_report_files(acron, issue_id, local_web_app_path, user, server, remote_web_app_path):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    issue_id_path = acron + '/' + issue_id

    folders = ['/htdocs/reports/']

    for folder in folders:
        dest_path = remote_web_app_path + folder + issue_id_path
        source_path = local_web_app_path + folder + issue_id_path
        xc.run_remote_mkdirs(user, server, dest_path)
        xc.run_rsync(source_path, user, server, dest_path)


def validate_xml_issue_data(issue_models, article):
    msg = []
    if article.tree is not None:

        # issue date
        if article.issue_pub_dateiso != issue_models.issue.dateiso:
            msg.append(html_reports.tag('h5', 'publication date'))
            msg.append('FATAL ERROR: Invalid value of publication date: ' + article.issue_pub_dateiso + '. Expected value: ' + issue_models.issue.dateiso)

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
            _sectitle = most_similar
        else:
            _sectitle = article.toc_section
        _sectitle = attributes.normalize_section_title(_sectitle)
        _article_type = attributes.normalize_section_title(article.article_type)
        rate = compare_article_type_and_section(_sectitle, _article_type)
        if rate < 0.5:
            if not _article_type in _sectitle:
                msg.append('WARNING: Check if ' + article.article_type + ' is a valid value for @article-type. <!--' + _sectitle + ' -->')

    msg = ''.join([html_reports.p_message(item) for item in msg])
    return (section_code, msg)


def compare_article_type_and_section(article_section, article_type):
    return utils.how_similar(article_section, article_type.replace('-', ' '))


def queue_packages(download_path, temp_path, queue_path, archive_path):
    invalid_pkg_files = []
    proc_id = datetime.now().isoformat()[11:16].replace(':', '')
    temp_path = temp_path + '/' + proc_id
    queue_path = queue_path + '/' + proc_id
    pkg_paths = []

    if archive_path is not None:
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
            if archive_path is not None:
                if os.path.isdir(archive_path):
                    shutil.copyfile(temp_path + '/' + pkg_name, archive_path + '/' + pkg_name)
            pkg_paths.append(queued_pkg_path)
        else:
            invalid_pkg_files.append(pkg_name)
            fs_utils.delete_file_or_folder(queued_pkg_path)
        fs_utils.delete_file_or_folder(temp_path + '/' + pkg_name)
    fs_utils.delete_file_or_folder(temp_path)

    return (pkg_paths, invalid_pkg_files)


def xml_converter_read_configuration(filename):
    r = None
    if os.path.isfile(filename):
        r = xc_config.XMLConverterConfiguration(filename)
        if not r.valid:
            r = None
    return r


def xml_converter_get_inputs(args):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    package_path = None
    script = None
    collection_acron = None
    print(args)
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
    errors = []
    if package_path is None:
        if collection_acron is None:
            errors.append('Missing collection acronym')
    else:
        errors = xml_utils.is_valid_xml_path(package_path)
    return errors


def xml_config_filename(collection_acron):
    filename = CURRENT_PATH + '/../../scielo_paths.ini'

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
    elif package_path is not None:
        execute_converter(package_path, collection_acron)


def send_message(mailer, to, subject, text, attaches=None):
    if mailer is not None:
        print('sending message ' + subject)
        mailer.send_message(to, subject, text, attaches)


def execute_converter(package_paths, collection_name=None):
    #collection_names = {'Brasil': 'scl', u'Salud Pública': 'spa'}
    collection_names = {}
    collection_acron = collection_names.get(collection_name)
    if collection_acron is None:
        collection_acron = collection_name

    config = xc.get_configuration(collection_acron)
    if config is not None:
        prepare_env(config)
        invalid_pkg_files = []
        bad_pkg_files = []
        bad_pkg_files_errors = []
        scilista = []

        mailer = xc.get_mailer(config)

        if package_paths is None:
            package_paths, invalid_pkg_files = queue_packages(config.download_path, config.temp_path, config.queue_path, config.archive_path)
        if package_paths is None:
            package_paths = []
        if not isinstance(package_paths, list):
            package_paths = [package_paths]

        for package_path in package_paths:
            package_folder = os.path.basename(package_path)
            print(package_path)
            report_location, scilista_item, acron_issue_label, results = convert_package(package_path)
            acron, issue_id = acron_issue_label.split(' ')
            #except Exception as e:
            #    print('ERROR!!!')
            #    print(e)
            #    bad_pkg_files.append(package_folder)
            #    bad_pkg_files_errors.append(str(e))
            #    report_location, report_path, scilista_item = [None, None, None]

            if scilista_item is not None:
                scilista.append(scilista_item)
                if config.is_enabled_transference:
                    transfer_website_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_server, config.remote_web_app_path)

            if report_location is not None:
                if config.is_windows:
                    pkg_reports.display_report(report_location)
                else:
                    link = converter_env.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
                    report_location = '<html><body>' + html_reports.link(link, link) + '</body></html>'

                    transfer_report_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_server, config.remote_web_app_path)
                if config.email_subject_package_evaluation is not None:
                    send_message(mailer, config.email_to, config.email_subject_package_evaluation + ' ' + package_folder + ': ' + results, report_location)

        if len(invalid_pkg_files) > 0:
            send_message(mailer, config.email_to, config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n'.join(invalid_pkg_files))
        if len(bad_pkg_files) > 0:
            send_message(mailer, config.email_to_adm, config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n'.join(bad_pkg_files) + '\n'.join(bad_pkg_files_errors))

        if len(scilista) > 0 and config.collection_scilista is not None:
            open(config.collection_scilista, 'a+').write('\n'.join(scilista) + '\n')
    print('finished')


def prepare_env(config):
    global converter_env

    if converter_env is None:
        converter_env = ConverterEnv()

    converter_env.db_isis = dbm_isis.IsisDAO(dbm_isis.UCISIS(dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660)))

    update_issue_copy(config.issue_db, config.issue_db_copy)
    converter_env.db_isis.update_indexes(config.issue_db_copy, config.issue_db_copy + '.fst')
    converter_env.db_issue = xc_models.IssueDAO(converter_env.db_isis, config.issue_db_copy)

    import institutions_service

    org_manager = institutions_service.OrgManager()
    org_manager.load()

    converter_env.db_article = xc_models.ArticleDAO(converter_env.db_isis, org_manager)

    converter_env.local_web_app_path = config.local_web_app_path
    converter_env.serial_path = config.serial_path
    converter_env.version = '1.0'
    converter_env.is_windows = config.is_windows
    converter_env.web_app_site = config.web_app_site
    converter_env.skip_identical_xml = config.skip_identical_xml
