# code = utf-8

import os


curr_path = os.path.dirname(__file__).replace('\\', '/')


iso_country_list = None


class CodesAndNames(object):

    def __init__(self, indexed_by_codes, indexed_by_names):
        self.indexed_by_codes = indexed_by_codes
        self.indexed_by_names = indexed_by_names

    def get_names(self, code):
        return self.indexed_by_codes.get(code, [])

    def get_code(self, name):
        return self.indexed_by_names.get(name)

    def find_code(self, text):
        code = None
        if text is not None:
            names = self.get_names(text)
            if len(names) > 0:
                code = text
            else:
                code = self.get_code(text, True)
        return code

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
    for item in open(curr_path + '/new_country_names.csv', 'r').readlines():
        item = item.strip().split('|')
        if len(item) == 2:
            name, code = item
            indexed_by_names[name] = code
        if not code in indexed_by_codes.keys():
            indexed_by_codes[code] = []
        indexed_by_codes[code].append(name)
    return (indexed_by_codes, indexed_by_names)


def get_iso_country_items():
    codes, names = load_iso_countries()
    return CodesAndNames(codes, names)


def get_code(country_name):
    global iso_country_list

    if iso_country_list is None:
        iso_country_list = get_iso_country_items()

    return iso_country_list.get_code(country_name)
