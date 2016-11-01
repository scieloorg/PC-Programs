# coding=utf-8

import sys
import os
from datetime import datetime

from __init__ import _
import validation_status
import attributes
import article_reports
import article_utils
import xpchecker
import html_reports
import utils
import fs_utils


log_items = []


class PackageValidationsResults(object):

    def __init__(self, report_path, prefix, suffix):
        self.validations_results_items = {}
        self.report_path = report_path
        self.prefix = prefix
        self.suffix = suffix
        self.read_reports()

    def item(self, name):
        if self.validations_results_items is not None:
            return self.validations_results_items.get(name)

    def add(self, name, validations_results):
        self.validations_results_items[name] = validations_results

    @property
    def total(self):
        return sum([item.total for item in self.validations_results_items.values()])

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in self.validations_results_items.values()])

    @property
    def errors(self):
        return sum([item.errors for item in self.validations_results_items.values()])

    @property
    def warnings(self):
        return sum([item.warnings for item in self.validations_results_items.values()])

    def report(self, errors_only=False):
        _reports = ''
        if self.validations_results_items is not None:
            for xml_name, results in self.validations_results_items.items():
                if results.total > 0 or errors_only is False:
                    _reports += html_reports.tag('h4', xml_name)
                    _reports += results.message
        return _reports

    def statistics_message(self):
        return '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(self.fatal_errors)), ('errors', str(self.errors)), ('warnings', str(self.warnings))]]) + ']'

    def save_reports(self):
        for xml_name, validations in self.validations_results_items.items():
            if validations.message is not None:
                if len(validations.message) > 0:
                    fs_utils.write_file(self.report_path + '/' + self.prefix + xml_name + self.suffix, validations.message)

    def read_reports(self, read_all=True):
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
                if os.path.isfile(self.report_path + '/' + item):
                    message = fs_utils.read_file(self.report_path + '/' + item)
                    if len(message) > 0:
                        if read_all is True or self.validations_results_items.get(xml_name) is None:
                            self.validations_results_items[xml_name] = ValidationsResults(message)


class ValidationsResults(object):

    def __init__(self, message):
        self.fatal_errors, self.errors, self.warnings = html_reports.statistics_numbers(message)
        self.message = message

    @property
    def total(self):
        return sum([self.fatal_errors, self.errors, self.warnings])

    def statistics_message(self):
        return '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(self.fatal_errors)), ('errors', str(self.errors)), ('warnings', str(self.warnings))]]) + ']'


