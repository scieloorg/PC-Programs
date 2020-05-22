# coding=utf-8
import logging
import logging.config
import os
import shutil
from copy import deepcopy

from prodtools import _
from prodtools.utils import fs_utils
from prodtools.utils import xml_utils
from prodtools.utils.reports import text_report
from prodtools.utils.reports import html_reports
from prodtools.utils.reports import validation_status
from prodtools.data import article
from prodtools.data import workarea
from prodtools.processing import symbols
from prodtools.processing import xml_versions
from prodtools.processing.sps_pkgmaker import PackageMaker


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class SGMLXML2SPSXMLError(Exception):
    pass


class SPXMLLoadingError(Exception):
    pass


class SGMLXMLWorkarea(workarea.MultiDocsPackageOuputs):
    """
    - markup_xml
        - errors
        - pmc_package
        - scielo_markup
        - scielo_package
        - src
            - sgmxml_name.xml
        - work
            - sgmxml_name
                - sgmxml_name.sgm.xml
                - sgmxml_name.temp.html
                - sgmxml_name*_arquivos
                - html
                    - temporarios html
                - scielo_package
                    - xml_name.xml

    """
    def __init__(self, sgmxml_filepath):
        # sgmxml_filepath = markup_xml/work/sgmxml_name/sgmxml_name.sgm.xml
        # basename = sgmxml_name.sgm.xml
        basename = os.path.basename(sgmxml_filepath)
        # basename = sgmxml_name.sgm
        basename, ign = os.path.splitext(basename)
        # self.sgmxml_fname = sgmxml_name
        self.sgmxml_fname, ign = os.path.splitext(basename)

        # self.sgmxml_dirname = markup_xml/work/sgmxml_name
        self.sgmxml_dirname = os.path.dirname(sgmxml_filepath)
        self.sgmxml_basename = basename + ".xml"

        # output_path = markup_xml
        output_path = os.path.dirname(os.path.dirname(self.sgmxml_dirname))
        workarea.MultiDocsPackageOuputs.__init__(self, output_path)

        # local e prefixo dos relatórios de erro
        self.sgmxml_outputs = self.get_doc_outputs(
            self.sgmxml_fname, self.sgmxml_fname)

        # self.src_path = markup_xml/src
        self.src_path = os.path.join(self.output_path, 'src')
        # src_file_path = markup_xml/src/sgmxml_name.xml
        src_file_path = os.path.join(self.src_path, self.sgmxml_basename)
        shutil.copyfile(sgmxml_filepath, src_file_path)
        self.src_pkgfiles = workarea.DocumentPackageFiles(src_file_path)

        # self.tmp_doc_pkg_path =
        # markup_xml/work/sgmxml_name/scielo_package
        self.tmp_doc_pkg_path = os.path.join(
            self.sgmxml_dirname, "scielo_package")
        if not os.path.dirname(self.tmp_doc_pkg_path):
            os.makedirs(self.tmp_doc_pkg_path)

    @property
    def html_filename(self):
        if not os.path.isdir(self.sgmxml_dirname):
            os.makedirs(self.sgmxml_dirname)
        _html_filename = os.path.join(
            self.sgmxml_dirname, self.sgmxml_fname + '.temp.htm')
        if not os.path.isfile(_html_filename):
            _html_filename += 'l'
        return _html_filename


class PackageName(object):

    def __init__(self, doc):
        self.doc = doc
        self.xml_name = doc.xml_name

    def generate(self, acron):
        parts = [self.issn, acron, self.doc.volume, self.issueno, self.suppl, self.last, self.doc.compl]
        return '-'.join([part for part in parts if part])

    def zero(self, value):
        return value and value.isdigit() and int(value) == 0

    @property
    def issueno(self):
        _issueno = self.doc.number
        if _issueno == 'ahead' or self.zero(_issueno):
            return
        if _issueno.isdigit():
            _issueno = _issueno.zfill(2)
        return _issueno

    @property
    def suppl(self):
        s = self.doc.volume_suppl or self.doc.number_suppl
        if s:
            if self.zero(s):
                return 'suppl'
            return 's' + s

    @property
    def issn(self):
        _issns = [self.doc.e_issn, self.doc.print_issn]
        if self.xml_name[0:9] in _issns:
            return self.xml_name[0:9]
        return self.doc.e_issn or self.doc.print_issn

    @property
    def last(self):
        if not self.zero(self.doc.fpage):
            return self.doc.fpage + (self.doc.fpage_seq or "")
        if self.doc.elocation_id:
            return self.doc.elocation_id
        if self.doc.number == 'ahead' and self.doc.doi and '/' in self.doc.doi:
            return self.doc.doi[self.doc.doi.find('/')+1:].replace('.', '-')
        return self.doc.publisher_article_id


