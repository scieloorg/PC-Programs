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


class SGMLXMLWorkarea(workarea.Workarea):

    def __init__(self, name, sgmxml_path):
        self.input_path = sgmxml_path
        self.name = name
        output_path = os.path.dirname(os.path.dirname(sgmxml_path))
        workarea.Workarea.__init__(self, output_path)
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

    @property
    def html_content(self):
        content = fs_utils.read_file(self.html_filename, encoding.SYS_DEFAULT_ENCODING)
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


class SGMLXMLContent(xml_utils.XMLContent):

    def __init__(self, content, sgmlhtml, src_pkgfiles):
        self.sgmlhtml = sgmlhtml
        self.src_pkgfiles = src_pkgfiles
        xml_utils.XMLContent.__init__(self, self.fix_begin_end(content))

    def fix_begin_end(self, content):
        s = content
        if '<?xml' in s:
            s = s[s.find('>')+1:]

        if '<!DOCTYPE' in s:
            s = s[s.find('>')+1:]
        if '<doc' in s:
            remove = s[:s.find('<doc')]
            if len(remove) > 0:
                content = content.replace(remove, '')
        if not content.endswith('</doc>') and '</doc>' in content:
            content = content[:content.rfind('</doc>')+len('</doc>')]
        return content

    def normalize(self):
        self.fix_quotes()
        self.content = xml_utils.remove_doctype(self.content)
        self.insert_mml_namespace_reference()
        self.identify_href_values()
        self.insert_xhtml_content()
        self.replace_fontsymbols()
        self.fix_styles_names()
        self.remove_exceding_styles_tags()
        self.content = self.fix_begin_end(self.content)
        if self.xml is None:
            self.fix()
        self.content = self.fix_begin_end(self.content)

    def fix_styles_names(self):
        for style in ['italic', 'bold', 'sup', 'sub']:
            s = '<' + style + '>'
            e = '</' + style + '>'
            self.content = self.content.replace(s.upper(), s.lower()).replace(e.upper(), e.lower())

    def remove_exceding_styles_tags(self):
        content = ''
        while content != self.content:
            content = self.content
            for style in ['italic', 'bold', 'sup', 'sub']:
                self._remove_exceding_style_tag(style)

    def _remove_exceding_style_tag(self, style):
        s = '<' + style + '>'
        e = '</' + style + '>'
        self.content = self.content.replace(e + s, '')
        self.content = self.content.replace(e + ' ' + s, ' ')

    def fix_quotes(self):
        if u'“' in self.content or u'”' in self.content:
            items = []
            for item in self.content.replace('<', '~BREAK~<').split('~BREAK~'):
                if u'“' in item or u'”' in item and item.startswith('<'):
                    elem = item[:item.find('>')]
                    new = elem.replace(u'“', '"').replace(u'”', '"')
                    item = item.replace(elem, new)
                items.append(item)
            self.content = ''.join(items)

    def insert_mml_namespace_reference(self):
        if '>' in self.content:
            self.content = self.content[:self.content.rfind('>') + 1]
        if 'mml:' in self.content and 'xmlns:mml="https://www.w3.org/1998/Math/MathML"' not in self.content:
            if '</' in self.content:
                main_tag = self.content[self.content.rfind('</') + 2:]
                main_tag = main_tag[:main_tag.find('>')]
                if '<' + main_tag + ' ':
                    self.content = self.content.replace('<' + main_tag + ' ', '<' + main_tag + ' xmlns:mml="https://www.w3.org/1998/Math/MathML" ')

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
            for item in self.content.replace('<xhtml', 'BREAKXHTML<xhtml').split('BREAKXHTML'):
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
                            xhtml_content = fs_utils.read_file(self.src_pkgfiles.path + '/' + href)
                            if '</body>' in xhtml_content and '<body ' in xhtml_content:
                                body = xhtml_content[xhtml_content.find('<body ')+1:xhtml_content.rfind('</body>')].strip()
                                body = body[body.find('<'):].strip()
                                if body.startswith('<table') and body.endswith('</table>'):
                                    item = item.replace(xhtml, '<xhtmltable>' + body + '</xhtmltable>')
                                elif body.startswith('<math') and body.endswith('</math>'):
                                    item = item.replace(xhtml, '<mmlmath>' + body + '</mmlmath>')
                                elif body.startswith('<mml:math') and body.endswith('</mml:math>'):
                                    item = item.replace(xhtml, '<mmlmath>' + body + '</mmlmath>')
                new.append(item)
            self.content = ''.join(new)

    def identify_href_values(self):
        self.content = self.content.replace('href=&quot;?', 'href="?')
        self.content = self.content.replace('"">', '">')
        self.content = self.content.replace('href=""?', 'href="?')
        self.images_origin = []
        if self.content.find('href="?' + self.sgmlhtml.xml_name) > 0:
            # for each graphic in sgml.xml, replace href="?xmlname" by href="image in src or image in work/html"
            self.content = self.content.replace('<graphic href="?' + self.sgmlhtml.xml_name, '--FIXHREF--<graphic href="?' + self.sgmlhtml.xml_name)
            parts = self.content.split('--FIXHREF--')
            previous_part = parts[0]
            new_parts = [parts[0]]
            parts = parts[1:]
            alternative_id = 0

            for part, html_href in zip(parts, self.sgmlhtml.unknown_href_items):
                graphic = part[0:part.find('>')]
                if html_href == 'None':
                    # remove <graphic *> e </graphic>, mantendo o restante de item
                    part = part.replace('<graphic', '<nographic').replace('</graphic>', '</nographic>')
                else:
                    href = get_href_content(graphic)
                    elem_name, elem_id = get_previous_element_which_has_id_attribute(previous_part)

                    chosen_image_id = elem_name + ' ' +  elem_id
                    chosen_image_src = None
                    chosen_image_doc = None
                    chosen_image_origin = None

                    src_href, possible_href_names, alternative_id = self.find_href_file_in_folder(elem_name, elem_id, alternative_id)

                    new_href_value = src_href
                    if src_href is not None:
                        chosen_image_src = self.src_pkgfiles.path + '/' + src_href
                        chosen_image_origin = 'src'

                    if html_href is not None:
                        if os.path.isfile(self.sgmlhtml.html_img_path + '/' + html_href):
                            chosen_image_doc = self.sgmlhtml.html_img_path + '/' + html_href

                    if chosen_image_src is None and chosen_image_doc is not None:
                        chosen_image_origin = 'doc'
                        new_href_value = self.sgmlhtml.xml_name + html_href.replace('image', '')
                        shutil.copyfile(chosen_image_doc, self.src_pkgfiles.path + '/' + new_href_value)
                        #self.input_pkgfiles.files.append(new_href_value)

                    if new_href_value is not None:
                        part = part.replace(graphic, graphic.replace(href, new_href_value))
                        self.images_origin.append((chosen_image_id, new_href_value, chosen_image_origin, chosen_image_src, chosen_image_doc))
                new_parts.append(part)
                previous_part = part
            self.content = ''.join(new_parts)

    def find_href_file_in_folder(self, elem_name, elem_id, alternative_id):
        found = []
        number, suffixes, alternative_id = get_mkp_href_data(elem_name, elem_id, alternative_id)
        if number != '':
            for f in self.src_pkgfiles.related_files:
                f_name, f_ext = os.path.splitext(f)
                suffix = f_name[len(self.src_pkgfiles.name):]
                if f_ext in img_utils.IMG_EXTENSIONS and suffix in suffixes:
                    found.append(f)
        else:
            for f in self.src_pkgfiles.related_files:
                f_name, f_ext = os.path.splitext(f)
                suffix = f_name[len(self.src_pkgfiles.name):]
                if f_ext in img_utils.IMG_EXTENSIONS and suffix == elem_id:
                    found.append(f)

        new_href = None if len(found) == 0 else found[0]
        return (new_href, self.src_pkgfiles.related_files, alternative_id)

    def alt_find_href_file_in_folder(self, elem_name, elem_id, alternative_id):
        found = []
        possible_href_names = []
        number, possibilities, alternative_id = get_mkp_href_data(elem_name, elem_id, alternative_id)
        if number != '':
            for name in self.src_pkgfiles.prefixes:
                for prefix_number in possibilities:
                    for ext in img_utils.IMG_EXTENSIONS:
                        href = name + prefix_number + ext
                        possible_href_names.append(href)
                        if href in self.src_pkgfiles.related_files:
                            found.append(href)
        else:
            for name in self.src_pkgfiles.prefixes:
                for ext in img_utils.IMG_EXTENSIONS:
                    href = name + elem_id + ext
                    possible_href_names.append(href)
                    if href in self.src_pkgfiles.related_files:
                        found.append(href)
        new_href = None if len(found) == 0 else found[0]
        return (new_href, list(set(possible_href_names)), alternative_id)


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

        self.dest_pkgfiles = workarea.PkgArticleFiles(dest_path + '/' + self.new_name + '.xml')

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

    def __init__(self, sgmxml_files):
        self.xml_pkgfiles = None
        self.xml_error = None
        self.sgmxml_files = sgmxml_files
        self.wk = SGMLXMLWorkarea(sgmxml_files.name, sgmxml_files.path)
        self.sgmhtml = SGMLHTML(sgmxml_files.name, self.wk.html_filename)
        self.sgmxml_outputs = workarea.OutputFiles(sgmxml_files.name, self.wk.reports_path, sgmxml_files.path)
        self.src_pkgfiles = workarea.PkgArticleFiles(self.wk.src_path + '/' + sgmxml_files.name + '.xml')
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
        self.src_pkgfiles.tiff2jpg()
        sgmxml_content = SGMLXMLContent(
            fs_utils.read_file(self.src_pkgfiles.filename),
            self.sgmhtml,
            self.src_pkgfiles)
        sgmxml_content.normalize()
        fs_utils.write_file(self.src_pkgfiles.filename, sgmxml_content.content)
        self.images_origin = sgmxml_content.images_origin
        self.xml_content = sgmxml_content.content

    def sgmxml2xml(self, converter):
        self.xml_content = converter.sgml2xml(self.xml_content)
        fs_utils.write_file(self.src_pkgfiles.filename, self.xml_content)

    def normalize_xml(self):
        spsxmlcontent = sps_pkgmaker.SPSXMLContent(self.xml_content)
        spsxmlcontent.normalize()
        self.xml_content = spsxmlcontent.content

    def report(self, acron):
        msg = self.invalid_xml_message
        if msg == '':
            pkgnamer = PackageNamer(self.xml_content, self.src_pkgfiles)
            pkgnamer.rename(acron, self.wk.scielo_package_path)
            self.xml_pkgfiles = pkgnamer.dest_pkgfiles
            self.xml_pkgfiles.previous_name = self.src_pkgfiles.name
            msg = pkgnamer.report()
            img_reports = ImagesOriginReport(self.images_origin, pkgnamer.hrefreplacements, self.xml_pkgfiles.path)
            html_reports.save(self.sgmxml_outputs.images_report_filename, '', img_reports.report())
        fs_utils.write_file(self.sgmxml_outputs.mkp2xml_report_filename, msg)

    def pack(self, acron, converter):
        self.normalize_sgmxml()
        self.sgmxml2xml(converter)
        self.normalize_xml()
        self.report(acron)

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


