# coding=utf-8

import os
import shutil
from datetime import datetime

from __init__ import _
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


converter_report_lines = []
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

CONFIG_PATH = CURRENT_PATH + '/../config/'
converter_env = None


categories_messages = {
    'converted': _('converted'), 
    'rejected': _('rejected'), 
    'not converted': _('not converted'), 
    'skipped': _('skipped conversion'), 
    'deleted ex-aop': _('deleted ex-aop'), 
    'deleted incorrect order': _('deleted incorrect order'), 
    'not deleted ex-aop': _('not deleted ex-aop'), 
    'new aop': _('aop version'), 
    'new doc': _('doc has no aop'), 
    'ex aop': _('aop is published in an issue'), 
    'matched aop': _('doc has aop version'), 
    'partially matched aop': _('doc has aop version partially matched (title/author are similar)'), 
    'aop missing PID': _('doc has aop version which has no PID'), 
    'unmatched aop': _('doc has an invalid aop version (title/author are not the same)'), 
}


class ConverterEnv(object):

    def __init__(self):
        self.version = None
        self.local_web_app_path = None
        self.serial_path = None
        self.is_windows = None
        self.db_manager = None


def register_log(message):
    if not '<' in message:
        message = html_reports.p_message(message)
    converter_report_lines.append(message)


def find_i_record(issue_label, print_issn, e_issn):
    i_record = None
    issues_records = converter_env.db_manager.db_issue.search(issue_label, print_issn, e_issn)
    if len(issues_records) > 0:
        i_record = issues_records[0]
    return i_record


def complete_issue_items_row(article, action, result, source, notes='', results=False):
    if results:
        labels = ['name', 'package or database', 'creation date | last update', 'action', 'result', 'order', 'pages', 'notes', 'aop PID', 'doi', 'article title']
    else:
        labels = ['name', 'package or database', 'creation date | last update', 'action', 'order', 'pages', 'notes', 'aop PID', 'doi', 'article title']
    _source = source
    if source == 'registered':
        _source = 'database'
        _dates = str(article.creation_date_display) + ' / ' + str(article.last_update)
        action = ''
    else:
        _dates = ''

    values = []
    values.append(article.xml_name)
    values.append(_source)
    values.append(_dates)
    values.append(action)
    if results:
        values.append(result)
    values.append(article.order)
    values.append(article.pages)
    values.append(notes)
    values.append(article.previous_pid)
    values.append(article.doi)
    values.append(article.title)
    return (labels, values)


def display_status_before_xc(registered_articles, pkg_articles, actions, status_column_label='action'):
    orders = [article.order for article in registered_articles.values()]
    for article in pkg_articles.values():
        if article.tree is None:
            orders.append('None')
        else:
            orders.append(article.order)

    orders = sorted(list(set([order for order in orders if order is not None])))

    sorted_registered = pkg_reports.articles_sorted_by_order(registered_articles)
    sorted_package = pkg_reports.articles_sorted_by_order(pkg_articles)
    items = []

    for order in orders:
        action = ''
        if order in sorted_registered.keys():
            for article in sorted_registered[order]:
                action = actions[article.xml_name]
                _notes = ''
                if action == 'update':
                    if registered_articles[article.xml_name].order != pkg_articles[article.xml_name].order:
                        action = 'delete'
                        _notes = 'new order=' + pkg_articles[article.xml_name].order
                labels, values = complete_issue_items_row(article, '', '', 'registered', _notes)
                items.append(pkg_reports.label_values(labels, values))

        if order in sorted_package.keys():
            for article in sorted_package[order]:
                action = actions[article.xml_name]
                _notes = ''
                if registered_articles.get(article.xml_name) is not None:
                    if registered_articles[article.xml_name].order != pkg_articles[article.xml_name].order:
                        _notes = _('replacing ') + registered_articles[article.xml_name].order
                labels, values = complete_issue_items_row(article, action, '', 'package', _notes)
                items.append(pkg_reports.label_values(labels, values))
    return html_reports.sheet(labels, items, 'dbstatus', 'action')


