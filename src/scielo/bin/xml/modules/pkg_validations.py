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
from . import utils


class PackageValidationsResult(dict):

    def __init__(self):
        dict.__init__(self)
        self.title = ''

    @property
    def total(self):
        return sum([item.total() for item in self.values()])

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
        _reports = self.title
        for xml_name, results in self.items():
            if results.total() > 0 or errors_only is False:
                _reports += html_reports.tag('h4', xml_name)
                _reports += results.message
        return _reports

    def statistics_message(self):
        return '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(self.fatal_errors)), ('errors', str(self.errors)), ('warnings', str(self.warnings))]]) + ']'


class ValidationsResult(object):

    def __init__(self):
        self._message = ''
        self.fatal_errors = 0
        self.errors = 0
        self.warnings = 0

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self.fatal_errors, self.errors, self.warnings = html_reports.statistics_numbers(value)

    def total(self):
        return sum([self.fatal_errors, self.errors, self.warnings])

    def statistics_message(self):
        return '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(self.fatal_errors)), ('errors', str(self.errors)), ('warnings', str(self.warnings))]]) + ']'


class ValidationsFile(object):

    def __init__(self, filename):
        self.validations = ValidationsResult()
        self.filename = filename
        self.read()

    @property
    def message(self):
        return self.validations.message

    @message.setter
    def message(self, _message):
        self.validations.message = _message
        self.write()

    def total(self):
        return self.validations.total

    def statistics_message(self):
        return self.validations.statistics_message()

    def block_report(self, new_name, label, id):
        return self.validations.block_report

    def write(self):
        m = self.validations.message if self.validations.message is not None else ''
        fs_utils.write_file(self.filename, m)

    def read(self):
        if os.path.isfile(self.filename):
            self.message = fs_utils.read_file(self.filename)
        else:
            self.message = ''


