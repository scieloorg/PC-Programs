# code = utf-8

import os

curr_path = os.path.dirname(__file__).replace('\\', '/')

_country = {}


def load():
    r = {}
    for item in open(curr_path + '/../tables/country_names.csv', 'r').readlines():
        item = item.strip().split('|')
        if len(item) > 1:
            name, code = item
            r[name] = code
    return r


def get_names(country_code):
    return [name for name, code in _country.items() if code == country_code]


def get_code(name):
    return _country.get(name)


def similar_names(country_name):
    import utils
    r = []
    best_matches = utils.best_matches(utils.similarity_ranking(_country.keys(), country_name), 0.5)
    for item in best_matches:
        r.append((item, _country[item]))
    return r


if len(_country) == 0:
    _country = load()
