# coding=utf-8
import os
import shutil
import tempfile
import xml.etree.ElementTree as etree
import xml.dom.minidom

try:
    from io import StringIO
    import html.parser as html_parser
except ImportError:
    from StringIO import StringIO
    import HTMLParser as html_parser

from ..__init__ import _
from ..__init__ import TABLES_PATH
from . import fs_utils
from . import encoding


ENTITIES_TABLE = None

namespaces = {}
namespaces['mml'] = 'http://www.w3.org/1998/Math/MathML'
namespaces['xlink'] = 'http://www.w3.org/1999/xlink'
namespaces['xml'] = 'http://www.w3.org/XML/1998/namespace'

for namespace_id, namespace_link in namespaces.items():
    etree.register_namespace(namespace_id, namespace_link)


def date_element(date_node):
    d = None
    if date_node is not None:
        d = {}
        d['season'] = node_findtext(date_node, 'season')
        d['month'] = node_findtext(date_node, 'month')
        d['year'] = node_findtext(date_node, 'year')
        d['day'] = node_findtext(date_node, 'day')
    return d


def element_lang(node):
    if node is not None:
        return node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')


def load_entities_table():
    table = {}
    entities_filename = TABLES_PATH + '/entities.csv'
    if os.path.isfile(entities_filename):
        for item in fs_utils.read_file_lines(entities_filename):
            items = item.split('|')
            if len(items) == 5:
                symbol, number_ent, named_ent, descr, representation = items
                table[named_ent] = symbol
    else:
        encoding.debugging('load_entities_table()', 'NOT FOUND ' + entities_filename)
    encoding.display_message(entities_filename)
    encoding.display_message(len(table))
    return table


class XMLContent(object):

    def __init__(self, content):
        self.content = content.strip()
        if not self.content.endswith('>'):
            self.content = self.content[:self.content.rfind('>')+1]

    def normalize(self):
        self.content = complete_entity(self.content)
        self.content, replaced_named_ent = convert_entities_to_chars(self.content)

    def load_xml(self):
        self.xml, self.xml_error = load_xml(self.content)

    def fix(self):
        if '<' in self.content:
            self.content = self.content[self.content.find('<'):]
        self.content = self.content.replace(' '*2, ' '*1)

        self.load_xml()
        if self.xml is None:
            self._fix_open_and_close_style_tags()
            self.load_xml()

        if self.xml is None:
            self._fix_open_close()

    def _fix_open_close(self):
        changes = []
        parts = self.content.split('>')
        for s in parts:
            if '<' in s:
                if '</' not in s and '<!--' not in s and '<?' not in s:

                    s = s[s.find('<')+1:]
                    if ' ' in s and '=' not in s:
                        test = s[s.find('<')+1:]
                        changes.append(test)
        for change in changes:
            self.content = self.content.replace('<' + test + '>', '[' + test + ']')

    def _fix_open_and_close_style_tags(self):
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
                    encoding.debugging('_fix_problem()', '\ncurrent:' + tag)
                if tag.startswith('</'):
                    if debug:
                        encoding.debugging('_fix_problem()', 'expected')
                        encoding.debugging('_fix_problem()', expected_close_tags)
                        encoding.debugging('_fix_problem()', 'ign_list')
                        encoding.debugging('_fix_problem()', ign_list)
                    if tag in ign_list:
                        if debug:
                            encoding.debugging('_fix_problem()', 'remove from ignore')
                        ign_list.remove(tag)
                        parts[k] = ''
                    else:
                        matched = False
                        if len(expected_close_tags) > 0:
                            matched = (expected_close_tags[-1] == tag)
                            if not matched:
                                if debug:
                                    encoding.debugging('_fix_problem()', 'not matched')
                                while not matched and len(expected_close_tags) > 0:
                                    ign_list.append(expected_close_tags[-1])
                                    parts[k-1] += expected_close_tags[-1]
                                    del expected_close_tags[-1]
                                    matched = (expected_close_tags[-1] == tag)
                                if debug:
                                    encoding.debugging('_fix_problem()', '...expected')
                                    encoding.debugging('_fix_problem()', expected_close_tags)
                                    encoding.debugging('_fix_problem()', '...ign_list')
                                    encoding.debugging('_fix_problem()', ign_list)

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
        if '?>' in content:
            xml_proc = content[0:content.find('?>')+2]
        xml = content[1:]
        if '<' in xml:
            xml = xml[xml.find('<'):]
        if len(new_doctype) > 0:
            content = xml_proc + '\n' + new_doctype + '\n' + xml
        else:
            content = xml_proc + '\n' + xml
    return content


