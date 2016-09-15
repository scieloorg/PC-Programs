# code = utf-8

import os
import webbrowser
import shutil

from __init__ import _
from . import attributes
from . import article
from . import article_reports
from . import article_validations
from . import article_utils
from . import fs_utils
from . import html_reports
from . import validation_status
from . import xpchecker
from . import xc_models
from . import utils


class PackageValidationsResult(dict):

    def __init__(self):
        dict.__init__(self)
        self.title = ''

    @property
    def total(self):
        return sum([item.total() for item in self.values()])

    @property
    def blocking_errors(self):
        return sum([item.blocking_errors for item in self.values()])

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in self.values()])

    @property
    def errors(self):
        return sum([item.errors for item in self.values()])

    @property
    def warnings(self):
        return sum([item.warnings for item in self.values()])

    def report(self, errors_only=False):
        _reports = ''
        for xml_name in sorted(self.keys()):
            results = self[xml_name]
            if results.total() > 0 or errors_only is False:
                _reports += html_reports.tag('h4', xml_name)
                _reports += results.message
        if len(_reports) > 0:
            _reports = self.title + _reports
        return _reports


class ValidationsResult(object):

    def __init__(self):
        self._message = ''
        self.numbers = {}

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self.calculate_numbers()

    def calculate_numbers(self):
        for status, style_checker_error_type in zip(validation_status.STATUS_LEVEL_ORDER, validation_status.STYLE_CHECKER_ERROR_TYPES):
            self.numbers[status] = word_counter(self.message, status)
            if style_checker_error_type != '':
                self.numbers[status] += number_after_words(self.message, style_checker_error_type)

    def total(self):
        return sum([item for item in self.numbers.values()])

    @property
    def statistics_label_and_number(self):
        items = []
        for status in validation_status.STATUS_LEVEL_ORDER:
            items.append((validation_status.STATUS_LABELS.get(status), str(self.numbers.get(status, 0))))
        return items

    @property
    def fatal_errors(self):
        return self.numbers.get(validation_status.STATUS_FATAL_ERROR, 0)

    @property
    def errors(self):
        return self.numbers.get(validation_status.STATUS_ERROR, 0)

    @property
    def blocking_errors(self):
        return self.numbers.get(validation_status.STATUS_BLOCKING_ERROR, 0)

    @property
    def warnings(self):
        return self.numbers.get(validation_status.STATUS_WARNING, 0)

    def statistics_display(self, inline=True):
        tag_name = 'span'
        text = ' | '.join([k + ': ' + v for k, v in self.statistics_label_and_number if v != '0'])
        if not inline:
            tag_name = 'div'
            text = ''.join([html_reports.tag('p', html_reports.display_label_value(_('Total of ') + k, v)) for k, v in self.statistics_label_and_number])
        style = validation_status.message_style(self.statistics_label_and_number)
        r = html_reports.tag(tag_name, text, style)
        return r


class ValidationsFile(ValidationsResult):

    def __init__(self, filename):
        ValidationsResult.__init__(self)
        self.filename = filename
        self._read()

    @ValidationsResult.message.setter
    def message(self, _message):
        self._message = _message
        self.calculate_numbers()
        self._write()

    def _write(self):
        m = self.message if self.message is not None else ''
        fs_utils.write_file(self.filename, m)

    def _read(self):
        if os.path.isfile(self.filename):
            self._message = fs_utils.read_file(self.filename)
        else:
            self._message = ''


class XMLJournalDataValidator(object):

    def __init__(self, journal_data):
        self.journal_data = journal_data

    def validate(self, article):
        if self.journal_data is None:
            r = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to identify {unidentified}. ').format(unidentified=_('journal'))
        else:
            items = []
            license_url = None
            if len(article.article_licenses) > 0:
                license_url = article.article_licenses.values()[0].get('href')
            print([article.journal_id_nlm_ta, self.journal_data.nlm_title])
            items.append([_('NLM title'), article.journal_id_nlm_ta, self.journal_data.nlm_title, validation_status.STATUS_FATAL_ERROR])
            items.append([_('journal-id (publisher-id)'), article.journal_id_publisher_id, self.journal_data.acron, validation_status.STATUS_FATAL_ERROR])
            items.append([_('e-ISSN'), article.e_issn, self.journal_data.e_issn, validation_status.STATUS_FATAL_ERROR])
            items.append([_('print ISSN'), article.print_issn, self.journal_data.p_issn, validation_status.STATUS_FATAL_ERROR])
            items.append([_('publisher name'), article.publisher_name, self.journal_data.publisher_name, validation_status.STATUS_ERROR])
            items.append([_('license'), license_url, self.journal_data.license, validation_status.STATUS_ERROR])
            r = evaluate_journal_data(items)
        return r


class XMLIssueDataValidator(object):

    def __init__(self, is_db_generation, issue_error_msg, issue_models):
        self.issue_error_msg = issue_error_msg
        self.issue_models = issue_models
        self.is_db_generation = is_db_generation

    def validate(self, article):
        r = ''
        if self.is_db_generation:
            r = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to identify {unidentified}. ').format(unidentified=_('issue'))
            if self.issue_error_msg is not None:
                r += self.issue_error_msg
            if self.issue_models:
                r = self.issue_models.validate_article_issue_data(article)
        return r


class XMLStructureValidator(object):

    def __init__(self, dtd_files):
        self.xml_validator = xpchecker.XMLValidator(dtd_files)
        self.logger = None

    def validate(self, work_area):

        self.xml_validator.logger = self.logger
        self.logger.register('XMLStructureValidator.validate() - inicio')
        separator = '\n\n\n' + '.........\n\n\n'

        name_error = ''
        if '_' in work_area.xml_name or '.' in work_area.xml_name:
            name_error = rst_title(_('Name errors')) + _('{value} has forbidden characters, which are {forbidden_characters}').format(value=work_area.xml_name, forbidden_characters='_.') + separator

        self.logger.register('XMLStructureValidator.validate() - err_filename')
        files_errors = ''
        if os.path.isfile(work_area.err_filename):
            files_errors = fs_utils.read_file(work_area.err_filename)

        self.logger.register('XMLStructureValidator.validate() - delete old version of reports')
        for f in [work_area.dtd_report_filename, work_area.style_report_filename, work_area.data_report_filename, work_area.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)
        #xml_filename = work_area.new_xml_filename
        self.logger.register('XMLStructureValidator.validate() - self.xml_validator.validate')
        xml, valid_dtd, valid_style = self.xml_validator.validate(work_area.new_xml_filename, work_area.dtd_report_filename, work_area.style_report_filename)
        xml_f, xml_e, xml_w = valid_style

        self.logger.register('XMLStructureValidator.validate() - xml_structure_report_content')
        xml_structure_report_content = ''
        if os.path.isfile(work_area.dtd_report_filename):
            xml_structure_report_content = rst_title(_('DTD errors')) + fs_utils.read_file(work_area.dtd_report_filename)
            #os.unlink(work_area.dtd_report_filename)

        self.logger.register('XMLStructureValidator.validate() - report_content')
        report_content = ''
        if xml is None:
            xml_f += 1
            report_content += validation_status.STATUS_FATAL_ERROR + ' ' + _('XML file is invalid') + '\n'
        if not valid_dtd:
            xml_f += 1
            report_content += validation_status.STATUS_FATAL_ERROR + ' ' + _('XML file has DTD errors') + '\n'
        if len(name_error) > 0:
            xml_f += 1
            report_content += validation_status.STATUS_FATAL_ERROR + ' ' + _('XML file has name errors') + '\n'

        if len(report_content) > 0:
            report_content = rst_title(_('Summary')) + report_content + separator
            report_content = report_content.replace('\n', '<br/>')

        self.logger.register('XMLStructureValidator.validate() - err_filename')
        if xml_f > 0:
            fs_utils.append_file(work_area.err_filename, name_error + xml_structure_report_content)

        self.logger.register('XMLStructureValidator.validate() - apaga ou escreve files')
        if work_area.ctrl_filename is None:
            if xml_f + xml_e + xml_w == 0:
                os.unlink(work_area.style_report_filename)
        else:
            fs_utils.write_file(work_area.ctrl_filename, 'Finished')

        self.logger.register('XMLStructureValidator.validate() - report_content')
        for rep_file in [work_area.err_filename, work_area.style_report_filename]:
            if os.path.isfile(rep_file):
                report_content += extract_report_core(fs_utils.read_file(rep_file))
        self.logger.register('XMLStructureValidator.validate() - fim')
        return report_content


