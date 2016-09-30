# coding=utf-8
import os
import sys
import shutil
import urllib
from datetime import datetime
from mimetypes import MimeTypes
import zipfile
import re

try:
    from PIL import Image
    IMG_CONVERTER = True
except Exception as e:
    IMG_CONVERTER = False

from __init__ import _
import utils
import fs_utils
import java_xml_utils
import html_reports
import article_validations
import xml_utils
import xml_versions
import xpchecker
import pkg_validations
import symbols
import article
import serial_files
import xc_models
import attributes
import validation_status


mime = MimeTypes()
messages = []


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
DISPLAY_REPORT = True
GENERATE_PMC = False


xpm_process_logger = fs_utils.ProcessLogger()


def format_last_part(fpage, seq, elocation_id, order, doi, issn):
    #utils.debugging((fpage, seq, elocation_id, order, doi, issn))
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
        if doi is not None:
            doi = doi[doi.find('/')+1:]
            if issn in doi:
                doi = doi[doi.find(issn) + len(issn):]
            doi = doi.replace('.', '_').replace('-', '_')
            r = doi
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


def xpm_version():
    f = None
    if os.path.isfile(CURRENT_PATH + '/../../xpm_version.txt'):
        f = CURRENT_PATH + '/../../xpm_version.txt'
    elif os.path.isfile(CURRENT_PATH + '/../../cfg/xpm_version.txt'):
        f = CURRENT_PATH + '/../../cfg/xpm_version.txt'
    elif os.path.isfile(CURRENT_PATH + '/../../cfg/version.txt'):
        f = CURRENT_PATH + '/../../cfg/version.txt'
    version = ''
    if f is not None:
        version = open(f).readlines()[0].decode('utf-8')
    return version


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
        return path

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


class SGMLXML(object):

    def __init__(self, article_files, sgmlxml_content, html_filename):
        self.sgml_content = sgmlxml_content
        self.article_files = article_files
        self.xml_name = self.article_files.xml_name
        self.src_path = self.article_files.path
        self.sgmxml_filename = self.article_files.xml_filename

        self.sgmlhtml = SGMLHTML(self.xml_name, html_filename)
        self.sorted_graphic_href_items = []
        self.src_folder_graphics = []
        self.xml_content = None
        self.IMG_EXTENSIONS = ('.tiff', '.tif', '.eps', '.jpg', '.png')

    def generate_xml(self, version):
        #content = fix_uppercase_tag(content)
        xpm_process_logger.register('SGMLXML.generate_xml')
        self.sgml_content = xml_utils.remove_doctype(self.sgml_content)
        self.insert_mml_namespace()
        self.fix_mkp_href_values()
        self.replace_fontsymbols()

        for style in ['italic', 'bold', 'sup', 'sub']:
            s = '<' + style + '>'
            e = '</' + style + '>'
            self.sgml_content = self.sgml_content.replace(s.upper(), s.lower()).replace(e.upper(), e.lower())

        xml, e = xml_utils.load_xml(self.sgml_content)
        if xml is None:
            xml_fixer = xml_utils.XMLContent(self.sgml_content)
            xml_fixer.fix()
            if not xml_fixer.content == self.sgml_content:
                self.sgml_content = xml_fixer.content
                utils.debugging(self.sgmxml_filename)
                fs_utils.write_file(self.sgmxml_filename, self.sgml_content)
                xml, e = xml_utils.load_xml(self.sgml_content)

        if xml is None:
            return self.sgml_content
        else:
            return java_xml_utils.xml_content_transform(self.sgml_content, xml_versions.xsl_sgml2xml(version))

    def insert_mml_namespace(self):
        if '>' in self.sgml_content:
            self.sgml_content = self.sgml_content[:self.sgml_content.rfind('>') + 1]
        if 'mml:' in self.sgml_content and not 'xmlns:mml="http://www.w3.org/1998/Math/MathML"' in self.sgml_content:
            if '</' in self.sgml_content:
                main_tag = self.sgml_content[self.sgml_content.rfind('</') + 2:]
                main_tag = main_tag[:main_tag.find('>')]
                if '<' + main_tag + ' ':
                    self.sgml_content = self.sgml_content.replace('<' + main_tag + ' ', '<' + main_tag + ' xmlns:mml="http://www.w3.org/1998/Math/MathML" ')

    def replace_fontsymbols(self):
        if self.sgml_content.find('<fontsymbol>') > 0:
            html_fontsymbol_items = self.sgmlhtml.get_fontsymbols()
            c = self.sgml_content.replace('<fontsymbol>', '~BREAK~<fontsymbol>')
            c = c.replace('</fontsymbol>', '</fontsymbol>~BREAK~')
            items = [item for item in c.split('~BREAK~') if item.startswith('<fontsymbol>') and item.endswith('</fontsymbol>')]
            i = 0
            for item in items:
                self.sgml_content = self.sgml_content.replace(item, html_fontsymbol_items[i])
                i += 1

    def fix_mkp_href_values(self):
        self.sgml_content = self.sgml_content.replace('href=&quot;?', 'href="?')
        self.sgml_content = self.sgml_content.replace('"">', '">')
        self.sgml_content = self.sgml_content.replace('href=""?', 'href="?')
        self.sorted_graphic_href_items = []
        self.src_folder_graphics = []
        if self.sgml_content.find('href="?' + self.xml_name) > 0:
            # for each graphic in sgml.xml, replace href="?xmlname" by href="image in src or image in work/html"
            html_unknown_href_items = self.sgmlhtml.unknown_href_items

            self.sgml_content = self.sgml_content.replace('<graphic href="?' + self.xml_name, '--FIXHREF--<graphic href="?' + self.xml_name)
            parts = self.sgml_content.split('--FIXHREF--')
            new_parts = []
            i = 0
            alternative_id = 0
            for part in parts:
                if part.startswith('<graphic href="?' + self.xml_name):
                    graphic = part[0:part.find('>')]
                    html_href = html_unknown_href_items[i - 1]
                    if html_href == 'None':
                        # remove <graphic *> e </graphic>, mantendo o restante de item
                        part = part.replace(graphic, '')
                    else:
                        href = get_href_content(graphic)
                        elem_name, elem_id = get_previous_element_which_has_id_attribute(parts[i - 1])
                        src_href, possible_href_names, alternative_id = self.select_href_file_from_src_folder(elem_name, elem_id, alternative_id)
                        renamed_href = src_href
                        if src_href is not None:
                            self.src_folder_graphics.append(src_href)
                        if renamed_href is None and html_href is not None:
                            if os.path.isfile(self.sgmlhtml.html_img_path + '/' + html_href):
                                renamed_href = self.xml_name + html_href.replace('image', '')
                                shutil.copyfile(self.sgmlhtml.html_img_path + '/' + html_href, self.src_path + '/' + renamed_href)

                        self.sorted_graphic_href_items.append((renamed_href, elem_name, elem_id, self.sgmlhtml.html_img_path + '/' + html_href))
                        if renamed_href is not None:
                            part = part.replace(graphic, graphic.replace(href, renamed_href))
                i += 1
                new_parts.append(part)
            self.sgml_content = ''.join(new_parts)

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
                    for ext in self.IMG_EXTENSIONS:
                        href = name + prefix_number + ext
                        possible_href_names.append(href)
                        if href in self.article_files.files:
                            found.append(href)
        else:
            for name in filenames:
                for ext in self.IMG_EXTENSIONS:
                    href = name + elem_id + ext
                    possible_href_names.append(href)
                    if href in self.article_files.files:
                        found.append(href)
        new_href = None if len(found) == 0 else found[0]
        return (new_href, list(set(possible_href_names)), alternative_id)


