# coding=utf-8

import os
import shutil

from __init__ import _
from . import attributes
from . import article_data_reports
from . import article_validations
from . import fs_utils
from . import html_reports
from . import validation_status
from . import xml_validator
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

        result = ValidationsResult()
        result.message = r
        return result


class XMLIssueDataValidator(object):

    def __init__(self, registered_issue_data):
        self.issue_error_msg = registered_issue_data.issue_error_msg
        self.issue_models = registered_issue_data.issue_models
        self.is_db_generation = registered_issue_data.articles_db_manager is not None

    def validate(self, article):
        r = ''
        if self.is_db_generation:
            if self.issue_error_msg is not None:
                r = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to identify {unidentified}. ').format(unidentified=_('issue'))
                r += self.issue_error_msg
            elif self.issue_models:
                r = self.issue_models.validate_article_issue_data(article)

        result = ValidationsResult()
        result.message = r
        return result


class XMLStructureValidator(object):

    def __init__(self, dtd_files):
        self.xml_validator = xml_validator.XMLValidator(dtd_files)

    def validate(self, outputs):
        separator = '\n\n\n' + '.........\n\n\n'

        name_error = ''
        if '_' in outputs.new_name or '.' in outputs.new_name:
            name_error = rst_title(_('Name errors')) + _('{value} has forbidden characters, which are {forbidden_characters}').format(value=outputs.new_name, forbidden_characters='_.') + separator

        files_errors = ''
        if os.path.isfile(outputs.err_filename):
            files_errors = fs_utils.read_file(outputs.err_filename)

        for f in [outputs.dtd_report_filename, outputs.style_report_filename, outputs.data_report_filename, outputs.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)
        #xml_filename = outputs.new_xml_filename
        xml, valid_dtd, valid_style = self.xml_validator.validate(outputs.new_xml_filename, outputs.dtd_report_filename, outputs.style_report_filename)
        xml_f, xml_e, xml_w = valid_style

        xml_structure_report_content = ''
        if os.path.isfile(outputs.dtd_report_filename):
            xml_structure_report_content = rst_title(_('DTD errors')) + fs_utils.read_file(outputs.dtd_report_filename)
            #os.unlink(outputs.dtd_report_filename)

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

        if xml_f > 0:
            fs_utils.append_file(outputs.err_filename, name_error + xml_structure_report_content)

        if outputs.ctrl_filename is None:
            if xml_f + xml_e + xml_w == 0:
                os.unlink(outputs.style_report_filename)
        else:
            fs_utils.write_file(outputs.ctrl_filename, 'Finished')

        for rep_file in [outputs.err_filename, outputs.style_report_filename]:
            if os.path.isfile(rep_file):
                report_content += extract_report_core(fs_utils.read_file(rep_file))

        r = ValidationsResult()
        r.message = report_content
        return r


class XMLContentValidator(object):

    def __init__(self, doi_services, pkgissuedata, registered_issue_data, package_path, is_xml_generation):
        self.registered_issue_data = registered_issue_data
        self.doi_services = doi_services
        self.package_path = package_path
        self.pkgissuedata = pkgissuedata
        self.is_xml_generation = is_xml_generation

    def validate(self, article, outputs):
        article_display_report = None
        article_validation_report = None

        if article.tree is None:
            content = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to get data from {item}. ').format(item=article.new_prefix)
        else:
            article_content_validation = article_validations.ArticleContentValidation(self.doi_services, self.pkgissuedata.journal, article, (self.registered_issue_data.articles_db_manager is not None), False)
            article_display_report = article_data_reports.ArticleDisplayReport(article_content_validation, self.package_path)
            article_validation_report = article_data_reports.ArticleValidationReport(article_content_validation)

            content = []

            if self.is_xml_generation:
                content.append(article_display_report.issue_header)
                content.append(article_display_report.article_front)
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.display_formulas)
                content.append(article_display_report.table_tables)
                r = open(outputs.images_report_filename).read()
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
                r = open(outputs.images_report_filename).read()
                r = r[r.find('<body'):]
                r = r[r.find('>')+1:]
                r = r[:r.find('</body>')]
                content.append(r)
                content.append(article_display_report.files_and_href())
            content = html_reports.join_texts(content)
        r = ValidationsResult()
        r.message = content
        return r, article_display_report


