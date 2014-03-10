# coding=utf-8

import xml.etree.ElementTree as etree

from StringIO import StringIO


MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }


def doi_pid(doi):
    pid = None

    if doi is not None:
        import urllib2
        import json

        try:
            f = urllib2.urlopen('http://dx.doi.org/' + doi)
            url = f.geturl()

            if 'scielo.php?script=sci_arttext&amp;pid=' in url:
                pid = url[url.find('pid=')+4:]
                pid = pid[0:23]

                try:
                    f = urllib2.urlopen('http://200.136.72.162:7000/api/v1/article?code=' + pid + '&format=json')
                    article_json = json.loads(f.read())
                    v880 = article_json['article'].get('v880')
                    v881 = article_json['article'].get('v881')

                    pid = v881 if v881 is not None else v880
                except:
                    pass
        except:
            pass
    return pid


def format_dateiso(adate):
    print(adate)
    if adate is not None:
        month = adate.get('season')
        if month is None:
            month = adate.get('month')
        else:
            if '-' in month:
                month = month[0:month.find('-')]
            month = MONTHS.get(month, '00')
        if month == '' or month is None:
            month = '00'
        y = adate.get('year', '0000')
        if y is None:
            y = '0000'
        d = adate.get('day', '00')
        if d is None:
            d = '00'
        return y + month + d


def display_pages(fpage, lpage):
    r = []
    if fpage is not None:
        r.append(fpage)
    if lpage is not None:
        r.append(lpage)

    return '-'.join(r)


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
