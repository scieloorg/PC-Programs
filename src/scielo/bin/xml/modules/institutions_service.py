# code = utf-8

import os

import utils
import dbm_sql


curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


wos_country_list = None
iso_country_list = None
br_state_list = None
orgname_list = None
location_list = None


class OrgManager(object):

    def __init__(self):
        self.manager = OrgDBManager()

    def load(self):
        pass

    def country_orgnames(self, country_code):
        return self.manager.country_orgnames(country_code)

    def get_organizations(self, orgname, city, state, country_code, country_name):
        return self.manager.get_organizations(orgname, city, state, country_code, country_name)

    def get_country_code(self, country_name):
        return self.manager.get_country_code(country_name)

    def get_similar_orgnames_in_country_name_items(self, orgname, country_name):
        return self.manager.get_similar_orgnames_in_country_name_items(orgname, country_name)

    def create_db(self):
        self.manager.create_db()


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

    def create_db(self):
        if os.path.isfile(self.db_filename):
            os.unlink(self.db_filename)
        self.sql.create_db(self.schema_filename)
        self.sql.insert_data(self.csv_filename, self.table_name, self.fields)

    def country_orgnames(self, country_code):
        expr = self.sql.get_select_statement(self.table_name, ['name', 'city', 'state'], 'country_code="' + country_code + '"')
        r = self.sql.query(expr)
        if len(r) > 0:
            r = list(set(r))
        return r

    def get_country_code(self, country_name):
        expr = self.sql.get_select_statement(self.table_name, self.fields, 'country_name="' + country_name + '"')
        data = self.sql.query_one(expr)
        return data[3] if data is not None else None

    def get_organizations(self, orgname, city, state, country_code, country_name):
        r = []
        and_expr = self.sql.format_expr(['name', 'city', 'state'], [orgname, city, state], ' AND ')
        or_expr = self.sql.format_expr(['country_name', 'country_code'], [country_name, country_code])
        if len(or_expr) > 0:
            or_expr = '(' + or_expr + ')'

        where_expr = ' AND '.join([item for item in [and_expr, or_expr] if item != ''])

        if len(where_expr) > 0:
            expr = self.sql.get_select_statement(self.table_name, ['name', 'city', 'state', 'country_code', 'country_name'], where_expr)
            r = self.sql.query(expr)
        return r

    def get_similar_orgnames_in_country_name_items(self, orgname, country_name):
        r = []
        where_expr = self.sql.format_expr(['name', 'country_name'], [orgname, country_name], ' AND ')
        if len(where_expr) > 0:
            expr = self.sql.get_select_statement(self.table_name, ['name', 'country_code'], where_expr)
            r = self.sql.query(expr)
        if len(r) == 0:
            where_expr = ' AND '.join(['name LIKE ' + "'%" + word + "%'" for word in orgname.split(' ')])
            expr = self.sql.get_select_statement(self.table_name, ['name', 'country_code'], where_expr)
            r += self.sql.query(expr)
        if len(r) == 0:
            for word in orgname.split(' '):
                where_expr = 'name LIKE ' + "'%" + word + "%'"
                expr = self.sql.get_select_statement(self.table_name, ['name', 'country_code'], where_expr)
                r += self.sql.query(expr)
            r = list(set(r))
        return r


