# coding=utf-8

import os
import shutil
from datetime import datetime

from __init__ import _
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
    'excluded ex-aop': _('excluded ex-aop'), 
    'excluded incorrect order': _('excluded incorrect order'), 
    'not excluded incorrect order': _('not excluded incorrect order'), 
    'not excluded ex-aop': _('not excluded ex-aop'), 
    'new aop': _('aop version'), 
    'new doc': _('doc has no aop'), 
    'ex aop': _('aop is published in an issue'), 
    'matched aop': _('doc has aop version'), 
    'partially matched aop': _('doc has aop version partially matched (title/author are similar)'), 
    'aop missing PID': _('doc has aop version which has no PID'), 
    'unmatched aop': _('doc has an invalid aop version (title/author are not the same)'), 
}


XC_STATUS = {}
XC_STATUS['rejected'] = [u"\u274C", _(' REJECTED ')]
XC_STATUS['ignored'] = ['', _('IGNORED')]
XC_STATUS['accepted'] = [u"\u2713" + ' ' + u"\u270D", _(' ACCEPTED but corrections required ')]
XC_STATUS['approved'] = [u"\u2705", _(' APPROVED ')]
XC_STATUS['not processed'] = ['', _(' NOT PROCESSED ')]


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
    return (articles, doc_file_info_items)