class XMLContentValidator(object):

    def __init__(self, doi_services, articles_data):
        self.articles_data = articles_data
        self.doi_services = doi_services

    def validate(self, article, pkg_path, work_area, is_xml_generation):
        article_display_report = None
        article_validation_report = None
        article_validation = None

        if article.tree is None:
            content = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to get data from {item}.').format(item=work_area.new_name)
        else:
            article_validation = article_validations.ArticleContentValidation(self.doi_services, self.articles_data.journal, article, (self.articles_data.articles_db_manager is not None), False)
            article_display_report = article_reports.ArticleDisplayReport(article_validation, pkg_path, work_area.new_name)
            article_validation_report = article_reports.ArticleValidationReport(article_validation)

            content = []

            if is_xml_generation:
                content.append(article_display_report.issue_header)
                content.append(article_display_report.article_front)

                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.table_tables)

                content.append(article_display_report.article_body)
                content.append(article_display_report.article_back)

            else:
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.table_tables)
                content.append(article_display_report.files_and_href())

            content = html_reports.join_texts(content)
        return content, article_display_report


class ArticleValidations(object):

    def __init__(self, work_area, is_xml_generation, is_db_generation):
        self.work_area = work_area
        self.is_xml_generation = is_xml_generation
        self.is_db_generation = is_db_generation
        self.validations_file = {}
        self.validations_file['journal'] = ValidationsFile(self.work_area.journal_validations_filename)
        self.validations_file['issue'] = ValidationsFile(self.work_area.issue_validations_filename)
        self.validations_file['xmlstructure'] = ValidationsFile(self.work_area.err_filename_html)
        self.validations_file['xmlcontent'] = ValidationsFile(self.work_area.data_report_filename)

    @property
    def journal_validation(self):
        return self.validations_file['journal'].message

    @property
    def issue_validation(self):
        return self.validations_file['issue'].message

    @property
    def xmlcontent_validation(self):
        return self.validations_file['xmlcontent'].message

    @property
    def xmlstructure_validation(self):
        return self.validations_file['xmlstructure'].message

    @journal_validation.setter
    def journal_validation(self, validation_result):
        self.validations_file['journal'].message = validation_result

    @issue_validation.setter
    def issue_validation(self, validation_result):
        self.validations_file['issue'].message = validation_result

    @xmlstructure_validation.setter
    def xmlstructure_validation(self, validation_result):
        self.validations_file['xmlstructure'].message = validation_result

    @xmlcontent_validation.setter
    def xmlcontent_validation(self, validation_result):
        self.validations_file['xmlcontent'].message = validation_result
        if self.is_xml_generation:
            stats = self.validations_file['xmlcontent'].statistics_display(False)
            title = [_('Data Quality Control'), self.work_area.new_name]
            self.validations_file['xmlcontent'].message = html_reports.report_title(title) + stats + self.validations_file['xmlcontent'].message

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in self.validations_file.values()])

    def hide_and_show_block(self, report_id):
        blocks = []
        block_parent_id = report_id + self.work_area.new_name
        blocks.append((_('Structure Validations'), 'xmlrep', self.validations_file['xmlstructure']))
        blocks.append((_('Contents Validations'),  'datarep', self.validations_file['xmlcontent']))
        if self.is_db_generation:
            blocks.append((_('Converter Validations'), 'xcrep', self.validations_file['issue']))
        _blocks = []
        for label, style, validations_file in blocks:
            if validations_file.total() > 0:
                status = validations_file.statistics_display()
                _blocks.append(html_reports.HideAndShowBlockItem(block_parent_id, label, style + self.work_area.new_name, style, validations_file.message, status))
        return html_reports.HideAndShowBlock(block_parent_id, _blocks)


class ArticlesPackage(object):

    def __init__(self, pkg_path, pkg_articles, is_xml_generation):
        self.pkg_path = pkg_path
        self.pkg_articles = pkg_articles
        self.is_xml_generation = is_xml_generation
        self.xml_names = [name for name in os.listdir(self.pkg_path) if name.endswith('.xml')]

    @property
    def xml_list(self):
        r = ''
        r += '<p>' + _('XML path') + ': ' + self.pkg_path + '</p>'
        r += '<p>' + _('Total of XML files') + ': ' + str(len(self.xml_names)) + '</p>'
        r += html_reports.format_list('', 'ol', self.xml_names)
        r = '<div class="xmllist">' + r + '</div>'
        return r


class ArticlesData(object):

    def __init__(self):
        self.articles_db_manager = None
        self.journal = None
        self.journal_data = None
        self.acron_issue_label = None
        self.issue_models = None
        self.issue_error_msg = None
        self.issue_files = None

    def setup(self, pkg, journals_manager, db_manager):
        self._identify_journal_data(pkg.pkg_articles, journals_manager)
        if db_manager is not None:
            self._identify_issue_data(db_manager)
            self._identify_articles_data(pkg.pkg_path, db_manager)

    def _identify_journal_data(self, pkg_articles, journals_manager):
        #journals_manager = xc_models.JournalsManager()
        journals = [(a.journal_title, a.print_issn, a.e_issn, a.issue_label) for a in pkg_articles.values() if a.journal_title is not None and a.issue_label is not None and (a.print_issn is not None or a.e_issn is not None)]
        journals = list(set(journals))
        if len(journals) > 0:
            journal = article.Journal()
            if len(journals[0]) == 4:
                journal.journal_title, journal.p_issn, journal.e_issn, self.issue_label = journals[0]
                self.journal, self.journal_data = journals_manager.journal(journal.p_issn, journal.e_issn, journal.journal_title)

    def _identify_issue_data(self, db_manager):
        if db_manager is not None and self.journal is not None:
            self.acron_issue_label, self.issue_models, self.issue_error_msg = db_manager.get_issue_models(self.journal.journal_title, self.issue_label, self.journal.p_issn, self.journal.e_issn)

    def _identify_articles_data(self, pkg_path, db_manager):
        if self.issue_error_msg is None:
            self.issue_files = db_manager.get_issue_files(self.issue_models, pkg_path)
            self.articles_db_manager = xc_models.ArticlesDBManager(db_manager.db_isis, self.issue_files)