def hdimg_to_jpg(source_image_filename, jpg_filename):
    if IMG_CONVERTER:
        try:
            im = Image.open(source_image_filename)
            im.thumbnail(im.size)
            im.save(jpg_filename, "JPEG")
            utils.display_message(jpg_filename)
            print(jpg_filename)
        except Exception as inst:
            utils.display_message('Unable to generate ' + jpg_filename)
            utils.display_message(inst)


def hdimages_to_jpeg(source_path, jpg_path, force_update=False):
    if IMG_CONVERTER:

        for item in os.listdir(source_path):
            image_filename = source_path + '/' + item
            if item.endswith('.tiff') or item.endswith('.eps') or item.endswith('.tif'):
                jpg_filename = source_path + '/' + item[0:item.rfind('.')] + '.jpg'
                doit = True if not os.path.isfile(jpg_filename) else force_update is True

                if doit:
                    hdimg_to_jpg(image_filename, jpg_filename)


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


def message_file_list(label, file_list):
    return '\n' + label + ': ' + str(len(file_list)) + '\n' + '\n'.join(sorted(file_list))


def fix_book_data(item):
    if 'publication-type="book"' in item and '</article-title>' in item:
        item = item.replace('article-title', 'chapter-title')
    if 'publication-type="book"' in item and not '</source>' in item:
        item = item.replace('chapter-title', 'source')
    return item


def fix_mixed_citation_ext_link(ref):
    replacements = {}
    if '<ext-link' in ref and '<mixed-citation>' in ref:
        mixed_citation = ref[ref.find('<mixed-citation>'):]
        mixed_citation = mixed_citation[:mixed_citation.find('</mixed-citation>')+len('</mixed-citation>')]
        new_mixed_citation = mixed_citation
        if not '<ext-link' in mixed_citation:
            for ext_link_item in ref.replace('<ext-link', '~BREAK~<ext-link').split('~BREAK~'):
                if ext_link_item.startswith('<ext-link'):
                    if '</ext-link>' in ext_link_item:
                        ext_link_element = ext_link_item[0:ext_link_item.find('</ext-link>')+len('</ext-link>')]
                        ext_link_content = ext_link_element[ext_link_element.find('>')+1:]
                        ext_link_content = ext_link_content[0:ext_link_content.find('</ext-link>')]
                        if '://' in ext_link_content:
                            urls = ext_link_content.split('://')
                            if not ' ' in urls[0]:
                                replacements[ext_link_content] = ext_link_element
            for ext_link_content, ext_link_element in replacements.items():
                new_mixed_citation = new_mixed_citation.replace(ext_link_content, ext_link_element)
            if new_mixed_citation != mixed_citation:
                ref = ref.replace(mixed_citation, new_mixed_citation)
    return ref


def fix_mixed_citation_label(item):
    if '<label>' in item and '<mixed-citation>' in item:
        mixed_citation = item[item.find('<mixed-citation>')+len('<mixed-citation>'):item.find('</mixed-citation>')]
        label = item[item.find('<label>')+len('<label>'):item.find('</label>')]
        changed = mixed_citation
        if not '<label>' in mixed_citation:
            if not changed.startswith(label):
                sep = ' '
                if changed.startswith('.'):
                    changed = changed[1:].strip()
                    sep = '. '
                if label.endswith('.'):
                    label = label[0:-1]
                    sep = '. '
                changed = label + sep + changed
            if mixed_citation != changed:
                if mixed_citation in item:
                    item = item.replace('<mixed-citation>' + mixed_citation + '</mixed-citation>', '<mixed-citation>' + changed + '</mixed-citation>')
                else:
                    print('Unable to insert label to mixed_citation')
                    print('mixed-citation:')
                    print(mixed_citation)
                    print('item:')
                    print(item)
                    print('changes:')
                    print(changed)
    return item


def normalize_references_item(item):
    if item.startswith('<ref') and item.endswith('</ref>'):
        item = fix_mixed_citation_label(item)
        item = fix_book_data(item)
        item = fix_mixed_citation_ext_link(item)
        item = fix_source(item)
    return item