class ArticleValidations(object):

    def __init__(self, article, work_area, pkg_path, is_xml_generation, is_db_generation, MAX_FATAL_ERRORS=None, MAX_ERRORS=None, MAX_WARNINGS=None):
        self.MAX_FATAL_ERRORS = MAX_FATAL_ERRORS
        self.MAX_ERRORS = MAX_ERRORS
        self.MAX_WARNINGS = MAX_WARNINGS
        self.article = article
        self.work_area = work_area
        self.pkg_path = pkg_path
        self.is_xml_generation = is_xml_generation
        self.is_db_generation = is_db_generation
        self.xml_journal_data_validations_file = ValidationsFile(self.work_area.journal_validations_filename)
        self.xml_issue_data_validations_file = ValidationsFile(self.work_area.issue_validations_filename)
        self.xml_structure_validations_file = ValidationsFile(self.work_area.dtd_report_filename)
        self.xml_content_validations_file = ValidationsFile(self.work_area.data_report_filename)

    @property
    def xml_validations(self):
        validations = ValidationsResult()
        validations.message = ''
        for item in [self.xml_journal_data_validations_file, self.xml_issue_data_validations_file, self.xml_structure_validations_file, self.xml_content_validations_file]:
            validations.message += item.message
        return validations

    def validate_xml_structure(self, dtd_files):
        for f in [self.work_area.dtd_report_filename, self.work_area.style_report_filename, self.work_area.data_report_filename, self.work_area.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)
        xml_filename = self.work_area.new_xml_filename

        xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, dtd_files, self.work_area.dtd_report_filename, self.work_area.style_report_filename)
        xml_f, xml_e, xml_w = valid_style

        if os.path.isfile(self.work_area.dtd_report_filename):
            separator = ''
            if os.path.isfile(self.work_area.err_filename):
                separator = '\n\n\n' + '.........\n\n\n'
            open(self.work_area.err_filename, 'a+').write(separator + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(self.work_area.dtd_report_filename, 'r').read())

        if xml is None:
            xml_f += 1
        if not valid_dtd:
            xml_f += 1
        if self.work_area.ctrl_filename is None:
            if xml_f + xml_e + xml_w == 0:
                os.unlink(self.work_area.style_report_filename)
        else:
            open(self.work_area.ctrl_filename, 'w').write('Finished')

        if os.path.isfile(self.work_area.dtd_report_filename):
            os.unlink(self.work_area.dtd_report_filename)
        report_content = ''
        for rep_file in [self.work_area.err_filename, self.work_area.dtd_report_filename, self.work_area.style_report_filename]:
            if os.path.isfile(rep_file):
                report_content += extract_report_core(fs_utils.read_file(rep_file))
                #if self.is_xml_generation is False:
                #    fs_utils.delete_file_or_folder(rep_file)
        return report_content

    def validate_xml_content(self, journal):
        if self.article.tree is None:
            sheet_data = None
            article_display_report = None
            article_validation_report = None
            content = validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to get data of ') + self.work_area.new_name + '.'
        else:
            article_validation = article_validations.ArticleContentValidation(journal, self.article, self.is_db_generation, False)
            sheet_data = article_reports.ArticleSheetData(article_validation)
            article_display_report = article_reports.ArticleDisplayReport(sheet_data, self.pkg_path, self.work_area.new_name)
            article_validation_report = article_reports.ArticleValidationReport(article_validation)

            content = []

            if self.is_xml_generation:
                content.append(article_display_report.issue_header)
                content.append(article_display_report.article_front)

                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.table_tables)

                content.append(article_display_report.article_body)
                content.append(article_display_report.article_back)

            else:
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.table_tables)
                content.append(sheet_data.files_and_href(self.pkg_path))

            content = html_reports.join_texts(content)

        return content

    def validate_journal_data(self, journal):
        items = []
        license_url = None
        if len(self.article.article_licenses) > 0:
            license_url = self.article.article_licenses.values()[0].get('href')
        items.append([_('NLM title'), self.article.journal_id_nlm_ta, journal.nlm_title, validation_status.STATUS_FATAL_ERROR])
        items.append([_('journal-id (publisher-id)'), self.article.journal_id_publisher_id, journal.acron, validation_status.STATUS_FATAL_ERROR])
        items.append([_('e-ISSN'), self.article.e_issn, journal.e_issn, validation_status.STATUS_FATAL_ERROR])
        items.append([_('print ISSN'), self.article.print_issn, journal.p_issn, validation_status.STATUS_FATAL_ERROR])
        items.append([_('publisher name'), self.article.publisher_name, journal.publisher_name, validation_status.STATUS_ERROR])
        items.append([_('license'), license_url, journal.license, validation_status.STATUS_ERROR])
        return evaluate_journal_data(items)

    def validate_issue_data(self, issue_models):
        return '' if issue_models is None else issue_models.validate_article_issue_data(self.article)

    def is_allowed_to_converter(self, pub_year, ref_count):
        doit = False
        score = (ref_count + 20)
        if self.xml_issue_data_validations_file.fatal_errors == 0:
            if pub_year is not None:
                if pub_year[0:4].isdigit():
                    if int(pub_year[0:4]) < (int(datetime.now().isoformat()[0:4]) - 1):
                        # doc anterior a dois anos atras
                        doit = True
            if doit is False:
                doit = True
                if self.MAX_FATAL_ERRORS is not None:
                    if self.xml_structure_validations_file.fatal_errors + self.xml_content_validations_file.fatal_errors > max_score(self.MAX_FATAL_ERRORS, score):
                        doit = False
                if self.MAX_ERRORS is not None:
                    if self.xml_structure_validations_file.errors + self.xml_content_validations_file.errors > max_score(self.MAX_ERRORS, score):
                        doit = False
                if self.MAX_WARNINGS is not None:
                    if self.xml_structure_validations_file.warnings + self.xml_content_validations_file.warnings > max_score(self.MAX_WARNINGS, score):
                        doit = False
        return doit

    def hide_and_show_block(self, report_id):
        blocks = []
        block_parent_id = report_id + self.work_area.new_name
        blocks.append((_('Structure Validations'), 'xmlrep', self.xml_structure_validations_file))
        blocks.append((_('Contents Validations'),  'datarep', self.xml_content_validations_file))
        if self.is_db_generation:
            blocks.append((_('Converter Validations'), 'xcrep', self.xml_issue_data_validations_file))
        _blocks = []
        for label, style, validations_file in blocks:
            if validations_file.total() > 0:
                _blocks.append(html_reports.HideAndShowBlockItem(block_parent_id, label, style + self.work_area.new_name, style, validations_file.message, validations_file.statistics_message()))
        return html_reports.HideAndShowBlock(block_parent_id, _blocks)

    @property
    def table_of_content(self):
        r = ''
        r += '<div>'
        #r += html_reports.tag('h7', self.work_area.xml_name)
        r += html_reports.tag('p', self.article.toc_section)
        r += html_reports.tag('p', self.article.article_type)
        #r += html_reports.tag('p', self.article.pages)
        r += html_reports.tag('p', self.article.doi)
        r += html_reports.tag('p', html_reports.tag('strong', self.article.title))
        r += html_reports.tag('p', html_reports.format_html_data({t.language: t.title for t in self.article.titles[1:]}))
        a = []
        for item in article.authors_list(self.article.article_contrib_items):
            a.append(html_reports.tag('span', item))
        r += html_reports.tag('p', '; '.join(a))
        r += '</div>'
        return r

    @property
    def data_with_lang(self):
        r = '<p>'
        r += '<ul>'
        for lang in sorted(self.article.title_abstract_kwd_languages):
            r += '<li>'

            label = html_reports.tag('smaller', attributes.LANGUAGES.get(lang, _('unknown')) + ' [' + lang + ']')

            items = [item.text for item in self.article.abstracts_by_lang.get(lang, [])]
            if len(items) > 0:
                r += html_reports.tag('p', label + ' ' + _('abstract'))
                r += html_reports.format_html_data(items)

            keywords = self.article.keywords_by_lang.get(lang, [])
            if keywords is not None:
                keywords = [kwd.text for kwd in keywords]
            if len(keywords) > 0:
                r += html_reports.tag('p', label + ' ' + _('keywords'))
                r += html_reports.format_html_data(keywords)
            r += '</li>'
        r += '</ul></p>'
        return r

    def validate(self, journal, issue_models, dtd_files):
        self.xml_journal_data_validations_file.message = self.validate_journal_data(journal)
        self.xml_issue_data_validations_file.message = self.validate_issue_data(issue_models)
        self.xml_structure_validations_file.message = self.validate_xml_structure(dtd_files)
        self.xml_content_validations_file.message = self.validate_xml_content(journal)
        if self.is_xml_generation:
            valresults = ValidationsFile(self.work_area.data_report_filename)
            stats = html_reports.statistics_display(valresults, False)
            title = [_('Data Quality Control'), self.work_area.new_name]
            valresults.message = stats + valresults.message