def display_status_after_xc(previous_registered_articles, registered_articles, pkg_articles, actions, unmatched_orders):
    actions_result_labels = {'delete': 'deleted', 'update': 'updated', 'add': 'added', '-': '-', 'skip-update': 'skipped', 'order changed': 'order changed', 'fail': 'update/add failed'}
    orders = sorted(list(set([article.order for article in previous_registered_articles.values()] + [article.order for article in registered_articles.values()] + [article.order if article.tree is not None else 'None' for article in pkg_articles.values()])))

    sorted_previous_registered = pkg_reports.articles_sorted_by_order(previous_registered_articles)
    sorted_registered = pkg_reports.articles_sorted_by_order(registered_articles)
    sorted_package = pkg_reports.articles_sorted_by_order(pkg_articles)

    items = []

    for order in orders:
        if order in sorted_registered.keys():
            # documento na base
            for article in sorted_registered[order]:
                action = actions[article.xml_name]
                result = actions_result_labels[action]
                _notes = ''
                if action == 'update':
                    if article.last_update is None:
                        result = 'error'
                    elif previous_registered_articles.get(article.xml_name).last_update == article.last_update:
                        result = 'error'
                    name = article.xml_name
                    if name in unmatched_orders.keys():
                        previous_order, new_order = unmatched_orders[name]
                        _notes = previous_order + '=>' + new_order
                        if result == 'error':
                            _notes = 'ERROR: ' + _('Unable to replace ') + _notes
                labels, values = complete_issue_items_row(article, action, result, 'registered', _notes, True)
                items.append(pkg_reports.label_values(labels, values))
        elif order in sorted_package.keys():
            # documento no pacote mas nao na base
            for article in sorted_package[order]:
                action = actions[article.xml_name]
                name = article.xml_name
                _notes = ''
                if name in unmatched_orders.keys():
                    previous_order, new_order = unmatched_orders[name]
                    _notes = previous_order + '=>' + new_order
                    _notes = 'ERROR: ' + _('Unable to replace ') + _notes

                labels, values = complete_issue_items_row(article, action, 'error', 'package', _notes, True)
                items.append(pkg_reports.label_values(labels, values))
        elif order in sorted_previous_registered.keys():
            # documento anteriormente na base
            for article in sorted_previous_registered[order]:
                action = 'delete'
                name = article.xml_name
                _notes = ''
                if name in unmatched_orders.keys():
                    previous_order, new_order = unmatched_orders[name]
                    _notes = 'deleted ' + previous_order + '=> new: ' + new_order
                labels, values = complete_issue_items_row(article, '?', 'deleted', 'excluded', _notes, True)
                items.append(pkg_reports.label_values(labels, values))
    return html_reports.sheet(labels, items, 'dbstatus', 'result')


def normalized_package(src_path, report_path, wrk_path, pkg_path, version):
    xml_filenames = sorted([src_path + '/' + f for f in os.listdir(src_path) if f.endswith('.xml') and not 'incorrect' in f])
    articles, doc_file_info_items = xpmaker.make_package(xml_filenames, report_path, wrk_path, pkg_path, version, 'acron')
    return (xml_filenames, articles, doc_file_info_items)