def fix_source(content):
    if '<source' in content and '<mixed-citation' in content:
        source = content[content.find('<source'):]
        if '</source>' in source:
            source = source[0:source.find('</source>')]
            source = source[source.find('>')+1:]
            mixed_citation = content[content.find('<mixed-citation'):]
            if '</mixed-citation>' in mixed_citation:
                mixed_citation = mixed_citation[0:mixed_citation.find('</mixed-citation>')]
                mixed_citation = mixed_citation[mixed_citation.find('>')+1:]
                s = source.replace(':', ': ')
                if not source in mixed_citation and s in mixed_citation:
                    content = content.replace(source, s)
    return content


def normalize_references(content):
    content = content.replace('<ref', '~BREAK~<ref')
    content = content.replace('</ref>', '</ref>~BREAK~')
    content = ''.join([normalize_references_item(item) for item in content.split('~BREAK~')])
    return content


def xml_status(content, label):
    print(label)
    xml, e = xml_utils.load_xml(content)
    if e is not None:
        print(e)


def remove_xmllang_off_article_title_alt(content):
    if '<article-title ' in content:
        new = []
        for item in content.replace('<article-title ', '<article-title~BREAK~').split('~BREAK~'):
            if item.strip().startswith('xml:lang') and '</article-title>' in item:
                item = item[item.find('>'):]
            new.append(item)
        content = ''.join(new)
    return content


def remove_xmllang_off_source_alt(content):
    if '<source ' in content:
        new = []
        for item in content.replace('<source ', '<source~BREAK~').split('~BREAK~'):
            if item.strip().startswith('xml:lang') and '</source>' in item:
                item = item[item.find('>'):]
            new.append(item)
        content = ''.join(new)
    return content


def remove_styles_off_content(content):
    for tag in ['article-title', 'trans-title', 'kwd', 'source']:
        content = remove_styles_off_tagged_content(tag, content)
    return content


def remove_styles_off_tagged_content(tag, content):
    open_tag = '<' + tag + '>'
    close_tag = '</' + tag + '>'
    content = content.replace(open_tag + ' ', ' ' + open_tag).replace(' ' + close_tag, close_tag + ' ')
    content = content.replace(open_tag, '~BREAK~' + open_tag).replace(close_tag, close_tag + '~BREAK~')
    parts = []
    for part in content.split('~BREAK~'):
        if part.startswith(open_tag) and part.endswith(close_tag):
            data = part[len(open_tag):]
            data = data[0:-len(close_tag)]
            data = ' '.join([w.strip() for w in data.split()])
            part = open_tag + data + close_tag
            remove_all = False
            if tag == 'source' and len(parts) > 0:
                remove_all = 'publication-type="journal"' in parts[len(parts)-1]
            for style in ['italic', 'bold', 'italic']:
                if remove_all or part.startswith(open_tag + '<' + style + '>') and part.endswith('</' + style + '>' + close_tag):
                    part = part.replace('<' + style + '>', '').replace('</' + style + '>', '')
        parts.append(part)
    return ''.join(parts).replace(open_tag + ' ', ' ' + open_tag).replace(' ' + close_tag, close_tag + ' ')


def xml_output(xml_filename, doctype, xsl_filename, result_filename):
    if result_filename == xml_filename:
        shutil.copyfile(xml_filename, xml_filename + '.bkp')
        xml_filename = xml_filename + '.bkp'

    if os.path.exists(result_filename):
        os.unlink(result_filename)

    bkp_xml_filename = xml_utils.apply_dtd(xml_filename, doctype)
    r = java_xml_utils.xml_transform(xml_filename, xsl_filename, result_filename)

    if not result_filename == xml_filename:
        xml_utils.restore_xml_file(xml_filename, bkp_xml_filename)
    if xml_filename.endswith('.bkp'):
        os.unlink(xml_filename)
    return r


class OriginalPackage(object):

    def __init__(self, xml_filenames):
        self.xml_filenames = xml_filenames
        self.articles_files = {}
        self.path = os.path.dirname(xml_filenames[0])

    def setUp(self):
        self.organize_files()
        hdimages_to_jpeg(self.path, self.path, False)

    def organize_files(self):
        files = os.listdir(self.path)
        for filename in self.xml_filenames:
            xml_filename = os.path.basename(filename)
            fname = xml_filename[:-4]
            if '.sgm' in fname:
                fname = fname[:-4]
                article_files = [f for f in files if f.startswith(fname)]
            else:
                article_files = [f for f in files if f.startswith(fname + '-') or f.startswith(fname + '.')]
            self.articles_files[fname] = ArticlePkgFiles(self.path, xml_filename, fname, article_files)
            self.articles_files[fname].convert_images()


class ArticlePkgFiles(object):

    def __init__(self, path, filename, xml_name, files):
        self.path = path
        self.xml_name = xml_name
        self.files = files
        self.filename = filename

    @property
    def xml_filename(self):
        return self.path + '/' + self.filename

    @property
    def splitext(self):
        return [os.path.splitext(f) for f in self.files]

    @property
    def png_files(self):
        return [name for name, ext in self.splitext if ext in ['.png']]

    @property
    def jpg_files(self):
        return [name for name, ext in self.splitext if ext in ['.jpg', '.jpeg']]

    @property
    def tif_files(self):
        return [name for name, ext in self.splitext if ext in ['.tif', '.tiff']]

    def convert_images(self):
        for item in self.tif_files:
            if not item in self.jpg_files and not item in self.png_files:
                source_fname = item + '.tif'
                if not source_fname in self.files:
                    source_fname = item + '.tiff'
                hdimg_to_jpg(self.path + '/' + source_fname, self.path + '/' + item + '.jpg')
                if os.path.isfile(self.path + '/' + item + '.jpg'):
                    self.files.append(item + '.jpg')


