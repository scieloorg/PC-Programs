# coding=utf-8
import os
import shutil
import tempfile
import xml.etree.ElementTree as etree
import HTMLParser
from StringIO import StringIO
import xml.dom.minidom

from __init__ import _
import fs_utils


ENTITIES_TABLE = None

namespaces = {}
namespaces['mml'] = 'http://www.w3.org/1998/Math/MathML'
namespaces['xlink'] = 'http://www.w3.org/1999/xlink'
namespaces['xml'] = 'http://www.w3.org/XML/1998/namespace'

for namespace_id, namespace_link in namespaces.items():
    etree.register_namespace(namespace_id, namespace_link)


def get_unicode(s):
    u = s
    if not isinstance(u, unicode):
        u = s.decode('utf-8')
    return u


def get_string(u):
    s = u
    if isinstance(u, unicode):
        s = u.encode('utf-8')
    return s


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
        if '<' in self.content:
            self.content = self.content[self.content.find('<'):]
        self.content = self.content.replace(' '*2, ' '*1)

        _xml, e = load_xml(self.content)
        if _xml is None:
            self._fix_open_and_close_style_tags()
            _xml, e = load_xml(self.content)
        if _xml is None:
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
    os.unlink(temp_filename)
    shutil.rmtree(os.path.dirname(temp_filename))


def remove_break_lines_characters(content):
    r = ' '.join(content.split())
    r = r.replace(' </', '</')
    return r


def node_text(node):
    text = node_xml(node)
    if not text is None:
        text = text.strip()
        if text.startswith('<') and text.endswith('>'):
            text = text[text.find('>')+1:]
            if '</' in text:
                text = text[0:text.rfind('</')]
                text = text.strip()
    return text


def node_xml(node):
    text = None
    if not node is None:
        text = etree.tostring(node)
        if '&' in text:
            text, replaced_named_ent = convert_entities_to_chars(text)
    return text


def tostring(node):
    return etree.tostring(node)


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
        elif 'line ' in msg:
            line = msg[msg.find('line ')+len('line '):]
            column = ''
            if 'column ' in line:
                column = line[line.find('column ')+len('column '):].strip()
            line = line[:line.find(',')].strip()
            if line.isdigit():
                line = int(line)
                lines = content.decode('utf-8').split('\n')
                col = len(lines[line-1])
                if column.isdigit():
                    col = int(column)
                msg += '\n...\n' + lines[line-1][:col] + '\n\n [[[[ ' + _('ERROR here') + ' ]]]] \n\n' + lines[line-1][col:] + '\n...\n'

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


def minidom_pretty_print(content):
    pretty = None

    try:
        content = content.replace('\r', '')
        content = ' '.join([item for item in content.split('\n')])
        content = preserve_styles(content)
        content = remove_exceeding_spaces_in_all_tags(content)
        prefix, content = split_prefix(content)

        if isinstance(content, unicode):
            content = content.encode('utf-8')

        print(content[content.find('Stern et al'):content.find('Stern et al')+400])
        doc = xml.dom.minidom.parseString(content)
        pretty = doc.toprettyxml().strip()
        if not isinstance(pretty, unicode):
            pretty = pretty.decode('utf-8')

        ign, pretty = split_prefix(pretty)
        pretty = '\n'.join([item for item in pretty.split('\n') if item.strip() != ''])

        pretty = remove_break_lines_off_element_content(pretty)

        pretty = restore_styles(pretty)
        pretty = prefix + remove_exceding_style_tags(pretty).strip()
    except Exception as e:
        print('ERROR in pretty')
        print(e)
        print(content)
        #print(pretty)
        fs_utils.write_file('./pretty_print.xml', content)
        raise
    return pretty


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
            item = ' '.join([w for w in item.split()])
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
        errors.append(_('Missing XML location.'))
    else:
        if os.path.isfile(xml_path):
            if not xml_path.endswith('.xml'):
                errors.append(_('Invalid file. XML file required.'))
        elif not is_valid_xml_dir(xml_path):
            errors.append(_('Invalid folder. Folder must have XML files.'))
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


