# code = utf-8
import os

from . import workarea
from . import article
from . import xml_utils
from . import fs_utils
from . import java_xml_utils

from . import symbols


class SGMLXMLContent(xml_utils.XMLContent):

    def __init__(self, content, sgmlhtml):
        self.sgmlhtml = sgmlhtml
        super(xml_utils.XMLContent, self).__init__(content) # Python 2
        for item in ['doc', 'article', 'text']:
            endtag = '</' + item + '>'
            if endtag in self.content:
                self.content = self.content[:self.content.rfind(endtag)+len(endtag)]
                break

    def normalize(self):
        self.fix_quotes()
        self.content = xml_utils.remove_doctype(self.content)
        self.insert_mml_namespace_reference()
        self.fix_mkp_href_values()
        self.xhtml_tables()
        self.replace_fontsymbols()
        self.fix_styles_names()
        self.remove_exceding_styles_tags()
        xml, e = xml_utils.load_xml(self.content)
        if xml is None:
            self.fix()

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
        if 'mml:' in self.content and not 'xmlns:mml="http://www.w3.org/1998/Math/MathML"' in self.content:
            if '</' in self.content:
                main_tag = self.content[self.content.rfind('</') + 2:]
                main_tag = main_tag[:main_tag.find('>')]
                if '<' + main_tag + ' ':
                    self.content = self.content.replace('<' + main_tag + ' ', '<' + main_tag + ' xmlns:mml="http://www.w3.org/1998/Math/MathML" ')

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

    def xhtml_tables(self):
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
                        if os.path.isfile(self.src_path + '/' + href):
                            xhtml_content = fs_utils.read_file(self.src_path + '/' + href)
                            if '<table' in xhtml_content and '</table>' in xhtml_content:
                                xhtml_content = xhtml_content[xhtml_content.find('<table'):xhtml_content.rfind('</table>')+len('</table>')]
                    item = item.replace(xhtml, '<xhtmltable>' + xhtml_content + '</xhtmltable>')
                new.append(item)
            self.content = ''.join(new)

    def fix_mkp_href_values(self):
        self.content = self.content.replace('href=&quot;?', 'href="?')
        self.content = self.content.replace('"">', '">')
        self.content = self.content.replace('href=""?', 'href="?')
        self.sorted_graphic_href_items = []
        self.src_folder_graphics = []
        if self.content.find('href="?' + self.xml_name) > 0:
            # for each graphic in sgml.xml, replace href="?xmlname" by href="image in src or image in work/html"
            self.content = self.content.replace('<graphic href="?' + self.xml_name, '--FIXHREF--<graphic href="?' + self.xml_name)
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
                    src_href, possible_href_names, alternative_id = self.select_href_file_from_src_folder(elem_name, elem_id, alternative_id)

                    renamed_href = src_href
                    if src_href is not None:
                        self.src_folder_graphics.append(src_href)
                    if renamed_href is None and html_href is not None:
                        #print('Extract from .doc', elem_name, elem_id)
                        if os.path.isfile(self.sgmlhtml.html_img_path + '/' + html_href):
                            renamed_href = self.xml_name + html_href.replace('image', '')
                            shutil.copyfile(self.sgmlhtml.html_img_path + '/' + html_href, self.src_path + '/' + renamed_href)
                            self.article_files.files.append(renamed_href)
                            #print(self.sgmlhtml.html_img_path + '/' + html_href, self.src_path + '/' + renamed_href)
                            #print('Extract from .doc', html_href, renamed_href)
                    self.sorted_graphic_href_items.append((renamed_href, elem_name, elem_id, self.sgmlhtml.html_img_path + '/' + html_href))
                    if renamed_href is not None:
                        part = part.replace(graphic, graphic.replace(href, renamed_href))
                new_parts.append(part)
                previous_part = part
            self.content = ''.join(new_parts)

    def select_href_file_from_src_folder(self, elem_name, elem_id, alternative_id):
        filenames = [self.xml_name]
        if 'v' in self.xml_name and self.xml_name.startswith('a'):
            filenames.append(self.xml_name[:self.xml_name.find('v')])
        found = []
        possible_href_names = []
        number, possibilities, alternative_id = get_mkp_href_data(elem_name, elem_id, alternative_id)
        if number != '':
            for name in filenames:
                for prefix_number in possibilities:
                    for ext in article.IMG_EXTENSIONS:
                        href = name + prefix_number + ext
                        possible_href_names.append(href)
                        if href in self.article_files.files:
                            found.append(href)
        else:
            for name in filenames:
                for ext in article.IMG_EXTENSIONS:
                    href = name + elem_id + ext
                    possible_href_names.append(href)
                    if href in self.article_files.files:
                        found.append(href)
        new_href = None if len(found) == 0 else found[0]
        #if new_href is None:
        #    print('====')
        #    print('Not found: ', self.xml_name, elem_name, elem_id, possibilities)            
        #    print('article_files:', self.article_files.files)
        #    print('====')
        return (new_href, list(set(possible_href_names)), alternative_id)


