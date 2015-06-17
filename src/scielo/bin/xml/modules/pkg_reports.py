# coding=utf-8

import os
from datetime import datetime

import attributes
import article_reports
import article_utils
import xpchecker
import html_reports


log_items = []


class ArticlePackage(object):

    def __init__(self, articles):
        self.articles = articles
        self.compile_references()

    @property
    def xml_name_sorted_by_order(self):
        if self.__xml_name_sorted_by_order is None:
            self.__xml_name_sorted_by_order = self.sort_xml_name_by_order()
        return self.__xml_name_sorted_by_order

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
        keys = ['authors without aff', 
                'authors with more than 1 affs', 
                'authors with invalid xref[@ref-type=aff]', 
                'incomplete affiliations']
        for k in keys:
            evaluation[k] = 0

        for xml_name, doc in self.articles.items():
            aff_ids = [aff.id for aff in doc.affiliations]
            for contrib in doc.contrib_names:
                if len(contrib.xref) == 0:
                    evaluation['authors without aff'] += 1
                elif len(contrib.xref) > 1:
                    valid_xref = [xref for xref in contrib.xref if xref in aff_ids]
                    if len(valid_xref) != len(contrib.xref):
                        evaluation['authors with invalid xref[@ref-type=aff]'] += 1
                    elif len(valid_xref) > 1:
                        evaluation['authors with more than 1 affs'] += 1
                    elif len(valid_xref) == 0:
                        evaluation['authors without aff'] += 1
            for aff in doc.affiliations:
                if None in [aff.id, aff.i_country, aff.norgname, aff.orgname, aff.city, aff.state, aff.country]:
                    evaluation['incomplete affiliations'] += 1
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
        for xml_name, doc in self.articles.items():
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

    def tabulate_dates(self):
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
        return (labels, items)

    def journal_and_issue_metadata(self, labels):
        invalid_xml_name_items = []
        pkg_metadata = {label: {} for label in labels}

        for xml_name, article in self.articles.items():
            if article.tree is None:
                invalid_xml_name_items.append(xml_name)
            else:
                art_data = article.summary()
                for label in labels:
                    pkg_metadata[label] = article_utils.add_new_value_to_index(pkg_metadata[label], art_data[label], xml_name)

        return (invalid_xml_name_items, pkg_metadata)


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


def generate_article_xml_validations_reports(xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename, run_background):

    xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, dtd_files, dtd_report, style_report, run_background)
    f, e, w = valid_style
    update_err_filename(err_filename, dtd_report)
    delete_irrelevant_reports(ctrl_filename, f + e + w == 0, dtd_report, style_report)
    if xml is None:
        f += 1
    if not valid_dtd:
        f += 1
    return (f, e, w)


def write_article_contents_validations_report(new_name, report_filename, content, display_title):

    f, e, w = html_reports.statistics_numbers(content)

    stats = ''
    title = ''
    if display_title:
        stats = html_reports.statistics_display(f, e, w, False)
        title = ['Data Quality Control', new_name]

    html_reports.save(report_filename, title, stats + content)
    return (f, e, w)


def get_report_text(filename):
    report = ''
    if os.path.isfile(filename):
        content = open(filename, 'r').read()
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
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
            content = content[content.find('<body'):]
            content = content[0:content.rfind('</body>')]
            report = content[content.find('>')+1:]
        elif '<body' in content:
            content = content[content.find('<body'):]
            report = content[content.find('>')+1:]
        else:
            report = ''
    return report


def sum_stats(stats_items):
    f = sum([i[0] for i in stats_items])
    e = sum([i[1] for i in stats_items])
    w = sum([i[2] for i in stats_items])
    return (f, e, w)


def xml_list(pkg_path, xml_filenames=None):
    r = ''
    r += '<p>XML path: ' + pkg_path + '</p>'
    if xml_filenames is None:
        xml_filenames = [pkg_path + '/' + name for name in os.listdir(pkg_path) if name.endswith('.xml')]
    r += '<p>Total of XML files: ' + str(len(xml_filenames)) + '</p>'
    r += html_reports.format_list('', 'ol', [os.path.basename(f) for f in xml_filenames])
    return '<div class="xmllist">' + r + '</div>'