class ArticlesPackage(object):

    def __init__(self, pkg_path, articles):
        self.pkg_path = pkg_path
        self.xml_names = [name for name in os.listdir(self.pkg_path) if name.endswith('.xml')]
        self.articles = articles
        self._identify_journal()

    def _identify_journal(self):
        journals = [(a.journal_title, a.print_issn, a.e_issn, a.issue_label) for a in self.articles.values()]
        journals = list(set(journals))
        self.journal = article.Journal()
        if len(journals) > 0:
            self.journal.journal_title, self.journal.p_issn, self.journal.e_issn, self.issue_label = journals[0]

    def identify_issue_label(self, acron):
        self.journal.acron = str(acron)
        self.acron_issue_label = self.journal.acron + ' ' + str(self.issue_label)

    @property
    def xml_list(self):
        r = ''
        r += '<p>' + _('XML path') + ': ' + self.pkg_path + '</p>'
        r += '<p>' + _('Total of XML files') + ': ' + str(len(self.xml_names)) + '</p>'
        r += html_reports.format_list('', 'ol', self.xml_names)
        r = '<div class="xmllist">' + r + '</div>'
        return r


class ArticlesSetValidations(object):

    def __init__(self, pkg, articles_work_area, journal, dtd_files, is_xml_generation, is_db_generation, registered_articles=None, issue_models=None):
        self.pkg = pkg
        self.pkg_articles = pkg.articles
        self.registered_articles = registered_articles if registered_articles is not None else {}
        self.merged_articles = {} if self.registered_articles is None else self.registered_articles.copy()
        self.merged_articles.update(self.pkg_articles)
        self.articles_work_area = articles_work_area
        self.articles_validations = {}
        self.journal = journal
        self.issue_models = issue_models
        self.dtd_files = dtd_files
        self.is_xml_generation = is_xml_generation
        self.is_db_generation = is_db_generation
        self.updated_articles = {}

        self.ERROR_LEVEL_FOR_UNIQUE_VALUES = {'order': validation_status.STATUS_FATAL_ERROR, 'doi': validation_status.STATUS_FATAL_ERROR, 'elocation id': validation_status.STATUS_FATAL_ERROR, 'fpage-lpage-seq-elocation-id': validation_status.STATUS_ERROR}
        if not self.is_db_generation:
            self.ERROR_LEVEL_FOR_UNIQUE_VALUES['order'] = validation_status.STATUS_WARNING

        self.blocked_update = []
        self.xc_articles = {}
        self.exact_comparison = {}
        self.relaxed_comparison = {}
        self.allowed_to_update = {}
        self.allowed_to_update_status = {}

        self._validate_orders()
        self._check_articles_set_ared_allowed_to_update()

        self.EXPECTED_COMMON_VALUES_LABELS = ['journal-title', 'journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'issue label', 'issue pub date', 'license']
        self.REQUIRED_DATA = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        self.EXPECTED_UNIQUE_VALUE_LABELS = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']

        self.compile_references()

    def _validate_orders(self):
        # order change must be allowed only if authors and titles are the same
        self.changed_orders = {}
        order_items = {name: article.order for name, article in self.registered_articles.items()}

        for name, article in self.pkg_articles.items():
            if name in order_items.keys():
                if order_items[name] != article.order:
                    self.changed_orders[name] = (order_items[name], article.order)

        order_values = {}
        for name, order in order_items.items():
            if not order in order_values.keys():
                order_values[order] = []
            order_values[order].append(name)

        self.rejected_order_change = {}
        for order, names in order_values.items():
            if len(names) > 1:
                self.rejected_order_change[order] = names

    def _check_articles_set_ared_allowed_to_update(self):
        self.blocked_update = []
        for xml_name, article in self.pkg_articles.items():
            registered = self.registered_articles.get(xml_name)
            if registered is not None:
                self._check_article_is_allowed_to_update(article, registered)
                if not self.allowed_to_update[article.xml_name]:
                    self.blocked_update.append(xml_name)
                else:
                    # update
                    self.xc_articles[xml_name] = article
            else:
                # new
                self.xc_articles[xml_name] = article
        return len(self.blocked_update) == 0

    def _check_article_is_allowed_to_update(self, article, registered):
        exact_comparison, relaxed_comparison = check_title_and_authors_changes(article, registered)

        allowed_to_update = False
        if len(exact_comparison) == 0:
            # no changes
            allowed_to_update = True
            status = validation_status.STATUS_INFO
        elif len(relaxed_comparison) == 0:
            # acceptable changes
            allowed_to_update = True
            status = validation_status.STATUS_WARNING
        else:
            # many changes
            allowed_to_update = False
            status = validation_status.STATUS_FATAL_ERROR
        if allowed_to_update:
            if article.order != registered.order:
                # order change
                if article.order in self.rejected_order_change.keys():
                    # order change is rejected
                    allowed_to_update = False
                    status = validation_status.STATUS_FATAL_ERROR
        self.exact_comparison[article.xml_name] = exact_comparison
        self.relaxed_comparison[article.xml_name] = relaxed_comparison
        self.allowed_to_update[article.xml_name] = allowed_to_update
        self.allowed_to_update_status[article.xml_name] = status

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
                required_items[label] = values.values()
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
                    if ref.year is None:
                        self.missing_year.append([xml_name, ref.id])
                    else:
                        numbers = len([n for n in ref.year if n.isdigit()])
                        not_numbers = len(ref.year) - numbers
                        if not_numbers > numbers:
                            self.unusual_years.append([xml_name, ref.id, ref.year])

                    if ref.source is None:
                        self.missing_source.append([xml_name, ref.id])
                    else:
                        numbers = len([n for n in ref.source if n.isdigit()])
                        not_numbers = len(ref.source) - numbers
                        if not_numbers < numbers:
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
        t1 = html_reports.tag('h2', _('Journal data: XML files and registered data'))
        msg = '<sup>*</sup>'
        msg += html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('Journal data in the XML files must be consistent with {link}').format(link=html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv')), 'note')
        t2 = '' if self.is_db_generation else msg
        return t1 + t2

    def validate(self):
        for name, article in self.merged_articles.items():
            self.articles_validations[name] = ArticleValidations(article, self.articles_work_area[name], self.pkg.pkg_path, self.is_xml_generation, self.is_db_generation)
            self.articles_validations[name].validate(self.journal, self.issue_models, self.dtd_files)

        self.pkg_journal_validations = PackageValidationsResult()
        self.pkg_journal_validations.title = self.pkg_journal_validations_report_title

        self.pkg_reg_issue_validations = PackageValidationsResult()
        self.pkg_reg_issue_validations.title = html_reports.tag('h2', _('Checking issue data: XML files and registered data'))

        for name, item in self.articles_validations.items():
            self.pkg_journal_validations[name] = item.xml_journal_data_validations_file.validations
            self.pkg_reg_issue_validations[name] = item.xml_issue_data_validations_file.validations

        self.consistence_validations = ValidationsResult()
        self.consistence_validations.message = self.consistence_validations_report

        self.xc_pre_validations = ValidationsResult()
        self.xc_pre_validations.message = self.xc_pre_validations_report

    @property
    def xml_validations_fatal_errors(self):
        return sum([validations.xml_validations.fatal_errors for validations in self.articles_validations.values()])

    @property
    def detailed_report(self):
        labels = ['file', 'order', _('pages'), _('article'), 'aop pid/related', _('reports')]
        values = {}
        hide_and_show_block_items = {}

        for new_name, article in self.articles:
            hide_and_show_block_items[new_name] = self.articles_validations[new_name].hide_and_show_block('view-reports-')

            values[new_name] = []
            values[new_name].append(new_name)
            values[new_name].append(article.order)
            values[new_name].append(article.pages)

            values[new_name].append(self.articles_validations[new_name].table_of_content)
            values[new_name].append({'aop doi': article.previous_pid, 'related': [item.get('xml', '') for item in article.related_articles]})

        report = html_reports.HideAndShowBlocksReport(labels, values, hide_and_show_block_items, html_cell_content=[_('article')])
        return report.content

    @property
    def toc_extended_report(self):
        labels = ['file', _('article'), _('pages'), '+']
        values = {}
        hide_and_show_block_items = {}
        for new_name, article in self.articles:
            report_id = 'toc-'
            block_parent_id = report_id + new_name
            block_items = [html_reports.HideAndShowBlockItem(block_parent_id, '+', 'more-' + new_name, 'xmlrep', self.articles_validations[new_name].data_with_lang, '')]
            hide_and_show_block_items[new_name] = html_reports.HideAndShowBlock(block_parent_id, block_items)
            values[new_name] = []
            values[new_name].append(new_name)
            values[new_name].append(self.articles_validations[new_name].table_of_content)
            values[new_name].append(article.pages)
        report = html_reports.HideAndShowBlocksReport(labels, values, hide_and_show_block_items, html_cell_content=[_('article')])
        return report.content

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
        articles = [self.registered_articles.get('new_name'), self.pkg.articles.get('new_name'), self.updated_articles.get('new_name')]
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
        labels = ['file', _('article'), _('processing history')]
        values = {}
        hide_and_show_block_items = {}
        for new_name, article in self.articles:
            report_id = 'dbstatus-'
            block_parent_id = report_id + new_name
            block_items = [html_reports.HideAndShowBlockItem(block_parent_id, _('processing history'), 'db-hist-' + new_name, 'datarep', self.article_db_status_report(new_name), '')]
            hide_and_show_block_items[new_name] = html_reports.HideAndShowBlock(block_parent_id, block_items)
            values[new_name] = []
            values[new_name].append(new_name)
            values[new_name].append(self.articles_validations[new_name].table_of_content)
        report = html_reports.HideAndShowBlocksReport(labels, values, hide_and_show_block_items, html_cell_content=[_('article')])
        return report.content

    @property
    def alt_detailed_report(self):
        labels = ['file', 'order', 'pages', 'doi | aop pid | related', 'subject | @article-type', 'article-title', _('reports')]
        items = []

        for new_name, article in self.articles:

            links, block = self.articles_validations[new_name].block_reports

            values = []
            values.append(new_name)

            d = {}
            d['order'] = article.order
            values.append(d)

            d = {}
            d['fpage'] = article.fpage
            d['pages'] = article.pages
            d['elocation-id'] = article.elocation_id
            d['article-id (other)'] = article.article_id_other
            values.append(d)

            d = {}
            d['doi'] = article.doi
            d['previous pid'] = article.previous_pid
            d['related'] = [item.get('xml', '') for item in article.related_articles]
            values.append(d)

            d = {}
            d['subject'] = article.sorted_toc_sections
            d['article-type'] = article.article_type
            values.append(d)

            values.append(article.title)
            values.append(links)

            items.append(label_values(labels, values))
            items.append({'reports': block})

        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=['reports'])

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
        return html_reports.tag('h4', _('Articles Dates Report')) + html_reports.sheet(labels, items, 'dbstatus')

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
        labels = ['source', 'total']
        h = None
        if len(self.reftype_and_sources) > 0:
            h = ''
            for reftype, sources in self.reftype_and_sources.items():
                items = []
                h += html_reports.tag('h4', reftype)
                for source in sorted(sources.keys()):
                    items.append({'source': source, 'total': sources[source]})
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
                            status = validation_status.STATUS_FATAL_ERROR if not article.is_epub_only else validation_status.STATUS_WARNING
                            msg.append(_('Invalid pages') + ': ' + _('check lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name})').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage == int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}) are the same').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage + 1 < int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('there is a gap between lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name})').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                    if int_fpage > int_lpage:
                        status = validation_status.STATUS_FATAL_ERROR
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
            r += html_reports.tag('div', html_reports.p_message(_('{status}: invalid XML files.').format(status=validation_status.STATUS_FATAL_ERROR)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', self.invalid_xml_name_items, 'issue-problem'))
        return r

    @property
    def missing_items_report(self):
        r = ''
        for label, items in self.missing_required_values.items():
            r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_FATAL_ERROR, label=label)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
        return r

    @property
    def duplicated_values_report(self):
        parts = []
        for label, values in self.duplicated_values.items():
            status = self.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
            _m = _('{status}: unique value of {label} is required for all the documents in the package').format(status=status, label=label)
            parts.append(html_reports.p_message(_m))
            for value, xml_files in values.items():
                parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def conflicting_values_report(self):
        parts = []
        for label, values in self.conflicting_values.items():
            compl = ''
            _status = validation_status.STATUS_FATAL_ERROR
            if label == 'issue pub date':
                if self.is_rolling_pass:
                    _status = validation_status.STATUS_WARNING
            elif label == 'license':
                _status = validation_status.STATUS_WARNING
            _m = _('{status}: same value for {label} is required for all the documents in the package.').format(status=_status, label=label)
            parts.append(html_reports.p_message(_m))
            parts.append(html_reports.format_html_data(values))
        return ''.join(parts)

    @property
    def consistence_validations_report(self):
        text = []
        text += self.invalid_xml_report
        text += self.missing_items_report
        text += self.conflicting_values_report
        text += self.duplicated_values_report

        r = html_reports.tag('h2', _('Checking issue data consistence'))
        r += html_reports.tag('div', ''.join(text), 'issue-messages')
        r += self.pages_report
        return r

    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.journal_issue_header_report)
        report.append(self.pkg_journal_validations.report(errors_only=not self.is_xml_generation))
        report.append(self.pkg_reg_issue_validations.report(errors_only=not self.is_xml_generation))
        report.append(self.consistence_validations_report)
        report.append(self.xc_pre_validations_report)
        return ''.join(report)

    @property
    def blocking_errors(self):
        return self.consistence_validations.fatal_errors + self.pkg_reg_issue_validations.fatal_errors + self.xc_pre_validations.fatal_errors

    @property
    def xml_validations_fatal_errors(self):
        return sum([v.xml_structure_validations_file.fatal_errors + v.xml_content_validations_file.fatal_errors for v in self.articles_validations.values()])

    @property
    def xc_pre_validations_report(self):
        error_messages = []
        if self.rejected_order_changes_report + self.update_report != '':
            error_messages.append(html_reports.tag('h2', _('Order validations')))
            error_messages.append(self.rejected_order_changes_report)
            if self.update_report != '':
                error_messages.append(html_reports.tag('h3', _('Changes detected')))
                error_messages.append(self.update_report)
        return ''.join(error_messages)

    @property
    def rejected_order_changes_report(self):
        error_messages = []
        if len(self.rejected_order_change) > 0:
            error_messages.append(html_reports.tag('h3', _('rejected orders')))
            error_messages.append('<div class="issue-problem">')
            error_messages.append(html_reports.p_message(validation_status.STATUS_FATAL_ERROR + ': ' + _('It is not allowed to use same order for different articles.')))
            for order, items in self.rejected_order_change.items():
                error_messages.append(html_reports.tag('p', html_reports.format_html_data({order: items})))
            error_messages.append('</div>')
        return ''.join(error_messages)

    @property
    def update_report(self):
        all_msg = []
        for xml_name, article in self.articles:
            msg = []

            if xml_name in self.blocked_update:
                msg.append(html_reports.p_message(_('{status}: {item} is not allowed to be updated.').format(status=self.allowed_to_update_status[xml_name], item=xml_name)))

            order_change = self.changed_orders.get(xml_name)
            if order_change is not None:
                # order change
                if order_change[1] in self.rejected_order_change.keys():
                    # order change is rejected
                    msg.append(html_reports.p_message(_('{status}: {new_order} is being assign to more than one file: {files}').format(status=validation_status.STATUS_FATAL_ERROR, new_order=order_change[1], files=', '.join(self.rejected_order_change[order_change[1]]))))
                else:
                    # order change is acceptable
                    msg.append(html_reports.p_message(_('{status}: order changed: {old} => {new}').format(status=validation_status.STATUS_INFO, old=order_change[0], new=order_change[1])))

            if len(self.relaxed_comparison.get(xml_name, [])) > 0:
                msg.append(html_reports.p_message(_('{status}: {item} contains too many differences. It seems {item} in the package is very different from the one previously published.').format(status=self.allowed_to_update_status[xml_name], item=name)))
            if len(self.exact_comparison.get(xml_name, [])) > 0:
                msg.append(html_reports.tag('h5', _('Previously registered:')))
                for label, differences in self.exact_comparison.get(xml_name, []):
                    msg.append(html_reports.tag('p', differences[1]))
                msg.append(html_reports.tag('h5', _('Update:')))
                for label, differences in self.exact_comparison.get(xml_name, []):
                    msg.append(html_reports.tag('p', differences[0]))

            if len(msg) > 0:
                all_msg.append(html_reports.tag('h4', xml_name))
                all_msg.append('<div class="issue-problem">')
                all_msg.append(''.join(msg))
                all_msg.append('</div>')
        return ''.join(all_msg)