def convert_package(src_path):
    validations_report = None
    xc_conclusion_msg = ''
    conversion_status = {}
    pkg_quality_fatal_errors = 0
    xc_results_report = ''
    aop_results_report = ''
    before_conversion_report = ''
    after_conversion_report = ''
    acron_issue_label = _('unidentified ') + os.path.basename(src_path)[:-4]
    scilista_item = None
    issue_files = None
    ex_aop_items = None
    report_components = {}

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
            #utils.debugging(path)

    xml_filenames, pkg_articles, doc_file_info_items = normalized_package(src_path, report_path, wrk_path, pkg_path, converter_env.version)

    pkg_manager = pkg_reports.PkgManager(pkg_articles)
    pkg_manager.is_db_generation = True

    pkg_manager.issue_models, issue_error_msg = converter_env.db_manager.get_issue_models(pkg_manager.pkg_journal_title, pkg_manager.pkg_issue_label, pkg_manager.pkg_p_issn, pkg_manager.pkg_e_issn)

    if issue_error_msg is not None:
        report_components['issue-report'] = issue_error_msg

    report_components['pkg_overview'] = pkg_manager.overview_report()
    report_components['pkg_overview'] += pkg_manager.references_overview_report()
    report_components['references'] = pkg_manager.sources_overview_report()

    if pkg_manager.issue_models is None:
        acron_issue_label = 'not_registered' + ' ' + os.path.basename(src_path)[:-4]
    else:
        pkg_manager.issue_files = converter_env.db_manager.get_issue_files(pkg_manager.issue_models, pkg_path)
        acron_issue_label = pkg_manager.issue_models.issue.acron + ' ' + pkg_manager.issue_models.issue.issue_label

        previous_registered_articles = get_registered_articles(pkg_manager.issue_files)

        if converter_env.skip_identical_xml:
            pkg_manager.select_articles_to_convert(previous_registered_articles, pkg_path, base_source_path=issue_files.base_source_path)
        else:
            pkg_manager.select_articles_to_convert(previous_registered_articles)

        #utils.debugging('display_status_before_xc')
        before_conversion_report = html_reports.tag('h4', _('Documents status in the package/database - before conversion'))
        before_conversion_report += display_status_before_xc(previous_registered_articles, pkg_articles, pkg_manager.actions)

        report_components['issue-report'] = pkg_manager.issue_report

        if len(pkg_manager.selected_articles) > 0:

            pkg_manager.validate_articles_pkg_xml_and_data(converter_env.db_manager.db_article.org_manager, doc_file_info_items, dtd_files, False)
            pkg_quality_fatal_errors = pkg_manager.pkg_xml_structure_validations.fatal_errors + pkg_manager.pkg_xml_content_validations.fatal_errors

            scilista_item, pkg_manager.pkg_conversion_results, conversion_status, aop_status = convert_articles(issue_files, pkg_manager, previous_registered_articles, pkg_path)
            if scilista_item is not None:
                if aop_status is not None:
                    if aop_status.get('updated bases') is not None:
                        ex_aop_items = []

                        for _aop in aop_status.get('updated bases'):
                            ex_aop_items.append(converter_env.db_manager.issue_models.issue.acron + ' ' + _aop)

            report_components['conversion-report'] = pkg_manager.pkg_conversion_results.report()

            #utils.debugging('detail_report')
            validations_report = pkg_manager.detail_report()

            if pkg_manager.pkg_conversion_results.fatal_errors == 0:
                #utils.debugging('after_conversion_report')
                after_conversion_report = html_reports.tag('h4', _('Documents status in the package/database - after conversion'))
                #utils.debugging('after_conversion_report')
                after_conversion_report += display_status_after_xc(previous_registered_articles, get_registered_articles(issue_files), pkg_articles, pkg_manager.actions, pkg_manager.changed_orders)

            #utils.debugging('xc_results_report')
            xc_results_report = html_reports.tag('h3', _('Conversion results')) + report_status(conversion_status, 'conversion')

            #utils.debugging('aop_results_report')
            aop_results_report = _('this journal has no aop.')
            if not aop_status is None:
                aop_results_report = report_status(aop_status, 'aop-block')
            aop_results_report = html_reports.tag('h3', _('AOP status')) + aop_results_report

            #sheets = pkg_reports.get_lists_report_text(articles_sheets)

            #utils.debugging('save_reports')
            issue_files.save_reports(report_path)

            report_path = issue_files.base_reports_path
            result_path = issue_files.issue_path

            if scilista_item is not None:
                issue_files.copy_files_to_local_web_app()

        xc_conclusion_msg = xc_conclusion_message(scilista_item, acron_issue_label, pkg_articles, pkg_manager.selected_articles, conversion_status, pkg_quality_fatal_errors)
        if len(after_conversion_report) == 0:
            after_conversion_report = xc_conclusion_msg

    #utils.debugging('-report_location-')
    report_location = report_path + '/xml_converter.html'

    report_components['xml-files'] = pkg_reports.xml_list(pkg_path, xml_filenames)
    if converter_env.is_windows:
        report_components['xml-files'] += pkg_reports.processing_result_location(result_path)

    report_components['db-overview'] = before_conversion_report + after_conversion_report
    report_components['summary-report'] = xc_conclusion_msg + xc_results_report + aop_results_report

    if validations_report is not None:
        report_components['detail-report'] = validations_report

    #utils.debugging('-format_complete_report-')
    xc_validations = pkg_reports.format_complete_report(report_components)
    content = xc_validations.message
    if old_report_path in content:
        content = content.replace(old_report_path, report_path)

    #utils.debugging('-format_email_subject-')
    email_subject = format_email_subject(scilista_item, pkg_manager.selected_articles, pkg_quality_fatal_errors, xc_validations.fatal_errors, xc_validations.errors, xc_validations.warnings)

    #utils.debugging(type(content))
    #utils.debugging('-save_report-')
    pkg_reports.save_report(report_location, [_('XML Conversion (XML to Database)'), acron_issue_label], content)

    #utils.debugging('-saved report-')
    if not converter_env.is_windows:
        #utils.debugging('-format_reports_for_web-')
        format_reports_for_web(report_path, pkg_path, acron_issue_label.replace(' ', '/'))
        #fs_utils.delete_file_or_folder(src_path)

    if old_result_path != result_path:
        fs_utils.delete_file_or_folder(old_result_path)
    #utils.debugging('-fim-')
    return (report_location, scilista_item, acron_issue_label, email_subject, ex_aop_items)


