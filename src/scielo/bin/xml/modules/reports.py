
import os
from datetime import datetime

import modules.utils as utils
import modules.xml_utils
import modules.article
import modules.content_validation


class TOCValidation(object):

    def __init__(self, filename_and_article_list):
        self.articles = filename_and_article_list

    def report(self):
        invalid = []
        equal_data = ['journal-title', 'journal_id_nlm_ta', 'journal_issns', 'publisher_name', 'issue_label', 'issue_date', ]
        unique_data = ['order', 'doi', 'fpage', 'fpage_seq', 'elocation_id']

        toc_data = {}
        for label in equal_data + unique_data:
            toc_data[label] = {}

        for filename, article in self.articles:
            if article is None:
                invalid.append(filename)
            else:
                art_data = utils.article_data(article)
                for label in toc_data.keys():
                    toc_data[label] = utils.update_values(filename, toc_data[label], art_data[label])

        r = ''
        if len(invalid) > 0:
            r += '\nERROR: Invalid XML files' + '\n'
            r += '; '.join(invalid)

        for label in equal_data:
            if len(toc_data[label]) != 1:
                r += '\nERROR: equal value of ' + label + ' is required for all the articles' + '\n'
                for k, v in toc_data[label].items():
                    r += label + '\n'
                    r += k + '\n'
                    r += '; '.join(v)

        for label in unique_data:
            if len(toc_data[label]) != len(self.articles):
                r += '\nERROR: unique value of ' + label + ' is required for all the articles' + '\n'
                for k, v in toc_data[label].items():
                    if len(v) > 1:
                        r += label + '\n'
                        r += k + '\n'
                        r += '; '.join(v)
        return r


class DisplayData(object):

    def __init__(self, article):
        self. article = article

    def article_data(self):
        r = ''
        r += utils.display_attributes('section', self.article.toc_section)
        r += utils.display_attributes('article titles', self.article.article_titles)
        r += utils.display_values_with_attributes('contrib_names', self.article.contrib_names)
        r += utils.display_values_with_attributes('contrib_collabs', self.article.contrib_collabs)
        r += utils.display_values_with_attributes('abstracts', self.article.abstracts)
        r += utils.display_values_with_attributes('keywords', self.article.keywords)
        r += utils.display_value('ORDER', self.article.order)
        r += utils.display_value('DOI', self.article.doi)
        r += utils.display_value('first page', self.article.fpage)
        r += utils.display_value('first page seq', self.article.fpage_seq)
        r += utils.display_value('elocation id', self.article.elocation_id)
        return r

    def issue_header(self):
        r = ''
        r += self.article.journal_title
        r += self.article.journal_id_nlm_ta
        r += self.article.issue_label
        r += self.article.issue_date
        return r


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

    def sheet(self, table_header, table_data, filename=None):
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

    def format_html(self, value):
        return '\n'.join(['<p>' + c + '</p>' for c in value.split('\n')])

    def format_cell(self, value):
        r = ''
        if value is None:
            r = ''
        elif isinstance(value, str):
            r = '|' + value + '|'
        elif isinstance(value, dict):
            r += '<ul>'
            for k, v in value:
                r += '<li>' + k + ': ' + v + ';</li>'
            r += '</ul>'
        else:
            r = ''
        return r

    def report_date():
        procdate = datetime.now().isoformat()
        return procdate[0:10] + ' ' + procdate[11:19]


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
                    if isinstance(item, modules.article.PersonAuthor):
                        row['given-names'] = a.fname
                        row['surname'] = a.surname
                        row['suffix'] = a.suffix
                        row['prefix'] = a.prefix
                    else:
                        row['collab'] = a.collab
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
            for n in node.findall('.//*[@id]'):
                r = {}
                r['escope'] = escope
                r['element'] = n.tag
                r['ID'] = n.attrib.get('id')
                res.append(r)
            return res

        r = []
        t_header = ['escope', 'ID', 'element']
        r += _ids(self.article_meta, 'article')
        r += _ids(self.body, 'article')
        r += _ids(self.back, 'article')

        for item in self.subarticles:
            r += _ids(item, 'sub-article ' + item.find('.').attrib.get('id'))
        for item in self.responses:
            r += _ids(item, 'response ' + item.find('.').attrib.get('id'))

        return (t_header, r)

    def tables(self):
        t_header = ['ID', 'label', 'caption', 'table', ]
        r = []
        for t in self.article.tree.findall('.//*[table]'):
            row = {}
            row['ID'] = t.attrib.get('id')
            row['label'] = t.findtext('.//label')
            row['caption'] = t.findtext('.//caption')
            row['table'] = modules.xml_utils.node_text(t.find('./table')) + modules.xml_utils.node_text(t.find('./graphic'))
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
        for a in self.affiliations:
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
            tree = modules.xml_utils.load_xml(xml_path + '/' + xml_name)
            article = modules.article.Article(tree)
            articles_and_filenames.append((xml_name, article))

    toc_report = TOCValidation(articles_and_filenames).report()
    toc_report = report.report('h1', 'TOC Report', toc_report)
    toc_report = report.format_html(toc_report)

    authors_sheet_data = ''
    sources_sheet_data = ''

    f = open(report_path + '/toc.html', 'w')
    report.title = 'TOC Validation'
    report.body = toc_report
    f.write(report.html())
    f.close()

    for xml_name, article in articles_and_filenames:

        report_name = report_filenames[xml_name] + '.contents.html'

        data = ArticleData(article)
        display_data = DisplayData(article)

        authors_data = data.authors(xml_name)
        sources_data = data.sources(xml_name)

        authors_sheet_data += authors_data
        sources_sheet_data += sources_data

        content = ''
        content += report.format_html(display_data.issue_header)
        content += report.format_html(display_data.article_data)
        content += toc_report
        content += report.format_html(modules.content_validation.ArticleContentValidation(article).report())

        content += report.body_section('h1', 'Authors', report.sheet(authors_data))
        content += report.body_section('h1', 'Affiliations', report.sheet(data.affiliations()))
        content += report.body_section('h1', 'IDs', report.sheet(data.ids()))
        content += report.body_section('h1', 'href', report.sheet(data.hrefs()))
        content += report.body_section('h1', 'Tables', report.sheet(data.tables()))
        content += report.body_section('h1', 'Sources', report.sheet(sources_data))

        report.title = xml_name + ' - ' + report.report_date()
        report.body = report.body_section('title', report.title, content)

        f = open(report_path + '/' + report_name, 'w')
        f.write(report.html())
        f.close()

    f = open(report_path + '/authors.html', 'w')
    report.title = 'Authors'
    report.body = report.body_section('title', 'Authors', report.sheet(authors_sheet_data))
    f.write(report.html())
    f.close()

    f = open(report_path + '/sources.html', 'w')
    report.title = 'Sources'
    report.body = report.body_section('title', 'Sources', report.sheet(sources_sheet_data))
    f.write(report.html())
    f.close()