class PkgArticles(object):

    def __init__(self, articles, pkg_path):
        self.articles = articles
        self.pkg_path = pkg_path
        self._xml_name_sorted_by_order = None
        self._compiled_pkg_metadata = None
        self.reftype_and_sources = None
        self.issue_files = None
        self.issue_models = None

        self.journal_check_list_labels = ['journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'license']
        self.expected_equal_values = ['journal-title', 'journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'issue label', 'issue pub date', 'license']
        self.expected_unique_value = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']
        self.required_journal_data = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]

    def xml_list(self, xml_filenames=None):
        r = ''
        r += '<p>' + _('XML path') + ': ' + self.pkg_path + '</p>'
        if xml_filenames is None:
            xml_filenames = [self.pkg_path + '/' + name for name in os.listdir(self.pkg_path) if name.endswith('.xml')]
        r += '<p>' + _('Total of XML files') + ': ' + str(len(xml_filenames)) + '</p>'
        r += html_reports.format_list('', 'ol', [os.path.basename(f) for f in xml_filenames])
        return '<div class="xmllist">' + r + '</div>'

    @property
    def xml_name_sorted_by_order(self):
        if self._xml_name_sorted_by_order is None:
            self._xml_name_sorted_by_order = self.sort_xml_name_by_order()
        return self._xml_name_sorted_by_order

    def sort_xml_name_by_order(self):
        order_and_xml_name_items = {}
        for xml_name, doc in self.articles.items():
            _order = str(doc.order)
            if not _order in order_and_xml_name_items.keys():
                order_and_xml_name_items[_order] = []
            order_and_xml_name_items[_order].append(xml_name)

        sorted_items = []
        for order in sorted(order_and_xml_name_items.keys()):
            for item in order_and_xml_name_items[order]:
                sorted_items.append(item)
        return sorted_items

    @property
    def is_processed_in_batches(self):
        return any([self.is_aop_issue, self.is_rolling_pass])

    @property
    def is_aop_issue(self):
        return any([a.is_ahead for a in self.articles.values()])

    @property
    def is_rolling_pass(self):
        _is_rolling_pass = False
        if not self.is_aop_issue:
            epub_dates = list(set([a.epub_dateiso for a in self.articles.values() if a.epub_dateiso is not None]))
            epub_ppub_dates = [a.epub_ppub_dateiso for a in self.articles.values() if a.epub_ppub_dateiso is not None]
            collection_dates = [a.collection_dateiso for a in self.articles.values() if a.collection_dateiso is not None]
            other_dates = list(set(epub_ppub_dates + collection_dates))
            if len(epub_dates) > 0:
                if len(other_dates) == 0:
                    _is_rolling_pass = True
                elif len(other_dates) > 1:
                    _is_rolling_pass = True
                elif len([None for a in self.articles.values() if a.collection_dateiso is None]) > 0:
                    _is_rolling_pass = True
        return _is_rolling_pass

    @property
    def compiled_pkg_metadata(self):
        if self._compiled_pkg_metadata is None:
            self.compile_pkg_metadata()
        return self._compiled_pkg_metadata

    def compile_pkg_metadata(self):
        self.invalid_xml_name_items = []
        self._compiled_pkg_metadata = {label: {} for label in self.expected_equal_values + self.expected_unique_value + ['license']}
        self.pkg_missing_items = {}
        labels = self.expected_equal_values + self.expected_unique_value
        for xml_name, article in self.articles.items():
            if article.tree is None:
                self.invalid_xml_name_items.append(xml_name)
            else:
                art_data = article.summary()
                for label in labels:
                    if art_data[label] is None:
                        if label in self.required_journal_data:
                            if not label in self.pkg_missing_items.keys():
                                self.pkg_missing_items[label] = []
                            self.pkg_missing_items[label].append(xml_name)
                    else:
                        self._compiled_pkg_metadata[label] = article_utils.add_new_value_to_index(self._compiled_pkg_metadata[label], art_data[label], xml_name)

    @property
    def pkg_journal_title(self):
        if self._compiled_pkg_metadata is None:
            self.compile_pkg_metadata()
        return more_frequent(self._compiled_pkg_metadata['journal-title'])

    @property
    def pkg_issue_label(self):
        if self._compiled_pkg_metadata is None:
            self.compile_pkg_metadata()
        return more_frequent(self._compiled_pkg_metadata.get('issue label'))

    @property
    def pkg_e_issn(self):
        if self._compiled_pkg_metadata is None:
            self.compile_pkg_metadata()
        return more_frequent(self._compiled_pkg_metadata['e-ISSN'])

    @property
    def pkg_p_issn(self):
        if self._compiled_pkg_metadata is None:
            self.compile_pkg_metadata()
        return more_frequent(self._compiled_pkg_metadata['print ISSN'])

    def identify_issue(self, db_manager, pkg_name):
        self.acron_issue_label, self.issue_models, issue_error_msg = db_manager.get_issue_models(self.pkg_journal_title, self.pkg_issue_label, self.pkg_p_issn, self.pkg_e_issn)
        self.acron_issue_label = self.acron_issue_label.replace('issue', pkg_name)
        self.issue_files = db_manager.get_issue_files(self.issue_models, self.pkg_path)
        return issue_error_msg

    @property
    def journal_check_list(self):
        data = {}
        index = 0
        for label in self.journal_check_list_labels:
            data[label] = self._compiled_pkg_metadata.get(label, {}).items()
        return data


class ArticlesPkgReport(object):

    def __init__(self, report_path, pkg_articles, journal, issue, previous_registered_articles, is_db_generation):
        self.journal = journal
        self.issue = issue
        self.pkg_articles = pkg_articles
        self.report_path = report_path
        if self.pkg_articles.issue_files is not None:
            self.report_path = self.pkg_articles.issue_files.base_reports_path
        if previous_registered_articles is None:
            self.complete_issue_articles = self.pkg_articles
        else:
            complete = {}
            for k, item in pkg_articles.articles.items():
                complete[k] = item
            for k, item in previous_registered_articles.items():
                if not k in complete.keys():
                    complete[k] = item
            self.complete_issue_articles = PkgArticles(complete, self.pkg_articles.issue_files.base_source_path)
            self.complete_issue_articles.issue_files = self.pkg_articles.issue_files
            self.complete_issue_articles.issue_models = self.pkg_articles.issue_models
        self.reftype_and_sources = None
        self.is_db_generation = is_db_generation
        self._blocking_errors = None
        self._registered_issue_data_validations = None
        self._registered_journal_data_validations = None
        self.consistence_blocking_errors = None
        self.xc_validations = None

        self.complete_issue_articles.error_level_for_unique = {'order': validation_status.STATUS_FATAL_ERROR, 'doi': validation_status.STATUS_FATAL_ERROR, 'elocation id': validation_status.STATUS_FATAL_ERROR, 'fpage-lpage-seq-elocation-id': validation_status.STATUS_ERROR}

        if not self.is_db_generation:
            self.complete_issue_articles.error_level_for_unique['order'] = validation_status.STATUS_WARNING

    def overview_report(self):
        r = ''
        r += html_reports.tag('h4', _('Languages overview'))
        labels, items = self.tabulate_elements_by_languages()
        r += html_reports.sheet(labels, items, 'dbstatus')

        r += html_reports.tag('h4', _('Dates overview'))
        labels, items = self.tabulate_dates()
        r += html_reports.sheet(labels, items, 'dbstatus')

        r += html_reports.tag('h4', _('Affiliations overview'))
        items = []
        affs_compiled = self.compile_affiliations()
        for label, occs in affs_compiled.items():
            items.append({'label': label, 'quantity': str(len(occs)), _('files'): sorted(list(set(occs)))})

        r += html_reports.sheet(['label', 'quantity', _('files')], items, 'dbstatus')
        return r

    def references_overview_report(self):

        if self.reftype_and_sources is None:
            self.compile_references()

        labels = ['label', 'status', 'message', _('why it is not a valid message?')]
        items = []

        values = []
        values.append(_('references by type'))
        values.append(validation_status.STATUS_INFO)
        values.append({reftype: str(sum([len(occ) for occ in sources.values()])) for reftype, sources in self.reftype_and_sources.items()})
        values.append('')
        items.append(label_values(labels, values))

        #message = {source: reftypes for source, reftypes in sources_and_reftypes.items() if len(reftypes) > 1}}
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
    def compiled_affiliations(self):
        if self._compiled_affilitions is None:
            self._compiled_affilitions = self.compile_affiliations()
        return self._compiled_affilitions

    def compile_affiliations(self):
        evaluation = {}
        keys = [_('authors without aff'), 
                _('authors with more than 1 affs'), 
                _('authors with invalid xref[@ref-type=aff]'), 
                _('incomplete affiliations')]
        for k in keys:
            evaluation[k] = []

        for xml_name, doc in self.complete_issue_articles.articles.items():
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
        for xml_name, doc in self.complete_issue_articles.articles.items():
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

    def tabulate_languages(self):
        labels = ['name', 'toc section', '@article-type', 'article titles', 
            'abstracts', 'key words', '@xml:lang', 'versions']

        items = []
        for xml_name in self.complete_issue_articles.xml_name_sorted_by_order:
            doc = self.complete_issue_articles.articles[xml_name]
            values = []
            values.append(xml_name)
            values.append(doc.sorted_toc_sections)
            values.append(doc.article_type)
            values.append(['[' + str(t.language) + '] ' + str(t.title) for t in doc.titles])
            values.append([t.language for t in doc.abstracts])
            k = {}
            for item in doc.keywords:
                if not item.get('l') in k.keys():
                    k[item.get('l')] = []
                k[item.get('l')].append(item.get('k'))
            values.append(k)
            values.append(doc.language)
            values.append(doc.trans_languages)
            items.append(label_values(labels, values))
        return (labels, items)

    def tabulate_elements_by_languages(self):
        labels = ['name', 'toc section', '@article-type', 'article titles, abstracts, key words', '@xml:lang', 'sub-article/@xml:lang']
        items = []
        for xml_name in self.complete_issue_articles.xml_name_sorted_by_order:
            doc = self.complete_issue_articles.articles[xml_name]
            lang_dep = {}
            for lang in doc.title_abstract_kwd_languages:

                data = {}
                data['title'] = doc.titles_by_lang.get(lang)
                data['abstract'] = doc.abstracts_by_lang.get(lang)
                data['keywords'] = doc.keywords_by_lang.get(lang)

                lang += ' (' + str(attributes.LANGUAGES.get(lang)).encode('utf-8') + ')'
                lang_dep[lang] = {}
                for k, values in data.items():
                    if values is not None:
                        if k == 'title':
                            lang_dep[lang][k] = [item.title for item in values]
                        else:
                            lang_dep[lang][k] = [item.text for item in values]
            authors = []
            for item in doc.contrib_names:
                item_content = ''
                if item.role is not None:
                    item_content += '(contrib-type=' + item.role + ') '
                if item.surname is not None:
                    item_content += item.surname
                if item.fname is not None:
                    item_content += ', ' + item.fname
                if item.prefix is not None:
                    item_content += ' | prefix: ' + item.prefix
                if item.suffix is not None:
                    item_content += ' | suffix: ' + item.suffix
                authors.append(item_content)
            for item in doc.contrib_collabs:
                item_content = 'collab: '
                if item.role is not None:
                    item_content += '(contrib-type=' + item.role + ') '
                if item.collab is not None:
                    item_content += item.collab
                authors.append(item_content)

            values = []
            values.append(xml_name)
            values.append(doc.sorted_toc_sections)
            values.append(doc.article_type)
            values.append(authors)
            values.append('')
            values.append('')
            items.append(label_values(labels, values))

            values = []
            values.append(xml_name)
            values.append(doc.sorted_toc_sections)
            values.append(doc.article_type)
            values.append(lang_dep)
            values.append(doc.language)
            values.append(doc.trans_languages)
            items.append(label_values(labels, values))
        return (labels, items)

    def tabulate_dates(self):
        labels = ['name', '@article-type', 
        'received', 'accepted', 'receive to accepted (days)', 'article date', 'issue date', 'accepted to publication (days)', 'accepted to today (days)']

        items = []
        for xml_name in self.complete_issue_articles.xml_name_sorted_by_order:
            #utils.debugging(xml_name)
            doc = self.complete_issue_articles.articles[xml_name]
            #utils.debugging(doc)
            values = []
            values.append(xml_name)

            #utils.debugging('doc.article_type')
            #utils.debugging(doc.article_type)
            values.append(doc.article_type)

            #utils.debugging('doc.received_dateiso')
            #utils.debugging(doc.received_dateiso)
            values.append(article_utils.display_date(doc.received_dateiso))

            #utils.debugging('doc.accepted_dateiso')
            #utils.debugging(doc.accepted_dateiso)
            values.append(article_utils.display_date(doc.accepted_dateiso))

            #utils.debugging('doc.history_days')
            #utils.debugging(doc.history_days)
            values.append(str(doc.history_days))

            #utils.debugging('doc.article_pub_dateiso')
            #utils.debugging(doc.article_pub_dateiso)
            values.append(article_utils.display_date(doc.article_pub_dateiso))

            #utils.debugging('doc.issue_pub_dateiso')
            #utils.debugging(doc.issue_pub_dateiso)
            values.append(article_utils.display_date(doc.issue_pub_dateiso))

            #utils.debugging('doc.publication_days')
            #utils.debugging(doc.publication_days)
            values.append(str(doc.publication_days))

            #utils.debugging('doc.registration_days')
            #utils.debugging(doc.registration_days)
            values.append(str(doc.registration_days))

            #utils.debugging(values)
            items.append(label_values(labels, values))
            #utils.debugging(items)

        return (labels, items)

    def pages(self):
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        for xml_name in self.complete_issue_articles.xml_name_sorted_by_order:
            #if self.complete_issue_articles.articles[xml_name].is_rolling_pass or self.complete_issue_articles.articles[xml_name].is_ahead:
            #else:
            fpage = self.complete_issue_articles.articles[xml_name].fpage
            lpage = self.complete_issue_articles.articles[xml_name].lpage
            msg = []
            status = ''
            if self.complete_issue_articles.articles[xml_name].pages == '':
                msg.append(_('no pagination was found'))
                if not self.complete_issue_articles.articles[xml_name].is_ahead:
                    status = validation_status.STATUS_ERROR
            if fpage is not None and lpage is not None:
                if fpage.isdigit() and lpage.isdigit():
                    int_fpage = int(fpage)
                    int_lpage = int(lpage)

                    #if not self.complete_issue_articles.articles[xml_name].is_rolling_pass and not self.complete_issue_articles.articles[xml_name].is_ahead:
                    if int_previous_lpage is not None:
                        if int_previous_lpage > int_fpage:
                            status = validation_status.STATUS_FATAL_ERROR if not self.complete_issue_articles.articles[xml_name].is_epub_only else validation_status.STATUS_WARNING
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
            #dates = '|'.join([item if item is not None else 'none' for item in [self.complete_issue_articles.articles[xml_name].epub_ppub_dateiso, self.complete_issue_articles.articles[xml_name].collection_dateiso, self.complete_issue_articles.articles[xml_name].epub_dateiso]])
            msg = '; '.join(msg)
            if len(msg) > 0:
                msg = '. ' + msg
            results.append({'label': xml_name, 'status': status, 'message': self.complete_issue_articles.articles[xml_name].pages + msg, _('why it is not a valid message?'): ''})
        return results

    @property
    def blocking_errors(self):
        if self._blocking_errors is None:
            if self.registered_issue_data_validations is not None:
                self._blocking_errors = self.registered_issue_data_validations.fatal_errors
            if self.registered_issue_data_validations is None:
                self._blocking_errors = 0
        return self._blocking_errors + self.consistence_blocking_errors

    @property
    def registered_journal_data_validations(self):
        licenses = []
        if self._registered_journal_data_validations is None:
            self._registered_journal_data_validations = PackageValidationsResults(self.report_path, 'journal-', '')

            for xml_name, article in self.pkg_articles.articles.items():
                unmatched = []
                items = []
                license_url = None
                if len(article.article_licenses) > 0:
                    license_url = article.article_licenses.values()[0].get('href')
                items.append([_('NLM title'), article.journal_id_nlm_ta, self.journal.nlm_title, validation_status.STATUS_FATAL_ERROR])
                items.append([_('journal-id (publisher-id)'), article.journal_id_publisher_id, self.journal.acron, validation_status.STATUS_FATAL_ERROR])
                items.append([_('e-ISSN'), article.e_issn, self.journal.e_issn, validation_status.STATUS_FATAL_ERROR])
                items.append([_('print ISSN'), article.print_issn, self.journal.p_issn, validation_status.STATUS_FATAL_ERROR])
                items.append([_('publisher name'), article.publisher_name, self.journal.publisher_name, validation_status.STATUS_ERROR])
                items.append([_('license'), license_url, self.journal.license, validation_status.STATUS_ERROR])

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
                self._registered_journal_data_validations.add(xml_name, ValidationsResults(validations_result))
        return self._registered_journal_data_validations

    @property
    def registered_issue_data_validations(self):
        if self._registered_issue_data_validations is None:
            if self.complete_issue_articles.issue_models is not None:
                self._registered_issue_data_validations = PackageValidationsResults(self.complete_issue_articles.issue_files.base_reports_path, 'issue-', '')
                for xml_name, article in self.complete_issue_articles.articles.items():
                    issue_validations_msg = self.complete_issue_articles.issue_models.validate_article_issue_data(self.complete_issue_articles.articles[xml_name])
                    self._registered_issue_data_validations.add(xml_name, ValidationsResults(issue_validations_msg))
        return self._registered_issue_data_validations

    @property
    def issue_report(self):
        report = []
        report.append(self.journal_issue_header_report)
        if self.registered_journal_data_validations is not None:
            if self.registered_journal_data_validations.total > 0:
                report.append(html_reports.tag('h2', _('Checking journal data: XML files and registered data') + '<sup>*</sup>') + html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('If the data in the XML files are correct, please, ignore the error messages and report the errors found in the registered data.') + html_reports.tag('p', html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', _('Consult the registered data'))), 'note') + self.registered_journal_data_validations.report(True))

        self.evaluate_pkg_journal_and_issue_data_consistence()

        for item in [self.xc_validations, self.pkg_data_consistence_validations]:
            if item is not None:
                print(item.total)
                if item.total > 0:
                    report.append(item.message)
            
        if self.is_db_generation:
            if self.registered_issue_data_validations is not None:
                if self.registered_issue_data_validations.total > 0:
                    report.append(html_reports.tag('h2', _('Checking issue data: XML files and registered data')) + self.registered_issue_data_validations.report(True))

        return ''.join(report) if len(report) > 0 else None

    def evaluate_pkg_journal_and_issue_data_consistence(self):
        if self.complete_issue_articles._compiled_pkg_metadata is None:
            self.complete_issue_articles.compile_pkg_metadata()
        self.consistence_blocking_errors = 0

        r = ''
        if len(self.complete_issue_articles.invalid_xml_name_items) > 0:
            r += html_reports.tag('div', html_reports.p_message(validation_status.STATUS_FATAL_ERROR + ': ' + _('Invalid XML files.')))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', self.complete_issue_articles.invalid_xml_name_items, 'issue-problem'))
        for label, items in self.complete_issue_articles.pkg_missing_items.items():
            r += html_reports.tag('div', html_reports.p_message(validation_status.STATUS_FATAL_ERROR + ': ' + _('Missing') + ' ' + label + ' ' + _('in') + ':'))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))

        for label in self.complete_issue_articles.expected_equal_values:
            if len(self.complete_issue_articles._compiled_pkg_metadata[label]) > 1:
                _status = validation_status.STATUS_FATAL_ERROR
                if label == 'issue pub date':
                    if self.complete_issue_articles.is_rolling_pass:
                        _status = validation_status.STATUS_WARNING
                elif label == 'license':
                    _status = validation_status.STATUS_WARNING
                _m = _('same value for %s is required for all the documents in the package') % (label)
                part = html_reports.p_message(_status + ': ' + _m + '.')
                for found_value, xml_files in self.complete_issue_articles._compiled_pkg_metadata[label].items():
                    part += html_reports.format_list(_('found') + ' ' + label + '="' + html_reports.display_xml(found_value) + '" ' + _('in') + ':', 'ul', xml_files, 'issue-problem')
                r += part

        for label in self.complete_issue_articles.expected_unique_value:
            if len(self.complete_issue_articles._compiled_pkg_metadata[label]) > 0 and len(self.complete_issue_articles._compiled_pkg_metadata[label]) != len(self.complete_issue_articles.articles):
                duplicated = {}
                for found_value, xml_files in self.complete_issue_articles._compiled_pkg_metadata[label].items():
                    if len(xml_files) > 1:
                        duplicated[found_value] = xml_files

                if len(duplicated) > 0:
                    _m = _(': unique value of %s is required for all the documents in the package') % (label)
                    part = html_reports.p_message(self.complete_issue_articles.error_level_for_unique[label] + _m)
                    if self.complete_issue_articles.error_level_for_unique[label] == validation_status.STATUS_FATAL_ERROR:
                        self.consistence_blocking_errors += 1
                    for found_value, xml_files in duplicated.items():
                        part += html_reports.format_list(_('found') + ' ' + label + '="' + found_value + '" ' + _('in') + ':', 'ul', xml_files, 'issue-problem')
                    r += part

        pages = html_reports.tag('h2', _('Pages Report')) + html_reports.tag('div', html_reports.sheet(['label', 'status', 'message', _('why it is not a valid message?')], self.pages(), table_style='validation'))

        toc_report = html_reports.tag('h2', _('Checking issue data consistence')) + html_reports.tag('div', r, 'issue-messages') + pages
        self.pkg_data_consistence_validations = ValidationsResults(toc_report)

    @property
    def journal_issue_header_report(self):
        if self.complete_issue_articles.compiled_pkg_metadata is None:
            self.complete_issue_articles.compile_pkg_metadata()
        issue_common_data = ''
        for label in self.complete_issue_articles.expected_equal_values:
            message = ''
            if len(self.complete_issue_articles._compiled_pkg_metadata[label].items()) == 1:
                issue_common_data += html_reports.tag('p', html_reports.display_label_value(label, self.complete_issue_articles._compiled_pkg_metadata[label].keys()[0]))
            else:
                issue_common_data += html_reports.format_list(label + ':', 'ol', self.complete_issue_articles._compiled_pkg_metadata[label].keys())
        return html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', issue_common_data, 'issue-data')

    def validate_articles_pkg_xml_and_data(self, doc_files_info_items, dtd_files, is_xml_generation, selected_names=None):
        pkg_path = os.path.dirname(doc_files_info_items.values()[0].new_xml_filename)

        self.pkg_xml_structure_validations = PackageValidationsResults(self.report_path, 'xmlstr-', '')
        self.pkg_xml_content_validations = PackageValidationsResults(self.report_path, 'xmlcon-', '')

        self.validate_articles_pkg_xml_structure(doc_files_info_items, dtd_files, selected_names)
        self.validate_articles_pkg_xml_content(doc_files_info_items, pkg_path, {k: v.new_name for k, v in doc_files_info_items.items()}, is_xml_generation, selected_names)

        if self.is_db_generation:
            self.pkg_xml_structure_validations.save_reports()
            self.pkg_xml_content_validations.save_reports()

    def validate_articles_pkg_xml_structure(self, doc_files_info_items, dtd_files, selected_names=None):
        if selected_names is None:
            selected_names = self.pkg_articles.articles.keys()
        n = '/' + str(len(self.pkg_articles.articles))
        index = 0

        utils.display_message('\n')
        utils.display_message(_('Validating XML files'))
        #utils.debugging('Validating package: inicio')
        for xml_name in self.pkg_articles.xml_name_sorted_by_order:
            doc = self.pkg_articles.articles[xml_name]
            doc_files_info = doc_files_info_items[xml_name]
            new_name = doc_files_info.new_name

            index += 1
            item_label = str(index) + n + ': ' + new_name
            utils.display_message(item_label)

            if xml_name in selected_names:
                for f in [doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename, doc_files_info.pmc_style_report_filename]:
                    if os.path.isfile(f):
                        os.unlink(f)
                xml_filename = doc_files_info.new_xml_filename

                # XML structure validations
                xml_f, xml_e, xml_w = validate_article_xml(xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)
                report_content = ''
                for rep_file in [doc_files_info.err_filename, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename]:
                    if os.path.isfile(rep_file):
                        report_content += extract_report_core(fs_utils.read_file(rep_file))
                        #if is_xml_generation is False:
                        #    fs_utils.delete_file_or_folder(rep_file)
                data_validations = ValidationsResults(report_content)
                data_validations.fatal_errors = xml_f
                data_validations.errors = xml_e
                data_validations.warnings = xml_w
                self.pkg_xml_structure_validations.add(xml_name, data_validations)
            else:
                utils.display_message(' -- not selected')

    def validate_articles_pkg_xml_content(self, doc_files_info_items, pkg_path, new_names, is_xml_generation, selected_names=None):
        if selected_names is None:
            selected_names = self.pkg_articles.articles.keys()
        n = '/' + str(len(self.pkg_articles.articles))
        index = 0

        utils.display_message('\n')
        utils.display_message(_('Validating XML files'))
        #utils.debugging('Validating package: inicio')
        for xml_name in self.pkg_articles.xml_name_sorted_by_order:
            doc = self.pkg_articles.articles[xml_name]
            doc_files_info = doc_files_info_items[xml_name]
            new_name = new_names.get(xml_name)
            index += 1
            item_label = str(index) + n + ': ' + new_name
            utils.display_message(item_label)

            if xml_name in selected_names:
                report_content = article_reports.article_data_and_validations_report(self.journal, doc, new_name, pkg_path, doc_files_info.images_report_filename, self.is_db_generation, is_xml_generation)
                data_validations = ValidationsResults(report_content)
                self.pkg_xml_content_validations.add(xml_name, data_validations)
                if is_xml_generation:
                    stats = html_reports.statistics_display(data_validations, False)
                    title = [_('Data Quality Control'), new_name]
                    fs_utils.write_file(doc_files_info.data_report_filename, html_reports.html(title, stats + report_content))
            else:
                utils.display_message(' -- not selected')

    def detail_report(self):
        labels = ['name', 'order', 'fpage', 'pagination', 'doi/aop pid/related', 'toc section', '@article-type', 'article title', 'reports']
        items = []

        n = '/' + str(len(self.complete_issue_articles.articles))
        index = 0

        validations_text = ''

        #utils.debugging(self.pkg_stats)
        #utils.debugging(self.complete_issue_articles.xml_name_sorted_by_order)
        utils.display_message('\n')
        utils.display_message(_('Generating Detail report'))
        for new_name in self.complete_issue_articles.xml_name_sorted_by_order:
            index += 1
            item_label = str(index) + n + ': ' + new_name
            utils.display_message(item_label)

            a_name = 'view-reports-' + new_name
            links = '<a name="' + a_name + '"/>'
            status = ''
            block = ''

            if self.pkg_xml_structure_validations.item(new_name) is not None:
                if self.pkg_xml_structure_validations.item(new_name).total > 0:
                    status = html_reports.statistics_display(self.pkg_xml_structure_validations.item(new_name))
                    links += html_reports.report_link('xmlrep' + new_name, '[ ' + _('Structure Validations') + ' ]', 'xmlrep', a_name)
                    links += html_reports.tag('span', status, 'smaller')
                    block += html_reports.report_block('xmlrep' + new_name, self.pkg_xml_structure_validations.item(new_name).message, 'xmlrep', a_name)

            if self.pkg_xml_content_validations.item(new_name) is not None:
                status = html_reports.statistics_display(self.pkg_xml_content_validations.item(new_name))
                links += html_reports.report_link('datarep' + new_name, '[ ' + _('Contents Validations') + ' ]', 'datarep', a_name)
                links += html_reports.tag('span', status, 'smaller')
                block += html_reports.report_block('datarep' + new_name, self.pkg_xml_content_validations.item(new_name).message, 'datarep', a_name)

            if self.is_db_generation:
                if self.registered_issue_data_validations is not None:
                    issue_validations = self.registered_issue_data_validations.item(new_name)
                    if issue_validations is not None:
                        if issue_validations.total > 0:
                            status = html_reports.statistics_display(issue_validations)
                            links += html_reports.report_link('xcrep' + new_name, '[ ' + _('Converter Validations') + ' ]', 'xcrep', a_name)
                            links += html_reports.tag('span', status, 'smaller')
                            block += html_reports.report_block('xcrep' + new_name, issue_validations.message, 'xcrep', a_name)

            values = []
            values.append(new_name)
            values.append(self.complete_issue_articles.articles[new_name].order)
            values.append(self.complete_issue_articles.articles[new_name].fpage)
            values.append(self.complete_issue_articles.articles[new_name].pages)
            values.append({'doi': self.complete_issue_articles.articles[new_name].doi, 'aop doi': self.complete_issue_articles.articles[new_name].previous_pid, 'related': [item.get('xml', '') for item in self.complete_issue_articles.articles[new_name].related_articles]})
            values.append(self.complete_issue_articles.articles[new_name].sorted_toc_sections)
            values.append(self.complete_issue_articles.articles[new_name].article_type)
            values.append(self.complete_issue_articles.articles[new_name].title)
            values.append(links)

            items.append(label_values(labels, values))
            items.append({'reports': block})

        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=['reports'])


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