class Conversion(object):

    def __init__(self, pkg, db):
        self.pkg = pkg
        self.db = db
        self.actions = None
        self.changed_orders = None
        self.conversion_status = {}

        for k in ['converted', 'not converted', 'rejected', 'skipped', 'excluded incorrect order', 'not excluded incorrect order']:
            self.conversion_status[k] = []

    def evaluate_pkg_and_registered_items(self, skip_identical_xml):
        #actions = {'add': [], 'skip-update': [], 'update': [], '-': [], 'changed order': []}
        self.previous_registered_articles = {}
        if self.db.registered_articles is not None:
            for k, v in self.db.registered_articles.items():
                self.previous_registered_articles[k] = v

        self.expected_registered = len(self.previous_registered_articles)

        self.actions = {}
        for name in self.previous_registered_articles.keys():
            if not name in self.pkg.articles.keys():
                self.actions[name] = '-'
                #self.complete_issue_items[name] = self.previous_registered_articles[name]
        self.changed_orders = {}
        for name, article in self.pkg.articles.items():
            action = 'add'
            if name in self.previous_registered_articles.keys():
                action = 'update'
                if skip_identical_xml:
                    if fs_utils.read_file(self.pkg.issue_files.base_source_path + '/' + name + '.xml') == fs_utils.read_file(self.pkg.pkg_path + '/' + name + '.xml'):
                        action = 'skip-update'
                if action == 'update':
                    self.pkg.articles[name].creation_date = self.previous_registered_articles[name].creation_date
                    if self.previous_registered_articles[name].order != self.pkg.articles[name].order:
                        self.changed_orders[name] = (self.previous_registered_articles[name].order, self.pkg.articles[name].order)
            self.actions[name] = action
            if action == 'add':
                self.expected_registered += 1
        unmatched_orders_errors = ''
        if self.changed_orders is not None:
            unmatched_orders_errors = ''.join([html_reports.p_message('WARNING: ' + _('orders') + ' ' + _('of') + ' ' + name + ': ' + ' -> '.join(list(order))) for name, order in self.changed_orders.items()])
        self.changed_orders_validations = pkg_reports.ValidationsResults(unmatched_orders_errors)

    @property
    def selected_articles(self):
        _selected_articles = None
        if self.blocking_errors == 0:
            #utils.debugging('toc_f == 0')
            _selected_articles = {}
            for xml_name, status in self.actions.items():
                if status in ['add', 'update']:
                    _selected_articles[xml_name] = self.pkg.articles[xml_name]
        return _selected_articles

    def initial_status_report(self):
        report = html_reports.tag('h4', _('Documents status in the package/database - before conversion'))

        orders = [article.order for article in self.previous_registered_articles.values()]
        for article in self.pkg.articles.values():
            if article.tree is None:
                orders.append('None')
            else:
                orders.append(article.order)

        orders = sorted(list(set([order for order in orders if order is not None])))

        sorted_registered = pkg_reports.articles_sorted_by_order(self.previous_registered_articles)
        sorted_package = pkg_reports.articles_sorted_by_order(self.pkg.articles)
        items = []

        for order in orders:
            action = ''
            if order in sorted_registered.keys():
                for article in sorted_registered[order]:
                    action = self.actions[article.xml_name]
                    _notes = ''
                    if action == 'update':
                        if self.previous_registered_articles[article.xml_name].order != self.pkg.articles[article.xml_name].order:
                            action = 'delete'
                            _notes = 'new order=' + self.pkg.articles[article.xml_name].order
                    labels, values = complete_issue_items_row(article, '', '', 'registered', _notes)
                    items.append(pkg_reports.label_values(labels, values))

            if order in sorted_package.keys():
                for article in sorted_package[order]:
                    action = self.actions[article.xml_name]
                    _notes = ''
                    if self.previous_registered_articles.get(article.xml_name) is not None:
                        if self.previous_registered_articles[article.xml_name].order != self.pkg.articles[article.xml_name].order:
                            _notes = _('replacing ') + self.previous_registered_articles[article.xml_name].order
                    labels, values = complete_issue_items_row(article, action, '', 'package', _notes)
                    items.append(pkg_reports.label_values(labels, values))
        return report + html_reports.sheet(labels, items, 'dbstatus', 'action')

    def final_status_report(self):
        actions_result_labels = {'delete': 'deleted', 'update': 'updated', 'add': 'added', '-': '-', 'skip-update': 'skipped', 'order changed': 'order changed', 'fail': 'update/add failed'}
        orders = sorted(list(set([article.order for article in self.previous_registered_articles.values()] + [article.order for article in self.db.registered_articles.values()] + [article.order if article.tree is not None else 'None' for article in self.pkg.articles.values()])))

        sorted_previous_registered = pkg_reports.articles_sorted_by_order(self.previous_registered_articles)
        sorted_registered = pkg_reports.articles_sorted_by_order(self.db.registered_articles)
        sorted_package = pkg_reports.articles_sorted_by_order(self.pkg.articles)

        items = []

        for order in orders:
            if order in sorted_registered.keys():
                # documento na base
                for article in sorted_registered[order]:
                    action = self.actions[article.xml_name]
                    result = actions_result_labels[action]
                    _notes = ''
                    if action == 'update':
                        if article.last_update is None:
                            result = 'error'
                        elif self.previous_registered_articles.get(article.xml_name).last_update == article.last_update:
                            result = 'error'
                        name = article.xml_name
                        if name in self.changed_orders.keys():
                            previous_order, new_order = self.changed_orders[name]
                            _notes = previous_order + '=>' + new_order
                            if result == 'error':
                                _notes = 'ERROR: ' + _('Unable to replace ') + _notes
                    labels, values = complete_issue_items_row(article, action, result, 'registered', _notes, True)
                    items.append(pkg_reports.label_values(labels, values))
            elif order in sorted_package.keys():
                # documento no pacote mas nao na base
                for article in sorted_package[order]:
                    action = self.actions[article.xml_name]
                    name = article.xml_name
                    _notes = ''
                    if name in self.changed_orders.keys():
                        previous_order, new_order = self.changed_orders[name]
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
                    if name in self.changed_orders.keys():
                        previous_order, new_order = self.changed_orders[name]
                        _notes = 'deleted ' + previous_order + '=> new: ' + new_order
                    labels, values = complete_issue_items_row(article, '?', 'deleted', 'excluded', _notes, True)
                    items.append(pkg_reports.label_values(labels, values))
        after_conversion_report = html_reports.tag('h4', _('Documents status in the package/database - after conversion'))
        after_conversion_report += html_reports.sheet(labels, items, 'dbstatus', 'result')
        return after_conversion_report

    def convert_articles(self, pkg_validator):
        index = 0

        n = '/' + str(len(self.pkg.articles))

        utils.display_message('Converting...')
        for xml_name in self.pkg.xml_name_sorted_by_order:
            index += 1
            item_label = str(index) + n + ' - ' + xml_name
            utils.display_message(item_label)

            xc_result = None
            if not self.actions[xml_name] in ['add', 'update']:
                xc_result = 'skipped'
            else:
                self.db.aop_manager.check_aop(self.pkg.articles[xml_name])
                permission = is_conversion_allowed(self.pkg.articles[xml_name].issue_pub_dateiso, len(self.pkg.articles[xml_name].references), pkg_validator)

                if permission:
                    valid_aop = self.db.aop_manager.aop_article(xml_name)
                    if valid_aop is not None:
                        self.pkg.articles[xml_name].registered_aop_pid = valid_aop.pid

                    incorrect_order = None
                    if xml_name in self.changed_orders.keys():
                        incorrect_order, curr_order = self.changed_orders[xml_name]

                    normalize_affiliations(self.pkg.articles[xml_name])
                    self.db.evaluate(self.pkg.issue_models.record, self.pkg.articles[xml_name], valid_aop, incorrect_order)
                else:
                    xc_result = 'rejected'
            if xc_result is not None:
                self.conversion_status[xc_result].append(xml_name)

        is_package_registered = self.db.finish_conversion(self.pkg.pkg_path, self.pkg.issue_models.record)
        self.conversion_status['converted'] = self.db.is_converted
        self.conversion_status['not converted'] = self.db.is_not_converted

        registered_scilista_item = None
        if is_package_registered is True:
            registered_scilista_item = self.pkg.acron_issue_label
            if not converter_env.is_windows:
                self.db.generate_windows_version()
        return registered_scilista_item

    @property
    def pkg_xc_validations(self):
        validations = pkg_reports.PackageValidationsResults(self.pkg.issue_files.base_reports_path, 'xc-', '')
        for xml_name, messages in self.db.registration_reports.items():
            validations.add(xml_name, pkg_reports.ValidationsResults(''.join(messages)))
        validations.save_reports()
        return validations