def format_text_as_xml(text):
    prefix = '<root'
    for n_id, n_link in namespaces.items():
        prefix += ' xmlns:' + n_id + '=' + '"' + n_link + '"'
    prefix += '>'

    pretty = pretty_print(prefix + text + '</root>')
    if pretty is not None:
        if '<root' in pretty:
            pretty = pretty[pretty.find('<root'):]
            pretty = pretty[pretty.find('>') + 1:].replace('</root>', '')
            text = pretty
    return text


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
        import xml.dom.minidom
        try:
            doc = xml.dom.minidom.parseString(get_string(self._xml))
            self._xml = get_unicode(doc.toprettyxml().strip())
            ign = self.split_prefix()
        except Exception as e:
            print('ERROR in minidom_pretty_print')
            print(e)
            print(self._xml)
            raise

    @property
    def xml(self):
        prefix = self.split_prefix()
        self.normalize_spaces_in_xml()
        self.preserve_styles()
        self.minidom_pretty_print()
        self.remove_inconvenient_break_lines()
        self.restore_styles()
        self.remove_exceding_style_tags()
        while ' '*2 in self._xml:
            self._xml = self._xml.replace(' '*2, ' ')
        return prefix + self._xml

    def preserve_styles(self):
        for tag in ['italic', 'bold', 'sup', 'sub']:
            self._xml = self._xml.replace('<' + tag + '>', '[' + tag + ']')
            self._xml = self._xml.replace('</' + tag + '>', '[/' + tag + ']')

    def restore_styles(self):
        for tag in ['italic', 'bold', 'sup', 'sub']:
            self._xml = self._xml.replace('[' + tag + ']', '<' + tag + '>')
            self._xml = self._xml.replace('[/' + tag + ']', '</' + tag + '>')

    def remove_inconvenient_break_lines(self):
        self._xml = '\n'.join([item for item in self._xml.split('\n') if item.strip() != ''])
        self._xml = self._xml.replace('>', '>NORMALIZESPACES')
        self._xml = self._xml.replace('<', 'NORMALIZESPACES<')
        self._xml = ''.join([self.fix_line(item) for item in self._xml.split('NORMALIZESPACES')])

    def normalize_spaces_in_xml(self):
        self._xml = self._xml.replace('>', '>NORMALIZESPACES')
        self._xml = self._xml.replace('<', 'NORMALIZESPACES<')
        self._xml = ''.join([self.normalize_spaces_in_xml_item(item) for item in self._xml.split('NORMALIZESPACES')])

    def remove_exceding_style_tags(self):
        doit = True
        while doit is True:
            doit = False
            curr_value = self._xml

            for style in ['sup', 'sub', 'bold', 'italic']:
                self._xml = self._xml.replace('<' + style + '/>', '')
                self._xml = self._xml.replace('<' + style + '> ', ' <' + style + '>')
                self._xml = self._xml.replace(' </' + style + '>', '</' + style + '> ')
                self._xml = self._xml.replace('</' + style + '><' + style + '>', '')
                self._xml = self._xml.replace('<' + style + '></' + style + '>', '')
                self._xml = self._xml.replace('<' + style + '> </' + style + '>', ' ')
                self._xml = self._xml.replace('</' + style + '> <' + style + '>', ' ')
            doit = (curr_value != self._xml)

    def normalize_spaces_in_xml_item(self, text):
        if text.startswith('<') and text.endswith('>'):
            text = '<' + ' '.join(text[1:-1].split()) + '>'
        elif text.strip() == '':
            pass
        else:
            text = text.replace(' ', 'PRESERVESPACES').replace('\n', 'PRESERVESPACES')
            text = ' '.join(text.split())
            while 'PRESERVESPACESPRESERVESPACES' in text:
                text = text.replace('PRESERVESPACESPRESERVESPACES', 'PRESERVESPACES')
        return text

    def fix_line(self, item):
        if item.strip() != '':
            item = item.strip()
        return item.replace('PRESERVESPACES', ' ')