class ArticlePkgMaker(object):

    def __init__(self, article_files, doc_files_info, scielo_pkg_path, version, acron, is_db_generation=False):
        self.article_files = article_files
        self.scielo_pkg_path = scielo_pkg_path
        self.version = version
        self.acron = acron
        self.is_db_generation = is_db_generation
        self.doc_files_info = doc_files_info
        self.content = fs_utils.read_file(doc_files_info.xml_filename)
        self.text_messages = []
        self.doc = None
        self.replacements_href_values = []
        self.replacements_related_files_items = {}
        self.replacements_href_files_items = {}

        self.missing_href_files = []
        self.original_href_filenames = []
        self.version_info = xml_versions.DTDFiles('scielo', version)
        self.sgmlxml = None
        self.xml = None
        self.e = None
        #self.sorted_graphic_href_items = []
        #self.src_folder_graphics = []

    def make_article_package(self):
        self.normalize_xml_content()
        self.normalize_filenames()
        self.pack_article_files()

        fs_utils.write_file(self.doc_files_info.err_filename, '\n'.join(self.text_messages))
        html_reports.save(self.doc_files_info.images_report_filename, '', self.get_images_comparison_report())
        if len(self.replacements_related_files_items) > 0:
            self.doc.related_files = [item[1] for item in self.replacements_related_files_items]

        return (self.doc, self.doc_files_info)

    def normalize_xml_content(self):
        xpm_process_logger.register('normalize_xml_content')

        self.content = xml_utils.complete_entity(self.content)

        xpm_process_logger.register('convert_entities_to_chars')
        self.content, replaced_named_ent = xml_utils.convert_entities_to_chars(self.content)
        if len(replaced_named_ent) > 0:
            self.messsages.append('Converted entities:' + '\n'.join(replaced_named_ent) + '-'*30)

        if self.doc_files_info.is_sgmxml:
            self.normalize_sgmlxml()

        self.xml, self.e = xml_utils.load_xml(self.content)
        if self.xml is not None:
            if 'contrib-id-type="' in self.content:
                for contrib_id, url in attributes.CONTRIB_ID_URLS.items():
                    self.content = self.content.replace(' contrib-id-type="' + contrib_id + '">' + url, ' contrib-id-type="' + contrib_id + '">')

            #content = remove_xmllang_off_article_title(content)
            self.content = self.content.replace('<comment content-type="cited"', '<comment')
            self.content = self.content.replace(' - </title>', '</title>').replace('<title> ', '<title>')
            self.content = self.content.replace('&amp;amp;', '&amp;')
            self.content = self.content.replace('&amp;#', '&#')
            self.content = self.content.replace('dtd-version="3.0"', 'dtd-version="1.0"')

            self.content = self.content.replace('ext-link-type="clinical-trial"', 'ext-link-type="ClinicalTrial"')
            self.content = self.content.replace('publication-type="conf-proc"', 'publication-type="confproc"')
            self.content = self.content.replace('publication-type="legaldoc"', 'publication-type="legal-doc"')
            self.content = self.content.replace('publication-type="web"', 'publication-type="webpage"')
            self.content = self.content.replace(' rid=" ', ' rid="')
            self.content = self.content.replace(' id=" ', ' id="')
            self.content = xml_utils.pretty_print(self.content)
            #self.content = remove_xmllang_off(self.content, 'article-title')
            #self.content = remove_xmllang_off(self.content, 'source')
            self.content = remove_xmllang_off_article_title_alt(self.content)
            self.content = remove_xmllang_off_source_alt(self.content)
            self.content = self.content.replace('> :', '>: ')
            self.content = normalize_references(self.content)
            self.content = remove_styles_off_content(self.content)
            self.content = self.content.replace('<institution content-type="normalized"/>', '')
            self.content = self.content.replace('<institution content-type="normalized"></institution>', '')
            self.xml, self.e = xml_utils.load_xml(self.content)

    def normalize_sgmlxml(self):
        self.sgmlxml = SGMLXML(self.article_files, self.content, self.doc_files_info.html_filename)
        self.content = self.sgmlxml.generate_xml(self.version)

    def replace_mimetypes(self):
        r = self.content
        if 'mimetype="replace' in self.content:
            self.content = self.content.replace('mimetype="replace', '_~BREAK~MIME_MIME:')
            self.content = self.content.replace('mime-subtype="replace"', '_~BREAK~MIME_')
            r = ''
            for item in self.content.split('_~BREAK~MIME_'):
                if item.startswith('MIME:'):
                    f = item[5:]
                    f = f[0:f.rfind('"')]
                    result = ''
                    if os.path.isfile(self.src_path + '/' + f):
                        result = mime.guess_type(self.src_path + '/' + f)
                    else:
                        url = urllib.pathname2url(f)
                        result = mime.guess_type(url)
                    try:
                        result = result[0]
                        if '/' in result:
                            m, ms = result.split('/')
                            r += 'mimetype="' + m + '" mime-subtype="' + ms + '"'
                        else:
                            pass
                    except:
                        pass
                else:
                    r += item
        else:
            utils.debugging('.............')
        self.content = r

    def get_images_comparison_report(self):
        if self.sgmlxml is not None:
            r = self.report_comparison_between_markup_and_src_images()
        else:
            r = self.report_images_in_the_package()
        return r

    def report_images_in_the_package(self):
        #self.replacements_href_values
        #self.sgmlxml.sorted_graphic_href_items = []
        #self.sgmlxml.src_folder_graphics = []
        #(elem_name, elem_id, self.sgmlhtml.html_img_path + '/' + html_href)
        rows = []

        rows.append(html_reports.tag('h2', _('Images Report')))
        rows.append(html_reports.tag('p', _('The images are presented in their original dimensions and in the same order they are found in the Markup document.')))

        rows.append('<ol>')
        for name, renamed in self.replacements_href_values:
            rows.append('<li>')
            rows.append(html_reports.tag('h4', renamed))

            # imagem final
            rows.append('<div class="compare_images">')
            rows.append(html_reports.tag('h5', _('* images presented in the same order they are in the XML file')))
            rows.append(html_reports.tag('h5', _('* original dimensions')))
            img_filename = self.scielo_pkg_path + '/' + renamed.replace('.tiff', '.jpg').replace('.tif', '.jpg')
            rows.append('<div class="compare_inline">')
            rows.append(html_reports.link(img_filename, html_reports.image(img_filename)))
            rows.append('</div>')
            rows.append('</div>')

            rows.append('</li>')
        rows.append('</ol>')
        return ''.join(rows)

    def report_comparison_between_markup_and_src_images(self):
        #self.replacements_href_values
        #self.sgmlxml.sorted_graphic_href_items = []
        #self.sgmlxml.src_folder_graphics = []
        #(elem_name, elem_id, self.sgmlhtml.html_img_path + '/' + html_href)
        rows = []
        if self.sgmlxml is not None:

            rows.append(html_reports.tag('h2', _('Images Report')))
            rows.append(html_reports.tag('p', _('This report presents the comparison between the images found in Markup document and in the package.')))
            replacements = {curr_href: new_href for curr_href, new_href in self.replacements_href_values}
            #print(replacements)
            #print(self.sgmlxml.sorted_graphic_href_items)
            #print(self.sgmlxml.src_folder_graphics)

            rows.append('<ol>')
            for name, elem_name, elem_id, filename in self.sgmlxml.sorted_graphic_href_items:
                rows.append('<li>')
                path = os.path.dirname(filename)
                fname = os.path.basename(filename)

                element_label = elem_name + ' ' + elem_id
                style = elem_name if elem_name in ['tabwrap', 'figgrp', 'equation'] else 'inline'

                renamed = replacements.get(name, '???')
                rows.append(html_reports.tag('h4', element_label))
                rows.append(html_reports.tag('h4', name + ' => ' + renamed))

                # imagem final
                replaced = replacements.get(name)
                #rows.append(html_reports.tag('h5', _('Image inserted into the package')))
                #rows.append(html_reports.tag('p', self.scielo_pkg_path))
                rows.append('<div class="compare_images">')
                rows.append(html_reports.tag('h5', _('* images presented in the same order they are in the XML file')))
                rows.append(html_reports.tag('h5', _('* original dimensions')))
                if replaced is not None:
                    img_filename = self.scielo_pkg_path + '/' + renamed.replace('.tiff', '.jpg').replace('.tif', '.jpg')
                    if self.sgmlxml is not None:
                        if name in self.sgmlxml.src_folder_graphics:
                            rows.append(html_reports.tag('h4', _('Image inserted into the package was gotten from src folder')))
                        else:
                            rows.append(html_reports.tag('h4', _('Image inserted into the package was extracted from the .doc file')))
                    rows.append('<div class="compare_' + style + '">')
                    rows.append(html_reports.link(img_filename, html_reports.image(img_filename)))
                    rows.append('</div>')

                if self.sgmlxml is not None:
                    if name in self.sgmlxml.src_folder_graphics:
                        rows.append(html_reports.tag('h4', _('Image in the .doc file')))
                        rows.append('<div class="compare_' + style + '">')
                        img_filename = filename.replace('.tiff', '.jpg').replace('.tif', '.jpg')
                        rows.append(html_reports.link(img_filename, html_reports.image(img_filename)))
                        rows.append('</div>')
                rows.append('</div>')
                rows.append('</li>')
            rows.append('<o/l>')
        return ''.join(rows)

    def normalize_filenames(self):
        xpm_process_logger.register('normalize_filenames')
        self.doc_files_info.new_xml_path = self.scielo_pkg_path
        self.doc = article.Article(self.xml, self.doc_files_info.xml_name)
        self.doc_files_info.new_name = self.doc_files_info.xml_name
        if self.doc.tree is not None:
            if self.doc_files_info.is_sgmxml:
                self.doc_files_info.new_name = self.generate_normalized_package_name()
            self.normalize_href_values()
        self.doc.new_prefix = self.doc_files_info.new_name
        self.doc_files_info.new_xml_filename = self.doc_files_info.new_xml_path + '/' + self.doc_files_info.new_name + '.xml'

    def generate_normalized_package_name(self):
        #doc, acron, self.doc_files_info.xml_name
        xpm_process_logger.register('generate_normalized_package_name')
        vol, issueno, fpage, seq, elocation_id, order, doi = self.doc.volume, self.doc.number, self.doc.fpage, self.doc.fpage_seq, self.doc.elocation_id, self.doc.order, self.doc.doi
        issns = [issn for issn in [self.doc.e_issn, self.doc.print_issn] if issn is not None]
        if len(issns) > 0:
            if self.doc_files_info.xml_name[0:9] in issns:
                issn = self.doc_files_info.xml_name[0:9]
            else:
                issn = issns[0]

        suppl = self.doc.volume_suppl if self.doc.volume_suppl else self.doc.number_suppl

        last = format_last_part(fpage, seq, elocation_id, order, doi, issn)
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
        parts = [issn, self.acron, vol, issueno, suppl, last, self.doc.compl]
        r = '-'.join([part for part in parts if part is not None and not part == ''])
        return r

    def normalize_href_values(self):
        href_items = [href for href in self.doc.hrefs if href.is_internal_file]
        if self.doc_files_info.is_sgmxml:
            for href in href_items:
                self.replacements_href_values.append((href.src, self.get_normalized_href_value(href)))
        else:
            for href in href_items:
                self.replacements_href_values.append((href.src, self.add_extension(href.src, href.src)))
        changed = False
        if len(self.replacements_href_values) > 0:
            for current, new in self.replacements_href_values:
                if current != new:
                    utils.display_message(current + ' => ' + new)
                    self.content = self.content.replace('href="' + current, 'href="' + new)
                    changed = True
        if changed:
            self.xml, self.e = xml_utils.load_xml(self.content)
            self.doc = article.Article(self.xml, self.doc_files_info.xml_name)

    def get_normalized_href_value(self, href):
        href_type = href_attach_type(href.parent.tag, href.element.tag)
        if href.id is None:
            href_name = href.src.replace(self.doc_files_info.xml_name, '')
            if href_name[0:1] in '-_':
                href_name = href_name[1:]
        else:
            href_name = href.id
            if '.' in href.src:
                href_name += href.src[href.src.rfind('.'):]
        href_name = href_name.replace('image', '').replace('img', '')
        if href_name.startswith(href_type):
            href_type = ''
        new_href = self.doc_files_info.new_name + '-' + href_type + href_name
        return self.add_extension(href.src, new_href)

    def add_extension(self, href, new_href):
        if not '.' in new_href:
            extensions = [f[f.rfind('.'):] for f in os.listdir(self.doc_files_info.xml_path) if f.startswith(href + '.')]
            if len(extensions) > 1:
                extensions = [e for e in extensions if '.tif' in e or '.eps' in e] + extensions
            if len(extensions) > 0:
                new_href += extensions[0]
        return new_href

    def eliminate_old_package_files(self):
        for item in os.listdir(self.scielo_pkg_path):
            if item.startswith(self.doc_files_info.new_name) or item.endswith('.sgm.xml'):
                eliminate = (item.endswith('incorrect.xml') or item.endswith('.sgm.xml'))
                if eliminate is False:
                    eliminate = not item.endswith('.xml')
                if eliminate:
                    try:
                        os.unlink(self.scielo_pkg_path + '/' + item)
                    except:
                        pass

    def pack_article_files(self):
        xpm_process_logger.register('pack_article_files: inicio')

        self.eliminate_old_package_files()

        if self.doc.tree is None:
            self.text_messages.append(self.e)
            self.text_messages.append(validation_status.STATUS_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=self.doc_files_info.new_xml_filename) + '\n' + _('Open it with XML Editor or Web Browser to find the errors easily.'))
        else:
            self.pack_article_href_files()
            self.pack_article_related_files()
            self.text_messages.append(self.generate_packed_files_report())

        self.pack_article_xml_file()
        xpm_process_logger.register('pack_article_files: fim')

    def pack_article_href_files(self):
        xpm_process_logger.register('pack_article_href_files: inicio')
        self.replacements_href_files_items = {}
        self.missing_href_files = []
        for original_href, normalized_href in self.replacements_href_values:
            original_href_name, original_href_ext = os.path.splitext(original_href)
            normalized_href_name, normalized_href_ext = os.path.splitext(normalized_href)
            original2normalized = [(src_file, src_file.replace(original_href_name, normalized_href_name)) for src_file in self.article_files.files if src_file.startswith(original_href_name + '.')]
            for original, normalized in original2normalized:
                self.replacements_href_files_items[original] = normalized
                shutil.copyfile(self.doc_files_info.xml_path + '/' + original, self.scielo_pkg_path + '/' + normalized)
            if len(original2normalized) == 0:
                self.missing_href_files.append((original_href, normalized_href))
        xpm_process_logger.register('pack_article_href_files: fim')

    def pack_article_related_files(self):
        xpm_process_logger.register('pack_article_related_files: inicio')
        self.replacements_related_files_items = {}
        for f in self.article_files.files:
            source_filename = self.article_files.path + '/' + f
            dest_filename = self.scielo_pkg_path + '/' + f.replace(self.doc_files_info.xml_name, self.doc_files_info.new_name)
            if f.startswith(self.doc_files_info.xml_name + '.'):
                self.replacements_related_files_items[f] = dest_filename
                shutil.copyfile(source_filename, dest_filename)
            elif f.startswith(self.doc_files_info.xml_name + '-'):
                if not f in self.replacements_href_files_items.keys():
                    self.replacements_related_files_items[f] = dest_filename
                    shutil.copyfile(source_filename, dest_filename)
        xpm_process_logger.register('pack_article_related_files: fim')

    def generate_packed_files_report(self):
        #doc_files_info, dest_path, related_packed, href_packed, href_replacement_items, not_found

        def format(files_list):
            return ['   ' + c + ' => ' + n for c, n in files_list]

        def format2(files_list):
            return ['   ' + k + ' => ' + files_list[k] for k in sorted(files_list.keys())]

        xml_name = self.doc_files_info.xml_name
        new_name = self.doc_files_info.new_name
        src_path = self.doc_files_info.xml_path
        dest_path = self.scielo_pkg_path

        log = []

        log.append(_('Report of files') + '\n' + '-'*len(_('Report of files')) + '\n')

        if src_path != dest_path:
            log.append(_('Source path') + ':   ' + src_path)
        log.append(_('Package path') + ':  ' + dest_path)
        if src_path != dest_path:
            log.append(_('Source XML name') + ': ' + xml_name)
        log.append(_('Package XML name') + ': ' + new_name)

        log.append(message_file_list(_('Total of related files'), format2(self.replacements_related_files_items)))
        log.append(message_file_list(_('Total of files in package'), format2(self.replacements_href_files_items)))
        log.append(message_file_list(_('Total of @href in XML'), format(self.replacements_href_values)))
        log.append(message_file_list(_('Total of files not found in package'), format(self.missing_href_files)))

        return '\n'.join(log)

    def pack_article_xml_file(self):
        xpm_process_logger.register('pack_article_xml_file')
        original = self.version_info.local
        final = self.version_info.remote
        if self.is_db_generation:
            original = self.version_info.remote
            final = self.version_info.local
        self.content = self.content.replace('"' + original + '"', '"' + final + '"')
        fs_utils.write_file(self.doc_files_info.new_xml_filename, self.content)
        xpm_process_logger.register('pack_article_xml_file: fim')


