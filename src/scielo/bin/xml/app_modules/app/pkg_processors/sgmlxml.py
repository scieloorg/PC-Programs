# coding=utf-8

import os
import shutil

from ...__init__ import _
from ...generics import fs_utils
from ...generics import java_xml_utils
from ...generics import xml_utils
from ...generics import img_utils
from ...generics import encoding
from ...generics.reports import text_report
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from ..data import article
from ..data import workarea
from . import symbols
from . import sps_pkgmaker
from .pkg_processors import xml_versions


class SGMLXMLWorkarea(workarea.MultiDocsPackageOuputs):

    def __init__(self, name, sgmxml_path):
        self.input_path = sgmxml_path
        self.name = name
        output_path = os.path.dirname(os.path.dirname(sgmxml_path))
        workarea.MultiDocsPackageOuputs.__init__(self, output_path)
        self.src_path = self.output_path + '/src'

    @property
    def html_filename(self):
        if not os.path.isdir(self.input_path):
            os.makedirs(self.input_path)
        _html_filename = self.input_path + '/' + self.name + '.temp.htm'
        if not os.path.isfile(_html_filename):
            _html_filename += 'l'
        return _html_filename


class PackageName(object):

    def __init__(self, doc):
        self.doc = doc
        self.xml_name = doc.xml_name

    def generate(self, acron):
        parts = [self.issn, acron, self.doc.volume, self.issueno, self.suppl, self.last, self.doc.compl]
        return '-'.join([part for part in parts if part is not None and not part == ''])

    @property
    def issueno(self):
        _issueno = self.doc.number
        if _issueno:
            if _issueno == 'ahead':
                _issueno = '0'
            if _issueno.isdigit():
                if int(_issueno) == 0:
                    _issueno = None
                else:
                    n = len(_issueno)
                    if len(_issueno) < 2:
                        n = 2
                    _issueno = _issueno.zfill(n)
        return _issueno

    @property
    def suppl(self):
        s = self.doc.volume_suppl if self.doc.volume_suppl else self.doc.number_suppl
        if s is not None:
            s = 's' + s if s != '0' else 'suppl'
        return s

    @property
    def issn(self):
        _issns = [_issn for _issn in [self.doc.e_issn, self.doc.print_issn] if _issn is not None]
        if len(_issns) > 0:
            if self.xml_name[0:9] in _issns:
                _issn = self.xml_name[0:9]
            else:
                _issn = _issns[0]
        return _issn

    @property
    def last(self):
        if self.doc.fpage is not None and self.doc.fpage != '0':
            _last = self.doc.fpage
            if self.doc.fpage_seq is not None:
                _last += self.doc.fpage_seq
        elif self.doc.elocation_id is not None:
            _last = self.doc.elocation_id
        elif self.doc.number == 'ahead' and self.doc.doi is not None and '/' in self.doc.doi:
            _last = self.doc.doi[self.doc.doi.find('/')+1:].replace('.', '-')
        else:
            _last = self.doc.publisher_article_id
        return _last