class OrgListManager(object):

    def __init__(self):
        self.indexedby_orgname = {}
        self.indexedby_isocountry = {}
        self.indexedby_country_name = {}

    def load(self):
        for item in open(curr_path + '/../tables/orgname_location_country.csv', 'r').readlines():
            if not isinstance(item, unicode):
                item = item.decode('utf-8')
            item = item.replace('"', '').strip().split('\t')
            if len(item) == 5:
                orgname, city, state, iso_country, country_name = item

                if not orgname in self.indexedby_orgname.keys():
                    self.indexedby_orgname[orgname] = []
                if not iso_country in self.indexedby_isocountry.keys():
                    self.indexedby_isocountry[iso_country] = []

                self.indexedby_orgname[orgname].append([city, state, iso_country])
                self.indexedby_isocountry[iso_country].append([orgname, city, state])
                self.indexedby_country_name[country_name] = iso_country

    def country_orgnames(self, iso_country):
        return self.indexedby_isocountry.get(iso_country, [])

    def get_organizations(self, orgname, city, state, country):
        valid = self.indexedby_orgname.get(orgname, [])
        #print('get_organizations: step1')
        #print(valid)
        if city is not None and len(valid) > 0:
            #print(city)
            valid = [[_city, _state, _country] for _city, _state, _country in valid if _city == city]
            #print('get_organizations: step2')
            #print(valid)
        if country is not None and len(valid) > 0:
            #print(country)
            valid = [[_city, _state, _country] for _city, _state, _country in valid if _country == country]
            #print('get_organizations: step3')
            #print(valid)
        return valid

    def get_country_code(self, country_name):
        return self.indexedby_country_name.get(country_name)

    def get_countries_orgnames(self):
        r = {}
        for country_name, country_code in self.indexedby_country_name.items():
            k = country_name + ' - ' + country_code
            r[k] = sorted(['\t'.join(item) for item in self.indexedby_isocountry[country_code]])
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
    import urllib
    import urllib2

    result = None
    values = {
                'q': text,
              }
    url = 'http://wayta.scielo.org/api/v1/institution'
    try:
        data = urllib.urlencode(values)
        full_url = url + '?' + data
        #print(full_url)
        response = urllib2.urlopen(full_url, timeout=2)
        result = response.read()
    except Exception as e:
        print(e)
        result = []
    return result


def format_wayta_results(result):
    import json
    r = []

    try:
        results = json.loads(result)
        for item in results.get('choices'):
            if item.get('country', '') != '' and item.get('value', '') != '':
                #location = [item.get('country'), item.get('state'), item.get('city')]
                r.append(item.get('value') + ' - ' + item.get('country'))
    except Exception as e:
        print(e)
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


def get_normalized_from_wayta(orgname, country):
    text = orgname + ', ' + country
    results = []
    for part in text.split(','):
        try:
            wayta_result = wayta_request(part)
            result = format_wayta_results(wayta_result)
            results += result
        except:
            pass
    results = sorted(list(set(results)))
    print('\nWayta')
    print('\n'.join(results))
    return results


def find_normalized_organizations(org_manager, orgname, country_name, country_code, state, city):
    return org_manager.get_organizations(orgname, city, state, country_code, country_name)


def validate_organization(org_manager, orgname, norgname, country_name, country_code, state, city):
    orgname_and_location_items = []
    if norgname is not None:
        orgname_and_location_items = find_normalized_organizations(org_manager, norgname, country_name, country_code, state, city)

    if len(orgname_and_location_items) == 0:
        if orgname is not None:
            orgname_and_location_items = find_normalized_organizations(org_manager, orgname, country_name, country_code, state, city)
    return orgname_and_location_items


def get_similars_from_normalized_list(org_manager, orgname, country_name):
    items = org_manager.get_similar_orgnames_in_country_name_items(orgname, country_name)
    results = sorted(list(set([_orgname + ' - ' + country_name for _orgname, _country_code in items])))
    print('\nNormalized')
    print('\n'.join(results))
    return results


def normaff_search(text):
    text = text.replace(' - ', ',')
    text = text.replace(';', ',')
    text = remove_sgml_tags(text)

    orgname = text[0:text.rfind(',')].strip()
    country = text[text.rfind(',')+1:].strip()
    print(orgname)
    print(country)
    results = get_normalized_from_wayta(orgname, country)
    org_manager = OrgManager()
    org_manager.load()
    results += get_similars_from_normalized_list(org_manager, orgname, country)
    results = sorted(list(set(results)))

    print('\nResults:')
    print('\n'.join(results))
    return results
