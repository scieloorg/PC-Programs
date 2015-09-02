# coding=utf-8
import os
import shutil
import tempfile
import xml.etree.ElementTree as etree
import HTMLParser
from StringIO import StringIO

from __init__ import _


ENTITIES_TABLE = None


def date_element(date_node):
    d = None
    if date_node is not None:
        d = {}
        d['season'] = date_node.findtext('season')
        d['month'] = date_node.findtext('month')
        d['year'] = date_node.findtext('year')
        d['day'] = date_node.findtext('day')
    return d


def element_lang(node):
    if node is not None:
        return node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')


def load_entities_table():
    table = {}
    curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    if os.path.isfile(curr_path + '/../tables/entities.csv'):
        for item in open(curr_path + '/../tables/entities.csv', 'r').readlines():
            if not isinstance(item, unicode):
                item.decode('utf-8')
            symbol, number_ent, named_ent, descr, representation = item.split('|')
            table[named_ent] = symbol
    else:
        print('NOT FOUND ' + curr_path + '/../tables/entities.csv')
    return table


class XMLContent(object):

    def __init__(self, content):
        self.content = content

    def fix(self):
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
    import fs_utils
    temp_filename = tempfile.mkdtemp() + '/' + os.path.basename(xml_filename)
    shutil.copyfile(xml_filename, temp_filename)
    content = replace_doctype(fs_utils.read_file(xml_filename), doctype)
    fs_utils.write_file(xml_filename, content)
    return temp_filename


def restore_xml_file(xml_filename, temp_filename):
    shutil.copyfile(temp_filename, xml_filename)
    os.unlink(temp_filename)
    shutil.rmtree(os.path.dirname(temp_filename))


def remove_break_lines_characters(content):
    r = ' '.join(content.split())
    r = r.replace('> <', '><')
    r = r.replace(' </', '</')
    return r


def node_text(node):
    text = node_xml(node)
    if not text is None:
        text = text.strip()
        if text.startswith('<') and text.endswith('>'):
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
                    if not isinstance(new, unicode):
                        new = new.decode('utf-8')
                    if not isinstance(ent, unicode):
                        ent = ent.decode('utf-8')
                    #print(type(new))
                    #print(type(ent))
                    #print(new)
                    #print(ent)
                    if new != ent:
                        replaced_named_ent.append(ent + '=>' + new)
                        content = content.replace(ent, new)
    return (content, replaced_named_ent)


def register_remaining_named_entities(content):
    if '&' in content:
        entities = []
        if os.path.isfile('./named_entities.txt'):
            entities = open('./named_entities.txt', 'r').read()
            entities = entities.decode('utf-8').split('\n')
        content = content[content.find('&'):]
        l = content.split('&')
        for item in l:
            if not item.startswith('#') and ';' in item:
                ent = item[0:item.find(';')]
                entities.append('&' + ent + ';')
        entities = sorted(list(set(entities)))
        if len(entities) > 0:
            open('./named_entities.txt', 'w').write('\n'.join(entities).encode('utf-8'))


def htmlent2char(content):
    if '&' in content:
        h = HTMLParser.HTMLParser()
        try:
            if not isinstance(content, unicode):
                content = content.decode('utf-8')
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
                        print('h.unescape')
                        print(e)
                        print(part)
                        part = '??'
                try:
                    new += part
                except Exception as e:
                    print(e)
                    print(part)
                    new += '??'
                    print(type(content))
                    print(type(part))
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
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
    return content


def parse_xml(content):
    message = None
    try:
        if isinstance(content, unicode):
            content = content.encode('utf-8')
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
    else:
        print(e)


def load_xml(content):
    content = read_xml(content)
    xml, e = parse_xml(content)
    return (xml, e)


def fix_pretty(content):
    r = []
    is_data = False
    for line in content.split('\n'):
        if '</' in line:
            if is_data:
                line = line[line.find('</'):]
                is_data = False
        elif not '<' in line:
            line = '{DADO}' + line.strip() + '{DADO}'
            is_data = True
        else:
            is_data = False
        r.append(line)
    return '\n'.join(r).replace('\n{DADO}', '').replace('{DADO}\n', '').replace('{DADO}', '')


def pretty_print(content):
    content = content.replace('</', '=BREAK=</')
    content = content.replace(' <', '=BREAK=REPLACESPACE<')
    content = content.replace('> ', '>REPLACESPACE=BREAK=')
    content = content.replace('>', '>=BREAK=')
    content = content.replace('<', '=BREAK=<')

    items = content.split('=BREAK=')
    new = []
    for item in items:
        if not '<' in item and not '>' in item:
            if item.endswith(' '):
                item += 'REPLACESPACE'
            if item.startswith(' '):
                item = 'REPLACESPACE' + item

            check_item = ' '.join(item.split())
            if len(check_item) > 0:
                item = check_item
            item = item.replace('REPLACESPACE', ' ')
        new.append(item)

    return ''.join(new)


def old_pretty_print(content):
    pretty = None
    tag = None
    begin = ''
    if content.startswith('<?xml'):
        begin = content[0:content.find('?>')+2]
    if not content.startswith('<?xml'):
        if not is_xml_well_formed(content):
            tag = 'root'
            content = '<' + tag + '>' + content + '</' + tag + '>'

    if is_xml_well_formed(content):
        content = remove_break_lines_characters(content)
        import xml.dom.minidom
        try:
            if isinstance(content, unicode):
                content = content.encode('utf-8')
            doc = xml.dom.minidom.parseString(content)
            pretty = doc.toprettyxml()
            pretty = fix_pretty(pretty)
            if pretty.startswith('<?xml'):
                pretty = pretty[pretty.find('?>'):]
                pretty = pretty[pretty.find('<'):]
            pretty = begin + '\n' + pretty
        except Exception as e:
            print('ERROR in pretty')
            print(e)
            open('./pretty_print.xml', 'w').write(content)
            x

    if pretty is None:
        pretty = content
    if tag is not None:
        pretty = pretty.replace('<' + tag + '>', '').replace('</' + tag + '>', '')
    return pretty


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
        errors.append(_('Missing XML location.'))
    else:
        if os.path.isfile(xml_path):
            if not xml_path.endswith('.xml'):
                errors.append(_('Invalid file. XML file required.'))
        elif not is_valid_xml_dir(xml_path):
            errors.append(_('Invalid folder. Folder must have XML files.'))
    return errors


def remove_tags(content):
    content = content.replace('<', '~BREAK~<')
    content = content.replace('>', '>~BREAK~')
    parts = content.split('~BREAK~')
    new = []
    for item in parts:
        if item.startswith('<') and item.endswith('>'):
            pass
        else:
            new.append(item)
    return ''.join(new)