def articles_pkg_consistency_report(articles_pkg, validate_order):
    equal_data = ['journal-title', 'journal id NLM', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
    unique_data = ['order', 'doi', 'elocation id']
    unique_status = {'order': 'FATAL ERROR', 'doi': 'FATAL ERROR', 'elocation id': 'FATAL ERROR', 'fpage-and-seq': 'ERROR'}

    if not validate_order:
        unique_status['order'] = 'WARNING'

    invalid_xml_name_items, pkg_metadata = articles_pkg.journal_and_issue_metadata(equal_data + unique_data)

    r = ''
    if len(invalid_xml_name_items) > 0:
        r += html_reports.tag('div', html_reports.format_message('FATAL ERROR: Invalid XML files.'))
        r += html_reports.tag('div', html_reports.format_list('', 'ol', invalid_xml_name_items, 'issue-problem'))

    for label in equal_data:
        if len(pkg_metadata[label]) > 1:
            part = html_reports.p_message('FATAL ERROR: same value for ' + label + ' is required for all the documents in the package')
            for found_value, xml_files in pkg_metadata[label].items():
                part += html_reports.format_list('found ' + label + ' "' + html_reports.display_xml(found_value, html_reports.XML_WIDTH*0.6) + '" in:', 'ul', xml_files, 'issue-problem')
            r += part

    for label in unique_data:
        if len(pkg_metadata[label]) > 0 and len(pkg_metadata[label]) != len(articles_pkg.articles):
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
                part = html_reports.p_message(unique_status[label] + ': unique value of ' + label + ' is required for all the documents in the package')
                for found_value, xml_files in duplicated.items():
                    part += html_reports.format_list('found ' + label + ' "' + found_value + '" in:', 'ul', xml_files, 'issue-problem')
                r += part
            if len(none) > 0:
                part = html_reports.p_message('INFO: there is no value for ' + label + '.')
                part += html_reports.format_list('no value for ' + label + ' in:', 'ul', none, 'issue-problem')
                r += part

    issue_common_data = ''
    for label in equal_data:
        message = ''
        if len(pkg_metadata[label].items()) == 1:
            issue_common_data += html_reports.display_labeled_value(label, pkg_metadata[label].keys()[0])
        else:
            message = '(ERROR: Unique value expected for ' + label + ')'
            issue_common_data += html_reports.format_list(label + message, 'ol', pkg_metadata[label].keys())
    return html_reports.tag('div', issue_common_data, 'issue-data') + html_reports.tag('div', r, 'issue-messages')


def articles_pkg_consistency_stats(articles_pkg_constency_report):
    return html_reports.statistics_numbers(articles_pkg_constency_report)


def validate_package(articles, validate_order):
    return article_reports.toc_report_data(articles, validate_order)


def articles_pkg_overview_report(articles_pkg):
    r = ''
    r += html_reports.tag('h4', 'Languages overview')
    labels, items = articles_pkg.tabulate_languages()
    r += html_reports.sheet(labels, items, 'dbstatus')

    r += html_reports.tag('h4', 'Dates overview')
    labels, items = articles_pkg.tabulate_dates()
    r += html_reports.sheet(labels, items, 'dbstatus')

    r += html_reports.tag('h4', 'Affiliations overview')
    items = []
    affs_compiled = articles_pkg.compile_affiliations()
    for label, q in affs_compiled.items():
        items.append({'label': label, 'quantity': str(q)})
    r += html_reports.sheet(['label', 'quantity'], items, 'dbstatus')
    return r


def articles_pkg_references_overview_report(articles_pkg):
    labels = ['label', 'status', 'message']
    items = []

    values = []
    values.append('references by type')
    values.append('INFO')
    values.append({reftype: str(sum(sources.values())) for reftype, sources in articles_pkg.reftype_and_sources.items()})
    items.append(label_values(labels, values))

    #message = {source: reftypes for source, reftypes in sources_and_reftypes.items() if len(reftypes) > 1}}
    if len(articles_pkg.bad_sources_and_reftypes) > 0:
        values = []
        values.append('same sources as different types')
        values.append('ERROR')
        values.append(articles_pkg.bad_sources_and_reftypes)
        items.append(label_values(labels, values))
        values = []
        values.append('same sources as different types references')
        values.append('INFO')
        values.append({source: articles_pkg.sources_at.get(source) for source in articles_pkg.bad_sources_and_reftypes.keys()})
        items.append(label_values(labels, values))

    if len(articles_pkg.missing_source) > 0:
        items.append({'label': 'references missing source', 'status': 'ERROR', 'message': [' - '.join(item) for item in articles_pkg.missing_source]})
    if len(articles_pkg.missing_year) > 0:
        items.append({'label': 'references missing year', 'status': 'ERROR', 'message': [' - '.join(item) for item in articles_pkg.missing_year]})
    if len(articles_pkg.unusual_sources) > 0:
        items.append({'label': 'references with unusual value for source', 'status': 'ERROR', 'message': [' - '.join(item) for item in articles_pkg.unusual_sources]})
    if len(articles_pkg.unusual_years) > 0:
        items.append({'label': 'references with unusual value for year', 'status': 'ERROR', 'message': [' - '.join(item) for item in articles_pkg.unusual_years]})

    return html_reports.tag('h4', 'Package references overview') + html_reports.sheet(labels, items, table_style='dbstatus')


def articles_pkg_sources_overview_report(reftype_and_sources):
    labels = ['source', 'total']
    h = ''
    for reftype, sources in reftype_and_sources.items():
        items = []
        h += html_reports.tag('h4', reftype)
        for source in sorted(sources.keys()):
            items.append({'source': source, 'total': str(sources[source])})
        h += html_reports.sheet(labels, items, 'dbstatus')
    return h


def package_articles_references_overview(sources_at, bad_sources_and_reftypes, reftype_and_sources, missing_source, missing_year, unusual_sources, unusual_years):
    labels = ['label', 'status', 'message']
    items = []

    values = []
    values.append('references by type')
    values.append('INFO')
    values.append({reftype: str(sum(sources.values())) for reftype, sources in reftype_and_sources.items()})
    items.append(label_values(labels, values))

    #message = {source: reftypes for source, reftypes in sources_and_reftypes.items() if len(reftypes) > 1}}
    if len(bad_sources_and_reftypes) > 0:
        values = []
        values.append('same sources as different types')
        values.append('ERROR')
        values.append(bad_sources_and_reftypes)
        items.append(label_values(labels, values))
        values = []
        values.append('same sources as different types')
        values.append('INFO')
        values.append({source: sources_at.get(source) for source in bad_sources_and_reftypes.keys()})
        items.append(label_values(labels, values))

    if len(missing_source) > 0:
        items.append({'label': 'references missing source', 'status': 'ERROR', 'message': [' - '.join(item) for item in missing_source]})
    if len(missing_year) > 0:
        items.append({'label': 'references missing year', 'status': 'ERROR', 'message': [' - '.join(item) for item in missing_year]})
    if len(unusual_sources) > 0:
        items.append({'label': 'references with unusual value for source', 'status': 'ERROR', 'message': [' - '.join(item) for item in unusual_sources]})
    if len(unusual_years) > 0:
        items.append({'label': 'references with unusual value for year', 'status': 'ERROR', 'message': [' - '.join(item) for item in unusual_years]})

    return html_reports.tag('h3', 'Package references overview') + html_reports.sheet(labels, items, table_style='validation', row_style='status')


def pkg_references_sources_and_types(pkg_articles):
    sources_and_reftypes = {}
    sources_at = {}
    reftype_and_sources = {}
    missing_source = []
    missing_year = []
    unusual_sources = []
    unusual_years = []
    for xml_name in sorted_xml_name_by_order(pkg_articles):
        doc = pkg_articles[xml_name]
        for ref in doc.references:
            norm_source = str(ref.source).strip().upper()
            if not norm_source in sources_and_reftypes.keys():
                sources_and_reftypes[norm_source] = {}
            if not ref.publication_type in sources_and_reftypes[norm_source].keys():
                sources_and_reftypes[norm_source][ref.publication_type] = 0
            sources_and_reftypes[norm_source][ref.publication_type] += 1

            if not norm_source in sources_at.keys():
                sources_at[norm_source] = []
            if not xml_name in sources_at[norm_source]:
                sources_at[norm_source].append(xml_name + ' - ' + ref.id)

            if not ref.publication_type in reftype_and_sources.keys():
                reftype_and_sources[ref.publication_type] = {}
            if not ref.source in reftype_and_sources[ref.publication_type].keys():
                reftype_and_sources[ref.publication_type][ref.source] = 0
            reftype_and_sources[ref.publication_type][ref.source] += 1

            # year
            if ref.publication_type in attributes.BIBLIOMETRICS_USE:
                if ref.year is None:
                    missing_year.append([ref.id, xml_name])
                else:
                    numbers = len([n for n in ref.year if n.isdigit()])
                    not_numbers = len(ref.year) - numbers
                    if not_numbers > numbers:
                        unusual_years.append([ref.year, ref.id, xml_name])

                if ref.source is None:
                    missing_source.append([xml_name, ref.id])
                else:
                    numbers = len([n for n in ref.source if n.isdigit()])
                    not_numbers = len(ref.source) - numbers
                    if not_numbers < numbers:
                        unusual_sources.append([xml_name, ref.id, ref.source])

    return (sources_at, sources_and_reftypes, reftype_and_sources, missing_source, missing_year, unusual_sources, unusual_years)


def pkg_sources_reports(sources, sources_at):
    labels = ['source', '@publication-type', 'xml name']
    items = []
    #bad_sources = {k:v for k, v in sources.items() if len(v) > 1}
    for source, reftypes in sources.items():
        values = []
        values.append(source)
        values.append(reftypes)
        values.append(sources_at.get(source))
        items.append(label_values(labels, values))

    return html_reports.sheet(labels, items)


def pkg_references_stats(doc_items):
    rows = []
    pkg_source_and_type = {}
    pkg_type_and_source = {}
    pkg_type_and_year = {}
    pkg_type = {}
    pkg_sources = {}
    pkg_publisher = {}
    for xml_name in sorted_xml_name_by_order(doc_items):
        doc = doc_items[xml_name]
        doc_type_and_year = {}
        doc_source_and_type = {}
        doc_type_and_source = {}
        doc_sources = {}
        doc_publisher = {}
        for ref in doc.references:
            if ref.year is None:
                key = ref.publication_type + ' - None'
            else:
                key = ref.publication_type + ' - ' + ref.year
            if not key in doc_type_and_year.keys():
                doc_type_and_year[key] = 0
            if not key in pkg_type_and_year.keys():
                pkg_type_and_year[key] = 0
            doc_type_and_year[key] += 1
            pkg_type_and_year[key] += 1
            if not ref.publication_type in pkg_type.keys():
                pkg_type[ref.publication_type] = 0
            pkg_type[ref.publication_type] += 1

            if ref.source is None:
                key = 'None [' + ref.publication_type + ']'
            else:
                key = ref.source + ' [' + ref.publication_type + ']'
            if not key in doc_source_and_type.keys():
                doc_source_and_type[key] = 0
            if not key in pkg_source_and_type.keys():
                pkg_source_and_type[key] = 0
            doc_source_and_type[key] += 1
            pkg_source_and_type[key] += 1

            if ref.source is None:
                key = 'None'
            else:
                key = ref.source
            if not ref.publication_type in doc_type_and_source.keys():
                doc_type_and_source[ref.publication_type] = []
            if not ref.publication_type in pkg_type_and_source.keys():
                pkg_type_and_source[ref.publication_type] = []
            doc_type_and_source[ref.publication_type].append(key)
            pkg_type_and_source[ref.publication_type].append(key)

            if ref.source is None:
                key = 'None'
            else:
                key = ref.source
            if not key in doc_sources.keys():
                doc_sources[key] = []
            if not key in pkg_sources.keys():
                pkg_sources[key] = []
            pkg_sources[key].append(ref.publication_type)
            doc_sources[key].append(ref.publication_type)

            if ref.publisher_name is None:
                key = 'None'
            else:
                key = ref.publisher_name
            if ref.publisher_loc is None:
                key += '|None'
            else:
                key += '|' + ref.publisher_loc
            if not key in doc_publisher.keys():
                doc_publisher[key] = 0
            if not key in pkg_publisher.keys():
                pkg_publisher[key] = 0
            pkg_publisher[key] += 1
            doc_publisher[key] += 1

        columns = {}
        columns['statistics'] = [k + ': ' + '|'.join(sorted(list(set(doc_sources[k])))) for k in sorted(doc_sources.keys()) if len(list(set(doc_sources[k]))) > 1]

        if len(columns['statistics']) > 0:
            columns['filename'] = xml_name
            columns['notes'] = ' WARNING: ref same sources different types'
            rows.append(columns)

        columns = {}
        columns['filename'] = xml_name
        columns['notes'] = 'ref types and sources'
        columns['statistics'] = {k: sorted(doc_type_and_source[k]) for k in sorted(doc_type_and_source.keys())}
        rows.append(columns)

        columns = {}
        columns['filename'] = xml_name
        columns['notes'] = 'ref sources and types'
        columns['statistics'] = [k + ': ' + str(doc_source_and_type[k]) for k in sorted(doc_source_and_type.keys())]
        rows.append(columns)

        columns = {}
        columns['filename'] = xml_name
        columns['notes'] = 'ref types'
        columns['statistics'] = [k + ': ' + str(doc.refstats[k]) for k in sorted(doc.refstats.keys())]
        rows.append(columns)

        columns = {}
        columns['filename'] = xml_name
        columns['notes'] = 'ref types and year'
        columns['statistics'] = [k + ': ' + str(doc_type_and_year[k]) for k in sorted(doc_type_and_year.keys())]
        rows.append(columns)

        #columns = {}
        #columns['filename'] = xml_name
        #columns['notes'] = 'publishers'
        #columns['statistics'] = [k + ': ' + str(doc_publisher[k]) for k in sorted(doc_publisher.keys())]
        #rows.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = 'WARNING: ref same sources different types'
    columns['statistics'] = [k + ': ' + '|'.join(sorted(list(set(pkg_sources[k])))) for k in sorted(pkg_sources.keys()) if len(list(set(pkg_sources[k]))) > 1]
    if len(columns['statistics']) > 0:
        rows.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = 'ref types and sources'
    columns['statistics'] = {k: sorted(pkg_type_and_source[k]) for k in sorted(pkg_type_and_source.keys())}
    rows.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = 'ref sources and types'
    columns['statistics'] = [k + ': ' + str(pkg_source_and_type[k]) for k in sorted(pkg_source_and_type.keys())]
    rows.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = 'ref types'
    columns['statistics'] = [k + ': ' + str(pkg_type[k]) for k in sorted(pkg_type.keys())]
    rows.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = 'ref types and year'
    columns['statistics'] = [k + ': ' + str(pkg_type_and_year[k]) for k in sorted(pkg_type_and_year.keys())]
    rows.append(columns)

    #columns = {}
    #columns['filename'] = 'PACKAGE'
    #columns['notes'] = 'publishers'
    #columns['statistics'] = [k + ': ' + str(pkg_publisher[k]) for k in sorted(pkg_publisher.keys())]
    #rows.append(columns)

    r = ''
    r += html_reports.tag('h2', 'References statistics')
    r += html_reports.sheet(['filename', 'notes', 'statistics'], rows)
    return r


def pkg_authors_and_affiliations_stats(doc_items):
    """
    x autores com afiliação
    x do país y
    x sem estado
    x sem cidade
    x com instituição normalizada
    """
    pkg_xref_counts = {}
    pkg_affs = {}
    pkg_norm_affs = {}

    statistics = []
    for xml_name in sorted_xml_name_by_order(doc_items):
        doc = doc_items[xml_name]

        doc_xref_counts = {}
        doc_invalid_xref = {}
        doc_affs = {}
        doc_norm_affs = {}

        aff_ids = [aff.id for aff in doc.affiliations if aff.id is not None]
        for contrib in doc.contrib_names:
            for xref in contrib.xref:
                if not xref in aff_ids:
                    if not 'not found aff/@id=' + xref in doc_invalid_xref.keys():
                        doc_invalid_xref['not found aff/@id=' + xref] = 0
                    doc_invalid_xref['not found aff/@id=' + xref] += 1
            label = 'authors with ' + str(len(contrib.xref)) + ' affs'
            if not label in doc_xref_counts.keys():
                doc_xref_counts[label] = 0
            if not label in pkg_xref_counts.keys():
                pkg_xref_counts[label] = 0
            doc_xref_counts[label] += 1
            pkg_xref_counts[label] += 1

        for aff in doc.affiliations:
            items = []
            for item in [aff.orgname, aff.norgname, aff.city, aff.state, aff.i_country, aff.country]:
                if item is None:
                    item = 'None'
                items.append(item)
            key = ' | '.join(items)
            if not key in doc_affs.keys():
                doc_affs[key] = 0
            if not key in pkg_affs.keys():
                pkg_affs[key] = 0
            doc_affs[key] += 1
            pkg_affs[key] += 1

            items = []
            for item in [aff.i_country, aff.norgname]:
                if item is None:
                    item = 'None'
                items.append(item)
            key = ' | '.join(items)
            if not key in doc_norm_affs.keys():
                doc_norm_affs[key] = 0
            if not key in pkg_norm_affs.keys():
                pkg_norm_affs[key] = 0
            doc_norm_affs[key] += 1
            pkg_norm_affs[key] += 1

        columns = {}
        columns['filename'] = xml_name
        columns['notes'] = 'quantity of affs by author'
        columns['statistics'] = doc_xref_counts
        statistics.append(columns)

        if len(doc_invalid_xref) > 0:
            columns = {}
            columns['filename'] = xml_name
            columns['notes'] = 'ERROR: invalid xref'

            columns['statistics'] = doc_invalid_xref
            statistics.append(columns)

        columns = {}
        columns['filename'] = xml_name
        columns['notes'] = 'full'
        columns['statistics'] = doc_affs
        statistics.append(columns)

        columns = {}
        columns['filename'] = xml_name
        columns['notes'] = 'normalized'
        columns['statistics'] = doc_norm_affs
        statistics.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = ''
    columns['statistics'] = pkg_xref_counts
    statistics.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = 'full'
    columns['statistics'] = {k: pkg_affs[k] for k in sorted(pkg_affs.keys())}
    statistics.append(columns)

    columns = {}
    columns['filename'] = 'PACKAGE'
    columns['notes'] = 'normalized'
    columns['statistics'] = {k: pkg_norm_affs[k] for k in sorted(pkg_norm_affs.keys())}
    statistics.append(columns)

    r = ''
    r += html_reports.tag('h2', 'Authors and affiliations statistics')
    r += html_reports.sheet(['filename', 'notes', 'statistics'], statistics)
    return r


def error_msg_subtitle():
    msg = html_reports.tag('p', 'Fatal error - indicates errors which impact on the quality of the bibliometric indicators and other services')
    msg += html_reports.tag('p', 'Error - indicates the other kinds of errors')
    msg += html_reports.tag('p', 'Warning - indicates that something can be an error or something needs more attention')
    return html_reports.tag('div', msg, 'subtitle')


def validate_pkg_items(org_manager, doc_items, doc_files_info_items, dtd_files, validate_order, display_all, xml_articles_status=None):
    articles_stats = {}
    articles_reports = {}
    articles_sheets = {}
    fatal_errors = 0

    for xml_name, doc_files_info in doc_files_info_items.items():
        for f in [doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename, doc_files_info.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)

    print('Validating package: inicio')

    for xml_name in sorted_xml_name_by_order(doc_items):
        doc = doc_items[xml_name]
        doc_files_info = doc_files_info_items[xml_name]

        new_name = doc_files_info.new_name
        print(new_name)
        register_log(new_name)

        skip = False
        if xml_articles_status is not None:
            skip = xml_articles_status[doc_files_info.xml_name] == 'skip-update'

        if skip:
            print(' -- skept')
        else:
            xml_filename = doc_files_info.new_xml_filename
            xml_f, xml_e, xml_w = generate_article_xml_validations_reports(xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename, display_all is False)

            article_display_report, article_validation_report, sheet_data = article_reports.get_article_report_data(org_manager, doc, new_name, os.path.dirname(xml_filename), validate_order)
            if article_display_report is None:
                content = 'FATAL ERROR: Unable to get data of ' + new_name + '.'
            else:
                content = article_reports.format_report(article_display_report, article_validation_report, display_all)

            data_f, data_e, data_w = write_article_contents_validations_report(new_name, doc_files_info.data_report_filename, content, display_all)

            articles_stats[new_name] = ((xml_f, xml_e, xml_w), (data_f, data_e, data_w))

            fatal_errors += xml_f + data_f

            articles_reports[new_name] = (doc_files_info.err_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename)

            #if sheet_data is not None:
            #    articles_sheets[new_name] = (sheet_data.authors_sheet_data(new_name), sheet_data.sources_sheet_data(new_name))
            #else:
            #    articles_sheets[new_name] = (None, None)

    print('Validating package: fim')
    return (fatal_errors, articles_stats, articles_reports)


def articles_pkg_xml_and_data_validation_report(org_manager, doc_items, doc_files_info_items, dtd_files, validate_order, display_all, xml_articles_status=None):
    #FIXME
    articles_stats = {}
    articles_reports = {}
    articles_sheets = {}
    fatal_errors = 0

    for xml_name, doc_files_info in doc_files_info_items.items():
        for f in [doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename, doc_files_info.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)

    print('Validating package: inicio')

    for xml_name in sorted_xml_name_by_order(doc_items):
        doc = doc_items[xml_name]
        doc_files_info = doc_files_info_items[xml_name]

        new_name = doc_files_info.new_name
        print(new_name)
        register_log(new_name)

        skip = False
        if xml_articles_status is not None:
            skip = xml_articles_status[doc_files_info.xml_name] == 'skip-update'

        if skip:
            print(' -- skept')
        else:
            xml_filename = doc_files_info.new_xml_filename
            xml_f, xml_e, xml_w = generate_article_xml_validations_reports(xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename, display_all is False)

            article_display_report, article_validation_report, sheet_data = article_reports.get_article_report_data(org_manager, doc, new_name, os.path.dirname(xml_filename), validate_order)
            if article_display_report is None:
                content = 'FATAL ERROR: Unable to get data of ' + new_name + '.'
            else:
                content = article_reports.format_report(article_display_report, article_validation_report, display_all)

            data_f, data_e, data_w = write_article_contents_validations_report(new_name, doc_files_info.data_report_filename, content, display_all)

            articles_stats[new_name] = ((xml_f, xml_e, xml_w), (data_f, data_e, data_w))

            fatal_errors += xml_f + data_f

            articles_reports[new_name] = (doc_files_info.err_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename)

            #if sheet_data is not None:
            #    articles_sheets[new_name] = (sheet_data.authors_sheet_data(new_name), sheet_data.sources_sheet_data(new_name))
            #else:
            #    articles_sheets[new_name] = (None, None)

    print('Validating package: fim')
    return (fatal_errors, articles_stats, articles_reports)


def validate_articles_pkg_xml_and_data(org_manager, pkg_articles, doc_files_info_items, dtd_files, validate_order, display_all, xml_articles_status=None):
    #FIXME
    articles_stats = {}
    articles_reports = {}
    articles_sheets = {}
    fatal_errors = 0

    for xml_name, doc_files_info in doc_files_info_items.items():
        for f in [doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename, doc_files_info.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)

    print('Validating package: inicio')
    articles_pkg = ArticlePackage(pkg_articles)
    for xml_name in articles_pkg.sorted_xml_name_by_order:
        doc = articles_pkg.articles[xml_name]
        doc_files_info = doc_files_info_items[xml_name]

        new_name = doc_files_info.new_name
        print(new_name)
        register_log(new_name)

        skip = False
        if xml_articles_status is not None:
            skip = xml_articles_status[doc_files_info.xml_name] == 'skip-update'

        if skip:
            print(' -- skept')
        else:
            xml_filename = doc_files_info.new_xml_filename
            xml_f, xml_e, xml_w = generate_article_xml_validations_reports(xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename, display_all is False)

            article_display_report, article_validation_report, sheet_data = article_reports.get_article_report_data(org_manager, doc, new_name, os.path.dirname(xml_filename), validate_order)
            if article_display_report is None:
                content = 'FATAL ERROR: Unable to get data of ' + new_name + '.'
            else:
                content = article_reports.format_report(article_display_report, article_validation_report, display_all)

            data_f, data_e, data_w = write_article_contents_validations_report(new_name, doc_files_info.data_report_filename, content, display_all)

            articles_stats[new_name] = ((xml_f, xml_e, xml_w), (data_f, data_e, data_w))

            fatal_errors += xml_f + data_f

            articles_reports[new_name] = (doc_files_info.err_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename)

            #if sheet_data is not None:
            #    articles_sheets[new_name] = (sheet_data.authors_sheet_data(new_name), sheet_data.sources_sheet_data(new_name))
            #else:
            #    articles_sheets[new_name] = (None, None)

    print('Validating package: fim')
    return (fatal_errors, articles_stats, articles_reports)


def get_toc_report_text(toc_f, toc_e, toc_w, toc_report):
    toc_text = ''
    if toc_f + toc_e + toc_w > 0:
        toc_text = html_reports.tag('h2', 'Table of contents Report')
        toc_text += html_reports.collapsible_block('toc', 'table of contents validations: ' + html_reports.statistics_display(toc_f, toc_e, toc_w), toc_report, html_reports.get_stats_numbers_style(toc_f, toc_e, toc_w))
    return toc_text


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


def get_articles_report_text(pkg_articles, articles_reports, articles_stats, conversion_reports=None):
    labels = ['name', 'order', 'fpage', 'aop pid', 'toc section', '@article-type', 'article title', 'reports']
    items = []

    n = '/' + str(len(articles_reports))
    validations_text = ''
    index = 0

    for new_name in sorted(articles_reports.keys()):
        index += 1
        item_label = str(index) + n + ' - ' + new_name
        print(item_label)

        xml_f, xml_e, xml_w = articles_stats[new_name][0]
        data_f, data_e, data_w = articles_stats[new_name][1]
        rep1, rep2, rep3 = articles_reports[new_name]

        links = ''
        block = ''
        if xml_f + xml_e + xml_w > 0:
            t = []
            v = []
            for rep in [rep1, rep2]:
                content = get_report_text(rep)
                if len(content) > 0:
                    t.append(os.path.basename(rep))
                    v.append(content)
            content = ''.join(v)
            status = html_reports.get_stats_numbers_style(xml_f, xml_e, xml_w)
            links += html_reports.report_link('xmlrep' + new_name, ' [ style ] ', status)
            block += html_reports.report_block('xmlrep' + new_name, content, status)

        if data_f + data_e + data_w > 0:
            status = html_reports.get_stats_numbers_style(data_f, data_e, data_w)
            links += html_reports.report_link('datarep' + new_name, ' [ quality control ] ', status)
            block += html_reports.report_block('datarep' + new_name, get_report_text(rep3), status)

        if conversion_reports is not None:
            r = conversion_reports.get(new_name)
            if r is not None:
                conv_f, conv_e, conv_w, conv_rep = r
                status = html_reports.get_stats_numbers_style(conv_f, conv_e, conv_w)
                links += html_reports.report_link('xcrep' + new_name, ' [ converter ] ', status)
                block += html_reports.report_block('xcrep' + new_name, conv_rep, status)

        values = []
        values.append(new_name)
        values.append(pkg_articles[new_name].order)
        values.append(pkg_articles[new_name].fpage)
        values.append(pkg_articles[new_name].previous_pid)
        values.append(pkg_articles[new_name].toc_section)
        values.append(pkg_articles[new_name].article_type)
        values.append(pkg_articles[new_name].title)
        values.append(links)

        items.append(label_values(labels, values))
        items.append({'reports': block})

    return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=['reports'])


