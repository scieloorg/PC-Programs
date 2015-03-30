# code = utf-8

import os
from datetime import datetime

import utils


curr_path = os.path.dirname(__file__).replace('\\', '/')


wos_country_list = None
iso_country_list = None
br_state_list = None
orgname_list = None
location_list = None


class OrgManager(object):

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

    def _load(self):
        for item in open(curr_path + '/../tables/orgname_location_country.csv', 'r').readlines():
            item = item.replace('"', '').strip().split('\t')
            if len(item) == 4:
                orgname, city, state, iso_country = item
                location = ', '.join([city, state, iso_country])
                city_state = ', '.join([city, state])
                city_country = ', '.join([city, iso_country])

                if not orgname in self.indexedby_orgname.keys():
                    self.indexedby_orgname[orgname] = []
                if not location in self.indexedby_location.keys():
                    self.indexedby_location[location] = []
                if not iso_country in self.indexedby_isocountry.keys():
                    self.indexedby_isocountry[iso_country] = []

                self.indexedby_orgname[orgname].append(location)
                self.indexedby_location[location].append(orgname)
                self.indexedby_isocountry[iso_country].append([orgname, city, state])

                if not city in self.indexedby_location.keys():
                    self.indexedby_location[city] = []
                if not city_state in self.indexedby_location.keys():
                    self.indexedby_location[city_state] = []
                if not city_country in self.indexedby_location.keys():
                    self.indexedby_location[city_country] = []
                self.indexedby_location[city].append([orgname, city, state, iso_country])
                self.indexedby_location[city_state].append([orgname, city, state, iso_country])
                self.indexedby_location[city_country].append([orgname, city, state, iso_country])

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


class CodesAndNames(object):

    def __init__(self, indexed_by_codes, indexed_by_names):
        self.indexed_by_codes = indexed_by_codes
        self.indexed_by_names = indexed_by_names

    def get_names(self, code):
        return self.indexed_by_codes.get(code, [])

    def get_code(self, name, similar_name):
        code = self.indexed_by_names.get(name)
        if code is None and similar_name is True:
            similar_names = self.get_similar_names(name)
            if len(similar_names) > 0:
                code = self.get_code(similar_names[0], False)
        return code

    def find_code(self, text):
        code = None
        if text is not None:
            names = self.get_names(text)
            if len(names) > 0:
                code = text
            else:
                code = self.get_code(text, True)
        return code

    def get_similar_names(self, name):
        ##print('-')
        ##print('get_similar_names')
        #print(name)
        ratio, r = utils.most_similar(utils.similarity(self.indexed_by_names.keys(), name, 0.75))
        #print(r)
        #print('-')
        return r

    def get_similar_items(self, text, text_list):
        r = []
        if len(text_list) > 0:
            #print('-')
            #print('get_similar_items')
            #print(text)
            ##print(text_list)
            ratio, r = utils.most_similar(utils.similarity(text_list, text, 0.75))
            #print(r)
            #print('-')
        return r

    def get_name_and_code_list(self, names):
        return [(name, self.indexed_by_names.get(name)) for name in names]

    def find_names(self, _code, _name):
        code_names = self.get_names(_code)
        names = []

        if _name in code_names:
            names = [_name]
        else:
            if len(code_names) > 0:
                names = self.get_similar_items(_name, code_names)
            if len(names) == 0:
                names = self.get_similar_names(_name)
        return (code_names, names)


def load_iso_countries():
    indexed_by_codes = {}
    indexed_by_names = {}
    for item in open(curr_path + '/../tables/new_country_names.csv', 'r').readlines():
        item = item.strip().split('|')
        if len(item) == 2:
            name, code = item
            indexed_by_names[name] = code
        if not code in indexed_by_codes.keys():
            indexed_by_codes[code] = []
        indexed_by_codes[code].append(name)
    return (indexed_by_codes, indexed_by_names)


def load_wos_countries():
    indexed_by_names = {}
    indexed_by_codes = {}
    for item in open(curr_path + '/../tables/country_en_pt_es.csv', 'r').readlines():
        if not isinstance(item, unicode):
            item = item.decode('utf-8')
        item = item.replace('"', '')
        item = item.strip().split('\t')
        if len(item) == 3:
            en, pt, es = item
            indexed_by_codes[en] = item
            indexed_by_names[en] = en
            indexed_by_names[pt] = en
            indexed_by_names[es] = en
    return (indexed_by_codes, indexed_by_names)


def load_br_states():
    indexed_by_names = {}
    indexed_by_codes = {}
    for item in open(curr_path + '/../tables/br_states.csv', 'r').readlines():
        if not isinstance(item, unicode):
            item = item.decode('utf-8')
        item = item.strip().split('|')
        if len(item) == 2:
            name, code = item
            indexed_by_codes[code] = [name]
            indexed_by_names[name] = code
    return (indexed_by_codes, indexed_by_names)


