# coding=utf-8

import os
import sys
import urllib
import shutil
from mimetypes import MimeTypes

from __init__ import _
from . import article
from . import xml_versions
from . import sgmlxml
from . import img_utils
from . import utils
from . import xml_utils
from . import fs_utils
from . import attributes
from . import workarea
from . import article_validations
from . import package_validations
from . import serial_files

from . import validators

import html_reports


messages = []
mime = MimeTypes()


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
xpm_process_logger = fs_utils.ProcessLogger()


def xpm_version():
    version_files = [
        CURRENT_PATH + '/../../xpm_version.txt',
        CURRENT_PATH + '/../../cfg/xpm_version.txt',
        CURRENT_PATH + '/../../cfg/version.txt',
    ]
    version = ''
    for f in version_files:
        if os.path.isfile(f):
            version = open(f).readlines()[0].decode('utf-8')
            break
    return version


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
            stage = 'xpm'
            if sgm_xml is not None:
                xml_list = [sgmlxml_workarea(sgm_xml, acron, version)]
                stage = 'xml'
            make_packages(xml_list, version, DISPLAY_REPORT, GENERATE_PMC, stage)


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


def sgmlxml_workarea(sgm_xml_filename, acron, version):
    wk = sgmlxml.SGMLXMLWorkarea(sgm_xml_filename)
    sgmlxml2xml = sgmlxml.SGMLXML2SPSXMLConverter(xml_versions.xsl_sgml2xml(version))
    package_maker = sgmlxml.SGMLXML2SPSXMLPackageMaker(wk)
    package_maker.pack(acron, sgmlxml2xml)
    return package_maker.xml_pkgfiles.filename


def xml_list_workarea(xml_list, stage):
    output_path = os.path.dirname(xml_list[0]) + '_' + stage
    return [workarea.Workarea(item, output_path) for item in xml_list]


def make_packages(xml_list, version, DISPLAY_REPORT, GENERATE_PMC, stage='xpm'):
    scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    """
    dtd_location_replacement = (scielo_dtd_files.local, scielo_dtd_files.remote)
    if stage == 'xc':
        dtd_location_replacement = (scielo_dtd_files.remote, scielo_dtd_files.local)
    """
    is_xml_generation = stage == 'xml'
    is_db_generation = stage == 'xc'
    package_folder = workarea.PackageFolder(workareas[0].xml_pkgfiles.path)
    scielo_pkg_path = workareas[0].scielo_package_path
    pmc_pkg_path = workareas[0].pmc_package_path
    report_path = workareas[0].reports_path
    results_path = os.path.dirname(report_path)
    article_items = {}
    article_work_area_items = {}
    wks = {}

    is_pmc_journal = False

    for wk in workareas:
        spsxml = SPSXML(wk)
        spsxml.normalize()
        spsxml.pack()

        if is_pmc_journal is False:
            if spsxml.doc.journal_id_nlm_ta is not None:
                is_pmc_journal = True
        wk.outputs.new_name = wk.xml_pkgfiles.name
        wk.outputs.new_xml_filename = wk.scielo_pkgfiles.filename
        wk.outputs.xml_name = wk.name
        wk.outputs.xml_path = wk.scielo_pkgfiles.path
        wk.outputs.xml_filename = wk.xml_pkgfiles.filename
        spsxml.doc.package_files = wk.scielo_pkgfiles.allfiles

        if not os.path.isfile(wk.outputs.images_report_filename):
            fs_utils.write_file(wk.outputs.images_report_filename, '')
        article_items[wk.name] = spsxml.doc
        article_items[wk.name].package_files = wk.scielo_pkgfiles.allfiles
        article_work_area_items[wk.name] = wk.outputs
        wks[wk.name] = wk

    pmc_package_maker = PMCPackageMaker(version)

    doi_services = article_validations.DOI_Services()

    pkgreports = package_validations.PackageReports(package_folder, article_items, wks)
    pkgissuedata = package_validations.PackageIssueData(article_items)
    registered_issue_data = package_validations.RegisteredIssueData(db_manager=None)
    registered_issue_data.get_data(pkgissuedata)

    validator = package_validations.ArticlesValidator(
        doi_services,
        scielo_dtd_files,
        registered_issue_data,
        pkgissuedata,
        scielo_pkg_path,
        is_xml_generation)

    articles_data_reports = package_validations.ArticlesDataReports(article_items)
    articles_validations_reports = validator.validate(article_items, article_work_area_items)

    files_final_location = serial_files.FilesFinalLocation(scielo_pkg_path, pkgissuedata.acron, pkgissuedata.issue_label, web_app_path=None)

    reports = package_validations.ReportsMaker(pkgreports, articles_data_reports, articles_validations_reports, files_final_location, xpm_version(), None)

    if not is_xml_generation:
        reports.processing_result_location = results_path
        reports.save_report(report_path, 'xpm.html', _('XML Package Maker Report'))
        if DISPLAY_REPORT:
            html_reports.display_report(report_path + '/xpm.html')

    if not is_db_generation:
        if is_xml_generation:
            pmc_package_maker.make_report(article_items, article_work_area_items)

        if is_pmc_journal:
            if GENERATE_PMC:
                pmc_package_maker.make_package(article_items, article_work_area_items)
                workarea.PackageFolder(pmc_pkg_path).zip()

            else:
                print('='*10)
                print(_('To generate PMC package, add -pmc as parameter'))
                print('='*10)

    if not is_xml_generation and not is_db_generation:
        workarea.PackageFolder(scielo_pkg_path).zip()

    utils.display_message(_('Result of the processing:'))
    utils.display_message(results_path)
    xpm_process_logger.write(report_path + '/log.txt')