class PreConversionValidator(object):

    def __init__(self, registered_articles, pkg_articles):
        self.registered_articles = registered_articles
        self.pkg_articles = pkg_articles
        self.conflicting_items = {}
        self.names_changed = []
        self.orders_changed = {}
        self.rejected_names_change = []
        self.rejected_orders_change = {}
        self.actions = {}
        for action in ['add', 'update', 'conditional update', 'reject', 'exclude', 'replace']:
            self.actions[action] = []

    @property
    def total_to_convert(self):
        return len(self.pkg_articles)

    @property
    def excluded_orders(self):
        return dict(self.actions['exclude'])

    @property
    def xc_articles(self):
        return self.pkg_articles

    @property
    def articles_actions(self):
        self.actions = {}
        for action in ['add', 'update', 'conditional update', 'reject', 'exclude', 'replace']:
            self.actions[action] = []
        _articles_actions = {}
        self.conflicting_items = {}
        self.exclude_items = []
        for name, article in self.pkg_articles.items():
            actions, exclude_name, conflicts = self._identify_actions(name, article)
            _articles_actions[name] = actions, exclude_name, conflicts
            for action in actions:
                self.actions[action].append(name)
                if action == 'update':
                    self.actions['exclude'].append((name, article.order))
            if exclude_name is not None:
                self.actions['replace'].append([(name, exclude_name), (article.order, self.registered_articles[exclude_name].order)])
            if conflicts is not None:
                self.conflicting_items[name].append(conflicts)
        return _articles_actions

    def _simulate_orders_updating(self):
        orders = {name: article.order for name, article in self.registered_articles.items()}
        for name, article in self.pkg_articles.items():
            actions, exclude_name, conflicts = self.articles_actions[name]
            self._apply_actions(name, article.order, article.marked_to_delete, actions, orders, exclude_name)
        return orders

    def _apply_actions(self, name, new_value, marked_to_delete, actions, result, exclude_name):
        done = []
        for action in actions:
            if action == 'update':
                if marked_to_delete:
                    if name in result.keys():
                        del result[name]
                        done.append('excluded')
                else:
                    result[name] = new_value
                    done.append('updated')
            elif action == 'add':

                result[name] = new_value
                done.append('added')
            elif action == 'conditional update':
                result[name] = new_value
                done.append('updated')
            if exclude_name is not None:
                if exclude_name in result.keys():
                    del result[name]
        return done

    def sort_articles_orders(self, updated_orders):
        orders = {}
        for name, order in updated_orders.items():
            if not order in orders.keys():
                orders[order] = []
            orders[order].append(name)
        return orders

    @property
    def rejected_because_order_duplication(self):
        _rejected_updating = []
        check_names = self.actions.get('conditional update') + self.actions.get('add')
        if len(check_names) > 0:
            updated_orders = self._simulate_orders_updating()
            sorted_orders = self.sort_articles_orders(updated_orders)
            self.duplicated_orders = {order: items for order, items in updated_orders.items() if len(items) > 1}
            if len(self.duplicated_orders) > 0:
                for name in check_names:
                    article = self.pkg_articles.get(name)
                    if article.order in self.duplicated_orders.keys():
                        _rejected_updating.append(name)
        _rejected_updating.sort()
        return _rejected_updating

    def has_order_conflict(self, name):
        return name in self.rejected_because_order_duplication

    @property
    def updated_articles(self):
        articles = self.registered_articles.copy()
        self.names_changed = []
        self.orders_changed = {}
        self.rejected_names_change = []
        self.rejected_orders_change = {}

        self.history = {name: [_('registered'), '/'.join([article.creation_date_display, article.last_update_display]), 'order={order}'.format(order=article.order)] for name, article in self.registered_articles.items()}

        for name, article in self.pkg_articles.items():
            if not name in self.history.keys():
                self.history[name] = [_('new article'), 'order={order}'.format(order=article.order)]
            actions, exclude_name, conflict_msg = self.articles_actions[name]

            self.history[name].append(_('package'))
            self.history[name].append('order={order}'.format(order=article.order))
            if conflict_msg is not None:
                self.history[name].append(conflict_msg)
            elif self.has_order_conflict(name):
                self.history[name].append(validation_status.STATUS_BLOCKING_ERROR + ' ' + _('There is order={order} in other files: {files}. ').format(order=article.order, files=', '.join(self.duplicated_orders[article.order])))
                if exclude_name is not None:
                    self.rejected_names_change.append((exclude_name, name))
                    self.history[name].append(validation_status.STATUS_BLOCKING_ERROR + ' ' + _('Unable to rename: {old} => {new}. ').format(old=exclude_name, new=name))
                if article.order != articles[name].order:
                    self.rejected_orders_change[name].append((articles[name].order, article.order))
                    self.history[name].append(validation_status.STATUS_BLOCKING_ERROR + ' ' + _('Unable to change order: {old} => {new}. ').format(old=articles[name].order, new=article.order))
            else:
                done = self._apply_actions(name, article, article.marked_to_delete, actions, articles, exclude_name)
                for item in done:
                    self.history[name].append(_(item))
                if exclude_name is not None:
                    self.names_changed.append((exclude_name, name))
                    self.history[name].append(validation_status.STATUS_INFO + ' ' + _('Renamed: {old} => {new}. ').format(old=exclude_name, new=name))
                if article.order != articles[name].order:
                    self.orders_changed[name].append((articles[name].order, article.order))
                    self.history[name].append(validation_status.STATUS_INFO + ' ' + _('Order changed: {old} => {new}. ').format(old=articles[name].order, new=article.order))
        self.names_changed.sort()
        #self.orders_changed.sort()
        self.rejected_names_change.sort()
        #self.rejected_orders_change.sort()

        return articles

    def _identify_actions(self, name, article):
        exclude_name = None
        registered = self.registered_item(name, article)
        conflicts = None
        if registered is None:
            matched_titaut_article_names = self.registered_titles_and_authors(article)
            matched_order_article_names = self.registered_order(article.order)
            registered_titaut = self._found_items(matched_titaut_article_names)
            registered_order = self._found_items(matched_order_article_names)
            registered_name = self.registered_articles.get(name)
            actions, exclude_name, conflicts = self._identify_actions_for_exceptions(name, registered_titaut, registered_order, registered_name)
        else:
            actions = ['update']
        return (actions, exclude_name, conflicts)

    def _found_items(self, found_names):
        if len(found_names) == 0:
            return None
        elif len(found_names) == 1:
            return self.registered_articles.get(found_names[0])
        else:
            return {name: self.registered_articles.get(name) for name in found_names}

    def _format_conflicts_message(self, conflicts):
        return '; '.join([data + ': ' + name for name, data in conflicts.items()])

    def _identify_actions_for_exceptions(self, name, registered_titaut, registered_order, registered_name):
        actions = []
        exclude_name = None
        conflicts = None
        if registered_titaut is None and registered_order is None and registered_name is None:
            actions = ['add']
        elif all([registered_titaut, registered_order, registered_name]):
            if id(registered_titaut) == id(registered_order) == id(registered_name):
                actions = ['update']
            elif id(registered_titaut) == id(registered_name):
                # titaut + name != order
                # avaliar mudanca de order | rejeitar
                actions = ['conditional update']
            elif id(registered_titaut) == id(registered_order):
                # titaut + order != name
                # rejeitar
                conflicts = {registered_titaut.xml_name: _(' and ').join([_('title/authors'), 'order'])}
            elif id(registered_name) == id(registered_order):
                # order + name != titaut
                # rejeitar
                conflicts = {name: 'order', registered_titaut.xml_name: _('title/authors')}
            else:
                # order != name != titaut
                # rejeitar
                conflicts = {registered_titaut.xml_name: _('title/authors'), registered_order.xml_name: 'order'}

        elif all([registered_titaut, registered_order]):
            if id(registered_titaut) == id(registered_order):
                actions = ['update']
                exclude_name = registered_titaut.xml_name
            else:
                conflicts = {registered_titaut.xml_name: _('title/authors'), registered_order.xml_name: 'order'}

        elif all([registered_titaut, registered_name]):
            if id(registered_titaut) == id(registered_name):
                actions = ['conditional update']
            else:
                conflicts = {registered_titaut.xml_name: _('title/authors')}
        elif all([registered_order, registered_name]):
            if id(registered_order) == id(registered_name):
                actions = ['update']
            else:
                conflicts = {registered_order.xml_name: 'order'}
        elif registered_titaut is not None:
            actions = ['conditional update']
            exclude_name = registered_titaut.xml_name
        elif registered_name is not None:
            actions = ['conditional update']
        elif registered_order is not None:
            actions = ['update']
            exclude_name = registered_titaut.xml_name

        if conflicts is not None:
            conflicts = _('Its data were found in other files: {conflicts}. ').format(item=name, conflicts=self._format_conflicts_message(conflicts))
        return (actions, exclude_name, conflicts)

    def registered_item(self, name, article):
        found = None
        registered = self.registered_articles.get(name)
        if registered is not None:
            similar, status, msg = self.compare_versions(registered, article)
            if registered.order == article.order and similar:
                found = registered
        return found

    def registered_order(self, order):
        return [reg_name for reg_name, reg in self.registered_articles.items() if reg.order == order]

    def registered_titles_and_authors(self, article):
        similar_items = []
        for name, registered in self.registered_articles.items():
            similar, status, message = self.compare_versions(registered, article)
            if similar:
                similar_items.append(name)
        return similar_items

    def compare_versions(self, registered, pkg_article):
        labels = [_('titles'), _('authors'), _('body')]
        validations = []
        validations.append((registered.textual_titles, article.textual_titles))
        validations.append((registered.textual_contrib_surnames, article.textual_contrib_surnames))
        validations.append((registered.body_words[0:200], article.body_words[0:200]))
        exact_comparison_result = [(label, items) for label, items in zip(labels, validations) if not items[0] == items[1]]
        relaxed_comparison_result = [(label, items) for label, items in zip(labels, validations) if not utils.is_similar(items[0], items[1])]

        valid_titles_and_authors = False
        status = validation_status.STATUS_BLOCKING_ERROR
        message = ''
        if len(exact_comparison_result) == 0:
            # no changes
            valid_titles_and_authors = True
            status = validation_status.STATUS_INFO
        elif len(relaxed_comparison_result) == 0:
            # acceptable changes
            valid_titles_and_authors = True
            status = validation_status.STATUS_WARNING
        message = self._differences_message(status, exact_comparison_result)
        return (valid_titles_and_authors, status, message)

    @property
    def _differences_message(self, status, comparison_result):
        msg = []
        if len(comparison_result) > 0:
            for label, differences in comparison_result:
                msg.append(html_reports.p_message(status))
                msg.append(html_reports.tag('h5', label))
                msg.append(html_reports.display_label_value(_('registered'), differences[0]))
                msg.append(html_reports.display_label_value(_('in the package'), differences[1]))
        return ''.join(msg)

    @property
    def names_change_report(self):
        r = ''
        if len(self.names_changed) > 0:
            r += html_reports.tag('h3', _('Names changed'))
            r += ''.join([html_reports.tag('p', '{old} => {new}'.format(old=old, new=new)) for old, new in self.names_changed])
        if len(self.rejected_names_change) > 0:
            r += html_reports.tag('h3', _('Rejected names change'))
            r += ''.join([html_reports.p_message('{status}: {old} => {new}'.format(old=old, new=new, status=validation_status.STATUS_BLOCKING_ERROR)) for old, new in self.rejected_names_change])
        return r

    @property
    def orders_change_report(self):
        r = ''
        if len(self.orders_changed) > 0:
            r += html_reports.tag('h3', _('Orders changed'))
            r += ''.join([html_reports.tag('p', '{name}: {old} => {new}'.format(name=name, old=item[0], new=item[1])) for name, item in self.orders_changed.items()])
        if len(self.rejected_orders_change) > 0:
            r += html_reports.tag('h3', _('Rejected orders change'))
            r += ''.join([html_reports.p_message('{status}: {name}: {old} => {new}'.format(name=name, old=item[0], new=item[1], status=validation_status.STATUS_BLOCKING_ERROR)) for name, item in self.rejected_orders_change.items()])
        return r

    @property
    def conflicting_report(self):
        r = ''
        if len(self.conflicting_items) > 0:
            r += html_reports.tag('h3', _('Conflicts'))
            r += html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to update some files'))
            for name, msg in self.conflicting_items.items():
                r += html_reports.tag('h4', name) + html_reports.tag('p', msg)
        return r

    @property
    def exclusions_report(self):
        deleted = []
        not_deleted = []
        for name, order in self.actions['exclude']:
            if article.marked_to_delete:
                if name in self.registered_articles.keys():
                    if name in self.updated_articles.keys():
                        not_deleted.append((name, order))
                    else:
                        deleted.append((name, order))
        r = ''
        if len(deleted) > 0:
            r += html_reports.tag('h3', _('Excluded items'))
            r += ''.join([html_reports.tag('p', '{name} / {order}'.format(name=name, order=order)) for name, order in deleted])
        if len(not_deleted) > 0:
            r += html_reports.tag('h3', _('Items not excluded'))
            r += ''.join([html_reports.p_message('{status}: {name} / {order}'.format(name=name, order=order, status=validation_status.STATUS_BLOCKING_ERROR)) for name, order in not_deleted])
        return r

    @property
    def replacements_report(self):
        r = ''
        if len(self.actions['replace']) > 0:
            r += html_reports.tag('h2', _('Replaced items'))
            i = 0
            for replacements in self.actions['replace']:
                i += 1
                r += html_reports.tag('h3', '{i}'.format(i=i))
                for replacement in replacements:
                    old, new = replacement
                    r += html_reports.tag('p', '{old} => {new}'.format(old=old, new=new))
        return r

    @property
    def errors_report(self):
        r = ''
        r += self.conflicting_report
        r += self.orders_change_report
        r += self.names_change_report
        r += self.replacements_report
        r += self.exclusions_report
        #r += self.history_report
        return r

    def article_report(self, _article):
        r = ''
        r += html_reports.tag('p', _article.toc_section, 'toc-section')
        r += html_reports.tag('p', _article.article_type, 'article-type')
        r += html_reports.tag('p', html_reports.tag('strong', _article.pages), 'fpage')
        r += html_reports.tag('p', _article.doi, 'doi')
        r += html_reports.tag('p', html_reports.tag('strong', _article.title), 'article-title')
        a = []
        for item in article.authors_list(_article.article_contrib_items):
            a.append(html_reports.tag('span', item))
        r += html_reports.tag('p', '; '.join(a))
        return r

    @property
    def history_report(self):
        #resulting_orders
        labels = [_('filename'), _('article'), _('history')]
        items = []
        for name in sorted(self.history.keys()):
            values = []
            values.append(name)
            values.append(self.article_report(self.pkg_articles.get(name, self.registered_articles.get(name))))
            values.append(''.join([html_reports.p_message(msg) for msg in self.history[name]]))
            items.append(label_values(labels, values))
        return html_reports.tag('h2', _('Registered and Package Articles')) + html_reports.sheet(labels, items, html_cell_content=[_('article'), _('history')])