def format_email_subject(scilista_item, selected_articles, pkg_quality_fatal_errors, f, e, w):
    inline_stats = '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(f)), ('errors', str(e)), ('warnings', str(w))]]) + ']'
    if scilista_item is None:
        if selected_articles is None:
            email_subject_status = u"\u274C" + _(' REJECTED ') + inline_stats
        elif len(selected_articles) == 0:
            email_subject_status = _('IGNORED')
        else:
            email_subject_status = u"\u274C" + _(' REJECTED ') + inline_stats
    elif pkg_quality_fatal_errors > 0:
        email_subject_status = u"\u2713" + ' ' + u"\u270D" + _(' ACCEPTED but corrections required ') + inline_stats
    else:
        email_subject_status = u"\u2705" + _(' APPROVED ') + inline_stats
    return email_subject_status


def format_reports_for_web(report_path, pkg_path, issue_path):
    if not os.path.isdir(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path):
        os.makedirs(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path)

    #utils.debugging('format_reports_for_web')
    #utils.debugging('content of ' + report_path)
    #utils.debugging('\n'.join(os.listdir(report_path)))

    for f in os.listdir(report_path):
        if f.endswith('.zip') or f == 'xml_converter.txt':
            os.unlink(report_path + '/' + f)
        else:
            #utils.debugging(report_path + '/' + f)
            content = fs_utils.read_file(report_path + '/' + f)
            content = content.replace('file:///' + pkg_path, '/img/revistas/' + issue_path)
            content = content.replace('file:///' + report_path, '/reports/' + issue_path)
            if isinstance(content, unicode):
                content = content.encode('utf-8')
            fs_utils.write_file(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path + '/' + f, content)


def is_conversion_allowed(pub_year, ref_count, pkg_manager):

    def max_score(quote, score):
        return ((score * quote) / 100) + 1

    doit = False
    score = (ref_count + 20)
    if pkg_manager.pkg_issue_data_validations.fatal_errors == 0:
        if pub_year is not None:
            if pub_year[0:4].isdigit():
                if int(pub_year[0:4]) < (int(datetime.now().isoformat()[0:4]) - 1):
                    #doc anterior a dois anos atrás)
                    doit = True
        if doit is False:
            doit = True
            if converter_env.max_fatal_error is not None:
                if pkg_manager.pkg_xml_structure_validations.fatal_errors + pkg_manager.pkg_xml_content_validations.fatal_errors > max_score(converter_env.max_fatal_error, score):
                    doit = False
            if converter_env.max_error is not None:
                if pkg_manager.pkg_xml_structure_validations.errors + pkg_manager.pkg_xml_content_validations.errors > max_score(converter_env.max_error, score):
                    doit = False
            if converter_env.max_warning is not None:
                if pkg_manager.pkg_xml_structure_validations.warnings + pkg_manager.pkg_xml_content_validations.warnings > max_score(converter_env.max_warning, score):
                    doit = False
    return doit


