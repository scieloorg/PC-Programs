# coding=utf-8

import xml.etree.ElementTree as etree

from StringIO import StringIO


MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }


def normalize_space(s):
    if s is not None:
        while '\n' in s:
            s = s.replace('\n', ' ')
        while '  ' in s:
            s = s.replace('  ', ' ')
    return s


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
    if fpage is not None and lpage is not None:
        n = lpage
        if len(fpage) == len(lpage):
            i = 0
            n = ''
            for i in range(0, len(fpage)):
                if fpage[i:i+1] != lpage[i:i+1]:
                    n = lpage[i:]
                    break
                i += 1
        lpage = n if n != '' else None
    r = []
    if fpage is not None:
        r.append(fpage)
    if lpage is not None:
        r.append(lpage)
    return '-'.join(r)


def node_text(node, exclude_root_tag=True):
    text = node
    if not node is None:
        text = etree.tostring(node)
        if exclude_root_tag:
            if '>' in text:
                text = text[text.find('>')+1:]
                text = text[0:text.rfind('</')]
    return text


def convert_using_htmlparser(content):
    import HTMLParser
    entities = []

    h = HTMLParser.HTMLParser()
    new = content.replace('&', '_BREAK_&')
    parts = new.split('_BREAK_')
    for part in parts:
        if part.startswith('&'):
            ent = part[0:part.find(';')+1]
            if not ent in entities:
                try:
                    new_ent = h.unescape(ent).encode('utf-8', 'xmlcharrefreplace')
                except Exception as inst:
                    new_ent = ent
                    print('convert_using_htmlparser:')
                    print(ent)
                    print(inst)
                if not new_ent in ['<', '>', '&']:
                    content = content.replace(ent, new_ent)
                entities.append(ent)
    return content


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


def handle_entities(content):
    return handle_mml_entities(convert_using_htmlparser(content))


def load_xml(content):

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
        content = normalize_space(handle_entities(content))

        try:
            r = etree.parse(StringIO(content))
        except Exception as e:

            print('XML is not well formed')
            print(e)
            r = None
    return r
