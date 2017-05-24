# code=utf-8

import os
import sys

from __init__ import _
from . import article
from . import xml_versions
from . import sgmlxml
from . import img_utils
from . import utils
from . import xml_utils
from . import fs_utils


messages = []


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
                xml_filename = generate_xml(sgm_xml_filename, acron, version)
                xml_list = [xml_filename]
                stage = 'xml'
            if xml_list is not None:
                validate_xml_list(xml_list, version, DISPLAY_REPORT, GENERATE_PMC, stage)


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


#FIXME
def generate_xml(sgm_xml_filename, acron, version):
    workarea = sgmlxml.SGMLXMLWorkarea(sgm_xml_filename)
    sgml_xml = sgmlxml.SGMLXML2SPSXML(workarea)
    sgml_xml.convert(acron, xml_versions.xsl_sgml2xml(version))
    sgml_xml.pack()
    return workarea.temp_package_files.filename


def validate_xml_list(xml_list, version, DISPLAY_REPORT, GENERATE_PMC, stage='xpm'):
    scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    """
    dtd_location_replacement = (scielo_dtd_files.local, scielo_dtd_files.remote)
    if stage == 'xc':
        dtd_location_replacement = (scielo_dtd_files.remote, scielo_dtd_files.local)
    """
    is_xml_generation = stage == 'xml'
    is_db_generation = stage == 'xc'
    package_folder = PackageFolder(xml_list, stage)
    scielo_pkg_path = package_folder.path
    pmc_pkg_path = os.path.dirname(scielo_pkg_path) + '/pmc_package'
    is_pmc_journal = False

    #FIXME name
    for name, workarea in package_folder.workarea_items.items():
        spsxml = SPSXML(workarea)
        spsxml.normalize()
        spsxml.pack()

        if is_pmc_journal is False:
            if spsxml.doc.journal_id_nlm_ta is not None:
                is_pmc_journal = True

        article_items[name] = (spsxml.doc, workarea.outputs)
        article_work_area_items[name] = workarea.outputs
        report_path = workarea.report_path
        results_path = os.path.dirname(report_path)

    pmc_package_maker = PMCPackageMaker(article_items, article_work_area_items, scielo_pkg_path, pmc_pkg_path, version)

    doi_services = article_validations.DOI_Services()

    articles_pkg = pkg_validations.ArticlesPackage(scielo_pkg_path, article_items, is_xml_generation)

    articles_data = pkg_validations.ArticlesData()
    articles_data.setup(articles_pkg, db_manager=None)
    articles_set_validations = pkg_validations.ArticlesSetValidations(articles_pkg, articles_data, xpm_process_logger)
    articles_set_validations.validate(doi_services, scielo_dtd_files, article_work_area_items)

    files_final_location = serial_files.FilesFinalLocation(scielo_pkg_path, articles_data.acron, articles_data.issue_label, web_app_path=None)

    reports = pkg_validations.ReportsMaker(package_folder.orphans, articles_set_validations, files_final_location, xpm_version(), None)

    if not is_xml_generation:
        reports.processing_result_location = results_path
        reports.save_report(report_path, 'xpm.html', _('XML Package Maker Report'))
        if DISPLAY_REPORT:
            html_reports.display_report(report_path + '/xpm.html')

    if not is_db_generation:
        if is_xml_generation:
            pmc_package_maker.make_pmc_report()

        if is_pmc_journal:
            if GENERATE_PMC:
                pmc_package_maker.make_pmc_package()
                make_pkg_zip(pmc_pkg_path)
            else:
                print('='*10)
                print(_('To generate PMC package, add -pmc as parameter'))
                print('='*10)

    if not is_xml_generation and not is_db_generation:
        make_pkg_zip(scielo_pkg_path)

    utils.display_message(_('Result of the processing:'))
    utils.display_message(results_path)
    xpm_process_logger.write(report_path + '/log.txt')