def apply_dtd(xml_filename, doctype):
    temp_filename = tempfile.mkdtemp() + '/' + os.path.basename(xml_filename)
    shutil.copyfile(xml_filename, temp_filename)
    content = replace_doctype(fs_utils.read_file(xml_filename), doctype)
    fs_utils.write_file(xml_filename, content)
    return temp_filename


def restore_xml_file(xml_filename, temp_filename):
    shutil.copyfile(temp_filename, xml_filename)
    fs_utils.delete_file_or_folder(temp_filename)
    fs_utils.delete_file_or_folder(os.path.dirname(temp_filename))


def new_apply_dtd(xml_filename, doctype):
    fs_utils.write_file(
        xml_filename,
        replace_doctype(fs_utils.read_file(xml_filename), doctype))


def node_findtext(node, xpath=None, multiple=False):
    # contrib.findtext('name/given-names')
    if node is None:
        return
    nodes = node
    if xpath is not None:
        if multiple is True:
            nodes = node.findall(xpath)
        else:
            nodes = node.find(xpath)
    if isinstance(nodes, list):
        return [node_text(item) for item in nodes]
    else:
        return node_text(nodes)


def node_text(node):
    text = tostring(node)
    if text is not None:
        text = text[text.find('>')+1:]
        if '</' in text:
            text = text[:text.rfind('</')]
        text = text.strip()
    return text


def node_xml(node):
    text = tostring(node)
    if node is not None and '&' in text:
        text, replaced_named_ent = convert_entities_to_chars(text)
    return text


def tostring(node):
    if node is not None:
        return encoding.decode(etree.tostring(node, encoding='utf-8'))


def complete_entity(xml_content):
    result = []
    for item in xml_content.replace('&#', '~BREAK~&#').split('~BREAK~'):
        if item.startswith('&#'):
            words = item.split(' ')
            if len(words) > 0:
                ent = words[0][2:]
                if ent.isdigit():
                    words[0] += ';'
            item = ' '.join(words)
        result.append(item)
    return ''.join(result)


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

    if '&' in content:
        text = content.replace('&', '_BREAK_&').replace(';', ';_BREAK_')
        entities = list(set([item for item in text.split('_BREAK_') if item.startswith('&') and item.endswith(';')]))
        if len(entities) > 0:
            global ENTITIES_TABLE

            if ENTITIES_TABLE is None:
                ENTITIES_TABLE = load_entities_table()
            if ENTITIES_TABLE is not None:
                for ent in entities:
                    new = ENTITIES_TABLE.get(ent, ent)
                    if new != ent:
                        replaced_named_ent.append(ent + '=>' + new)
                        content = content.replace(ent, new)
    return (content, replaced_named_ent)


def register_remaining_named_entities(content):
    if '&' in content:
        entities = []
        if os.path.isfile('./named_entities.txt'):
            entities = fs_utils.read_file_lines('./named_entities.txt')
        content = content[content.find('&'):]
        l = content.split('&')
        for item in l:
            if not item.startswith('#') and ';' in item:
                ent = item[0:item.find(';')]
                entities.append('&' + ent + ';')
        entities = sorted(list(set(entities)))
        if len(entities) > 0:
            fs_utils.write_file('./named_entities.txt', '\n'.join(entities))


