# code=utf-8

import sys


from __init__ import _
from . import utils
from . import xml_utils
from . import fs_utils


# FIXME
mime = MimeTypes()
messages = []


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
xpm_process_logger = fs_utils.ProcessLogger()


def call_make_packages(args, version):
    script, path, acron, DISPLAY_REPORT, GENERATE_PMC = read_inputs(args)

    if path is None and acron is None:
        # GUI
        # FIXME
        import xml_gui
        xml_gui.open_main_window(False, None)
    else:
        sgm_xml, xml_list, errors = evaluate_inputs(path, acron)
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
            if sgm_xml is not None:
                xml_list = [generate_xml(sgm_xml, acron, version)]
            if xml_list is not None:
                validate_xml_list(xml_list, version, DISPLAY_REPORT, GENERATE_PMC)


def read_inputs(args):
    DISPLAY_REPORT = True
    GENERATE_PMC = False

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
    return (script, path, acron, DISPLAY_REPORT, GENERATE_PMC)


def evaluate_inputs(xml_path, acron):
    errors = []
    sgm_xml = None
    xml_list = None
    if xml_path is None:
        errors.append(_('Missing XML location. '))
    else:
        if os.path.isfile(xml_path):
            if xml_path.endswith('.sgm.xml'):
                sgm_xml = xml_path
            elif xml_path.endswith('.xml'):
                xml_list = [xml_path]
            else:
                errors.append(_('Invalid file. XML file required. '))
        elif os.path.isdir(xml_path):
            xml_list = [xml_path + '/' + item for item in os.listdir(xml_path) if item.endswith('.xml')]
            if len(xml_list) == 0:
                errors.append(_('Invalid folder. Folder must have XML files. '))
        else:
            errors.append(_('Missing XML location. '))
    return sgm_xml, xml_list, errors


def generate_xml(sgm_xml_filename, acron, version, scielo_pkg_path):
    workarea = sgmlxml.SGMLXMLWorkarea(sgm_xml_filename)
    sgml_xml = sgmlxml.SGMLXML2SPS(workarea, acron)
    # FIXME
    sgml_xml.convert(acron, xml_versions.xsl_sgml2xml(version))

            if self.doc.tree is None:
            self.text_messages.append(self.e)
            self.text_messages.append(validation_status.STATUS_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=self.doc_files_info.new_xml_filename) + '\n' + _('Open it with XML Editor or Web Browser to find the errors easily. '))

    SPSXML(sgml_xml.workarea.xml_filename, scielo_pkg_path, sgml_xml.xml_name, new_name)
    return sgml_xml.xml_filename


def validate_xml_list(xml_list, version, DISPLAY_REPORT, GENERATE_PMC):
    for item in xml_list:
        spsxml = SPSXML(item, scielo_pkg_path, original_name, new_name)
        spsxml.normalize()


class SPSXMLWorkarea(object):

    def __init__(self, filename):
        super(workarea.Workarea, self).__init__(filename) # Python 2


class SPSXML(object):

    def __init__(self, workarea):
        self.workarea = workarea
        self.content = SPSXMLContent(open(workarea.filename).read())

    def normalize(self):
        self.content.normalize()
        return self.content.content

    @property
    def xml(self):
        _xml, e = xml_utils.load_xml(self.content)
        if _xml is not None:
            return _xml

    @property
    def doc(self):
        a = article.Article(self.xml, self.workarea.name)
        a.new_prefix = self.new_name
        return a

    # FIXME
    def fix_dtd_location(self):
        original = self.version_info.local
        final = self.version_info.remote
        if self.is_db_generation:
            original = self.version_info.remote
            final = self.version_info.local
        self.content = self.content.replace('"' + original + '"', '"' + final + '"')
        fs_utils.write_file(self.doc_files_info.new_xml_filename, self.content)
        xpm_process_logger.register('pack_article_xml_file: fim')

    def normalize_href_values(self):
        for href in self.doc.hrefs:
            if href.is_internal_file:
                new = self.workarea.name_with_extension(href.src, href.src)
                self.replacements_href_values.append((href.src, new))
                if href.src != new:
                    self.content = self.content.replace('href="' + href.src + '"', 'href="' + new + '"')