class ArticlesSetValidations(object):

    def __init__(self, pkg, articles_data, logger):
        self.logger = logger
        self.pkg = pkg
        self.articles_data = articles_data
        self.registered_articles = {}
        self.is_db_generation = articles_data.articles_db_manager is not None
        if articles_data.articles_db_manager is not None:
            self.registered_articles = articles_data.articles_db_manager.registered_articles
        self.merged_articles = self.registered_articles.copy()
        self.merged_articles.update(pkg.pkg_articles)
        self.articles_validations = {}
        self.updated_articles = {}

        self.ERROR_LEVEL_FOR_UNIQUE_VALUES = {'order': validation_status.STATUS_BLOCKING_ERROR, 'doi': validation_status.STATUS_BLOCKING_ERROR, 'elocation id': validation_status.STATUS_BLOCKING_ERROR, 'fpage-lpage-seq-elocation-id': validation_status.STATUS_ERROR}
        if not self.is_db_generation:
            self.ERROR_LEVEL_FOR_UNIQUE_VALUES['order'] = validation_status.STATUS_WARNING

        self.EXPECTED_COMMON_VALUES_LABELS = ['journal-title', 'journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'issue label', 'issue pub date', 'license']
        self.REQUIRED_DATA = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        self.EXPECTED_UNIQUE_VALUE_LABELS = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']

    @property
    def articles_common_data(self):
        data = {}
        for label in self.EXPECTED_COMMON_VALUES_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]

                if not value in values:
                    values[value] = []
                values[value].append(xml_name)

            data[label] = values
        return data

    @property
    def articles_unique_data(self):
        data = {}
        for label in self.EXPECTED_UNIQUE_VALUE_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]

                if not value in values:
                    values[value] = []
                values[value].append(xml_name)

            data[label] = values
        return data

    @property
    def invalid_xml_name_items(self):
        return sorted([xml_name for xml_name, doc in self.merged_articles.items() if doc.tree is None])

    @property
    def missing_required_values(self):
        required_items = {}
        for label, values in self.articles_common_data.items():
            if None in values.keys():
                required_items[label] = values[None]
        return required_items

    @property
    def conflicting_values(self):
        data = {}
        for label, values in self.articles_common_data.items():
            if len(values) > 1:
                data[label] = values
        return data

    @property
    def duplicated_values(self):
        duplicated_labels = {}
        for label, values in self.articles_unique_data.items():
            if len(values) > 0 and len(values) != len(self.articles):

                duplicated = {value: xml_files for value, xml_files in values.items() if len(xml_files) > 1}

                if len(duplicated) > 0:
                    duplicated_labels[label] = duplicated
        return duplicated_labels

    @property
    def compiled_affiliations(self):
        evaluation = {}
        keys = [_('authors without aff'), 
                _('authors with more than 1 affs'), 
                _('authors with invalid xref[@ref-type=aff]'), 
                _('incomplete affiliations')]
        for k in keys:
            evaluation[k] = []

        for xml_name, doc in self.merged_articles.items():
            aff_ids = [aff.id for aff in doc.affiliations]
            for contrib in doc.contrib_names:
                if len(contrib.xref) == 0:
                    evaluation[_('authors without aff')].append(xml_name)
                elif len(contrib.xref) > 1:
                    valid_xref = [xref for xref in contrib.xref if xref in aff_ids]
                    if len(valid_xref) != len(contrib.xref):
                        evaluation[_('authors with invalid xref[@ref-type=aff]')].append(xml_name)
                    elif len(valid_xref) > 1:
                        evaluation[_('authors with more than 1 affs')].append(xml_name)
                    elif len(valid_xref) == 0:
                        evaluation[_('authors without aff')].append(xml_name)
            for aff in doc.affiliations:
                if None in [aff.id, aff.i_country, aff.norgname, aff.orgname, aff.city, aff.state, aff.country]:
                    evaluation[_('incomplete affiliations')].append(xml_name)
        return evaluation

    def compile_references(self):
        self.sources_and_reftypes = {}
        self.reftype_and_sources = {}
        self.missing_source = []
        self.missing_year = []
        self.unusual_sources = []
        self.unusual_years = []
        self.years = {}
        for xml_name, doc in self.merged_articles.items():
            for ref in doc.references:
                if ref.source is not None:
                    if not ref.source in self.sources_and_reftypes.keys():
                        self.sources_and_reftypes[ref.source] = {}
                    if not ref.publication_type in self.sources_and_reftypes[ref.source].keys():
                        self.sources_and_reftypes[ref.source][ref.publication_type] = []
                    self.sources_and_reftypes[ref.source][ref.publication_type].append(xml_name + ': ' + str(ref.id))

                if not ref.publication_type in self.reftype_and_sources.keys():
                    self.reftype_and_sources[ref.publication_type] = {}
                if not ref.source in self.reftype_and_sources[ref.publication_type].keys():
                    self.reftype_and_sources[ref.publication_type][ref.source] = []
                self.reftype_and_sources[ref.publication_type][ref.source].append(xml_name + ': ' + str(ref.id))

                # year
                if ref.publication_type in attributes.BIBLIOMETRICS_USE:
                    if not ref.year in self.years.keys():
                        self.years[ref.year] = []
                    self.years[ref.year].append(xml_name + ': ' + str(ref.id))
                    if ref.year is None:
                        self.missing_year.append([xml_name, ref.id])
                    else:
                        if not ref.year.isdigit():
                            self.unusual_years.append([xml_name, ref.id, ref.year])

                    if ref.source is None:
                        self.missing_source.append([xml_name, ref.id])
                    else:
                        if ref.source.isdigit():
                            self.unusual_sources.append([xml_name, ref.id, ref.source])
        self.bad_sources_and_reftypes = {source: reftypes for source, reftypes in self.sources_and_reftypes.items() if len(reftypes) > 1}

    @property
    def is_processed_in_batches(self):
        return any([self.is_aop_issue, self.is_rolling_pass])

    @property
    def is_aop_issue(self):
        return any([a.is_ahead for a in self.merged_articles.values()])

    @property
    def is_rolling_pass(self):
        _is_rolling_pass = False
        if not self.is_aop_issue:
            epub_dates = list(set([a.epub_dateiso for a in self.merged_articles.values() if a.epub_dateiso is not None]))
            epub_ppub_dates = [a.epub_ppub_dateiso for a in self.merged_articles.values() if a.epub_ppub_dateiso is not None]
            collection_dates = [a.collection_dateiso for a in self.merged_articles.values() if a.collection_dateiso is not None]
            other_dates = list(set(epub_ppub_dates + collection_dates))
            if len(epub_dates) > 0:
                if len(other_dates) == 0:
                    _is_rolling_pass = True
                elif len(other_dates) > 1:
                    _is_rolling_pass = True
                elif len([None for a in self.merged_articles.values() if a.collection_dateiso is None]) > 0:
                    _is_rolling_pass = True
        return _is_rolling_pass

    @property
    def articles(self):
        return articles_sorted_by_order(self.merged_articles)

    @property
    def pkg_journal_validations_report_title(self):
        signal = ''
        msg = ''
        if not self.is_db_generation:
            signal = '<sup>*</sup>'
            msg = html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('Journal data in the XML files must be consistent with {link}').format(link=html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv')), 'note')
        return html_reports.tag('h2', _('Journal data: XML files and registered data') + signal) + msg

    def validate(self, doi_services, dtd_files, articles_work_area):
        utils.display_message(_('Validate package ({n} files)').format(n=len(self.merged_articles)))
        if len(self.registered_articles) > 0:
            utils.display_message(_('Previously registered: ({n} files)').format(n=len(self.registered_articles)))

        self.logger.register('compile_references')
        self.compile_references()

        self.logger.register('pkg_journal_validations')
        self.pkg_journal_validations = PackageValidationsResult()
        self.pkg_journal_validations.title = self.pkg_journal_validations_report_title

        self.logger.register('pkg_reg_issue_validations')
        self.pkg_reg_issue_validations = PackageValidationsResult()
        self.pkg_reg_issue_validations.title = html_reports.tag('h2', _('Checking issue data: XML files and registered data'))

        self.logger.register('articles validations - prep')
        self.articles_validations = {}
        xml_journal_data_validator = XMLJournalDataValidator(self.articles_data.journal_data)
        xml_issue_data_validator = XMLIssueDataValidator(self.is_db_generation, self.articles_data.issue_error_msg, self.articles_data.issue_models)
        xml_structure_validator = XMLStructureValidator(dtd_files)
        xml_structure_validator.logger = self.logger
        xml_content_validator = XMLContentValidator(doi_services, self.articles_data)

        self.logger.register('articles validations')
        self.articles_validations = {}
        for name, article in self.merged_articles.items():
            utils.display_message(_('Validate {name}').format(name=name))
            self.logger.register(' '.join(['validate', name]))
            self.articles_validations[name] = ArticleValidations(articles_work_area[name], self.pkg.is_xml_generation, self.is_db_generation)

            utils.display_message(_(' - validate journal data'))
            self.logger.register(' '.join([name, 'journal']))
            self.articles_validations[name].validations_file['journal'].message = xml_journal_data_validator.validate(article)

            utils.display_message(_(' - validate issue data'))
            self.logger.register(' '.join([name, 'issue']))
            self.articles_validations[name].validations_file['issue'].message = xml_issue_data_validator.validate(article)

            utils.display_message(_(' - validate XML structure'))
            self.logger.register(' '.join([name, 'xmlstructure']))
            self.articles_validations[name].validations_file['xmlstructure'].message = xml_structure_validator.validate(articles_work_area[name])

            utils.display_message(_(' - validate XML contents'))
            self.logger.register(' '.join([name, 'xmlcontent']))
            self.articles_validations[name].validations_file['xmlcontent'].message, self.articles_validations[name].article_display_report = xml_content_validator.validate(article, self.pkg.pkg_path, articles_work_area[name], self.pkg.is_xml_generation)
            self.logger.register(' '.join([name, 'fim']))

            self.pkg_journal_validations[name] = self.articles_validations[name].validations_file['journal']
            self.pkg_reg_issue_validations[name] = self.articles_validations[name].validations_file['issue']

        self.logger.register('consistency validations')
        self.consistency_validations = ValidationsResult()
        self.consistency_validations.message = self.consistency_validations_report

        self.logger.register('xc pre validations')
        self.xc_pre_validator = PreConversionValidator(self.registered_articles, self.pkg.pkg_articles)
        self.xc_pre_validator.updated_articles

        self.xc_pre_validations = ValidationsResult()
        self.xc_pre_validations.message = self.xc_pre_validator.errors_report
        self.logger.register('xc pre validations - fim')

    @property
    def detailed_report(self):
        labels = ['file', 'order', _('pages'), _('article'), 'aop pid/related', _('reports')]
        widths = {}
        widths['file'] = '10'
        widths['order'] = '5'
        widths[_('pages')] = '5'
        widths[_('article')] = '60'
        widths['aop pid/related'] = '10'
        widths[_('reports')] = '10'
        pdf_items = []
        items = []
        for new_name, article in self.articles:
            hide_and_show_block_items = self.articles_validations[new_name].hide_and_show_block('view-reports-')
            values = []
            values.append(new_name)
            values.append(article.order)
            values.append(article.pages)
            if self.articles_validations[new_name].article_display_report is None:
                values.append('')
            else:
                values.append(self.articles_validations[new_name].article_display_report.table_of_contents)
            related = {}
            for k, v in {'aop doi': article.previous_pid, 'related': [item.get('xml', '') for item in article.related_articles]}.items():
                if v is not None:
                    if len(v) > 0:
                        related[k] = v
            values.append(related)
            items.append((values, hide_and_show_block_items))
        report = html_reports.HideAndShowBlocksReport(labels, items, html_cell_content=[_('article')], widths=widths)
        return report.content

    @property
    def toc_extended_report(self):
        labels = ['file', _('article'), 'pdf']
        widths = {'file': '10', _('article'): '40', 'pdf': '50'}
        items = []
        for new_name, article in self.articles:
            values = []
            values.append(new_name)
            if self.articles_validations[new_name].article_display_report is None:
                values.append('')
                values.append('')
            else:
                values.append(self.articles_validations[new_name].article_display_report.table_of_contents_detailed)
                values.append(self.articles_validations[new_name].article_display_report.embedded_pdf_items())
            items.append(label_values(labels, values))
        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=[_('article'), 'pdf'], widths=widths)

    # FIXME
    @property
    def article_db_status_report(self, new_name):
        labels = [
            _('type'),
            _('creation date'),
            _('last update'),
            _('order'),
            _('pages'),
            _('aop PID'),
            _('doi'),
            _('authors'),
            _('title'),
        ]
        rows = []
        articles = [self.registered_articles.get('new_name'), self.pkg.pkg_articles.get('new_name'), self.updated_articles.get('new_name')]
        types = [_('registered, before converting'), _('package'), _('registered, after converting')]
        for tp, a in zip(types, articles):
            if a is not None:
                values = []
                values.append(tp)
                values.append(a.creation_date_display)
                values.append(a.last_update_display)
                values.append(a.order)
                values.append(a.pages)
                values.append(a.previous_article_pid)
                values.append(a.doi)
                values.append('; '.join(article.authors_list(a.article_contrib_items)))
                values.append(article.title)
                rows.append(label_values(labels, values))
        return html_reports.sheet(labels, rows, table_style='reports-sheet', html_cell_content=['title'])

    @property
    def db_status_report(self):
        # FIXME
        labels = ['file', _('article'), _('processing history')]
        items = []
        for new_name, article in self.articles:
            report_id = 'dbstatus-'
            block_parent_id = report_id + new_name
            block_items = [html_reports.HideAndShowBlockItem(block_parent_id, _('processing history'), 'db-hist-' + new_name, 'datarep', self.article_db_status_report(new_name), '')]
            hide_and_show_block_items = html_reports.HideAndShowBlock(block_parent_id, block_items)
            values = []
            values.append(new_name)
            values.append(self.articles_validations[new_name].article_display_report.table_of_contents)
            items.append((values, hide_and_show_block_items))
        report = html_reports.HideAndShowBlocksReport(labels, items, html_cell_content=[_('article')])
        return report.content

    @property
    def articles_dates_report(self):
        labels = ['name', '@article-type',
        'received', 'accepted', 'receive to accepted (days)', 'article date', 'issue date', 'accepted to publication (days)', 'accepted to today (days)']
        items = []
        for xml_name, doc in self.articles:
            values = []
            values.append(xml_name)
            values.append(doc.article_type)
            values.append(article_utils.display_date(doc.received_dateiso))
            values.append(article_utils.display_date(doc.accepted_dateiso))
            values.append(str(doc.history_days))
            values.append(article_utils.display_date(doc.article_pub_dateiso))
            values.append(article_utils.display_date(doc.issue_pub_dateiso))
            values.append(str(doc.publication_days))
            values.append(str(doc.registration_days))
            items.append(label_values(labels, values))
        article_dates = html_reports.sheet(labels, items, 'dbstatus')

        labels = [_('year'), _('location')]
        items = []
        for year in sorted(self.years.keys()):
            values = []
            values.append(year)
            values.append(self.years[year])
            items.append(label_values(labels, values))
        reference_dates = html_reports.sheet(labels, items, 'dbstatus')

        return html_reports.tag('h4', _('Articles Dates Report')) + article_dates + reference_dates

    @property
    def articles_affiliations_report(self):
        r = html_reports.tag('h4', _('Affiliations Report'))
        items = []
        for label, occs in self.compiled_affiliations.items():
            items.append({'label': label, 'quantity': str(len(occs)), _('files'): sorted(list(set(occs)))})
        r += html_reports.sheet(['label', 'quantity', _('files')], items, 'dbstatus')
        return r

    @property
    def references_overview_report(self):
        labels = ['label', 'status', 'message', _('why it is not a valid message?')]
        items = []
        values = []
        values.append(_('references by type'))
        values.append(validation_status.STATUS_INFO)
        values.append({reftype: str(sum([len(occ) for occ in sources.values()])) for reftype, sources in self.reftype_and_sources.items()})
        values.append('')
        items.append(label_values(labels, values))

        if len(self.bad_sources_and_reftypes) > 0:
            values = []
            values.append(_('same sources as different types references'))
            values.append(validation_status.STATUS_ERROR)
            values.append(self.bad_sources_and_reftypes)
            values.append('')
            items.append(label_values(labels, values))

        if len(self.missing_source) > 0:
            items.append({'label': _('references missing source'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.missing_source], _('why it is not a valid message?'): ''})
        if len(self.missing_year) > 0:
            items.append({'label': _('references missing year'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.missing_year], _('why it is not a valid message?'): ''})
        if len(self.unusual_sources) > 0:
            items.append({'label': _('references with unusual value for source'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.unusual_sources], _('why it is not a valid message?'): ''})
        if len(self.unusual_years) > 0:
            items.append({'label': _('references with unusual value for year'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.unusual_years], _('why it is not a valid message?'): ''})

        return html_reports.tag('h4', _('Package references overview')) + html_reports.sheet(labels, items, table_style='dbstatus')

    @property
    def sources_overview_report(self):
        labels = ['source', _('location')]
        h = ''
        if len(self.reftype_and_sources) > 0:
            for reftype, sources in self.reftype_and_sources.items():
                items = []
                h += html_reports.tag('h4', reftype)
                for source in sorted(sources.keys()):
                    items.append({'source': source, _('location'): sources[source]})
                h += html_reports.sheet(labels, items, 'dbstatus')
        return h

    @property
    def pages_report(self):
        # FIXME
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        for xml_name, article in self.articles:
            fpage = article.fpage
            lpage = article.lpage
            msg = []
            status = ''
            if article.pages == '':
                msg.append(_('no pagination was found'))
                if not article.is_ahead:
                    status = validation_status.STATUS_ERROR
            if fpage is not None and lpage is not None:
                if fpage.isdigit() and lpage.isdigit():
                    int_fpage = int(fpage)
                    int_lpage = int(lpage)

                    #if not article.is_rolling_pass and not article.is_ahead:
                    if int_previous_lpage is not None:
                        if int_previous_lpage > int_fpage:
                            status = validation_status.STATUS_BLOCKING_ERROR if not article.is_epub_only else validation_status.STATUS_WARNING
                            msg.append(_('Invalid pages') + ': ' + _('check lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name})').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage == int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}) are the same').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage + 1 < int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('there is a gap between lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name})').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                    if int_fpage > int_lpage:
                        status = validation_status.STATUS_BLOCKING_ERROR
                        msg.append(_('Invalid page range'))
                    int_previous_lpage = int_lpage
                    previous_lpage = lpage
                    previous_xmlname = xml_name
            #dates = '|'.join([item if item is not None else 'none' for item in [article.epub_ppub_dateiso, article.collection_dateiso, article.epub_dateiso]])
            msg = '; '.join(msg)
            if len(msg) > 0:
                msg = '. ' + msg
            results.append({'label': xml_name, 'status': status, 'message': article.pages + msg, _('why it is not a valid message?'): ''})
        return html_reports.tag('h2', _('Pages Report')) + html_reports.tag('div', html_reports.sheet(['label', 'status', 'message', _('why it is not a valid message?')], results, table_style='validation'))

    @property
    def journal_issue_header_report(self):
        articles_common_data = ''
        for label, values in self.articles_common_data.items():
            message = ''
            if len(values.keys()) == 1:
                articles_common_data += html_reports.tag('p', html_reports.display_label_value(label, values.keys()[0]))
            else:
                articles_common_data += html_reports.format_list(label + ':', 'ol', values.keys())
        return html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', articles_common_data, 'issue-data')

    @property
    def invalid_xml_report(self):
        r = ''
        if len(self.invalid_xml_name_items) > 0:
            r += html_reports.tag('div', html_reports.p_message(_('{status}: invalid XML files.').format(status=validation_status.STATUS_BLOCKING_ERROR)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', self.invalid_xml_name_items, 'issue-problem'))
        return r

    @property
    def missing_items_report(self):
        r = ''
        for label, items in self.missing_required_values.items():
            r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_BLOCKING_ERROR, label=label)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
        return r

    @property
    def duplicated_values_report(self):
        parts = []
        for label, values in self.duplicated_values.items():
            status = self.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
            _m = _('Unique value for {label} is required for all the documents in the package').format(label=label)
            parts.append(html_reports.p_message(status + ': ' + _m))
            for value, xml_files in values.items():
                parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def conflicting_values_report(self):
        parts = []
        for label, values in self.conflicting_values.items():
            compl = ''
            _status = validation_status.STATUS_BLOCKING_ERROR
            if label == 'issue pub date':
                if self.is_rolling_pass:
                    _status = validation_status.STATUS_WARNING
            elif label == 'license':
                _status = validation_status.STATUS_WARNING
            _m = _('{status}: same value for {label} is required for all the documents in the package.').format(status=_status, label=label)
            parts.append(html_reports.p_message(_m))
            parts.append(html_reports.tag('div', html_reports.format_html_data(values), 'issue-problem'))
        return ''.join(parts)

    @property
    def consistency_validations_report(self):
        text = []
        text += self.invalid_xml_report
        text += self.missing_items_report
        text += self.conflicting_values_report
        text += self.duplicated_values_report
        text = html_reports.tag('div', ''.join(text), 'issue-messages')
        text += self.pages_report
        return html_reports.tag('h2', _('Checking issue data consistency')) + text

    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.journal_issue_header_report)
        report.append(self.pkg_journal_validations.report(errors_only=not self.pkg.is_xml_generation))
        report.append(self.pkg_reg_issue_validations.report(errors_only=not self.pkg.is_xml_generation))
        if self.consistency_validations.total() > 0:
            report.append(self.consistency_validations.message)
        report.append(self.xc_pre_validations.message)
        return ''.join(report)

    @property
    def blocking_errors(self):
        return sum([self.consistency_validations.blocking_errors, self.pkg_reg_issue_validations.blocking_errors, self.xc_pre_validations.blocking_errors])

    @property
    def fatal_errors(self):
        return sum([article_validations.fatal_errors for article_validations in self.articles_validations.validations_file.values()])