def make_package(xml_files, report_path, wrk_path, scielo_pkg_path, version, acron, is_db_generation=False):
    package = OriginalPackage(xml_files)
    package.setUp()

    doc_items = {}
    article_work_area_items = {}
    xpm_process_logger.register('make packages')
    utils.display_message('\n' + _('Make package for {n} files.').format(n=str(len(xml_files))))
    n = '/' + str(len(xml_files))
    index = 0

    for xml_name, article_files in package.articles_files.items():
        article_work_area = serial_files.ArticleWorkArea(article_files.xml_filename, report_path, wrk_path)
        article_work_area.clean()

        index += 1
        item_label = str(index) + n + ': ' + article_work_area.xml_name
        utils.display_message(item_label)

        article_pkg_maker = ArticlePkgMaker(article_files, article_work_area, scielo_pkg_path, version, acron, is_db_generation)
        doc, article_work_area = article_pkg_maker.make_article_package()

        article_work_area_items[article_work_area.xml_name] = article_work_area
        doc_items[article_work_area.xml_name] = doc

    return (doc_items, article_work_area_items)


def make_pmc_report(articles, doc_files_info_items):
    for xml_name, doc in articles.items():
        msg = _('generating report...')
        if doc.tree is None:
            msg = _('Unable to generate the XML file.')
        else:
            if doc.journal_id_nlm_ta is None:
                msg = _('It is not PMC article or unable to find journal-id (nlm-ta) in the XML file.')
        html_reports.save(doc_files_info_items[xml_name].pmc_style_report_filename, 'PMC Style Checker', msg)