class SGMLHTML(object):

    def __init__(self, xml_name, html_filename):
        self.xml_name = xml_name
        self.html_filename = html_filename
        self.html_img_path = html_filename
        self.tree, self.errors = xml_utils.load_html(html_filename)

    def file(self, html_href):
        img_doc = os.path.join(self.html_img_path, html_href)
        if os.path.isfile(img_doc):
            return img_doc

    @property
    def html_img_path(self):
        return self._html_img_path

    @html_img_path.setter
    def html_img_path(self, html_file_path):
        """
        Ao salvar o arquivo marcado, o Word também salva o arquivo em HTML
        e suas imagens ficam em uma pasta junto como o HTML.
        """
        path = None
        html_dirname = os.path.dirname(html_file_path)
        html_basename = os.path.basename(html_file_path)
        html_name, ext = os.path.splitext(html_basename)
        for item in os.listdir(html_dirname):
            item_path = os.path.join(html_dirname, item)
            if os.path.isdir(item_path) and item.startswith(html_name):
                path = item_path
                break
        if path is None:
            # devido a diferentes versoes de Word as imagens podem
            # ser criadas em um local diferente do esperado
            # criá-las no local esperado
            path = self._create_new_html_img_path(html_dirname, html_name)
        if path is None:
            path = html_dirname
        self._html_img_path = path

    def _create_new_html_img_path(self, html_dirname, html_name):
        # name_image001
        name_pattern = html_name + '_image'
        new_html_folder = os.path.join(
            html_dirname, html_name + '_arquivosalt')
        if not os.path.isdir(new_html_folder):
            os.makedirs(new_html_folder)
        for item in os.listdir(html_dirname):
            item_path = os.path.join(html_dirname, item)
            if os.path.isfile(item_path) and item.startswith(name_pattern):
                new_name = item[len(html_name)+1:]
                shutil.copyfile(
                    item_path, os.path.join(new_html_folder, new_name))
        return new_html_folder

    @property
    def images(self):
        # [graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
        # src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
        img_src = []
        for img in self.tree.findall(".//img"):
            src = img.get("src")
            if src:
                basename = os.path.basename(src)
                img_src.append(basename)
            else:
                img_src.append('None')
        return img_src


