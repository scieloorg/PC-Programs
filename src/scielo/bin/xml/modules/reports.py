
import os
from datetime import datetime

import utils
import xml_utils
import content_validation

from article import Article, PersonAuthor, CorpAuthor


def report_date():
    procdate = datetime.now().isoformat()
    return procdate[0:10] + ' ' + procdate[11:19]


class TOCValidation(object):

    def __init__(self, filename_and_article_list):
        self.articles = filename_and_article_list
        self.html_report = HTMLReport()

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
            r += self.html_report.format_div(self.html_report.format_list('ERROR: Invalid XML files', 'ol', invalid))

        for label in equal_data:
            if len(toc_data[label]) != 1:
                part = self.html_report.format_p('ERROR: equal value of ' + label + ' is required for all the articles')
                for k, v in toc_data[label].items():
                    part += self.html_report.format_list(k, 'ul', v)
                r += self.html_report.format_div(part)

        for label in unique_data:
            if len(toc_data[label]) > 0 and len(toc_data[label]) != len(self.articles):
                part = self.html_report.format_p('ERROR: unique value of ' + label + ' is required for all the articles')
                for k, v in toc_data[label].items():
                    if len(v) > 1:
                        part += self.html_report.format_list(k, 'ul', v)
                r += self.html_report.format_div(part)
        return r


class DisplayData(object):

    def __init__(self, article):
        self.article = article
        self.article_validation = content_validation.ArticleContentValidation(article)

    def article_data(self):
        r = ''
        r += self.article_validation.toc_section
        r += self.article_validation.titles
        r += self.article_validation.trans_titles
        r += self.article_validation.contrib_names
        r += self.article_validation.contrib_collabs
        r += self.article_validation.abstracts
        r += self.article_validation.keywords
        r += self.article_validation.order
        r += self.article_validation.doi
        r += self.article_validation.fpage
        r += utils.display_value('first page seq', self.article.fpage_seq)
        r += utils.display_value('elocation id', self.article.elocation_id)
        return r

    def issue_header(self):
        r = [self.article.journal_title, self.article.journal_id_nlm_ta, self.article.issue_label, utils.format_date(self.article.issue_pub_date)]
        return '\n'.join([item for item in r if item is not None])


class HTMLReport(object):

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
        s += self.body
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
                r += '<td>' + self.format_cell(row.get(label)) + '</td>'
            r += '</tr>'
        r += '</table>'
        return r

    def format_html(self, value):
        return ''.join([self.format_p(c) for c in value.split('\n')])

    def format_p(self, value):
        css_class = ''
        if 'ERROR' in value:
            css_class = 'error'
        if 'WARNING' in value:
            css_class = 'warning'
        if css_class != '':
            css_class = ' class="' + css_class + '"'
        if '<p' in value:
            tag = 'div'
        else:
            tag = 'p'
        return '<' + tag + css_class + '>' + value + '</' + tag + '>'

    def format_div(self, content):
        return '<div>' + content + '</div>'

    def format_list(self, label, list_type, list_items):
        r = self.format_p(label)
        r += '<p>'
        r += '<' + list_type + '>'
        if isinstance(list_items, dict):
            r += ''.join(['<li>' + self.display_value(k, v) + '</li>' for k, v in list_items.items()])
        elif isinstance(list_items, list):
            r += ''.join(['<li>' + item + '</li>' for item in list_items])
        r += '</' + list_type + '></p>'
        return r

    def format_cell(self, value):
        r = ''
        if value is None:
            r = ''
        elif isinstance(value, str):
            r = '|' + value + '|'
        elif isinstance(value, dict):
            r += '<ul>'
            for k, v in value.items():
                if isinstance(v, list):
                    r += '<li>' + k + ': ' + ', '.join(v) + ';</li>'
                else:
                    r += '<li>' + utils.display_value(k, v) + ';</li>'
            r += '</ul>'
        else:
            r = ''
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

    def display_value(self, label, value):
        return '<span class="label">' + label + '</span>: ' + value + '\n' if value is not None else 'None\n'

    def display_values(self, label, values):
        return label + ': ' + '\n'.join(values) + '\n'

    def display_attributes(self, label, attributes):
        r = []
        for key, value in attributes.items():
            if value is list:
                value = '; '.join(value)
            r.append(display_value(key, value))
        return label + '\n' + '\n'.join(r) + '\n'

    def display_items_with_attributes(self, label, items_with_attributes):
        r = label + ': ' + '\n'
        for item_name, item_values in items_with_attributes.items():
            r += display_values_with_attributes(item_name, item_values)
        return r + '\n'

    def display_values_with_attributes(self, label, values_with_attributes):
        return label + ': ' + '\n' + '\n'.join([display_attributes('=>', item) for item in values_with_attributes]) + '\n'

    def conditional_required(self, label, value):
        return display_value(label, value) if value is not None else 'WARNING: Required ' + label + ', if exists. '

    def required(self, label, value):
        return display_value(label, value) if value is not None else 'ERROR: Required ' + label + '. '

    def required_one(self, label, value):
        return display_attributes(label, value) if value is not None else 'ERROR: Required ' + label + '. '

    def expected_values(self, label, value, expected):
        return display_value(label, value) if value in expected else 'ERROR: ' + value + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected)

    def add_new_value_to_index(self, dict_key_and_values, key, value):
        print(key)
        if key is not None:
            if not key in dict_key_and_values.keys():
                dict_key_and_values[key] = []
            dict_key_and_values[key].append(value)
        return dict_key_and_values