def load_br_locations():
    indexed_by_codes = {}
    indexed_by_names = {}
    for item in open(curr_path + '/../tables/br_locations.csv', 'r').readlines():
        if not isinstance(item, unicode):
            item = item.decode('utf-8')
        item = item.replace('"', '')
        item = item.strip().split('\t')
        if len(item) == 2:
            state, city = item
            if not city in indexed_by_names.keys():
                indexed_by_names[city] = []
            indexed_by_names[city].append(state)
            if not state in indexed_by_codes.keys():
                indexed_by_codes[state] = []
            indexed_by_codes[state].append(city)
    return (indexed_by_codes, indexed_by_names)


def load_normaff():
    indexed_by_codes = {}
    indexed_by_names = {}
    for item in open(curr_path + '/../tables/aff_normalized.txt', 'r').readlines():
        if not isinstance(item, unicode):
            item = item.decode('iso-8859-1')
        if len(item) > 0:
            item = item.strip().split('|')

            if len(item) == 2:
                orgname, wos_country_en = item
                indexed_by_names[orgname] = wos_country_en
                if not wos_country_en in indexed_by_codes.keys():
                    indexed_by_codes[wos_country_en] = []
                indexed_by_codes[wos_country_en].append(orgname)
    return (indexed_by_codes, indexed_by_names)


def get_all_normaff():
    results = []
    for item in open(curr_path + '/../tables/aff_normalized.txt', 'r').readlines():
        if not isinstance(item, unicode):
            item = item.decode('iso-8859-1')
        if len(item) > 0:
            item = item.strip().split('|')

            if len(item) == 2:
                orgname, country = item
                results.append(orgname + ' - ' + country)
    return results


def get_wos_country_items():
    codes, names = load_wos_countries()
    return CodesAndNames(codes, names)


def get_iso_country_items():
    codes, names = load_iso_countries()
    return CodesAndNames(codes, names)


def get_br_states():
    codes, names = load_br_states()
    return CodesAndNames(codes, names)


def get_locations():
    codes, names = load_br_locations()
    return CodesAndNames(codes, names)


def get_orgnames():
    codes, names = load_normaff()
    return CodesAndNames(codes, names)


def find_state_code(state):
    global br_state_list
    if br_state_list is None:
        br_state_list = get_br_states()

    state_code = None
    if state is not None:
        names = br_state_list.get_names(state)
        if len(names) > 0:
            state_code = state
        else:
            state_code = br_state_list.get_code(state, True)
    return state_code


def normalize_location(city, state):
    global location_list
    global br_state_list
    if location_list is None:
        location_list = get_locations()
    if br_state_list is None:
        br_state_list = get_br_states()

    norm_state = None
    norm_city = None
    errors = []

    norm_state = br_state_list.find_code(state)
    state_cities, city_names = location_list.find_names(state, city)
    valid_city_names = [name for name in city_names if name in state_cities]

    if len(valid_city_names) > 0:
        norm_city = valid_city_names[0]

    if norm_city is None:
        if len(city_names) > 0:
            norm_city = city_names[0]

    if norm_city is None:
        if not city is None:
            errors.append(city + ' was not identified as city.')
    if norm_state is None:
        if state is None:
            if not norm_city is None:
                city_states = location_list.get_code(norm_city, False)
                if len(city_states) > 0:
                    norm_state = city_states[0]
        else:
            errors.append(state + ' was not identified as state.')

    #print('--- normalize_location: resultado ---')
    #print([city, state])
    #print([norm_city, norm_state, '\n'.join(errors)])

    return (norm_city, norm_state, errors)


def find_country_names(country_name, country_code):
    global iso_country_list
    global wos_country_list

    if iso_country_list is None:
        iso_country_list = get_iso_country_items()
    if wos_country_list is None:
        wos_country_list = get_wos_country_items()

    if iso_country_list.get_code(country_name, False) is not None:
        iso_similar_name = country_name
    else:
        iso_similar_name = iso_country_list.get_similar_names(country_name)
        if len(iso_similar_name) > 0:
            iso_similar_name = iso_similar_name[0]
        else:
            iso_similar_name = None

    if wos_country_list.get_code(country_name, False) is not None:
        wos_similar_name = country_name
    else:
        wos_similar_name = wos_country_list.get_similar_names(country_name)
        if len(wos_similar_name) > 0:
            wos_similar_name = wos_similar_name[0]
        else:
            wos_similar_name = None

    code_names = iso_country_list.get_names(country_code)

    return (iso_similar_name, wos_similar_name, code_names)


def find_country_codes(iso_name, wos_name):
    global iso_country_list
    global wos_country_list

    if iso_country_list is None:
        iso_country_list = get_iso_country_items()
    if wos_country_list is None:
        wos_country_list = get_wos_country_items()

    iso_code = None
    wos_en = None

    if iso_name is not None:
        iso_code = iso_country_list.get_code(iso_name, False)
    if wos_name is not None:
        wos_en = wos_country_list.get_code(wos_name, False)

    return (iso_code, wos_en)