class SGMLXMLContentEnhancer(xml_utils.SuitableXML):
    """
    Faz correções, se necessárias, nos XML gerados pelo
    Markup que é XML em que será aplicada um XSL para que seja convertido ao
    XML SciELO.
    Como vem do Word, pode vir com caracteres indesejáveis, mescla de estilos
    por mesclas tags do html e do xml etc
    - remove "junk" depois da última tag de fecha
    - conserta entidades que faltam ;
    - converte as entidades em caracteres
    - conserta a posicao de tags que fecham devido à mescla de tags de estilo
    e tags do Markup
    """

    def __init__(self, src_pkgfiles, sgmlhtml):
        self.sgmlhtml = sgmlhtml
        self.src_pkgfiles = src_pkgfiles
        super().__init__(src_pkgfiles.filename)
        if self.xml_error:
            raise Exception(self.xml_error)
        logger.debug("_convert_font_symbols_to_entities")
        self._convert_font_symbols_to_entities()
        logger.debug("_set_graphic_href_values")
        self._set_graphic_href_values()
        logger.debug("_insert_xhtml_tables_in_document")
        self._insert_xhtml_tables_in_document()
        logger.debug("...")

    def well_formed_xml_content(self):
        logger.debug("_fix_quotes")
        self._fix_quotes()
        logger.debug("_fix_styles")
        self._fix_styles()
        logger.debug("well_formed_xml_content")
        super().well_formed_xml_content()

    def _fix_styles(self):
        # TODO: corrigir misplaced tags
        content = self._content
        for style in ("BOLD", "ITALIC", "SUP", "SUB"):
            tag_open = "<{}>".format(style)
            tag_close = "</{}>".format(style)
            content = content.replace(tag_open, tag_open.lower())
            content = content.replace(tag_close, tag_close.lower())
        self._content = content

    def _fix_quotes(self):
        """
        Às vezes a codificação das aspas vem diferente de ", sendo assim
        são necessários trocas antes de carregar a árvore de XML
        """
        content = self._content
        content = content.replace("<", "FIXQUOTESBREK<")
        content = content.replace(">", ">FIXQUOTESBREK")
        items = []
        for item in content.split("FIXQUOTESBREK"):
            if "=" in item and item.startswith("<") and item.endswith(">"):
                item = item.replace(
                    u'"“', '"').replace(
                    u'”"', '"').replace(
                    u'“"', '"').replace(
                    u'"”', '"').replace(
                    u'“', '"').replace(
                    u'”', '"')
            items.append(item)
        self._content = ''.join(items)

    def _convert_font_symbols_to_entities(self):
        for fontsymbol in self.xml.findall(".//fontsymbol"):
            fontsymbol.text = symbols.get_symbol(fontsymbol.text)
            fontsymbol.tag = "CHANGED"
        xml_utils.etree.strip_tags(self.xml, "CHANGED")

    def _insert_xhtml_tables_in_document(self):
        for xhtml in self.xml.findall(".//xhtml"):
            href = xhtml.get("href")
            if not href:
                continue
            table_file_path = os.path.join(self.src_pkgfiles.path, href)
            if not os.path.isfile(table_file_path):
                continue

            xml_table = xml_utils.SuitableXML(table_file_path)
            if not xml_table.xml:
                continue
            table = xml_table.xml.find(".//table")
            if table is not None:
                parent = xhtml.getparent()
                parent.replace(xhtml, deepcopy(table))

    def _set_graphic_href_values(self):
        """
        No arquivo Word marcado o elemento gráfico é identificado com a
        etiqueta graphic. No seu atributo href consta apenas ? seguido do
        nome do arquivo Word. Ao gerar o XML, o arquivo Word é salvo em html
        em background. No arquivo XML gerado a partir da marcação (não XML SP
        ainda) fica a marcação `<graphic href="?nomearquivo"/>` e no arquivo
        HTML ficam de fato as referências às imagens
        `[graphic href="?nomearquivo"]<img src="imagem.jpg"/>[/graphic]`
        Aqui se fará a correspondencia entre os arquivos XML e HTML para
        trocar href="?nomearquivo" pelo nome do arquivo da imagem
        correspondente
        """
        html_filename = "?{}".format(self.sgmlhtml.xml_name)

        nodes = [
            node
            for node in self.xml.findall(".//graphic[@href]")
            if node.get("href").startswith(html_filename)
        ]
        self.images_origin = []
        html_images = self.sgmlhtml.images
        logger.info("markup: graphic[@href]: %i" % len(nodes))
        logger.info("html: img[@src]: %i" % len(html_images))
        for graphic, html_href in zip(nodes, html_images):
            logger.info("%s x %s" % (graphic.get("href"), html_href))
            no_parents_img_counter = 0
            if html_href == 'None':
                graphic.tag = "nographic"
                continue
            # procura o parent de graphic para obter o nome e id do elemento
            node = graphic
            for i in range(0, 3):
                parent = node.getparent()
                if parent.get("id"):
                    break
            if parent.get("id"):
                elem_name = parent.tag
                elem_id = parent.get("id")
            else:
                elem_name = ""
                elem_id = ""

            img_id = elem_name + ' ' + elem_id
            img_from_src = None
            img_from_doc = None
            img_origin = None
            new_href_value = None

            # procura na pasta src um arquivo cujo nome tem padrao
            # tipo de elemento + id ou ainda image independente
            # do elemento pai (fig, table, equation) como imagens soltas
            src_href, no_parents_img_counter = self._find_href_file_in_folder(
                elem_name, elem_id, no_parents_img_counter)

            # preferencialmente considerar a imagem que está na pasta src
            img_origin = 'src'
            if src_href:
                new_href_value = src_href
                img_from_src = os.path.join(
                    self.src_pkgfiles.path, src_href)

            # no entanto, havendo a imagem proveniente do Word/HTML, informar
            # sua existência
            if html_href:
                img_doc = self.sgmlhtml.file(html_href)
                if os.path.isfile(img_doc):
                    img_from_doc = img_doc

            # nao existindo a imagem na pasta src, obter a imagem de doc
            # e copiar para a pasta src
            if img_from_src is None and img_from_doc:
                img_origin = 'doc'
                new_href_value = self.sgmlhtml.xml_name + html_href
                shutil.copyfile(
                    img_from_doc,
                    os.path.join(self.src_pkgfiles.path, new_href_value))

            if new_href_value:
                # atualiza href com novo valor e
                # registra os dados da imagem para o relatório
                graphic.set("href", new_href_value)
                self.images_origin.append(
                    (img_id, new_href_value,
                        img_origin, img_from_src, img_from_doc))

    def _find_href_file_in_folder(self, elem_name, elem_id,
                                  no_parents_img_counter):
        number, suffixes, no_parents_img_counter = get_mkp_href_patterns(
            elem_name, elem_id, no_parents_img_counter)
        found = self.src_pkgfiles.search_files(
            number, elem_id, suffixes
        )
        new_href = None if len(found) == 0 else found[0]
        return (new_href, no_parents_img_counter)


