# coding=utf-8

import os

from ...generics import encoding


curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


wos_country_list = None
iso_country_list = None
br_state_list = None
orgname_list = None
location_list = None


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


def unicode2cp1252(results):
    r = []
    for item in results:
        item = encoding.decode(item)
        item = encoding.encode(item, 'cp1252', True)
        if len(item) > 0:
            r.append(item)
    return '\n'.join(r)


def display_results(results):
    print('\n'.join(sorted(results)))


def normaff_search(institutions_manager, text):

    text = remove_sgml_tags(text)

    orgname, country = text.split('|')
    if '(' in country:
        country = country[0:country.find('(')].strip()

    results = institutions_manager.search_institution_and_country_items(orgname, country, country)

    return results