class SPSXMLContent(xml_utils.XMLContent):

    def __init__(self, content):
        #super().__init__()               # Python 3
        super(xml_utils.XMLContent, self).__init__(content) # Python 2

    @property
    def xml(self):
        _xml, e = xml_utils.load_xml(self.content)
        if _xml is not None:
            return _xml

    def normalize(self):
        super(xml_utils.XMLContent, self).normalize()
        self.insert_mml_namespace()
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
            self.content = self.content.replace('publication-type="conf-proc"', 'publication-type="confproc"')
            self.content = self.content.replace('publication-type="legaldoc"', 'publication-type="legal-doc"')
            self.content = self.content.replace('publication-type="web"', 'publication-type="webpage"')
            self.content = self.content.replace(' rid=" ', ' rid="')
            self.content = self.content.replace(' id=" ', ' id="')
            self.content = xml_utils.pretty_print(self.content)
            self.remove_xmllang_from_element('article-title')
            self.remove_xmllang_from_element('source')
            self.content = self.content.replace('> :', '>: ')
            self.normalize_references()
            for tag in ['article-title', 'trans-title', 'kwd', 'source']:
                self.remove_styles_from_tagged_content(tag)
            self.content = self.content.replace('<institution content-type="normalized"/>', '')
            self.content = self.content.replace('<institution content-type="normalized"></institution>', '')

    def insert_mml_namespace(self):
        if '</math>' in self.content:
            new = []
            for part in self.content.replace('</math>', '</math>BREAK-MATH').split('BREAK-MATH'):
                before = part[:part.find('<math')]
                math = part[part.find('<math'):]
                part = before + math.replace('<', '<mml:').replace('<mml:/', '</mml:')
                new.append(part)
            self.content = ''.join(new)

    def remove_xmllang_from_element(self, element_name):
        start = '<' + element_name + ' '
        mark = '<' + element_name + '~BREAK~'
        end = '</' + element_name + '>'
        if start in self.content:
            new = []
            for item in self.content.replace(start, mark).split('~BREAK~'):
                if item.strip().startswith('xml:lang') and end in item:
                    item = item[item.find('>'):]
                new.append(item)
            self.content = ''.join(new)

    def remove_styles_from_tagged_content(self, tag):
        open_tag = '<' + tag + '>'
        close_tag = '</' + tag + '>'
        self.content = self.content.replace(open_tag + ' ', ' ' + open_tag).replace(' ' + close_tag, close_tag + ' ')
        self.content = self.content.replace(open_tag, '~BREAK~' + open_tag).replace(close_tag, close_tag + '~BREAK~')
        parts = []
        for part in self.content.split('~BREAK~'):
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
        self.content = ''.join(parts).replace(open_tag + ' ', ' ' + open_tag).replace(' ' + close_tag, close_tag + ' ')

    def normalize_references(self):
        self.content = self.content.replace('<ref', '~BREAK~<ref')
        self.content = self.content.replace('</ref>', '</ref>~BREAK~')
        refs = []
        for item in [SPSRefXMLContent(item) for item in self.content.split('~BREAK~')]:
            item.normalize()
            refs.append(item.content)
        self.content = ''.join(refs)

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
                    #utils.display_message(current + ' => ' + new)
                    self.content = self.content.replace('href="' + current + '"', 'href="' + new + '"')
                    changed = True
        if changed:
            self.xml, self.e = xml_utils.load_xml(self.content)
            self.doc = article.Article(self.xml, xml_name)

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


