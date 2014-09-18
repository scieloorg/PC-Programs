# coding=utf-8
import os
import shutil
import tempfile
import xml.etree.ElementTree as etree
from StringIO import StringIO

from utils import u_encode


class XMLContent(object):

    def __init__(self, content):
        self.content = content

    def fix(self):
        self.content = self.content[0:self.content.rfind('>')+1]
        self.content = self.content[self.content.find('<'):]
        self.content = self.content.replace(' '*2, ' '*1)
        if xml_utils.is_xml_well_formed(self.content) is None:
            self._fix_style_tags()
        if xml_utils.is_xml_well_formed(self.content) is None:
            self._fix_open_close()

    def _fix_open_close(self):
        changes = []
        parts = self.content.split('>')
        for s in parts:
            if '<' in s:
                if not '</' in s and not '<!--' in s and not '<?' in s:

                    s = s[s.find('<')+1:]
                    if ' ' in s and not '=' in s:
                        test = s[s.find('<')+1:]
                        changes.append(test)
        for change in changes:
            print(change)
            self.content = self.content.replace('<' + test + '>', '[' + test + ']')

    def _fix_style_tags(self):
        rcontent = self.content
        tags = ['italic', 'bold', 'sub', 'sup']
        tag_list = []
        for tag in tags:
            rcontent = rcontent.replace('<' + tag.upper() + '>', '<' + tag + '>')
            rcontent = rcontent.replace('</' + tag.upper() + '>', '</' + tag + '>')
            tag_list.append('<' + tag + '>')
            tag_list.append('</' + tag + '>')
            rcontent = rcontent.replace('<' + tag + '>',  'BREAKBEGINCONSERTA<' + tag + '>BREAKBEGINCONSERTA').replace('</' + tag + '>', 'BREAKBEGINCONSERTA</' + tag + '>BREAKBEGINCONSERTA')
        if self.content != rcontent:
            parts = rcontent.split('BREAKBEGINCONSERTA')
            self.content = self._fix_problem(tag_list, parts)
        for tag in tags:
            self.content = self.content.replace('</' + tag + '><' + tag + '>', '')

    def _fix_problem(self, tag_list, parts):
        expected_close_tags = []
        ign_list = []
        debug = False
        k = 0
        for part in parts:
            if part in tag_list:
                tag = part
                if debug:
                    print('\ncurrent:' + tag)
                if tag.startswith('</'):
                    if debug:
                        print('expected')
                        print(expected_close_tags)
                        print('ign_list')
                        print(ign_list)
                    if tag in ign_list:
                        if debug:
                            print('remove from ignore')
                        ign_list.remove(tag)
                        parts[k] = ''
                    else:
                        matched = False
                        if len(expected_close_tags) > 0:
                            matched = (expected_close_tags[-1] == tag)
                            if not matched:
                                if debug:
                                    print('not matched')
                                while not matched and len(expected_close_tags) > 0:
                                    ign_list.append(expected_close_tags[-1])
                                    parts[k-1] += expected_close_tags[-1]
                                    del expected_close_tags[-1]
                                    matched = (expected_close_tags[-1] == tag)
                                if debug:
                                    print('...expected')
                                    print(expected_close_tags)
                                    print('...ign_list')
                                    print(ign_list)

                            if matched:
                                del expected_close_tags[-1]
                else:
                    expected_close_tags.append(tag.replace('<', '</'))
            k += 1
        return ''.join(parts)


def remove_doctype(content):
    return replace_doctype(content, '')


def replace_doctype(content, new_doctype):
    if '\n<!DOCTYPE' in content:
        temp = content[content.find('\n<!DOCTYPE'):]
        temp = temp[0:temp.find('>')+1]
        if len(temp) > 0:
            content = content.replace(temp, new_doctype)
    elif content.startswith('<?xml '):
        temp = content
        temp = temp[0:temp.find('?>')+2]
        if len(new_doctype) > 0:
            content = content.replace(temp, temp + '\n' + new_doctype)
    return content


def apply_dtd(xml_filename, doctype):
    temp_filename = tempfile.mkdtemp() + '/' + os.path.basename(xml_filename)
    shutil.copyfile(xml_filename, temp_filename)
    content = replace_doctype(open(xml_filename, 'r').read(), doctype)
    open(xml_filename, 'w').write(content)
    return temp_filename


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
    content = content.replace('&#x000', '&#x')
    content = content.replace('&#x00', '&#x')
    content = content.replace('&#x0', '&#x')
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
    if not '<' in content:
        # is a file
        try:
            r = etree.parse(content)
        except Exception as e:
            content = open(content, 'r').read()

    if '<' in content:
        content = convert_entities_to_chars(content)

        try:
            r = etree.parse(StringIO(content))
        except Exception as e:
            print('XML is not well formed')
            print(e)
            open('./teste.xml', 'w').write(content)
            r = None
    return r


def is_xml_well_formed(content):
    return load_xml(content)
