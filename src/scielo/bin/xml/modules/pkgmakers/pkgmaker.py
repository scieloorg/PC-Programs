# coding=utf-8

import os

from ..__init__ import _

from .. import utils
from .. import fs_utils
from .. import html_reports
from . import pmcxml
from ..db import workarea
from ..validations import package_validations
from ..data import package
from ..db import registered


def xpm_version():
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

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


class PackageMaker(object):

    def __init__(self, config, version, DISPLAY_REPORT, GENERATE_PMC, stage='xpm'):
        self.config = config
        self.DISPLAY_REPORT = DISPLAY_REPORT
        self.GENERATE_PMC = GENERATE_PMC
        self.stage = stage
        self.is_xml_generation = stage == 'xml'
        self.is_db_generation = stage == 'xc'
        self.db_manager = None
        self.web_app_path = None
        self.web_url = None
        self.serial_path = None
        self.version = version

    def package(self, input_xml_list):
        workarea_path = os.path.dirname(input_xml_list[0])
        if self.stage != 'xml':
            workarea_path += '_' + self.stage
        return package.Package(input_xml_list, workarea_path)

    def make_package(self, input_xml_list):
        pkg = self.package(input_xml_list)
        registered_issue_data = registered.RegisteredIssueData(self.db_manager)
        registered_issue_data.get_data(pkg.pkgissuedata)
        pkg_validations = self.validate_package(pkg, registered_issue_data)

        conversion = None
        self.report(pkg, pkg_validations, conversion)
        self.make_pmc_package(pkg, registered_issue_data)
        self.zip(pkg)
        utils.display_message(_('Result of the processing:'))
        utils.display_message(pkg.wk.output_path)
        #xpm_process_logger.write(pkg.wk.reports_path + '/log.txt')

    def validate_package(self, pkg, registered_issue_data):
        validator = package_validations.ArticlesValidator(
            self.version,
            registered_issue_data,
            pkg.pkgissuedata,
            self.is_xml_generation)
        return validator.validate(pkg.articles, pkg.outputs, pkg.package_folder.pkgfiles_items)

    def report(self, pkg, pkg_validations, conversion=None):
        files_final_location = workarea.FilesFinalLocation(
            pkg_path=pkg.wk.scielo_package_path,
            acron=pkg.pkgissuedata.acron,
            issue_label=pkg.pkgissuedata.issue_label,
            serial_path=self.serial_path,
            web_app_path=self.web_app_path,
            web_url=self.web_url)
        pkgreports = package_validations.PackageReports(pkg.package_folder)
        articles_data_reports = package_validations.ArticlesDataReports(pkg.articles)
        reports = package_validations.ReportsMaker(pkgreports, articles_data_reports, pkg_validations, files_final_location, xpm_version(), conversion)

        if not self.is_xml_generation:
            reports.processing_result_location = pkg.wk.output_path
            reports.save_report(pkg.wk.reports_path, 'xpm.html', _('XML Package Maker Report'))
            if self.DISPLAY_REPORT:
                html_reports.display_report(pkg.wk.reports_path + '/xpm.html')

    def make_pmc_package(self, pkg):
        if not self.is_db_generation:
            # FIXME
            pmc_package_maker = pmcxml.PMCPackageMaker(self.version)
            if self.is_xml_generation:
                pmc_package_maker.make_report(pkg.articles, pkg.outputs)
            if pkg.is_pmc_journal:
                if self.GENERATE_PMC:
                    pmc_package_maker.make_package(pkg.articles, pkg.outputs)
                    workarea.PackageFolder(pkg.wk.pmc_package_path).zip()
                else:
                    print('='*10)
                    print(_('To generate PMC package, add -pmc as parameter'))
                    print('='*10)

    def zip(self, pkg):
        if not self.is_xml_generation and not self.is_db_generation:
            workarea.PackageFolder(pkg.wk.scielo_package_path).zip()