def update_err_filename(err_filename, dtd_report):
    if os.path.isfile(dtd_report):
        separator = ''
        if os.path.isfile(err_filename):
            separator = '\n\n\n' + '.........\n\n\n'
        open(err_filename, 'a+').write(separator + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(dtd_report, 'r').read())


def delete_irrelevant_reports(ctrl_filename, is_valid_style, dtd_validation_report, style_checker_report):
    if ctrl_filename is None:
        if is_valid_style is True:
            os.unlink(style_checker_report)
    else:
        open(ctrl_filename, 'w').write('Finished')
    if os.path.isfile(dtd_validation_report):
        os.unlink(dtd_validation_report)


def validate_article_xml(xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename):
    xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, dtd_files, dtd_report, style_report)
    f, e, w = valid_style
    update_err_filename(err_filename, dtd_report)
    if xml is None:
        f += 1
    if not valid_dtd:
        f += 1
    delete_irrelevant_reports(ctrl_filename, f + e + w == 0, dtd_report, style_report)
    return (f, e, w)


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


def sum_stats(stats_items):
    f = sum([i[0] for i in stats_items])
    e = sum([i[1] for i in stats_items])
    w = sum([i[2] for i in stats_items])
    return (f, e, w)


def error_msg_subtitle():
    msg = html_reports.tag('p', _('Fatal error - indicates errors which impact on the quality of the bibliometric indicators and other services'))
    msg += html_reports.tag('p', _('Error - indicates the other kinds of errors'))
    msg += html_reports.tag('p', _('Warning - indicates that something can be an error or something needs more attention'))
    return html_reports.tag('div', msg, 'subtitle')


