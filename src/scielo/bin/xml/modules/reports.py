
import os
from datetime import datetime

import utils
import xml_utils
import content_validation

from article import Article, PersonAuthor, CorpAuthor, format_author


def report_date():
    procdate = datetime.now().isoformat()
    return procdate[0:10] + ' ' + procdate[11:19]


class TOCReport(object):

    def __init__(self, filename_and_article_list):
        self.articles = filename_and_article_list
        self.html_page = HTMLPage()

    def report(self):
        invalid = []
        equal_data = ['journal-title', 'journal id NLM', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        unique_data = ['order', 'doi', 'fpage', 'fpage seq', 'elocation id']

        toc_data = {}
        for label in equal_data + unique_data:
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
            r += self.html_page.format_div(self.html_page.format_message('ERROR: Invalid XML files'))
            r += self.html_page.format_div(self.html_page.format_list('', 'ol', invalid))

        for label in equal_data:
            if len(toc_data[label]) != 1:
                part = self.html_page.format_message('ERROR: equal value of ' + label + ' is required for all the articles')
                for k, v in toc_data[label].items():
                    part += self.html_page.format_list(k, 'ul', v)
                r += self.html_page.format_div(part)

        for label in unique_data:
            if len(toc_data[label]) > 0 and len(toc_data[label]) != len(self.articles):
                part = self.html_page.format_message('ERROR: unique value of ' + label + ' is required for all the articles')
                for k, v in toc_data[label].items():
                    if len(v) > 1:
                        part += self.html_page.format_list(k, 'ul', v)
                r += self.html_page.format_div(part)
        return r


class ArticleDisplay(object):

    def __init__(self, article, html_page):
        self.article = article
        self.html_page = html_page

    def article_summary(self):
        r = ''
        r += self.toc_section
        r += self.display_titles()
        r += self.contrib_names
        r += self.contrib_collabs
        r += self.abstracts
        r += self.keywords
        r += self.order
        r += self.doi
        r += self.fpage
        r += self.fpage_seq
        r += self.elocation_id
        return r

    def display_p(self, label, value):
        return self.html_page.format_p(self.html_page.display_label_value(label, value))

    def display_titles(self):
        r = ''
        for t in self.article.title:
            r += self.display_p(t.language, t.title)
        for t in self.article.trans_titles:
            r += self.display_p(t.language, t.title)
        return r

    def display_text(self, label, items):
        r = self.html_page.format_label(label)
        for item in items:
            r += self.display_p(item.language, item.text)
        return r

    @property
    def toc_section(self):
        return self.display_p('toc section:', self.article.toc_section)

    @property
    def contrib_names(self):
        return self.display_p('pers authors:', '; '.join([format_author(a) for a in self.article.contrib_names]))

    @property
    def contrib_collabs(self):
        return self.display_p('corp authors:', '; '.join([a for a in self.article.contrib_collabs]))

    @property
    def abstracts(self):
        return self.display_text('abstracts', self.article.abstracts)

    @property
    def keywords(self):
        return self.html_page.format_list('keywords:', 'ul', self.article.keywords)

    @property
    def order(self):
        return self.display_p('order:', self.article.order)

    @property
    def doi(self):
        return self.display_p('doi:', self.article.doi)

    @property
    def fpage(self):
        return self.display_p('fpage:', self.article.fpage)

    @property
    def fpage_seq(self):
        return self.display_p('fpage_seq:', self.article.fpage_seq)

    @property
    def elocation_id(self):
        return self.display_p('elocation_id:', self.article.elocation_id)

    def issue_header(self):
        r = [self.article.journal_title, self.article.journal_id_nlm_ta, self.article.issue_label, utils.format_date(self.article.issue_pub_date)]
        return '\n'.join([self.display_p('', item) for item in r if item is not None])


class ArticleReport(object):

    def __init__(self, article_validation, html_page):
        self.article_validation = article_validation
        self.html_page = html_page

    def report(self):
        r = ''
        items = [self.article_validation.journal_title, 
                    self.article_validation.publisher_name,
                    self.article_validation.journal_id,
                    self.article_validation.journal_id_nlm_ta,
                    self.article_validation.journal_issns,
                    self.article_validation.issue_label,
                    self.article_validation.toc_section,
                    self.article_validation.order,
                    self.article_validation.doi,
                    self.article_validation.fpage,
                    self.article_validation.article_type,
                    self.article_validation.language
                    ]

        for item in items:
            r += self.html_page.format_message(item)

        r += self.titles
        r += self.contrib_names
        r += '; '.join([a.collab for a in self.contrib_collabs])

        r += self.affiliations

        items = [self.article_validation.funding,
                    self.article_validation.license,
                    self.article_validation.history,
                    ]

        for item in items:
            r += self.html_page.format_message(item)

        items = [self.abstracts,
                 self.keywords]
        for item in items:
            r += self.report_items(item)

        r += self.references

    def report_items(self, items):
        r = ''
        for item in items:
            r += self.html_page.format_message(item)
        return r

    @property
    def titles(self):
        r = ''
        r += self.report_items(self.article_validation.titles)
        r += self.report_items(self.article_validation.trans_titles)
        return r

    @property
    def contrib_names(self):
        r = ''
        for item in self.article_validation.contrib_names:
            r += self.html_page.format_message(item.surname)
            r += self.html_page.format_message(item.fname)
        return r

    @property
    def affiliations(self):
        r = ''
        for item in self.article_validation.affiliations:
            r += self.html_page.format_xml(item.xml)
            r += self.html_page.format_message(item.original)
            r += self.html_page.format_message(item.norgname)
            r += self.html_page.format_message(item.orgname)
            r += self.html_page.format_message(item.country)
        return r

    @property
    def funding(self):
        return self.report_item(self.article_validation.funding)

    @property
    def license(self):
        return self.report_item(self.article_validation.license)

    @property
    def history(self):
        return self.report_item(self.article_validation.history)

    @property
    def abstracts(self):
        return self.report_item(self.article_validation.abstracts)

    @property
    def keywords(self):
        return self.report_item(self.article_validation.keywords)

    @property
    def references(self):
        return self.report_item(self.article_validation.references)


class HTMLPage(object):

    def __init__(self):
        self.title = ''
        self.body = ''

    def html(self):
        s = ''
        s += '<html>'
        s += '<head>'
        s += '<meta charset="utf-8"/><title>' + self.title + '</title>'
        s += self.styles()
        s += '</head>'
        s += '<body>'
        s += '<p class="time">' + report_date() + '</p>'
        s += self.body_section('h1', self.title, self.body)
        s += '</body>'
        s += '</html>'

        return s

    def styles(self):
        return '<style>' + open('./report.css', 'r').read() + '</style>'

    def body_section(self, style, title, content):
        return '<' + style + '>' + title + '</' + style + '>' + content

    def sheet(self, table_header_and_data, filename=None):
        table_header, table_data = table_header_and_data
        r = '<table>'
        r += '<tr>'
        if filename is not None:
            r += '<th></th>'
        for label in table_header:
            r += '<th>' + label + '</th>'
        r += '</tr>'
        for row in table_data:
            r += '<tr>'
            if filename is not None:
                r += '<td>' + filename + '</td>'

            for label in table_header:
                r += '<td>' + self.format_cell(row.get(label), not label in ['filename', 'scope']) + '</td>'
            r += '</tr>'
        r += '</table>'
        return r

    def format_html(self, value):
        return ''.join([self.format_p(c) for c in value.split('\n')])

    def format_p(self, value):
        if '<p' in value:
            tag = 'div'
        else:
            tag = 'p'
        return '<' + tag + '>' + value + '</' + tag + '>'

    def format_xml(self, value):
        return '<pre>' + value.replace('<', '&lt;').replace('>', '&gt;') + '</pre>'

    def format_message(self, value):
        if '<p' in value:
            tag = 'div'
        else:
            tag = 'p'
        return '<' + tag + self.css_class(value) + '>' + value + '</' + tag + '>'

    def css_class(self, value):
        r = ''
        if 'ERROR' in value:
            r = 'error'
        if 'WARNING' in value:
            r = 'warning'
        if r != '':
            r = ' class="' + r + '"'
        return r

    def format_div(self, content):
        return '<div>' + content + '</div>'

    def format_list(self, label, list_type, list_items):
        r = self.format_label(label)
        r += '<p>'
        r += '<' + list_type + '>'
        if isinstance(list_items, dict):
            r += ''.join(['<li>' + self.display_label_value(k, v) + '</li>' for k, v in list_items.items()])
        elif isinstance(list_items, list):
            for item in list_items:
                if isinstance(item, dict):
                    for k, v in item.items():
                        r += '<li>' + self.display_label_value(k, v) + '</li>'
                else:
                    r += ''.join(['<li>' + item + '</li>' for item in list_items])
        r += '</' + list_type + '></p>'
        return r

    def format_cell(self, value, is_data=True):
        r = '-'
        if value is None:
            r = '-'
        elif isinstance(value, str):
            r = value
        elif isinstance(value, dict):
            r += '<ul>'
            for k, v in value.items():
                if isinstance(v, list):
                    r += '<li>' + k + ': ' + ', '.join(v) + ';</li>'
                else:
                    r += '<li>' + utils.display_label_value(k, v) + ';</li>'
            r += '</ul>'
        if is_data:
            style = self.css_class(r)
            if style == '':
                style = ' class="ok"'
            r = '<span' + style + '>' + r + '</span>'
        return r

    def save(self, filename, title=None, body=None):
        if title is not None:
            self.title = title
        if body is not None:
            self.body = body
        f = open(filename, 'w')
        r = self.html()
        if isinstance(r, unicode):
            r = r.encode('utf-8')
        f.write(r)
        f.close()

    def format_label(self, label):
        return '<span class="label">' + label + '</span>'

    def display_label_value(self, label, value):
        return self.format_label(label) + value + '\n' if value is not None else 'None\n'

    def display_attributes(self, label, attributes):
        r = []
        for key, value in attributes.items():
            if value is list:
                value = '; '.join(value)
            r.append(display_label_value(key, value))
        return label + '\n' + '\n'.join(r) + '\n'

    def display_items_with_attributes(self, label, items_with_attributes):
        r = label + ': ' + '\n'
        for item_name, item_values in items_with_attributes.items():
            r += display_label_values_with_attributes(item_name, item_values)
        return r + '\n'

    def display_label_values_with_attributes(self, label, values_with_attributes):
        return label + ': ' + '\n' + '\n'.join([display_attributes('=>', item) for item in values_with_attributes]) + '\n'

    def conditional_required(self, label, value):
        return display_label_value(label, value) if value is not None else 'WARNING: Required ' + label + ', if exists. '

    def required(self, label, value):
        return display_label_value(label, value) if value is not None else 'ERROR: Required ' + label + '. '

    def required_one(self, label, value):
        return display_attributes(label, value) if value is not None else 'ERROR: Required ' + label + '. '

    def expected_values(self, label, value, expected):
        return display_label_value(label, value) if value in expected else 'ERROR: ' + value + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected)

    def add_new_value_to_index(self, dict_key_and_values, key, value):
        print(key)
        if key is not None:
            if not key in dict_key_and_values.keys():
                dict_key_and_values[key] = []
            dict_key_and_values[key].append(value)
        return dict_key_and_values


