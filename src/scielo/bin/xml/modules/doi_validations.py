# coding=utf-8

import ws_requester


MIN_IMG_DPI = 300
MIN_IMG_WIDTH = 789
MAX_IMG_WIDTH = 2250
MAX_IMG_HEIGHT = 2625


class DOI_Services(object):

    def __init__(self):
        self.doi_data_items = {}
        self.doi_journal_prefixes = {}

    def get_doi_data(self, doi):
        doi_data = self.doi_data_items.get(doi)
        if doi_data is None:
            url = ws_requester.wsr.article_doi_checker_url(doi)
            article_json = ws_requester.wsr.json_result_request(url)
            if article_json is not None:
                data = article_json.get('message')
                if data is not None:
                    doi_data = DOI_Data(doi)
                    doi_data.journal_titles = data.get('container-title')
                    doi_data.article_titles = data.get('title')
                    doi_data.pid = data.get('alternative-id')
                    if doi_data.pid is not None:
                        doi_data.pid = doi_data.pid[0]
        if doi_data is not None:
            self.doi_data_items[doi] = doi_data
        return doi_data

    def doi_journal_prefix(self, issn, year):
        prefix = self.doi_journal_prefixes.get(issn)
        if prefix is None:
            url = ws_requester.wsr.journal_doi_prefix_url(issn, year)
            json_results = ws_requester.wsr.json_result_request(url)
            if json_results is not None:
                items = json_results.get('message', {}).get('items')
                if items is not None:
                    if len(items) > 0:
                        prefix = items[0].get('prefix')
                        if prefix is not None:
                            if '/prefix/' in prefix:
                                prefix = prefix[prefix.find('/prefix/')+len('/prefix/'):]
        if prefix is not None:
            self.doi_journal_prefixes[issn] = prefix
        return prefix


class DOI_Data(object):

    def __init__(self, doi):
        self.doi = doi
        self.journal_titles = None
        self.article_titles = None
        self.pid = None

    def validate_doi_format(self):
        errors = []
        if self.doi is not None:
            for item in self.doi:
                if item.isdigit():
                    pass
                elif item in '-.-;()/':
                    pass
                elif item in 'abcdefghijklmnopqrstuvwxyz' or item in 'abcdefghijklmnopqrstuvwxyz'.upper():
                    pass
                else:
                    errors.append(item)
        return errors
