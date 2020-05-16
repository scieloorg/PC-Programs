# coding=utf-8
import os
import shutil
import tempfile
import html
from copy import deepcopy
from io import StringIO

from lxml import etree

from ..__init__ import _
from . import fs_utils
from . import encoding

namespaces = {}
namespaces['xml'] = 'http://www.w3.org/XML/1998/namespace'
namespaces['xlink'] = 'http://www.w3.org/1999/xlink'
namespaces['mml'] = 'http://www.w3.org/1998/Math/MathML'

for namespace_id, namespace_link in namespaces.items():
    etree.register_namespace(namespace_id, namespace_link)


class Entity2Char:
    LT = (
        ('&#x0003C;', '<REPLACEENT>lt</REPLACEENT>'),
        ('&#x003C;', '<REPLACEENT>lt</REPLACEENT>'),
        ('&#x03C;', '<REPLACEENT>lt</REPLACEENT>'),
        ('&#x3C;', '<REPLACEENT>lt</REPLACEENT>'),
        ('&#60;', '<REPLACEENT>lt</REPLACEENT>'),
        ('&lt;', '<REPLACEENT>lt</REPLACEENT>'),
    )
    GT = (
        ('&#x0003E;', '<REPLACEENT>gt</REPLACEENT>'),
        ('&#x003E;', '<REPLACEENT>gt</REPLACEENT>'),
        ('&#x03E;', '<REPLACEENT>gt</REPLACEENT>'),
        ('&#x3E;', '<REPLACEENT>gt</REPLACEENT>'),
        ('&#62;', '<REPLACEENT>gt</REPLACEENT>'),
        ('&gt;', '<REPLACEENT>gt</REPLACEENT>'),
    )

    def __init__(self):
        pass

    def convert(self, content):
        if '&' not in content:
            return content
        for find, replace in self.LT + self.GT:
            content = content.replace(find, replace)
        content = html.unescape(content)
        content = html.unescape(content)
        if "&" in content:
            content = self._replace_incomplete_entity(content)
        content = content.replace("&", "&amp;")
        content = content.replace("<REPLACEENT>", "&")
        content = content.replace("</REPLACEENT>", ";")
        return content

    def _replace_incomplete_entity(self, content):
        result = []
        for item in content.replace('&', '~BREAK~&').split('~BREAK~'):
            if item.startswith('&'):
                ent = self._looks_like_entity(item)
                if ent and len(ent) > 2:
                    entity = ent
                    if entity[-1] != ";":
                        entity += ";"
                    print(entity)
                    new = html.unescape(entity)
                    if new != entity:
                        item = new + item[len(ent):]
            result.append(item)
        return ''.join(result)

    def _looks_like_entity(self, text):
        if len(text) < 2:
            return
        ent = "&"
        if text[1] == "#":
            for c in text[2:]:
                if c.isalnum():
                    ent += c
                    continue
                if c == ";":
                    ent += c
                break
        else:
            for c in text[1:]:
                if c.isalpha():
                    ent += c
                    continue
                if c == ";":
                    ent += c
                break
        return ent

entity2char = Entity2Char()


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


class SuitableXML(object):
    """
    XML adequado / aceitável
    - sem "junk" depois da última tag de fecha
    - garante que os conteúdos de elementos não tenha quebra de linha ou tab
    - garante que tenha entidades completas que terminam em ;
    - converte as entidades em caracteres, especialmente as "nomeadas" pois
    não são entidades aceitas no XML
    - preserva DOCTYPE original
    - preserva xml declaration original
    """
    def __init__(self, str_or_filepath, do_changes=True):
        self.do_changes = do_changes
        self.changed = False
        self._xml = None
        self._content = None
        self.filename = None
        if str_or_filepath.endswith(".xml"):
            self.filename = str_or_filepath
            str_or_filepath = fs_utils.read_file(self.filename)
        self.original = str_or_filepath
        self.content = str_or_filepath

    @property
    def xml_declaration(self):
        if self.original.startswith('<?xml'):
            return '<?xml version="1.0" encoding="utf-8"?>'
        if self.original.startswith("<?"):
            if self.xml is not None and self.xml.docinfo is not None:
                return '<?xml version="{}" encoding="{}"?>'.format(
                    self.xml.docinfo.xml_version, self.xml.docinfo.encoding)

    @property
    def doctype(self):
        if self.xml is not None and self.xml.docinfo is not None:
            return self.xml.docinfo.doctype

    @property
    def xml(self):
        return self._xml

    @property
    def content(self):
        """
        Retorna apenas o XML em si
        """
        if self._xml is None:
            return self._content
        return tostring(self._xml)

    @content.setter
    def content(self, value):
        """
        Atribui valor apenas para XML em si
        """
        self._content = value.strip()

        if self.do_changes and not self.changed:
            self.well_formed_xml_content()
            self.changed = True

        self._xml, self.xml_error = load_xml(self._content)

    def well_formed_xml_content(self):
        xml_content = self._content
        # padroniza os espaços, necessário pois há casos em que
        # foram inseridos quebras de linha dentro de conteúdo de elementos
        xml_content = " ".join([word for word in xml_content.split() if word])

        # remove "junk" (texto após a última tag)
        if not xml_content.endswith('>'):
            xml_content = xml_content[:xml_content.rfind('>')+1]

        # converte as entidades em caracteres, necesário especialmente para as
        # entidades "nomeadas" pois invalidam o XML
        xml_content = entity2char.convert(xml_content)
        self._content = xml_content

    def get_doctype(self, dtd_location_type=None):
        """
        Retorna doctype com system_url (remota ou "local")
        local: somente o nome do arquivo
        remote: url
        Para o site, é importante ser "local" para não demorar a carregar
        """
        if self.xml is not None and self.xml.docinfo:
            if dtd_location_type == 'local':
                url = self.xml.docinfo.system_url
                basename = os.path.basename(url)
                return self.xml.docinfo.doctype.replace(url, basename)
            return self.xml.docinfo.doctype or None

    def format(self, pretty_print=False, dtd_location_type=None):
        doctype = self.get_doctype(dtd_location_type)
        if self.xml is not None:
            return etree.tostring(
                self.xml, encoding="utf-8", method="xml",
                xml_declaration=self.xml_declaration,
                pretty_print=pretty_print, doctype=doctype
                ).decode("utf-8")
        return "\n".join([
                self.xml_declaration,
                self.doctype,
                self.content,
            ])
            

    def write(self, dest_file_path, pretty_print=False,
              dtd_location_type=None):
        doctype = self.get_doctype(dtd_location_type)
        if self.xml is None:
            fs_utils.write_file(
                dest_file_path, self.format(pretty_print, dtd_location_type))
        else:
            self.xml.write(
                dest_file_path, encoding="utf-8", method="xml",
                xml_declaration=self.xml_declaration,
                pretty_print=pretty_print, doctype=doctype)


