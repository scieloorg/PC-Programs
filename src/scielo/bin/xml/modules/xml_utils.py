# coding=utf-8
import os
import shutil
import tempfile
import xml.etree.ElementTree as etree
import HTMLParser
from StringIO import StringIO


ENTITIES_TABLE = {}


def element_lang(node):
    if node is not None:
        return node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')


def load_entities_table():
    if len(ENTITIES_TABLE) == 0:
        curr_path = os.path.dirname(__file__).replace('\\', '/')
        if os.path.isfile(curr_path + '/../tables/entities.csv'):
            for item in open(curr_path + '/../tables/entities.csv', 'r').readlines():
                symbol, number_ent, named_ent, descr, representation = item.split('|')
                ENTITIES_TABLE[named_ent] = symbol
        else:
            print('NOT FOUND ' + curr_path + '/../tables/entities.csv')


class XMLContent(object):

    def __init__(self, content):
        self.content = content

    def fix(self):
        self.content = self.content[0:self.content.rfind('>')+1]
        self.content = self.content[self.content.find('<'):]
        self.content = self.content.replace(' '*2, ' '*1)
        if is_xml_well_formed(self.content) is None:
            self._fix_style_tags()
        if is_xml_well_formed(self.content) is None:
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
    content = content.replace('\r\n', '\n')
    if '<!DOCTYPE' in content:
        find_text = content[content.find('<!DOCTYPE'):]
        find_text = find_text[0:find_text.find('>')+1]
        if len(find_text) > 0:
            if len(new_doctype) > 0:
                content = content.replace(find_text, new_doctype)
            else:
                if find_text + '\n' in content:
                    content = content.replace(find_text + '\n', new_doctype)
    elif content.startswith('<?xml '):
        xml_proc = content[0:content.find('?>')+2]
        xml = content[1:]
        xml = xml[xml.find('<'):]
        if len(new_doctype) > 0:
            content = xml_proc + '\n' + new_doctype + '\n' + xml
        else:
            content = xml_proc + '\n' + xml
    return content


def apply_dtd(xml_filename, doctype):
    temp_filename = tempfile.mkdtemp() + '/' + os.path.basename(xml_filename)
    shutil.copyfile(xml_filename, temp_filename)
    content = replace_doctype(open(xml_filename, 'r').read(), doctype)
    open(xml_filename, 'w').write(content)
    return temp_filename


def restore_xml_file(xml_filename, temp_filename):
    shutil.copyfile(temp_filename, xml_filename)
    os.unlink(temp_filename)
    shutil.rmtree(os.path.dirname(temp_filename))


def strip(content):
    r = content.split()
    return ' '.join(r)


def node_text(node):
    text = node_xml(node)
    if not text is None:
        if text.startswith('<'):
            text = text[text.find('>')+1:]
            text = text[0:text.rfind('</')]
    return text


def node_xml(node):
    text = None
    if not node is None:
        text = etree.tostring(node)
    return text


def preserve_xml_entities(content):
    if '&' in content:
        content = content.replace('&#x0003C;', '<REPLACEENT>lt</REPLACEENT>')
        content = content.replace('&#x0003E;', '<REPLACEENT>gt</REPLACEENT>')
        content = content.replace('&#x00026;', '<REPLACEENT>amp</REPLACEENT>')
        content = content.replace('&#x003C;', '<REPLACEENT>lt</REPLACEENT>')
        content = content.replace('&#x003E;', '<REPLACEENT>gt</REPLACEENT>')
        content = content.replace('&#x0026;', '<REPLACEENT>amp</REPLACEENT>')
        content = content.replace('&#x03C;', '<REPLACEENT>lt</REPLACEENT>')
        content = content.replace('&#x03E;', '<REPLACEENT>gt</REPLACEENT>')
        content = content.replace('&#x026;', '<REPLACEENT>amp</REPLACEENT>')
        content = content.replace('&#x3C;', '<REPLACEENT>lt</REPLACEENT>')
        content = content.replace('&#x3E;', '<REPLACEENT>gt</REPLACEENT>')
        content = content.replace('&#x26;', '<REPLACEENT>amp</REPLACEENT>')

        content = content.replace('&#60;', '<REPLACEENT>lt</REPLACEENT>')
        content = content.replace('&#62;', '<REPLACEENT>gt</REPLACEENT>')
        content = content.replace('&#38;', '<REPLACEENT>amp</REPLACEENT>')
        content = content.replace('&lt;', '<REPLACEENT>lt</REPLACEENT>')
        content = content.replace('&gt;', '<REPLACEENT>gt</REPLACEENT>')
        content = content.replace('&amp;', '<REPLACEENT>amp</REPLACEENT>')
    return content


