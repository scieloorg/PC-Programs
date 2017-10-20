# coding=utf-8

from datetime import datetime

from .. import encoding


class DOIWebServicesRequester(object):

    def __init__(self, _ws_requester):
        self.ws_requester = _ws_requester
        self.doi_requested = {}
        self.doi_journal_prefixes = {}

    def journal_doi_prefix_url(self, issn, year=None):
        if year is None:
            year = datetime.now().year
        if issn is not None:
            return 'https://api.crossref.org/works?filter=issn:{issn},from-pub-date:{year}'.format(issn=issn, year=year)

    def article_doi_checker_url(self, doi):
        #https://api.crossref.org/works/10.1037/0003-066X.59.1.29
        url = None
        if doi is not None:
            url = 'https://api.crossref.org/works/' + doi
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
            result = self.ws_requester.json_result_request(url)
            if result is not None:
                data = DOIData(result)
                self.doi_requested[doi] = data
        return data

    def journal_prefix(self, issn, year):
        key = [issn, year]
        key = ''.join([k for k in key if k is not None])
        prefix = self.doi_journal_prefixes.get(key)
        if prefix is None:
            url = self.journal_doi_prefix_url(issn, year)
            json_results = self.ws_requester.json_result_request(url)
            if json_results is not None:
                items = json_results.get('message', {}).get('items')
                if items is not None:
                    if len(items) > 0:
                        prefix = items[0].get('prefix')
                        if prefix is not None:
                            if '/prefix/' in prefix:
                                prefix = prefix[prefix.find('/prefix/')+len('/prefix/'):]
        if prefix is not None:
            self.doi_journal_prefixes[key] = prefix
        return prefix


class DOIData(object):

    def __init__(self, json_data):
        self.json_data = json_data.get('message')
        if self.json_data is not None:
            self.journal_titles = self.json_data.get('container-title')
            article_titles = []
            items = self.json_data.get('title')
            if items is not None:
                for article_title in items:
                    if '/' in article_title:
                        article_titles.extend(article_title.split('/'))
                    else:
                        article_titles.append(article_title)
            self.article_titles = [item.strip() for item in article_titles]

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
        except Exception as e:
            encoding.report_exception('ws_doi.authors()', e, self.json_data.get('author'))
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
        except Exception as e:
            encoding.report_exception('ws_doi.data()', e, self.json_data)
            raise
