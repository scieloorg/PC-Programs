
# code = utf-8

import os
import shutil

from __init__ import _
from . import attributes
from . import article_reports
from . import article_validations
from . import fs_utils
from . import html_reports
from . import validation_status
from . import xpchecker
from . import xc_models
from . import utils


class ValidationsResultItems(dict):

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
            items.append((status, validation_status.STATUS_LABELS.get(status), str(self.numbers.get(status, 0))))
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

    def statistics_display(self, inline=True, html_format=True):
        tag_name = 'span'
        text = ' | '.join([k + ': ' + v for ign, k, v in self.statistics_label_and_number if v != '0'])
        if not inline:
            tag_name = 'div'
            text = ''.join([html_reports.tag('p', html_reports.display_label_value(_('Total of ') + k, v)) for ign, k, v in self.statistics_label_and_number])
        if html_format:
            style = validation_status.message_style(self.statistics_label_and_number)
            r = html_reports.tag(tag_name, text, style)
        else:
            r = text
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

            items.append([_('NLM title'), article.journal_id_nlm_ta, self.journal_data.nlm_title, validation_status.STATUS_FATAL_ERROR])
            #items.append([_('journal-id (publisher-id)'), article.journal_id_publisher_id, self.journal_data.acron, validation_status.STATUS_FATAL_ERROR])
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
            if self.issue_error_msg is not None:
                r = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to identify {unidentified}. ').format(unidentified=_('issue'))
                r += self.issue_error_msg
            elif self.issue_models:
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
        if '_' in work_area.new_name or '.' in work_area.new_name:
            name_error = rst_title(_('Name errors')) + _('{value} has forbidden characters, which are {forbidden_characters}').format(value=work_area.new_name, forbidden_characters='_.') + separator

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
            content = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to get data from {item}. ').format(item=work_area.new_name)
        else:
            article_validation = article_validations.ArticleContentValidation(self.doi_services, self.articles_data.journal, article, (self.articles_data.articles_db_manager is not None), False)
            article_display_report = article_reports.ArticleDisplayReport(article_validation, pkg_path, work_area.new_name)
            article_validation_report = article_reports.ArticleValidationReport(article_validation)

            content = []

            if is_xml_generation:
                content.append(article_display_report.issue_header)
                content.append(article_display_report.article_front)
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.display_formulas)
                content.append(article_display_report.table_tables)
                r = open(work_area.images_report_filename).read()
                r = r[r.find('<body'):]
                r = r[r.find('>')+1:]
                r = r[:r.find('</body>')]
                content.append(r)
                content.append(article_display_report.article_body)
                content.append(article_display_report.article_back)
            else:
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.display_formulas)
                content.append(article_display_report.table_tables)
                r = open(work_area.images_report_filename).read()
                r = r[r.find('<body'):]
                r = r[r.find('>')+1:]
                r = r[:r.find('</body>')]
                content.append(r)
                content.append(article_display_report.files_and_href())
            content = html_reports.join_texts(content)
        return content, article_display_report