class SPSRefXMLContent(xml_utils.XMLContent):

    def __init__(self, content):
        #super().__init__()               # Python 3
        super(xml_utils.XMLContent, self).__init__(content) # Python 2

    def normalize(self):
        if self.content.startswith('<ref') and self.content.endswith('</ref>'):
            self.content = self.fix_mixed_citation_label()
            self.content = self.fix_book_data()
            self.content = self.fix_mixed_citation_ext_link()
            self.content = self.fix_source()

    def fix_book_data(self):
        if 'publication-type="book"' in self.content and '</article-title>' in self.content:
            self.content = self.content.replace('article-title', 'chapter-title')
        if 'publication-type="book"' in self.content and not '</source>' in self.content:
            self.content = self.content.replace('chapter-title', 'source')

    def fix_mixed_citation_ext_link(self):
        replacements = {}
        if '<ext-link' in self.content and '<mixed-citation>' in self.content:
            mixed_citation = self.content[self.content.find('<mixed-citation>'):]
            mixed_citation = mixed_citation[:mixed_citation.find('</mixed-citation>')+len('</mixed-citation>')]
            new_mixed_citation = mixed_citation
            if not '<ext-link' in mixed_citation:
                for ext_link_item in self.content.replace('<ext-link', '~BREAK~<ext-link').split('~BREAK~'):
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
                    self.content = self.content.replace(mixed_citation, new_mixed_citation)


    def fix_mixed_citation_label(self):
        if '<label>' in self.content and '<mixed-citation>' in self.content:
            mixed_citation = self.content[self.content.find('<mixed-citation>')+len('<mixed-citation>'):self.content.find('</mixed-citation>')]
            label = self.content[self.content.find('<label>')+len('<label>'):self.content.find('</label>')]
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
                    if mixed_citation in self.content:
                        self.content = self.content.replace('<mixed-citation>' + mixed_citation + '</mixed-citation>', '<mixed-citation>' + changed + '</mixed-citation>')
                    else:
                        print('Unable to insert label to mixed_citation')
                        print('mixed-citation:')
                        print(mixed_citation)
                        print('self.content:')
                        print(self.content)
                        print('changes:')
                        print(changed)

    def fix_source(self):
        if '<source' in self.content and '<mixed-citation' in self.content:
            source = self.content[self.content.find('<source'):]
            if '</source>' in source:
                source = source[0:source.find('</source>')]
                source = source[source.find('>')+1:]
                mixed_citation = self.content[self.content.find('<mixed-citation'):]
                if '</mixed-citation>' in mixed_citation:
                    mixed_citation = mixed_citation[0:mixed_citation.find('</mixed-citation>')]
                    mixed_citation = mixed_citation[mixed_citation.find('>')+1:]
                    s = source.replace(':', ': ')
                    if not source in mixed_citation and s in mixed_citation:
                        self.content = self.content.replace(source, s)


class PackageMaker(object):

    def __init_(self, path):
        self.path = path


    def normalize_filenames(self):
        self.doc_files_info.new_xml_path = self.scielo_pkg_path
        self.doc = article.Article(self.xml, self.doc_files_info.xml_name)
        self.doc_files_info.new_name = self.doc_files_info.xml_name
        if self.doc.tree is not None:
            if self.doc_files_info.is_sgmxml:
                self.doc_files_info.new_name = self.generate_normalized_package_name()
            self.normalize_href_values()
        self.doc.new_prefix = self.doc_files_info.new_name
        self.doc_files_info.new_xml_filename = self.doc_files_info.new_xml_path + '/' + self.doc_files_info.new_name + '.xml'


###################################################



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








def hdimg_to_jpg(source_image_filename, jpg_filename):
    if IMG_CONVERTER:
        try:
            im = Image.open(source_image_filename)
            im.thumbnail(im.size)
            im.save(jpg_filename, "JPEG")
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




def message_file_list(label, file_list):
    return '\n' + label + ': ' + str(len(file_list)) + '\n' + '\n'.join(sorted(file_list))