def make_pmc_package(articles, doc_files_info_items, scielo_pkg_path, pmc_pkg_path, scielo_dtd_files, pmc_dtd_files):
    do_it = False

    utils.display_message('\n')
    utils.display_message(_('Generating PMC Package'))
    n = '/' + str(len(articles))
    index = 0

    for xml_name, doc in articles.items():
        doc_files_info = doc_files_info_items[xml_name]
        if doc.journal_id_nlm_ta is None:
            html_reports.save(doc_files_info.pmc_style_report_filename, 'PMC Style Checker', _('{label} is a mandatory data, and it was not informed. ').format(label='journal-id (nlm-ta)'))
        else:
            do_it = True

            index += 1
            item_label = str(index) + n + ': ' + doc_files_info.xml_name
            utils.display_message(item_label)

            pmc_xml_filename = pmc_pkg_path + '/' + doc_files_info.new_name + '.xml'
            xml_output(doc_files_info.new_xml_filename, scielo_dtd_files.doctype_with_local_path, scielo_dtd_files.xsl_output, pmc_xml_filename)

            xpchecker.style_validation(pmc_xml_filename, pmc_dtd_files.doctype_with_local_path, doc_files_info.pmc_style_report_filename, pmc_dtd_files.xsl_prep_report, pmc_dtd_files.xsl_report, pmc_dtd_files.database_name)
            xml_output(pmc_xml_filename, pmc_dtd_files.doctype_with_local_path, pmc_dtd_files.xsl_output, pmc_xml_filename)

            add_files_to_pmc_package(scielo_pkg_path, pmc_xml_filename, doc.language)

    if do_it:
        make_pkg_zip(pmc_pkg_path)