def conclusion_message(total, converted, not_converted, xc_status, acron_issue_label):
    app_site = converter_env.web_app_site if converter_env.web_app_site is not None else _('scielo web site')
    status = ''
    action = ''
    result = _('be updated/published on ') + app_site
    reason = ''
    if xc_status == 'rejected':
        action = _(' not')
        status = 'FATAL ERROR'
        if total > 0:
            if not_converted > 0:
                reason = _('because it is not complete (') + str(not_converted) + '/' + str(total) + _(' were not converted).')
            else:
                reason = _('unknown')
        else:
            reason = _('because there are blocking errors in the package.')
    elif xc_status == 'ignored':
        action = _(' not')
        reason = _('because no document was changed.')
    elif xc_status == 'accepted':
        status = 'WARNING'
        reason = _(' even though there are some fatal errors. Note: These errors must be fixed in order to have good quality of bibliometric indicators and services.')
    elif xc_status == 'approved':
        status = 'OK'
        reason = ''
    else:
        status = 'FATAL ERROR'
        reason = _('because there are blocking errors in the package.')
    text = status + ': ' + acron_issue_label + _(' will') + action + ' ' + result + ' ' + reason
    text = html_reports.tag('h2', _('Summary report')) + html_reports.p_message(_('converted') + ': ' + str(converted) + '/' + str(total)) + html_reports.p_message(text)
    return text


def package_paths_preparation(src_path):
    result_path = src_path + '_xml_converter_result'
    wrk_path = result_path + '/work'
    pkg_path = result_path + '/scielo_package'
    report_path = result_path + '/errors'

    for path in [result_path, wrk_path, pkg_path, report_path]:
        if not os.path.isdir(path):
            os.makedirs(path)
    return (report_path, wrk_path, pkg_path, result_path)