class ReportsMaker(object):

    def __init__(self, articles_set_validations, xpm_version=None, conversion=None, display_report=False):
        self.display_report = display_report
        self.processing_result_location = None
        self.articles_set_validations = articles_set_validations
        self.conversion = conversion
        self.xpm_version = xpm_version
        self.tabs = ['pkg-files', 'summary-report', 'issue-report', 'toc-extended', 'individual-report', 'references', 'dates-report', 'aff-report', 'xc-validations', 'db-report']
        self.labels = {
            'pkg-files': _('Files/Folders'),
            'summary-report': _('Summary'),
            'issue-report': 'journal/issue',
            'individual-report': _('XML Validations'),
            'xc-validations': _('Conversion'),
            'db-report': _('Database'),
            'aff-report': _('Affiliations'),
            'dates-report': _('Dates'),
            'references': _('References'),
            'toc-extended': _('ToC'),
        }
        self.validations = ValidationsResult()

    @property
    def report_components(self):
        components = {}
        components['pkg-files'] = self.articles_set_validations.pkg.xml_list
        if self.processing_result_location is not None:
            components['pkg-files'] += processing_result_location(self.processing_result_location)

        components['summary-report'] = ''
        components['issue-report'] = ''
        components['individual-report'] = self.articles_set_validations.detailed_report
        components['aff-report'] = self.articles_set_validations.articles_affiliations_report
        components['dates-report'] = self.articles_set_validations.articles_dates_report
        components['references'] = (self.articles_set_validations.references_overview_report +
            self.articles_set_validations.sources_overview_report)

        if not self.articles_set_validations.pkg.is_xml_generation:
            components['toc-extended'] = self.articles_set_validations.toc_extended_report
            components['issue-report'] += self.articles_set_validations.journal_and_issue_report

        if self.conversion is not None:
            if self.articles_set_validations.articles_data.issue_error_msg is not None:
                components['issue-report'] += self.articles_set_validations.articles_data.issue_error_msg
            components['xc-validations'] = self.conversion.xc_pre_validator.errors_report + self.conversion.articles_conversion_validations.report(True)
            components['db-report'] = self.articles_set_validations.xc_pre_validator.history_report
            components['summary-report'] = self.conversion.conclusion_message + self.conversion.conversion_status_report + self.conversion.aop_status_report

        self.validations.message = html_reports.join_texts(components.values())
        components['summary-report'] = error_msg_subtitle() + self.validations.statistics_display(False) + components['summary-report']
        components = {k: label_errors(v) for k, v in components.items() if v is not None}
        return components

    @property
    def footnote(self):
        content = html_reports.tag('p', _('finished'))
        if self.xpm_version is not None:
            content += html_reports.tag('p', _('report generated by XPM ') + self.xpm_version)
        return content

    def save_report(self, report_path, report_filename, report_title):
        self.tabbed_report = html_reports.TabbedReport(self.labels, self.tabs, self.report_components, 'summary-report', self.footnote)
        self.tabbed_report.save_report(report_path, report_filename, report_title, self.display_report)