class SPSXML(object):

    def __init__(self, workarea):
        self.workarea = workarea
        self.spsxmlcontent = SPSXMLContent(fs_utils.read_file(self.workarea.xml_pkgfiles.filename))

    def normalize(self):
        self.spsxmlcontent.normalize()
        return self.spsxmlcontent.content

    @property
    def xml(self):
        _xml, e = xml_utils.load_xml(self.spsxmlcontent.content)
        if _xml is not None:
            return _xml

    @property
    def doc(self):
        if self.xml is not None:
            a = article.Article(self.xml, self.workarea.xml_pkgfiles.name)
            a.new_prefix = self.workarea.xml_pkgfiles.name
            return a

    def pack(self):
        self.workarea.xml_pkgfiles.copy(self.workarea.scielo_pkgfiles.path)
        fs_utils.write_file(self.workarea.scielo_pkgfiles.filename, self.spsxmlcontent.content)


class SPSXMLContent(xml_utils.XMLContent):

    def __init__(self, content):
        xml_utils.XMLContent.__init__(self, content)

    @property
    def xml(self):
        _xml, e = xml_utils.load_xml(self.content)
        if _xml is not None:
            return _xml

    def normalize(self):
        xml_utils.XMLContent.normalize(self)
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
        for href in self.doc.hrefs:
            if href.is_internal_file:
                new = self.workarea.name_with_extension(href.src, href.src)
                self.replacements_href_values.append((href.src, new))
                if href.src != new:
                    self.content = self.content.replace('href="' + href.src + '"', 'href="' + new + '"')


class SPSRefXMLContent(xml_utils.XMLContent):

    def __init__(self, content):
        xml_utils.XMLContent.__init__(self, content)

    def normalize(self):
        if self.content.startswith('<ref') and self.content.endswith('</ref>'):
            self.fix_mixed_citation_label()
            self.fix_book_data()
            self.fix_mixed_citation_ext_link()
            self.fix_source()

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


class PMCPackageMaker(object):

    def __init__(self, version):
        self.pmc_dtd_files = xml_versions.DTDFiles('pmc', version)
        self.scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    def make_package(self, article_items, workareas):
        doit = False

        utils.display_message('\n')
        utils.display_message(_('Generating PMC Package'))
        n = '/' + str(len(article_items))
        index = 0

        path = None
        for xml_name, doc in article_items.keys():
            wk = workareas[xml_name]
            path = wk.pmc_pkgfiles.path

            index += 1
            item_label = str(index) + n + ': ' + xml_name
            utils.display_message(item_label)

            doit = PMCPackageItemMaker(doc, wk, self.scielo_dtd_files, self.pmc_dtd_files).make_package()

        if doit and path is not None:
            workarea.PackageFolder(path).zip()

    def make_report(self, article_items, workareas):
        for xml_name, doc in article_items.items():
            msg = _('generating report... ')
            if doc.tree is None:
                msg = _('Unable to generate the XML file. ')
            else:
                if doc.journal_id_nlm_ta is None:
                    msg = _('It is not PMC article or unable to find journal-id (nlm-ta) in the XML file. ')
            html_reports.save(workareas[xml_name].pmc_style_report_filename, 'PMC Style Checker', msg)


