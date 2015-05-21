# coding=utf-8
import os
import shutil
from datetime import datetime

import xml_utils
import article_utils
import article_validations
import html_reports

from article import Article, PersonAuthor, CorpAuthor, format_author


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


class TOCReport(object):

    def __init__(self, articles, validate_order):
        self.articles = articles
        self.validate_order = validate_order

    def report(self):
        invalid = []
        equal_data = ['journal-title', 'journal id NLM', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        unique_data = ['order', 'doi', 'elocation id']
        unique_status = {'order': 'FATAL ERROR', 'doi': 'FATAL ERROR', 'elocation id': 'FATAL ERROR', 'fpage-and-seq': 'ERROR'}

        if not self.validate_order:
            unique_status['order'] = 'WARNING'

        toc_data = {}
        for label in equal_data + unique_data:
            toc_data[label] = {}

        for xml_name, article in self.articles.items():
            if article.tree is None:
                invalid.append(xml_name)
            else:
                art_data = article.summary()
                for label in toc_data.keys():
                    toc_data[label] = article_utils.add_new_value_to_index(toc_data[label], art_data[label], xml_name)

        r = ''
        if len(invalid) > 0:
            r += html_reports.tag('div', html_reports.format_message('FATAL ERROR: Invalid XML files.'))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', invalid, 'issue-problem'))

        for label in equal_data:
            if len(toc_data[label]) > 1:
                part = html_reports.p_message('FATAL ERROR: same value for ' + label + ' is required for all the articles of the package')
                for found_value, xml_files in toc_data[label].items():
                    part += html_reports.format_list('found ' + label + ' "' + html_reports.display_xml(found_value) + '" in:', 'ul', xml_files, 'issue-problem')
                r += part

        for label in unique_data:
            if len(toc_data[label]) > 0 and len(toc_data[label]) != len(self.articles):
                none = []
                duplicated = {}
                pages = {}
                for found_value, xml_files in toc_data[label].items():
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
                    part = html_reports.p_message(unique_status[label] + ': unique value of ' + label + ' is required for all the articles of the package')
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
            if len(toc_data[label].items()) == 1:
                issue_common_data += html_reports.display_labeled_value(label, toc_data[label].keys()[0])
            else:
                message = '(ERROR: Unique value expected for ' + label + ')'
                issue_common_data += html_reports.format_list(label + message, 'ol', toc_data[label].keys())
        return html_reports.tag('div', issue_common_data, 'issue-data') + html_reports.tag('div', r, 'issue-messages')


class ArticleDisplayReport(object):

    def __init__(self, article, sheet_data, xml_path, xml_name):
        self.article = article
        self.xml_name = xml_name
        self.xml_path = xml_path
        self.files = package_files(xml_path, xml_name)
        self.sheet_data = sheet_data

    @property
    def article_front(self):
        r = self.xml_name + ' is invalid.'
        if self.article.tree is not None:
            r = ''
            r += self.sps
            r += self.language
            r += self.toc_section
            r += self.article_type
            r += self.display_titles()
            r += self.doi
            r += self.article_id_other
            r += self.article_previous_id
            r += self.order
            r += self.fpage
            r += self.fpage_seq
            r += self.elocation_id
            r += self.article_dates
            r += self.contrib_names
            r += self.contrib_collabs
            r += self.affiliations
            r += self.abstracts
            r += self.keywords

        return html_reports.tag('h2', 'Article front') + html_reports.tag('div', r, 'article-data')

    @property
    def article_body(self):
        r = ''
        r += self.sections
        r += self.formulas
        r += self.tables
        return html_reports.tag('h2', 'Article body') + html_reports.tag('div', r, 'article-data')

    @property
    def article_back(self):
        r = ''
        r += self.funding
        r += self.footnotes
        return html_reports.tag('h2', 'Article back') + html_reports.tag('div', r, 'article-data')

    @property
    def files_and_href(self):
        r = ''
        r += html_reports.tag('h2', 'Files in the package')
        th, w, data = self.sheet_data.package_files(self.files)
        r += html_reports.sheet(th, w, data)
        r += html_reports.tag('h2', '@href')
        th, w, data = self.sheet_data.hrefs_sheet_data(self.xml_path)
        r += html_reports.sheet(th, w, data)
        return r

    @property
    def authors_sheet(self):
        labels, width, data = self.sheet_data.authors_sheet_data()
        return html_reports.tag('h2', 'Authors') + html_reports.sheet(labels, width, data)

    @property
    def sources_sheet(self):
        labels, width, data = self.sheet_data.sources_sheet_data()
        return html_reports.tag('h2', 'Sources') + html_reports.sheet(labels, width, data)

    def display_labeled_value(self, label, value, style=''):
        return html_reports.display_labeled_value(label, value, style)

    def display_titles(self):
        r = ''
        for title in self.article.titles:
            r += html_reports.display_labeled_value(title.language, title.title)
        return r

    def display_text(self, label, items):
        r = html_reports.tag('p', label, 'label')
        for item in items:
            r += self.display_labeled_value(item.language, item.text)
        return html_reports.tag('div', r)

    @property
    def language(self):
        return self.display_labeled_value('@xml:lang', self.article.language)

    @property
    def sps(self):
        return self.display_labeled_value('@specific-use', self.article.sps)

    @property
    def toc_section(self):
        return self.display_labeled_value('toc section', self.article.toc_section, 'toc-section')

    @property
    def article_type(self):
        return self.display_labeled_value('@article-type', self.article.article_type, 'article-type')

    @property
    def article_dates(self):
        return self.display_labeled_value('date(epub-ppub)', article_utils.format_date(self.article.epub_ppub_date)) + self.display_labeled_value('date(epub)', article_utils.format_date(self.article.epub_date)) + self.display_labeled_value('date(collection)', article_utils.format_date(self.article.collection_date))

    @property
    def contrib_names(self):
        return html_reports.format_list('authors:', 'ol', [format_author(a) for a in self.article.contrib_names])

    @property
    def contrib_collabs(self):
        r = [a.collab for a in self.article.contrib_collabs]
        if len(r) > 0:
            r = html_reports.format_list('collabs', 'ul', r)
        else:
            r = self.display_labeled_value('collabs', 'None')
        return r

    @property
    def abstracts(self):
        return self.display_text('abstracts', self.article.abstracts)

    @property
    def keywords(self):
        return html_reports.format_list('keywords:', 'ol', ['(' + k['l'] + ') ' + k['k'] for k in self.article.keywords])

    @property
    def order(self):
        return self.display_labeled_value('order', self.article.order, 'order')

    @property
    def doi(self):
        return self.display_labeled_value('doi', self.article.doi, 'doi')

    @property
    def fpage(self):
        r = self.display_labeled_value('fpage', self.article.fpage, 'fpage')
        r += self.display_labeled_value('lpage', self.article.fpage, 'lpage')
        return r

    @property
    def fpage_seq(self):
        return self.display_labeled_value('fpage/@seq', self.article.fpage_seq, 'fpage')

    @property
    def elocation_id(self):
        return self.display_labeled_value('elocation-id', self.article.elocation_id, 'fpage')

    @property
    def funding(self):
        r = self.display_labeled_value('ack', self.article.ack_xml)
        r += self.display_labeled_value('fn[@fn-type="financial-disclosure"]', self.article.financial_disclosure, 'fpage')
        return r

    @property
    def article_id_other(self):
        return self.display_labeled_value('article-id (other)', self.article.article_id_other)

    @property
    def article_previous_id(self):
        return self.display_labeled_value('previous article id', self.article.article_previous_id)

    @property
    def sections(self):
        _sections = ['[' + sec_id + '] ' + sec_title + ' (' + str(sec_type) + ')' for sec_id, sec_type, sec_title in self.article.article_sections]
        return html_reports.format_list('sections:', 'ul', _sections)

    @property
    def formulas(self):
        r = html_reports.tag('p', 'disp-formulas:', 'label')
        for item in self.article.formulas:
            r += html_reports.tag('p', item)
        return r

    @property
    def footnotes(self):
        r = ''
        for item in self.article.article_fn_list:
            scope, fn_xml = item
            r += html_reports.tag('p', scope, 'label')
            r += html_reports.tag('p', fn_xml)
        if len(r) > 0:
            r = html_reports.tag('p', 'foot notes:', 'label') + r
        return r

    @property
    def issue_header(self):
        if self.article.tree is not None:
            r = [self.article.journal_title, self.article.journal_id_nlm_ta, self.article.issue_label, article_utils.format_date(self.article.issue_pub_date)]
            return html_reports.tag('div', '\n'.join([html_reports.tag('h5', item) for item in r if item is not None]), 'issue-data')
        else:
            return ''

    @property
    def tables(self):
        r = html_reports.tag('p', 'Tables:', 'label')
        for t in self.article.tables:
            header = html_reports.tag('h3', t.id)
            table_data = ''
            table_data += html_reports.display_labeled_value('label', t.label, 'label')
            table_data += html_reports.display_labeled_value('caption',  t.caption, 'label')
            table_data += html_reports.tag('p', 'table-wrap/table (xml)', 'label')
            table_data += html_reports.tag('div', html_reports.format_html_data(t.table), 'xml')
            if t.table:
                table_data += html_reports.tag('p', 'table-wrap/table', 'label')
                table_data += html_reports.tag('div', t.table, 'element-table')
            if t.graphic:
                #table_data += html_reports.display_labeled_value('table-wrap/graphic', t.graphic.display('file:///' + self.xml_path), 'value')
                table_data += html_reports.display_labeled_value('table-wrap/graphic', html_reports.image('file:///' + self.xml_path), 'value')
            r += header + html_reports.tag('div', table_data, 'block')
        return r

    @property
    def affiliations(self):
        r = html_reports.tag('p', 'Affiliations:', 'label')
        for item in self.article.affiliations:
            r += html_reports.tag('p', html_reports.format_html_data(item.xml))
        th, w, data = self.sheet_data.affiliations_sheet_data()
        r += html_reports.sheet(th, w, data)
        return r

    @property
    def id_and_xml_list(self):
        sheet_data = []
        t_header = ['@id', 'xml']
        for item in self.article.elements_which_has_id_attribute:
            row = {}
            row['@id'] = item.attrib.get('id')
            row['xml'] = xml_utils.node_xml(item)
            row['xml'] = row['xml'][0:row['xml'].find('>')+1]
            sheet_data.append(row)
        r = html_reports.tag('h2', 'elements and @id:')
        r += html_reports.sheet(t_header, [], sheet_data)
        return r

    @property
    def id_and_tag_list(self):
        sheet_data = []
        t_header = ['@id', 'tag']
        for item in self.article.elements_which_has_id_attribute:
            row = {}
            row['@id'] = item.attrib.get('id')
            row['tag'] = item.tag
            sheet_data.append(row)
        r = html_reports.tag('h2', 'elements and @id:')
        r += html_reports.sheet(t_header, [], sheet_data)
        return r

    @property
    def references_stats(self):
        r = html_reports.tag('h2', 'references')
        sheet_data = []
        for ref_type, q in self.article.refstats.items():
            row = {}
            row['element-citation/@publication-type'] = ref_type
            row['quantity'] = q
            sheet_data.append(row)
        r += html_reports.sheet(['element-citation/@publication-type', 'quantity'], [], sheet_data)
        return r


class ArticleValidationReport(object):

    def __init__(self, article_validation):
        self.article_validation = article_validation

    def display_items(self, items):
        r = ''
        for item in items:
            r += self.display_item(item)
        return r

    def display_item(self, item):
        return html_reports.p_message(item)

    def format_rows(self, items):
        content = []
        for label, status, msg in items:
            row = {}
            row['label'] = label
            row['status'] = status
            row['message'] = msg
            content.append(row)
        return content

    def validations_sheet(self, content):
        return html_reports.sheet(['label', 'status', 'message'], None, self.format_rows(content), table_style='validation', row_style='status')

    def validations(self, display_problems):
        items, performance = self.article_validation.validations

        if display_problems:
            items = [(label, status, msg) for label, status, msg in items if status != 'OK']

        r = ''
        if len(items) > 0:
            r += self.validations_sheet(items)

        r += self.references(display_problems)

        if len(r) > 0:
            r = html_reports.tag('div', html_reports.tag('h2', 'Validations') + r, 'article-messages')

        return r

    def references(self, display_problems):
        rows = ''
        for ref, ref_result in self.article_validation.references:
            if display_problems:
                ref_result = [(label, status, msg) for label, status, msg in ref_result if status != 'OK']

            if len(ref_result) > 0:
                rows += html_reports.tag('h3', 'Reference ' + ref.id)
                rows += html_reports.display_xml(ref.xml)
                rows += self.validations_sheet(ref_result)
        return rows


class ArticleSheetData(object):

    def __init__(self, article, article_validation):
        self.article = article
        self.article_validation = article_validation

    def authors_sheet_data(self, filename=None):
        r = []
        t_header = ['xref', 'publication-type', 'role', 'given-names', 'surname', 'suffix', 'prefix', 'collab']
        if not filename is None:
            t_header = ['filename', 'scope'] + t_header
        for a in self.article.contrib_names:
            row = {}
            row['scope'] = 'article meta'
            row['filename'] = filename
            row['xref'] = ' '.join(a.xref)
            row['role'] = a.role
            row['publication-type'] = self.article.article_type
            row['given-names'] = a.fname
            row['surname'] = a.surname
            row['suffix'] = a.suffix
            row['prefix'] = a.prefix
            r.append(row)

        for a in self.article.contrib_collabs:
            row = {}
            row['scope'] = 'article meta'
            row['filename'] = filename
            row['publication-type'] = self.article.article_type
            row['collab'] = a.collab
            row['role'] = a.role
            r.append(row)

        for ref in self.article.references:
            for item in ref.authors_list:
                row = {}
                row['scope'] = ref.id
                row['filename'] = filename
                row['publication-type'] = ref.publication_type

                if isinstance(item, PersonAuthor):
                    row['given-names'] = item.fname
                    row['surname'] = item.surname
                    row['suffix'] = item.suffix
                    row['prefix'] = item.prefix
                    row['role'] = item.role
                elif isinstance(item, CorpAuthor):
                    row['collab'] = item.collab
                    row['role'] = item.role
                else:
                    row['given-names'] = '?'
                    row['surname'] = '?'
                    row['suffix'] = '?'
                    row['prefix'] = '?'
                    row['role'] = '?'
                r.append(row)
        return (t_header, [], r)

    def sources_sheet_data(self, filename=None):
        r = []
        t_header = ['ID', 'type', 'year', 'source', 'publisher name', 'location', ]
        if not filename is None:
            t_header = ['filename', 'scope'] + t_header

        for ref in self.article.references:
            row = {}
            row['scope'] = ref.id
            row['ID'] = ref.id
            row['filename'] = filename
            row['type'] = ref.publication_type
            row['year'] = ref.year
            row['source'] = ref.source
            row['publisher name'] = ref.publisher_name
            row['location'] = ref.publisher_loc
            r.append(row)
        return (t_header, [], r)

    def tables_sheet_data(self, path):
        t_header = ['ID', 'label/caption', 'table/graphic']
        r = []
        for t in self.article.tables:
            row = {}
            row['ID'] = t.graphic_parent.id
            row['label/caption'] = t.graphic_parent.label + '/' + t.graphic_parent.caption
            #row['table/graphic'] = t.table + t.graphic_parent.graphic.display('file:///' + path)
            row['table/graphic'] = t.table + html_reports.image('file:///' + path)
            r.append(row)
        return (t_header, ['label/caption', 'table/graphic'], r)

    def hrefs_sheet_data(self, path):
        t_header = ['href', 'display', 'xml']
        r = []
        for status, href_items in self.article_validation.href_list(path).items():
            for hrefitem in href_items:
                row = {}
                row['href'] = hrefitem.src
                hreflocation = hrefitem.src if not hrefitem.is_internal_file else 'file:///' + hrefitem.file_location(path)

                row['display'] = ''
                if hrefitem.is_image:
                    row['display'] = html_reports.image(hreflocation)
                else:
                    row['display'] = html_reports.link(hreflocation, hrefitem.src)

                if not status == 'ok':
                    if hrefitem.is_internal_file:
                        if status == 'warning':
                            row['display'] += status.upper() + ': missing extension of ' + hrefitem.src + '.'
                        else:
                            row['display'] += status.upper() + ': ' + hrefitem.src + ' not found in package'
                    else:
                        row['display'] += status.upper() + ': ' + hrefitem.src + ' is not working'

                row['xml'] = hrefitem.xml
                r.append(row)
        return (t_header, ['display', 'xml'], r)

    def package_files(self, files):
        t_header = ['files', 'status']
        r = []
        inxml = [item.src for item in self.article.hrefs]

        for item in files:
            row = {}
            row['files'] = item
            status = ''
            if item in inxml:
                status = 'found in XML'
            else:
                if not item.endswith('.pdf'):
                    if item[:-4] in inxml:
                        status = 'found in XML'
                    else:
                        if item.endswith('.jpg') and item.replace('.jpg', '.tif') in ' '.join(inxml):
                            # jpg was converted from a tif
                            status = ''
                        else:
                            status = 'WARNING: not found in XML'
            row['status'] = status
            r.append(row)
        return (t_header, ['files', 'status'], r)

    def affiliations_sheet_data(self):
        t_header = ['aff id', 'aff orgname', 'aff norgname', 'aff orgdiv1', 'aff orgdiv2', 'aff country', 'aff city', 'aff state', ]
        r = []
        for a in self.article.affiliations:
            row = {}
            row['aff id'] = a.id
            row['aff norgname'] = a.norgname
            row['aff orgname'] = a.orgname
            row['aff orgdiv1'] = a.orgdiv1
            row['aff orgdiv2'] = a.orgdiv2
            row['aff city'] = a.city
            row['aff state'] = a.state
            row['aff country'] = a.country
            r.append(row)
        return (t_header, ['aff xml'], r)


def package_files(path, xml_name):
    r = []
    for item in os.listdir(path):
        prefix = xml_name.replace('.xml', '')
        if item.startswith(prefix + '.') or item.startswith(prefix + '-') or item.startswith(prefix + '_'):
            if not item.endswith('.xml'):
                r.append(item)
    return r


def toc_report_data(articles, validate_order):
    toc_report_content = TOCReport(articles, validate_order).report()
    toc_f, toc_e, toc_w = html_reports.statistics_numbers(toc_report_content)
    return (toc_f, toc_e, toc_w, toc_report_content)


def get_article_report_data(org_manager, article, new_name, package_path, validate_order):
    if article.tree is None:
        sheet_data = None
        article_display_report = None
        article_validation_report = None
    else:
        article_validation = article_validations.ArticleContentValidation(org_manager, article, validate_order, False)
        sheet_data = ArticleSheetData(article, article_validation)
        article_display_report = ArticleDisplayReport(article, sheet_data, package_path, new_name)
        article_validation_report = ArticleValidationReport(article_validation)
    return (article_display_report, article_validation_report, sheet_data)


def format_report(article_display_report, article_validation_report, display_all):
    content = []

    if display_all:
        content.append(article_display_report.issue_header)

    content.append(article_display_report.article_front)
    content.append(article_validation_report.validations(not display_all))
    content.append(article_display_report.files_and_href)
    content.append(article_display_report.references_stats)
    if display_all:
        content.append(article_display_report.article_body)
        content.append(article_display_report.article_back)
        content.append(article_display_report.authors_sheet)
        content.append(article_display_report.sources_sheet)
    return html_reports.join_texts(content)


def example():
    xml_path = '/Users/robertatakenaka/Documents/vm_dados/scielo_data/serial/pab/v48n7/markup_xml/scielo_package'
    report_path = '/Users/robertatakenaka/Documents/vm_dados/scielo_data/_xpm_reports_'
    report_filenames = {v:v.replace('.xml', '') for v in os.listdir(xml_path) if v.endswith('.xml') and not 'incorre' in v }
    generate_contents_reports(xml_path, report_path, report_filenames)
    print('Reports in ' + report_path)