def htmlent2char(content):
    if '&' in content:
        h = html_parser.HTMLParser()
        try:
            content = encoding.decode(content)
            content = h.unescape(content)
        except Exception as e:
            content = content.replace('&', '_BREAK_&').replace(';', ';_BREAK_')
            parts = content.split('_BREAK_')
            new = u''
            for part in parts:
                if part.startswith('&') and part.endswith(';'):
                    try:
                        part = h.unescape(part)
                    except Exception as e:
                        encoding.report_exception('htmlent2char(): h.unescape', e, part)
                        part = '??'
                try:
                    new += part
                except Exception as e:
                    encoding.report_exception('htmlent2char() 2', e, part)
                    new += '??'
                    encoding.report_exception('htmlent2char() 3', e, type(content))
                    encoding.report_exception('htmlent2char() 4', e, type(part))
                    x
            content = new
    return content


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
        content = htmlent2char(content)
        content = content.replace('&mldr;', u"\u2026")
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
    if '<' not in content:
        # is a file
        content = fs_utils.read_file(content)
    return content


def parse_xml(content):
    message = None
    try:
        r = etree.parse(StringIO(encoding.encode(content)))
    except Exception as e:
        message = 'XML is not well formed\n'
        msg = ''
        try:
            msg = encoding.decode(str(e))
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
            elif 'line ' in msg:
                line = msg[msg.find('line ')+len('line '):]
                column = ''
                if 'column ' in line:
                    column = line[line.find('column ')+len('column '):].strip()
                line = line[:line.find(',')].strip()
                if line.isdigit():
                    line = int(line)
                    lines = content.split('\n') if content is not None else ['']
                    col = len(lines[line-1])
                    if column.isdigit():
                        col = int(column)
                    msg += '\n...\n' + lines[line-1][:col] + '\n\n [[[[ ' + _('ERROR here') + ' ]]]] \n\n' + lines[line-1][col:] + '\n...\n'
        except:
            msg += ''
        message += msg

        r = None
    return (r, message)


def load_xml(content):
    content = read_xml(content)
    xml, e = parse_xml(content)
    return (xml, e)


def split_prefix(content):
    prefix = ''
    p = content.rfind('</')
    if p > 0:
        tag = content[p+2:]
        tag = tag[0:tag.find('>')].strip()
        if '<' + tag in content:
            prefix = content[:content.find('<' + tag)]
            content = content[content.find('<' + tag):].strip()
            content = content[:content.rfind('>') + 1].strip()
    return (prefix.replace('{PRESERVE_SPACE}', ''), content)


def preserve_styles(content):
    content = content.replace('> ', '>{PRESERVE_SPACE}')
    content = content.replace(' <', '{PRESERVE_SPACE}<')
    for tag in ['italic', 'bold', 'sup', 'sub']:
        content = content.replace('<' + tag + '>', '[' + tag + ']')
        content = content.replace('</' + tag + '>', '[/' + tag + ']')
    return content


def restore_styles(content):
    for tag in ['italic', 'bold', 'sup', 'sub']:
        content = content.replace('[' + tag + ']', '<' + tag + '>')
        content = content.replace('[/' + tag + ']', '</' + tag + '>')
    content = content.replace('{PRESERVE_SPACE}', ' ')
    return content


def remove_break_lines_off_element_content_item(item):
    if not item.startswith('<') and not item.endswith('>'):
        if item.strip() != '':
            item = ' '.join([item.split()])
    return item


def remove_break_lines_off_element_content(content):
    data = content.replace('>', '>~remove_break_lines_off_element_content~')
    data = data.replace('<', '~remove_break_lines_off_element_content~<')
    return ''.join([remove_break_lines_off_element_content_item(item) for item in data.split('~remove_break_lines_off_element_content~')]).strip()


def pretty_print(content):
    return PrettyXML(content).xml


def is_valid_xml_file(xml_path):
    r = False
    if os.path.isfile(xml_path):
        r = xml_path.endswith('.xml')
    return r