class SGMLHTML(object):

    def __init__(self, xml_name, html_filename):
        self.xml_name = xml_name
        self.html_filename = html_filename

    def file(self, html_href):
        img_doc = os.path.join(self.html_img_path, html_href)
        if os.path.isfile(img_doc):
            return img_doc

    @property
    def html_content(self):
        content = fs_utils.read_file(self.html_filename)
        if '<html' not in content.lower():
            c = content
            for c in content:
                if ord(c) == 0:
                    break
            content = content.replace(c, '')
        return content

    @property
    def html_img_path(self):
        path = None

        html_path = os.path.dirname(self.html_filename)
        html_name = os.path.basename(self.html_filename)
        html_name, ext = os.path.splitext(html_name)
        for item in os.listdir(html_path):
            if os.path.isdir(html_path + '/' + item) and item.startswith(html_name):
                path = html_path + '/' + item
                break
        if path is None:
            path = self.create_html_images(html_path, html_name)
        if path is None:
            path = html_path
        return path

    def create_html_images(self, html_path, html_name):
        #name_image001
        new_html_folder = html_path + '/' + html_name + '_arquivosalt'
        if not os.path.isdir(new_html_folder):
            os.makedirs(new_html_folder)
        for item in os.listdir(html_path):
            if os.path.isfile(html_path + '/' + item) and item.startswith(html_name + '_image'):
                new_name = item[len(html_name)+1:]
                shutil.copyfile(html_path + '/' + item, new_html_folder + '/' + new_name)
        return new_html_folder

    @property
    def unknown_href_items(self):
        #[graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
        #src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
        html_content = self.html_content
        if 'href=&quot;?' in html_content:
            html_content = html_content.replace('href=&quot;?', 'href="?')
        #if '“' in html_content:
        #    html_content = html_content.replace('“', '"')
        #if '”' in html_content:
        #    html_content = html_content.replace('”', '"')
        _items = html_content.replace('href="?', 'href="?--~BREAK~FIXHREF--FIXHREF').split('--~BREAK~FIXHREF--')
        items = [item for item in _items if item.startswith('FIXHREF')]
        img_src = []
        for item in items:
            if 'src="' in item:
                src = item[item.find('src="') + len('src="'):]
                src = src[0:src.find('"')]
                if '/' in src:
                    src = src[src.find('/') + 1:]
                if len(src) > 0:
                    img_src.append(src)
            else:
                img_src.append('None')
        return img_src

    def get_fontsymbols(self):
        r = []
        html_content = self.html_content
        if '[fontsymbol]' in html_content.lower():
            for style in ['italic', 'sup', 'sub', 'bold']:
                html_content = html_content.replace('<' + style + '>', '[' + style + ']')
                html_content = html_content.replace('</' + style + '>', '[/' + style + ']')

            html_content = html_content.replace('[fontsymbol]'.upper(), '[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]'.upper(), '[/fontsymbol]')
            html_content = html_content.replace('[fontsymbol]', '~BREAK~[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]', '[/fontsymbol]~BREAK~')

            html_fontsymbol_items = [item for item in html_content.split('~BREAK~') if item.startswith('[fontsymbol]')]
            for item in html_fontsymbol_items:
                item = item.replace('[fontsymbol]', '').replace('[/fontsymbol]', '')
                item = item.replace('<', '~BREAK~<').replace('>', '>~BREAK~')
                item = item.replace('[', '~BREAK~[').replace(']', ']~BREAK~')
                parts = [part for part in item.split('~BREAK~') if not part.endswith('>') and not part.startswith('<')]

                new = ''
                for part in parts:
                    if part.startswith('['):
                        new += part
                    else:

                        for c in part:
                            _c = c.strip()
                            if _c.isdigit() or _c == '':
                                n = c
                            else:
                                try:
                                    n = symbols.get_symbol(c)
                                except:
                                    n = '?'
                            new += n
                for style in ['italic', 'sup', 'sub', 'bold']:
                    new = new.replace('[' + style + ']', '<' + style + '>')
                    new = new.replace('[/' + style + ']', '</' + style + '>')
                r.append(new)
        return r


