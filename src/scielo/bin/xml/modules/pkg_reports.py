# coding=utf-8

import sys
import os
from datetime import datetime

from __init__ import _
import attributes
import article_reports
import article_utils
import xpchecker
import html_reports
import utils
import fs_utils


log_items = []


class PackageValidationsResults(object):

    def __init__(self, validations_results_items=None):
        if validations_results_items is None:
            self.validations_results_items = {}
        else:
            self.validations_results_items = validations_results_items

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

    def report(self, errors_only=False):
        _reports = ''
        if self.validations_results_items is not None:
            for xml_name, results in self.validations_results_items.items():
                if results.total > 0 or errors_only is False:
                    _reports += html_reports.tag('h4', xml_name)
                    _reports += results.message
        return _reports


class ValidationsResults(object):

    def __init__(self, message):
        self.fatal_errors, self.errors, self.warnings = html_reports.statistics_numbers(message)
        self.message = message

    @property
    def total(self):
        return sum([self.fatal_errors, self.errors, self.warnings])


class ArticlePackage(object):

    def __init__(self, articles):
        self.articles = articles
        self.compile_references()
        self._xml_name_sorted_by_order = None
        self._indexed_by_order = None

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
    def indexed_by_order(self):
        if self._indexed_by_order is None:
            self._indexed_by_order = self.index_by_order()
        return self._indexed_by_order

    def index_by_order(self):
        indexed = {}
        for xml_name, article in self.articles.items():
            _order = str(article.order)
            if not _order in indexed.keys():
                indexed[_order] = []
            indexed[_order].append(article)
        return indexed

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
            evaluation[k] = 0

        for xml_name, doc in self.articles.items():
            aff_ids = [aff.id for aff in doc.affiliations]
            for contrib in doc.contrib_names:
                if len(contrib.xref) == 0:
                    evaluation[_('authors without aff')] += 1
                elif len(contrib.xref) > 1:
                    valid_xref = [xref for xref in contrib.xref if xref in aff_ids]
                    if len(valid_xref) != len(contrib.xref):
                        evaluation[_('authors with invalid xref[@ref-type=aff]')] += 1
                    elif len(valid_xref) > 1:
                        evaluation[_('authors with more than 1 affs')] += 1
                    elif len(valid_xref) == 0:
                        evaluation[_('authors without aff')] += 1
            for aff in doc.affiliations:
                if None in [aff.id, aff.i_country, aff.norgname, aff.orgname, aff.city, aff.state, aff.country]:
                    evaluation[_('incomplete affiliations')] += 1
        return evaluation

    def compile_references(self):
        self.sources_and_reftypes = {}
        self.sources_at = {}
        self.reftype_and_sources = {}
        self.missing_source = []
        self.missing_year = []
        self.unusual_sources = []
        self.unusual_years = []
        for xml_name, doc in self.articles.items():
            for ref in doc.references:
                if not ref.source in self.sources_and_reftypes.keys():
                    self.sources_and_reftypes[ref.source] = {}
                if not ref.publication_type in self.sources_and_reftypes[ref.source].keys():
                    self.sources_and_reftypes[ref.source][ref.publication_type] = 0
                self.sources_and_reftypes[ref.source][ref.publication_type] += 1
                if not ref.source in self.sources_at.keys():
                    self.sources_at[ref.source] = []
                if not xml_name in self.sources_at[ref.source]:
                    self.sources_at[ref.source].append(ref.id + ' - ' + xml_name)
                if not ref.publication_type in self.reftype_and_sources.keys():
                    self.reftype_and_sources[ref.publication_type] = {}
                if not ref.source in self.reftype_and_sources[ref.publication_type].keys():
                    self.reftype_and_sources[ref.publication_type][ref.source] = 0
                self.reftype_and_sources[ref.publication_type][ref.source] += 1

                # year
                if ref.publication_type in attributes.BIBLIOMETRICS_USE:
                    if ref.year is None:
                        self.missing_year.append([ref.id, xml_name])
                    else:
                        numbers = len([n for n in ref.year if n.isdigit()])
                        not_numbers = len(ref.year) - numbers
                        if not_numbers > numbers:
                            self.unusual_years.append([ref.year, ref.id, xml_name])

                    if ref.source is None:
                        self.missing_source.append([ref.id, xml_name])
                    else:
                        numbers = len([n for n in ref.source if n.isdigit()])
                        not_numbers = len(ref.source) - numbers
                        if not_numbers < numbers:
                            self.unusual_sources.append([ref.source, ref.id, xml_name])
        self.bad_sources_and_reftypes = {source: reftypes for source, reftypes in self.sources_and_reftypes.items() if len(reftypes) > 1}

    def tabulate_languages(self):
        labels = ['name', 'toc section', '@article-type', 'article titles', 
            'abstracts', 'key words', '@xml:lang', 'versions']

        items = []
        for xml_name in self.xml_name_sorted_by_order:
            doc = self.articles[xml_name]
            values = []
            values.append(xml_name)
            values.append(doc.toc_section)
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
        for xml_name in self.xml_name_sorted_by_order:
            doc = self.articles[xml_name]
            lang_dep = {}
            for lang in doc.title_abstract_kwd_languages:

                elements = {}
                elem = doc.titles_by_lang.get(lang)
                if elem is not None:
                    elements['title'] = elem.title
                elem = doc.abstracts_by_lang.get(lang)
                if elem is not None:
                    elements['abstract'] = elem.text
                elem = doc.keywords_by_lang.get(lang)
                if elem is not None:
                    elements['keywords'] = [k.text for k in elem]
                lang_dep[lang] = elements

            values = []
            values.append(xml_name)
            values.append(doc.toc_section)
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
        for xml_name in self.xml_name_sorted_by_order:
            #utils.debugging(xml_name)
            doc = self.articles[xml_name]
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

    def journal_and_issue_metadata(self, labels, required_data):
        invalid_xml_name_items = []
        pkg_metadata = {label: {} for label in labels}
        missing_data = {}

        n = '/' + str(len(self.articles))
        index = 0

        utils.display_message('\n')
        utils.display_message('Package report')
        for xml_name, article in self.articles.items():
            index += 1
            item_label = str(index) + n + ': ' + xml_name
            utils.display_message(item_label)

            if article.tree is None:
                invalid_xml_name_items.append(xml_name)
            else:
                art_data = article.summary()
                for label in labels:
                    if art_data[label] is None:
                        if label in required_data:
                            if not label in missing_data.keys():
                                missing_data[label] = []
                            missing_data[label].append(xml_name)
                    else:
                        pkg_metadata[label] = article_utils.add_new_value_to_index(pkg_metadata[label], art_data[label], xml_name)

        return (invalid_xml_name_items, pkg_metadata, missing_data)

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
        return _is_rolling_pass

    def pages(self):
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        for xml_name in self.xml_name_sorted_by_order:
            #if self.articles[xml_name].is_rolling_pass or self.articles[xml_name].is_ahead:
            #else:
            fpage = self.articles[xml_name].fpage
            lpage = self.articles[xml_name].lpage
            msg = []
            status = ''
            if self.articles[xml_name].pages == '':
                msg.append(_('no pagination was found'))
                if not self.articles[xml_name].is_ahead:
                    status = 'ERROR'
            if fpage is not None and lpage is not None:
                if fpage.isdigit() and lpage.isdigit():
                    int_fpage = int(fpage)
                    int_lpage = int(lpage)

                    #if not self.articles[xml_name].is_rolling_pass and not self.articles[xml_name].is_ahead:
                    if int_previous_lpage is not None:
                        if int_previous_lpage > int_fpage:
                            status = 'FATAL ERROR' if not self.articles[xml_name].is_rolling_pass and not self.articles[xml_name].is_ahead else 'WARNING'
                            msg.append(_('Invalid pages') + ': ' + _('check lpage of {previous_article} and fpage of {xml_name}').format(previous_article=previous_xmlname, xml_name=xml_name))
                        elif int_previous_lpage == int_fpage:
                            status = 'WARNING'
                            msg.append(_('lpage of {previous_article} and fpage of {xml_name} are the same').format(previous_article=previous_xmlname, xml_name=xml_name))
                        elif int_previous_lpage + 1 < int_fpage:
                            status = 'WARNING'
                            msg.append(_('there is a gap between the lpage of {previous_article} and fpage of {xml_name}').format(previous_article=previous_xmlname, xml_name=xml_name))
                    if int_fpage > int_lpage:
                        status = 'FATAL ERROR'
                        msg.append(_('Invalid page range'))
                    int_previous_lpage = int_lpage
                    previous_lpage = lpage
                    previous_xmlname = xml_name
            #dates = '|'.join([item if item is not None else 'none' for item in [self.articles[xml_name].epub_ppub_dateiso, self.articles[xml_name].collection_dateiso, self.articles[xml_name].epub_dateiso]])
            msg = '; '.join(msg)
            if len(msg) > 0:
                msg = '. ' + msg
            results.append({'label': xml_name, 'status': status, 'message': self.articles[xml_name].pages + msg})
        return results

    def validate_articles_pkg_xml_and_data(self, org_manager, doc_files_info_items, dtd_files, validate_order, xml_generation, xc_actions=None):
        #FIXME
        self.pkg_xml_structure_validations = PackageValidationsResults()
        self.pkg_xml_content_validations = PackageValidationsResults()

        for xml_name, doc_files_info in doc_files_info_items.items():
            for f in [doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename, doc_files_info.pmc_style_report_filename]:
                if os.path.isfile(f):
                    os.unlink(f)

        n = '/' + str(len(self.articles))
        index = 0

        utils.display_message('\n')
        utils.display_message(_('Validating XML files'))
        #utils.debugging('Validating package: inicio')
        for xml_name in self.xml_name_sorted_by_order:
            doc = self.articles[xml_name]
            doc_files_info = doc_files_info_items[xml_name]

            new_name = doc_files_info.new_name

            index += 1
            item_label = str(index) + n + ': ' + new_name
            utils.display_message(item_label)

            skip = False
            if xc_actions is not None:
                skip = (xc_actions[xml_name] == 'skip-update')

            if skip:
                utils.display_message(' -- skept')
            else:
                xml_filename = doc_files_info.new_xml_filename

                # XML structure validations
                xml_f, xml_e, xml_w = validate_article_xml(xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)
                report_content = ''
                for rep_file in [doc_files_info.err_filename, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename]:
                    if os.path.isfile(rep_file):
                        report_content += extract_report_core(fs_utils.read_file(rep_file))
                        if xml_generation is False:
                            fs_utils.delete_file_or_folder(rep_file)
                data_validations = ValidationsResults(report_content)
                data_validations.fatal_errors = xml_f
                data_validations.errors = xml_e
                data_validations.warnings = xml_w
                self.pkg_xml_structure_validations.add(xml_name, data_validations)

                # XML Content validations
                report_content = article_reports.article_data_and_validations_report(org_manager, doc, new_name, os.path.dirname(xml_filename), validate_order, xml_generation)
                data_validations = ValidationsResults(report_content)
                self.pkg_xml_content_validations.add(xml_name, data_validations)
                if xml_generation:
                    stats = html_reports.statistics_display(data_validations, False)
                    title = [_('Data Quality Control'), new_name]
                    html_reports.save(doc_files_info.data_report_filename, title, stats + report_content)

                #self.pkg_fatal_errors += xml_f + data_f
                #self.pkg_stats[xml_name] = ((xml_f, xml_e, xml_w), (data_f, data_e, data_w))
                #self.pkg_reports[xml_name] = (doc_files_info.err_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename)

        #utils.debugging('Validating package: fim')