def is_valid_xml_dir(xml_path):
    total = 0
    if os.path.isdir(xml_path):
        total = len([item for item in os.listdir(xml_path) if item.endswith('.xml')])
    return total > 0


def is_valid_xml_path(xml_path):
    errors = []
    if xml_path is None:
        errors.append(_('Missing XML location. '))
    else:
        if os.path.isfile(xml_path):
            if not xml_path.endswith('.xml'):
                errors.append(_('Invalid file. XML file required. '))
        elif not is_valid_xml_dir(xml_path):
            errors.append(_('Invalid folder. Folder must have XML files. '))
    return errors


def remove_tags(content):
    if content is not None:
        content = content.replace('<', '~BREAK~<')
        content = content.replace('>', '>~BREAK~')
        parts = content.split('~BREAK~')
        new = []
        for item in parts:
            if item.startswith('<') and item.endswith('>'):
                pass
            else:
                new.append(item)
        content = ''.join(new)
    return content


def remove_exceeding_spaces_in_tag(item):
    if not item.startswith('<') and not item.endswith('>'):
        #if item.strip() == '':
        #    item = ''
        pass
    elif item.startswith('</') and item.endswith('>'):
        #close
        item = '</' + item[2:-1].strip() + '>'
    elif item.startswith('<') and item.endswith('/>'):
        #empty tag
        item = '<' + ' '.join(item[1:-2].split()) + '/>'
    elif item.startswith('<') and item.endswith('>'):
        #open
        item = '<' + ' '.join(item[1:-1].split()) + '>'
    return item


def remove_exceeding_spaces_in_all_tags(content):
    content = content.replace('>', '>NORMALIZESPACES')
    content = content.replace('<', 'NORMALIZESPACES<')
    content = ''.join([remove_exceeding_spaces_in_tag(item) for item in content.split('NORMALIZESPACES')])
    return content


def fix_styles_spaces(content):
    for style in ['bold', 'italic']:
        if content.count('</' + style + '> ') == 0 and content.count('</' + style + '>') > 0:
            content = content.replace('</' + style + '>', '</' + style + '> ')
        if content.count(' <' + style + '>') == 0 and content.count('<' + style + '>') > 0:
            content = content.replace('<' + style + '>', ' <' + style + '>')
    return content


def remove_exceding_style_tags(content):
    doit = True

    while doit is True:
        doit = False
        new = content
        for style in ['sup', 'sub', 'bold', 'italic']:
            new = new.replace('<' + style + '/>', '')
            new = new.replace('<' + style + '> ', ' <' + style + '>')
            new = new.replace(' </' + style + '>', '</' + style + '> ')
            new = new.replace('</' + style + '><' + style + '>', '')
            new = new.replace('<' + style + '></' + style + '>', '')
            new = new.replace('<' + style + '> </' + style + '>', ' ')
            new = new.replace('</' + style + '> <' + style + '>', ' ')
        doit = (new != content)
        content = new
    return new