class ArticleData(object):

    def __init__(self, article):
        self.article = article

    def authors(self, filename=None):
        r = []
        t_header = ['location', 'collab', 'given-names', 'surname', 'suffix', 'prefix', ]
        if not filename is None:
            t_header = ['filename'] + t_header
        for a in self.article.contrib_names:
            row = {}
            row['filename'] = filename
            row['location'] = ' '.join(a.xref)
            row['given-names'] = a.fname
            row['surname'] = a.surname
            row['suffix'] = a.suffix
            row['prefix'] = a.prefix
            r.append(row)

        for a in self.article.contrib_collabs:
            row = {}
            row['location'] = ''
            row['collab'] = a.collab
            r.append(row)

        for ref in self.article.references:
            for grp in ref.person_groups:
                for item in grp:
                    row = {}
                    row['location'] = ref.id
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
            t_header = ['filename'] + t_header

        for ref in self.article.references:
            row = {}
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
        def _ids(node, escope):
            res = []
            if node is not None:
                for n in node.findall('.//*[@id]'):
                    r = {}
                    r['escope'] = escope
                    r['element'] = n.tag
                    r['ID'] = n.attrib.get('id')
                    res.append(r)
            return res

        r = []
        t_header = ['escope', 'ID', 'element']
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
    report = HTMLReport()

    articles_and_filenames = []
    for xml_name in os.listdir(xml_path):
        if not 'incorrect' in xml_name and xml_name.endswith('.xml'):
            tree = xml_utils.load_xml(xml_path + '/' + xml_name)
            article = Article(tree)
            articles_and_filenames.append((xml_name, article))

    report_content = TOCValidation(articles_and_filenames).report()
    authors_sheet_data = ''
    sources_sheet_data = ''

    if not os.path.isdir(report_path):
        os.makedirs(report_path)

    report.save(report_path + '/toc.html', 'TOC Validation', report_content)

    for xml_name, article in articles_and_filenames:

        report_name = report_filenames[xml_name] + '.contents.html'

        data = ArticleData(article)
        display_data = DisplayData(article)

        authors_data = report.sheet(data.authors(xml_name), xml_name)
        sources_data = report.sheet(data.sources(xml_name), xml_name)

        authors_sheet_data += authors_data
        sources_sheet_data += sources_data

        content = ''
        content += report.format_html(display_data.issue_header())
        content += report.format_html(display_data.article_data())
        content += report_content
        content += report.format_html(content_validation.ArticleContentValidation(article).report())

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
    report.body = report.body_section('title', 'Authors', authors_sheet_data)
    report.save(report_path + '/authors.html')

    report.title = 'Sources'
    report.body = report.body_section('title', 'Sources', sources_sheet_data)
    report.save(report_path + '/sources.html')


xml_path = '/Users/robertatakenaka/Documents/vm_dados/scielo_data/serial/pab/v48n7/markup_xml/scielo_package'
report_path = '/Users/robertatakenaka/Documents/_xpm_reports_'
report_filenames = {v:v.replace('.xml', '') for v in os.listdir(xml_path) if v.endswith('.xml') and not 'incorre' in v }
generate_package_reports(xml_path, report_path, report_filenames)
print('Reports in ' + report_path)