def validate_pmc_image(img_filename):
    img = utils.tiff_image(img_filename)
    if img is not None:
        if img.info is not None:
            if img.info.get('dpi') < 300:
                print(_('PMC: {file} has invalid dpi: {dpi}').format(file=os.path.basename(img_filename), dpi=img.info.get('dpi')))


def add_files_to_pmc_package(scielo_pkg_path, pmc_xml_filename, language):
    dest_path = os.path.dirname(pmc_xml_filename)
    xml_name = os.path.basename(pmc_xml_filename)[:-4]
    xml, e = xml_utils.load_xml(pmc_xml_filename)
    doc = article.Article(xml, xml_name)
    if language == 'en':
        if os.path.isfile(scielo_pkg_path + '/' + xml_name + '.pdf'):
            shutil.copyfile(scielo_pkg_path + '/' + xml_name + '.pdf', dest_path + '/' + xml_name + '.pdf')
        for item in doc.href_files:
            if os.path.isfile(scielo_pkg_path + '/' + item.src):
                shutil.copyfile(scielo_pkg_path + '/' + item.src, dest_path + '/' + item.src)
                validate_pmc_image(dest_path + '/' + item.src)
    else:
        if os.path.isfile(scielo_pkg_path + '/' + xml_name + '-en.pdf'):
            shutil.copyfile(scielo_pkg_path + '/' + xml_name + '-en.pdf', dest_path + '/' + xml_name + '.pdf')
        content = fs_utils.read_file(pmc_xml_filename)
        for item in doc.href_files:
            new = item.src.replace('-en.', '.')
            content = content.replace(item.src, new)
            if os.path.isfile(scielo_pkg_path + '/' + item.src):
                shutil.copyfile(scielo_pkg_path + '/' + item.src, dest_path + '/' + new)
                validate_pmc_image(dest_path + '/' + new)
        fs_utils.write_file(pmc_xml_filename, content)


def pack_and_validate(xml_files, results_path, acron, version, is_db_generation=False):
    global DISPLAY_REPORT
    global GENERATE_PMC
    is_xml_generation = any([f.endswith('.sgm.xml') for f in xml_files])

    scielo_pkg_path = results_path + '/scielo_package'
    pmc_pkg_path = results_path + '/pmc_package'
    report_path = results_path + '/errors'
    wrk_path = results_path + '/work'

    report_components = {}

    pmc_dtd_files = xml_versions.DTDFiles('pmc', version)
    scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    for d in [scielo_pkg_path, pmc_pkg_path, report_path, wrk_path]:
        if not os.path.isdir(d):
            os.makedirs(d)

    if len(xml_files) == 0:
        utils.display_message(_('No files to process'))
    else:
        articles, articles_work_area = make_package(xml_files, report_path, wrk_path, scielo_pkg_path, version, acron, is_db_generation)

        doi_services = article_validations.DOI_Services()

        articles_pkg = pkg_validations.ArticlesPackage(scielo_pkg_path, articles, is_xml_generation)

        articles_data = pkg_validations.ArticlesData()
        articles_data.setup(articles_pkg, xc_models.JournalsManager(), db_manager=None)

        articles_set_validations = pkg_validations.ArticlesSetValidations(articles_pkg, articles_data, xpm_process_logger)
        articles_set_validations.validate(doi_services, scielo_dtd_files, articles_work_area)

        reports = pkg_validations.ReportsMaker(articles_set_validations, xpm_version(), None, display_report=DISPLAY_REPORT)

        if not is_xml_generation:
            filename = report_path + '/xml_package_maker.html'
            reports.processing_result_location = os.path.dirname(report_path)
            reports.save_report(report_path, 'xml_package_maker.html', _('XML Package Maker Report'))

        if not is_db_generation:
            if is_xml_generation:
                make_pmc_report(articles, articles_work_area)
            if is_pmc_journal(articles):
                if GENERATE_PMC:
                    make_pmc_package(articles, articles_work_area, scielo_pkg_path, pmc_pkg_path, scielo_dtd_files, pmc_dtd_files)
                else:
                    print('='*10)
                    print(_('To generate PMC package, add -pmc as parameter'))
                    print('='*10)

            #make_pkg_zip(scielo_pkg_path)
            #if not is_xml_generation:
            #    make_pkg_items_zip(scielo_pkg_path)

        utils.display_message(_('Result of the processing:'))
        utils.display_message(results_path)
        xpm_process_logger.write(report_path + '/log.txt')