def get_href_content(graphic):
    href = graphic[graphic.find('?'):]
    if '"' in href:
        href = href[:href.find('"')]
    if '&quot;' in href:
        href = href[:href.find('&quot;')]
    return href


def get_previous_element_which_has_id_attribute(text):
    elem_id = ''
    elem_name = ''
    if ' id="' in text:
        patch = text[text.rfind(' id="') + len(' id="'):]

        elem_id = patch
        elem_id = elem_id[:elem_id.find('"')]

        tag_end = patch
        if '>' in tag_end:
            tag_end = tag_end[:tag_end.find('>')]

        elem_name = text[:text.rfind(' id="')]
        elem_name = elem_name[elem_name.rfind('<')+1:]
        if ' ' in elem_name:
            elem_name = elem_name[:elem_name.find(' ')]

        if patch.find('</' + elem_name + '>') >= 0 or tag_end.endswith('/'):
            elem_name = ''
            elem_id = ''
    return (elem_name, elem_id)


def get_mkp_href_data(elem_name, elem_id, alternative_id):
    prefixes = []
    possibilities = []
    n = ''
    if elem_name == 'equation':
        prefixes.append('frm')
        prefixes.append('form')
        prefixes.append('eq')
        n = get_number_from_element_id(elem_id)
    elif elem_name in ['tabwrap', 'equation', 'figgrp']:
        prefixes.append(elem_name[0])
        prefixes.append(elem_name[0:3])
        n = get_number_from_element_id(elem_id)
    else:
        prefixes.append('img')
        prefixes.append('image')
        alternative_id += 1
        n = str(alternative_id)

    for prefix in prefixes:
        possibilities.append(prefix + n)
        if n != '':
            possibilities.append(prefix + '0' + n)
    return (n, possibilities, alternative_id)


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