def get_articles_report_text_v1(articles_reports, articles_stats, conversion_reports=None):
    n = '/' + str(len(articles_reports))
    validations_text = ''
    index = 0
    validations_text = html_reports.tag('h2', 'XML Validations')
    for new_name in sorted(articles_reports.keys()):
        index += 1
        item_label = str(index) + n + ' - ' + new_name
        print(item_label)
        validations_text += html_reports.tag('h4', item_label)
        xml_f, xml_e, xml_w = articles_stats[new_name][0]
        data_f, data_e, data_w = articles_stats[new_name][1]

        rep1, rep2, rep3 = articles_reports[new_name]
        if xml_f + xml_e + xml_w > 0:
            t = []
            v = []
            for rep in [rep1, rep2]:
                content = get_report_text(rep)
                if len(content) > 0:
                    t.append(os.path.basename(rep))
                    v.append(content)
            content = ''.join(v)
            s = html_reports.statistics_display(xml_f, xml_e, xml_w)
            validations_text += html_reports.collapsible_block('xmlrep' + str(index), 'XML validations (' + ' and '.join(t) + '): ' + s, content, html_reports.get_stats_numbers_style(xml_f, xml_e, xml_w))

        if data_f + data_e + data_w > 0:
            s = html_reports.statistics_display(data_f, data_e, data_w)
            validations_text += html_reports.collapsible_block('datarep' + str(index), 'Data quality control (' + os.path.basename(rep3) + '): ' + s, get_report_text(rep3), html_reports.get_stats_numbers_style(data_f, data_e, data_w))

        if conversion_reports is not None:
            r = conversion_reports.get(new_name)
            if r is not None:
                validations_text += r[3]
    return validations_text


