# coding=utf-8

import os

from ..__init__ import institutions_manager


curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


wos_country_list = None
iso_country_list = None
br_state_list = None
orgname_list = None
location_list = None


def normalize_term(term):
    if term is not None:
        if not isinstance(term, unicode):
            term = term.decode('utf-8')
        term = ' '.join([item.strip() for item in term.split()])
    return term


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


def validate_organization(orgname, norgname, country_name, country_code, state, city):
    normalized_results = []
    not_normalized_results = []
    if orgname is not None and norgname is not None:
        if orgname != norgname:
            if norgname is not None:
                normalized_results = institutions_manager.search_institutions(norgname, city, state, country_code, country_name)
            if orgname is not None:
                not_normalized_results = institutions_manager.search_institutions(orgname, city, state, country_code, country_name)
        else:
            normalized_results = institutions_manager.search_institutions(norgname, city, state, country_code, country_name)
    elif orgname is not None:
        not_normalized_results = institutions_manager.search_institutions(orgname, city, state, country_code, country_name)
    elif norgname is not None:
        normalized_results = institutions_manager.search_institutions(norgname, city, state, country_code, country_name)

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

    results = institutions_manager.search_institution_and_country_items(orgname, country, country)

    return results
