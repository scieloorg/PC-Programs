# code = utf-8

import os

curr_path = os.path.dirname(__file__).replace('\\', '/')


wos_country_list = None
iso_country_list = None
br_state_list = None
orgname_list = None
location_list = None


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
        import utils
        return utils.ranking(utils.similarity(self.indexed_by_names.keys(), name), 0.5)

    def is_similar(self, text, text_list):
        import utils
        return utils.ranking(utils.similarity(text_list, text), 0.5)

    def get_name_and_code_list(self, names):
        return [(name, self.indexed_by_names.get(name)) for name in names]

    def find_names(self, _code, _name):
        code_names = self.get_names(_code)
        names = []

        if _name in code_names:
            names = [_name]
        else:
            if len(code_names) > 0:
                names = self.is_similar(_name, code_names)
            if len(names) == 0:
                names = self.similar_names(_name)
                if len(names) > 0:
                    names = [names[0]]
        return (code_names, names)

    def match_names(self, code_names, names):
        return [name for name in code_names if name in names]

    def match_report(self, _code, _name, code_names, names):
        msg = []
        matched = [name for name in code_names if name in names]
        if len(matched) == 0:
            if len(code_names) > 0:
                msg.append(_code + ': ' + '|'.join(code_names))
            else:
                msg.append(_code + ' is invalid.')
            if len(names) > 0:
                msg.append(_name + ': ' + '|'.join([name + '(' + self.get_code(name, False) + ')' for name in names]))
            else:
                msg.append(_name + ' is invalid.')
        return '\n'.join(msg)

    def select_names_by_code(self, name_and_code_items, selected_code):
        return [name for name, code in name_and_code_items if code == selected_code]


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
    return (indexed_by_names, indexed_by_codes)


def load_wos_countries():
    indexed_by_names = {}
    indexed_by_codes = {}
    for item in open(curr_path + '/../tables/country_en_pt_es.csv', 'r').readlines():
        item = item.strip().split('|')
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
        item = item.strip().split('\t')
        if len(item) == 3:
            state, ign, city = item
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
        item = item.strip().split('\t')
        if len(item) == 2:
            orgname, wos_country_en = item
            indexed_by_names[orgname] = wos_country_en
            if not wos_country_en in indexed_by_codes.keys():
                indexed_by_codes[wos_country_en] = []
            indexed_by_codes[wos_country_en].append(orgname)
    return (indexed_by_codes, indexed_by_names)


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


def check_location(city, state):
    global location_list
    global br_state_list
    if location_list is None:
        location_list = get_locations()
    if br_state_list is None:
        br_state_list = get_br_states()

    norm_state = br_state_list.find_code(state)
    state_cities, city_names = location_list.find_names(state, city)
    valid_city_names = location_list.match_names(state_cities, city_names)
    if len(valid_city_names) > 0:
        return (valid_city_names[0], norm_state)
    else:
        return location_list.match_report(norm_state, city, state_cities, city_names)


def find_country_names(country_name, country_code):
    global iso_country_list
    global wos_country_list

    if iso_country_list is None:
        iso_country_list = get_iso_country_items()
    if wos_country_list is None:
        wos_country_list = get_wos_country_items()

    if country_code is None:
        country_code = iso_country_list.get_code(country_name, True)

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


def check_country(country_name, country_code):
    global iso_country_list
    global wos_country_list

    if iso_country_list is None:
        iso_country_list = get_iso_country_items()
    if wos_country_list is None:
        wos_country_list = get_wos_country_items()

    iso_name, wos_name, code_names = find_country_names(country_name, country_code)
    iso_code, wos_en = find_country_codes(iso_name, wos_name)

    matched = (iso_name in code_names) and wos_en is not None
    if matched:
        return (wos_name, iso_code)
    else:
        msg = []
        if len(code_names) > 0:
            msg.append(country_code + ': ' + '|'.join(code_names))
        else:
            msg.append(country_code + ' is invalid.')
        if wos_en is None:
            msg.append(country_name + ' is invalid.')
        if iso_code is not None:
            msg.append(country_name + ': ' + iso_code)
        return '\n'.join(msg)


def check_orgname(orgname, country_name, country_code):
    global orgname_list

    if orgname_list is None:
        orgname_list = get_orgnames()

    r = None
    norm_country_name = None
    norm_country_code = None
    result = check_country(country_name, country_code)

    if isinstance(result, tuple):
        norm_country_name, norm_country_code = result

    if not norm_country_name is None:
        norm_country_orgnames = orgname_list.get_names(norm_country_name)
        if orgname in norm_country_orgnames:
            r = (orgname, norm_country_name, norm_country_code)
        else:
            similar_orgnames = orgname_list.is_similar(orgname, norm_country_orgnames)
            if len(similar_orgnames) > 0:
                r = (similar_orgnames[0], norm_country_name, norm_country_code)

    if r is None:
        similar_orgnames = orgname_list.get_similar_names(orgname)
        if len(similar_orgnames) > 0:
            orgname_and_country_items = {name:orgname_list.get_code(name, False) for name in similar_orgnames}
            msg.append(orgname + ': ' + '|'.join([name + '(' + country + ')' for name, country in orgname_and_country_items.items()]))
        else:
            msg.append(orgname + ' is invalid')

        if norm_country_name is None:
            msg.append(result)

        r = '.\n'.join(msg)
    return r


def validate_affiliation(orgname, norgname, country_name, country_code, state, city):
    _orgname = norgname if norgname is not None else orgname

    norm_orgname = None
    norm_country_name = None
    norm_country_code = None
    norm_state = state
    norm_city = city

    r = None
    result = check_orgname(_orgname, country_name, country_code)
    if isinstance(result, tuple):
        norm_orgname, norm_country_name, norm_country_code = result
        r = (norm_orgname, norm_country_name, norm_country_code, norm_state, norm_city)
        if norm_country_code == 'BR' or norm_country_name == 'Brazil':
            result = check_location(city, state)
            if isinstance(result, tuple):
                norm_city, norm_state = result
                r = (norm_orgname, norm_country_name, norm_country_code, norm_state, norm_city)

    if isinstance(r, tuple):
        return r
    else:
        return result