def extract_report_core(content):
    report = ''
    if 'Parse/validation finished' in content and '<!DOCTYPE' in content:
        part1 = content[0:content.find('<!DOCTYPE')]
        part2 = content[content.find('<!DOCTYPE'):]

        l = part1[part1.rfind('Line number:')+len('Line number:'):]
        l = l[0:l.find('Column')]
        l = ''.join([item.strip() for item in l.split()])
        if l.isdigit():
            l = str(int(l) + 1) + ':'
            if l in part2:
                part2 = part2[0:part2.find(l)] + '\n...'

        part1 = part1.replace('\n', '<br/>')
        part2 = part2.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>').replace('\t', '&nbsp;'*4)
        report = '<p>' + part1 + part2 + '</p>'
    elif '</body>' in content:
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
        content = content[content.find('<body'):]
        content = content[0:content.rfind('</body>')]
        report = content[content.find('>')+1:]
    elif '<body' in content:
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
        content = content[content.find('<body'):]
        report = content[content.find('>')+1:]
    elif not '<' in content:
        report = content.replace('\n', '<br/>')
    return report


def label_values(labels, values):
    r = {}
    for i in range(0, len(labels)):
        r[labels[i]] = values[i]
    return r


def evaluate_journal_data(items):
    unmatched = []
    for label, value, expected_values, err_msg in items:
        if expected_values is None or expected_values == '':
            expected_values = _('no value')
        if not isinstance(expected_values, list):
            expected_values = [expected_values]
        expected_values_msg = _(' or ').join(expected_values)
        value = _('no value') if value is None else value.strip()
        if len(expected_values) == 0:
            expected_values_msg = _('no value')
            status = validation_status.STATUS_WARNING if value != expected_values_msg else validation_status.STATUS_OK
        else:
            status = validation_status.STATUS_OK
            if not value in expected_values:
                if label == _('license'):
                    status = err_msg
                    for expected_value in expected_values:
                        if '/' + expected_value.lower() + '/' in str(value) + '/':
                            status = validation_status.STATUS_OK
                            break
                else:
                    status = err_msg
        if status != validation_status.STATUS_OK:
            unmatched.append({_('data'): label, 'status': status, _('in XML'): value, _('registered journal data') + '*': expected_values_msg, _('why it is not a valid message?'): ''})

    validations_result = ''
    if len(unmatched) > 0:
        validations_result = html_reports.sheet([_('data'), 'status', _('in XML'), _('registered journal data') + '*', _('why it is not a valid message?')], unmatched, table_style='dbstatus')
    return validations_result


