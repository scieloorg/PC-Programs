# coding=utf-8
import os
import shutil
from datetime import datetime

import xml_utils
import article_utils
import article_validations
import reports

from article import Article, PersonAuthor, CorpAuthor, format_author


html_report = reports.ReportHTML()


def get_valid_xml(xml_filename):
    xml, e = xml_utils.load_xml(xml_filename)
    if xml is None:
        shutil.copyfile(xml_filename, xml_filename + '.bkp')
        xml_content = open(xml_filename, 'r').read()
        xml_content, replaced_named_ent = xml_utils.convert_entities_to_chars(xml_content)
        open(xml_filename, 'w').write(xml_content)
        open(xml_filename + '.replaced.txt', 'w').write('\n'.join(replaced_named_ent))
        xml, e = xml_utils.load_xml(xml_content)
    return xml


class TOCReport(object):

    def __init__(self, articles, validate_order):
        self.articles = articles
        self.validate_order = validate_order

    def report(self):
        invalid = []
        equal_data = ['journal-title', 'journal id NLM', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        if self.validate_order:
            unique_data = ['order', 'doi', 'elocation id']
        else:
            unique_data = ['doi', 'elocation id']
        conditional_unique_data = ['fpage-and-seq']

        toc_data = {}
        for label in equal_data + unique_data + conditional_unique_data:
            toc_data[label] = {}

        for xml_name, article in self.articles.items():
            if article is None:
                invalid.append(xml_name)
            else:
                art_data = article.summary()
                for label in toc_data.keys():
                    toc_data[label] = article_utils.add_new_value_to_index(toc_data[label], art_data[label], xml_name)

        r = ''
        if len(invalid) > 0:
            r += html_report.tag('div', html_report.format_message('FATAL ERROR: Invalid XML files'))
            r += html_report.tag('div', html_report.format_list('', 'ol', invalid))

        for label in equal_data:
            if len(toc_data[label]) > 1:
                part = html_report.format_message('FATAL ERROR: equal value of ' + label + ' is required for all the articles of the package')
                for found_value, xml_files in toc_data[label].items():
                    part += html_report.format_list('found ' + label + ' "' + found_value + '" in:', 'ul', xml_files, 'issue-problem')
                r += part

        for label in unique_data:
            if len(toc_data[label]) > 0 and len(toc_data[label]) != len(self.articles):
                part = html_report.format_message('FATAL ERROR: unique value of ' + label + ' is required for all the articles of the package')
                for found_value, xml_files in toc_data[label].items():
                    if len(xml_files) > 1:
                        part += html_report.format_list('found ' + label + ' "' + found_value + ' in:', 'ul', xml_files, 'issue-problem')
                r += part

        if not len(toc_data['fpage-and-seq']) == len(self.articles):
            result = False
            if len(toc_data['fpage-and-seq']) == 1:
                found_values = toc_data['fpage-and-seq'].keys()
                if found_values[0].isdigit():
                    if int(found_values[0]) == 0 and len(toc_data['fpage-and-seq'].values()) == len(self.articles):
                        result = True
            if not result:
                part = html_report.format_message('FATAL ERROR: unique value of fpage/seq is required for all the articles of the package')
                for found_value, xml_files in toc_data['fpage-and-seq'].items():
                    if len(xml_files) > 1:
                        part += html_report.format_list('found fpage/seq "' + found_value + ' in:', 'ul', xml_files, 'issue-problem')
                r += part
        return html_report.tag('div', r, 'issue-messages')


class ArticleDisplayReport(object):

    def __init__(self, article, sheet_data, xml_path, xml_name):
        self.article = article
        self.xml_name = xml_name
        self.xml_path = xml_path
        self.files = package_files(xml_path, xml_name)
        self.sheet_data = sheet_data

    @property
    def summary(self):
        return self.issue_header + self.article_front

    @property
    def article_front(self):
        r = self.xml_name + ' is invalid.'
        if self.article is not None:
            r = ''
            r += self.toc_section
            r += self.article_type
            r += self.display_titles()
            r += self.doi
            r += self.article_id_other
            r += self.order
            r += self.fpage
            r += self.fpage_seq
            r += self.elocation_id
            r += self.article_date
            r += self.contrib_names
            r += self.contrib_collabs
            r += self.affiliations
            r += self.abstracts
            r += self.keywords

        return html_report.tag('h2', 'Article front') + html_report.tag('div', r, 'article-data')

    @property
    def article_body(self):
        r = ''
        r += self.sections
        r += self.formulas
        r += self.tables
        return html_report.tag('h2', 'Article body') + html_report.tag('div', r, 'article-data')

    @property
    def article_back(self):
        r = ''
        r += self.funding
        r += self.footnotes
        return html_report.tag('h2', 'Article back') + html_report.tag('div', r, 'article-data')

    @property
    def files_and_href(self):
        r = ''
        r += html_report.tag('h2', 'Files in the package') + html_report.sheet(self.sheet_data.package_files(self.files))
        r += html_report.tag('h2', 'Files in @href') + html_report.sheet(self.sheet_data.hrefs_sheet_data(self.xml_path))
        return r

    @property
    def authors_sheet(self):
        return html_report.tag('h2', 'Authors') + html_report.sheet(self.sheet_data.authors_sheet_data())

    @property
    def sources_sheet(self):
        return html_report.tag('h2', 'Sources') + html_report.sheet(self.sheet_data.sources_sheet_data())

    def display_value_with_discret_label(self, label, value, style='', tag='p'):
        if value is None:
            value = 'None'
        return html_report.display_value_with_discret_label(label, value, style, tag)

    def display_titles(self):
        r = ''
        for title in self.article.titles:
            r += html_report.display_value_with_discret_label(title.language, title.title)
        for title in self.article.trans_titles:
            r += html_report.display_value_with_discret_label(title.language, title.title)
        return r

    def display_text(self, label, items):
        r = html_report.tag('p', label, 'label')
        for item in items:
            r += self.display_value_with_discret_label(item.language, item.text)
        return html_report.tag('div', r)

    @property
    def toc_section(self):
        return self.display_value_with_discret_label('toc section', self.article.toc_section, 'toc-section')

    @property
    def article_type(self):
        return self.display_value_with_discret_label('@article-type', self.article.article_type, 'article-type')

    @property
    def article_date(self):
        return self.display_value_with_discret_label('@article-date', article_utils.format_date(self.article.article_pub_date))

    @property
    def contrib_names(self):
        return html_report.format_list('authors:', 'ol', [format_author(a) for a in self.article.contrib_names])

    @property
    def contrib_collabs(self):
        r = [format_author(a) for a in self.article.contrib_collabs]
        if len(r) > 0:
            r = html_report.format_list('collabs', 'ul', r)
        else:
            r = self.display_value_with_discret_label('collabs', 'None')
        return r

    @property
    def abstracts(self):
        return self.display_text('abstracts', self.article.abstracts)

    @property
    def keywords(self):
        return html_report.format_list('keywords:', 'ol', ['(' + k['l'] + ') ' + k['k'] for k in self.article.keywords])

    @property
    def order(self):
        return self.display_value_with_discret_label('order', self.article.order, 'order')

    @property
    def doi(self):
        return self.display_value_with_discret_label('doi', self.article.doi, 'doi')

    @property
    def fpage(self):
        return self.display_value_with_discret_label('pages', self.article.fpage + '-' + self.article.lpage, 'fpage')

    @property
    def fpage_seq(self):
        return self.display_value_with_discret_label('fpage/@seq', self.article.fpage_seq, 'fpage')

    @property
    def elocation_id(self):
        return self.display_value_with_discret_label('elocation-id', self.article.elocation_id, 'fpage')

    @property
    def funding(self):
        r = self.display_value_with_discret_label('ack', html_report.display_xml(self.article.ack_xml))
        r += self.display_value_with_discret_label('fn[@fn-type="financial-disclosure"]', self.article.financial_disclosure, 'fpage')
        return r

    @property
    def article_id_other(self):
        return self.display_value_with_discret_label('.//article-id[@pub-id-type="other"]', self.article.article_id_other)

    @property
    def sections(self):
        _sections = ['[' + sec_id + '] ' + sec_title + ' (' + str(sec_type) + ')' for sec_id, sec_type, sec_title in self.article.article_sections]
        return html_report.format_list('sections:', 'ul', _sections)

    @property
    def formulas(self):
        r = html_report.tag('p', 'disp-formulas:', 'label')
        for item in self.article.formulas:
            r += html_report.tag('p', item)
        return r

    @property
    def footnotes(self):
        r = html_report.tag('p', 'foot notes:', 'label')
        for item in self.article.article_fn_list:
            scope, fn_xml = item
            r += html_report.tag('p', scope, 'label')
            r += html_report.tag('p', html_report.display_xml(fn_xml))
        return r

    @property
    def issue_header(self):
        if self.article is not None:
            r = [self.article.journal_title, self.article.journal_id_nlm_ta, self.article.issue_label, article_utils.format_date(self.article.issue_pub_date)]
            return html_report.tag('div', '\n'.join([html_report.tag('h5', item) for item in r if item is not None]), 'issue-data')
        else:
            return ''

    @property
    def tables(self):
        r = html_report.tag('p', 'Tables:', 'label')
        for t in self.article.tables:
            header = html_report.tag('h3', t.id)
            table_data = ''
            table_data += html_report.display_value_with_discret_label('label', t.label, 'label')
            table_data += html_report.display_value_with_discret_label('caption',  html_report.display_xml(t.caption), 'label')
            table_data += html_report.tag('p', 'table-wrap/table (xml)', 'label')
            table_data += html_report.tag('div', html_report.display_xml(t.table), 'xml')
            if t.table:
                table_data += html_report.tag('p', 'table-wrap/table', 'label')
                table_data += html_report.tag('div', t.table, 'element-table')
            if t.graphic:
                table_data += html_report.display_value_with_discret_label('table-wrap/graphic', t.graphic.display(self.xml_path), 'value')
            r += header + html_report.tag('div', table_data, 'block')
        return r

    @property
    def affiliations(self):
        r = html_report.tag('p', 'Affiliations:', 'label')
        for item in self.article.affiliations:
            r += html_report.tag('p', html_report.display_xml(item.xml))
        r += html_report.sheet(self.sheet_data.affiliations_sheet_data())
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
        return html_report.format_message(item)

    def validation_table(self, content):
        r = '<p>'
        r += '<table class="validation">'
        r += '<thead>'
        r += '<tr>'
        for label in ['label', 'status', 'message/value']:
            r += '<th class="th">' + label + '</th>'
        r += '</tr></thead>'
        r += '<tbody>' + content + '</tbody>'
        r += '</table></p>'
        return r

    def format_validation_data(self, table_data):
        r = ''
        for row in table_data:
            cell = ''
            cell += html_report.tag('td', row[0], 'td_label')
            cell += html_report.tag('td', row[1], 'td_status')
            style = html_report.message_style(row[1] + ':')
            value = row[2]
            if style == 'ok':
                if '<pre>' in value and '</pre>' in value:
                    value = html_report.display_xml(value)
                value = html_report.tag('span', value, 'value')
            cell += html_report.tag('td', value, 'td_message')
            r += html_report.tag('tr', cell, style)
        return r

    def report(self):
        r = ''
        rows = ''
        items = [self.article_validation.journal_title,
                    self.article_validation.publisher_name,
                    self.article_validation.journal_id,
                    self.article_validation.journal_id_nlm_ta,
                    self.article_validation.journal_issns,
                    self.article_validation.issue_label,
                    self.article_validation.article_type,
                    self.article_validation.toc_section,
                    self.article_validation.order,
                    self.article_validation.doi,
                    self.article_validation.fpage,
                    self.article_validation.language,
                    self.article_validation.total_of_pages,
                    self.article_validation.total_of_equations,
                    self.article_validation.total_of_tables,
                    self.article_validation.total_of_figures,
                    self.article_validation.total_of_references,
                    ]
        rows += self.format_validation_data(items)
        rows += self.format_validation_data(self.article_validation.titles)
        rows += self.format_validation_data(self.article_validation.trans_titles)
        rows += self.format_validation_data(self.article_validation.contrib_names)
        rows += self.format_validation_data(self.article_validation.contrib_collabs)
        rows += self.format_validation_data(self.affiliations)
        rows += self.format_validation_data(self.article_validation.funding)
        items = [
                    self.article_validation.license,
                    ]
        rows += self.format_validation_data(items)
        rows += self.format_validation_data(self.article_validation.history)
        rows += self.format_validation_data(self.article_validation.abstracts)
        rows += self.format_validation_data(self.article_validation.keywords)
        rows = self.validation_table(rows)
        rows += self.references
        return html_report.tag('div', html_report.tag('h2', 'Validations') + rows, 'article-messages')

    @property
    def affiliations(self):
        r = []
        for a in self.article_validation.affiliations:
            label, status, xml = a
            if label == 'xml':
                r.append((label, status, html_report.display_xml(xml)))
            else:
                r.append(a)
        return r

    @property
    def references(self):
        rows = ''
        for ref in self.article_validation.references:
            rows += html_report.tag('h3', 'Reference ' + ref.id)
            r = []
            for item in ref.evaluate():
                r.append(item)
            rows += self.validation_table(self.format_validation_data(r))
        return rows


class ArticleSheetData(object):

    def __init__(self, article, article_validation):
        self.article = article
        self.article_validation = article_validation

    def authors_sheet_data(self, filename=None):
        r = []
        t_header = ['xref', 'given-names', 'surname', 'suffix', 'prefix', 'collab', 'role']
        if not filename is None:
            t_header = ['filename', 'scope'] + t_header
        for a in self.article.contrib_names:
            row = {}
            row['scope'] = 'article meta'
            row['filename'] = filename
            row['xref'] = ' '.join(a.xref)
            row['given-names'] = a.fname
            row['surname'] = a.surname
            row['suffix'] = a.suffix
            row['prefix'] = a.prefix
            row['role'] = a.role
            r.append(row)

        for a in self.article.contrib_collabs:
            row = {}
            row['scope'] = 'article meta'
            row['filename'] = filename
            row['collab'] = a.collab
            row['role'] = a.role
            r.append(row)

        for ref in self.article.references:
            for item in ref.authors_list:
                row = {}
                row['scope'] = ref.id
                row['filename'] = filename
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

    def ids_sheet_data(self):
        def _ids(node, scope):
            res = []
            if node is not None:
                for n in node.findall('.//*[@id]'):
                    r = {}
                    r['scope'] = scope
                    r['element'] = n.tag
                    r['ID'] = n.attrib.get('id')
                    r['xref list'] = [html_report.display_xml(item) for item in self.article.xref_list.get(n.attrib.get('id'), [])]
                    res.append(r)
            return res

        r = []
        t_header = ['scope', 'ID', 'element', 'xref list']
        r += _ids(self.article.article_meta, 'article')
        r += _ids(self.article.body, 'article')
        r += _ids(self.article.back, 'article')

        for item in self.article.subarticles:
            r += _ids(item, 'sub-article ' + item.find('.').attrib.get('id', ''))
        for item in self.article.responses:
            r += _ids(item, 'response ' + item.find('.').attrib.get('id', ''))

        return (t_header, ['xref list'], r)

    def tables_sheet_data(self, path):
        t_header = ['ID', 'label/caption', 'table/graphic']
        r = []
        for t in self.article.tables:
            row = {}
            row['ID'] = t.graphic_parent.id
            row['label/caption'] = t.graphic_parent.label + '/' + t.graphic_parent.caption
            row['table/graphic'] = html_report.display_xml(t.table + t.graphic_parent.graphic.display(path))
            r.append(row)
        return (t_header, ['label/caption', 'table/graphic'], r)

    def hrefs_sheet_data(self, path):
        t_header = ['href', 'display', 'xml']
        r = []

        for item in self.article.href_files:
            row = {}
            row['href'] = item.src
            msg = ''
            if not ':' in item.src:
                if not os.path.isfile(path + '/' + item.src) and not os.path.isfile(path + '/' + item.src + '.jpg'):
                    msg = 'ERROR: ' + item.src + ' not found in package'
            row['display'] = item.display(path) + msg
            row['xml'] = html_report.display_xml(item.xml)
            r.append(row)
        return (t_header, ['display', 'xml'], r)

    def package_files(self, files):
        t_header = ['files', 'status']
        r = []
        inxml = [item.src for item in self.article.hrefs]

        for item in files:
            row = {}
            row['files'] = item
            if item in inxml:
                status = 'found in XML'
            else:
                if item.endswith('.jpg'):
                    if item[:-4] in inxml:
                        status = 'found in XML'
                    else:
                        status = 'WARNING: not found in XML'
                else:
                    status = 'WARNING: not found in XML'
            row['status'] = status
            r.append(row)
        return (t_header, ['files', 'status'], r)

    def affiliations_sheet_data(self):
        t_header = ['aff id', 'aff orgname', 'aff norgname', 'aff orgdiv1', 'aff orgdiv2', 'aff country', 'aff city', 'aff state', 'aff xml']
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
            row['aff xml'] = a.xml
            r.append(row)
        return (t_header, ['aff xml'], r)


def package_files(path, xml_name):
    r = []
    for item in os.listdir(path):
        if not item.endswith('.xml'):
            prefix = xml_name.replace('.xml', '')
            if item.startswith(prefix + '.') or item.startswith(prefix + '-') or item.startswith(prefix + '_'):
                r.append(item)
    return r


def toc_report(articles_and_filenames, validate_order):
    toc_report_content = TOCReport(articles_and_filenames, validate_order).report()
    toc_f, toc_e, toc_w = reports.statistics_numbers(toc_report_content)
    return (toc_f, toc_e, toc_w, toc_report_content)


def _validate_article_data(article, new_name, package_path, validate_order):
    if article is None:
        content = 'FATAL ERROR: Unable to get data of ' + new_name + '.'
        sheet_data = None
    else:
        article_validation = article_validations.ArticleContentValidation(article, validate_order)
        sheet_data = ArticleSheetData(article, article_validation)
        article_display_report = ArticleDisplayReport(article, sheet_data, package_path, new_name)
        article_validation_report = ArticleValidationReport(article_validation)
        content = article_report_content(article_display_report, article_validation_report)

    return (content, sheet_data)


def validate_article_data(article, new_name, package_path, report_filename, validate_order):
    content, sheet_data = _validate_article_data(article, new_name, package_path, validate_order)
    f, e, w = reports.statistics_numbers(content)
    stats = html_report.statistics_messages(f, e, w, '')

    html_report.title = ['Report of data validations required by SciELO ', new_name]
    html_report.body = stats + content
    html_report.save(report_filename)
    return (f, e, w, sheet_data)


def article_report_content(data_display, data_validation):
    content = ''
    content += data_display.summary
    content += data_display.article_back
    content += data_display.article_body
    content += data_display.files_and_href
    content += data_validation.report()
    content += data_display.authors_sheet
    content += data_display.sources_sheet
    return content


def example():
    xml_path = '/Users/robertatakenaka/Documents/vm_dados/scielo_data/serial/pab/v48n7/markup_xml/scielo_package'
    report_path = '/Users/robertatakenaka/Documents/vm_dados/scielo_data/_xpm_reports_'
    report_filenames = {v:v.replace('.xml', '') for v in os.listdir(xml_path) if v.endswith('.xml') and not 'incorre' in v }
    generate_contents_reports(xml_path, report_path, report_filenames)
    print('Reports in ' + report_path)