class ArticleValidator(object):

    def __init__(self, xml_journal_data_validator, xml_issue_data_validator, xml_structure_validator, xml_content_validator):
        self.xml_journal_data_validator = xml_journal_data_validator
        self.xml_issue_data_validator = xml_issue_data_validator
        self.xml_structure_validator = xml_structure_validator
        self.xml_content_validator = xml_content_validator

    def validate(self, article, outputs):
        artval = ArticleValidations()
        artval.journal_validations = self.xml_journal_data_validator.validate(article)
        artval.issue_validations = self.xml_issue_data_validator.validate(article)
        artval.xml_structure_validations = self.xml_structure_validator.validate(outputs)
        artval.xml_content_validations, artval.article_display_report = self.xml_content_validator.validate(article, outputs)
        if self.xml_content_validator.is_xml_generation:
            stats = artval.xml_content_validations.statistics_display(False)
            title = [_('Data Quality Control'), article.new_prefix]
            fs_utils.write_file(outputs.data_report_filename, html_reports.html(title, stats + artval.xml_content_validations.message))
        return artval


class ArticleValidations(object):

    def __init__(self):
        self.journal_validations = None
        self.issue_validations = None
        self.xml_structure_validations = None
        self.xml_content_validations = None

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in [self.xml_structure_validations, self.xml_content_validations]])

    def hide_and_show_block(self, report_id, new_name):
        blocks = []
        block_parent_id = report_id + new_name
        blocks.append((_('Structure Validations'), 'xmlrep', self.xml_structure_validations))
        blocks.append((_('Contents Validations'),  'datarep', self.xml_content_validations))
        if self.issue_validations:
            blocks.append((_('Converter Validations'), 'xcrep', self.issue_validations))
        _blocks = []
        for label, style, validations_file in blocks:
            if validations_file.total() > 0:
                status = validations_file.statistics_display()
                _blocks.append(html_reports.HideAndShowBlockItem(block_parent_id, label, style + new_name, style, validations_file.message, status))
        return html_reports.HideAndShowBlock(block_parent_id, _blocks)