def label_values(labels, values):
    r = {}
    for i in range(0, len(labels)):
        r[labels[i]] = values[i]
    return r


def articles_sorted_by_order(articles):
    sorted_by_order = {}
    for xml_name, article in articles.items():
        try:
            _order = article.order
        except:
            _order = 'None'
        if not _order in sorted_by_order.keys():
            sorted_by_order[_order] = []
        sorted_by_order[_order].append(article)
    return sorted_by_order


def processing_result_location(result_path):
    return '<h5>' + _('Result of the processing:') + '</h5>' + '<p>' + html_reports.link('file:///' + result_path, result_path) + '</p>'


def save_report(filename, title, content, xpm_version=None):
    if xpm_version is not None:
        content += html_reports.tag('p', _('report generated by XPM ') + xpm_version)
    html_reports.save(filename, title, content)
    utils.display_message('\n\nReport:' + '\n ' + filename)


def display_report(report_filename):
    try:
        import webbrowser
        webbrowser.open('file:///' + report_filename.replace('//', '/').encode(encoding=sys.getfilesystemencoding()), new=2)
    except:
        pass


def format_complete_report(report_components):
    content = ''
    order = ['xml-files', 'summary-report', 'issue-report', 'detail-report', 'conversion-report', 'pkg_overview', 'db-overview', 'issue-not-registered', 'toc', 'references']
    labels = {
        'issue-report': 'journal/issue',
        'summary-report': _('Summary report'), 
        'detail-report': _('XML Validations report'), 
        'conversion-report': _('Conversion report'),
        'xml-files': _('Files/Folders'),
        'db-overview': _('Database'),
        'pkg_overview': _('Package overview'),
        'references': _('Sources')
    }
    validations = ValidationsResults(html_reports.join_texts(report_components.values()))
    report_components['summary-report'] = error_msg_subtitle() + html_reports.statistics_display(validations, False) + report_components.get('summary-report', '')

    content += html_reports.tabs_items([(tab_id, labels[tab_id]) for tab_id in order if report_components.get(tab_id) is not None], 'summary-report')
    for tab_id in order:
        c = report_components.get(tab_id)
        if c is not None:
            style = 'selected-tab-content' if tab_id == 'summary-report' else 'not-selected-tab-content'
            content += html_reports.tab_block(tab_id, c, style)

    content += html_reports.tag('p', _('finished'))
    validations.message = label_errors(content)
    return validations


