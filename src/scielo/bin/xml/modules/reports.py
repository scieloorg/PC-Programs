

import modules.utils as utils
import modules.xml_utils
import modules.article


class TOCValidation(object):

    def __init__(self, articles):
        self.articles = articles

    def report(self):
        invalid = []
        equal_data = ['journal-title', 'journal_id_nlm_ta', 'journal_issns', 'publisher_name', 'issue_label', 'issue_date', ]
        unique_data = ['order', 'doi', 'fpage', 'fpage_seq', 'elocation_id']

        toc_data = {}
        for label in equal_data + unique_data:
            toc_data[label] = {}

        for filename, article in self.articles.items():
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


class Sheet(object):

    def __init__(self, table_header, table_data):
        self.table_header = table_header
        self.table_data = table_data

    def report(self):
        r = '<table>'
        r += '<tr>'
        for label in self.table_header:
            r += '<th>' + label + '</th>'
        r += '</tr>'
        for row in self.table_data:
            r += '<tr>'
            for label in self.table_header:
                r += '<td>|' + self.format(row.get(label)) + '|</td>'
            r += '</tr>'
        r += '</table>'

    def format(self, value):
        r = ''
        if value is None:
            r = ''
        elif isinstance(value, str):
            r = value
        elif isinstance(value, dict):
            r += '<ul>'
            for k, v in value:
                r += '<li>' + k + ': ' + v + ';</li>'
            r += '</ul>'
        else:
            r = ''
        return r


class ArticleData(object):

    def __init__(self, article):
        self.article = article

    def authors(self):
        r = []
        t_header = ['location', 'collab', 'given-names', 'surname', 'suffix', 'prefix', ]
        for a in self.article.contrib_names:
            row = {}
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

    def source(self):
        r = []
        t_header = ['ID', 'type', 'year', 'source', 'publisher name', 'location', ]
        for ref in self.article.references:
            row = {}
            row['ID'] = ref.id
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
