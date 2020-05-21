# coding=utf-8
import os
import html
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
    """
    Converte entidades numéricas ou nomeadas
    Especialmente as nomeadas porque quebram o XML e não é possível
    resolver com a biblioteca html
    """
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
    def __init__(self, str_or_filepath, do_changes=True, recover=False):
        self.do_changes = do_changes
        self.recover = recover
        self.changed = False
        self._xml = None
        self._content = None
        self.filename = None
        if os.path.isfile(str_or_filepath):
            self.filename = str_or_filepath
            try:
                str_or_filepath = fs_utils.read_file(self.filename)
            except UnicodeError:
                str_or_filepath = fs_utils.read_file(
                    self.filename, encode="iso-8859-1")
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

        self._xml, self.xml_error = load_xml(
            self._content, recover=self.recover)

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

    def write(self, dest_file_path, pretty_print=True,
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
    """
    Modo simplificado para carregar uma árvore de XML dado um arquivo
    """
    parser = xml_parser
    if parser is None:
        parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(file_path, parser)


def transform(xml_obj, xsl_file_path):
    """
    Aplica uma XSL dada pelo arquivo em uma árvore de XML
    O resutado é um `lxml.etree._XSLTResultTree`
    """
    xslt_doc = etree.parse(xsl_file_path)
    XSLT = etree.XSLT(xslt_doc)
    return XSLT(xml_obj)


def validate(xml_obj, dtd_external_id=None, dtd_file_path=None):
    """
    Valida contra uma DTD informando qual pelos parâmetros:
        dtd_external_id ou dtd_file_path
    """
    dtd_is_valid = False
    dtd_errors = []
    try:
        dtd = None
        if dtd_external_id:
            dtd = etree.DTD(external_id=dtd_external_id.encode())
        if not dtd and dtd_file_path:
            dtd = etree.DTD(StringIO(fs_utils.read_file(dtd_file_path)))
        if dtd:
            dtd_is_valid = dtd.validate(xml_obj)
            dtd_errors = dtd.error_log
    except Exception as e:
        dtd_errors = [str(e)]
    return dtd_is_valid, dtd_errors


def format_validations_msg(errors):
    """
    https://lxml.de/api/lxml.etree._LogEntry-class.html
    message: the message text
    domain: the domain ID (see lxml.etree.ErrorDomains)
    type: the message type ID (see lxml.etree.ErrorTypes)
    level: the log level ID (see lxml.etree.ErrorLevels)
    line: the line at which the message originated (if applicable)
    column: the character column at which the message originated (if applicable)
    filename: the name of the file in which the message originated (if applicable)
    path: the location in which the error was found (if available)
    """
    rows = []
    for e in errors:
        rows.append("{}: line: {} - {}".format(
            e.level, e.line, e.message
            ))
    return rows


def write(file_path, tree):
    """
    Escreve em arquivo o documento carregado na árvore
    tree pode ser de XML ou HTML
    """
    name, ext = os.path.splitext(file_path)
    if ext == ".xml":
        tree.write(
            file_path,
            encoding="utf-8",
            xml_declaration='<?xml version="1.0" encoding="utf-8"?>',
            inclusive_ns_prefixes=namespaces.keys(),
            pretty_print=True
        )
        return
    tree.write(file_path, method="html", pretty_print=True)


def node_xml_content(node):
    """
    Retorna o "tostring" interno ao node. Exemplo:
    node = "<p>texto 1 <bold> texto 2 </bold> texto 3</p>"
    Retorna `texto 1 <bold> texto 2 </bold> texto 3`
    """
    text = ''
    text += node.text or ''
    for child in node.getchildren():
        text += tostring(child, with_tail=True)
    return text


def tostring(node, pretty_print=False, with_tail=False):
    """
    Retorna o "tostring" do node. Exemplo:
    node = "<p>texto 1 <bold> texto 2 </bold> texto 3</p>"
    Retorna `<p>texto 1 <bold> texto 2 </bold> texto 3</p>`
    Retorna str
    """
    if node is not None:
        return encoding.decode(
            etree.tostring(
                node, encoding='utf-8',
                pretty_print=pretty_print,
                with_tail=with_tail
                ))


def load_xml(str_or_filepath, remove_blank_text=True, validate=False, recover=False):
    """
    Retorna uma árvore de XML e erros (se ocorrer ao carregá-lo)
    Pode receber o XML em str ou caminho de um arquivo
    Usado na conversao do Markup para XML
    """
    parser = etree.XMLParser(
        remove_blank_text=remove_blank_text,
        resolve_entities=True,
        recover=recover,
        dtd_validation=validate
    )
    try:
        xml = None
        errors = None
        if str_or_filepath.endswith(".xml"):
            source = str_or_filepath
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


def load_html(file_path):
    """
    Retorna uma árvore de HTML e erros (se ocorrer ao carregá-lo)
    Pode receber o XML em str ou caminho de um arquivo
    Usado na conversao do Markup para XML
    """
    parser = etree.HTMLParser(
        remove_blank_text=True, recover=True)
    try:
        html = None
        errors = None
        if file_path.endswith(".html") or file_path.endswith(".htm"):
            source = file_path
            html = etree.parse(file_path, parser)
        elif ">" not in file_path and "<" not in file_path:
            source = file_path
            raise ValueError(
                "Invalid value: it must be an HTML content or HTML file path")
        else:
            source = "str"
            if file_path.startswith('<?') and '?>' in file_path:
                file_path = file_path[file_path.find(
                    '?>')+2:].strip()
            html = etree.parse(StringIO(file_path), parser)
    except (etree.XMLSyntaxError,
            FileNotFoundError,
            ValueError, TypeError) as e:
        errors = "Loading HTML from '{}': {}".format(source, e)
    except Exception as e:
        errors = "Loading HTML from '{}': {}".format(source, e)
    finally:
        return html, errors


def pretty_print(content):
    xml, error = load_xml(content)
    return tostring(xml, pretty_print=True)


def is_valid_xml_dir(xml_path):
    """
    Verifica se a pasta contém arquivos XML
    Retorna True, se houver XML
    """
    total = 0
    if os.path.isdir(xml_path):
        total = len([item for item in os.listdir(xml_path) if item.endswith('.xml')])
    return total > 0


def get_errors_if_xml_not_found(xml_path):
    """
    Verifica se a pasta contém arquivos XML
    """
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
    """
    Remove tags de content
    """
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
    """
    Remove nós que combinam com o xpath dado
    """
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
    """
    Substitui o valor de atributos que combinam com elemento e nome de atributo
    """
    for attrname, value, new_value in tuple_attr_name_and_value_and_new_value:
        xpath = ".//*[@{}='{}']".format(attrname, value)
        for node in root.findall(xpath):
            node.set(attrname, new_value)


def find_nodes(root, xpaths):
    """
    Retorna os nodes que combinam com uma lista de xpaths
    """
    nodes = []
    for xpath in xpaths:
        nodes.extend(root.findall(xpath))
    return nodes


def nodes_xml_content_and_attributes(root, node_xpaths):
    """
    Retorna o resultado de `tostring(node), node.attrib` dos nodes
    que combinam com uma lista de xpaths
    """
    return [(tostring(node), node.attrib)
            for node in find_nodes(root, node_xpaths)]


def nodes_xml_content(root, node_xpaths):
    """
    Retorna node_xml_content(node) dos nodes
    que combinam com uma lista de xpaths
    """
    return [node_xml_content(node) for node in find_nodes(root, node_xpaths)]


def nodes_tostring(root, node_xpaths):
    """
    Retorna o resultado de tostring(node) dos nodes
    que combinam com uma lista de xpaths
    """
    return [tostring(node) for node in find_nodes(root, node_xpaths)]
