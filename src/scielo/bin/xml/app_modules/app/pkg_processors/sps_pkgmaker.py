# coding=utf-8
import logging
import logging.config
import os
from mimetypes import MimeTypes
from urllib.request import pathname2url

from packtools.utils import SPPackage

from ...generics import fs_utils
from ...generics import xml_utils
from ..data import attributes
from ..data import workarea
from ..data import package


messages = []
mime = MimeTypes()
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class SPSXMLContent(xml_utils.SuitableXML):
    """
    Aplica:
    - ajustes por migrações de versões SPS
    - normalizações porque os pacotes ser gerados por quaisquer ferramentas
    """

    def __init__(self, file_path):
        self.pkg_path = os.path.dirname(file_path)

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
        for node in self.xml.findall(".//*[@mimetype]"):
            asset_filename = node.get("mimetype")
            if asset_filename.startswith('replace'):
                asset_filename = asset_filename.replace("replace", "")
                file_path = os.path.join(self.pkg_path, asset_filename)
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
        if source.text and ":" in source.text and ": " not in source.text:
            mixed_citation = self.tree.find(".//mixed-citation")
            check = source.text.replace(":", ": ")
            mixed_citation_text = " ".join(mixed_citation.itertext())
            if check in mixed_citation_text:
                source.text = check


class PackageMaker(object):

    def __init__(self, pkg_path, output_path, optimise=True):
        """
        Reempacota os arquivos de pacote SP,
        padronizando-os e/ou otimizando-os.

        Args:
            pkg_path (str): caminho da pasta em que há arquivos XML SP,
                ativos digitais e manifestações de 1 ou mais documentos,
                que serão empacotados, ou seja, são arquivos de entrada.

            output_path (str): caminho da pasta onde serão geradas as saídas
                do empacotamento, como relatórios, os arquivos temporários,
                os arquivos do pacote etc.

            optimise (bool): gera imagens otimizadas para web

        """
        self.optimise = optimise

        # origem da pasta que pode conter 1 ou mais XML
        self.source_folder = workarea.MultiDocsPackageFolder(pkg_path)

        # outputs
        self.output_folder = workarea.MultiDocsPackageOuputs(output_path)

        # destination
        self.destination_path = self.output_folder.scielo_package_path

    def _enhance_doc_package(self, doc_files, doc_outs,
                             dtd_location_type='remote',
                             optimise_individually=False):
        """
        Padroniza o XML de um documento.

        Args:
            doc_files (workarea.DocumentPackageFiles): dados do conjunto
                de arquivos de um documento SP
            doc_outs (workarea.DocumentOutputFiles): caminhos das saídas
                de um documento SP
            dtd_location_type (str): valores remote ou local para indicar se
                deve eliminar https://... do caminho da DTD, necessário para
                o site (Web) para não demorar a carregar a página.
        """
        logger.debug(
            "PackageMaker._enhance_doc_package %s" %
            doc_files.filename)

        xmlcontent = SPSXMLContent(doc_files.filename)

        if self.optimise and optimise_individually:
            new_pkg_path = doc_outs.create_dir_at_work_path("enhanced")
        else:
            new_pkg_path = self.destination_path

        new_pkg_filepath = os.path.join(new_pkg_path, doc_files.basename)
        xmlcontent.write(new_pkg_filepath, dtd_location_type=dtd_location_type,
                         pretty_print=True)
        doc_files.copy_related_files(new_pkg_path)
        logger.debug(
            "PackageMaker._enhance_doc_package (%s): %s" %
            (doc_files.filename, new_pkg_path))
        return new_pkg_path

    def _optimise_doc_package(self, doc_pkg_path, tmp_path):
        """
        Otimiza as imagens e altera o XML de um documento para inserir
        alternatives das imagens otimizadas.

        Args:
            doc_pkg_path (str): caminho da pasta de 1 documento a ser otimizado
            doc_outs (workarea.DocumentOutputFiles): caminhos das saídas
                de um documento SP
        """
        logger.debug("_optimise_doc_package %s" % doc_pkg_path)
        print("Optimise: %s" % doc_pkg_path)
        files = [os.path.join(doc_pkg_path, f)
                 for f in os.listdir(doc_pkg_path)]

        zip_regular = os.path.join(tmp_path, "regular.zip")
        zip_optimised = os.path.join(tmp_path, "optimised.zip")
        extracted_package = os.path.join(tmp_path, "extracted")
        if not os.path.isdir(extracted_package):
            os.makedirs(extracted_package)
        if os.path.isfile(zip_regular):
            fs_utils.delete_file_or_folder(zip_regular)
        if os.path.isfile(zip_optimised):
            fs_utils.delete_file_or_folder(zip_optimised)

        fs_utils.zip(zip_regular, files)

        # packtools
        spp = SPPackage(package_file=fs_utils.ZipFile(zip_regular),
                        extracted_package=extracted_package)
        spp.optimise(new_package_file_path=zip_optimised,
                     preserve_files=False)
        fs_utils.unzip(zip_optimised, self.destination_path)

        doc_pkg_zip_filepath = doc_pkg_path + ".zip"
        fs_utils.delete_file_or_folder(doc_pkg_zip_filepath)
        if self.destination_path == doc_pkg_path:
            os.rename(zip_optimised, doc_pkg_zip_filepath)
        else:
            fs_utils.delete_file_or_folder(zip_optimised)
        fs_utils.delete_file_or_folder(zip_regular)
        print("Optimised: %s" % self.destination_path)

    def pack(self, xml_list=None, dtd_location_type='remote',
             sgmxml_name=None):
        """
        Se `xml_list` igual a `None`, então gera o pacote de todos os
        documentos SP da pasta `self.source_folder.path`, senão gera apenas
        para aqueles informados em `xml_list`.

        Args:
            xml_list (None or list): lista dos caminhos completos dos arquivos
                XML que se deseja gerar pacotes

            dtd_location_type (str): remote ou local

        Returns:
            package.SPPackage: instância com dados de um pacote com 1 ou mais
            documentos XML SP, issue e articles
        """
        _xml_names = [
            os.path.basename(item)
            for item in xml_list or []
        ]
        print("Package have {} document(s)".format(
            len(self.source_folder.pkgfiles_items)))
        print("Selected to pack {} document(s)".format(len(_xml_names)))

        percent = len(_xml_names) / len(self.source_folder.pkgfiles_items)
        optimise_individually = (percent < 1)

        for item in self.source_folder.pkgfiles_items.values():
            logger.info("PackageMaker.pack %s?" % item.filename)

            if item.basename not in _xml_names:
                logger.info("PackageMaker: skip %s" % item.basename)
                continue

            print("Pack %s" % item.filename)
            doc_outs = self.output_folder.get_doc_outputs(item.name)
            enhanced_pkg_path = self._enhance_doc_package(
                item, doc_outs, dtd_location_type, optimise_individually)

            if self.optimise and optimise_individually:
                tmp_path = doc_outs.create_dir_at_work_path("opt")
                self._optimise_doc_package(enhanced_pkg_path, tmp_path)

        if self.optimise and not optimise_individually:
            self._optimise_doc_package(
                self.destination_path,
                self.output_folder.tmp_path)

        print("Packed: %s" % self.destination_path)
        pkg = package.SPPackage(self.destination_path,
                                self.output_folder.output_path, _xml_names,
                                sgmxml_name, optimised=self.optimise)
        return pkg
