# coding=utf-8

import xml.etree.ElementTree as etree

from StringIO import StringIO


def normalize_space(s):
    if s is not None:
        while '\n' in s:
            s = s.replace('\n', ' ')
        while '  ' in s:
            s = s.replace('  ', ' ')
    return s


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
    print('conver ....')
    import HTMLParser
    s = content

    content = content.replace('&#x3C;', 'REPLACE_LT')
    content = content.replace('&#x3E;', 'REPLACE_GT')
    content = content.replace('&#x26;', 'REPLACE_AMP')
    content = content.replace('&lt;', 'REPLACE_LT')
    content = content.replace('&gt;', 'REPLACE_GT')
    content = content.replace('&amp;', 'REPLACE_AMP')

    h = HTMLParser.HTMLParser()
    if type(content) is str:
        content = content.decode('utf-8')
    if type(content) is unicode:
        content = h.unescape(content)
        try:
            content = content.encode('utf-8')
        except:
            try:
                content = content.encode('utf-8', 'xmlcharrefreplace')
            except:
                content = content.encode('utf-8', 'ignore')
    if '&' in content:
        content = content.replace('&', 'REPLACEamp')
        content = content.replace('REPLACEamp' + '#', '&#')
        content = content.replace('REPLACEamp', '&amp;')

    content = content.replace('REPLACE_GT;', '&gt;')
    content = content.replace('REPLACE_LT;', '&lt;')
    content = content.replace('REPLACE_AMP', '&amp;')

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
            print('parse ' + content)
            r = etree.parse(content)
        except Exception as e:
            print('read ' + content)
            content = open(content, 'r').read()

    if '<' in content:
        print('normalize xml')
        content = normalize_space(handle_entities(content))

        try:
            r = etree.parse(StringIO(content))
        except Exception as e:
            print('XML is not well formed')
            print(e)
            r = None
    return r
