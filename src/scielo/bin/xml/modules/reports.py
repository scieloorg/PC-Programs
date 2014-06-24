

import modules.utils as utils


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
                r += '<td>|' + row.get(label, '') + '|</td>'
            r += '</tr>'
        r += '</table>'


class ArticleSheets(object):

    def __init__(self, article):
        self.article = article

    def 
