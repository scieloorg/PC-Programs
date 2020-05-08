# coding=utf-8

from ...generics import xml_utils
from ..data import attributes
from ..pkg_processors import xml_versions


messages = []


class SPSXMLContent(xml_utils.BrokenXML):
    """
    Aplica:
    - ajustes por migrações de versões SPS
    - normalizações porque os pacotes ser gerados por quaisquer ferramentas
    """

    def __init__(self, content):
        xml_utils.BrokenXML.__init__(self, content)

    def normalize(self):
        if self.xml is not None:
            if 'contrib-id-type="' in self.content:
                for contrib_id, url in attributes.CONTRIB_ID_URLS.items():
                    self.content = self.content.replace(' contrib-id-type="' + contrib_id + '">' + url, ' contrib-id-type="' + contrib_id + '">')
            #content = remove_xmllang_off_article_title(content)
            self.content = self.content.replace('http://creativecommons.org', 'https://creativecommons.org')
            self.content = self.content.replace('<comment content-type="cited"', '<comment')
            self.content = self.content.replace(' - </title>', '</title>').replace('<title> ', '<title>')
            self.content = self.content.replace('&amp;amp;', '&amp;')
            self.content = self.content.replace('&amp;#', '&#')
            self.content = self.content.replace('dtd-version="3.0"', 'dtd-version="1.0"')
            self.content = self.content.replace('publication-type="conf-proc"', 'publication-type="confproc"')
            self.content = self.content.replace('publication-type="legaldoc"', 'publication-type="legal-doc"')
            self.content = self.content.replace('publication-type="web"', 'publication-type="webpage"')
            self.content = self.content.replace(' rid=" ', ' rid="')
            self.content = self.content.replace(' id=" ', ' id="')
            self.remove_xmllang_from_element('article-title')
            self.remove_xmllang_from_element('source')
            self.content = self.content.replace('> :', '>: ')
            self.normalize_references()
            for tag in ['article-title', 'trans-title', 'kwd', 'source']:
                self.remove_styles_from_tagged_content(tag)
            self.content = self.content.replace('<institution content-type="normalized"/>', '')
            self.content = self.content.replace('<institution content-type="normalized"></institution>', '')
            self.content = xml_utils.pretty_print(self.content)

    def set_doctype(self, dtd_location_type):
        """
        Altera a localização da DTD (remota ou "local")
        Por local, significa sem o caminho completo, somente o nome do arquivo
        Para o site, é importante estar "local" para não demorar a carregar
        """
        local, remote = xml_versions.dtd_location(self.doctype)
        loc = '"{}"'.format(local)
        rem = '"{}"'.format(remote)
        if dtd_location_type == 'remote':
            self.doctype = self.doctype.replace(loc, rem)
        else:
            self.doctype = self.doctype.replace(rem, loc)
            self.doctype = self.doctype.replace(
                rem.replace('https:', 'http:'), loc)

    def remove_xmllang_from_element(self, tag):
        """
        Remove @xml:lang de dado elemento
        """
        xpath = ".//{}[@{http://www.w3.org/XML/1998/namespace}lang]".format(
            tag)
        for elem in self.xml.findall(xpath):
            elem.attrib.pop("{http://www.w3.org/XML/1998/namespace}lang")

    def remove_styles_from_tagged_content(self, tag):
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
            xml_utils.remove_styles_from_tagged_content(node, STYLES)

    def normalize_references(self):
        for ref in self.xml.findall(".//ref"):
            broken_ref = BrokenRef(ref)
            broken_ref.normalize()


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