def get_lists_report_text(articles_sheets):
    toc_authors_sheet_data = []
    toc_sources_sheet_data = []
    authors_h = None
    authors_w = None
    sources_h = None
    sources_w = None

    lists_text = html_reports.tag('h2', 'Authors and Sources Lists')

    for new_name in sorted(articles_sheets.keys()):
        if not articles_sheets[new_name][0] is None:
            authors_h, authors_w, authors_data = articles_sheets[new_name][0]
            toc_authors_sheet_data += authors_data

        if not articles_sheets[new_name][1] is None:
            sources_h, sources_w, sources_data = articles_sheets[new_name][1]
            toc_sources_sheet_data += sources_data

    authors = html_reports.sheet(authors_h, toc_authors_sheet_data)
    lists_text += html_reports.collapsible_block('authors', 'Authors in the package', authors)

    sources = html_reports.sheet(sources_h, toc_sources_sheet_data)
    lists_text += html_reports.collapsible_block('sources', 'Sources in the package', sources)

    return lists_text


def processing_result_location(result_path):
    return '<h5>Result of the processing: </h5>' + '<p>' + html_reports.link('file:///' + result_path, result_path) + '</p>'


def save_report(filename, title, content):
    html_reports.save(filename, title, content)
    print('\n\nReport:\n ' + filename)