class ReportsMaker(object):

    def __init__(self, articles_set_validations, xpm_version=None, conversion_reports=None, display_report=False):
        self.display_report = display_report
        self.processing_result_location = None
        self.articles_set_validations = articles_set_validations
        self.conversion_reports = conversion_reports
        self.xpm_version = xpm_version
        self.tabs = ['pkg-files', 'toc-extended', 'summary-report', 'issue-report', 'individual-report', 'references', 'dates-report', 'aff-report', 'conversion-report', 'db-overview']
        self.labels = {
            'pkg-files': _('Files/Folders'),
            'summary-report': _('Summary'),
            'issue-report': 'journal/issue',
            'individual-report': _('XML Validations'),
            'conversion-report': _('Conversion'),
            'db-overview': _('Database'),
            'aff-report': _('Affiliations'),
            'dates-report': _('Dates'),
            'references': _('References'),
            'toc-extended': _('ToC'),
        }

    @property
    def report_components(self):
        components = {}
        components['pkg-files'] = self.articles_set_validations.pkg.xml_list
        if self.processing_result_location is not None:
            components['pkg-files'] += processing_result_location(self.processing_result_location)

        components['summary-report'] = ''
        components['individual-report'] = self.articles_set_validations.detailed_report
        components['aff-report'] = self.articles_set_validations.articles_affiliations_report
        components['dates-report'] = self.articles_set_validations.articles_dates_report
        components['references'] = self.articles_set_validations.references_overview_report
        components['references'] += self.articles_set_validations.sources_overview_report

        if not self.articles_set_validations.is_xml_generation:
            components['toc-extended'] = self.articles_set_validations.toc_extended_report
            components['issue-report'] = self.articles_set_validations.journal_and_issue_report

        if self.conversion_reports:
            if self.conversion_reports.issue_error_msg != '':
                components['issue-report'] = self.conversion_reports.issue_error_msg
            components['conversion-report'] = self.conversion_reports.xc_pre_validations_report
            components['db-overview'] = self.conversion_reports.db_status_report
            components['summary-report'] = self.conversion_reports.xc_conclusion_msg + self.conversion_reports.xc_results_report + self.conversion_reports.aop_results_report

        validations = ValidationsResult()
        validations.message = html_reports.join_texts(components.values())
        components['summary-report'] = error_msg_subtitle() + html_reports.statistics_display(validations, False) + components['summary-report']
        components = {k: label_errors(v) for k, v in components.items()}
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
    return [(xml_name, articles[xml_name]) for order, xml_name in l]


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


def check_title_and_authors_changes(article, registered):
    validations = []
    validations.append((article.textual_titles, registered.textual_titles))
    validations.append((article.textual_contrib_surnames, registered.textual_contrib_surnames))
    exact_comparison = [(label, items) for label, items in zip(labels, validations) if not items[0] == items[1]]
    relaxed_comparison = [(label, items) for label, items in zip(labels, validations) if not utils.is_similar(items[0], items[1])]
    return (exact_comparison, relaxed_comparison)


def error_msg_subtitle():
    msg = html_reports.tag('p', _('Fatal error - indicates errors which impact on the quality of the bibliometric indicators and other services'))
    msg += html_reports.tag('p', _('Error - indicates the other kinds of errors'))
    msg += html_reports.tag('p', _('Warning - indicates that something can be an error or something needs more attention'))
    return html_reports.tag('div', msg, 'subtitle')


def label_errors(content):
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