class ArticlesPkgReport(object):

    def __init__(self, package):
        self.package = package

    def validate_consistency(self, validate_order):
        critical, toc_report = self.consistency_report(validate_order)
        toc_validations = ValidationsResults(toc_report)
        return (critical, toc_validations)

    def consistency_report(self, validate_order):
        critical = 0
        equal_data = ['journal-title', 'journal id NLM', 'e-ISSN', 'print ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        unique_data = ['order', 'doi', 'elocation id', ]
        if not self.package.is_processed_in_batches:
            unique_data += ['fpage-and-seq', 'lpage']
        error_level_for_unique = {'order': 'FATAL ERROR', 'doi': 'FATAL ERROR', 'elocation id': 'FATAL ERROR', 'fpage-and-seq': 'FATAL ERROR', 'lpage': 'WARNING'}
        required_data = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]

        if not validate_order:
            error_level_for_unique['order'] = 'WARNING'

        invalid_xml_name_items, pkg_metadata, missing_data = self.package.journal_and_issue_metadata(equal_data + unique_data, required_data)

        r = ''

        if len(invalid_xml_name_items) > 0:
            r += html_reports.tag('div', html_reports.p_message('FATAL ERROR: ' + _('Invalid XML files.')))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', invalid_xml_name_items, 'issue-problem'))
        for label, items in missing_data.items():
            r += html_reports.tag('div', html_reports.p_message('FATAL ERROR: ' + _('Missing') + ' ' + label + ' ' + _('in') + ':'))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))

        for label in equal_data:
            if len(pkg_metadata[label]) > 1:
                _m = _('same value for %s is required for all the documents in the package') % (label)
                part = html_reports.p_message('FATAL ERROR: ' + _m + '.')
                for found_value, xml_files in pkg_metadata[label].items():
                    part += html_reports.format_list(_('found') + ' ' + label + '="' + html_reports.display_xml(found_value, html_reports.XML_WIDTH*0.6) + '" ' + _('in') + ':', 'ul', xml_files, 'issue-problem')
                r += part

        for label in unique_data:
            if len(pkg_metadata[label]) > 0 and len(pkg_metadata[label]) != len(self.package.articles):
                none = []
                duplicated = {}
                pages = {}
                for found_value, xml_files in pkg_metadata[label].items():
                    if found_value == 'None':
                        none = xml_files
                    else:
                        if len(xml_files) > 1:
                            duplicated[found_value] = xml_files
                        if label == 'fpage-and-seq':
                            v = found_value
                            if v.isdigit():
                                v = str(int(found_value))
                            if not v in pages.keys():
                                pages[v] = []
                            pages[v] += xml_files

                if len(pages) == 1 and '0' in pages.keys():
                    duplicated = []

                if len(duplicated) > 0:
                    _m = _(': unique value of %s is required for all the documents in the package') % (label)
                    part = html_reports.p_message(error_level_for_unique[label] + _m)
                    if error_level_for_unique[label] == 'FATAL ERROR':
                        critical += 1
                    for found_value, xml_files in duplicated.items():
                        part += html_reports.format_list(_('found') + ' ' + label + '="' + found_value + '" ' + _('in') + ':', 'ul', xml_files, 'issue-problem')
                    r += part
                if len(none) > 0:
                    part = html_reports.p_message('INFO: ' + _('there is no value for ') + label + '.')
                    part += html_reports.format_list(_('no value for ') + label + ' ' + _('in') + ':', 'ul', none, 'issue-problem')
                    r += part

        issue_common_data = ''

        for label in equal_data:
            message = ''
            if len(pkg_metadata[label].items()) == 1:
                issue_common_data += html_reports.display_labeled_value(label, pkg_metadata[label].keys()[0])
            else:
                issue_common_data += html_reports.format_list(label, 'ol', pkg_metadata[label].keys())
                #issue_common_data += html_reports.p_message('FATAL ERROR: ' + _('Unique value expected for ') + label)

        pages = html_reports.tag('h2', 'Pages Report') + html_reports.tag('div', html_reports.sheet(['label', 'status', 'message'], self.package.pages(), table_style='validation', row_style='status'))

        return (critical, html_reports.tag('div', issue_common_data, 'issue-data') + html_reports.tag('div', r, 'issue-messages') + pages)

    def overview_report(self):
        r = ''

        r += html_reports.tag('h4', _('Languages overview'))
        labels, items = self.package.tabulate_elements_by_languages()
        r += html_reports.sheet(labels, items, 'dbstatus')

        r += html_reports.tag('h4', _('Dates overview'))
        labels, items = self.package.tabulate_dates()
        r += html_reports.sheet(labels, items, 'dbstatus')

        r += html_reports.tag('h4', _('Affiliations overview'))
        items = []
        affs_compiled = self.package.compile_affiliations()
        for label, q in affs_compiled.items():
            items.append({'label': label, 'quantity': str(q)})

        r += html_reports.sheet(['label', 'quantity'], items, 'dbstatus')
        return r

    def references_overview_report(self):
        labels = ['label', 'status', 'message']
        items = []

        values = []
        values.append(_('references by type'))
        values.append('INFO')
        values.append({reftype: str(sum(sources.values())) for reftype, sources in self.package.reftype_and_sources.items()})
        items.append(label_values(labels, values))

        #message = {source: reftypes for source, reftypes in sources_and_reftypes.items() if len(reftypes) > 1}}
        if len(self.package.bad_sources_and_reftypes) > 0:
            values = []
            values.append(_('same sources as different types'))
            values.append('ERROR')
            values.append(self.package.bad_sources_and_reftypes)
            items.append(label_values(labels, values))
            values = []
            values.append(_('same sources as different types references'))
            values.append('INFO')
            values.append({source: self.package.sources_at.get(source) for source in self.package.bad_sources_and_reftypes.keys()})
            items.append(label_values(labels, values))

        if len(self.package.missing_source) > 0:
            items.append({'label': _('references missing source'), 'status': 'ERROR', 'message': [' - '.join(item) for item in self.package.missing_source]})
        if len(self.package.missing_year) > 0:
            items.append({'label': _('references missing year'), 'status': 'ERROR', 'message': [' - '.join(item) for item in self.package.missing_year]})
        if len(self.package.unusual_sources) > 0:
            items.append({'label': _('references with unusual value for source'), 'status': 'ERROR', 'message': [' - '.join(item) for item in self.package.unusual_sources]})
        if len(self.package.unusual_years) > 0:
            items.append({'label': _('references with unusual value for year'), 'status': 'ERROR', 'message': [' - '.join(item) for item in self.package.unusual_years]})

        return html_reports.tag('h4', _('Package references overview')) + html_reports.sheet(labels, items, table_style='dbstatus')

    def detail_report(self, pkg_conversion_validations=None):
        labels = ['name', 'order', 'fpage', 'pagination', 'doi', 'aop pid', 'toc section', '@article-type', 'article title', 'reports']
        items = []

        n = '/' + str(len(self.package.articles))
        index = 0

        validations_text = ''

        #utils.debugging(self.package.pkg_stats)
        #utils.debugging(self.package.xml_name_sorted_by_order)
        utils.display_message('\n')
        utils.display_message(_('Generating Detail report'))
        for new_name in self.package.xml_name_sorted_by_order:
            index += 1
            item_label = str(index) + n + ': ' + new_name
            utils.display_message(item_label)

            a_name = 'view-reports-' + new_name
            links = '<a name="' + a_name + '"/>'
            status = ''
            block = ''

            if self.package.pkg_xml_structure_validations.item(new_name).total > 0:
                status = html_reports.statistics_display(self.package.pkg_xml_structure_validations.item(new_name))
                links += html_reports.report_link('xmlrep' + new_name, '[ ' + _('Structure Validations') + ' ]', 'xmlrep', a_name)
                links += html_reports.tag('span', status, 'smaller')
                block += html_reports.report_block('xmlrep' + new_name, self.package.pkg_xml_structure_validations.item(new_name).message, 'xmlrep', a_name)

            if self.package.pkg_xml_content_validations.item(new_name).total > 0:
                status = html_reports.statistics_display(self.package.pkg_xml_content_validations.item(new_name))
                links += html_reports.report_link('datarep' + new_name, '[ ' + _('Contents Validations') + ' ]', 'datarep', a_name)
                links += html_reports.tag('span', status, 'smaller')
                block += html_reports.report_block('datarep' + new_name, self.package.pkg_xml_content_validations.item(new_name).message, 'datarep', a_name)

            if pkg_conversion_validations is not None:
                conversion_validations = pkg_conversion_validations.item(new_name)
                if conversion_validations is not None:
                    if conversion_validations.total > 0:
                        status = html_reports.statistics_display(conversion_validations)
                        links += html_reports.report_link('xcrep' + new_name, '[ ' + _('Converter Validations') + ' ]', 'xcrep', a_name)
                        links += html_reports.tag('span', status, 'smaller')
                        block += html_reports.report_block('xcrep' + new_name, conversion_validations.message, 'xcrep', a_name)

            values = []
            values.append(new_name)
            values.append(self.package.articles[new_name].order)
            values.append(self.package.articles[new_name].fpage)
            values.append(self.package.articles[new_name].pages)

            values.append(self.package.articles[new_name].doi)
            values.append(self.package.articles[new_name].previous_pid)
            values.append(self.package.articles[new_name].toc_section)
            values.append(self.package.articles[new_name].article_type)
            values.append(self.package.articles[new_name].title)
            values.append(links)

            items.append(label_values(labels, values))
            items.append({'reports': block})

        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=['reports'])

    def sources_overview_report(self):
        labels = ['source', 'total']
        h = None
        if len(self.package.reftype_and_sources) > 0:
            h = ''
            for reftype, sources in self.package.reftype_and_sources.items():
                items = []
                h += html_reports.tag('h4', reftype)
                for source in sorted(sources.keys()):
                    items.append({'source': source, 'total': str(sources[source])})
                h += html_reports.sheet(labels, items, 'dbstatus')
        return h


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
        report = part1 + part2
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