class PMCPackageItemMaker(object):

    def __init__(self, doc, wk, scielo_dtd_files, pmc_dtd_files):
        self.doc = doc
        self.wk = wk
        self.pmc_dtd_files = pmc_dtd_files
        self.scielo_dtd_files = scielo_dtd_files
        self.pmc_xml_filename = wk.pmc_pkgfiles.filename
        self.scielo_xml_filename = wk.scielo_pkgfiles.filename
        self.pmc_style_report_filename = self.wk.outputs.pmc_style_report_filename

    def make_package(self):
        if self.doc.journal_id_nlm_ta is None:
            html_reports.save(self.pmc_style_report_filename, 'PMC Style Checker', _('{label} is a mandatory data, and it was not informed. ').format(label='journal-id (nlm-ta)'))
        else:
            xml_output(
                self.scielo_xml_filename,
                self.scielo_dtd_files.doctype_with_local_path,
                self.scielo_dtd_files.xsl_output,
                self.pmc_xml_filename)

            xml_validator = validators.XMLValidator(self.pmc_dtd_files)
            xml_validator.validate_style(
                self.pmc_xml_filename,
                self.pmc_style_report_filename
                )

            xml_output(self.pmc_xml_filename,
                self.pmc_dtd_files.doctype_with_local_path,
                self.pmc_dtd_files.xsl_output,
                self.pmc_xml_filename)

            self.add_files_to_pmc_package()
            self.svg2tiff()
            self.evaluate_tiff_images()
            self.replace_href_values()
            self.normalize_pmc_file()
            return True

    def normalize_pmc_file(self):
        content = fs_utils.read_file(self.pmc_xml_filename)
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
                fs_utils.write_file(self.pmc_xml_filename, ''.join(result))

    def add_files_to_pmc_package(self):
        errors = []
        if self.doc.language == 'en':
            self.wk.scielo_pkgfiles.copy(self.wk.pmc_pkgfiles.path)
            for img in self.wk.pmc_pkgfiles.tiff_items:
                error = img_utils.validate_tiff_image_file(self.wk.pmc_pkgfiles.path+'/'+img)
                if error is not None:
                    errors.append(error)
        else:
            self.remove_en_from_filenames(self)

    def svg2tiff(self):
        for item in self.wk.pmc_pkgfiles.files_except_xml:
            if item.endswith('.svg'):
                img_utils.convert_svg2png(self.wk.pmc_pkgfiles.path + '/' + item)
        for item in self.wk.pmc_pkgfiles.files_except_xml:
            if item.endswith('.png'):
                img_utils.convert_png2tiff(self.wk.pmc_pkgfiles.path + '/' + item)

    def evaluate_tiff_images(self):
        errors = []
        for f in self.wk.pmc_pkgfiles.tiff_items:
            error = img_utils.validate_tiff_image_file(self.wk.pmc_pkgfiles.path+'/'+f)
            if error is not None:
                errors.append(error)
        return errors

    def remove_en_from_filenames(self):
        content = fs_utils.read_file(self.wk.pmc_pkgfiles.filename)
        files = [os.path.splitext(f) for f in self.wk.scielo_pkgfiles.files_except_xml]
        files = [(name, name[:-3], ext) for name, ext in files if name.endswith('-en')]
        for name, new_name, ext in files:
            shutil.copyfile(
                self.wk.scielo_pkgfiles.path + '/' + name+ext,
                self.wk.pmc_pkgfiles.path+'/'+new_name+ext)
            content = content.replace(name+ext, new_name+ext)
        fs_utils.write_file(self.pmc_xml_filename, content)

    def replace_href_values(self):
        content = fs_utils.read_file(self.wk.pmc_pkgfiles.filename)
        href_items = {href.name_with_extension: href.ext for href in self.doc.href_files}
        for tif in self.wk.pmc_pkgfiles.tiff_names:
            ext = href_items.get(tif)
            if not ext.startswith('.tif'):
                new_name = tif + '.tif'
                if not new_name in self.wk.pmc_pkgfiles.tiff_items:
                    new_name = tif + '.tiff'
                if new_name in self.wk.pmc_pkgfiles.tiff_items:
                    content = content.replace('href="'+href.src+'"', 'href="'+new_name+'"')
                    print(href.src, new_name)
        fs_utils.write_file(self.pmc_xml_filename, content)


def xml_output(xml_filename, doctype, xsl_filename, result_filename):
    #FIXME
    if result_filename == xml_filename:
        shutil.copyfile(xml_filename, xml_filename + '.bkp')
        xml_filename = xml_filename + '.bkp'

    if os.path.exists(result_filename):
        fs_utils.delete_file_or_folder(result_filename)

    bkp_xml_filename = xml_utils.apply_dtd(xml_filename, doctype)
    r = java_xml_utils.xml_transform(xml_filename, xsl_filename, result_filename)

    if not result_filename == xml_filename:
        xml_utils.restore_xml_file(xml_filename, bkp_xml_filename)
    if xml_filename.endswith('.bkp'):
        fs_utils.delete_file_or_folder(xml_filename)
    return r
