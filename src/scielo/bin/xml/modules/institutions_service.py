# coding=utf-8

import urllib
import os
import json

import utils
import dbm_sql
import ws_requester


curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


wos_country_list = None
iso_country_list = None
br_state_list = None
orgname_list = None
location_list = None

previous_requests = {}


def normalize_term(term):
    if term is not None:
        if not isinstance(term, unicode):
            term = term.decode('utf-8')
        term = ' '.join([item.strip() for item in term.split()])
    return term


class OrgManager(object):

    def __init__(self):
        self.local_institutions_manager = OrgDBManager()

    def load(self):
        pass

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
        r = [(_orgname, _city, _state, _country_code, _country_name) for score, _orgname, _city, _state, _country_code, _country_name in wayta_search(orgname, country_name, exact_country, complements) if _orgname == orgname]
        if not len(r) == 1:
            r = [(_orgname, _city, _state, _country_code, _country_name) for score, _orgname, _city, _state, _country_code, _country_name in wayta_search(orgname, country_name, exact_country, complements)]
        return r


class OrgDBManager(object):

    def __init__(self):
        self.db_filename = curr_path + '/../tables/xc.db'
        self.sql = dbm_sql.SQL(self.db_filename)
        self.csv_filename = curr_path + '/../tables/orgname_location_country.csv'
        self.schema_filename = curr_path + '/xc.sql'
        self.fields = ['name', 'city', 'state', 'country_code', 'country_name']
        self.table_name = 'institutions'
        if not os.path.isfile(self.db_filename):
            self.create_db()
        self.normalized_country_items = self.get_country_items()

    def create_db(self):
        if os.path.isfile(self.db_filename):
            os.unlink(self.db_filename)
        self.sql.create_db(self.schema_filename)
        self.sql.insert_data(self.csv_filename, self.table_name, self.fields)

    def get_country_items(self):
        expr = self.sql.get_select_statement(self.table_name, ['country_name', 'country_code'], None)
        r = self.sql.query(expr)
        items = {}

        if len(r) > 0:
            for country_name, country_code in r:
                items[country_name] = country_code
        return items

    def get_similar_country_names(self, country_name):
        rate, most_similars = utils.most_similar(utils.similarity(self.normalized_country_items.keys(), country_name, 0.7))
        return most_similars

    def normalized_country_name(self, country_code, country_name):
        if country_name is None:
            if not country_code is None:
                country_name = self.normalized_country_items.get(country_code)
        else:
            if not country_name in self.normalized_country_items.values():
                country_name = None
        return country_name

    def get_institutions(self, orgname, city, state, country_code, country_name):
        orgname, city, state, country_code, country_name = [normalize_term(item) for item in [orgname, city, state, country_code, country_name]]
        norm_country_name = self.normalized_country_name(country_code, country_name)
        if norm_country_name is not None and country_code is None:
            country_code = self.normalized_country_items.get(norm_country_name)
        results = self.institution_exists(orgname, city, state, country_code, norm_country_name)

        if not len(results) == 1:
            _results = self.institution_exists(orgname, None, None, country_code, norm_country_name)
            if len(_results) == 1:
                results = _results
            else:
                results += _results

        results = list(set(results))
        return results

    def get_countries_expr(self, country_names):
        or_expr = self.sql.format_expr(['country_name' for item in country_names], country_names, ' OR ')
        if len(or_expr) > 0:
            or_expr = '(' + or_expr + ')'
        return or_expr

    def institution_exists(self, orgname, city, state, country_code, country_name):
        r = []
        name_city_expr = self.sql.format_expr(['name', 'city'], [orgname, city], ' AND ')
        country_expr = self.sql.format_expr(['country_code', 'country_name'], [country_code, country_name], ' OR ')
        if len(country_expr) > 0:
            country_expr = '(' + country_expr + ')'

        where_expr = ' AND '.join([item for item in [name_city_expr, country_expr] if item != ''])
        if len(where_expr) > 0:
            expr = self.sql.get_select_statement(self.table_name, self.fields, where_expr)
            r = self.sql.query(expr)
        return r

    def similar_institutions(self, orgname, city, state, country_code, country_name):
        r = []

        similar_orgname_expr = ' OR '.join(['name LIKE ' + "'%" + word + "%'" for word in orgname.split(' ')])
        if len(similar_orgname_expr) > 0:
            similar_orgname_expr = '(' + similar_orgname_expr + ')'
        country_expr = self.get_countries_expr(self.get_similar_country_names(country_name))
        city_expr = self.sql.format_expr(['city'], [city], ' OR ')
        country_code_expr = self.sql.format_expr(['country_code'], [country_code], ' OR ')
        items = [item for item in [similar_orgname_expr, country_expr, city_expr, country_code_expr] if item != '']
        where_expr = ' AND '.join(items)

        expr = self.sql.get_select_statement(self.table_name, self.fields, where_expr)

        r = self.sql.query(expr)
        r = list(set(r))
        return r


