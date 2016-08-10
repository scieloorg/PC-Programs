import os

from __init__ import _
from . import article
from . import article_reports
from . import article_validations
from . import article_utils
from . import fs_utils
from . import html_reports
from . import validation_status
from . import xpchecker


class PackageValidationsResults(dict):

    def __init__(self, report_path, prefix, suffix):
        dict.__init__(self)
        self.report_path = report_path
        self.prefix = prefix
        self.suffix = suffix
        self.load()

    @property
    def total(self):
        return sum([item.total for item in self.values()])

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in self.values()])

    @property
    def errors(self):
        return sum([item.errors for item in self.values()])

    @property
    def warnings(self):
        return sum([item.warnings for item in self.values()])

    @property
    def report_content(self, title, errors_only=False):
        return title + self.report(errors_only) if self.total > 0 else ''

    def report(self, errors_only=False):
        _reports = ''
        if title is not None:
            _reports += title
        for xml_name, results in self.items():
            if results.total > 0 or errors_only is False:
                _reports += html_reports.tag('h4', xml_name)
                _reports += results.message
        return _reports

    def statistics_message(self):
        return '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(self.fatal_errors)), ('errors', str(self.errors)), ('warnings', str(self.warnings))]]) + ']'

    def save_reports(self):
        for xml_name, validations in self.items():
            validations.write_report(self.report_path + '/' + self.prefix + xml_name + self.suffix)

    def load(self, read_all=True):
        for item in os.listdir(self.report_path):
            valid = False
            xml_name = item
            if len(self.prefix) > 0:
                if item.startswith(self.prefix):
                    xml_name = xml_name[len(self.prefix):]
                    valid = True
            if len(self.suffix) > 0:
                if item.endswith(self.suffix):
                    xml_name = xml_name[0:-len(self.suffix)]
                    valid = True
            if valid is True:
                self[xml_name] = ValidationsResults('')
                self[xml_name].read_report(self.report_path + '/' + item)


class ValidationsResults(object):

    def __init__(self, message):
        self.fatal_errors, self.errors, self.warnings = html_reports.statistics_numbers(message)
        self.message = message

    @property
    def total(self):
        return sum([self.fatal_errors, self.errors, self.warnings])

    def statistics_message(self):
        return '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(self.fatal_errors)), ('errors', str(self.errors)), ('warnings', str(self.warnings))]]) + ']'

    def block_report(self, new_name, label, id):
        if self.total > 0:
            a_name = 'view-reports-' + new_name
            status = html_reports.statistics_display(self)
            links = html_reports.report_link(id + new_name, '[ ' + label + ' ]', id, a_name)
            links += html_reports.tag('span', status, 'smaller')
            block = html_reports.report_block(id + new_name, self.message, id, a_name)
        return (links, block)

    def write_report(self, report_filename):
        if self.message is not None:
            if len(self.message) > 0:
                fs_utils.write_file(report_filename, self.message)

    def read_report(self, report_filename):
        if os.path.isfile(report_filename):
            self.message = fs_utils.read_file(self.report_path + '/' + item)
            self.fatal_errors, self.errors, self.warnings = html_reports.statistics_numbers(self.message)


