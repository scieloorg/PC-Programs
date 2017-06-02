# coding=utf-8

import os
import sys
from mimetypes import MimeTypes

from __init__ import _

from . import article
from . import xml_versions
from . import sgmlxml
from . import img_utils
from . import utils
from . import xml_utils
from . import fs_utils

from . import workarea
from . import article_validations
from . import package_validations
from . import serial_files

from . import validators
from . import spsxml

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
            pkgfiles = []
            if sgm_xml is not None:
                pkgfiles = [sgmlxml2xml(sgm_xml, acron, version)]
                stage = 'xml'
            else:
                pkgfiles = normalize_xml_packages(xml_list, stage)
            validate_packages(pkgfiles, version, DISPLAY_REPORT, GENERATE_PMC, stage, sgm_xml)


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


def sgmlxml2xml(sgm_xml_filename, acron, version):
    sgmlxml2xml = sgmlxml.SGMLXML2SPSXMLConverter(xml_versions.xsl_sgml2xml(version))
    pkgfiles = workarea.PackageFiles(sgm_xml_filename)
    wk = sgmlxml.SGMLXMLWorkarea(pkgfiles.name, pkgfiles.path)
    package_maker = sgmlxml.SGMLXML2SPSXMLPackageMaker(wk, pkgfiles)
    package_maker.pack(acron, sgmlxml2xml)
    return package_maker.xml_pkgfiles


def normalize_xml_packages(xml_list, stage='xpm'):
    pkgfiles_items = [workarea.PackageFiles(item) for item in xml_list]

    path = pkgfiles_items[0].path + '_' + stage
    if not os.path.dirname(path):
        os.makedirs(path)

    wk = workarea.Workarea(path)

    dest_path = wk.scielo_package_path
    dest_pkgfiles_items = [workarea.PackageFiles(dest_path + '/' + item.basename) for item in pkgfiles_items]

    for src, dest in zip(pkgfiles_items, dest_pkgfiles_items):
        xmlcontent = spsxml.SPSXMLContent(fs_utils.read_file(src.filename))
        xmlcontent.normalize()
        fs_utils.write_file(dest.filename, xmlcontent.content)
        src.copy(dest_path)
    return dest_pkgfiles_items


def validate_packages(pkgfiles, version, DISPLAY_REPORT, GENERATE_PMC, stage='xpm', sgm_xml=None):
    scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    wk = workarea.Workarea(os.path.dirname(pkgfiles[0].path))
    package_folder = workarea.PackageFolder(pkgfiles[0].path)

    pkgfiles = {item.name: item for item in pkgfiles}
    is_xml_generation = stage == 'xml'
    is_db_generation = stage == 'xc'

    scielo_pkg_path = wk.scielo_package_path
    pmc_pkg_path = wk.pmc_package_path
    report_path = wk.reports_path
    results_path = wk.output_path

    article_items = {item.name: article.ArticleXMLContent(fs_utils.read_file(item.filename), item.previous_name, item.name).doc for item in pkgfiles.values()}
    outputs_items = {item.name: workarea.OutputFiles(item.previous_name, wk.reports_path, item.ctrl_path) for item in pkgfiles.values()}
    is_pmc_journal = False

    for name, doc in article_items.items():
        if is_pmc_journal is False:
            if doc.journal_id_nlm_ta is not None:
                is_pmc_journal = True
        #FIXME
        article_items[name].package_files = pkgfiles[name].allfiles

    pmc_package_maker = PMCPackageMaker(version)

    doi_services = article_validations.DOI_Services()

    pkgreports = package_validations.PackageReports(package_folder, article_items, pkgfiles)
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
    articles_validations_reports = validator.validate(article_items, outputs_items, pkgfiles)

    files_final_location = serial_files.FilesFinalLocation(scielo_pkg_path, pkgissuedata.acron, pkgissuedata.issue_label, web_app_path=None)

    reports = package_validations.ReportsMaker(pkgreports, articles_data_reports, articles_validations_reports, files_final_location, xpm_version(), None)

    if not is_xml_generation:
        reports.processing_result_location = results_path
        reports.save_report(report_path, 'xpm.html', _('XML Package Maker Report'))
        if DISPLAY_REPORT:
            html_reports.display_report(report_path + '/xpm.html')

    if not is_db_generation:
        if is_xml_generation:
            pmc_package_maker.make_report(article_items, outputs_items)

        if is_pmc_journal:
            if GENERATE_PMC:
                pmc_package_maker.make_package(article_items, outputs_items)
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