def processing_result_location(result_path):
    return '<h5>' + _('Result of the processing:') + '</h5>' + '<p>' + html_reports.link('file:///' + result_path, result_path) + '</p>'


def display_report(report_filename):
    try:
        webbrowser.open('file:///' + report_filename.replace('//', '/').encode(encoding=sys.getfilesystemencoding()), new=2)
    except:
        pass


def articles_sorted_by_order(articles):
    l = sorted([(article.order, xml_name) for xml_name, article in articles.items()])
    l = [(xml_name, articles[xml_name]) for order, xml_name in l]
    return l


def max_score(quote, score):
    return ((score * quote) / 100) + 1


def db_status_item_row(article, history):
    labels = ['order', 'name', 'article title', 'creation date | last update', 'history']
    _source = source
    if source == 'registered':
        _source = 'database'
        _dates = str(article.creation_date_display) + ' / ' + str(article.last_update_display)
    else:
        _dates = ''

    values = []
    values.append(article.order)
    values.append(article.xml_name)
    values.append(_dates)
    values.append(article.title)
    values.append(history)
    return (labels, values)


def error_msg_subtitle():
    msg = html_reports.tag('p', _('Blocking error - indicates errors of data consistency'))
    msg += html_reports.tag('p', _('Fatal error - indicates errors which impact on the quality of the bibliometric indicators and other services'))
    msg += html_reports.tag('p', _('Error - indicates the other kinds of errors'))
    msg += html_reports.tag('p', _('Warning - indicates that something can be an error or something needs more attention'))
    return html_reports.tag('div', msg, 'subtitle')