class PrettyXML(object):

    def __init__(self, xml):
        self._xml = xml.replace('\r', '')

    def split_prefix(self):
        prefix = ''
        p = self._xml.rfind('</')
        p2 = self._xml.rfind('>')
        if p > 0 and p2 > 0:
            self._xml = self._xml[:p2 + 1]
            tag = self._xml[p + 2:p2]
            if '<' + tag in self._xml:
                prefix = self._xml[:self._xml.find('<' + tag)]
                self._xml = self._xml[self._xml.find('<' + tag):]
        self._xml = self._xml.strip()
        return prefix

    def minidom_pretty_print(self):
        try:
            doc = xml.dom.minidom.parseString(encoding.encode(self._xml))
            self._xml = encoding.decode(doc.toprettyxml().strip())
            ign = self.split_prefix()
        except Exception as e:
            encoding.report_exception('minidom_pretty_print()', e, self._xml)

    @property
    def xml(self):
        node, e = load_xml(self._xml)
        if node is not None:
            prefix = self.split_prefix()
            self.remove_exceding_style_tags()
            self.mark_valid_spaces()
            self.preserve_styles()
            self.minidom_pretty_print()
            self.restore_valid_spaces()
            self.restore_styles()
            self.remove_exceding_style_tags()
            return prefix + self._xml
        return self._xml

    def preserve_styles(self):
        for tag in ['italic', 'bold', 'sup', 'sub']:
            self._xml = self._xml.replace('<' + tag + '>', '[' + tag + ']')
            self._xml = self._xml.replace('</' + tag + '>', '[/' + tag + ']')

    def restore_styles(self):
        for tag in ['italic', 'bold', 'sup', 'sub']:
            self._xml = self._xml.replace('[' + tag + ']', '<' + tag + '>')
            self._xml = self._xml.replace('[/' + tag + ']', '</' + tag + '>')

    def restore_valid_spaces(self):
        self._xml = '\n'.join([item for item in self._xml.split('\n') if item.strip() != ''])
        self._xml = self._xml.replace('>', '>NORMALIZESPACES')
        self._xml = self._xml.replace('<', 'NORMALIZESPACES<')
        self._xml = ''.join([item if item.strip() == '' else item.strip() for item in self._xml.split('NORMALIZESPACES')])
        self._xml = self._xml.replace('PRESERVESPACES', ' ')

    def mark_valid_spaces(self):
        self._xml = self._xml.replace('>', '>NORMALIZESPACES')
        self._xml = self._xml.replace('<', 'NORMALIZESPACES<')
        self._xml = ''.join([self.insert_preserve_spaces_mark(item) for item in self._xml.split('NORMALIZESPACES')])

    def remove_exceding_style_tags(self):
        doit = True
        while doit is True:
            doit = False
            curr_value = self._xml

            for style in ['sup', 'sub', 'bold', 'italic']:
                tclose = '</' + style + '>'
                topen = '<' + style + '>'
                x = self._xml
                self._xml = self._xml.replace('<' + style + '/>', '')
                self._xml = self._xml.replace('<' + style + '> ', ' <' + style + '>')
                self._xml = self._xml.replace(' </' + style + '>', '</' + style + '> ')
                self._xml = self._xml.replace('</' + style + '> <' + style + '>', ' ')
                self._xml = self._xml.replace(tclose + topen, '')
                self._xml = self._xml.replace(topen + tclose, '')
                """
                if self._xml != x:
                    from datetime import datetime
                    it = datetime.now().isoformat()
                    print('changed', style)
                    fs_utils.write_file(style + '{}_antes.txt'.format(it), x)
                    fs_utils.write_file(style + '{}_depois.txt'.format(it), self._xml)
                """
            doit = (curr_value != self._xml)
        while ' '*2 in self._xml:
            self._xml = self._xml.replace(' '*2, ' ')

    def insert_preserve_spaces_mark(self, text):
        if text.startswith('<') and text.endswith('>'):
            text = '<' + ' '.join(text[1:-1].split()) + '>'
        elif text.strip() != '':
            text = text.replace(' ', 'PRESERVESPACES').replace('\n', 'PRESERVESPACES')
            text = ' '.join(text.split())
            while 'PRESERVESPACESPRESERVESPACES' in text:
                text = text.replace('PRESERVESPACESPRESERVESPACES', 'PRESERVESPACES')
        return text


class XMLNode(object):

    def __init__(self, root):
        self.root = root

    @property
    def xml(self):
        return node_xml(self.root)

    def nodes(self, xpaths):
        found_items = [self.root.findall(xpath) for xpath in xpaths]
        r = []
        for found in found_items:
            if found is not None:
                r.extend(found)
        return r

    def nodes_text(self, xpaths):
        return [node_text(node) for node in self.nodes(xpaths) if node is not None]

    def nodes_xml(self, xpaths):
        return [node_xml(node) for node in self.nodes(xpaths) if node is not None]

    def nodes_data(self, xpaths):
        return [(node_xml(node), node.attrib) for node in self.nodes(xpaths) if node is not None]