def xml_list(pkg_path, xml_filenames=None):
    r = ''
    r += '<p>' + _('XML path') + ': ' + pkg_path + '</p>'
    if xml_filenames is None:
        xml_filenames = [pkg_path + '/' + name for name in os.listdir(pkg_path) if name.endswith('.xml')]
    r += '<p>' + _('Total of XML files') + ': ' + str(len(xml_filenames)) + '</p>'
    r += html_reports.format_list('', 'ol', [os.path.basename(f) for f in xml_filenames])
    return '<div class="xmllist">' + r + '</div>'


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


def sorted_xml_name_by_order(articles):
    order_and_xml_name_items = {}
    for xml_name, article in articles.items():
        if article.tree is None:
            _order = 'None'
        else:
            _order = article.order
        if not _order in order_and_xml_name_items.keys():
            order_and_xml_name_items[_order] = []
        order_and_xml_name_items[_order].append(xml_name)

    sorted_items = []
    for order in sorted(order_and_xml_name_items.keys()):
        for item in order_and_xml_name_items[order]:
            sorted_items.append(item)
    return sorted_items


def processing_result_location(result_path):
    return '<h5>' + _('Result of the processing:') + '</h5>' + '<p>' + html_reports.link('file:///' + result_path, result_path) + '</p>'


def save_report(filename, title, content, xpm_version=None):
    if xpm_version is not None:
        content += html_reports.tag('p', _('report generated by XPM ') + xpm_version)
    html_reports.save(filename, title, content)
    utils.display_message('\n\nReport:' + '\n ' + filename)


def display_report(report_filename):
    try:
        os.system('python -mwebbrowser file:///' + report_filename.replace('//', '/').encode(encoding=sys.getfilesystemencoding()))
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
    content = content.replace('ERROR', '[ERROR')
    content = content.replace('FATAL [ERROR', 'FATAL ERROR')
    content = label_errors_type(content, 'FATAL ERROR', 'F')
    content = label_errors_type(content, '[ERROR', 'E')
    content = label_errors_type(content, 'WARNING', 'W')
    content = content.replace('[ERROR', 'ERROR')
    return content


def join_reports(reports, errors_only=False):
    _reports = ''
    if reports is not None:
        for xml_name, results in reports.items():
            if results.total > 0 or errors_only is False:
                _reports += html_reports.tag('h4', xml_name)
                _reports += results.message
    return _reports