def convert_articles(issue_files, pkg_manager, registered_articles, pkg_path):
    index = 0
    pkg_conversion_results = pkg_reports.PackageValidationsResults()
    conversion_status = {}

    for k in ['converted', 'rejected', 'not converted', 'skipped', 'deleted incorrect order']:
        conversion_status[k] = []

    n = '/' + str(len(pkg_manager.pkg_articles))

    i_ahead_records = {}
    current_year = datetime.now().isoformat()[0:4]
    for year in range(current_year-2, current_year+1):
        i_ahead_records[year] = find_i_record(year + 'nahead', pkg_manager.issue_models.issue.issn_id, None)

    aop_status = None
    aop_manager = xc_models.AopManager(converter_env.db_isis, issue_files.journal_files, i_ahead_records)
    db_article = xc_models.ArticleDB(converter_env.db_isis, issue_files)

    utils.display_message('Converting...')
    for xml_name in pkg_reports.sorted_xml_name_by_order(pkg_manager.pkg_articles):
        article = pkg_manager.pkg_articles[xml_name]
        index += 1

        item_label = str(index) + n + ' - ' + xml_name
        utils.display_message(item_label)

        msg = ''
        if not pkg_manager.actions[xml_name] in ['add', 'update']:
            xc_result = 'skipped'
        else:
            aop_manager.get_aop(article)

            xc_result = 'None'

            if is_conversion_allowed(article.issue_pub_dateiso, len(article.references), pkg_manager):

                if aop_manager.aop_info.get(article.xml_name) is not None:
                    article._ahead_pid = aop_manager.aop_info.get(article.xml_name)[0].ahead_pid

                article_files = serial_files.ArticleFiles(issue_files, article.order, xml_name)

                article.creation_date = None if not xml_name in registered_articles.keys() else registered_articles[xml_name].creation_date

                saved = db_article.save_article(pkg_manager.issue_models.record, article, article_files)
                if saved:
                    #utils.debugging('convert_articles: unmatched_orders')
                    if xml_name in pkg_manager.changed_orders.keys():
                        prev_order, curr_order = pkg_manager.changed_orders[xml_name]
                        msg += html_reports.p_message('WARNING: ' + _('Replacing orders: ') + prev_order + _(' by ') + curr_order)
                        prev_article_files = serial_files.ArticleFiles(issue_files, prev_order, xml_name)
                        if os.path.isfile(prev_article_files.id_filename):
                            msg += html_reports.p_message('WARNING: ' + _('Deleting ') + os.path.basename(prev_article_files.id_filename))
                            os.unlink(prev_article_files.id_filename)
                        conversion_status['deleted incorrect order'].append(prev_order)

                    #utils.debugging('convert_articles: aop_status is not None')
                    if aop_status is not None:
                        if doc_aop_status in ['matched aop', 'partially matched aop']:
                            saved, aop_msg = aop_manager.manage_ex_aop(valid_aop)
                            msg += ''.join([item for item in aop_msg])
                            if saved:
                                aop_status['deleted ex-aop'].append(xml_name)
                                msg += html_reports.p_message('INFO: ' + _('ex aop was deleted'))
                            else:
                                aop_status['not deleted ex-aop'].append(xml_name)
                                msg += html_reports.p_message('ERROR: ' + _('Unable to delete ex aop'))
                    xc_result = 'converted'
                else:
                    xc_result = 'not converted'
            else:
                xc_result = 'rejected'

        conversion_status[xc_result].append(xml_name)

        msg += html_reports.p_message(_('Result: ') + xc_result)
        if not xc_result in ['converted', 'skipped']:
            msg += html_reports.p_message('FATAL ERROR')
        pkg_conversion_results.add(xml_name, pkg_reports.ValidationsResults(msg))

    #utils.debugging('convert_articles: journal_has_aop()')
    if aop_manager.journal_publishes_aop():
        if aop_status is None:
            aop_status = {}
        aop_status['updated bases'] = aop_manager.update_all_aop_db()
        aop_status['still aop'] = aop_manager.still_aop_items()

    scilista_item = None
    #utils.debugging('convert_articles: conclusion')
    if pkg_conversion_results.fatal_errors == 0:
        saved = db_article.finish_conversion(pkg_path)
        if saved > 0:
            scilista_item = pkg_manager.issue_models.issue.acron + ' ' + pkg_manager.issue_models.issue.issue_label
            if not converter_env.is_windows:
                db_article.generate_windows_version()
    #utils.debugging('convert_articles: fim')
    return (scilista_item, pkg_conversion_results, conversion_status, aop_status)