class SGMLXMLWorkarea(workarea.Workarea):

    def __init__(self, filename):
        super(workarea.Workarea, self).__init__(filename) # Python 2
        self.name, self.ext = os.path.splitext(self.name)
        self.src_path = self.dirname.replace('work', 'src')

    @property
    def html_filename(self):
        if not os.path.isdir(self.work_path):
            os.makedirs(self.work_path)
        html_filename = self.work_path + '/' + self.name + '.temp.htm'
        if not os.path.isfile(html_filename):
            html_filename += 'l'
        return html_filename


class SGMLXML2SPS(object):

    def __init__(self, workarea):
        self.workarea = workarea
        self.href_replacements = []
        self.sgmxmlcontent = SGMLXMLContent(
            fs_utils.read_file(workarea.filename),
            SGMLHTML(self.workarea.name, self.workarea.html_filename))

    @property
    def xml_name(self):
        return self.workarea.name

    @property
    def new_name(self):
        return self.workarea.new_name

    @property
    def xml(self):
        _xml, e = xml_utils.load_xml(self.xml_content)
        if _xml is not None:
            return _xml

    @property
    def doc(self):
        a = article.Article(self.xml, self.workarea.name)
        a.new_prefix = self.new_name
        return a

    def convert(self, acron, xsl):
        self.sgmxmlcontent.normalize()
        fs_utils.write_file(self.workarea.filename, self.sgmxmlcontent.content)

        self.xml_content = self.sgmxmlcontent.content
        if self.xml_content is not None:
            self.xml_content = java_xml_utils.xml_content_transform(self.sgmxmlcontent.content, xsl)
            self._normalize_href_values()
            self.workarea.new_name = PackageName(self.doc).generate(acron)
        fs_utils.write_file(self.workarea.new_filename, self.xml_content)

    def _normalize_href_values(self):
        self.href_replacements = []
        for href in self.doc.hrefs:
            if href.is_internal_file:
                new = self._normalize_href_value(href)
                self.href_replacements.append((href.src, new))
                if href.src != new:
                    self.xml_content = self.xml_content.replace('href="' + href.src + '"', 'href="' + new + '"')

    def _normalize_href_value(self, href):
        href_type = href_attach_type(href.parent.tag, href.element.tag)
        if href.id is None:
            href_name = href.src.replace(self.xml_name, '')
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
        return self.workarea.name_with_extension(href.src, new_href)