def label_errors(content):
    if content is None:
        content = ''
    else:
        content = label_errors_type(content, validation_status.STATUS_BLOCKING_ERROR, 'B')
        content = label_errors_type(content, validation_status.STATUS_FATAL_ERROR, 'F')
        content = label_errors_type(content, validation_status.STATUS_ERROR, 'E')
        content = label_errors_type(content, validation_status.STATUS_WARNING, 'W')
    return content


def label_errors_type(content, error_type, prefix):
    new = []
    i = 0
    content = content.replace(error_type, '~BREAK~' + error_type)
    for part in content.split('~BREAK~'):
        if part.startswith(error_type):
            i += 1
            part = part.replace(error_type, error_type + ' [' + prefix + str(i) + ']')
        new.append(part)
    return ''.join(new)


def word_counter(content, word):
    return len(content.split(word)) - 1


def number_after_words(content, text='Total of errors = '):
    n = 0
    if text in content:
        content = content[content.find(text) + len(text):]
        finished = False
        n = ''
        while not finished and len(content) > 0:
            if content[0].isdigit():
                n += content[0]
                content = content[1:]
            else:
                finished = True

        if len(n) > 0:
            n = int(n)
        else:
            n = 0
    return n


def rst_title(title):
    return '\n\n' + title + '\n' + '-'*len(title) + '\n'