def aop_message(article, ahead, status):
    data = []
    msg_list = []
    if status == 'new aop':
        msg_list.append('INFO: ' + _('This document is an "aop".'))
    else:
        msg_list.append(_('Checking if ') + article.xml_name + _(' has an "aop version"'))
        if article.doi is not None:
            msg_list.append(_('Checking if ') + article.doi + _(' has an "aop version"'))

        if status == 'new doc':
            msg_list.append('WARNING: ' + _('Not found an "aop version" of this document.'))
        else:
            msg_list.append('WARNING: ' + _('Found: "aop version"'))
            if status == 'partially matched aop':
                msg_list.append('WARNING: ' + _('the title/author of article and its "aop version" are similar.'))
            elif status == 'aop missing PID':
                msg_list.append('ERROR: ' + _('the "aop version" has no PID'))
            elif status == 'unmatched aop':
                status = 'unmatched aop'
                msg_list.append('FATAL ERROR: ' + _('the title/author of article and "aop version" are different.'))

            t = '' if article.title is None else article.title
            data.append(_('doc title') + ':' + t)
            t = '' if ahead.article_title is None else ahead.article_title
            data.append(_('aop title') + ':' + t)
            t = '' if article.first_author_surname is None else article.first_author_surname
            data.append(_('doc first author') + ':' + t)
            t = '' if ahead.first_author_surname is None else ahead.first_author_surname
            data.append(_('aop first author') + ':' + t)
    msg = ''
    msg += html_reports.tag('h5', _('Checking existence of aop version'))
    msg += ''.join([html_reports.p_message(item) for item in msg_list])
    msg += ''.join([html_reports.display_xml(item, html_reports.XML_WIDTH*0.9) for item in data])
    return msg


def get_registered_articles(issue_files):
    registered_issue_models, registered_articles = converter_env.db_manager.db_article.registered_items(issue_files)
    return registered_articles


def report_status(status, style=None):
    text = ''
    for category in sorted(status.keys()):
        _style = style
        if len(status[category]) == 0:
            ltype = 'ul'
            list_items = ['None']
            _style = None
        else:
            ltype = 'ol'
            list_items = status[category]
        text += html_reports.format_list(categories_messages.get(category, category), ltype, list_items, _style)

    return text


def xc_conclusion_message(scilista_item, issue_label, pkg_articles, selected_articles, xc_status, pkg_quality_fatal_errors):
    total = len(selected_articles) if selected_articles is not None else 0
    converted = len(xc_status.get('converted', []))
    failed = total - converted
    app_site = converter_env.web_app_site if converter_env.web_app_site is not None else _('scielo web site')
    status = ''
    action = ''
    result = _('be updated/published on ') + app_site
    reason = ''
    if scilista_item is None:
        action = _(' not')
        if selected_articles is None:
            status = 'FATAL ERROR'
            reason = _('because there are errors in the package.')
        elif len(selected_articles) == 0:
            status = 'WARNING'
            reason = _('because no document was changed.')
        elif failed > 0:
            status = 'FATAL ERROR'
            reason = _('because it is not complete (') + str(failed) + _(' were not converted).')
        else:
            status = 'FATAL ERROR'
            reason = _('because it was unable to save the database.')
    else:
        if pkg_quality_fatal_errors > 0:
            status = 'WARNING'
            reason = _(' even though there are some fatal errors. Note: These errors must be fixed in order to have good quality of bibliometric indicators and services.')
        else:
            status = 'OK'
            reason = ''

    text = status + ': ' + issue_label + _(' will') + action + ' ' + result + ' ' + reason
    text = html_reports.tag('h2', _('Summary report')) + html_reports.p_message(_('converted') + ': ' + str(converted) + '/' + str(total)) + html_reports.p_message(text)
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


def queue_packages(download_path, temp_path, queue_path, archive_path):
    invalid_pkg_files = []
    proc_id = datetime.now().isoformat()[11:16].replace(':', '')
    temp_path = temp_path + '/' + proc_id
    queue_path = queue_path + '/' + proc_id
    pkg_paths = []

    if os.path.isdir(temp_path):
        fs_utils.delete_file_or_folder(temp_path)
    if os.path.isdir(queue_path):
        fs_utils.delete_file_or_folder(queue_path)

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
            errors.append(_('Missing collection acronym'))
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
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append('ERROR: ' + _('No configuration file was informed'))
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append('ERROR: ' + _('unable to read XML Converter configuration file: ') + configuration_filename)
    return messages


