# coding=utf-8

import sqlite3

from .. import fs_utils
from .. import encoding


class SQL(object):

    def __init__(self, db_filename):
        self.db_filename = db_filename

    def create_db(self, schema_filename):
        with sqlite3.connect(self.db_filename) as conn:
            conn.executescript(fs_utils.read_file(schema_filename))

    def insert_data(self, csv_filename, table_name, fields):
        conn = sqlite3.connect(self.db_filename)
        _fields = ', '.join(fields)

        for row in fs_utils.read_file_lines(csv_filename):
            items = row.split('\t')

            if len(items) == len(fields):
                _values = []
                for item in items:
                    if '"' not in item:
                        _values.append('"' + item.replace('  ', ' ').strip() + '"')
                    elif "'" not in item:
                        _values.append("'" + item.replace('  ', ' ').strip() + "'")
                    else:
                        _values.append('`' + item.replace('  ', ' ').strip() + '`')
                instruction = 'insert into ' + table_name + ' (' + _fields + ') ' + ' values (' + ', '.join(_values) + ')'
                encoding.debugging('insert_data()', instruction)
                conn.execute(instruction + '\n')
                conn.commit()
        conn.close()

    def query(self, expr):
        results = []
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(expr)
                for row in cursor.fetchall():
                    results.append(row)
            except Exception as e:
                encoding.report_exception('query()', e, ('ERROR: query', expr))
                encoding.debugging('query()', expr)
        conn.close()
        return results

    def query_one(self, expr):
        results = []
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(expr)
            results = cursor.fetchone()
        conn.close()
        return results

    def get_select_statement(self, table_name, fields, where_expr=None):
        if where_expr is None:
            where_expr = ''
        else:
            where_expr = ' where ' + where_expr
        expr = 'select ' + ', '.join(fields) + ' from ' + table_name + where_expr
        return expr

    def format_expr(self, labels, values, connector=' OR '):
        expr = [label + '="' + encoding.encode(value.replace('"', '')) + '"' for label, value in zip(labels, values) if value is not None]
        return connector.join(expr)