def xml_status(content, label):
    print(label)
    xml, e = xml_utils.load_xml(content)
    if e is not None:
        print(e)



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
        self.article_pkg_files = None
        self.path = os.path.dirname(xml_filenames[0])
        
    def setUp(self):
        self.organize_files()
        hdimages_to_jpeg(self.path, self.path, False)

    def organize_files(self):
        self.orphan_files = [f for f in os.listdir(self.path) if not f.endswith(".xml")]
        self.article_pkg_files = {}
        
        for filename in self.xml_filenames:
            xml_filename = os.path.basename(filename)
            fname = xml_filename[:-4]
            if '.sgm' in fname:
                fname = fname[:-4]
            article_files = package_files(self.path, xml_filename)
            for f in article_files:
                self.orphan_files.remove(f)
            self.article_pkg_files[fname] = ArticlePkgFiles(self.path, xml_filename, fname, article_files)
            self.article_pkg_files[fname].convert_images()


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
            self.doc.related_files = [os.path.basename(f) for f in self.replacements_related_files_items.values()]
        
        self.doc.package_files = package_files(self.scielo_pkg_path, self.doc.new_prefix)
        return (self.doc, self.doc_files_info)



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
        r = ''
        #if self.sgmlxml is not None:
        #    r = self.report_comparison_between_markup_and_src_images()
        r += self.report_images_in_the_package()
        return r

    def report_images_in_the_package(self):
        rows = []
        if len(self.replacements_href_values) == 0:
            rows.append(html_reports.tag('h4', _('No image found')))
        else:
            rows.append('<ol>')
            fixed_markup_href_items = {}
            if self.sgmlxml is not None:
                fixed_markup_href_items = {fixed_mkp_href_name:(elem_name, filename) for fixed_mkp_href_name, elem_name, elem_id, filename in self.sgmlxml.sorted_graphic_href_items}

            for name, renamed in self.replacements_href_values:
                rows.append('<li>')
                if name != renamed:
                    rows.append(html_reports.tag('h4', name + ' => ' + renamed))
                else:
                    rows.append(html_reports.tag('h4', renamed))
                        
                # imagem final
                if self.sgmlxml is not None:
                    if name in fixed_markup_href_items.keys():
                        # name eh fixed markup href 
                        origin = html_reports.tag('h5', _('Extracted from the .doc file'))
                        if name in self.sgmlxml.src_folder_graphics:
                            origin = html_reports.tag('h5', _('Came from src folder'))
                        rows.append(origin)

                rows.append('<div class="compare_images">')
                #rows.append(html_reports.tag('h5', _('* images presented in the same order they are in the XML file')))
                #rows.append(html_reports.tag('h5', _('* original dimensions')))
                img_filename = 'file:///' + self.scielo_pkg_path + '/' + renamed.replace('.tiff', '.jpg').replace('.tif', '.jpg')
                rows.append('<div class="compare_inline">')
                rows.append(html_reports.link(img_filename, html_reports.image(img_filename)))
                rows.append('</div>')

                if self.sgmlxml is not None:
                    if not name in self.sgmlxml.src_folder_graphics:
                        if name in fixed_markup_href_items.keys():
                            elem_name, filename = fixed_markup_href_items.get(name)
                            style = elem_name if elem_name in ['tabwrap', 'figgrp', 'equation'] else 'inline'
                            rows.append(html_reports.tag('h5', _('Image in the .doc file')))
                            rows.append('<div class="compare_' + style + '">')
                            img_filename = 'file:///' + filename.replace('.tiff', '.jpg').replace('.tif', '.jpg')
                            rows.append(html_reports.link(img_filename, html_reports.image(img_filename)))
                            rows.append('</div>')

                rows.append('</div>')
                rows.append('</li>')
            rows.append('</ol>')
        return html_reports.tag('h2', _('Images Report')) + ''.join(rows)

    def report_comparison_between_markup_and_src_images(self):
        #self.replacements_href_values
        #self.sgmlxml.sorted_graphic_href_items = []
        #self.sgmlxml.src_folder_graphics = []
        #(elem_name, elem_id, self.sgmlhtml.html_img_path + '/' + html_href)
        rows = []
        if self.sgmlxml is not None:
            if len(self.sgmlxml.sorted_graphic_href_items) > 0:
                rows.append(html_reports.tag('h2', _('Images Report')))
                rows.append(html_reports.tag('p', _('This report presents the comparison between the images found in Markup document and in the package. ')))
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
                    #rows.append(html_reports.tag('h5', _('* images presented in the same order they are in the XML file')))
                    #rows.append(html_reports.tag('h5', _('* original dimensions')))
                    if replaced is not None:
                        img_filename = 'file:///' + self.scielo_pkg_path + '/' + renamed.replace('.tiff', '.jpg').replace('.tif', '.jpg')
                        if name in self.sgmlxml.src_folder_graphics:
                            rows.append(html_reports.tag('h4', _('Image inserted into the package came from src folder')))
                        else:
                            rows.append(html_reports.tag('h4', _('Image inserted into the package was extracted from the .doc file')))
                        rows.append('<div class="compare_' + style + '">')
                        rows.append(html_reports.link(img_filename, html_reports.image(img_filename)))
                        rows.append('</div>')

                    if name in self.sgmlxml.src_folder_graphics:
                        rows.append(html_reports.tag('h4', _('Image in the .doc file')))
                        rows.append('<div class="compare_' + style + '">')
                        img_filename = 'file:///' + filename.replace('.tiff', '.jpg').replace('.tif', '.jpg')
                        rows.append(html_reports.link(img_filename, html_reports.image(img_filename)))
                        rows.append('</div>')
                    rows.append('</div>')
                    rows.append('</li>')
                rows.append('<o/l>')
        return ''.join(rows)



    def eliminate_old_package_files(self):
        for item in os.listdir(self.scielo_pkg_path):
            if item.startswith(self.doc_files_info.new_name + '-') or item.startswith(self.doc_files_info.new_name + '.') or item.endswith('.sgm.xml'):
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
            self.text_messages.append(validation_status.STATUS_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=self.doc_files_info.new_xml_filename) + '\n' + _('Open it with XML Editor or Web Browser to find the errors easily. '))
        else:
            self.pack_article_href_files()
            self.pack_article_related_files()
            self.text_messages.append(self.generate_packed_files_report())

        self.pack_article_xml_file()
        xpm_process_logger.register('pack_article_files: fim')

    def pack_article_href_files(self):
        xpm_process_logger.register('pack_article_href_files: inicio')
        src_files = []
        if self.sgmlxml is not None:
            src_files = os.listdir(self.doc_files_info.xml_path)
        self.replacements_href_files_items = {}
        self.missing_href_files = []
        for original_href, normalized_href in self.replacements_href_values:
            original_href_name, original_href_ext = os.path.splitext(original_href)
            normalized_href_name, normalized_href_ext = os.path.splitext(normalized_href)
            original2normalized = [(src_file, src_file.replace(original_href_name+'.', normalized_href_name+'.')) for src_file in self.article_files.files if src_file.startswith(original_href_name + '.')]

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
            dest_filename = None
            source_filename = self.article_files.path + '/' + f
            if f.startswith(self.doc_files_info.xml_name + '.') and not f.endswith('.sgm.xml'):
                dest_filename = f.replace(self.doc_files_info.xml_name + '.', self.doc_files_info.new_name + '.')
            elif f.startswith(self.doc_files_info.xml_name + '-'):
                dest_filename = f.replace(self.doc_files_info.xml_name + '-', self.doc_files_info.new_name + '-')
            if dest_filename is not None:
                if not f in self.replacements_href_files_items.keys():
                    self.replacements_related_files_items[f] = dest_filename
                    shutil.copyfile(source_filename, self.scielo_pkg_path + '/' + dest_filename)
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