class ArticleValidations(object):

    def __init__(self, article, work_area, issue_data_validations):
        self.issue_data_validations = issue_data_validations
        self.work_area = work_area
        self.article = article
        self.validations = {}
        self.validations['xmlstructure'] = ValidationsResult()
        self.validations['xmlcontent'] = ValidationsResult()

    def validate(self, pkg, xml_structure_validator, xml_content_validator):

        #utils.display_message(_(' - validate XML structure'))
        self.logger.register(' xmlstructure')
        self.validations['xmlstructure'].message = xml_structure_validator.validate(self.work_area)

        #utils.display_message(_(' - validate XML contents'))
        self.logger.register(' xmlcontent')
        self.validations['xmlcontent'].message, self.article_display_report = xml_content_validator.validate(self.article, pkg.pkg_path, self.work_area, pkg.is_xml_generation)

        if pkg.is_xml_generation:
            stats = self.validations['xmlcontent'].statistics_display(False)
            title = [_('Data Quality Control'), self.work_area.new_name]
            fs_utils.write_file(self.work_area.data_report_filename, html_reports.html(title, stats + self.validations['xmlcontent'].message))

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in self.validations.values()])

    def hide_and_show_block(self, report_id, new_name):
        blocks = []
        block_parent_id = report_id + new_name
        blocks.append((_('Structure Validations'), 'xmlrep', self.validations['xmlstructure']))
        blocks.append((_('Contents Validations'),  'datarep', self.validations['xmlcontent']))
        if self.issue_data_validations:
            blocks.append((_('Converter Validations'), 'xcrep', self.issue_data_validations))
        _blocks = []
        for label, style, validations_file in blocks:
            if validations_file.total() > 0:
                status = validations_file.statistics_display()
                _blocks.append(html_reports.HideAndShowBlockItem(block_parent_id, label, style + new_name, style, validations_file.message, status))
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
        r += u'<p>{}: {}</p>'.format(_('XML path'), self.pkg_path)
        r += u'<p>{}: {}</p>'.format(_('Total of XML files'), len(self.pkg_articles))

        files = ''
        for name, article in self.pkg_articles.items():
            files += '<li>{}</li>'.format(html_reports.format_list(name, 'ol', article.package_files))
        r += '<ol>{}</ol>'.format(files)
        return u'<div class="xmllist">{}</div>'.format(r)

    @property
    def invalid_xml_name_items(self):
        return sorted([xml_name for xml_name, doc in self.pkg_articles.items() if doc.tree is None])

    @property
    def invalid_xml_report(self):
        r = ''
        if len(self.invalid_xml_name_items) > 0:
            r += html_reports.tag('div', html_reports.p_message(_('{status}: invalid XML files. ').format(status=validation_status.STATUS_BLOCKING_ERROR)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', self.invalid_xml_name_items, 'issue-problem'))
        return r

    def data(self):
        pkg_journal_title = None
        pkg_p_issn = None
        pkg_e_issn = None
        pkg_issue_label = None
        data = list(set([(a.journal_title, a.print_issn, a.e_issn, a.issue_label) for a in self.pkg_articles.values()]))
        data.sort(reverse=True)
        if len(data) > 0:
            data = list(data[0])
            if any(data):
                pkg_journal_title, pkg_p_issn, pkg_e_issn, pkg_issue_label = data
        return pkg_journal_title, pkg_p_issn, pkg_e_issn, pkg_issue_label


class ArticlesData(object):

    def __init__(self):
        self.pkg_journal_title = None
        self.pkg_p_issn = None
        self.pkg_e_issn = None
        self.pkg_issue_label = None

        self.journal = None
        self.journal_data = None
        self._issue_label = None
        self.issue_models = None
        self.issue_error_msg = None

        self.serial_path = None
        self.articles_db_manager = None

    def setup(self, pkg, db_manager):
        self.pkg_journal_title, self.pkg_p_issn, self.pkg_e_issn, self.pkg_issue_label = pkg.data()
        if db_manager is None:
            journals_list = xc_models.JournalsList()
            self.journal = journals_list.get_journal(self.pkg_p_issn, self.pkg_e_issn, self.pkg_journal_title)
            self.journal_data = journals_list.get_journal_data(self.pkg_p_issn, self.pkg_e_issn, self.pkg_journal_title)
        else:
            self._identify_registered_data(db_manager)
            self.serial_path = db_manager.serial_path

    @property
    def acron(self):
        a = 'unknown_acron'
        if self.journal is not None:
            if self.journal.acron is not None:
                a = self.journal.acron
        return a

    @property
    def acron_issue_label(self):
        return self.acron + ' ' + self.issue_label

    @property
    def issue_label(self):
        r = self._issue_label if self._issue_label else self.pkg_issue_label
        if r is None:
            r = 'unknown_issue_label'
        return r

    def _identify_registered_data(self, db_manager):
        acron_issue_label, self.issue_models, self.issue_error_msg, self.journal, self.journal_data = db_manager.get_registered_data(self.pkg_journal_title, self.pkg_issue_label, self.pkg_p_issn, self.pkg_e_issn)
        ign, self._issue_label = acron_issue_label.split(' ')
        if self.issue_error_msg is None:
            issue_files = db_manager.get_issue_files(self.issue_models)
            self.articles_db_manager = xc_models.ArticlesManager(db_manager.db_isis, issue_files)


class RegisteredArticles(dict):

    def __init__(self, registered_articles):
        dict.__init__(self, registered_articles)

    def registered_item(self, name, article):
        found = None
        registered = self.get(name)
        if registered is not None:
            exact_comparison_result, relax_result = articles_similarity(registered, article)
            status = evaluate_articles_similarity_result(exact_comparison_result, relax_result)
            if registered.order == article.order and status in [validation_status.STATUS_INFO, validation_status.STATUS_WARNING]:
                found = registered
        return found

    def registered_order(self, order):
        return [reg_name for reg_name, reg in self.items() if reg.order == order]

    def registered_titles_and_authors(self, article):
        similar_items = []
        for name, registered in self.items():
            exact_comparison_result, relax_result = articles_similarity(registered, article)
            status = evaluate_articles_similarity_result(exact_comparison_result, relax_result)
            if status in [validation_status.STATUS_INFO, validation_status.STATUS_WARNING]:
                similar_items.append(name)
        return similar_items

    def search_articles(self, name, article):
        registered = self.registered_item(name, article)
        registered_titaut = registered
        registered_name = registered
        registered_order = registered
        if registered is None:
            matched_titaut_article_names = self.registered_titles_and_authors(article)
            matched_order_article_names = self.registered_order(article.order)

            registered_titaut = self.registered_items_by_names(matched_titaut_article_names)
            registered_order = self.registered_items_by_names(matched_order_article_names)
            registered_name = self.get(name)
        return (registered_titaut, registered_name, registered_order)

    def registered_items_by_names(self, found_names):
        if len(found_names) == 0:
            return None
        elif len(found_names) == 1:
            return self.get(found_names[0])
        else:
            return {name: self.get(name) for name in found_names}

    def analyze_registered_articles(self, name, registered_titaut, registered_name, registered_order):
        actions = None
        conflicts = None
        old_name = None
        #print('analyze_registered_articles')
        #print([registered_titaut, registered_name, registered_order])
        #print('-')
        if registered_titaut is None and registered_order is None and registered_name is None:
            actions = 'add'
        elif all([registered_titaut, registered_order, registered_name]):
            if id(registered_titaut) == id(registered_order) == id(registered_name):
                actions = 'update'
            elif id(registered_titaut) == id(registered_name):
                # titaut + name != order
                # rejeitar
                conflicts = {_('registered article retrieved by the order'): registered_order, _('registered article retrieved by title/authors/name'): registered_titaut}
            elif id(registered_titaut) == id(registered_order):
                # titaut + order != name
                # rejeitar
                conflicts = {'registered article retrieved by title/authors/order': registered_order, _('registered article retrieved by name'): registered_name}
            elif id(registered_name) == id(registered_order):
                # order + name != titaut
                # rejeitar
                conflicts = {'registered article retrieved by name/order': registered_order, _('registered article retrieved by title/authors'): registered_titaut}
            else:
                # order != name != titaut
                # rejeitar
                conflicts = {_('name'): registered_name, _('registered article retrieved by the order'): registered_order, _('title/authors'): registered_titaut}
        elif all([registered_titaut, registered_order]):
            if id(registered_titaut) == id(registered_order):
                if registered_order.is_ex_aop:
                    actions = 'reject'
                else:
                    actions = 'name change'
                    old_name = registered_titaut.xml_name
            else:
                conflicts = {_('registered article retrieved by the order'): registered_order, _('title/authors'): registered_titaut}
        elif all([registered_titaut, registered_name]):
            if id(registered_titaut) == id(registered_name):
                if registered_name.is_ex_aop:
                    actions = 'reject'
                else:
                    actions = 'order change'
            else:
                conflicts = {_('registered article retrieved by title/authors'): registered_titaut, _('registered article retrieved by name'): registered_name}
        elif all([registered_order, registered_name]):
            if id(registered_order) == id(registered_name):
                # titulo autores etc muito diferentes
                conflicts = {_('registered article retrieved by the order'): registered_order}
            else:
                conflicts = {_('registered article retrieved by the order'): registered_order, _('registered article retrieved by name'): registered_name}
        elif registered_titaut is not None:
            # order e name nao encontrados; order testar antes de atualizar;
            if registered_titaut.is_ex_aop:
                actions = 'reject'
            else:
                actions = 'order change, name change'
                old_name = registered_titaut.xml_name
        elif registered_name is not None:
            conflicts = {_('registered article retrieved by name'): registered_name}
        elif registered_order is not None:
            conflicts = {_('registered article retrieved by the order'): registered_order}
        #print((actions, old_name, conflicts))
        return (actions, old_name, conflicts)


class ArticlesMerger(object):

    def __init__(self, registered_articles, pkg_articles):
        self._merged_articles = registered_articles.copy()
        self.registered_articles = RegisteredArticles(registered_articles)
        self.pkg_articles = pkg_articles

    def analyze_pkg(self):
        self._exclusions = []
        self._conflicts = {}
        self._actions = {}
        self._name_changes = {}
        self.order_changes = {}

        for name, article in self.pkg_articles.items():
            action, old_name, conflicts = self.analyze_pkg_article(name, article)
            if conflicts is not None:
                self._conflicts[name] = conflicts
            if action is not None:
                self._actions[name] = action
            if action == 'update' and article.marked_to_delete:
                self._exclusions.append(name)
            if old_name is not None:
                self._name_changes[old_name] = name
            if name in self.registered_articles.keys():
                if article.order != self.registered_articles[name].order:
                    self.order_changes[name] = (self.registered_articles[name].order, article.order)

    def analyze_pkg_article(self, name, pkg_article):
        registered_titaut, registered_name, registered_order = self.registered_articles.search_articles(name, pkg_article)
        action, old_name, conflicts = self.registered_articles.analyze_registered_articles(name, registered_titaut, registered_name, registered_order)
        return (action, old_name, conflicts)

    @property
    def merged_articles(self):
        return self._merged_articles

    def merge(self):
        self.analyze_pkg()
        self.update_articles()

    def update_articles(self):
        self.history_items = {}
        # starts history with registered articles data
        self.history_items = {name: [('registered article', article)] for name, article in self.registered_articles.items()}

        # exclude registered items
        for name in self._exclusions:
            self.history_items[name].append(('excluded article', self._merged_articles[name]))
            del self._merged_articles[name]

        # indicates package articles reception
        for name, article in self.pkg_articles.items():
            if not name in self.history_items.keys():
                self.history_items[name] = []
            self.history_items[name].append(('package', article))

        # indicates names changes, and exclude old names
        for previous_name, name in self._name_changes.items():
            self.history_items[previous_name].append(('replaced by', self.pkg_articles[name]))

            self.history_items[name].append(('replaces', self._merged_articles[previous_name]))
            del self._merged_articles[previous_name]

        # merge pkg and registered, considering some of them are rejected
        orders_to_check = []
        for name, article in self.pkg_articles.items():
            if not article.marked_to_delete:
                action = self._actions.get(name)

                if name in self._conflicts.keys():
                    action = 'reject'
                if not action in ['reject', None]:
                    self._merged_articles[name] = self.pkg_articles[name]

        #for name, article in self.merged_articles.items():
        #    if article.order in self.orders_conflicts(self.merged_articles).keys() or self._actions.get(name) in ['reject', None]:
        #        self.history_items[name].append(('rejected', self._merged_articles[name]))

    def registered_data_conflicts_report(self):
        merging_errors = []
        if len(self._conflicts) > 0:
            merging_errors = [html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to update because the registered article data and the package article data do not match. '))]
            for name, conflicts in self._conflicts.items():
                labels = ['package']
                values = [article_reports.display_article_data_to_compare(self.pkg_articles.get(name))]
                for k, articles in conflicts.items():
                    labels.append(k)
                    if isinstance(articles, dict):
                        data = []
                        for article in articles.values():
                            data.append(article_reports.display_article_data_to_compare(article))
                        values.append(''.join(data))
                    else:
                        values.append(article_reports.display_article_data_to_compare(articles))
                merging_errors.append(html_reports.sheet(labels, [label_values(labels, values)], table_style='dbstatus', html_cell_content=labels))
        return ''.join(merging_errors)

    @property
    def validations(self):
        v = ValidationsResult()
        v.message = ''.join([display_order_conflicts(self.orders_conflicts(self.merged_articles)) + self.registered_data_conflicts_report()])
        return v

    @property
    def total_to_convert(self):
        return len(self.pkg_articles)

    def orders_conflicts(self, articles):
        orders = {}
        for name, article in articles.items():
            if not article.order in orders.keys():
                orders[article.order] = []
            orders[article.order].append(name)
        return {order: names for order, names in orders.items() if len(names) > 1}

    @property
    def excluded_orders(self):
        #excluded_orders
        items = {}
        orders = [article.order for article in self._merged_articles.values()]
        for name, article in self.registered_articles.items():
            if not article.order in orders:
                items[name] = article.order
        return {name: article.order for name, article in self.registered_articles.items() if not article.order in orders}

    @property
    def xc_articles(self):
        return self.pkg_articles

    @property
    def names_change_report(self):
        r = []
        if len(self._name_changes) > 0:
            r.append(html_reports.tag('h3', _('Names changes')))
            for old, new in self._name_changes.items():
                r.append(html_reports.tag('p', '{old} => {new}'.format(old=old, new=new), 'info'))
        return ''.join(r)

    @property
    def orders_change_report(self):
        r = []
        if len(self.order_changes) > 0:
            r.append(html_reports.tag('h3', _('Orders changes')))
            for name, changes in self.order_changes.items():
                r.append(html_reports.tag('p', '{name}: {old} => {new}'.format(name=name, old=changes[0], new=changes[1]), 'info'))
        if len(self.excluded_orders) > 0:
            r.append(html_reports.tag('h3', _('Orders exclusions')))
            for name, order in self.excluded_orders.items():
                r.append(html_reports.tag('p', '{order} ({name})'.format(name=name, order=order), 'info'))
        return ''.join(r)

    @property
    def changes_report(self):
        r = ''
        r += self.orders_change_report
        r += self.names_change_report
        if len(r) > 0:
            r = html_reports.tag('h2', _('Changes Report')) + r
        return r


class ArticlesSetValidations(object):

    def __init__(self, pkg, articles_data, logger):
        self.logger = logger
        self.pkg = pkg
        self.articles_data = articles_data

        self.registered_articles = {}
        self.is_db_generation = articles_data.articles_db_manager is not None
        if articles_data.articles_db_manager is not None:
            self.registered_articles = articles_data.articles_db_manager.registered_articles

        self.articles_merger = ArticlesMerger(self.registered_articles, self.pkg.pkg_articles)
        self.articles_merger.merge()
        self.merged_articles = self.articles_merger.merged_articles

        self.articles_validations = {}

        self.ERROR_LEVEL_FOR_UNIQUE_VALUES = {'order': validation_status.STATUS_BLOCKING_ERROR, 'doi': validation_status.STATUS_BLOCKING_ERROR, 'elocation id': validation_status.STATUS_BLOCKING_ERROR, 'fpage-lpage-seq-elocation-id': validation_status.STATUS_ERROR}
        if not self.is_db_generation:
            self.ERROR_LEVEL_FOR_UNIQUE_VALUES['order'] = validation_status.STATUS_WARNING
        self.IGNORE_NONE = ['journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', ]
        self.EXPECTED_COMMON_VALUES_LABELS = ['journal-title', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'issue label', 'issue pub date', 'license']
        self.REQUIRED_DATA = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        self.EXPECTED_UNIQUE_VALUE_LABELS = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']

    @property
    def merged_articles_common_data(self):
        data = {}
        for label in self.EXPECTED_COMMON_VALUES_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]
                if label in self.IGNORE_NONE and value is None:
                    pass
                else:
                    if not value in values:
                        values[value] = []
                    values[value].append(xml_name)

            data[label] = values
        return data

    @property
    def merged_articles_unique_data(self):
        data = {}
        for label in self.EXPECTED_UNIQUE_VALUE_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]
                if value is not None:
                    if not value in values:
                        values[value] = []
                    values[value].append(xml_name)

            data[label] = values
        return data

    @property
    def merged_articles_missing_required_values(self):
        required_items = {}
        for label in self.REQUIRED_DATA:
            if label in self.merged_articles_common_data.keys():
                if None in self.merged_articles_common_data[label].keys():
                    required_items[label] = self.merged_articles_common_data[label][None]
        return required_items

    @property
    def conflicting_values_in_merged_articles(self):
        data = {}
        for label, values in self.merged_articles_common_data.items():
            if len(values) > 1:
                data[label] = values
        return data

    @property
    def duplicated_values_in_merged_articles(self):
        duplicated_labels = {}
        for label, values in self.merged_articles_unique_data.items():
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
        return all([a for a in self.merged_articles.values() if a.is_epub_only])

    @property
    def articles(self):
        return articles_sorted_by_order(self.merged_articles)

    @property
    def pkg_articles(self):
        return articles_sorted_by_order(self.pkg.pkg_articles)

    @property
    def pkg_journal_validations_report_title(self):
        #FIXME
        signal = ''
        msg = ''
        if not self.is_db_generation:
            signal = '<sup>*</sup>'
            msg = html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('Journal data in the XML files must be consistent with {link}').format(link=html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv')), 'note')
        return html_reports.tag('h2', _('Journal data: XML files and registered data') + signal) + msg

    def validate(self, doi_services, dtd_files, articles_work_area):
        utils.display_message(_('Validate package ({n} files)').format(n=len(self.pkg.pkg_articles)))
        if len(self.registered_articles) > 0:
            utils.display_message(_('Previously registered: ({n} files)').format(n=len(self.registered_articles)))

        self.logger.register('compile_references')
        self.compile_references()

        self.logger.register('pkg_journal_validations')
        self.pkg_journal_validations = ValidationsResultItems()
        self.pkg_journal_validations.title = self.pkg_journal_validations_report_title

        self.logger.register('pkg_issue_validations')
        self.pkg_issue_validations = ValidationsResultItems()
        self.pkg_issue_validations.title = html_reports.tag('h2', _('Checking issue data: XML files and registered data'))

        self.logger.register('articles validations - prep')

        xml_journal_data_validator = XMLJournalDataValidator(self.articles_data.journal_data)
        xml_issue_data_validator = XMLIssueDataValidator(self.is_db_generation, self.articles_data.issue_error_msg, self.articles_data.issue_models)
        xml_structure_validator = XMLStructureValidator(dtd_files)
        xml_structure_validator.logger = self.logger
        xml_content_validator = XMLContentValidator(doi_services, self.articles_data)

        self.logger.register('articles validations')
        self.articles_validations = {}

        for name, article in self.pkg.pkg_articles.items():
            utils.display_message(_('Validate {name}').format(name=name))
            self.logger.register(' '.join(['validate', name]))

            #utils.display_message(_(' - validate journal data'))
            self.pkg_journal_validations[name] = ValidationsResult()
            self.pkg_journal_validations[name].message = xml_journal_data_validator.validate(article)

            #utils.display_message(_(' - validate issue data'))
            self.pkg_issue_validations[name] = ValidationsResult()
            self.pkg_issue_validations[name].message = xml_issue_data_validator.validate(article)

            self.articles_validations[name] = ArticleValidations(article, articles_work_area[name], self.pkg_issue_validations[name])
            self.articles_validations[name].logger = self.logger
            self.articles_validations[name].validate(self.pkg, xml_structure_validator, xml_content_validator)

            self.logger.register(' '.join([name, 'fim']))

        self.logger.register('consistency validations')
        self.consistency_validations = ValidationsResult()

        issue_message = self.consistency_validations_report
        if self.articles_data.issue_error_msg is not None:
            issue_message = self.articles_data.issue_error_msg + issue_message

        self.consistency_validations.message = issue_message

        self.logger.register('xc pre validations - fim')

    @property
    def detailed_report(self):
        labels = [_('filename'), 'order', _('article'), 'aop pid/related', _('reports')]
        widths = {}
        widths[_('filename')] = '10'
        widths['order'] = '5'
        widths[_('article')] = '60'
        widths['aop pid/related'] = '10'
        widths[_('reports')] = '10'
        pdf_items = []
        items = []
        for new_name, article in self.pkg_articles:
            hide_and_show_block_items = self.articles_validations[new_name].hide_and_show_block('view-reports-', new_name)
            values = []
            values.append(new_name)
            values.append(article.order)
            if self.articles_validations[new_name].article_display_report is None:
                values.append('')
            else:
                values.append(self.articles_validations[new_name].article_display_report.table_of_contents)
            related = {}
            for k, v in {'article-id(previous-pid)': article.previous_pid, 'related': [item.get('xml', '') for item in article.related_articles]}.items():
                if v is not None:
                    if len(v) > 0:
                        related[k] = v
            values.append(related)
            items.append((values, hide_and_show_block_items))
        report = html_reports.HideAndShowBlocksReport(labels, items, html_cell_content=[_('article')], widths=widths)
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
            values.append(utils.display_datetime(doc.received_dateiso))
            values.append(utils.display_datetime(doc.accepted_dateiso))
            values.append(str(doc.history_days))
            values.append(utils.display_datetime(doc.article_pub_dateiso))
            values.append(utils.display_datetime(doc.issue_pub_dateiso))
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
    def merged_articles_pages_report(self):
        # FIXME
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        error_level = validation_status.STATUS_BLOCKING_ERROR
        fpage_and_article_id_other_status = [all([a.fpage, a.lpage, a.article_id_other]) for xml_name, a in self.articles]
        if all(fpage_and_article_id_other_status):
            error_level = validation_status.STATUS_ERROR

        for xml_name, article in self.articles:
            fpage = article.fpage
            lpage = article.lpage
            msg = []
            status = ''
            if article.pages == '':
                msg.append(_('no pagination was found. '))
                if not article.is_ahead:
                    status = validation_status.STATUS_ERROR
            if fpage is not None and lpage is not None:
                if fpage.isdigit() and lpage.isdigit():
                    int_fpage = int(fpage)
                    int_lpage = int(lpage)

                    #if not article.is_rolling_pass and not article.is_ahead:
                    if int_previous_lpage is not None:
                        if int_previous_lpage > int_fpage:
                            status = error_level if not article.is_epub_only else validation_status.STATUS_WARNING
                            msg.append(_('Invalid value for fpage and lpage. Check lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage == int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}) are the same. ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage + 1 < int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('There is a gap between lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                    if int_fpage > int_lpage:
                        status = error_level
                        msg.append(_('Invalid page range: {fpage} (fpage) > {lpage} (lpage). '.format(fpage=int_fpage, lpage=int_lpage)))
                    int_previous_lpage = int_lpage
                    previous_lpage = lpage
                    previous_xmlname = xml_name
            #dates = '|'.join([item if item is not None else 'none' for item in [article.epub_ppub_dateiso, article.collection_dateiso, article.epub_dateiso]])
            msg = '\n'.join(msg)
            results.append({'label': xml_name, 'status': status, 'pages': article.pages, 'message': msg, _('why it is not a valid message?'): ''})
        return html_reports.tag('h2', _('Pages Report')) + html_reports.tag('div', html_reports.sheet(['label', 'status', 'pages', 'message', _('why it is not a valid message?')], results, table_style='validation_sheet', widths={'label': '10', 'status': '10', 'pages': '5', 'message': '75'}))

    @property
    def journal_issue_header_report(self):
        merged_articles_common_data = ''
        for label, values in self.merged_articles_common_data.items():
            if len(values.keys()) == 1:
                merged_articles_common_data += html_reports.tag('p', html_reports.display_label_value(label, values.keys()[0]))
            else:
                merged_articles_common_data += html_reports.format_list(label + ':', 'ol', values.keys())
        return html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', merged_articles_common_data, 'issue-data')

    @property
    def missing_items_in_merged_articles_report(self):
        r = ''
        for label, items in self.merged_articles_missing_required_values.items():
            r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_BLOCKING_ERROR, label=label)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
        return r

    @property
    def duplicated_values_in_merged_articles_report(self):
        parts = []
        for label, values in self.duplicated_values_in_merged_articles.items():
            status = self.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
            _m = _('Unique value for {label} is required for all the documents in the package').format(label=label)
            parts.append(html_reports.p_message(status + ': ' + _m))
            for value, xml_files in values.items():
                parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def conflicting_values_in_merged_articles_report(self):
        parts = []
        for label, values in self.conflicting_values_in_merged_articles.items():
            compl = ''
            _status = validation_status.STATUS_BLOCKING_ERROR
            if label == 'issue pub date':
                if self.is_rolling_pass:
                    _status = validation_status.STATUS_WARNING
            elif label == 'license':
                _status = validation_status.STATUS_WARNING
            _m = _('{status}: same value for {label} is required for all the documents in the package. ').format(status=_status, label=label)
            parts.append(html_reports.p_message(_m))
            parts.append(html_reports.tag('div', html_reports.format_html_data(values), 'issue-problem'))
        return ''.join(parts)

    @property
    def consistency_validations_report(self):
        text = []
        text += self.pkg.invalid_xml_report
        text += self.missing_items_in_merged_articles_report
        text += self.conflicting_values_in_merged_articles_report
        text += self.duplicated_values_in_merged_articles_report
        text = html_reports.tag('div', ''.join(text), 'issue-messages')
        text += self.merged_articles_pages_report
        return html_reports.tag('h2', _('Checking issue data consistency')) + text

    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.journal_issue_header_report)
        report.append(self.pkg_journal_validations.report(errors_only=not self.pkg.is_xml_generation))
        report.append(self.pkg_issue_validations.report(errors_only=not self.pkg.is_xml_generation))
        if self.consistency_validations.total() > 0:
            report.append(self.consistency_validations.message)

        if self.articles_merger.validations.total() > 0:
            report.append(html_reports.tag('h2', _('Data Conflicts Report')))
            report.append(self.articles_merger.validations.message)
        return ''.join(report)

    @property
    def blocking_errors(self):
        return sum([self.consistency_validations.blocking_errors, self.pkg_issue_validations.blocking_errors, self.articles_merger.validations.blocking_errors])

    @property
    def fatal_errors(self):
        return sum([v.fatal_errors for v in self.articles_validations.values()])


class ReportsMaker(object):

    def __init__(self, orphan_files, articles_set_validations, files_location, xpm_version=None, conversion=None):
        self.processing_result_location = None
        self.orphan_files = orphan_files
        self.articles_set_validations = articles_set_validations
        self.conversion = conversion
        self.xpm_version = xpm_version
        self.files_location = files_location

        self.tabs = ['pkg-files', 'summary-report', 'group-validations-report', 'individual-validations-report', 'references', 'dates-report', 'aff-report', 'xc-validations', 'website']
        self.labels = {
            'pkg-files': _('Files/Folders'),
            'summary-report': _('Summary'),
            'group-validations-report': _('Group Validations'),
            'individual-validations-report': _('Individual Validations'),
            'xc-validations': _('Converter Validations'),
            'aff-report': _('Affiliations'),
            'dates-report': _('Dates'),
            'references': _('References'),
            'website': _('Website'),
        }
        self.validations = ValidationsResult()

    @property
    def orphan_files_report(self):
        if len(self.orphan_files) > 0:
            return '<div class="xmllist"><p>{}</p>{}</div>'.format(_('Invalid files names'), html_reports.format_list('', 'ol', self.orphan_files))
        return ''

    @property
    def report_components(self):
        components = {}
        components['pkg-files'] = self.articles_set_validations.pkg.xml_list
        if self.processing_result_location is not None:
            components['pkg-files'] += processing_result_location(self.processing_result_location)

        components['summary-report'] = self.orphan_files_report
        components['group-validations-report'] = self.orphan_files_report
        components['individual-validations-report'] = self.articles_set_validations.detailed_report
        components['aff-report'] = self.articles_set_validations.articles_affiliations_report
        components['dates-report'] = self.articles_set_validations.articles_dates_report
        components['references'] = (self.articles_set_validations.references_overview_report +
            self.articles_set_validations.sources_overview_report)

        if not self.articles_set_validations.pkg.is_xml_generation:
            components['group-validations-report'] += self.articles_set_validations.journal_and_issue_report

        if self.conversion is None:
            components['website'] = toc_extended_report(self.articles_set_validations.pkg.pkg_articles)
        else:
            components['website'] = self.conversion.conclusion_message + toc_extended_report(self.conversion.registered_articles)
            if self.articles_set_validations.articles_data.issue_error_msg is not None:
                components['group-validations-report'] += self.articles_set_validations.articles_data.issue_error_msg

            #components['xc-validations'] = self.conversion.conclusion_message + self.conversion.articles_merger.changes_report + self.conversion.conversion_status_report + self.conversion.aop_status_report + self.conversion.articles_conversion_validations.report(True) + self.conversion.conversion_report
            components['xc-validations'] = html_reports.tag('h3', _('Conversion Result')) + self.conversion.conclusion_message + self.conversion.articles_merger.changes_report + self.conversion.aop_status_report + self.conversion.articles_conversion_validations.report(True) + self.conversion.conversion_report

        self.validations.message = html_reports.join_texts(components.values())

        components['summary-report'] += error_msg_subtitle() + self.validations.statistics_display(False)
        if self.conversion is not None:
            components['summary-report'] += html_reports.tag('h2', _('Summary report')) + self.conversion.conclusion_message

        components = {k: label_errors(v) for k, v in components.items() if v is not None}
        return components

    @property
    def footnote(self):
        content = html_reports.tag('p', _('finished'))
        if self.xpm_version is not None:
            content += html_reports.tag('p', _('report generated by XPM ') + self.xpm_version)
        return content

    def save_report(self, report_path, report_filename, report_title):
        filename = report_path + '/' + report_filename
        if not os.path.isdir(report_path):
            os.makedirs(report_path)
        #if os.path.isfile(filename):
        #    bkp_filename = report_path + '/' + report_filename + '-'.join(utils.now()) + '.html'
        #    shutil.copyfile(filename, bkp_filename)

        html_reports.save(filename, report_title, self.content)
        msg = _('Saved report: {f}').format(f=filename)
        utils.display_message(msg)
        self.xml_report(report_path)

    @property
    def content(self):
        tabbed_report = html_reports.TabbedReport(self.labels, self.tabs, self.report_components, 'summary-report')
        content = tabbed_report.report_content
        origin = ['{IMG_PATH}', '{PDF_PATH}', '{XML_PATH}', '{RES_PATH}', '{REP_PATH}']
        replac = [self.files_location.img_link, self.files_location.pdf_link, self.files_location.xml_link, self.files_location.result_path, self.files_location.report_path]
        for o, r in zip(origin, replac):
            content = content.replace(o, r)
        return content + self.footnote

    def xml_report(self, report_path):
        if self.files_location.web_url is None:
            print('xml report is not necessary')
        else:
            for item in self.articles_set_validations.pkg.xml_names:
                shutil.copyfile(self.articles_set_validations.pkg.pkg_path + '/' + item, report_path + '/' + item)


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
    for label, value, expected_values, default_status in items:
        if expected_values is None:
            expected_values = [None]
        if len(expected_values) == 0:
            expected_values.extend([None, ''])
        status = validation_status.STATUS_OK
        if not value in expected_values:
            status = default_status
            for expected_value in expected_values:
                if expected_value is not None and value is not None:
                    if '/' + expected_value.lower() + '/' in value.lower() + '/':
                        status = validation_status.STATUS_OK
                        break

        if status != validation_status.STATUS_OK:
            if None in expected_values:
                expected_values = [item for item in expected_values if item is not None]
                expected_values.append(_('none'))
            unmatched.append({_('data'): label, 'status': status, 'XML': value, _('registered journal data') + '*': _(' or ').join(expected_values), _('why it is not a valid message?'): ''})

    validations_result = ''
    if len(unmatched) > 0:
        validations_result = html_reports.sheet([_('data'), 'status', 'XML', _('registered journal data') + '*', _('why it is not a valid message?')], unmatched, table_style='dbstatus')
    return validations_result


def processing_result_location(result_path):
    return '<h5>' + _('Result of the processing:') + '</h5>' + '<p>' + html_reports.link('file:///' + result_path, result_path) + '</p>'


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


def articles_similarity(article1, article2):
    relaxed_labels = [_('titles'), _('authors')]
    relaxed_data = []
    relaxed_data.append((article1.textual_titles, article2.textual_titles))
    relaxed_data.append((article_reports.display_authors(article1.article_contrib_items, '; '), article_reports.display_authors(article2.article_contrib_items, '; ')))

    if not any([article1.textual_titles, article2.textual_titles, article1.textual_contrib_surnames, article2.textual_contrib_surnames]):
        if article1.body_words is not None and article2.body_words is not None:
            relaxed_labels.append(_('body'))
            relaxed_data.append((article1.body_words[0:200], article2.body_words[0:200]))

    exact_labels = [_('order'), _('prefix'), _('doi')]
    exact_data = []
    exact_data.append((article1.order, article2.order))
    exact_data.append((article1.prefix, article2.prefix))
    exact_data.append((article1.doi, article2.doi))
    exact_data.extend(relaxed_data)
    exact_labels.extend(relaxed_labels)

    exact_comparison_result = [(label, items) for label, items in zip(exact_labels, exact_data) if not items[0] == items[1]]
    relaxed_comparison_result = [(label, items) for label, items in zip(relaxed_labels, relaxed_data) if not utils.is_similar(items[0], items[1])]
    return (exact_comparison_result, relaxed_comparison_result)


def evaluate_articles_similarity_result(exact_comparison_result, relaxed_comparison_result):
    status = validation_status.STATUS_BLOCKING_ERROR
    #print(len(exact_comparison_result))
    #print(len(relaxed_comparison_result))
    #print(exact_comparison_result)
    #print(relaxed_comparison_result)

    if len(exact_comparison_result) == 0:
        status = validation_status.STATUS_INFO
    elif len(exact_comparison_result) == 1 and len(relaxed_comparison_result) in [0, 1]:
        status = validation_status.STATUS_WARNING
    return status


def display_articles_differences(article1, article2, label1='article 1', label2='article 2'):
    exact_comparison_result, relaxed_comparison_result = articles_similarity(article1, article2)
    status = evaluate_articles_similarity_result(exact_comparison_result, relaxed_comparison_result)
    return format_diffences_message(status, exact_comparison_result, label1, label2)


def format_diffences_message(status, comparison_result, label1='article 1', label2='article 2'):
    msg = []
    if len(comparison_result) > 0:
        msg.append(html_reports.p_message(status))
        for label, differences in comparison_result:
            msg.append(html_reports.tag('p', differences[0] + '&#160;=>&#160;' + differences[1]))
    return ''.join(msg)


def display_order_conflicts(orders_conflicts):
    r = []
    if len(orders_conflicts) > 0:
        html_reports.tag('h2', _('Order conflicts'))
        for order, names in orders_conflicts.items():
            r.append(html_reports.tag('h3', order))
            r.append(html_reports.format_html_data(names))
    return ''.join(r)


def new_toc_extended_report(articles):
    if articles is None:
        return ''
    else:
        labels = [_('article'), _('last update')]
        widths = {_('last update'): '5', _('article'): '88'}
        items = []
        for new_name, article in articles_sorted_by_order(articles):
            if not article.is_ex_aop:
                values = []
                values.append(article_reports.display_article_data_in_toc(article))
                last_update_display = article.last_update_display
                if last_update_display is None:
                    last_update_display = ''
                if last_update_display[:10] == utils.display_datetime(utils.now()[0]):
                    last_update_display = html_reports.tag('span', last_update_display, 'report-date')
                values.append(last_update_display)
                items.append(label_values(labels, values))
        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=[_('article'), _('last update')], widths=widths)


def toc_extended_report(articles):
    if articles is None:
        return ''
    else:
        labels = [_('filename'), 'order', _('last update'), _('article')]
        widths = {_('filename'): '5', 'order': '2', _('last update'): '5', _('article'): '88'}
        items = []
        for new_name, article in articles_sorted_by_order(articles):
            if not article.is_ex_aop:
                values = []
                values.append(new_name)
                values.append(article.order)
                last_update_display = article.last_update_display
                if last_update_display is None:
                    last_update_display = ''
                if last_update_display[:10] == utils.display_datetime(utils.now()[0]):
                    last_update_display = html_reports.tag('span', last_update_display, 'report-date')
                values.append(last_update_display)
                values.append(article_reports.display_article_data_in_toc(article))
                items.append(label_values(labels, values))
        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=[_('article'), _('last update')], widths=widths)