def convert_package(src_path):
    xc_conclusion_msg = ''
    pkg_xml_fatal_errors = 0
    xc_results_report = ''
    aop_results_report = ''
    before_conversion_report = ''
    after_conversion_report = ''
    registered_scilista_item = None
    report_components = {}
    scilista_items = []
    xc_status = 'not processed'
    is_db_generation = True
    converted = 0
    not_converted = 0
    total = 0

    dtd_files = xml_versions.DTDFiles('scielo', converter_env.version)

    pkg_name = os.path.basename(src_path)[:-4]

    log_package = './' + datetime.now().isoformat().replace(':', '_') + os.path.basename(pkg_name)

    fs_utils.append_file(log_package, 'preparing')
    tmp_report_path, wrk_path, pkg_path, tmp_result_path = package_paths_preparation(src_path)
    final_result_path = tmp_result_path
    final_report_path = tmp_report_path

    fs_utils.append_file(log_package, 'normalized_package')
    pkg_articles, doc_file_info_items = normalized_package(src_path, tmp_report_path, wrk_path, pkg_path, converter_env.version)

    pkg = pkg_reports.PkgArticles(pkg_articles, pkg_path)

    fs_utils.append_file(log_package, 'identify_issue')
    issue_error_msg = pkg.identify_issue(converter_env.db_manager, pkg_name)

    fs_utils.append_file(log_package, 'pkg.xml_list()')
    report_components['xml-files'] = pkg.xml_list()

    scilista_items.append(pkg.acron_issue_label)
    if issue_error_msg is not None:
        xc_status = 'rejected'
        report_components['issue-report'] = issue_error_msg
    else:

        fs_utils.append_file(log_package, 'db_article')
        db_article = xc_models.ArticleDB(converter_env.db_manager.db_isis, pkg.issue_files, xc_models.AopManager(converter_env.db_manager.db_isis, pkg.issue_files.journal_files))

        conversion = Conversion(pkg, db_article)

        fs_utils.append_file(log_package, 'conversion.evaluate_pkg_and_registered_items')
        conversion.evaluate_pkg_and_registered_items(converter_env.skip_identical_xml)

        pkg_validator = pkg_reports.ArticlesPkgReport(tmp_report_path, pkg, conversion.previous_registered_articles, is_db_generation)

        fs_utils.append_file(log_package, 'pkg_validator.overview_report()')
        report_components['pkg_overview'] = pkg_validator.overview_report()

        fs_utils.append_file(log_package, 'pkg_validator.references_overview_report()')
        report_components['pkg_overview'] += pkg_validator.references_overview_report()

        fs_utils.append_file(log_package, 'pkg_validator.sources_overview_report()')
        report_components['references'] = pkg_validator.sources_overview_report()

        fs_utils.append_file(log_package, 'pkg_validator.issue_report')
        report_components['issue-report'] = pkg_validator.issue_report

        conversion.blocking_errors = pkg_validator.blocking_errors

        fs_utils.append_file(log_package, 'conversion.initial_status_report')
        before_conversion_report = conversion.initial_status_report()

        if conversion.blocking_errors == 0:

            fs_utils.append_file(log_package, 'pkg_validator.validate_articles_pkg_xml_and_data')

            pkg_validator.validate_articles_pkg_xml_and_data(converter_env.institution_normalizer, doc_file_info_items, dtd_files, False, conversion.selected_articles.keys())

            pkg_xml_fatal_errors = pkg_validator.pkg_xml_structure_validations.fatal_errors + pkg_validator.pkg_xml_content_validations.fatal_errors

            fs_utils.append_file(log_package, 'pkg_validator.detail_report')
            report_components['detail-report'] = pkg_validator.detail_report()

            fs_utils.append_file(log_package, 'conversion.convert_articles')
            registered_scilista_item = conversion.convert_articles(pkg_validator)

            fs_utils.append_file(log_package, 'conversion.pkg_xc_validations.report')
            report_components['conversion-report'] = conversion.pkg_xc_validations.report()
            if conversion.pkg_xc_validations.fatal_errors == 0:
                after_conversion_report = conversion.final_status_report()

            fs_utils.append_file(log_package, 'Conversion results')
            xc_results_report = report_status(_('Conversion results'), conversion.conversion_status, 'conversion')

            fs_utils.append_file(log_package, 'AOP status')
            aop_results_report = report_status(_('AOP status'), conversion.db.aop_manager.aop_sorted_by_status, 'aop-block')
            if len(aop_results_report) == 0:
                aop_results_report = _('this journal has no aop.')

            final_report_path = pkg.issue_files.base_reports_path
            final_result_path = pkg.issue_files.issue_path

            if registered_scilista_item is not None:
                fs_utils.append_file(log_package, 'pkg.issue_files.copy_files_to_local_web_app()')
                pkg.issue_files.copy_files_to_local_web_app()

            fs_utils.append_file(log_package, 'xc_status = get_xc_status()')
            xc_status = get_xc_status(registered_scilista_item, conversion.pkg_xc_validations.fatal_errors, pkg_xml_fatal_errors, conversion.blocking_errors)

            if conversion.db.aop_manager.aop_sorted_by_status.get('aop scilista item to update') is not None:
                for item in conversion.db.aop_manager.aop_sorted_by_status.get('aop scilista item to update'):
                    scilista_items.append(item)

            total = len(conversion.selected_articles) if conversion.selected_articles is not None else 0
            converted = len(conversion.conversion_status.get('converted', [])) if conversion.conversion_status.get('converted', []) is not None else 0
            not_converted = len(conversion.conversion_status.get('not converted', [])) if conversion.conversion_status.get('not converted', []) is not None else 0

        fs_utils.append_file(log_package, 'conversion.conclusion(')
        xc_conclusion_msg = conclusion_message(total, converted, not_converted, xc_status, pkg.acron_issue_label)
        if len(after_conversion_report) == 0:
            after_conversion_report = xc_conclusion_msg

    if converter_env.is_windows:
        fs_utils.append_file(log_package, 'pkg_reports.processing_result_location')
        report_components['xml-files'] += pkg_reports.processing_result_location(final_result_path)

    report_components['db-overview'] = before_conversion_report + after_conversion_report
    report_components['summary-report'] = xc_conclusion_msg + xc_results_report + aop_results_report

    fs_utils.append_file(log_package, 'pkg_reports.format_complete_report')

    xc_validations = pkg_reports.format_complete_report(report_components)
    content = xc_validations.message
    if tmp_report_path in content:
        fs_utils.append_file(log_package, 'content.replace(tmp_report_path, final_report_path)')
        content = content.replace(tmp_report_path, final_report_path)

    report_location = final_report_path + '/xml_converter.html'
    pkg_reports.save_report(report_location, [_('XML Conversion (XML to Database)'), pkg.acron_issue_label], content)

    if not converter_env.is_windows:
        fs_utils.append_file(log_package, 'format_reports_for_web')
        format_reports_for_web(final_report_path, pkg_path, pkg.acron_issue_label.replace(' ', '/'))

    if tmp_result_path != final_result_path:
        fs_utils.delete_file_or_folder(tmp_result_path)

    fs_utils.append_file(log_package, 'antes de return - convert_package')

    os.unlink(log_package)
    return (scilista_items, xc_status, xc_validations.statistics_message(), report_location)