class PackageMaker(object):

    def __init__(self, xml_files, results_path, acron, version, is_db_generation=False):
        self.version = version
        self.acron = acron
        self.is_db_generation = is_db_generation
        self.xml_files = xml_files
        self.results_path = results_path
        self.scielo_pkg_path = results_path + '/scielo_package'
        self.pmc_pkg_path = results_path + '/pmc_package'
        self.report_path = results_path + '/errors'
        self.xml_path = results_path + '/work'

        for d in [self.scielo_pkg_path, self.pmc_pkg_path, self.report_path, self.wrk_path]:
            if not os.path.isdir(d):
                os.makedirs(d)
        self.pmc_dtd_files = xml_versions.DTDFiles('pmc', version)
        self.scielo_dtd_files = xml_versions.DTDFiles('scielo', version)
        self.article_items = {}
        self.article_work_area_items = {}
        self.is_pmc_journal = False
        self.orphan_files = None

    def make_sps_package(self):
        package = OriginalPackage(self.xml_files)
        package.setUp()
        self.orphan_files = package.orphan_files

        xpm_process_logger.register('make packages')
        utils.display_message('\n' + _('Make package for {n} files. ').format(n=str(len(self.xml_files))))
        n = '/' + str(len(self.xml_files))
        index = 0

        for xml_name, article_files in package.article_pkg_files.items():
            article_work_area = serial_files.ArticleWorkArea(article_files.xml_filename, self.report_path, self.wrk_path)
            article_work_area.clean()

            index += 1
            item_label = str(index) + n + ': ' + article_work_area.xml_name
            utils.display_message(item_label)

            article_pkg_maker = ArticlePkgMaker(article_files, article_work_area, self.scielo_pkg_path, self.version, self.acron, self.is_db_generation)
            self.article_items[xml_name], self.article_work_area_items[xml_name] = article_pkg_maker.make_article_package()
            if self.article_items[xml_name] is not None:
                if self.article_items[xml_name].journal_id_nlm_ta is not None:
                    self.is_pmc_journal = True

    def make_pmc_report(self):
        for xml_name, doc in self.article_items.items():
            msg = _('generating report... ')
            if doc.tree is None:
                msg = _('Unable to generate the XML file. ')
            else:
                if doc.journal_id_nlm_ta is None:
                    msg = _('It is not PMC article or unable to find journal-id (nlm-ta) in the XML file. ')
            html_reports.save(self.article_work_area_items[xml_name].pmc_style_report_filename, 'PMC Style Checker', msg)

    def make_pmc_package(self):
        do_it = False

        utils.display_message('\n')
        utils.display_message(_('Generating PMC Package'))
        n = '/' + str(len(self.article_items))
        index = 0

        for xml_name, doc in self.article_items.items():
            article_work_area = self.article_work_area_items[xml_name]
            if doc.journal_id_nlm_ta is None:
                html_reports.save(article_work_area.pmc_style_report_filename, 'PMC Style Checker', _('{label} is a mandatory data, and it was not informed. ').format(label='journal-id (nlm-ta)'))
            else:
                do_it = True

                index += 1
                item_label = str(index) + n + ': ' + article_work_area.xml_name
                utils.display_message(item_label)

                pmc_xml_filename = self.pmc_pkg_path + '/' + article_work_area.new_name + '.xml'
                xml_output(article_work_area.new_xml_filename, self.scielo_dtd_files.doctype_with_local_path, self.scielo_dtd_files.xsl_output, pmc_xml_filename)

                xpchecker.style_validation(pmc_xml_filename, self.pmc_dtd_files.doctype_with_local_path, article_work_area.pmc_style_report_filename, self.pmc_dtd_files.xsl_prep_report, self.pmc_dtd_files.xsl_report, self.pmc_dtd_files.database_name)
                xml_output(pmc_xml_filename, self.pmc_dtd_files.doctype_with_local_path, self.pmc_dtd_files.xsl_output, pmc_xml_filename)

                self.add_files_to_pmc_package(pmc_xml_filename, doc.language)
                self.normalize_pmc_file(pmc_xml_filename)

        if do_it:
            make_pkg_zip(self.pmc_pkg_path)

    def normalize_pmc_file(self, pmc_xml_filename):
        content = fs_utils.read_file(pmc_xml_filename)
        if 'mml:math' in content:
            result = []
            n = 0
            math_id = None
            for item in content.replace('<mml:math', '~BREAK~<mml:math').split('~BREAK~'):
                if item.startswith('<mml:math'):
                    n += 1
                    elem = item[:item.find('>')]
                    if ' id="' not in elem:
                        math_id = 'math{}'.format(n)
                        item = item.replace('<mml:math', '<mml:math id="{}"'.format(math_id))
                        print(math_id)
                result.append(item)
            if math_id is not None:
                fs_utils.write_file(pmc_xml_filename, ''.join(result))

    def validate_pmc_image(self, img_filename):
        img = utils.tiff_image(img_filename)
        if img is not None:
            if img.info is not None:
                if img.info.get('dpi') < 300:
                    print(_('PMC: {file} has invalid dpi: {dpi}').format(file=os.path.basename(img_filename), dpi=img.info.get('dpi')))

    def add_files_to_pmc_package(self, pmc_xml_filename, language):
        dest_path = os.path.dirname(pmc_xml_filename)
        xml_name = os.path.basename(pmc_xml_filename)[:-4]
        xml, e = xml_utils.load_xml(pmc_xml_filename)
        doc = article.Article(xml, xml_name)
        if language == 'en':
            if os.path.isfile(self.scielo_pkg_path + '/' + xml_name + '.pdf'):
                shutil.copyfile(self.scielo_pkg_path + '/' + xml_name + '.pdf', dest_path + '/' + xml_name + '.pdf')
            for item in doc.href_files:
                if os.path.isfile(self.scielo_pkg_path + '/' + item.src):
                    shutil.copyfile(self.scielo_pkg_path + '/' + item.src, dest_path + '/' + item.src)
                    self.validate_pmc_image(dest_path + '/' + item.src)
        else:
            if os.path.isfile(self.scielo_pkg_path + '/' + xml_name + '-en.pdf'):
                shutil.copyfile(self.scielo_pkg_path + '/' + xml_name + '-en.pdf', dest_path + '/' + xml_name + '.pdf')
            content = fs_utils.read_file(pmc_xml_filename)
            for item in doc.href_files:
                new = item.src.replace('-en.', '.')
                content = content.replace(item.src +'.', new+'.')
                if os.path.isfile(self.scielo_pkg_path + '/' + item.src):
                    shutil.copyfile(self.scielo_pkg_path + '/' + item.src, dest_path + '/' + new)
                    self.validate_pmc_image(dest_path + '/' + new)
            fs_utils.write_file(pmc_xml_filename, content)