class ArticleSheetData(object):

    def __init__(self, article):
        self.article = article

    def authors(self, filename=None):
        r = []
        t_header = ['xref', 'given-names', 'surname', 'suffix', 'prefix', 'collab', ]
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
            r.append(row)

        for a in self.article.contrib_collabs:
            row = {}
            row['scope'] = 'article meta'
            row['filename'] = filename
            row['collab'] = a.collab
            r.append(row)

        for ref in self.article.references:
            for grp in ref.person_groups:
                for item in grp:
                    row = {}
                    row['scope'] = ref.id
                    row['filename'] = filename
                    if isinstance(item, PersonAuthor):
                        row['given-names'] = item.fname
                        row['surname'] = item.surname
                        row['suffix'] = item.suffix
                        row['prefix'] = item.prefix
                    elif isinstance(item, CorpAuthor):
                        row['collab'] = item.collab
                    else:
                        print(type(item))
                    r.append(row)
        return (t_header, r)

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
        return (t_header, r)

    def ids(self):
        def _ids(node, scope):
            res = []
            if node is not None:
                for n in node.findall('.//*[@id]'):
                    r = {}
                    r['scope'] = scope
                    r['element'] = n.tag
                    r['ID'] = n.attrib.get('id')
                    res.append(r)
            return res

        r = []
        t_header = ['scope', 'ID', 'element']
        r += _ids(self.article.article_meta, 'article')
        r += _ids(self.article.body, 'article')
        r += _ids(self.article.back, 'article')

        for item in self.article.subarticles:
            r += _ids(item, 'sub-article ' + item.find('.').attrib.get('id', ''))
        for item in self.article.responses:
            r += _ids(item, 'response ' + item.find('.').attrib.get('id', ''))

        return (t_header, r)

    def tables(self):
        t_header = ['ID', 'label', 'caption', 'table', ]
        r = []
        for t in self.article.tree.findall('.//*[table]'):
            row = {}
            row['ID'] = t.attrib.get('id')
            row['label'] = t.findtext('.//label')
            row['caption'] = t.findtext('.//caption')

            table = xml_utils.node_text(t.find('./table'))
            if table is None:
                table = ''

            graphic = xml_utils.node_text(t.find('./graphic'))
            if graphic is None:
                graphic = ''
            row['table'] = table + graphic
            r.append(row)
        return (t_header, r)

    def hrefs(self, path=''):
        t_header = ['ID', 'Parent', 'Element', 'href', 'label', 'caption', ]
        r = []
        for parent in self.article.tree.findall('.//*[@{http://www.w3.org/1999/xlink}href]/..'):
            for elem in parent.findall('.//*[@{http://www.w3.org/1999/xlink}href]'):
                href = elem.attrib.get('{http://www.w3.org/1999/xlink}href')
                if ':' in href:
                    row = {}
                    row['Parent'] = parent.tag
                    row['Parent ID'] = parent.attrib.get('id', '')
                    row['label'] = parent.findtext('label')
                    row['caption'] = parent.findtext('caption')
                    row['Element'] = elem.tag
                    if elem.tag == 'graphic':
                        row['href'] = '<img src="' + path + href + '"/>'
                    else:
                        row['href'] = href
                    r.append(row)
        return (t_header, r)

    def affiliations(self):
        t_header = ['ID', 'data']
        r = []
        for a in self.article.affiliations:
            row = {}
            row['ID'] = a.id
            data = {}
            data['ordered'] = ['original', 'orgname', 'norgname', 'orgdiv1', 'orgdiv2', 'orgdiv3', 'orgdiv2', 'city', 'state', 'country', 'xml']
            data['original'] = a.original
            data['norgname'] = a.norgname
            data['orgname'] = a.orgname
            data['orgdiv1'] = a.orgdiv1
            data['orgdiv2'] = a.orgdiv2
            data['orgdiv3'] = a.orgdiv3
            data['city'] = a.city
            data['state'] = a.state
            data['country'] = a.country
            data['xml'] = a.xml
            row['data'] = data
            r.append(row)
        return (t_header, r)


