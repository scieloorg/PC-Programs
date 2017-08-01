# coding=utf-8

import os
import sys

from .__init__ import _

from . import utils
from . import fs_utils
from . import html_reports
from . import article
from pkgmakers import sgmlxml
from pkgmakers import spsxml
from pkgmakers import pmcxml
from data import workarea
from validations import package_validations


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
    sgmlxml2xml = sgmlxml.SGMLXML2SPSXMLConverter(version)
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

    pmc_package_maker = pmcxml.PMCPackageMaker(version)

    pkgreports = package_validations.PackageReports(package_folder, article_items, pkgfiles)
    pkgissuedata = package_validations.PackageIssueData(article_items)
    registered_issue_data = package_validations.RegisteredIssueData(db_manager=None)
    registered_issue_data.get_data(pkgissuedata)

    validator = package_validations.ArticlesValidator(
        version,
        registered_issue_data,
        pkgissuedata,
        is_xml_generation)

    articles_data_reports = package_validations.ArticlesDataReports(article_items)
    articles_validations_reports = validator.validate(article_items, outputs_items, pkgfiles)

    files_final_location = workarea.FilesFinalLocation(scielo_pkg_path, pkgissuedata.acron, pkgissuedata.issue_label, web_app_path=None)

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