def remove_sgml_tags(text):
    text = text.replace('[', '***BREAK***IGNORE[')
    text = text.replace(']', ']IGNORE***BREAK***')
    items = text.split('***BREAK***')
    r = ''
    for item in items:
        if item.endswith(']IGNORE') or item.startswith('IGNORE['):
            r += ''
        else:
            r += item
    return r


def wayta_request(text):

    if isinstance(text, unicode):
        text = text.encode('utf-8')
    result = None
    values = {
                'q': text,
              }
    url = 'http://wayta.scielo.org/api/v1/institution'
    try:
        data = urllib.urlencode(values)
        full_url = url + '?' + data

        result = previous_requests.get(full_url)
        if result is None:
            result = ws_requester.wsr.request(full_url, timeout=30)
            previous_requests[full_url] = result
    except Exception as e:
        print('wayta_request:')
        print(e)
    return result


def format_wayta_results(result, filter_country=None):
    r = []
    keys = ['score', 'value', 'city', 'state', 'iso3166', 'country']
    try:
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


def unicode2cp1252(results):
    r = []
    for item in results:
        text = ''
        if not isinstance(item, unicode):
            item = item.decode('utf-8')
        if isinstance(item, unicode):
            try:
                text = item.encode('cp1252')
            except Exception as e:
                try:
                    text = item.encode('cp1252', 'xmlcharrefreplace')
                except Exception as e:
                    print(e)
                    print(item)
        if len(text) > 0:
            r.append(text)
    return '\n'.join(r)


def wayta_search(orgname, country, filter_country=None, complements=[]):
    results = []
    for text in orgname.split(','):
        try:
            if len(complements) > 0:
                text += ', ' + ', '.join(complements)
            if country is not None:
                text += ', ' + country
            wayta_result = wayta_request(text)
            result = format_wayta_results(wayta_result, filter_country)
            results += result
        except:
            pass
    results = sorted(list(set(results)))
    results.reverse()
    return results


def validate_organization(orgname, norgname, country_name, country_code, state, city):
    org_manager = OrgManager()
    normalized_results = []
    not_normalized_results = []
    if orgname is not None and norgname is not None:
        if orgname != norgname:
            if norgname is not None:
                normalized_results = org_manager.search_institutions(norgname, city, state, country_code, country_name)
            if orgname is not None:
                not_normalized_results = org_manager.search_institutions(orgname, city, state, country_code, country_name)
        else:
            normalized_results = org_manager.search_institutions(norgname, city, state, country_code, country_name)
    elif orgname is not None:
        not_normalized_results = org_manager.search_institutions(orgname, city, state, country_code, country_name)
    elif norgname is not None:
        normalized_results = org_manager.search_institutions(norgname, city, state, country_code, country_name)

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


def display_results(results):
    print('\n'.join(sorted(results)))


def normaff_search(text):

    text = remove_sgml_tags(text)

    orgname, country = text.split('|')
    if '(' in country:
        country = country[0:country.find('(')].strip()

    org_manager = OrgManager()
    results = org_manager.search_institution_and_country_items(orgname, country, country)

    return results