class SGMLXMLContent(xml_utils.SuitableXML):
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
        super().__init__(self, src_pkgfiles.filename)
        self.identify_href_values()
        self.insert_xhtml_content()
        self.replace_fontsymbols()

    def well_formed_xml_content(self):
        self._fix_quotes()
        super().well_formed_xml_content(self)

    def _fix_quotes(self):
        """
        Às vezes a codificação das aspas vem diferente de ", sendo assim
        são necessários trocas antes de carregar a árvore de XML
        """
        content = self._content
        content = content.replace("<", "FIXQUOTESBREK<")
        content = content.replace(">", ">FIXQUOTESBREK")
        items = content.split("FIXQUOTESBREK")
        for item in items:
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

    def replace_fontsymbols(self):
        if self.content.find('<fontsymbol>') > 0:
            html_fontsymbol_items = self.sgmlhtml.get_fontsymbols()
            c = self.content.replace('<fontsymbol>', '~BREAK~<fontsymbol>')
            c = c.replace('</fontsymbol>', '</fontsymbol>~BREAK~')
            items = [item for item in c.split('~BREAK~') if item.startswith('<fontsymbol>') and item.endswith('</fontsymbol>')]
            i = 0
            for item in items:
                self.content = self.content.replace(item, html_fontsymbol_items[i])
                i += 1

    def insert_xhtml_content(self):
        if '<xhtml' in self.content:
            new = []
            for item in self.content.replace(
                '<xhtml', 'BREAKXHTML<xhtml').split('BREAKXHTML'):
                if item.startswith('<xhtml'):
                    xhtml = item
                    if '</xhtml>' in xhtml:
                        xhtml = xhtml[:xhtml.find('</xhtml>')+len('</xhtml>')]
                    else:
                        xhtml = xhtml[:xhtml.find('>')+1]
                    href = xhtml[xhtml.find('"')+1:xhtml.rfind('"')]
                    href = href.replace('"', '')
                    xhtml_content = ''
                    if href != '':
                        if os.path.isfile(self.src_pkgfiles.path + '/' + href):
                            xhtml_content = fs_utils.read_file(
                                self.src_pkgfiles.path + '/' + href)
                            body = html_body(xhtml_content)
                            if body is not None:
                                item = item.replace(xhtml, body)
                new.append(item)
            self.content = ''.join(new)

    def identify_href_values(self):
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
            for node in self.xml.findall(".//*[@href]")
            if node.get("href").startswith(html_filename)
        ]
        self.images_origin = []
        for graphic, html_href in zip(nodes, self.sgmlhtml.unknown_href_items):
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
            if not parent.get("id"):
                continue
            elem_name = parent.tag
            elem_id = parent.get("id")

            img_id = elem_name + ' ' + elem_id
            img_from_src = None
            img_from_doc = None
            img_origin = None
            new_href_value = None

            # procura na pasta src um arquivo cujo nome tem padrao
            # tipo de elemento + id ou ainda image independente
            # do elemento pai (fig, table, equation) como imagens soltas
            src_href, no_parents_img_counter = self.find_href_file_in_folder(
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

    def find_href_file_in_folder(self, elem_name, elem_id,
                                 no_parents_img_counter):
        number, suffixes, no_parents_img_counter = get_mkp_href_patterns(
            elem_name, elem_id, no_parents_img_counter)
        found = self.src_pkgfiles.search_files(
            number, elem_id, suffixes
        )
        new_href = None if len(found) == 0 else found[0]
        return (new_href, no_parents_img_counter)


class SGMLXML2SPSXMLConverter(object):

    def __init__(self, xsl_getter):
        self.xsl_getter = xsl_getter

    def sgml2xml(self, xml):
        r = xml
        _xml, xml_error = xml_utils.load_xml(r)
        if _xml is not None:
            sps_version = ''
            if 'sps="' in xml:
                sps_version = xml[xml.find('sps="')+len('sps="'):]
                sps_version = sps_version[:sps_version.find('"')]
                if 'sps-' in sps_version:
                    sps_version = sps_version[4:]
            xsl = self.xsl_getter(sps_version)
            r = java_xml_utils.xml_content_transform(xml, xsl)
        return r


class PackageNamer(object):

    def __init__(self, xml_content, src_pkgfiles):
        self.xml_content = xml_content
        self.src_pkgfiles = src_pkgfiles
        self.dest_pkgfiles = None

    def rename(self, acron, dest_path):
        self._fix_href_values(acron)

        self.dest_pkgfiles = workarea.DocumentPackageFiles(dest_path + '/' + self.new_name + '.xml')

        self.dest_pkgfiles.clean()
        fs_utils.write_file(self.dest_pkgfiles.filename, self.xml_content)

        self._rename_href_files()
        self._rename_other_files()

    def _fix_href_values(self, acron):
        _xml, xml_error = xml_utils.load_xml(self.xml_content)
        if _xml is not None:
            doc = article.Article(_xml, self.src_pkgfiles.name)
            self.new_name = PackageName(doc).generate(acron)

            self.hrefreplacements = []
            for href in doc.hrefs:
                if href.is_internal_file:
                    new = self._xml_href_value(href)
                    self.hrefreplacements.append((href.src, new))
                    if href.src != new:
                        self.xml_content = self.xml_content.replace('href="' + href.src + '"', 'href="' + new + '"')

    def _xml_href_value(self, href):
        href_type = href.href_attach_type
        if href.id is None:
            href_name = href.src.replace(self.src_pkgfiles.name, '')
            if href_name[0:1] in '-_':
                href_name = href_name[1:]
        else:
            href_name = href.id
            if '.' in href.src:
                href_name += href.src[href.src.rfind('.'):]
        href_name = href_name.replace('image', '').replace('img', '')
        if href_name.startswith(href_type):
            href_type = ''
        new_href = self.new_name + '-' + href_type + href_name
        new_href = self.src_pkgfiles.add_extension(new_href)
        return new_href

    def _rename_href_files(self):
        self.href_files_copy = []
        self.href_names = []
        self.missing_href_files = []

        for f, new in self.hrefreplacements:
            name, _ = os.path.splitext(f)
            new_name, _ = os.path.splitext(new)
            for ext in self.src_pkgfiles.related_files_by_name.get(name, []):
                shutil.copyfile(self.src_pkgfiles.path + '/' + name + ext, self.dest_pkgfiles.path + '/' + new_name + ext)
                self.href_files_copy.append((name + ext, new_name + ext))
                self.href_names.append(name)
            if self.dest_pkgfiles.related_files_by_name.get(new_name) is None:
                self.missing_href_files.append(new)

    def _rename_other_files(self):
        self.related_files_copy = []
        for name, ext_items in self.src_pkgfiles.related_files_by_name.items():
            if name not in self.href_names:
                for ext in ext_items:
                    new_name = name.replace(self.src_pkgfiles.name, self.new_name)
                    if self.new_name in new_name:
                        shutil.copyfile(self.src_pkgfiles.path + '/' + name + ext, self.dest_pkgfiles.path + '/' + new_name + ext)
                        self.related_files_copy.append((name + ext, new_name + ext))

    def report(self):
        log = []
        log.append(_('Report of files') + '\n' + '-'*len(_('Report of files')) + '\n')
        log.append(_('Source path') + ':   ' + self.src_pkgfiles.path)
        log.append(_('Package path') + ':  ' + self.dest_pkgfiles.path)
        log.append(_('Source XML name') + ': ' + self.src_pkgfiles.name)
        log.append(_('Package XML name') + ': ' + self.new_name)
        log.append(text_report.display_labeled_list(_('Total of related files'), text_report.display_pairs_list(self.related_files_copy)))
        log.append(text_report.display_labeled_list(_('Total of files in package'), text_report.display_pairs_list(self.href_files_copy)))
        log.append(text_report.display_labeled_list(_('Total of @href in XML'), text_report.display_pairs_list(self.hrefreplacements)))
        log.append(text_report.display_labeled_list(_('Total of files not found in package'), self.missing_href_files))
        return '\n'.join(log)


class SGMLXML2SPSXML(object):

    def __init__(self, sgm_xml_filename, acron):
        self.acron = acron
        self.transformer = SGMLXML2SPSXMLConverter(xml_versions.xsl_getter)
        self.xml_pkgfiles = None
        self.xml_error = None
        self.sgmxml_files = workarea.DocumentPackageFiles(sgm_xml_filename)
        self.wk = SGMLXMLWorkarea(
            self.sgmxml_files.name, self.sgmxml_files.path)
        self.sgmxml_outputs = workarea.DocumentOutputFiles(
            self.sgmxml_files.name, self.wk.reports_path,
            self.sgmxml_files.path)
        self.sgm_xml_at_src_file_path = os.path.join(
            self.wk.src_path, self.sgmxml_files.name + '.xml')
        self.src_pkgfiles = workarea.DocumentPackageFiles(
            self.sgm_xml_at_src_file_path)

        shutil.copyfile(self.sgmxml_files.filename, self.src_pkgfiles.filename)
        self.xml_pkgfiles = self.src_pkgfiles

    @property
    def xml(self):
        _xml, self.xml_error = xml_utils.load_xml(self.xml_content)
        return _xml

    @property
    def doc(self):
        if self.xml is not None:
            a = article.Article(self.xml, self.sgmxml_files.name)
            a.new_prefix = self.sgmxml_files.name
            return a

    def normalize_sgmxml(self):
        sgmxml_content = SGMLXMLContent(
            self.src_pkgfiles,
            SGMLHTML(self.sgmxml_files.name, self.wk.html_filename)
            )
        sgmxml_content.normalize()
        fs_utils.write_file(self.src_pkgfiles.filename, sgmxml_content.content)
        self.images_origin = sgmxml_content.images_origin
        self.xml_content = sgmxml_content.content

    def sgmxml2xml(self):
        self.xml_content = self.transformer.sgml2xml(self.xml_content)
        fs_utils.write_file(self.src_pkgfiles.filename, self.xml_content)

    def normalize_xml(self):
        spsxmlcontent = sps_pkgmaker.SPSXMLContent(self.src_pkgfiles.filename)
        self.xml_content = spsxmlcontent.content

    def report(self):
        msg = self.invalid_xml_message
        if msg == '':
            pkgnamer = PackageNamer(self.xml_content, self.src_pkgfiles)
            pkgnamer.rename(self.acron, self.wk.scielo_package_path)
            self.xml_pkgfiles = pkgnamer.dest_pkgfiles
            self.xml_pkgfiles.previous_name = self.src_pkgfiles.name
            msg = pkgnamer.report()
            img_reports = ImagesOriginReport(self.images_origin, pkgnamer.hrefreplacements, self.xml_pkgfiles.path)
            html_reports.save(self.sgmxml_outputs.images_report_filename, '', img_reports.report())
        fs_utils.write_file(self.sgmxml_outputs.mkp2xml_report_filename, msg)

    def pack(self):
        self.normalize_sgmxml()
        self.sgmxml2xml()
        self.normalize_xml()
        self.report()

    @property
    def invalid_xml_message(self):
        msg = ''
        if self.doc is None:
            messages = []
            messages.append(self.xml_error)
            messages.append(validation_status.STATUS_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=self.xml_pkgfiles.filename) + '\n' + _('Open it with XML Editor or Web Browser to find the errors easily. '))
            msg = '\n'.join(messages)
        return msg