def get_xml_object(file_path, xml_parser=None):
    parser = xml_parser
    if parser is None:
        parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(file_path, parser)


def get_xsl_object(file_path):
    xslt_doc = etree.parse(file_path)
    return etree.XSLT(xslt_doc)


def transform(xml_obj, xsl_obj):
    return xsl_obj(xml_obj)


def write(file_path, tree):
    tree.write(
        file_path,
        encoding="utf-8",
        xml_declaration='<?xml version="1.0" encoding="utf-8"?>',
        inclusive_ns_prefixes=namespaces.keys(),
    )


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
    copied = deepcopy(node)
    copied.tail = None
    return tostring(copied)


def tostring(node, pretty_print=False):
    if node is not None:
        return encoding.decode(etree.tostring(node, encoding='utf-8', pretty_print=pretty_print))


def load_xml(str_or_filepath):
    parser = etree.XMLParser(
        remove_blank_text=True, resolve_entities=True, recover=True)
    try:
        xml = None
        errors = None
        if str_or_filepath.endswith(".xml"):
            source = str_or_filepath
            print("AQI")
            xml = etree.parse(str_or_filepath, parser)
        elif ">" not in str_or_filepath and "<" not in str_or_filepath:
            source = str_or_filepath
            raise ValueError(
                "Invalid value: it must be an XML content or XML file path")
        else:
            source = "str"
            if str_or_filepath.startswith('<?') and '?>' in str_or_filepath:
                str_or_filepath = str_or_filepath[str_or_filepath.find(
                    '?>')+2:].strip()
            xml = etree.parse(StringIO(str_or_filepath), parser)
    except (etree.XMLSyntaxError,
            FileNotFoundError,
            ValueError, TypeError) as e:
        errors = "Loading XML from '{}': {}".format(source, e)
    except Exception as e:
        errors = "Loading XML from '{}': {}".format(source, e)
    finally:
        return xml, errors


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
    xml, error = load_xml(content)
    return tostring(xml, pretty_print=True)


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


def merge_siblings_style_tags_content(node, styles_tags):
    """
    Junta em um mesmo elemento, os elementos do mesmo estilo
    que estão adjacentes
    <bold>texto 1</bold> <bold>texto 2</bold>
    <bold>texto 1 texto 2</bold>
    """
    for elem in node.findall(".//*"):
        previous = elem.getprevious()
        if (elem.tag in styles_tags and previous is not None and
                previous.tag == elem.tag and
                not (previous.tail or "").strip()):
            if previous.text and elem.text:
                sep = " "
            elem.text = previous.text + sep + elem.text
            parent = previous.getparent()
            parent.remove(previous)


def remove_styles_off_tagged_content(node, styles_tags):
    """
    Remove as tags de estilos se elas estão aplicadas no elemento inteiro
    pois as tags de estilos só fazem sentido se aplicadas em partes do elemento
    <node><bold>texto</bold></node>
    <node>texto</node>
    """
    for elem in node.findall(".//*"):
        text = " ".join(node.itertext())
        if (elem.tag in styles_tags and
                " ".join(elem.itertext()).strip() == text.strip()):
            elem.tag = "REMOVE"
            etree.strip_tags(node, "REMOVE")


def remove_nodes(root, xpath):
    for node in root.findall(xpath):
        parent = node.getparent()
        parent.remove(node)


def remove_attribute(root, xpath, attr_name):
    """
    Localiza nodes por xpath
    Remove o atributo cujo nome é attr_name
    """
    for node in root.findall(xpath):
        if node.get(attr_name):
            node.attrib.pop(attr_name)


def replace_attribute_values(root, tuple_attr_name_and_value_and_new_value):
    for attrname, value, new_value in tuple_attr_name_and_value_and_new_value:
        xpath = ".//*[@{}='{}']".format(attrname, value)
        for node in root.findall(xpath):
            node.set(attrname, new_value)


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
