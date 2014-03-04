# coding=utf-8


import os
import shutil
from datetime import datetime
import xml.etree.ElementTree as etree

from StringIO import StringIO


MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }


def format_dateiso(self, adate):
    month = adate.get('season', adate.get('month', '00'))
    if not month.isdigit():
        if '-' in month:
            month = month[0:month.find('-')]
        month = MONTHS.get(month, '00')
    if month == '':
        month = '00'
    return adate.get('year', '0000') + month + adate.get('day', '00')


def xml_string(node):
    return etree.tostring(node) if node is not None else ''


def load_xml(content):
    def handle_mml_entities(content):
        if '<mml:' in content:
            temp = content.replace('<mml:math', 'BREAKBEGINCONSERTA<mml:math')
            temp = temp.replace('</mml:math>', '</mml:math>BREAKBEGINCONSERTA')
            replaces = [item for item in temp.split('BREAKBEGINCONSERTA') if '<mml:math' in item and '&' in item]
            for repl in replaces:
                content = content.replace(repl, repl.replace('&', 'MYMATHMLENT'))
        if '<math' in content:
            temp = content.replace('<math', 'BREAKBEGINCONSERTA<math')
            temp = temp.replace('</math>', '</math>BREAKBEGINCONSERTA')
            replaces = [item for item in temp.split('BREAKBEGINCONSERTA') if '<math' in item and '&' in item]
            for repl in replaces:
                content = content.replace(repl, repl.replace('&', 'MYMATHMLENT'))
        return content

    NAMESPACES = {'mml': 'http://www.w3.org/TR/MathML3/'}
    for prefix, uri in NAMESPACES.items():
        etree.register_namespace(prefix, uri)

    if not '<' in content:
        # is a file
        try:
            r = etree.parse(content)
        except Exception as e:
            content = open(content, 'r').read()

    if '<' in content:
        content = handle_mml_entities(content)

        try:
            r = etree.parse(StringIO(content))
        except Exception as e:
            print('XML is not well formed')
            print(e)
            r = None
    return r