class PackageNamer(object):

    def __init__(self, src_pkgfiles, acron, dest_path):
        self.src_pkgfiles = src_pkgfiles
        self.xml = xml_utils.SuitableXML(self.src_pkgfiles.filename)
        if self.xml.xml_error:
            raise SGMLXML2SPSXMLError(
                _("{}: PackageNamer: {}: {}").format(
                    validation_status.STATUS_BLOCKING_ERROR,
                    self.src_pkgfiles.filename,
                    self.xml.xml_error
                ))
        self.doc = article.Article(self.xml.xml, self.src_pkgfiles.name)
        self.new_name = PackageName(self.doc).generate(acron)
        dest_filepath = os.path.join(dest_path, self.new_name + ".xml")
        self.dest_pkgfiles = workarea.DocumentPackageFiles(dest_filepath)
        self.dest_pkgfiles.clean()
        shutil.copyfile(
            self.src_pkgfiles.filename, self.dest_pkgfiles.filename)
        logger.debug("PackageNamer: %s -> %s" %
                     (self.src_pkgfiles.filename, self.dest_pkgfiles.filename))

    def rename(self):
        logger.debug("PackageNamer._fix_href_values")
        self._fix_href_values()
        logger.debug("PackageNamer._rename_href_files")
        self._rename_href_files()
        logger.debug("PackageNamer._rename_other_files")
        self._rename_other_files()
        logger.debug("PackageNamer.xml.write")
        self.xml.write(self.dest_pkgfiles.filename)

    def _fix_href_values(self):
        self.href_replacements = []
        for element in article.nodes_which_have_xlink_href(self.doc.tree):
            value = element.attrib['{http://www.w3.org/1999/xlink}href']
            parent = element.getparent()
            new_value = self.new_href_value(parent, value)
            if value != new_value:
                self.href_replacements.append((value, new_value))
                element.set("{http://www.w3.org/1999/xlink}href", new_value)

    def new_href_value(self, element, value):
        basename, ext = os.path.splitext(value)
        elem_type = href_attach_type(element.getparent().tag, element.tag)
        elem_id = element.get("id")
        if elem_id:
            elem_id += ext
        else:
            elem_id = value.replace(self.src_pkgfiles.name, '')
            if elem_id[0] in '-_':
                elem_id = elem_id[1:]
        elem_id = elem_id.replace('image', '').replace('img', '')
        if elem_id.startswith(elem_type):
            elem_type = ''
        return self.new_name + '-' + elem_type + elem_id

    def _rename_href_files(self):
        self.href_files_copy = []
        self.href_names = []
        self.missing_href_files = []
        for f, new in self.href_replacements:
            name, _ = os.path.splitext(f)
            new_name, _ = os.path.splitext(new)

            for ext in self.src_pkgfiles.related_files_by_name.get(name) or []:
                source = os.path.join(self.src_pkgfiles.path, name + ext)
                dest = os.path.join(self.dest_pkgfiles.path, new_name + ext)
                shutil.copyfile(source, dest)
                self.href_files_copy.append((source, dest))
                self.href_names.append(name)

            if self.dest_pkgfiles.related_files_by_name.get(new_name) is None:
                self.missing_href_files.append(new)

    def _rename_other_files(self):
        self.related_files_copy = []
        for name, exts in self.src_pkgfiles.related_files_by_name.items():
            if name in self.href_names:
                continue
            new_name = name.replace(self.src_pkgfiles.name, self.new_name)
            if new_name.startswith(self.new_name):
                for ext in exts:
                    source = os.path.join(self.src_pkgfiles.path, name + ext)
                    dest = os.path.join(
                        self.dest_pkgfiles.path, new_name + ext)
                    shutil.copyfile(source, dest)
                    self.related_files_copy.append((source, dest))

    def report(self):
        log = []
        log.append(_('Report of files'))
        log.append("")
        log.append('-'*len(_('Report of files')))
        log.append("")
        log.append(_('Source path') + ':   ' + self.src_pkgfiles.path)
        log.append(_('Package path') + ':  ' + self.dest_pkgfiles.path)
        log.append(_('Source XML name') + ': ' + self.src_pkgfiles.name)
        log.append(_('Package XML name') + ': ' + self.new_name)
        log.append(
            text_report.display_labeled_list(
                _('Total of related files'),
                text_report.display_pairs_list(self.related_files_copy)))
        log.append(
            text_report.display_labeled_list(
                _('Total of files in package'),
                text_report.display_pairs_list(self.href_files_copy)))
        log.append(
            text_report.display_labeled_list(
                _('Total of @href in XML'),
                text_report.display_pairs_list(self.href_replacements)))
        log.append(
            text_report.display_labeled_list(
                _('Total of files not found in package'),
                self.missing_href_files))
        return '\n'.join(log)