def get_xc_status(registered_scilista_item, xc_errors, pkg_xml_fatal_errors, blocking_errors):
    if registered_scilista_item is None:
        result = 'rejected'
        if blocking_errors + pkg_xml_fatal_errors + xc_errors == 0:
            result = 'ignored'
    elif pkg_xml_fatal_errors > 0:
        result = 'accepted'
    else:
        result = 'approved'
    return result


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


def is_conversion_allowed(pub_year, ref_count, pkg_validator):

    def max_score(quote, score):
        return ((score * quote) / 100) + 1

    doit = False
    score = (ref_count + 20)
    if pkg_validator.registered_issue_data_validations.fatal_errors == 0:
        if pub_year is not None:
            if pub_year[0:4].isdigit():
                if int(pub_year[0:4]) < (int(datetime.now().isoformat()[0:4]) - 1):
                    #doc anterior a dois anos atrás)
                    doit = True
        if doit is False:
            doit = True
            if converter_env.max_fatal_error is not None:
                if pkg_validator.pkg_xml_structure_validations.fatal_errors + pkg_validator.pkg_xml_content_validations.fatal_errors > max_score(converter_env.max_fatal_error, score):
                    doit = False
            if converter_env.max_error is not None:
                if pkg_validator.pkg_xml_structure_validations.errors + pkg_validator.pkg_xml_content_validations.errors > max_score(converter_env.max_error, score):
                    doit = False
            if converter_env.max_warning is not None:
                if pkg_validator.pkg_xml_structure_validations.warnings + pkg_validator.pkg_xml_content_validations.warnings > max_score(converter_env.max_warning, score):
                    doit = False
    return doit


