
import os
import shutil
from datetime import datetime

import utils
import xml_utils
import contents_validation
import report_html

from article import Article, PersonAuthor, CorpAuthor, format_author


class TOCReport(object):

    def __init__(self, filename_and_article_list):
        self.articles = filename_and_article_list
        self.html_report = report_html.ReportHTML()

    def report(self):
        invalid = []
        equal_data = ['journal-title', 'journal id NLM', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        unique_data = ['order', 'doi', 'elocation id']
        conditional_unique_data = ['fpage-and-seq']

        toc_data = {}
        for label in equal_data + unique_data + conditional_unique_data:
            toc_data[label] = {}

        for filename, article in self.articles:
            if article is None:
                invalid.append(filename)
            else:
                art_data = article.summary()
                for label in toc_data.keys():
                    toc_data[label] = utils.add_new_value_to_index(toc_data[label], art_data[label], filename)

        r = ''
        if len(invalid) > 0:
            r += self.html_report.format_div(self.html_report.format_message('FATAL ERROR: Invalid XML files'))
            r += self.html_report.format_div(self.html_report.format_list('', 'ol', invalid))

        for label in equal_data:
            if len(toc_data[label]) > 1:
                part = self.html_report.format_message('FATAL ERROR: equal value of ' + label + ' is required for all the articles of the package')
                for found_value, xml_files in toc_data[label].items():
                    part += self.html_report.format_list('found ' + label + ' "' + found_value + '" in:', 'ul', xml_files, 'issue-problem')
                r += part

        for label in unique_data:
            if len(toc_data[label]) > 0 and len(toc_data[label]) != len(self.articles):
                part = self.html_report.format_message('FATAL ERROR: unique value of ' + label + ' is required for all the articles of the package')
                for found_value, xml_files in toc_data[label].items():
                    if len(xml_files) > 1:
                        part += self.html_report.format_list('found ' + label + ' "' + found_value + ' in:', 'ul', xml_files, 'issue-problem')
                r += part

        if not len(toc_data['fpage-and-seq']) == len(self.articles):
            result = False
            if len(toc_data['fpage-and-seq']) == 1:
                found_values = toc_data['fpage-and-seq'].keys()
                if found_values[0].isdigit():
                    if int(found_values[0]) == 0 and len(toc_data['fpage-and-seq'].values()) == len(self.articles):
                        result = True
            if not result:
                part = self.html_report.format_message('FATAL ERROR: unique value of fpage/seq is required for all the articles of the package')
                for found_value, xml_files in toc_data['fpage-and-seq'].items():
                    if len(xml_files) > 1:
                        part += self.html_report.format_list('found fpage/seq "' + found_value + ' in:', 'ul', xml_files, 'issue-problem')
                r += part
        return self.html_report.format_div(r, 'issue-messages')


class ArticleDisplayReport(object):

    def __init__(self, article, html_report, sheet_data, xml_path, xml_name, files):
        self.article = article
        self.html_report = html_report
        self.xml_name = xml_name
        self.xml_path = xml_path
        self.files = files
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

        return self.html_report.tag('h2', 'Article front') + self.html_report.format_div(r, 'article-data')

    @property
    def article_body(self):
        r = ''
        r += self.sections
        r += self.formulas
        r += self.tables
        return self.html_report.tag('h2', 'Article body') + self.html_report.format_div(r, 'article-data')

    @property
    def article_back(self):
        r = ''
        r += self.funding
        r += self.footnotes
        return self.html_report.tag('h2', 'Article back') + self.html_report.format_div(r, 'article-data')

    @property
    def files_and_href(self):
        r = ''
        r += self.html_report.tag('h2', 'Files in the package') + self.html_report.sheet(self.sheet_data.package_files(self.files))
        r += self.html_report.tag('h2', 'Files in @href') + self.html_report.sheet(self.sheet_data.hrefs(self.xml_path))
        return r

    @property
    def authors_sheet(self):
        return self.html_report.tag('h2', 'Authors') + self.html_report.sheet(self.sheet_data.authors())

    @property
    def sources_sheet(self):
        return self.html_report.tag('h2', 'Sources') + self.html_report.sheet(self.sheet_data.sources())

    def display_value_with_discret_label(self, label, value, style='', tag='p'):
        if value is None:
            value = 'None'
        return self.html_report.display_value_with_discret_label(label, value, style, tag)

    def display_titles(self):
        r = ''
        for t in self.article.titles:
            r += self.html_report.display_value_with_discret_label(t.language, t.title)
        for t in self.article.trans_titles:
            r += self.html_report.display_value_with_discret_label(t.language, t.title)
        return r

    def display_text(self, label, items):
        r = self.html_report.tag('p', label, 'label')
        for item in items:
            r += self.display_value_with_discret_label(item.language, item.text)
        return self.html_report.tag('div', r)

    @property
    def toc_section(self):
        return self.display_value_with_discret_label('toc section', self.article.toc_section, 'toc-section')

    @property
    def article_type(self):
        return self.display_value_with_discret_label('@article-type', self.article.article_type, 'article-type')

    @property
    def article_date(self):
        return self.display_value_with_discret_label('@article-date', utils.format_date(self.article.article_pub_date))

    @property
    def contrib_names(self):
        return self.html_report.format_list('authors:', 'ol', [format_author(a) for a in self.article.contrib_names])

    @property
    def contrib_collabs(self):
        r = [format_author(a) for a in self.article.contrib_collabs]
        if len(r) > 0:
            r = self.html_report.format_list('collabs', 'ul', r)
        else:
            r = self.display_value_with_discret_label('collabs', 'None')
        return r

    @property
    def abstracts(self):
        return self.display_text('abstracts', self.article.abstracts)

    @property
    def keywords(self):
        return self.html_report.format_list('keywords:', 'ol', ['(' + k['l'] + ') ' + k['k'] for k in self.article.keywords])

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
        r = self.display_value_with_discret_label('ack', self.article.ack_xml)
        r += self.display_value_with_discret_label('fn[@fn-type="funding-disclosure"]', self.article.elocation_id, 'fpage')
        return r

    @property
    def article_id_other(self):
        return self.display_value_with_discret_label('.//article-id[@pub-id-type="other"]', self.article.fn_financial_disclosure)

    @property
    def sections(self):
        _sections = ['[' + sec_id + '] ' + sec_title + ' (' + str(sec_type) + ')' for sec_id, sec_type, sec_title in self.article.article_sections]
        return self.html_report.format_list('sections:', 'ul', _sections)

    @property
    def formulas(self):
        r = self.html_report.tag('p', 'disp-formulas:', 'label')
        for item in self.article.formulas:
            r += self.html_report.tag('p', item)
        return r

    @property
    def footnotes(self):
        r = self.html_report.tag('p', 'foot notes:', 'label')
        for item in self.article.article_fn_list:
            scope, fn_xml = item
            r += self.html_report.tag('p', scope, 'label')
            r += self.html_report.tag('p', self.html_report.display_xml(fn_xml))
        return r

    @property
    def issue_header(self):
        if self.article is not None:
            r = [self.article.journal_title, self.article.journal_id_nlm_ta, self.article.issue_label, utils.format_date(self.article.issue_pub_date)]
            return self.html_report.tag('div', '\n'.join([self.html_report.tag('h5', item) for item in r if item is not None]), 'issue-data')
        else:
            return ''

    @property
    def tables(self):
        r = self.html_report.tag('p', 'Tables:', 'label')
        for t in self.article.tables:
            header = self.html_report.tag('h3', t.id)
            table_data = ''
            table_data += self.html_report.display_value_with_discret_label('label', t.label, 'label')
            table_data += self.html_report.display_value_with_discret_label('caption',  self.html_report.display_xml(t.caption), 'label')
            table_data += self.html_report.tag('p', 'table-wrap/table (xml)', 'label')
            table_data += self.html_report.tag('div', self.html_report.display_xml(t.table), 'xml')
            if t.table:
                table_data += self.html_report.tag('p', 'table-wrap/table', 'label')
                table_data += self.html_report.tag('div', t.table, 'element-table')
            if t.graphic:
                table_data += self.html_report.display_value_with_discret_label('table-wrap/graphic', t.graphic.display(self.xml_path), 'value')
            r += header + self.html_report.tag('div', table_data, 'block')
        return r

    @property
    def affiliations(self):
        r = self.html_report.tag('p', 'Affiliations:', 'label')
        for item in self.article.affiliations:
            r += self.html_report.tag('p', self.html_report.display_xml(item.xml))
        r += self.html_report.sheet(self.sheet_data.affiliations())
        return r


class ArticleValidationReport(object):

    def __init__(self, article_validation, html_report):
        self.article_validation = article_validation
        self.html_report = html_report

    def display_items(self, items):
        r = ''
        for item in items:
            r += self.display_item(item)
        return r

    def display_item(self, item):
        return self.html_report.format_message(item)

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
            cell += self.html_report.tag('td', row[0], 'td_label')
            cell += self.html_report.tag('td', row[1], 'td_status')
            style = self.html_report.message_style(row[1] + ':')
            value = row[2]
            if style == 'ok':
                if '<pre>' in value and '</pre>' in value:
                    value = self.html_report.display_xml(value)
                value = self.html_report.tag('span', value, 'value')
            cell += self.html_report.tag('td', value, 'td_message')
            r += self.html_report.tag('tr', cell, style)
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
        return self.html_report.format_div(self.html_report.tag('h2', 'Validations') + rows, 'article-messages')

    @property
    def affiliations(self):
        r = []
        for a in self.article_validation.affiliations:
            label, status, xml = a
            if label == 'xml':
                r.append((label, status, self.html_report.display_xml(xml)))
            else:
                r.append(a)
        return r

    @property
    def references(self):
        rows = ''
        for ref in self.article_validation.references:
            rows += self.html_report.tag('h3', 'Reference ' + ref.id)
            r = []
            for item in ref.evaluate():
                r.append(item)
            rows += self.validation_table(self.format_validation_data(r))
        return rows


class ArticleSheetData(object):

    def __init__(self, article, article_validation):
        self.article = article
        self.article_validation = article_validation
        self.html_report = report_html.ReportHTML()

    def authors(self, filename=None):
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

    def sources(self, filename=None):
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

    def ids(self):
        def _ids(node, scope):
            res = []
            if node is not None:
                for n in node.findall('.//*[@id]'):
                    r = {}
                    r['scope'] = scope
                    r['element'] = n.tag
                    r['ID'] = n.attrib.get('id')
                    r['xref list'] = [self.html_report.display_xml(item) for item in self.article.xref_list.get(n.attrib.get('id'), [])]
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

    def tables(self, path):
        t_header = ['ID', 'label/caption', 'table/graphic']
        r = []
        for t in self.article.tables:
            row = {}
            row['ID'] = t.graphic_parent.id
            row['label/caption'] = t.graphic_parent.label + '/' + t.graphic_parent.caption
            row['table/graphic'] = self.html_report.display_xml(t.table + t.graphic_parent.graphic.display(path))
            r.append(row)
        return (t_header, ['label/caption', 'table/graphic'], r)

    def hrefs(self, path):
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
            row['xml'] = self.html_report.display_xml(item.xml)
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
                        status = 'ERROR: not found in XML'
                else:
                    status = 'ERROR: not found in XML'
            row['status'] = status
            r.append(row)
        return (t_header, ['files', 'status'], r)

    def affiliations(self):
        t_header = ['ID', 'orgname', 'norgname', 'orgdiv1', 'orgdiv2', 'country', 'city', 'state', 'xml']
        r = []
        for a in self.article.affiliations:
            row = {}
            row['ID'] = a.id
            row['norgname'] = a.norgname
            row['orgname'] = a.orgname
            row['orgdiv1'] = a.orgdiv1
            row['orgdiv2'] = a.orgdiv2
            row['city'] = a.city
            row['state'] = a.state
            row['country'] = a.country
            row['xml'] = a.xml
            r.append(row)
        return (t_header, ['xml'], r)


def statistics(content, word):
    return len(content.split(word)) - 1


def statistics_numbers(content):
    e = statistics(content, 'ERROR')
    f = statistics(content, 'FATAL ERROR')
    e = e - f
    w = statistics(content, 'WARNING')
    return (f, e, w)


def statistics_messages(f, e, w, title=''):
    s = [('Total of fatal errors:', f), ('Total of errors:', e), ('Total of warnings:', w)]
    s = ''.join([report_html.ReportHTML().format_p_label_value(l, str(v)) for l, v in s])
    _html_report = report_html.ReportHTML()
    text = 'FATAL ERROR' if f > 0 else 'ERROR' if e > 0 else 'WARNING' if w > 0 else ''
    style = _html_report.message_style(text)
    if style == '' or style == 'ok':
        style = 'success'
    return _html_report.tag('h3', title) + _html_report.format_div(_html_report.format_div(s, style), 'statistics')


def package_files(path, xml_name):
    r = []
    for item in os.listdir(path):
        if not item.endswith('.xml'):
            prefix = xml_name.replace('.xml', '')
            if item.startswith(prefix + '.') or item.startswith(prefix + '-') or item.startswith(prefix + '_'):
                r.append(item)
    return r


def get_articles_and_filenames(package_path, xml_names):
    articles_and_filenames = []
    for new_name, xml_name in xml_names.items():
        xml_filename = package_path + '/' + new_name + '.xml'
        if os.path.isfile(xml_filename):
            xml, e = xml_utils.load_xml(package_path + '/' + new_name + '.xml')
            if xml is None:
                shutil.copyfile(xml_filename, xml_filename + '.bkp')
                xml_content = open(xml_filename, 'r').read()
                xml_content, replaced_named_ent = xml_utils.convert_entities_to_chars(xml_content)
                open(xml_filename, 'w').write(xml_content)
                open(xml_filename + '.replaced.txt', 'w').write('\n'.join(replaced_named_ent))
                xml, e = xml_utils.load_xml(xml_content)

        else:
            xml = None
        article = None if xml is None else Article(xml)
        articles_and_filenames.append((new_name, article))
    return articles_and_filenames


def toc_report(articles_and_filenames):
    toc_report_content = TOCReport(articles_and_filenames).report()
    toc_f, toc_e, toc_w = statistics_numbers(toc_report_content)
    return (toc_f, toc_e, toc_w, toc_report_content)


def generate_contents_reports(package_path, xml_names, report_path, create_toc_report=True):
    html_report = report_html.ReportHTML()

    toc_authors_sheet_data = []
    toc_sources_sheet_data = []
    authors_h = None
    authors_w = None
    sources_h = None
    sources_w = None
    issues = []
    validation_results = {}
    articles_and_filenames = get_articles_and_filenames(package_path, xml_names)
    if create_toc_report:
        toc_f, toc_e, toc_w, toc_report_content = toc_report(articles_and_filenames)
    else:
        toc_f, toc_e, toc_w, toc_report_content = (0, 0, 0, '')
    package_f, package_e, package_w = (0, 0, 0)
    for new_name, article in articles_and_filenames:
        report_name = xml_names[new_name]
        if article is None:
            content = 'FATAL ERROR: ' + new_name + ' is not valid.'
            f, e, w = statistics_numbers(content)
            write_article_report(html_report, report_path, report_name, statistics_messages(f, e, w) + content)

        else:
            article_validation = contents_validation.ArticleContentValidation(article)
            sheet_data = ArticleSheetData(article, article_validation)
            article_display_report = ArticleDisplayReport(article, html_report, sheet_data, package_path, new_name, package_files(package_path, new_name))
            article_validation_report = ArticleValidationReport(article_validation, html_report)
            content = article_report_content(article_display_report, article_validation_report)

            f, e, w = statistics_numbers(content)

            toc_report_content += statistics_messages(f, e, w, report_name)
            write_article_report(html_report, report_path, report_name, statistics_messages(f, e, w) + content)

            authors_h, authors_w, authors_data = sheet_data.authors(new_name)
            sources_h, sources_w, sources_data = sheet_data.sources(new_name)

            if not article.issue_label in issues:
                issues.append(article.issue_label)

            if create_toc_report:
                package_e += e
                package_f += f
                package_w += w
                toc_authors_sheet_data += authors_data
                toc_sources_sheet_data += sources_data

        validation_results[new_name] = ((f, e, w), article)

    if create_toc_report:
        html_report.title = 'Authors'
        html_report.body = html_report.sheet((authors_h, authors_w, toc_authors_sheet_data))
        html_report.save(report_path + '/authors.html')

        html_report.title = 'Sources'
        html_report.body = html_report.sheet((sources_h, sources_w, toc_sources_sheet_data))
        html_report.save(report_path + '/sources.html')

        html_report.save(report_path + '/toc.html', 'TOC Report', statistics_messages(toc_f, toc_e, toc_w, 'Table of Contents statistics') + statistics_messages(package_f, package_e, package_w, 'All the files statistics') + toc_report_content)
    return ((toc_f, toc_e, toc_w), (package_f, package_e, package_w), validation_results, issues)


def write_article_report(html_report, report_path, xml_name, content):
    report_name = xml_name + '.contents.html'
    if os.path.isfile(report_path + '/' + report_name):
        os.unlink(report_path + '/' + report_name)
    html_report.title = ['Report of contents validations required by SciELO', xml_name]
    html_report.body = content
    html_report.save(report_path + '/' + report_name)


def article_report_content(data_display, data_validation):
    content = ''
    content += data_display.summary
    content += data_display.article_back
    content += data_display.files_and_href
    content += data_display.article_body
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
