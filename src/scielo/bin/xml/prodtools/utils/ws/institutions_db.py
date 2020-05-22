# coding=utf-8

import os

from prodtools.utils import encoding
from prodtools.utils import fs_utils
from prodtools.utils.dbm import dbm_sql

from prodtools import TABLES_PATH


def normalize_term(term):
    if term is not None:
        term = encoding.decode(term)
        term = ' '.join([item.strip() for item in term.split()])
    return term


class InstitutionsDBManager(object):

    def __init__(self):
        self.db_filename = TABLES_PATH + '/xc.db'
        self.sql = dbm_sql.SQL(self.db_filename)
        self.csv_filename = TABLES_PATH + '/orgname_location_country.csv'
        self.schema_filename = TABLES_PATH + '/xc.sql'
        self.fields = ['name', 'city', 'state', 'country_code', 'country_name']
        self.table_name = 'institutions'
        if not os.path.isfile(self.db_filename):
            self.create_db()
        self.normalized_country_items = self.get_country_items()

    def create_db(self):
        fs_utils.delete_file_or_folder(self.db_filename)
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
            if country_code is not None:
                country_name = self.normalized_country_items.get(country_code)
        else:
            if country_name not in self.normalized_country_items.values():
                country_name = None
        return country_name

    def get_institutions(self, orgname, city, state, country_code, country_name):
        orgname, city, state, country_code, country_name = [normalize_term(item) for item in [orgname, city, state, country_code, country_name]]
        norm_country_name = self.normalized_country_name(country_code, country_name)
        if norm_country_name is not None and country_code is None:
            country_code = self.normalized_country_items.get(norm_country_name)
        results = self.institution_exists(orgname, city, state, country_code, norm_country_name)

        if not len(results) == 1:
            _results = self.institution_exists(orgname, None, None, country_code, norm_country_name)
            if len(_results) == 1:
                results = _results
            else:
                results += _results

        results = list(set(results))
        return results

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
        orgname = orgname.replace('"', '')
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