def generate_package_reports(xml_path, report_path, report_filenames):
    report = HTMLPage()

    articles_and_filenames = []
    for xml_name in os.listdir(xml_path):
        if not 'incorrect' in xml_name and xml_name.endswith('.xml'):
            tree = xml_utils.load_xml(xml_path + '/' + xml_name)
            article = Article(tree)
            articles_and_filenames.append((xml_name, article))

    toc_validation = TOCReport(articles_and_filenames).report()
    toc_report_content = toc_validation

    authors_sheet_data = ''
    sources_sheet_data = ''

    if not os.path.isdir(report_path):
        os.makedirs(report_path)

    for xml_name, article in articles_and_filenames:

        report_name = report_filenames[xml_name] + '.contents.html'
        article_validation = content_validation.ArticleContentValidation(article)
        data = ArticleSheetData(article_validation)
        display_data = ArticleDisplay(article, report)
        article_report = ArticleReport(article_validation, report)

        authors_data = report.sheet(data.authors(xml_name))
        sources_data = report.sheet(data.sources(xml_name))

        authors_sheet_data += authors_data
        sources_sheet_data += sources_data

        content = ''
        article_summary = display_data.issue_header()
        article_summary += display_data.article_summary()
        toc_report_content += article_summary

        content += article_summary
        content += toc_validation
        content += article_report.report()

        content += report.body_section('h1', 'Authors', authors_data)
        content += report.body_section('h1', 'Affiliations', report.sheet(data.affiliations()))
        content += report.body_section('h1', 'IDs', report.sheet(data.ids()))
        content += report.body_section('h1', 'href', report.sheet(data.hrefs()))
        content += report.body_section('h1', 'Tables', report.sheet(data.tables()))
        content += report.body_section('h1', 'Sources', sources_data)

        report.title = xml_name + ' - ' + report_date()
        report.body = report.body_section('title', report.title, content)
        report.save(report_path + '/' + report_name)

    report.title = 'Authors'
    report.body = authors_sheet_data
    report.save(report_path + '/authors.html')

    report.title = 'Sources'
    report.body = sources_sheet_data
    report.save(report_path + '/sources.html')

    report.save(report_path + '/toc.html', 'TOC Report', toc_report_content)

xml_path = '/Users/robertatakenaka/Documents/vm_dados/scielo_data/serial/pab/v48n7/markup_xml/scielo_package'
report_path = '/Users/robertatakenaka/Documents/_xpm_reports_'
report_filenames = {v:v.replace('.xml', '') for v in os.listdir(xml_path) if v.endswith('.xml') and not 'incorre' in v }
generate_package_reports(xml_path, report_path, report_filenames)
print('Reports in ' + report_path)