class ArticleValidations(object):

    def __init__(self, journal, article, doc_files_info, dtd_files, new_name, pkg_path, is_xml_generation, is_db_generation):
        self.new_name = new_name
        self.article = article
        self.doc_files_info = doc_files_info
        self.dtd_files = dtd_files
        self.pkg_path = pkg_path
        self.journal = journal
        self.is_xml_generation = is_xml_generation
        self.is_db_generation = is_db_generation

    @property
    def xml_structure_validations(self):
        for f in [self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename, self.doc_files_info.data_report_filename, self.doc_files_info.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)
        xml_filename = self.doc_files_info.new_xml_filename

        xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, self.dtd_files, self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename)
        xml_f, xml_e, xml_w = valid_style

        if os.path.isfile(self.doc_files_info.dtd_report_filename):
            separator = ''
            if os.path.isfile(self.doc_files_info.err_filename):
                separator = '\n\n\n' + '.........\n\n\n'
            open(self.doc_files_info.err_filename, 'a+').write(separator + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(self.doc_files_info.dtd_report_filename, 'r').read())

        if xml is None:
            xml_f += 1
        if not valid_dtd:
            xml_f += 1
        if self.doc_files_info.ctrl_filename is None:
            if xml_f + xml_e + xml_w == 0:
                os.unlink(self.doc_files_info.style_report_filename)
        else:
            open(self.doc_files_info.ctrl_filename, 'w').write('Finished')

        if os.path.isfile(self.doc_files_info.dtd_report_filename):
            os.unlink(self.doc_files_info.dtd_report_filename)

        report_content = ''
        for rep_file in [self.doc_files_info.err_filename, self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename]:
            if os.path.isfile(rep_file):
                report_content += extract_report_core(fs_utils.read_file(rep_file))
                #if self.is_xml_generation is False:
                #    fs_utils.delete_file_or_folder(rep_file)
        return ValidationsResults(report_content)

    @property
    def xml_structure_block_report(self):
        return self.xml_structure_validations.block_report(self.new_name, _('Structure Validations'), 'xmlrep')

    @property
    def xml_content_block_report(self):
        return self.xml_content_validations.block_report(self.new_name, _('Contents Validations'), 'datarep')

    @property
    def xml_content_validations(self):
        if self.article.tree is None:
            sheet_data = None
            article_display_report = None
            article_validation_report = None
            content = validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to get data of ') + self.new_name + '.'
        else:
            article_validation = article_validations.ArticleContentValidation(self.journal, self.article, self.is_db_generation, False)
            sheet_data = article_reports.ArticleSheetData(article_validation)
            article_display_report = article_reports.ArticleDisplayReport(sheet_data, self.pkg_path, self.new_name)
            article_validation_report = article_reports.ArticleValidationReport(article_validation)

            content = []

            img_report_content = ''
            if os.path.isfile(self.doc_files_info.images_report_filename):
                img_report_content = fs_utils.read_file(self.doc_files_info.images_report_filename)
            if len(img_report_content) > 0:
                content.append(html_reports.tag('h1', _('ATTENTION'), 'warning'))
                content.append(html_reports.tag('h1', _('New report: Images Report at the bottom'), 'warning'))

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

            if len(img_report_content) > 0:
                content.append(img_report_content)

            content = html_reports.join_texts(content)
        data_validations = ValidationsResults(content)
        if self.is_xml_generation:
            stats = html_reports.statistics_display(data_validations, False)
            title = [_('Data Quality Control'), self.new_name]
            fs_utils.write_file(self.doc_files_info.data_report_filename, html_reports.html(title, stats + content))
        return data_validations

    @property
    def journal_data_validations(self):
        items = []
        license_url = None
        if len(self.article.article_licenses) > 0:
            license_url = self.article.article_licenses.values()[0].get('href')
        items.append([_('NLM title'), self.article.journal_id_nlm_ta, self.journal.nlm_title, validation_status.STATUS_FATAL_ERROR])
        items.append([_('journal-id (publisher-id)'), self.article.journal_id_publisher_id, self.journal.acron, validation_status.STATUS_FATAL_ERROR])
        items.append([_('e-ISSN'), self.article.e_issn, self.journal.e_issn, validation_status.STATUS_FATAL_ERROR])
        items.append([_('print ISSN'), self.article.print_issn, self.journal.p_issn, validation_status.STATUS_FATAL_ERROR])
        items.append([_('publisher name'), self.article.publisher_name, self.journal.publisher_name, validation_status.STATUS_ERROR])
        items.append([_('license'), license_url, self.journal.license, validation_status.STATUS_ERROR])
        return ValidationsResults(evaluate_journal_data(items))

    def registered_issue_data_validations(self, issue_models):
        issue_validations_msg = issue_models.validate_article_issue_data(self.article)
        return ValidationsResults(issue_validations_msg)

    @property
    def block_reports(self):
        a_name = 'view-reports-' + self.new_name
        links = '<a name="' + a_name + '"/>'
        status = ''
        block = ''

        _link, _block = self.xml_structure_validations.block_report(self.new_name, _('Structure Validations'), 'xmlrep')
        links += _link
        block += _block

        _link, _block = self.xml_content_validations.block_report(self.new_name, _('Contents Validations'), 'datarep')
        links += _link
        block += _block

        if self.is_db_generation:
            _link, _block = self.registered_issue_data_validations.block_report(self.new_name, _('Converter Validations'), 'xcrep')
            links += _link
            block += _block
        return (links, block)