def pack_and_validate(xml_files, results_path, acron, version, is_db_generation=False):
    global DISPLAY_REPORT
    global GENERATE_PMC
    is_xml_generation = any([f.endswith('.sgm.xml') for f in xml_files])

    if len(xml_files) == 0:
        utils.display_message(_('No files to process'))
    else:
        pkg_maker = PackageMaker(xml_files, results_path, acron, version, is_db_generation)
        pkg_maker.make_sps_package()

        doi_services = article_validations.DOI_Services()

        articles_pkg = pkg_validations.ArticlesPackage(pkg_maker.scielo_pkg_path, pkg_maker.article_items, is_xml_generation)

        articles_data = pkg_validations.ArticlesData()
        articles_data.setup(articles_pkg, db_manager=None)
        
        articles_set_validations = pkg_validations.ArticlesSetValidations(articles_pkg, articles_data, xpm_process_logger)
        articles_set_validations.validate(doi_services, pkg_maker.scielo_dtd_files, pkg_maker.article_work_area_items)

        files_final_location = serial_files.FilesFinalLocation(pkg_maker.scielo_pkg_path, articles_data.acron, articles_data.issue_label, web_app_path=None)

        reports = pkg_validations.ReportsMaker(pkg_maker.orphan_files, articles_set_validations, files_final_location, xpm_version(), None)

        if not is_xml_generation:
            reports.processing_result_location = os.path.dirname(pkg_maker.report_path)
            reports.save_report(pkg_maker.report_path, 'xpm.html', _('XML Package Maker Report'))
            if DISPLAY_REPORT:
                html_reports.display_report(pkg_maker.report_path + '/xpm.html')

        if not is_db_generation:
            if is_xml_generation:
                pkg_maker.make_pmc_report()

            if pkg_maker.is_pmc_journal:
                if GENERATE_PMC:
                    pkg_maker.make_pmc_package()
                else:
                    print('='*10)
                    print(_('To generate PMC package, add -pmc as parameter'))
                    print('='*10)

        if not is_xml_generation and not is_db_generation:
            make_pkg_zip(pkg_maker.scielo_pkg_path)

        utils.display_message(_('Result of the processing:'))
        utils.display_message(pkg_maker.results_path)
        xpm_process_logger.write(pkg_maker.report_path + '/log.txt')


