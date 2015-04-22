# coding=utf-8

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

    def get_institutions(self, orgname, city, state, country_code, country_name):
        return self.manager.get_institutions(orgname, city, state, country_code, country_name)

    def institution_exists(self, orgname, city, state, country_code, country_name):
        return self.manager.institution_exists(orgname, city, state, country_code, country_name)

    def similar_institutions(self, orgname, city, state, country_code, country_name):
        return self.manager.similar_institutions(orgname, city, state, country_code, country_name)

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
        if orgname is not None:
            if not isinstance(orgname, unicode):
                orgname = orgname.decode('utf-8')
        if city is not None:
            if not isinstance(city, unicode):
                city = city.decode('utf-8')
        if country_name is not None:
            if not isinstance(country_name, unicode):
                country_name = country_name.decode('utf-8')

        norm_country_name = self.normalized_country_name(country_code, country_name)
        if norm_country_name is not None and country_code is None:
            country_code = self.normalized_country_items.get(norm_country_name)
        results = self.institution_exists(orgname, city, state, country_code, norm_country_name)

        if not len(results) == 1:
            results += self.institution_exists(orgname, None, None, country_code, norm_country_name)

        if len(results) == 0:
            results += self.similar_institutions(orgname, city, state, country_code, country_name)

        return list(set(results))

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

    print(text)
    print(type(text))
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    print(text)
    print(type(text))

    result = None
    values = {
                'q': text,
              }
    url = 'http://wayta.scielo.org/api/v1/institution'
    try:
        data = urllib.urlencode(values)
        full_url = url + '?' + data
        print(full_url)
        response = urllib2.urlopen(full_url, timeout=30)
        result = response.read()
    except Exception as e:
        print(e)
        result = []
    return result


def format_wayta_results(result, country):
    import json
    r = []

    try:
        results = json.loads(result)
        for item in results.get('choices'):
            if item.get('country', '') == country and item.get('value', '') != '':
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
            result = format_wayta_results(wayta_result, country)
            results += result
        except:
            pass
    results = sorted(list(set(results)))
    #print('\nWayta')
    #print('\n'.join(results))
    return results


def validate_organization(org_manager, orgname, norgname, country_name, country_code, state, city):
    orgname_and_location_items = []
    if norgname is not None:
        orgname_and_location_items += org_manager.get_institutions(norgname, city, state, country_code, country_name)

    if not len(orgname_and_location_items) == 1:
        if orgname is not None:
            orgname_and_location_items += org_manager.get_institutions(orgname, city, state, country_code, country_name)

    return list(set(orgname_and_location_items))


def get_similars_from_normalized_list_for_wayta(org_manager, orgname, country_name):
    items = org_manager.get_institutions(orgname, None, None, None, country_name)
    results = sorted(list(set([_orgname + ' - ' + _country_name for _orgname, city, state, code, _country_name in items])))
    #print('\nNormalized')
    #print('\n'.join(results))
    return results


def display_results(results):
    print('\n'.join(sorted(results)))


def normaff_search(text):
    print(text)
    print(type(text))
    if not isinstance(text, unicode):
        text = text.decode('cp1252')

    print(text)
    print(type(text))
    text = remove_sgml_tags(text)

    orgname, country = text.split('|')
    if '(' in country:
        country = country[0:country.find('(')].strip()

    print(orgname)
    print(country)

    results = []
    try:
        results = get_normalized_from_wayta(orgname, country)
        print('wayta results:')
        print(len(results))
    except:
        pass

    try:
        org_manager = OrgManager()
        org_manager.load()
        results += get_similars_from_normalized_list_for_wayta(org_manager, orgname, country)
        print('list results')
        print(len(results))
    except:
        pass

    results = sorted(list(set(results)))
    print('all results:')
    print(len(results))
    display_results(results)
    return results