class SGMLXML2SPSXML(object):

    def __init__(self, sgmxml_filepath, acron):
        self.acron = acron
        self.FILES = SGMLXMLWorkarea(sgmxml_filepath)

    def _sgmxml2xml(self):
        """
        convert o arquivo sgmlxml para xml
        """
        xml_obj, xml_error = xml_utils.load_xml(
            self.FILES.src_pkgfiles.filename)
        if xml_error:
            html_reports.webbrowser.open(
                'file://' + self.FILES.src_pkgfiles.filename
            )
            raise SGMLXML2SPSXMLError(
                _("{}: Error as loading {}: {}. ".format(
                    validation_status.STATUS_BLOCKING_ERROR,
                    self.FILES.src_pkgfiles.filename,
                    xml_error
                )))
        sps_version = xml_obj.find(".").get("sps")
        if sps_version is None:
            sps_version = xml_versions._SPS_VERSIONS[-1][0][4:]
            xml_obj.find(".").set("sps", sps_version)
        xsl_filepath = xml_versions.xsl_getter(sps_version)
        result = xml_utils.transform(xml_obj, xsl_filepath)
        #result.docinfo.doctype = xml_versions.dtd_files(
        #    sps_version).doctype_with_remote_path
        xml_utils.write(self.FILES.src_pkgfiles.filename, result)

        # print((self.FILES.src_pkgfiles.filename))
        # result.docinfo.doctype = xml_versions.dtd_files(
        #    sps_version).doctype_with_remote_path

    def _make_package(self):
        """
        Copia os arquivos da pasta src e o da pasta temporária do pacote
        individual scielo_package
        markup_xml/work/sgmxml_name/scielo_package_tmp
        """
        self.pkg_namer = PackageNamer(self.FILES.src_pkgfiles, self.acron,
                                      self.FILES.tmp_doc_pkg_path)
        self.pkg_namer.rename()
        """
        cria o pacote otimizado na pasta individual
        markup_xml/work/sgmxml_name/scielo_package
        """
        self.pkg_maker = PackageMaker(self.FILES.tmp_doc_pkg_path,
                                      self.FILES.output_path)
        pkg = self.pkg_maker.pack(
            [self.pkg_namer.dest_pkgfiles.filename],
            sgmxml_name=self.FILES.src_pkgfiles.name)
        return pkg

    def _report(self, blocking_error, pkg):
        msg = html_reports.p_message(blocking_error or "")
        if not blocking_error:
            msg = self.pkg_namer.report()
            img_reports = ImagesOriginReport(
                self.enhancer.images_origin,
                self.pkg_namer.href_replacements, pkg.package_folder.path)
            html_reports.save(
                self.FILES.sgmxml_outputs.images_report_filename, '',
                img_reports.report())
        fs_utils.write_file(
            self.FILES.sgmxml_outputs.mkp2xml_report_filename, msg)

    def pack(self):
        blocking_error = None
        pkg = None
        try:
            """
            faz ajustes no arquivo gerado pelo markup .sgm.xml
            antes de gerar o XML do SPS
            """
            logger.info(
                "Enhance SGMLXML %s" % self.FILES.src_pkgfiles.filename)
            self.enhancer = SGMLXMLContentEnhancer(
                self.FILES.src_pkgfiles,
                SGMLHTML(self.FILES.sgmxml_fname, self.FILES.html_filename)
            )
            self.enhancer.write(self.FILES.src_pkgfiles.filename)

            logger.info("Convert sgml to xml")
            self._sgmxml2xml()

            logger.info("Rename and make the package")
            pkg = self._make_package()
        except Exception as e:
            blocking_error = str(e)
            logger.exception(e)
            raise e

        finally:
            logger.info("Create Images Report")
            self._report(blocking_error, pkg)
        return pkg