def display_report(report_filename):
    try:
        os.system('python -mwebbrowser file:///' + report_filename.replace('//', '/'))
    except:
        pass


def statistics_and_subtitle(f, e, w):
    x = error_msg_subtitle()
    x += html_reports.statistics_display(f, e, w, False)
    return x


def format_complete_report(report_components):
    content = ''
    order = ['summary-report', 'detail-report', 'xml-files', 'pkg_overview', 'db-overview', 'issue-not-registered', 'toc', 'references']
    labels = {
        'summary-report': 'Summary report', 
        'detail-report': 'Detail report', 
        'xml-files': 'Files/Folders',
        'db-overview': 'Database overview',
        'pkg_overview': 'Package overview',
        'issue-not-registered': 'Issue validations (not registered)',
        'toc': 'Issue validations (toc)',
        'references': 'Sources'
    }
    f, e, w = html_reports.statistics_numbers(html_reports.join_texts(report_components.values()))
    report_components['summary-report'] = statistics_and_subtitle(f, e, w) + report_components.get('summary-report', '')

    print('issue-not-registered')
    print(report_components.get('issue-not-registered'))
    print(type(report_components.get('issue-not-registered')))

    print('toc')
    print(report_components.get('toc'))
    print(type(report_components.get('toc')))

    content += html_reports.tabs_items([(tab_id, labels[tab_id]) for tab_id in order if report_components.get(tab_id) is not None], 'summary-report')
    for tab_id in order:
        c = report_components.get(tab_id)
        if c is not None:
            style = 'selected-tab-content' if tab_id == 'summary-report' else 'not-selected-tab-content'
            content += html_reports.tab_block(tab_id, c, style)

    content += html_reports.tag('p', 'Finished.')
    return (f, e, w, content)