class ImagesOriginReport(object):

    def __init__(self, images_origin, src2xmlhrefreplacements, package_path):
        self.package_path = package_path
        self.src2xmlhrefreplacements = dict(src2xmlhrefreplacements)
        self.images_origin = images_origin

    def report(self):
        rows = []
        if len(self.src2xmlhrefreplacements) == 0:
            rows.append(html_reports.tag('h4', _('Article has no image')))
        else:
            rows.append('<ol>')
            for item in self.images_origin:
                rows.append(self.item_report(item))
            rows.append('</ol>')
        return html_reports.tag('h2', _('Images Origin Report')) + ''.join(rows)

    def item_report(self, item):
        chosen_image_id, chosen_name, chosen_image_origin, chosen_image_src, chosen_image_doc = item
        elem_name, elem_id = chosen_image_id.split(' ')
        style = elem_name if elem_name in ['tabwrap', 'figgrp', 'equation'] else 'inline'
        rows = []
        rows.append('<li>')
        rows.append(html_reports.tag('h3', chosen_image_id))
        rows.append(self.item_report_replacement(chosen_name, self.src2xmlhrefreplacements.get(chosen_name)))
        rows.append(html_reports.tag('h4', chosen_image_origin))
        rows.append('<div class="compare_images">')
        rows.append(self.display_image(self.package_path + '/' + self.src2xmlhrefreplacements.get(chosen_name), "compare_" + style, chosen_image_origin))
        if chosen_image_src is not None:
            rows.append(self.display_image(chosen_image_src, "compare_" + style, 'src'))
        if chosen_image_doc is not None:
            rows.append(self.display_image(chosen_image_doc, "compare_" + style, 'doc'))
        rows.append('</div>')
        rows.append('</li>')
        return '\n'.join(rows)

    def item_report_replacement(self, name, renamed):
        return html_reports.tag('h4', renamed if name == renamed else name + ' => ' + renamed)

    def display_image(self, img_filename, style, title):
        rows = []
        if title is not None:
            rows.append(html_reports.tag('h5', title))
        img_filename = 'file://' + img_filename.replace('.tiff', '.jpg').replace('.tif', '.jpg')
        return '<div class="{}">'.format(style) + html_reports.link(img_filename, html_reports.image(img_filename)) + '</div>'


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


def html_body(xhtml_content):
    if '</body>' in xhtml_content and '<body' in xhtml_content:
        body = xhtml_content[xhtml_content.find('<body'):xhtml_content.rfind('</body>')]
        xhtml = {'table': 'xhtmltable', 'math': 'mmlmath', 'mml:math': 'mmlmath'}
        tags = ['table', 'math', 'mml:math']
        p_items = [body.find('<{}'.format(tag)) for tag in tags]
        p_min = min([item for item in p_items if item >= 0])

        if p_min >= 0:
            body = body[p_min:]
            tag = body[1:body.find('>')]
            if ' ' in tag:
                tag = tag[:tag.find(' ')]
            close_tag = u'</{}>'.format(tag)
            if close_tag in body:
                body = body[:body.rfind(close_tag)+len(close_tag)]
                return u'<{}>'.format(xhtml[tag]) + body + u'</{}>'.format(xhtml[tag])