class SPSXMLfromMkp(object):

    def __init__(self, workarea):
        self.workarea = workarea
        self.href_replacements = []
        self.sgmxmlcontent = SGMLXMLContent(
            fs_utils.read_file(workarea.filename),
            SGMLHTML(self.workarea.name, self.workarea.html_filename))

    @property
    def xml_name(self):
        return self.workarea.name

    @property
    def new_name(self):
        return self.workarea.new_name

    @property
    def xml(self):
        _xml, e = xml_utils.load_xml(self.xml_content)
        if _xml is not None:
            return _xml

    @property
    def doc(self):
        a = article.Article(self.xml, self.workarea.name)
        a.new_prefix = self.new_name
        return a

    def convert(self, acron, xsl):
        self.sgmxmlcontent.normalize()
        fs_utils.write_file(self.workarea.filename, self.sgmxmlcontent.content)

        self.xml_content = self.sgmxmlcontent.content
        if self.xml_content is not None:
            self.xml_content = java_xml_utils.xml_content_transform(self.sgmxmlcontent.content, xsl)
            self._normalize_href_values()
            self.workarea.new_name = PackageName(self.doc).generate(acron)
        fs_utils.write_file(self.workarea.new_filename, self.xml_content)

    def _normalize_href_values(self):
        self.href_replacements = []
        for href in self.doc.hrefs:
            if href.is_internal_file:
                new = self._normalize_href_value(href)
                self.href_replacements.append((href.src, new))
                if href.src != new:
                    self.xml_content = self.xml_content.replace('href="' + href.src + '"', 'href="' + new + '"')

    def _normalize_href_value(self, href):
        href_type = href_attach_type(href.parent.tag, href.element.tag)
        if href.id is None:
            href_name = href.src.replace(self.xml_name, '')
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
        return self.workarea.name_with_extension(href.src, new_href)


class SGMLHTML(object):

    def __init__(self, xml_name, html_filename):
        self.xml_name = xml_name
        self.html_filename = html_filename

    @property
    def html_content(self):
        content = fs_utils.read_file(self.html_filename, sys.getfilesystemencoding())
        if not '<html' in content.lower():
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


class PackageName(object):

    def __init__(self, doc):
        self.doc = doc
        self.xml_name = doc.xml_name

    def generate(self, acron):
        vol, issueno, fpage, seq, elocation_id, order, doi, publisher_article_id = self.doc.volume, self.doc.number, self.doc.fpage, self.doc.fpage_seq, self.doc.elocation_id, self.doc.order, self.doc.doi, self.doc.publisher_article_id
        issns = [issn for issn in [self.doc.e_issn, self.doc.print_issn] if issn is not None]
        if len(issns) > 0:
            if xml_name[0:9] in issns:
                issn = xml_name[0:9]
            else:
                issn = issns[0]

        suppl = self.doc.volume_suppl if self.doc.volume_suppl else self.doc.number_suppl

        last = self.format_last_part(fpage, seq, elocation_id, order, doi, issn, publisher_article_id)
        if issueno:
            if issueno == 'ahead' or int(issueno) == 0:
                issueno = None
            else:
                n = len(issueno)
                if len(issueno) < 2:
                    n = 2
                issueno = issueno.zfill(n)
        if suppl:
            suppl = 's' + suppl if suppl != '0' else 'suppl'
        parts = [issn, acron, vol, issueno, suppl, last, self.doc.compl]
        r = '-'.join([part for part in parts if part is not None and not part == ''])
        return r

    def format_last_part(self, fpage, seq, elocation_id, order, doi, issn, publisher_article_id):
        #utils.debugging((fpage, seq, elocation_id, order, doi, issn))
        article_id = doi if doi is not None else publisher_article_id
        r = None
        if r is None:
            if fpage is not None:
                r = fpage.zfill(5)
                if seq is not None:
                    r += '-' + seq
                if r == '00000':
                    r = None
        if r is None:
            if elocation_id is not None:
                r = elocation_id
        if r is None:
            if article_id is not None:
                article_id = article_id[article_id.find('/')+1:]
                if issn in article_id:
                    article_id = article_id[article_id.find(issn) + len(issn):]
                article_id = article_id.replace('.', '_').replace('-', '_')
                r = article_id
        if r is None:
            if order is not None:
                r = order.zfill(5)
        return r


def get_href_content(graphic):
    href = graphic[graphic.find('?'):]
    if '"' in href:
        href = href[:href.find('"')]
    if '&quot;' in href:
        href = href[:href.find('&quot;')]
    return href


def get_previous_element_which_has_id_attribute(text):
    #print('\nget_previous_element_which_has_id_attribute:')
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
        #print((elem_name, elem_id))
    #else:
    #    print('No element id')
    #    print(text.encode('utf-8'))
    #print('---')

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
