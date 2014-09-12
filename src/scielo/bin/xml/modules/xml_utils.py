# coding=utf-8

import xml.etree.ElementTree as etree

from StringIO import StringIO

from utils import u_encode


def normalize_space(s):
    if s is not None:
        while '\n' in s:
            s = s.replace('\n', ' ')
        while '\t' in s:
            s = s.replace('\t', ' ')
        while '\r' in s:
            s = s.replace('\r', ' ')
        while '  ' in s:
            s = s.replace('  ', ' ')
    return s


def node_text(node, exclude_root_tag=True):
    text = ''
    if not node is None:
        text = etree.tostring(node)
        if '<' in text[0:1]:
            text = text[text.find('>')+1:]
            text = text[0:text.rfind('</')]
    return text


def node_xml(node):
    text = ''
    if not node is None:
        text = etree.tostring(node)
    return text


def normalize_xml_ent(content):
    content = content.replace('&#x3C;', '&lt;')
    content = content.replace('&#x3E;', '&gt;')
    content = content.replace('&#x26;', '&amp;')
    content = content.replace('&#60;', '&lt;')
    content = content.replace('&#62;', '&gt;')
    content = content.replace('&#38;', '&amp;')
    return content


def convert_entities_to_chars(content, debug=False):
    import HTMLParser
    s = content

    content = normalize_xml_ent(content)

    if '&' in content:
        content = content.replace('&lt;', '<REPLACEENT>lt</REPLACEENT>')
        content = content.replace('&gt;', '<REPLACEENT>gt</REPLACEENT>')
        content = content.replace('&amp;', '<REPLACEENT>amp</REPLACEENT>')

    if '&' in content:
        h = HTMLParser.HTMLParser()
        if type(content) is str:
            content = content.decode('utf-8')
        content = h.unescape(content)

        if '&' in content:
            content = content.replace('&', 'REPLACEamp')
            content = content.replace('REPLACEamp' + '#', '&#')
            content = content.replace('REPLACEamp', '&amp;')

        content = u_encode(content, 'utf-8')

    if '<REPLACEENT>' in content:
        content = content.replace('<REPLACEENT>gt</REPLACEENT>', '&gt;')
        content = content.replace('<REPLACEENT>lt</REPLACEENT>', '&lt;')
        content = content.replace('<REPLACEENT>amp</REPLACEENT>', '&amp;')
    if debug:
        if s != content:
            print(s)
            print(content)
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
    return handle_mml_entities(convert_entities_to_chars(content))


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


def is_xml_well_formed(content):
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