def is_pmc_journal(articles):
    r = False
    for doc in articles.values():
        if doc.journal_id_nlm_ta is not None:
            r = True
            break
    return r


def get_xml_package_folders_info(input_pkg_path):
    xml_files = []
    results_path = ''

    if os.path.isdir(input_pkg_path):
        xml_files = sorted([input_pkg_path + '/' + f for f in os.listdir(input_pkg_path) if f.endswith('.xml') and not f.endswith('.sgm.xml')])
        results_path = input_pkg_path + '_xml_package_maker_result'
        fs_utils.delete_file_or_folder(results_path)
        os.makedirs(results_path)

    elif os.path.isfile(input_pkg_path):
        if input_pkg_path.endswith('.sgm.xml'):
            # input_pkg_path = ?/serial/<acron>/<issueid>/markup_xml/work/<name>/<name>.sgm.xml
            # fname = <name>.sgm.xml
            fname = os.path.basename(input_pkg_path)

            #results_path = ?/serial/<acron>/<issueid>/markup_xml/work/<name>
            results_path = os.path.dirname(input_pkg_path)

            #results_path = ?/serial/<acron>/<issueid>/markup_xml/work
            results_path = os.path.dirname(results_path)

            #results_path = ?/serial/<acron>/<issueid>/markup_xml
            results_path = os.path.dirname(results_path)

            #src_path = ?/serial/<acron>/<issueid>/markup_xml/src
            src_path = results_path + '/src'
            if not os.path.isdir(src_path):
                os.makedirs(src_path)
            for item in os.listdir(src_path):
                if item.endswith('.sgm.xml'):
                    os.unlink(src_path + '/' + item)
            shutil.copyfile(input_pkg_path, src_path + '/' + fname)
            xml_files = [src_path + '/' + fname]
        elif input_pkg_path.endswith('.xml'):
            xml_files = [input_pkg_path]
            results_path = os.path.dirname(input_pkg_path) + '_xml_package_maker_result'
            if not os.path.isdir(results_path):
                os.makedirs(results_path)
    return (xml_files, results_path)


def make_packages(path, acron, version='1.0', is_db_generation=False, pmc=False):
    global GENERATE_PMC

    if pmc is True:
        GENERATE_PMC = pmc
    path = fs_utils.fix_path(path)
    xml_files, results_path = get_xml_package_folders_info(path)
    if len(xml_files) > 0:
        pack_and_validate(xml_files, results_path, acron, version, is_db_generation)
    utils.display_message('finished')


def get_inputs(args):
    global DISPLAY_REPORT
    global GENERATE_PMC

    args = [arg.decode(encoding=sys.getfilesystemencoding()) for arg in args]
    script = args[0]
    path = None
    acron = None

    items = []
    for item in args:
        if item == '-auto':
            DISPLAY_REPORT = False
        elif item == '-pmc':
            GENERATE_PMC = True
        else:
            items.append(item)

    if len(items) == 3:
        script, path, acron = items
    elif len(items) == 2:
        script, path = items
    return (script, path, acron)


def call_make_packages(args, version):
    script, path, acron = get_inputs(args)

    if path is None and acron is None:
        # GUI
        import xml_gui
        xml_gui.open_main_window(False, None)

    else:
        errors = validate_inputs(path, acron)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ATTENTION =====\n')
            messages.append('ERROR: ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python ' + script + ' <xml_src> [-auto]')
            messages.append(_('where') + ':')
            messages.append('  <xml_src> = ' + _('XML filename or path which contains XML files'))
            messages.append('  [-auto]' + _('optional parameter to omit report'))
            messages.append('\n'.join(errors))
            utils.display_message('\n'.join(messages))
        else:
            make_packages(path, acron)


def validate_inputs(xml_path, acron):
    return xml_utils.is_valid_xml_path(xml_path)


def make_zip(files, zip_name):
    try:
        zipf = zipfile.ZipFile(zip_name, 'w')
        for f in files:
            zipf.write(f, arcname=os.path.basename(f))
        zipf.close()
    except:
        pass


def make_pkg_zip(src_pkg_path):
    pkg_name = None
    for item in os.listdir(src_pkg_path):
        if item.endswith('.xml'):
            if '-' in item:
                pkg_name = item[0:item.rfind('-')]

    if pkg_name is not None:
        dest_path = src_pkg_path + '_zips'
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        zip_name = dest_path + '/' + pkg_name + '.zip'
        make_zip([src_pkg_path + '/' + f for f in os.listdir(src_pkg_path)], zip_name)


def make_pkg_items_zip(src_pkg_path):
    dest_path = src_pkg_path + '_zips'
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    xml_files = [src_pkg_path + '/' + f for f in os.listdir(src_pkg_path) if f.endswith('.xml')]
    for xml_filename in xml_files:
        make_pkg_item_zip(xml_filename, dest_path)


def make_pkg_item_zip(xml_filename, dest_path):
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)

    src_path = os.path.dirname(xml_filename)
    xml_name = os.path.basename(xml_filename)
    name = xml_name[0:-4]
    try:
        zipf = zipfile.ZipFile(dest_path + '/' + name + '.zip', 'w')
        for item in os.listdir(src_path):
            if item.startswith(name + '.') or item.startswith(name + '-'):
                zipf.write(src_path + '/' + item, arcname=item)
        zipf.close()
    except:
        pass


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