def get_xml_package_folders_info(input_pkg_path):
    xml_files = []
    results_path = ''

    if os.path.isdir(input_pkg_path):
        xml_files = sorted([input_pkg_path + '/' + f for f in os.listdir(input_pkg_path) if f.endswith('.xml') and not f.endswith('.sgm.xml')])
        results_path = input_pkg_path + '_xpm'
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
            results_path = os.path.dirname(input_pkg_path) + '_xpm'
            if not os.path.isdir(results_path):
                os.makedirs(results_path)
    return (xml_files, results_path)



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






def package_files(pkg_path, xml_filename):
    fname = xml_filename
    if xml_filename.endswith('.xml'):
        fname, ext = os.path.splitext(xml_filename)
        if fname.endswith('.sgm'):
            fname = fname[:-4]
    r = [item for item in os.listdir(pkg_path) if (item.startswith(fname + '-') or item.startswith(fname + '.')) and not item.endswith('.xml')]
    if '.sgm.xml' in xml_filename:
        fname = xml_filename[:-8]
        suffixes = ['t', 'f', 'e', 'img', 'image']
        suffixes.extend(['-'+s for s in suffixes])
        for suffix in suffixes:
            r += [item for item in os.listdir(pkg_path) if item.startswith(fname + suffix)]
        r = list(set(r))
    r = [item for item in r if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml')]
    #print(fname, r)
    return sorted(r)
    