def report_status(title, status, style=None):
    text = ''
    if status is not None:
        for category in sorted(status.keys()):
            _style = style
            if status.get(category) is None:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            elif len(status[category]) == 0:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            else:
                ltype = 'ol'
                list_items = status[category]
            text += html_reports.format_list(categories_messages.get(category, category), ltype, list_items, _style)
    if len(text) > 0:
        text = html_reports.tag('h3', title) + text
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
    collection_names = {}
    collection_acron = collection_names.get(collection_name)
    if collection_acron is None:
        collection_acron = collection_name

    config = xc.get_configuration(collection_acron)
    if config is not None:
        prepare_env(config)
        invalid_pkg_files = []
        bad_pkg_files = []

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
            scilista_items = []
            xc_status = 'interrupted'
            stats_msg = ''
            report_location = None
            try:
                scilista_items, xc_status, stats_msg, report_location = convert_package(package_path)
            except Exception as e:
                if config.queue_path is not None:
                    fs_utils.delete_file_or_folder(package_path)
                if config.email_subject_invalid_packages is not None:
                    send_message(mailer, config.email_to_adm, '[Step 1]' + config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))
                if len(package_paths) == 1:
                    raise

            try:
                acron, issue_id = scilista_items[0].split(' ')

                if xc_status in ['accepted', 'approved']:
                    if config.collection_scilista is not None:
                        open(config.collection_scilista, 'a+').write('\n'.join(scilista_items) + '\n')

                    if config.is_enabled_transference:
                        transfer_website_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_server, config.remote_web_app_path)

                if report_location is not None:
                    if config.is_windows:
                        pkg_reports.display_report(report_location)

                    if config.email_subject_package_evaluation is not None:
                        results = ' '.join(XC_STATUS.get(xc_status, [])) + ' ' + stats_msg
                        link = converter_env.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
                        report_location = '<html><body>' + html_reports.link(link, link) + '</body></html>'

                        transfer_report_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_server, config.remote_web_app_path)
                        send_message(mailer, config.email_to, config.email_subject_package_evaluation + u' ' + package_folder + u': ' + results, report_location)

            except Exception as e:
                if config.email_subject_invalid_packages is not None:
                    send_message(mailer, config.email_to_adm, '[Step 2]' + config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))

                if len(package_paths) == 1:
                    print('exception as finishing')
                    raise

        if len(invalid_pkg_files) > 0:
            if config.email_subject_invalid_packages is not None:
                send_message(mailer, config.email_to, config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n'.join(invalid_pkg_files))

    utils.display_message(_('finished'))


def normalize_affiliations(article):
    article.normalized_affiliations = {}
    for aff in article.affiliations:
        norm_aff, ign = converter_env.institution_normalizer.normalized_institution(aff)
        if norm_aff is not None:
            article.normalized_affiliations[aff.id] = norm_aff


def prepare_env(config):
    global converter_env

    if converter_env is None:
        converter_env = ConverterEnv()

    import institutions_service

    org_manager = institutions_service.OrgManager()
    org_manager.load()

    from article import InstitutionNormalizer
    converter_env.institution_normalizer = InstitutionNormalizer(org_manager)

    db_isis = dbm_isis.IsisDAO(dbm_isis.UCISIS(dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660)))
    converter_env.db_manager = xc_models.DBManager(db_isis, [config.title_db, config.title_db_copy, CURRENT_PATH + '/title.fst'], [config.issue_db, config.issue_db_copy, CURRENT_PATH + '/issue.fst'], config.serial_path, config.local_web_app_path)

    converter_env.local_web_app_path = config.local_web_app_path
    converter_env.version = '1.0'
    converter_env.is_windows = config.is_windows
    converter_env.web_app_site = config.web_app_site
    converter_env.skip_identical_xml = config.skip_identical_xml
    converter_env.max_fatal_error = config.max_fatal_error
    converter_env.max_error = config.max_error
    converter_env.max_warning = config.max_warning