def format_declaration_report(validations_results):
    t = ['FATAL ERROR', 'ERROR', 'WARNING']
    i = 0
    lines = []
    for item in [validations_results.fatal_errors, validations_results.errors, validations_results.warnings]:
        for n in range(item):
            lines.append({'label': '[' + t[i][0] + str(n + 1) + ']', 'status': '[' + t[i] + ']', _('why it is not a valid message?'): '&#160;'})
        i += 1
    return html_reports.sheet(['label', 'status', _('why it is not a valid message?')], lines, table_style='dbstatus')


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


def label_errors(content):
    content = label_errors_type(content, validation_status.STATUS_FATAL_ERROR, 'F')
    content = label_errors_type(content, validation_status.STATUS_ERROR, 'E')
    content = label_errors_type(content, validation_status.STATUS_WARNING, 'W')
    return content


def join_reports(reports, errors_only=False):
    _reports = ''
    if reports is not None:
        for xml_name, results in reports.items():
            if results.total > 0 or errors_only is False:
                _reports += html_reports.tag('h4', xml_name)
                _reports += results.message
    return _reports


def more_frequent(data):
    if data is not None:
        items = data.keys()
        if len(items) == 1:
            return items[0]
        elif len(items) > 1:
            q = 0
            selected = None
            for item in items:
                if len(data[item]) > q:
                    q = len(data[item])
                    selected = item
            return selected