def is_valid_pkg_file(filename):
    return os.path.isfile(filename) and (filename.endswith('.zip') or filename.endswith('.tgz'))


def update_db_copy(isis_db, isis_db_copy, fst_file):
    d = os.path.dirname(isis_db_copy)
    if not os.path.isdir(d):
        os.makedirs(d)
    if not os.path.isfile(isis_db_copy + '.fst'):
        shutil.copyfile(fst_file, isis_db_copy + '.fst')
    if fs_utils.read_file(fst_file) != fs_utils.read_file(isis_db_copy + '.fst'):
        shutil.copyfile(fst_file, isis_db_copy + '.fst')
    shutil.copyfile(isis_db + '.mst', isis_db_copy + '.mst')
    shutil.copyfile(isis_db + '.xrf', isis_db_copy + '.xrf')


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
            messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
            messages.append('ERROR: ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python xml_converter.py <xml_folder> | <collection_acron>')
            messages.append(_('where') + ':')
            messages.append('  <xml_folder> = ' + _('path of folder which contains'))
            messages.append('  <collection_acron> = ' + _('collection acron'))
            messages.append('\n'.join(errors))
            utils.display_message('\n'.join(messages))
        else:
            execute_converter(package_path, collection_acron)
    elif collection_acron is not None:
        execute_converter(package_path, collection_acron)
    elif package_path is not None:
        execute_converter(package_path)


def send_message(mailer, to, subject, text, attaches=None):
    if mailer is not None:
        #utils.debugging('sending message ' + subject)
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
            utils.display_message(package_path)
            try:
                report_location, scilista_item, acron_issue_label, results, ex_aop_items = convert_package(package_path)
                acron, issue_id = acron_issue_label.split(' ')
            except Exception as e:
                utils.display_message('-'*10)
                utils.display_message('XCINTERRUPTED')
                utils.display_message(package_path)
                utils.display_message(e)
                utils.display_message('-'*10)
                #raise
                bad_pkg_files.append(package_path)
                bad_pkg_files.append(str(e))
                report_location, report_path, scilista_item = [None, None, None]
                if config.queue_path is not None:
                    fs_utils.delete_file_or_folder(package_path)

            if scilista_item is not None:
                if ex_aop_items is not None:
                    for ex_aop_item in ex_aop_items:
                        scilista.append(ex_aop_item)
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
                    send_message(mailer, config.email_to, config.email_subject_package_evaluation + u' ' + package_folder + u': ' + results, report_location)

        if len(invalid_pkg_files) > 0:
            send_message(mailer, config.email_to, config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n'.join(invalid_pkg_files))
        if len(bad_pkg_files) > 0:
            send_message(mailer, config.email_to_adm, 'x ' + config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n'.join(bad_pkg_files))

        if len(scilista) > 0 and config.collection_scilista is not None:
            open(config.collection_scilista, 'a+').write('\n'.join(scilista) + '\n')
    utils.display_message(_('finished'))


def prepare_env(config):
    global converter_env

    if converter_env is None:
        converter_env = ConverterEnv()

    import institutions_service

    org_manager = institutions_service.OrgManager()
    org_manager.load()

    db_isis = dbm_isis.IsisDAO(dbm_isis.UCISIS(dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660)))
    converter_env.db_manager = xc_models.DBManager(db_isis, config.title_db_copy, config.issue_db_copy, org_manager, config.serial_path, config.local_web_app_path)

    update_db_copy(config.issue_db, config.issue_db_copy, CURRENT_PATH + '/issue.fst')
    converter_env.db_manager.db_isis.update_indexes(config.issue_db_copy, config.issue_db_copy + '.fst')

    update_db_copy(config.title_db, config.title_db_copy, CURRENT_PATH + '/title.fst')
    converter_env.db_manager.db_isis.update_indexes(config.title_db_copy, config.title_db_copy + '.fst')

    converter_env.local_web_app_path = config.local_web_app_path
    converter_env.version = '1.0'
    converter_env.is_windows = config.is_windows
    converter_env.web_app_site = config.web_app_site
    converter_env.skip_identical_xml = config.skip_identical_xml
    converter_env.max_fatal_error = config.max_fatal_error
    converter_env.max_error = config.max_error
    converter_env.max_warning = config.max_warning