class PkgArticles(object):

    def __init__(self, pkg_path, articles):
        self.pkg_path = pkg_path
        self.xml_names = [name for name in os.listdir(self.pkg_path) if name.endswith('.xml')]
        self.articles = articles
        self._issue_identification()

    def _issue_identification(self):
        journals = [[a.journal_title, a.print_issn, a.e_issn, a.issue_label] for a in self.articles.values()]
        journals = list(set(journals))
        self.journal = article.Journal()
        if len(journals) > 0:
            self.journal.journal_title, self.journal.p_issn, self.journal.e_issn, self.issue_label = journals[0]

    @property
    def xml_list(self):
        r = ''
        r += '<p>' + _('XML path') + ': ' + self.pkg_path + '</p>'
        r += '<p>' + _('Total of XML files') + ': ' + str(len(self.xml_names)) + '</p>'
        r += html_reports.format_list('', 'ol', self.xml_names)
        return '<div class="xmllist">' + r + '</div>'


class IssueItemsValidations(object):

    def __init__(self, pkg_path, articles, doc_files_info_items, new_names, dtd_files, is_xml_generation, is_db_generation, xpm_version=None):
        self.articles = articles
        self.xpm_version = xpm_version
        self.is_xml_generation = is_xml_generation
        self.is_db_generation = is_db_generation

        self.invalid_xml_name_items = []

        self.EXPECTED_EQUAL_VALUES_LABELS = ['journal-title', 'journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'issue label', 'issue pub date', 'license']
        self.EXPECTED_UNIQUE_VALUE_LABELS = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']
        self.REQUIRED_DATA = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        self.CHECKLIST_LABELS = ['journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'license']

        self.validate_journal_and_issue_data()

        self.pkg_path = pkg_path
        self.xml_filenames = sorted([self.pkg_path + '/' + name for name in os.listdir(self.pkg_path) if name.endswith('.xml')])

        self.articles = articles
        self.doc_files_info_items = doc_files_info_items
        self.new_names = new_names

        self.compile_references()

    @property
    def xml_name_sorted_by_order(self):
        l = sorted([(order, xml_name) for xml_name, article in self.articles.items()])
        return [xml_name for order, xml_name in l]

    def compile_references(self):
        self.sources_and_reftypes = {}
        self.reftype_and_sources = {}
        self.missing_source = []
        self.missing_year = []
        self.unusual_sources = []
        self.unusual_years = []
        for xml_name, doc in self.articles.items():
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
    def journal_and_issue_expected_equal_items(self):
        return {label: self.articles_data_set.journal_and_issue_data[label].keys() for label in self.EXPECTED_EQUAL_VALUES_LABELS}

    @property
    def journal_and_issue_expected_unique_items(self):
        return {label: self.articles_data_set.journal_and_issue_data[label].keys() for label in self.EXPECTED_UNIQUE_VALUE_LABELSs}

    @property
    def registered_issue_data_validations(self):
        r = PackageValidationsResults(self.report_path, 'issue-', '')
        for xml_name, article_validations in self.articles_validations.items():
            r[xml_name] = articles_validations.registered_issue_data_validations(self.issue_models)
        return r

    def xml_structure_validations(self):
        r = PackageValidationsResults(self.report_path, 'xmlstr-', '')
        for xml_name, article_validations in self.articles_validations.items():
            r[xml_name] = articles_validations.xml_structure_validations
        return r

    def xml_content_validations(self):
        r = PackageValidationsResults(self.report_path, 'xmlcon-', '')
        for xml_name, article_validations in self.articles_validations.items():
            r[xml_name] = articles_validations.xml_content_validations
        return r

    @property
    def xml_files_with_duplicated_values(self):
        duplicated_labels = {}
        for label, values in self.journal_and_issue_expected_unique_items.items():
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

        for xml_name, doc in self.articles.items():
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
    def blocking_errors(self):
        return self.registered_issue_data_validations.fatal_errors + self.journal_and_issue_consistences_validations.fatal_errors

    def validate_journal_and_issue_data(self):
        self.pkg_missing_items = {}
        self.journal_and_issue_data = {}
        labels = self.EXPECTED_EQUAL_VALUES_LABELS + self.EXPECTED_UNIQUE_VALUE_LABELS
        for xml_name, article in self.articles.items():
            if article.tree is None:
                self.invalid_xml_name_items.append(xml_name)
            else:
                art_data = article.summary()
                for label in labels:
                    if art_data[label] is None:
                        if label in self.REQUIRED_DATA:
                            if not label in self.pkg_missing_items.keys():
                                self.pkg_missing_items[label] = []
                            self.pkg_missing_items[label].append(xml_name)
                    else:
                        if not label in self.journal_and_issue_data.keys():
                            self.journal_and_issue_data[label] = {}
                        if not art_data[label] in self.journal_and_issue_data[label].keys():
                            self.journal_and_issue_data[label][art_data[label]] = []
                        self.journal_and_issue_data[label][art_data[label]].append(xml_name)

    @property
    def articles_validations(self):
        return {name: ArticleValidations(self.journal, a, self.doc_files_info_items[name], self.dtd_files, self.pkg_path, self.new_names[name], self.is_xml_generation, self.is_db_generation) for name, a in self.articles.items()}


    @property
    def articles_dates_report(self):
        labels = ['name', '@article-type', 
        'received', 'accepted', 'receive to accepted (days)', 'article date', 'issue date', 'accepted to publication (days)', 'accepted to today (days)']
        items = []
        for xml_name, doc in self.articles.items():
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
        r += html_reports.tag('h4', _('Affiliations Report'))
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
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        for new_name in self.xml_name_sorted_by_order:
            #if article.is_rolling_pass or article.is_ahead:
            #else:
            article = self.articles.get(new_name)
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
    def journal_validations_report(self):
        r = ''
        if self.journal_validations is not None:
            t1 = html_reports.tag('h2', _('Journal data: XML files and registered data') + '<sup>*</sup>')
            t2 = html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('Journal data in the XML files must be consistent with {link}').format(link=html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'), 'note'))
            r = self.journal_validations.report_content(t1 + t2, True)
        return r

    @property
    def journal_issue_header_report(self):
        issue_common_data = ''
        for label, values in self.journal_and_issue_expected_equal_items.items():
            message = ''
            if len(values) == 1:
                issue_common_data += html_reports.tag('p', values[0])
            else:
                issue_common_data += html_reports.format_list(label + ':', 'ol', values)
        return html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', issue_common_data, 'issue-data')

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
        for label, items in self.pkg_missing_items.items():
            r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_FATAL_ERROR, label=label)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
        return r

    @property
    def conflicting_values_report(self):
        parts = []
        status = {'issue pub date rolling pass': validation_status.STATUS_WARNING, 'license': validation_status.STATUS_WARNING}
        for label, values in self.journal_and_issue_expected_equal_items.items():
            if len(values) > 1:
                compl = ''
                if label == 'issue pub date':
                    if self.is_rolling_pass:
                        compl += ' rolling pass'
                _status = status.get(label, validation_status.STATUS_FATAL_ERROR)
                _m = _('{status}: same value for {label} is required for all the documents in the package.').format(status=status, label=label)
                parts.append(html_reports.p_message(_m))
                for found_value, xml_files in values.items():
                    parts.append(html_reports.format_list(_('found {label}="{xml}" in: ').format(label=label, xml=html_reports.display_xml(found_value)), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def duplicated_values_report(self):
        parts = []
        for label, values in self.xml_files_with_duplicated_values.items():
            status = self.error_level_for_unique[label]
            _m = _('{status}: unique value of {label} is required for all the documents in the package').format(status=status, label=label)
            part.append(html_reports.p_message(_m))
            for value, xml_files in values.items():
                parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def journal_and_issue_consistences_validations(self):
        r = ''
        r += self.invalid_xml_report
        r += self.missing_items_report
        r += self.conflicting_values_report
        r += self.duplicated_values_report
        toc_report = html_reports.tag('h2', _('Checking issue data consistence')) + html_reports.tag('div', r, 'issue-messages') + self.pages_report
        return ValidationsResults(toc_report)

    @property
    def issue_report(self):
        report = []
        report.append(self.journal_issue_header_report)
        report.append(self.journal_validations_report)

        items = [self.xc_validations, self.journal_and_issue_consistences_validations]
        for item in items:
            if item is not None:
                if item.total > 0:
                    report.append(item.message)

        if self.is_db_generation:
            if self.registered_issue_data_validations is not None:
                t = html_reports.tag('h2', _('Checking issue data: XML files and registered data'))
                report.append(self.registered_issue_data_validations.report_content(t, True))
        return ''.join(report) if len(report) > 0 else None


class ReportsMaker(object):

    def __init__(self, pkg_articles, issue_items_validations):
        self.pkg_articles = pkg_articles
        self.issue_items_validations = issue_items_validations
        self.tabs = ['pkg-files', 'summary-report', 'issue-report', 'detail-report', 'conversion-report', 'pkg_overview', 'db-overview', 'issue-not-registered', 'toc', 'references']
        self.labels = {
            'issue-report': 'journal/issue',
            'summary-report': _('Summary report'), 
            'detail-report': _('XML Validations report'), 
            'conversion-report': _('Conversion report'),
            'pkg-files': _('Files/Folders'),
            'db-overview': _('Database'),
            'pkg_overview': _('Package overview'),
            'references': _('Sources')
        }
        self.generate_components()

    def generate_components(self):
        self.components = {}
        self.components['pkg-files'] = self.pkg_articles.xml_list

        self.components['pkg_overview'] = self.issue_items_validations.overview_report
        self.components['references'] = self.issue_items_validations.references_overview_report
        self.components['references'] += self.issue_items_validations.sources_overview_report

        if not self.issue_items_validations.is_xml_generation:
            self.components['issue-report'] = self.issue_items_validations.issue_report

            self.components['detail-report'] = self.issue_items_validations.detail_report
            self.components['pkg-files'] += processing_result_location(os.path.dirname(self.issue_items_validations.pkg_path))

    def save_report(self, report_filename='xml_package_maker.html', report_title=_('XML Package Maker Report')):
        if not self.issue_items_validations.is_xml_generation:

            filename = report_path + '/' + report_filename
            if os.path.isfile(filename):
                bkp_filename = report_path + '/' + report_filename + '-'.join(utils.now()) + '.html'
                shutil.copyfile(filename, bkp_filename)

            #    def save_report(filename, title, content, xpm_version=None):
            html_reports.save(filename, report_title, self.content_report)

            print(_('Report:\n  {filename}').format(filename)

    @property
    def content_report(self):
        validations = ValidationsResults(html_reports.join_texts(self.components.values()))

        pre_selected = 'summary-report'
        self.components['summary-report'] = error_msg_subtitle() + html_reports.statistics_display(validations, False) + self.components['summary-report']

        # tabs
        content = html_reports.tabs_items([(tab_id, labels[tab_id]) for tab_id in self.tabs if self.components.get(tab_id) is not None], pre_selected)
        # tabs content
        for tab_id in self.tabs:
            c = self.components.get(tab_id)
            if c is not None:
                style = 'selected-tab-content' if tab_id == pre_selected else 'not-selected-tab-content'
                content += html_reports.tab_block(tab_id, c, style)

        content += html_reports.tag('p', _('finished'))
        if self.issue_items_validations.xpm_version is not None:
            content += html_reports.tag('p', _('report generated by XPM ') + self.issue_items_validations.xpm_version)

        return label_errors(content)

    def detail_report(self):
        labels = ['file', 'order/pages/elocation-id', 'doi/aop pid/related', 'subject/@article-type', 'article-title', _('reports')]
        items = []

        n = '/' + str(len(self.articles_set.articles))
        index = 0

        validations_text = ''

        #utils.debugging(self.pkg_stats)
        #utils.debugging(self.articles_set.xml_name_sorted_by_order)
        utils.display_message('\n')
        utils.display_message(_('Generating Detail report'))
        for new_name in self.articles_set.xml_name_sorted_by_order:
            index += 1
            item_label = str(index) + n + ': ' + new_name
            utils.display_message(item_label)

            links, block = self.issue_items_validations.articles_validations[new_name].block_reports

            values = []
            values.append(new_name)

            d = {}
            d['order'] = self.issue_items_validations.articles[new_name].order
            d['pages'] = self.issue_items_validations.articles[new_name].fpage
            d['elocation-id'] = self.issue_items_validations.articles[new_name].pages
            values.append(d)

            d = {}
            d['doi'] = self.issue_items_validations.articles[new_name].doi
            d['doi aop'] = self.issue_items_validations.articles[new_name].previous_pid
            d['related'] = self.issue_items_validations.articles[new_name].related_articles
            values.append(d)

            d = {}
            d['subject'] = self.issue_items_validations.articles[new_name].sorted_toc_sections
            d['article-type'] = self.issue_items_validations.articles[new_name].article_type
            values.append(d)

            values.append(self.issue_items_validations.articles[new_name].title)
            values.append(links)

            items.append(label_values(labels, values))
            items.append({'reports': block})

        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=['reports'])


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