class ImagesOriginReport(object):

    def __init__(self, images_origin, href_replacements, package_path):
        self.package_path = package_path
        self.href_replacements = dict(href_replacements)
        self.images_origin = images_origin

    def report(self):
        rows = []
        if len(self.href_replacements) == 0:
            rows.append(html_reports.tag('h4', _('Article has no image')))
        else:
            rows.append(
                html_reports.tag(
                    "div",
                    _('The images which compose the package can come from '
                      '"src" folder or from "doc", i.e., the markup document '
                      '(the images embedded in the markup file). This report '
                      'presents the origin of '
                      'each image. Images from "src" folder have preference '
                      'over those embedded in document. '), "note"))
            rows.append('<div><ul>')
            n = len(self.images_origin)
            for i, item in enumerate(self.images_origin):
                rows.append(html_reports.tag('h3', "{}/{}".format(i+1, n)))
                rows.append(self.item_report(item))
            rows.append('</ul></div>')
        return html_reports.tag(
            'h2', _('Images Origin Report')) + ''.join(rows)

    def item_report(self, item):
        image_id, name, image_origin, image_src, image_doc = item
        elem_name, elem_id = image_id.split(' ')
        style = 'inline'
        if elem_name in ['tabwrap', 'figgrp', 'equation']:
            style = elem_name
        compare_style = "compare_" + style
        rows = []
        rows.append('<li>')
        rows.append(html_reports.tag('h3', image_id))
        rows.append(
            self.item_report_replacement(
                name, self.href_replacements.get(name)))
        if image_src:
            rows.append('<div class="compare_images">')
            rows.append(
                self.display_image(
                    image_src, compare_style, 'src', image_origin))
            rows.append('</div>')
        if image_doc:
            rows.append('<div class="compare_images">')
            rows.append(
                self.display_image(
                    image_doc, compare_style, 'doc', image_origin))
            rows.append('</div>')
        rows.append('</li>')
        return '\n'.join(rows)

    def item_report_replacement(self, name, renamed):
        return html_reports.tag(
            'h4', renamed if name == renamed else name + ' => ' + renamed)

    def display_image(self, img_filename, style, origin, selected):
        rows = []
        if origin == selected:
            icon = "&#x2713;"
            text = _('[selected]')
        else:
            icon = "&#x2717;"
            text = _("[not selected]")
        rows.append(
            html_reports.tag(
                'h4', _('Image from {} {} {}').format(origin, icon, text)))
        rows.append(
            html_reports.tag('p', img_filename))
        img_filename = os.path.join('file://', img_filename)
        basename = os.path.basename(img_filename)
        name, ext = os.path.splitext(img_filename)
        if ext.startswith(".tif"):
            link = basename
        else:
            link = html_reports.image(img_filename)
        rows.append(
                '<div class="{}">'.format(style) +
                html_reports.link(img_filename, link) + '</div>')
        return ''.join(rows)


def get_mkp_href_patterns(elem_name, elem_id, no_parents_img_counter):
    prefixes = []
    possibilities = []
    number = ''
    if elem_name == 'equation':
        prefixes.append('frm')
        prefixes.append('form')
        prefixes.append('eq')
        number = get_number_from_element_id(elem_id)
    elif elem_name in ['tabwrap', 'equation', 'figgrp']:
        prefixes.append(elem_name[0])
        prefixes.append(elem_name[0:3])
        number = get_number_from_element_id(elem_id)
    else:
        prefixes.append('img')
        prefixes.append('image')
        no_parents_img_counter += 1
        number = str(no_parents_img_counter)

    for prefix in prefixes:
        possibilities.append(prefix + number)
        if number:
            possibilities.append(prefix + '0' + number)
    return (number, possibilities, no_parents_img_counter)


def get_number_from_element_id(element_id):
    n = ''
    i = 0
    is_letter = True
    while i < len(element_id) and is_letter:
        is_letter = not element_id[i].isdigit()
        i += 1
    if not is_letter:
        n = element_id[i-1:]
        if n != '':
            n = str(int(n))
    return n


def href_attach_type(parent_tag, tag):
    if 'suppl' in tag or 'media' == tag:
        attach_type = 's'
    elif 'inline' in tag:
        attach_type = 'i'
    elif parent_tag in ['equation', 'disp-formula']:
        attach_type = 'e'
    else:
        attach_type = 'g'
    return attach_type
