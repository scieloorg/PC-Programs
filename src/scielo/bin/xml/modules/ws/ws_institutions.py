# coding=utf-8

import urllib
import json


class Wayta(object):

    def __init__(self, _ws_requester):
        self.ws_requester = _ws_requester
        self._url = 'http://wayta.scielo.org/api/v1/institution'
        self.results = {}

    def url(self, text):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        values = {
                    'q': text,
                  }
        data = urllib.urlencode(values)
        return self._url + '?' + data

    def request(self, text, filter_country=None):
        result = self.results.get(text)
        try:
            if result is None:
                result = self.ws_requester.request(self.url(text), timeout=30)
                self.results[text] = format_wayta_results(result, filter_country)
        except Exception as e:
            print('wayta_request:')
            print(e)
        return result

    def search(self, orgname, country, filter_country=None, complements=[]):
        results = []
        for text in orgname.split(','):
            try:
                if len(complements) > 0:
                    text += ', ' + ', '.join(complements)
                if country is not None:
                    text += ', ' + country
                result = self.request(text, filter_country)
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
        print('format_wayta_results:')
        print(e)
        print(result)
    return r
