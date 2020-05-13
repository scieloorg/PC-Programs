# coding=utf-8
import os
from mimetypes import MimeTypes
from urllib.request import pathname2url

from ...generics import xml_utils
from ..data import attributes


messages = []
mime = MimeTypes()


class SPSXMLContent(xml_utils.SuitableXML):
    """
    Aplica:
    - ajustes por migrações de versões SPS
    - normalizações porque os pacotes ser gerados por quaisquer ferramentas
    """

    def __init__(self, file_path):
        xml_utils.SuitableXML.__init__(self, file_path)
        self._normalize()

    def _normalize(self):
        if self.xml is None:
            return
        # remove elementos
        xml_utils.remove_nodes(
            self.xml, ".//institution[@content-type='normalized']")

        for tag in ['article-title', 'trans-title', 'kwd', 'source']:
            self.remove_styles_off_tagged_content(tag)

        # remove atributos
        self.remove_attributes()

        # altera valor de elementos
        self.remove_uri_off_contrib_id()

        # altera valores de atributos
        xml_utils.replace_attribute_values(
            self.xml,
            (
                ('dtd-version', '3.0', '1.0'),
                ('publication-type', 'conf-proc', 'confproc'),
                ('publication-type', 'legaldoc', 'legal-doc'),
                ('publication-type', 'web', 'webpage'),
            )
        )
        self.replace_mimetypes()

        self.fix_content()
        self.normalize_references()

    def fix_content(self):
        """
        Conserta usando funcoes de str (melhorar futuramente)
        """
        content = self.content
        content = content.replace(
            'http://creativecommons.org', 'https://creativecommons.org')
        content = content.replace(
            ' - </title>', '</title>').replace('<title> ', '<title>')
        content = content.replace(' rid=" ', ' rid="')
        content = content.replace(' id=" ', ' id="')
        content = content.replace('> :', '>: ')
        self.content = content

    def remove_uri_off_contrib_id(self):
        if self.xml.find(".//contrib-id") is None:
            return
        for contrib_id_type, uri in attributes.CONTRIB_ID_URLS.items():
            xpath = ".//contrib-id[@contrib-id-type='{}']".format(
                contrib_id_type)
            for contrib_id in self.xml.findall(xpath):
                if uri in contrib_id.text:
                    contrib_id.text = contrib_id.text.replace(uri, "")

    def remove_attributes(self):
        """
        Remove atributos como:
        - @xml:lang de article-title e source
        - @content-type de comment
        """
        xpath_and_attr = (
            (".//comment[@content-type='cited']", 'content-type'),
            (".//article-title[@{http://www.w3.org/XML/1998/namespace}lang]",
             '{http://www.w3.org/XML/1998/namespace}lang'),
            (".//source[@{http://www.w3.org/XML/1998/namespace}lang]",
             '{http://www.w3.org/XML/1998/namespace}lang'),
            (".//*[@mime-subtype='replace']", 'mime-subtype'),
        )
        for xpath, attr in xpath_and_attr:
            xml_utils.remove_attribute(self.xml, xpath, attr)

    def remove_styles_off_tagged_content(self, tag):
        """
        As tags de estilo não devem ser aplicadas no conteúdo inteiro de
        certos elementos. As tags de estilo somente pode destacar partes do
        conteúdo de um dado elemento
        <source><italic>texto texto texto</italic></source> - não aceitável
        <source><italic>texto</italic> texto texto</source> - aceitável
        """
        STYLES = ("italic", "bold")
        nodes = []
        for style in STYLES:
            nodes.extend(self.xml.findall(".//{}[{}]".format(tag, style)))
        for node in set(nodes):
            xml_utils.merge_siblings_style_tags_content(node, STYLES)
            xml_utils.remove_styles_off_tagged_content(node, STYLES)

    def normalize_references(self):
        for ref in self.xml.findall(".//ref"):
            broken_ref = BrokenRef(ref)
            broken_ref.normalize()

    def replace_mimetypes(self):
        pkg_path = os.path.dirname(self.filename)
        for node in self.xml.findall(".//*[@mimetype]"):
            asset_filename = node.get("mimetype")
            if asset_filename.startswith('replace'):
                asset_filename = asset_filename.replace("replace", "")
                file_path = os.path.join(pkg_path, asset_filename)
                if os.path.isfile(file_path):
                    guessed_type = mime.guessed_type(file_path)
                else:
                    try:
                        location = pathname2url(file_path)
                        guessed_type = mime.guessed_type(location)
                    except Exception:
                        guessed_type = None
                if guessed_type and "/" in guessed_type:
                    m, ms = guessed_type.split("/")
                    node.set("mimetype", m)
                    node.set("mime-subtype", ms)


