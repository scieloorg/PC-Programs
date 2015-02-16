# code = utf-8

import os

curr_path = os.path.dirname(__file__).replace('\\', '/')

COUNTRY_CODES = {}
COUNTRY_NAMES = {}


def load():
    r = {}
    names = {}
    for item in open(curr_path + '/../tables/country_names.csv', 'r').readlines():
        item = item.strip().split('|')
        if len(item) > 1:
            name, code = item
            r[name] = code
        if not code in names.keys():
            names[code] = []
        names[code].append(name)
    return (r, names)


def get_names(country_code):
    return COUNTRY_NAMES.get(country_code)


def get_code(name):
    return COUNTRY_CODES.get(name)


def get_similar_names(country_name, country_list=None):
    import utils

    if country_list is None:
        country_list = COUNTRY_CODES.keys()
    return utils.ranking(utils.similarity(country_list, country_name), 0.5)


def get_items(names):
    return [(name, COUNTRY_CODES[name]) for name in names]


def get_icountry_names(name_and_code_items, i_country):
    return [name for name, code in name_and_code_items if code == i_country]


def is_valid_country(i_country, country_name):
    msg = []
    code_names = get_names(i_country)
    similar_names = get_similar_names(country_name)

    if code_names is None:
        msg.append(i_country + ' is a invalid value for @country.')

    if len(similar_names) == 0:
        msg.append(country_name + 'is a invalid value for country.')
    else:
        if not code_names is None:
            matched = [name for name in code_names if name in similar_names]
            if len(matched) == 0:
                msg.append('@country=' + i_country + ': ' + ';'.join(code_names))
                msg.append('country=' + country_name + ': ' + '|'.join([name + '(' + code + ')' for name, code in similar_names]))
    r = 'ERROR' if len(msg) > 0 else 'OK'
    return (r, '.\n'.join(msg))


if len(COUNTRY_NAMES) == 0:
    COUNTRY_CODES, COUNTRY_NAMES = load()