class PackageReports(object):

    def __init__(self, package_folder, articles, workareas):
        self.package_folder = package_folder
        self.articles = articles
        self.workareas = workareas

    @property
    def xml_list(self):
        r = ''
        r += u'<p>{}: {}</p>'.format(_('XML path'), self.package_folder.path)
        r += u'<p>{}: {}</p>'.format(_('Total of XML files'), len(self.articles))

        files = ''
        for name, article in self.articles.items():
            files += '<li>{}</li>'.format(html_reports.format_list(name, 'ol', self.workareas[name].input_pkgfiles.files))
        r += '<ol>{}</ol>'.format(files)
        return u'<div class="xmllist">{}</div>'.format(r)

    @property
    def invalid_xml_name_items(self):
        return sorted([xml_name for xml_name, doc in self.articles.items() if doc.tree is None])

    @property
    def invalid_xml_report(self):
        r = ''
        if len(self.invalid_xml_name_items) > 0:
            r += html_reports.tag('div', html_reports.p_message(_('{status}: invalid XML files. ').format(status=validation_status.STATUS_BLOCKING_ERROR)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', self.invalid_xml_name_items, 'issue-problem'))
        return r

    @property
    def orphan_files_report(self):
        if len(self.package_folder.orphans) > 0:
            return '<div class="xmllist"><p>{}</p>{}</div>'.format(_('Invalid files names'), html_reports.format_list('', 'ol', self.package_folder.orphans))
        return ''


class PackageIssueData(object):

    def __init__(self, articles):
        self.articles = articles
        self.pkg_journal_title = None
        self.pkg_p_issn = None
        self.pkg_e_issn = None
        self.pkg_issue_label = None

        self.journal = None
        self.journal_data = None
        self._issue_label = None

    def setup(self):
        data = list(set([(a.journal_title, a.print_issn, a.e_issn, a.issue_label) for a in self.articles.values()]))
        data.sort(reverse=True)
        if len(data) > 0:
            data = list(data[0])
            if any(data):
                self.pkg_journal_title, self.pkg_p_issn, self.pkg_e_issn, self.pkg_issue_label = data

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


class RegisteredIssueData(object):

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.articles_db_manager = None
        self.issue_error_msg = None
        self.issue_models = None
        self.issue_files = None
        self.serial_path = None

    def get_data(self, pkgissuedata):
        if self.db_manager is None:
            journals_list = xc_models.JournalsList()
            pkgissuedata.journal = journals_list.get_journal(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
            pkgissuedata.journal_data = journals_list.get_journal_data(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
        else:
            acron_issue_label, self.issue_models, self.issue_error_msg, pkgissuedata.journal, pkgissuedata.journal_data = self.db_manager.get_registered_data(pkgissuedata.pkg_journal_title, pkgissuedata.pkg_issue_label, pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn)
            ign, pkgissuedata._issue_label = acron_issue_label.split(' ')
            if self.issue_error_msg is None:
                self.issue_files = self.db_manager.get_issue_files(self.issue_models)
                self.articles_db_manager = xc_models.ArticlesManager(self.db_manager.db_isis, self.issue_files)
                self.serial_path = self.db_manager.serial_path

    @property
    def registered_articles(self):
        articles = {}
        if self.articles_db_manager is not None:
            articles = registered_issue_data.articles_db_manager.registered_articles
        return articles


class ArticlesDataReports(object):

    def __init__(self, pkg_articles):
        self.pkg_articles = pkg_articles
        self.compile_references()

    @property
    def articles(self):
        l = sorted([(article.order, xml_name) for xml_name, article in self.pkg_articles.items()])
        l = [(xml_name, self.pkg_articles[xml_name]) for order, xml_name in l]
        return l

    @property
    def compiled_affiliations(self):
        evaluation = {}
        keys = [
            _('authors without aff'),
            _('authors with more than 1 affs'),
            _('authors with invalid xref[@ref-type=aff]'),
            _('incomplete affiliations')
            ]
        for k in keys:
            evaluation[k] = []

        for xml_name, doc in self.pkg_articles.items():
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

    def compile_references(self):
        self.sources_and_reftypes = {}
        self.reftype_and_sources = {}
        self.missing_source = []
        self.missing_year = []
        self.unusual_sources = []
        self.unusual_years = []
        self.years = {}
        for xml_name, doc in self.pkg_articles.items():
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


class MergedArticlesData(object):

    def __init__(self, merged_articles, is_db_generation):
        self.merged_articles = merged_articles
        self.ERROR_LEVEL_FOR_UNIQUE_VALUES = {'order': validation_status.STATUS_BLOCKING_ERROR, 'doi': validation_status.STATUS_BLOCKING_ERROR, 'elocation id': validation_status.STATUS_BLOCKING_ERROR, 'fpage-lpage-seq-elocation-id': validation_status.STATUS_ERROR}
        if not is_db_generation:
            self.ERROR_LEVEL_FOR_UNIQUE_VALUES['order'] = validation_status.STATUS_WARNING
        self.IGNORE_NONE = ['journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', ]
        self.EXPECTED_COMMON_VALUES_LABELS = ['journal-title', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'issue label', 'issue pub date', 'license']
        self.REQUIRED_DATA = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        self.EXPECTED_UNIQUE_VALUE_LABELS = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']

    @property
    def articles(self):
        l = sorted([(article.order, xml_name) for xml_name, article in self.merged_articles.items()])
        l = [(xml_name, self.merged_articles[xml_name]) for order, xml_name in l]
        return l

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
    def common_data(self):
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
    def missing_required_data(self):
        required_items = {}
        for label in self.REQUIRED_DATA:
            if label in self.common_data.keys():
                if None in self.common_data[label].keys():
                    required_items[label] = self.common_data[label][None]
        return required_items

    @property
    def conflicting_values(self):
        data = {}
        for label, values in self.common_data.items():
            if len(values) > 1:
                data[label] = values
        return data

    @property
    def duplicated_values(self):
        duplicated_labels = {}
        for label, values in self.unique_values.items():
            if len(values) > 0 and len(values) != len(self.articles):
                duplicated = {value: xml_files for value, xml_files in values.items() if len(xml_files) > 1}
                if len(duplicated) > 0:
                    duplicated_labels[label] = duplicated
        return duplicated_labels

    @property
    def unique_values(self):
        data = {}
        for label in self.EXPECTED_UNIQUE_VALUE_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]
                if value is not None:
                    if value not in values:
                        values[value] = []
                    values[value].append(xml_name)

            data[label] = values
        return data

    def orders_conflicts(self):
        orders = {}
        for name, article in self._merged_articles.items():
            if not article.order in orders.keys():
                orders[article.order] = []
            orders[article.order].append(name)
        return {order: names for order, names in orders.items() if len(names) > 1}


class MergedArticlesReports(object):

    def __init__(self, merged_articles_data, merging_result):
        self.merged_articles_data = merged_articles_data
        self.merging_result = merging_result

    @property
    def report_data_consistency(self):
        text = []
        text += self.report_missing_required_data
        text += self.report_conflicting_values
        text += self.report_duplicated_values
        text = html_reports.tag('div', ''.join(text), 'issue-messages')
        text += self.report_page_values
        return html_reports.tag('h2', _('Checking issue data consistency')) + text

    @property
    def report_missing_required_data(self):
        r = ''
        for label, items in self.merged_articles_data.missing_required_data.items():
            r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_BLOCKING_ERROR, label=label)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
        return r

    @property
    def report_conflicting_values(self):
        parts = []
        for label, values in self.merged_articles_data.conflicting_values.items():
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
    def report_duplicated_values(self):
        parts = []
        for label, values in self.merged_articles_data.duplicated_values.items():
            status = self.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
            _m = _('Unique value for {label} is required for all the documents in the package').format(label=label)
            parts.append(html_reports.p_message(status + ': ' + _m))
            for value, xml_files in values.items():
                parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def report_page_values(self):
        # FIXME separar validacao e relatório
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        error_level = validation_status.STATUS_BLOCKING_ERROR
        fpage_and_article_id_other_status = [all([a.fpage, a.lpage, a.article_id_other]) for xml_name, a in self.merged_articles_data.articles]
        if all(fpage_and_article_id_other_status):
            error_level = validation_status.STATUS_ERROR

        for xml_name, article in self.merged_articles_data.articles:
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

    def report_merging_conflicts(self):
        merging_errors = []
        if len(self.conflicts) > 0:
            merging_errors = [html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to update because the registered article data and the package article data do not match. '))]
            for name, conflicts in self.conflicts.items():
                labels = ['package']
                values = [name]
                for k, articles in conflicts.items():
                    labels.append(k)
                    if isinstance(articles, dict):
                        data = []
                        for article in articles.values():
                            data.append(article_data_reports.display_article_data_to_compare(article))
                        values.append(''.join(data))
                    else:
                        values.append(article_data_reports.display_article_data_to_compare(articles))
                merging_errors.append(html_reports.sheet(labels, [label_values(labels, values)], table_style='dbstatus', html_cell_content=labels))
        return ''.join(merging_errors)

    def display_order_conflicts(self):
        r = []
        if len(self.merged_articles_data.orders_conflicts) > 0:
            html_reports.tag('h2', _('Order conflicts'))
            for order, names in self.merged_articles_data.orders_conflicts.items():
                r.append(html_reports.tag('h3', order))
                r.append(html_reports.format_html_data(names))
        return ''.join(r)

    @property
    def validations(self):
        v = ValidationsResult()
        v.message = ''.join([self.display_order_conflicts() + self.report_merging_conflicts()])
        return v

    @property
    def report_names_changes(self):
        r = []
        if len(self.merging_result.name_changes) > 0:
            r.append(html_reports.tag('h3', _('Names changes')))
            for old, new in self.merging_result.name_changes.items():
                r.append(html_reports.tag('p', '{old} => {new}'.format(old=old, new=new), 'info'))
        return ''.join(r)

    @property
    def report_order_status(self):
        r = []
        if len(self.merging_result.order_changes) > 0:
            r.append(html_reports.tag('h3', _('Orders changes')))
            for name, changes in self.merging_result.order_changes.items():
                for change in changes:
                    r.append(html_reports.tag('p', '{name}: {old} => {new}'.format(name=name, old=change[0], new=change[1]), 'info'))
        if len(self.merging_result.excluded_orders) > 0:
            r.append(html_reports.tag('h3', _('Orders exclusions')))
            for name, order in self.merging_result.excluded_orders.items():
                r.append(html_reports.tag('p', '{order} ({name})'.format(name=name, order=order), 'info'))
        return ''.join(r)

    @property
    def changes_report(self):
        r = ''
        r += self.report_order_status
        r += self.report_names_changes
        if len(r) > 0:
            r = html_reports.tag('h2', _('Changes Report')) + r
        return r


class MergingResult(object):

    def __init__(self):
        self.exclusions = []
        self.conflicts = {}
        self.actions = {}
        self.name_changes = {}
        self.order_changes = {}
        self.excluded_orders = None


class ArticlesMerger(object):

    def __init__(self, registered_articles, articles):
        self._merged_articles = registered_articles.copy()
        self.registered_articles = RegisteredArticles(registered_articles)
        self.articles = articles
        self.merging_result = MergingResult()

    @property
    def merged_articles(self):
        return self._merged_articles

    def merge(self):
        self.analyze_pkg()
        self.update_articles()

    def analyze_pkg(self):
        for name, article in self.articles.items():
            action, old_name, conflicts = self.analyze_pkg_article(name, article)
            if conflicts is not None:
                self.merging_result.conflicts[name] = conflicts
            if action is not None:
                self.merging_result.actions[name] = action
            if action == 'update' and article.marked_to_delete:
                self.merging_result.exclusions.append(name)
            if old_name is not None:
                self.merging_result.name_changes[old_name] = name
            if name in self.registered_articles.keys():
                if article.order != self.registered_articles[name].order:
                    self.merging_result.order_changes[name] = (self.registered_articles[name].order, article.order)

    def analyze_pkg_article(self, name, pkg_article):
        registered_titaut, registered_name, registered_order = self.registered_articles.search_articles(name, pkg_article)
        action, old_name, conflicts = self.registered_articles.analyze_registered_articles(name, registered_titaut, registered_name, registered_order)
        return (action, old_name, conflicts)

    def update_articles(self):
        self.merging_result.history_items = {}
        # starts history with registered articles data
        self.merging_result.history_items = {name: [('registered article', article)] for name, article in self.registered_articles.items()}

        # exclude registered items
        for name in self.merging_result.exclusions:
            self.merging_result.history_items[name].append(('excluded article', self._merged_articles[name]))
            del self._merged_articles[name]

        # indicates package articles reception
        for name, article in self.articles.items():
            if not name in self.merging_result.history_items.keys():
                self.merging_result.history_items[name] = []
            self.merging_result.history_items[name].append(('package', article))

        # indicates names changes, and exclude old names
        for previous_name, name in self.merging_result.name_changes.items():
            self.merging_result.history_items[previous_name].append(('replaced by', self.articles[name]))

            self.merging_result.history_items[name].append(('replaces', self._merged_articles[previous_name]))
            del self._merged_articles[previous_name]

        # merge pkg and registered, considering some of them are rejected
        orders_to_check = []
        for name, article in self.articles.items():
            if not article.marked_to_delete:
                action = self.merging_result.actions.get(name)
                if name in self.merging_result.conflicts.keys():
                    action = 'reject'
                if not action in ['reject', None]:
                    self._merged_articles[name] = self.articles[name]

        self.merging_result.excluded_orders = self.excluded_orders

    @property
    def excluded_orders(self):
        #excluded_orders
        items = {}
        orders = [article.order for article in self.merged_articles.values()]
        for name, article in self.registered_articles.items():
            if not article.order in orders:
                items[name] = article.order
        return {name: article.order for name, article in self.registered_articles.items() if not article.order in orders}


class ArticlesValidator(object):

    def __init__(self, doi_services, dtd_files, registered_issue_data, pkgissuedata, package_path, is_xml_generation):
        self.registered_issue_data = registered_issue_data
        self.pkgissuedata = pkgissuedata
        self.package_path = package_path
        self.is_xml_generation = is_xml_generation
        self.is_db_generation = self.registered_issue_data.db_manager is not None

        xml_journal_data_validator = XMLJournalDataValidator(self.pkgissuedata.journal_data)
        xml_issue_data_validator = XMLIssueDataValidator(self.registered_issue_data)
        xml_structure_validator = XMLStructureValidator(dtd_files)
        xml_content_validator = XMLContentValidator(doi_services, self.pkgissuedata, self.registered_issue_data, self.package_path, self.is_xml_generation)
        self.article_validator = ArticleValidator(xml_journal_data_validator, xml_issue_data_validator, xml_structure_validator, xml_content_validator)

    def validate(self, articles, outputs):
        articles_validations_reports = ArticlesValidationsReports(self.is_xml_generation, self.is_db_generation)

        articles_merger = ArticlesMerger(self.registered_issue_data.registered_articles, articles)
        articles_merger.merge()
        merged_articles_data = MergedArticlesData(articles_merger.merged_articles, self.is_db_generation)
        articles_validations_reports.merged_articles_reports = MergedArticlesReports(merged_articles_data, articles_merger.merging_result)

        utils.display_message(_('Validate package ({n} files)').format(n=len(articles)))
        if len(self.registered_issue_data.registered_articles) > 0:
            utils.display_message(_('Previously registered: ({n} files)').format(n=len(self.registered_issue_data.registered_articles)))

        results = {}
        for name, article in articles.items():
            utils.display_message(_('Validate {name}').format(name=name))
            results[name] = self.article_validator.validate(article, outputs[name])

        articles_validations_reports.consistency_validations = ValidationsResult()
        articles_validations_reports.consistency_validations.message = articles_validations_reports.merged_articles_reports.report_data_consistency
        if self.registered_issue_data.issue_error_msg is not None:
            articles_validations_reports.consistency_validations.message = self.registered_issue_data.issue_error_msg + articles_validations_reports.consistency_validations.message

        articles_validations_reports.articles_validations = results

        return articles_validations_reports


class ArticlesValidationsReports(object):

    def __init__(self, is_xml_generation=False, is_db_generation=False):
        self.consistency_validations = None
        self.articles_validations = None
        self.is_xml_generation = is_xml_generation
        self.is_db_generation = is_db_generation
        self.merged_articles_reports = None

    @property
    def pkg_journal_validations(self):
        items = ValidationsResultItems()
        for name, validation in self.articles_validations.items():
            items[name] = validation.journal_validations
        signal = ''
        msg = ''
        if not self.is_db_generation:
            signal = '<sup>*</sup>'
            msg = html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('Journal data in the XML files must be consistent with {link}').format(link=html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv')), 'note')
        items.title = html_reports.tag('h2', _('Journal data: XML files and registered data') + signal) + msg
        return items

    @property
    def pkg_issue_validations(self):
        items = ValidationsResultItems()
        for name, validation in self.articles_validations.items():
            items[name] = validation.issue_validations
        items.title = html_reports.tag('h2', _('Checking issue data: XML files and registered data'))
        return items

    @property
    def detailed_report(self):
        labels = [_('filename'), 'order', _('article'), 'aop pid/related', _('reports')]
        widths = {}
        widths[_('filename')] = '10'
        widths['order'] = '5'
        widths[_('article')] = '60'
        widths['aop pid/related'] = '10'
        widths[_('reports')] = '10'
        items = []
        for new_name, validations in self.articles_validations.items():
            article = validations.article_display_report.article
            hide_and_show_block_items = validations.hide_and_show_block('view-reports-', new_name)
            values = []
            values.append(new_name)
            values.append(article.order)
            if validations.article_display_report is None:
                values.append('')
            else:
                values.append(validations.article_display_report.table_of_contents)
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
    def journal_issue_header_report(self):
        common_data = ''
        for label, values in self.merged_articles_reports.merged_articles_data.common_data.items():
            if len(values.keys()) == 1:
                common_data += html_reports.tag('p', html_reports.display_label_value(label, values.keys()[0]))
            else:
                common_data += html_reports.format_list(label + ':', 'ol', values.keys())
        return html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', common_data, 'issue-data')

    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.journal_issue_header_report)
        errors_only = not self.is_xml_generation
        report.append(self.pkg_journal_validations.report(errors_only))
        report.append(self.pkg_issue_validations.report(errors_only))
        if self.consistency_validations.total() > 0:
            report.append(self.consistency_validations.message)

        if self.merged_articles_reports.validations.total() > 0:
            report.append(html_reports.tag('h2', _('Data Conflicts Report')))
            report.append(self.merged_articles_reports.validations.message)
        return ''.join(report)

    @property
    def blocking_errors(self):
        return sum([self.consistency_validations.blocking_errors, self.pkg_issue_validations.blocking_errors, self.merged_articles_reports.validations.blocking_errors])

    @property
    def fatal_errors(self):
        return sum([v.fatal_errors for v in self.articles_validations.values()])


class ArticlesPackage(object):

    def __init__(self, pkg_path, pkg_articles, is_xml_generation):
        self.pkg_path = pkg_path
        self.pkg_articles = pkg_articles
        self.is_xml_generation = is_xml_generation
        self.xml_names = [name for name in os.listdir(self.pkg_path) if name.endswith('.xml')]


class ArticlesData(object):

    def __init__(self):
        self.pkg_journal_title = None
        self.pkg_p_issn = None
        self.pkg_e_issn = None
        self.pkg_issue_label = None


class RegisteredArticles(dict):

    def __init__(self, registered_articles):
        dict.__init__(self, registered_articles)

    def registered_item(self, name, article):
        found = None
        registered = self.get(name)
        if registered is not None:
            similar, status, msg = compare_articles(registered, article, _('registered'), _('package'))
            if registered.order == article.order and similar:
                found = registered
        return found

    def registered_order(self, order):
        return [reg_name for reg_name, reg in self.items() if reg.order == order]

    def registered_titles_and_authors(self, article):
        similar_items = []
        for name, registered in self.items():
            similar, status, message = compare_articles(registered, article, _('registered'), _('package'))
            if similar:
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
        return (actions, old_name, conflicts)


class ReportsMaker(object):

    def __init__(self, package_reports, articles_data_reports, articles_validations_reports, files_location, xpm_version=None, conversion=None):
        self.processing_result_location = None
        self.package_reports = package_reports
        self.articles_data_reports = articles_data_reports
        self.articles_validations_reports = articles_validations_reports
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
    def report_components(self):
        components = {}
        components['pkg-files'] = self.package_reports.xml_list
        if self.processing_result_location is not None:
            components['pkg-files'] += processing_result_location(self.processing_result_location)

        components['summary-report'] = self.package_reports.orphan_files_report + self.package_reports.invalid_xml_report
        components['group-validations-report'] = self.package_reports.orphan_files_report + self.package_reports.invalid_xml_report
        components['individual-validations-report'] = self.articles_validations_reports.detailed_report
        components['aff-report'] = self.articles_data_reports.articles_affiliations_report
        components['dates-report'] = self.articles_data_reports.articles_dates_report
        components['references'] = (self.articles_data_reports.references_overview_report +
            self.articles_data_reports.sources_overview_report)

        if not self.articles_validations_reports.is_xml_generation:
            components['group-validations-report'] += self.articles_validations_reports.journal_and_issue_report

        if self.conversion is None:
            components['website'] = toc_extended_report(self.package_reports.articles)
        else:
            components['website'] = self.conversion.conclusion_message + toc_extended_report(self.conversion.registered_articles)
            if self.articles_validations_reports.registered_issue_data.issue_error_msg is not None:
                components['group-validations-report'] += self.articles_validations_reports.registered_issue_data.issue_error_msg

            #components['xc-validations'] = self.conversion.conclusion_message + self.conversion.articles_merger.changes_report + self.conversion.conversion_status_report + self.conversion.aop_status_report + self.conversion.articles_conversion_validations.report(True) + self.conversion.conversion_report
            components['xc-validations'] = html_reports.tag('h3', _('Conversion Result')) + self.conversion.conclusion_message + self.conversion.articles_validations_reports.merged_articles_reports.changes_report + self.conversion.aop_status_report + self.conversion.articles_conversion_validations.report(True) + self.conversion.conversion_report

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
            for item in self.package_reports.package_folder.xml_names:
                shutil.copyfile(self.package_reports.package_folder.path + '/' + item, report_path + '/' + item)


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


def compare_articles(article1, article2, label1='article 1', label2='article 2'):
    labels = [_('titles'), _('authors'), _('body')]
    validations = []
    validations.append((article1.textual_titles, article2.textual_titles))
    validations.append((article1.textual_contrib_surnames, article2.textual_contrib_surnames))

    if not any([article1.textual_titles, article2.textual_titles, article1.textual_contrib_surnames, article2.textual_contrib_surnames]):
        if article1.body_words is not None and article2.body_words is not None:
            validations.append((article1.body_words[0:200], article2.body_words[0:200]))

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
    elif len(exact_comparison_result) == 1 or len(relaxed_comparison_result) == 1:
        valid_titles_and_authors = True
        status = validation_status.STATUS_WARNING
    message = display_articles_differences(status, exact_comparison_result, label1, label2)
    return (valid_titles_and_authors, status, message)


def display_articles_differences(status, comparison_result, label1='article 1', label2='article 2'):
    msg = []
    if len(comparison_result) > 0:
        for label, differences in comparison_result:
            msg.append(html_reports.p_message(status))
            msg.append(html_reports.tag('h5', label))
            msg.append(html_reports.display_label_value(label1, differences[0]))
            msg.append(html_reports.display_label_value(label2, differences[1]))
    return ''.join(msg)


def display_order_conflicts(orders_conflicts):
    r = []
    if len(orders_conflicts) > 0:
        html_reports.tag('h2', _('Order conflicts'))
        for order, names in orders_conflicts.items():
            r.append(html_reports.tag('h3', order))
            r.append(html_reports.format_html_data(names))
    return ''.join(r)


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
                values.append(article_data_reports.display_article_data_in_toc(article))
                items.append(label_values(labels, values))
        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=[_('article'), _('last update')], widths=widths)