class BrokenRef(object):

    def __init__(self, tree):
        self.tree = tree
        self.content = xml_utils.tostring(self.tree)

    def normalize(self):
        self.insert_label_text_in_mixed_citation_text()
        self.fix_book_data()
        self.insert_ext_link_elements_in_mixed_citation()
        self.fix_source()

    def fix_book_data(self):
        """
        Renomeia as tags:
        article-title para chapter-title, na ausência de chapter-title
        chapter-title para source, na ausência de source
        """
        book = self.tree.find(".//element-citation[@publication-type='book']")
        if book is not None:
            chapter_title = book.find(".//chapter-title")
            source = book.find(".//source")
            if chapter_title is not None and source is not None:
                return
            article_title = book.find(".//article-title")
            if article_title is not None and chapter_title is not None:
                return
            if chapter_title is None and article_title is not None:
                article_title.tag = "chapter-title"
                article_title = book.find(".//article-title")
                chapter_title = book.find(".//chapter-title")
            if source is None and chapter_title is not None:
                chapter_title.tag = "source"
                chapter_title = book.find(".//chapter-title")
                source = book.find(".//source")

    def insert_ext_link_elements_in_mixed_citation(self):
        """
        Se no texto de mixed-citation há links não identificados como ext-link,
        inserir ext-link baseados nos ext-links existentes em element-citation
        """
        links = self.tree.findall(".//mixed-citation//ext-link")
        if links:
            return
        mixed_citation = self.tree.find(".//mixed-citation")
        if mixed_citation is None:
            return
        links = self.tree.findall(".//element-citation//ext-link")
        if not links:
            return
        mixed_citation_text = xml_utils.tostring(mixed_citation)
        for link in links:
            mixed_citation_text = mixed_citation_text.replace(
                link.text, xml_utils.tostring(link)
            )
        new_mixed_citation = xml_utils.etree.fromstring(mixed_citation_text)
        parent = mixed_citation.getparent()
        parent.replace(mixed_citation, new_mixed_citation)

    def insert_label_text_in_mixed_citation_text(self):
        """
        Insere o conteúdo de label no início de mixed-citation.
        """
        mixed_citation = self.tree.find(".//mixed-citation")
        if mixed_citation is None:
            return
        label = self.tree.find(".//label")
        if label is None:
            return
        if mixed_citation.text.startswith(label.text):
            return
        label_text = label.text
        if label.text[-1] == mixed_citation.text[0]:
            label_text = label_text[:-1]
        sep = " "
        if not mixed_citation.text[0].isalnum():
            sep = ""
        mixed_citation.text = label_text + sep + mixed_citation.text

    def fix_source(self):
        """
        Insere um espaço em branco após : caso não exista, dentro do elemento
        `source`
        <mixed-citation>Texto: texto2</mixed-citation>
        <source>Texto:texto2</source>

        Resultado:
        <source>Texto: texto2</source>
        """
        source = self.tree.find(".//source")
        if source is None:
            return
        if ":" in source.text and ": " not in source.text:
            mixed_citation = self.tree.find(".//mixed-citation")
            check = source.text.replace(":", ": ")
            mixed_citation_text = " ".join(mixed_citation.itertext())
            if check in mixed_citation_text:
                source.text = check