class SPSXMLWorkarea(object):

    def __init__(self, filename, output_path):
        workarea.Workarea.__init__(self, filename, output_path)


class SPSXML(object):

    def __init__(self, workarea):
        self.workarea = workarea
        self.temp_package_files = self.workarea.temp_package_files
        self.workarea.scielo_package_files = PackageFiles(self.workarea.scielo_package_filename)
        self.content = SPSXMLContent(open(self.temp_package_files.filename).read())

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
        if self.xml is not None:
            a = article.Article(self.xml, self.temp_package_files.name)
            a.new_prefix = self.temp_package_files.name
            return a

    def pack(self):
        fs_utils.write_file(self.workarea.scielo_package_files.filename, self.content)
        self.workarea.copy()


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


class PackageFolder(object):

    def __init__(self, xml_list, stage='xpm'):
        self.path = os.path.dirname(xml_list[0])
        self.xml_list = xml_list
        self.output_path = os.path.dirname(self.path) + '_' + stage

    @property
    def workarea_items(self):
        items = {}
        for item in self.xml_list:
            workarea = SPSXMLWorkarea(item, self.output_path)
            items[workarea.scielo_package_files.name] = workarea
        return items

    @property
    def valid_files(self):
        items = []
        for name, workarea in self.workarea_items.items():
            items.extend(workarea.scielo_package_files.files)
        return items

    @property
    def orphans(self):
        items = []
        for f in os.listdir(self.path):
            if f not in self.valid_files:
                items.append(f)
        return items


class PMCPackageMaker(object):

    def __init__(self, article_items, workarea_items, scielo_pkg_path, pmc_pkg_path, version):

        self.article_items = article_items
        self.workarea_items = workarea_items
        self.scielo_pkg_path = scielo_pkg_path
        self.pmc_pkg_path = pmc_pkg_path

        self.pmc_dtd_files = xml_versions.DTDFiles('pmc', version)
        self.scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    def make_pmc_report(self):
        for xml_name, doc in self.article_items.items():
            msg = _('generating report... ')
            if doc.tree is None:
                msg = _('Unable to generate the XML file. ')
            else:
                if doc.journal_id_nlm_ta is None:
                    msg = _('It is not PMC article or unable to find journal-id (nlm-ta) in the XML file. ')
            html_reports.save(self.workarea_items[xml_name].outputs.pmc_style_report_filename, 'PMC Style Checker', msg)

    def make_pmc_package(self):
        do_it = False

        utils.display_message('\n')
        utils.display_message(_('Generating PMC Package'))
        n = '/' + str(len(self.article_items))
        index = 0

        for xml_name, doc in self.article_items.keys():
            workarea = self.workarea[xml_name]

            pmc_style_report_filename = workarea.outputs.pmc_style_report_filename
            pmc_xml_filename = workarea.pmc_package_files.filename
            scielo_xml_filename = workarea.scielo_package_files.filename

            if doc.journal_id_nlm_ta is None:
                html_reports.save(pmc_style_report_filename, 'PMC Style Checker', _('{label} is a mandatory data, and it was not informed. ').format(label='journal-id (nlm-ta)'))
            else:
                do_it = True

                index += 1
                item_label = str(index) + n + ': ' + xml_name
                utils.display_message(item_label)

                xml_output(scielo_xml_filename, self.scielo_dtd_files.doctype_with_local_path, self.scielo_dtd_files.xsl_output, pmc_xml_filename)

                xpchecker.style_validation(pmc_xml_filename, self.pmc_dtd_files.doctype_with_local_path, pmc_style_report_filename, self.pmc_dtd_files.xsl_prep_report, self.pmc_dtd_files.xsl_report, self.pmc_dtd_files.database_name)
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
        img = img_utils.tiff_image(img_filename)
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



###################################################






def xml_output(xml_filename, doctype, xsl_filename, result_filename):
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
