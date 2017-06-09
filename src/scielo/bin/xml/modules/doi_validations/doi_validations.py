# coding=utf-8

from .. import ws_requester
from .. import validation_status
from ..__init__ import _
from .. import utils

from datetime import datetime

from .. import xml_utils


class DOIValidator(object):

    def __init__(self):
        self.doi_services = DOIWebServicesRequester()

    def validate(self, article):
        self.messages = []
        self._validate_format(article.doi)
        self._validate_doi_prefix(article)
        doi_data = self.doi_services.doi_data(article.doi)
        if doi_data is not None:
            self._validate_journal_title(article, doi_data)
            self._validate_article_title(article, doi_data)
            self._validate_issn(article, doi_data)
        return self.messages

    def _validate_format(self, doi):
        errors = []
        if doi is not None:
            for item in doi:
                if item.isdigit():
                    pass
                elif item in '-.-;()/':
                    pass
                elif item in 'abcdefghijklmnopqrstuvwxyz' or item in 'abcdefghijklmnopqrstuvwxyz'.upper():
                    pass
                else:
                    errors.append(item)
        if len(errors) > 0:
            self.messages.append(('doi', validation_status.STATUS_FATAL_ERROR, _('{value} has {q} invalid characteres ({invalid}). Valid characters are: {valid_characters}. ').format(value=doi, valid_characters=_('numbers, letters no diacritics, and -._;()/'), invalid=' '.join(errors), q=str(len(errors)))))

    def _validate_doi_prefix(self, article):
        prefix = article.doi[:article.doi.find('/')]
        valid_prefixes = []
        for issn in [article.e_issn, article.print_issn]:
            if issn is not None:
                doi_prefix = self.doi_services.journal_prefix(issn, article.pub_date_year)
                if doi_prefix is not None:
                    valid_prefixes.append(doi_prefix)
        if prefix not in valid_prefixes:
            self.messages.append(('doi', validation_status.STATUS_FATAL_ERROR, _('{value} is an invalid value for {label}. ').format(value=prefix, label=_('doi prefix')) + _('{label} must starts with: {expected}. ').format(label='doi', expected=_(' or ').join(valid_prefixes))))

    def _validate_journal_title(self, article, doi_data):
        if not doi_data.journal_titles is None:
            status = validation_status.STATUS_INFO
            if article.journal_title not in doi_data.journal_titles:
                max_rate, items = utils.most_similar(utils.similarity(doi_data.journal_titles, article.journal_title))
                if max_rate < 0.7:
                    status = validation_status.STATUS_FATAL_ERROR
            self.messages.append(('doi', status, _('{item} is registered as belonging to {owner}. ').format(item=article.doi, owner='|'.join(doi_data.journal_titles))))

    def _validate_article_title(self, article, doi_data):
        if not doi_data.article_titles is None:
            status = validation_status.STATUS_INFO
            max_rate = 0
            selected = None
            for t in article.titles:
                rate, items = utils.most_similar(utils.similarity(doi_data.article_titles, xml_utils.remove_tags(t.title)))
                if rate > max_rate:
                    max_rate = rate
            if max_rate < 0.7:
                status = validation_status.STATUS_FATAL_ERROR
            self.messages.append(('doi', status, _('{item} is registered as belonging to {owner}. ').format(item=article.doi, owner='|'.join(doi_data.article_titles))))

    def _validate_issn(self, article, doi_data):
        if doi_data.journal_titles is None:
            found = False
            for issn in [article.print_issn, article.e_issn]:
                if issn is not None:
                    if issn.upper() in article.doi.upper():
                        found = True
            if not found:
                self.messages.append(('doi', validation_status.STATUS_ERROR, _('Be sure that {item} belongs to this journal. ').format(item='DOI=' + article.doi)))


class DOIWebServicesRequester(ws_requester.WebServicesRequester):

    def __init__(self):
        ws_requester.WebServicesRequester.__init__(self)
        self.doi_requested = {}
        self.doi_journal_prefixes = {}

    def journal_doi_prefix_url(self, issn, year=None):
        if year is None:
            year = datetime.now().year
        if issn is not None:
            return 'http://api.crossref.org/works?filter=issn:{issn},from-pub-date:{year}'.format(issn=issn, year=year)

    def article_doi_checker_url(self, doi):
        #http://api.crossref.org/works/10.1037/0003-066X.59.1.29
        url = None
        if doi is not None:
            url = 'http://api.crossref.org/works/' + doi
        return url

    def _fix_doi(self, doi):
        if 'doi.org' in doi:
            doi = doi[doi.find('doi.org/')+len('doi.org/'):]
        return doi.strip().lower()

    def doi_data(self, doi):
        doi = self._fix_doi(doi)
        data = self.doi_requested.get(doi)
        if data is None:
            url = self.article_doi_checker_url(doi)
            result = self.json_result_request(url)
            if result is not None:
                data = DOIData(result)
                self.doi_requested[doi] = data
        return data

    def journal_prefix(self, issn, year):
        prefix = self.doi_journal_prefixes.get(issn+year)
        if prefix is None:
            url = self.journal_doi_prefix_url(issn, year)
            json_results = self.json_result_request(url)
            if json_results is not None:
                items = json_results.get('message', {}).get('items')
                if items is not None:
                    if len(items) > 0:
                        prefix = items[0].get('prefix')
                        if prefix is not None:
                            if '/prefix/' in prefix:
                                prefix = prefix[prefix.find('/prefix/')+len('/prefix/'):]
        if prefix is not None:
            self.doi_journal_prefixes[issn+year] = prefix
        return prefix


class DOIData(object):

    def __init__(self, json_data):
        self.json_data = json_data.get('message')
        if self.json_data is not None:
            self.journal_titles = self.json_data.get('container-title')
            self.article_titles = self.json_data.get('title')

    @property
    def _authors(self):
        authors = self.json_data.get('author', [])
        if authors is not None:
            return [item.get('family') for item in authors if item.get('family') is not None]
        return []

    @property
    def authors(self):
        try:
            return ' '.join(self._authors)
        except:
            print(self.json_data.get('author'))
            raise

    @property
    def _alternative_id(self):
        return self.json_data.get('alternative-id')

    @property
    def pid(self):
        if self._alternative_id is not None:
            if len(self._alternative_id) > 0:
                return self._alternative_id[0]
        return ''

    @property
    def _issns(self):
        return self.json_data.get('ISSN', [])

    @property
    def issns(self):
        if len(self._issns) > 0:
            return self._issns[0]
        return ''

    @property
    def _deposited_date(self):
        _date = self.json_data.get('deposited', {}).get('date-parts')
        if len(_date) > 0:
            if isinstance(_date[0], list):
                if len(_date[0]) == 3:
                    return _date[0]

    @property
    def deposited_date(self):
        return ''.join([str(v).zfill(2) for v in self._deposited_date])

    @property
    def _epub_date(self):
        _date = self.json_data.get('published-online', self.json_data.get('published-print', {})).get('date-parts')
        if len(_date) > 0:
            if isinstance(_date[0], list):
                return _date[0]

    @property
    def year(self):
        if self._epub_date is not None:
            return str(self._epub_date[0])

    @property
    def data(self):
        try:
            if all([self.authors, self.pid, self.issns, self.deposited_date, self.year]):
                return (self.pid, self.authors, self.issns, self.year, self.deposited_date)
        except:
            print(self.json_data)
            raise