def named_ent_to_char(content):
    replaced_named_ent = []
    load_entities_table()
    if '&' in content:
        for find, replace in ENTITIES_TABLE.items():
            if find in content:
                replaced_named_ent.append(find + '=>' + replace)
                content = content.replace(find, replace)
    replaced_named_ent = list(set(replaced_named_ent))
    return (content, replaced_named_ent)


def register_remaining_named_entities(content):
    if '&' in content:
        entities = []
        if os.path.isfile('./named_entities.txt'):
            entities = open('./named_entities.txt', 'r').readlines()
        content = content[content.find('&'):]
        l = content.split('&')
        for item in l:
            if not item.startswith('#') and ';' in item:
                ent = item[0:item.find(';')]
                entities.append('&' + ent + ';')
        entities = sorted(list(set(entities)))
        if len(entities) > 0:
            open('./named_entities.txt', 'w').write('\n'.join(entities))


def all_ent_to_char(content):
    unicode_input = isinstance(content, unicode)
    r = content
    if '&' in content:
        h = HTMLParser.HTMLParser()
        u = content
        if not isinstance(content, unicode):
            u = u.decode('utf-8')
        u = h.unescape(u)
        r = u
        if isinstance(r, unicode):
            if not unicode_input:
                r = u.encode('utf-8')
    return r


def restore_xml_entities(content):
    if '<REPLACEENT>' in content:
        content = content.replace('<REPLACEENT>gt</REPLACEENT>', '&gt;')
        content = content.replace('<REPLACEENT>lt</REPLACEENT>', '&lt;')
        content = content.replace('<REPLACEENT>amp</REPLACEENT>', '&amp;')
    return content


def convert_entities_to_chars(content, debug=False):
    replaced_named_ent = []
    if '&' in content:
        content = preserve_xml_entities(content)
        content = all_ent_to_char(content)
        content, replaced_named_ent = named_ent_to_char(content)
        register_remaining_named_entities(content)

        content = restore_xml_entities(content)
    return content, replaced_named_ent


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


def read_xml(content):
    if not '<' in content:
        # is a file
        content = open(content, 'r').read()
    return content


def parse_xml(content):
    message = None
    try:
        r = etree.parse(StringIO(content))
    except Exception as e:
        #print('XML is not well formed')
        message = 'XML is not well formed\n'
        msg = str(e)
        if 'position ' in msg:
            pos = msg.split('position ')
            pos = pos[1]
            pos = pos[0:pos.find(': ')]
            if '-' in pos:
                pos = pos[0:pos.find('-')]
            if pos.isdigit():
                pos = int(pos)
            msg += '\n'
            text = content[0:pos]
            text = text[text.rfind('<'):]
            msg += text + '[[['
            msg += content[pos:pos+1]
            text = content[pos+1:]
            msg += ']]]' + text[0:text.find('>')+1]
        message += msg
        r = None
    return (r, message)


def is_xml_well_formed(content):
    node, e = parse_xml(content)
    if e is None:
        return node


def load_xml(content):
    content = read_xml(content)
    xml, e = parse_xml(content)
    return (xml, e)
