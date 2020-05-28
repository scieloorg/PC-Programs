# coding=utf-8

import json

from prodtools.utils import encoding


class Wayta(object):

    def __init__(self, _ws_requester):
        self.ws_requester = _ws_requester
        self._url = 'http://wayta.scielo.org/api/v1/institution'
        self.results = {}

    def request(self, text, filter_country=None):
        result = self.results.get(text)
        try:
            if result is None:
                url = self.ws_requester.format_url(self._url, {'q':text})
                request_result = self.ws_requester.request(url, timeout=30)
                self.results[text] = format_wayta_results(request_result, filter_country)
                result = self.results[text]
        except Exception as e:
            encoding.report_exception('ws_institutions.request()', e, None)
        return result

    def search(self, orgname, country, filter_country=None, complements=[]):
        results = []
        for text in orgname.split(','):

            terms = [text, country]
            terms.extend(complements)

            expr = ', '.join([term for term in terms if term is not None])
            try:
                result = self.request(expr, filter_country)
                if result is not None:
                    results += result
            except:
                pass
        results = sorted(list(set(results)))
        results.reverse()
        return results


def format_wayta_results(result, filter_country=None):
    r = []
    keys = ['score', 'value', 'city', 'state', 'iso3166', 'country']
    try:
        if result is not None:
            results = json.loads(result)
            if filter_country is None:
                r = [tuple([item.get(key) for key in keys]) for item in results.get('choices') if item.get('value', '') != '']
            else:
                r = [tuple([item.get(key) for key in keys]) for item in results.get('choices') if item.get('value', '') != '' and filter_country == item.get('country')]
    except Exception as e:
        encoding.report_exception('ws_institutions.format_wayta_results()', e, result)
    return r