def normalize_country(country_name, country_code):
    global iso_country_list
    global wos_country_list

    if iso_country_list is None:
        iso_country_list = get_iso_country_items()
    if wos_country_list is None:
        wos_country_list = get_wos_country_items()

    norm_country_name = None
    norm_country_code = None
    errors = []

    iso_name, wos_name, code_names = find_country_names(country_name, country_code)
    #print([iso_name, wos_name, code_names])
    iso_code, wos_en = find_country_codes(iso_name, wos_name)
    #print([iso_code, wos_en])

    if country_code is None:
        country_code = iso_code
        code_names = [iso_name]

    if iso_name in code_names:
        norm_country_code = iso_code
    else:
        if len(code_names) > 0:
            errors.append(country_code + ' is code of ' + '|'.join(code_names))
        else:
            errors.append('No country was found which code is ' + country_code)

        if iso_code is not None:
            errors.append('code of ' + country_name + ' is: ' + iso_code)

    if wos_en is not None:
        norm_country_name = wos_en

    return (norm_country_name, norm_country_code, errors)


def get_country_name(country_code):
    global iso_country_list

    if iso_country_list is None:
        iso_country_list = get_iso_country_items()
    names = iso_country_list.get_names(country_code)
    if len(names) > 0:
        return names[0]


def normalized_affiliations(organizations_manager, orgname, country_name, country_code, state, city):
    errors = []
    normalized = []
    if country_code is None:
        #print(datetime.now().isoformat() + ' normalized_affiliations: indexedby_country_name')
        country_code = organizations_manager.indexedby_country_name.get(country_name)
        if country_code is None:
            #print(datetime.now().isoformat() + ' normalized_affiliations: normalize_country')
            country_name, country_code, errors = normalize_country(country_name, country_code)

    if country_code is not None:
        #print(datetime.now().isoformat() + ' normalized_affiliations: get_organizations')
        options = organizations_manager.get_organizations(orgname, city, state, country_code)
        #print(options)
        if len(options) == 0:
            #print(datetime.now().isoformat() + ' normalized_affiliations: country_orgnames')
            orgname_city_state_items = organizations_manager.country_orgnames(country_code)

            if city is not None and len(orgname_city_state_items) > 0:
                orgname_city_state_items = [[_orgname, _city, _state] for _orgname, _city, _state in orgname_city_state_items if _city == city]

            #print(datetime.now().isoformat() + ' normalized_affiliations: orgname_city_state_items')
            for _orgname, _city, _state in orgname_city_state_items:
                #print(_orgname)
                for word in orgname.split(' '):
                    #print('=>' + word)
                    if word in _orgname.split() and len(word) > 5:
                        #print('...' + _orgname)
                        normalized.append(', '.join([_orgname, _city, _state, country_code]))
                        break

            #print(datetime.now().isoformat() + ' normalized_affiliations: list(set(normalized))')
            normalized = [item.split(', ') for item in list(set(normalized))]
        else:
            #print(datetime.now().isoformat() + ' normalized_affiliations: if len(options) > 0')
            normalized = [[orgname, _city, _state, _country] for _city, _state, _country in options]
    #print(errors)
    #print(normalized)
    #print(datetime.now().isoformat() + ' normalized_affiliations: fim')
    return (errors, normalized)


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
        response = urllib2.urlopen(full_url, timeout=5)
        result = response.read()
    except Exception as e:
        print(e)
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
    return results


def validate_affiliation(org_manager, orgname, norgname, country, i_country, state, city):
    errors = []
    orgname_and_location_items = []

    #print(datetime.now().isoformat() + ' validate_affiliation: inicio')
    if norgname is not None:
        #print(datetime.now().isoformat() + ' validate_affiliation: normalized_affiliations 1')
        errors, orgname_and_location_items = normalized_affiliations(org_manager, norgname, country, i_country, state, city)
        #print(datetime.now().isoformat() + ' validate_affiliation: normalized_affiliations 2')
        #print(orgname_and_location_items)
    if len(errors) == 0:
        if len(orgname_and_location_items) == 0:
            if orgname is not None:
                #print(datetime.now().isoformat() + ' validate_affiliation: normalized_affiliations 3')
                errors, orgname_and_location_items = normalized_affiliations(org_manager, orgname, country, i_country, state, city)
                #print(datetime.now().isoformat() + ' validate_affiliation: normalized_affiliations 4')
                #print(orgname_and_location_items)
    return (errors, orgname_and_location_items)


def get_normalized_from_list(org_manager, orgname, country):
    errors, orgname_and_location_items = normalized_affiliations(org_manager, orgname, country, None, None, None)
    new = []
    for _orgname, city, state, _country in orgname_and_location_items:
        country_name = get_country_name(_country)
        if country_name is not None:
            new.append(_orgname + ' - ' + _country)
    return list(set(new))


def normaff_search(text):
    text = text.replace(' - ', ',')
    text = text.replace(';', ',')
    text = remove_sgml_tags(text)

    orgname = text[0:text.rfind(',')].strip()
    country = text[text.rfind(',')+1:].strip()
    results = get_normalized_from_wayta(orgname, country)
    org_manager = OrgManager()
    org_manager.load()
    results += get_normalized_from_list(org_manager, orgname, country)

    return sorted(list(set(results)))
