# coding=utf-8

from . import ws_institutions
from . import institutions_db


class InstitutionsManager(object):

    def __init__(self, app_ws_requester):
        self.local_institutions_manager = institutions_db.InstitutionsDBManager()
        self.ws = ws_institutions.Wayta(app_ws_requester)

    def search_institutions(self, orgname, city, state, country_code, country_name, exact_country=None):
        results = self.local_institutions_manager.get_institutions(orgname, city, state, country_code, country_name)
        results += self.search_at_wayta(orgname, country_name, exact_country, [city, state])
        results = sorted(list(set(results)))
        return results

    def institution_exists(self, orgname, city, state, country_code, country_name):
        results = self.local_institutions_manager.institution_exists(orgname, city, state, country_code, country_name)
        results += self.search_at_wayta(orgname, country_name)
        results = sorted(list(set([(_orgname, _city, _state, _code, _country_name) for _orgname, _city, _state, _code, _country_name in results if _orgname == orgname])))
        return results

    def search_institution_and_country_items(self, orgname, country_name, exact_country):
        items = self.search_institutions(orgname, None, None, None, country_name, exact_country)
        results = sorted(list(set([_orgname + ' - ' + _country_name for _orgname, _city, _state, _code, _country_name in items])))
        return results

    def create_db(self):
        self.local_institutions_manager.create_db()

    def search_at_wayta(self, orgname, country_name, exact_country=None, complements=[]):
        #keys = ['score', 'value', 'city', 'state', 'iso3166', 'country']
        r = [(_orgname, _city, _state, _country_code, _country_name) for score, _orgname, _city, _state, _country_code, _country_name in self.ws.search(orgname, country_name, exact_country, complements) if _orgname == orgname]
        if not len(r) == 1:
            r = [(_orgname, _city, _state, _country_code, _country_name) for score, _orgname, _city, _state, _country_code, _country_name in self.ws.search(orgname, country_name, exact_country, complements)]
        return r

    def validate_organization(self, orgname, norgname, country_name, country_code, state, city):
        normalized_results = []
        not_normalized_results = []
        if orgname is not None and norgname is not None:
            if orgname != norgname:
                if norgname is not None:
                    normalized_results = self.search_institutions(norgname, city, state, country_code, country_name)
                if orgname is not None:
                    not_normalized_results = self.search_institutions(orgname, city, state, country_code, country_name)
            else:
                normalized_results = self.search_institutions(norgname, city, state, country_code, country_name)
        elif orgname is not None:
            not_normalized_results = self.search_institutions(orgname, city, state, country_code, country_name)
        elif norgname is not None:
            normalized_results = self.search_institutions(norgname, city, state, country_code, country_name)

        _results = normalized_results + not_normalized_results
        if len(normalized_results) == 1:
            if normalized_results[0] in not_normalized_results:
                _results = normalized_results

        _results = list(set(_results))
        if len(_results) > 1:
            fixed = []
            for orgname, city, state, country_code, country_name in _results:
                fixed.append((orgname, '', '', country_code, country_name))
            fixed = list(set(fixed))
            if len(fixed) == 1:
                _results = fixed
        return _results
