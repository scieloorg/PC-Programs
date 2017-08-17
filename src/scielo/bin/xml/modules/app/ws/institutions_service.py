# coding=utf-8

from ...generics import encoding


wos_country_list = None
iso_country_list = None
br_state_list = None
orgname_list = None
location_list = None


def remove_sgml_tags(text):
    text = text.replace('[', '***BREAK***IGNORE[')
    text = text.replace(']', ']IGNORE***BREAK***')
    items = [item for item in text.split('***BREAK***') if not item.endswith(']IGNORE') and not item.startswith('IGNORE[')]
    return ''.join(items)


def unicode2cp1252_item(item):
    return encoding.encode(encoding.decode(item), 'cp1252', True)


def unicode2cp1252(results):
    items = [unicode2cp1252_item(item) for item in results]
    return '\n'.join([item for item in items if len(item) > 0])


def normaff_search(institutions_manager, text):

    text = remove_sgml_tags(text)

    orgname, country = text.split('|')
    if '(' in country:
        country = country[0:country.find('(')].strip()

    results = institutions_manager.search_institution_and_country_items(
        orgname, country, country)

    return results
