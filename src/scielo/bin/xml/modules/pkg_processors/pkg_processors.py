# coding=utf-8

import os
import shutil

from ..__init__ import _

from ..useful import utils
from ..useful import fs_utils
from ..reports import html_reports
from ..validations import validation_status
from ..validations import article_reports
from ..validations import package_validations
from ..data import package
from ..data import workarea
from ..db import registered
from . import pmc_pkgmaker


categories_messages = {
    'converted': _('converted'),
    'rejected': _('rejected'),
    'not converted': _('not converted'),
    'skipped': _('skipped conversion'),
    'excluded ex-aop': _('excluded ex-aop'),
    'excluded incorrect order': _('excluded incorrect order'),
    'not excluded incorrect order': _('not excluded incorrect order'),
    'not excluded ex-aop': _('not excluded ex-aop'),
    'new aop': _('aop version'),
    'regular doc': _('doc has no aop'),
    'ex aop': _('aop is published in an issue'),
    'matched aop': _('doc has aop version'),
    'partially matched aop': _('doc has aop version partially matched (title/author are similar)'), 
    'aop missing PID': _('doc has aop version which has no PID'),
    'unmatched aop': _('doc has an invalid aop version (title/author are not the same)'), 
}


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
            version = fs_utils.read_file_lines(f)[0]
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


class ArticlesConverter(object):

    def __init__(self, registered_issue_data, pkg, create_windows_base, web_app_path, web_app_site):
        self.create_windows_base = create_windows_base
        self.registered_issue_data = registered_issue_data
        self.db = self.registered_issue_data.articles_db_manager
        self.local_web_app_path = web_app_path
        self.pkg = pkg
        self.merging_result = self.articles_validations_reports.merged_articles_reports.merging_result
        self.merged_articles = self.articles_validations_reports.merged_articles_reports.merged_articles_data.merged_articles

    def convert(self):
        self.articles_conversion_validations = {}
        scilista_items = [self.pkg.pkgissuedata.acron_issue_label]
        if self.articles_validations_reports.blocking_errors == 0 and self.total_to_convert > 0:
            self.conversion_status = {}
            self.error_messages = self.db.exclude_articles(self.merging_result.order_changes, self.merging_result.excluded_orders)

            _scilista_items = self.db.convert_articles(self.pkg.pkgissuedata.acron_issue_label, self.merging_result.articles_to_convert, self.registered_issue_data.issue_models.record, self.create_windows_base)
            scilista_items.extend(_scilista_items)
            self.conversion_status.update(self.db.db_conversion_status)

            for name, message in self.db.articles_conversion_messages.items():
                self.articles_conversion_validations[name] = package_validations.ValidationsResult()
                self.articles_conversion_validations[name].message = message

            if len(_scilista_items) > 0:
                self.db.issue_files.copy_files_to_local_web_app(self.pkg.package_folder.path, self.local_web_app_path)
                self.db.issue_files.save_source_files(self.pkg.package_folder.path)
                self.replace_ex_aop_pdf_files()

            self.aop_status.update(self.db.db_aop_status)
        return scilista_items

    def replace_ex_aop_pdf_files(self):
        # FIXME
        print(self.db.aop_pdf_replacements)
        for xml_name, aop_location_data in self.db.aop_pdf_replacements.items():
            folder, aop_name = aop_location_data

            aop_pdf_path = self.local_web_app_path + '/bases/pdf/' + folder
            if not os.path.isdir(aop_pdf_path):
                os.makedirs(aop_pdf_path)
            issue_pdf_path = self.local_web_app_path + '/bases/pdf/' + self.pkg.pkgissuedata.acron_issue_label.replace(' ', '/')

            issue_pdf_files = [f for f in os.listdir(issue_pdf_path) if f.startswith(xml_name) or f[2:].startswith('_'+xml_name)]

            for pdf in issue_pdf_files:
                aop_pdf = pdf.replace(xml_name, aop_name)
                print((issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf))
                shutil.copyfile(issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf)

    @property
    def conversion_report(self):
        #resulting_orders
        labels = [_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('achieved results')]
        widths = {_('article'): '20', _('registered') + '/' + _('before conversion'): '20', _('package'): '20', _('executed actions'): '20',  _('achieved results'): '20'}

        #print(self.merging_result.history_items)
        for status, status_items in self.aop_status.items():
            for status_data in status_items:
                if status != 'aop':
                    name = status_data
                    article = self.merging_result.articles_to_convert[name]
                    self.merging_result.history_items[name].append((status, article))
        for status, names in self.conversion_status.items():
            for name in names:
                self.merging_result.history_items[name].append((status, self.merging_result.articles_to_convert[name]))

        history = sorted([(hist[0][1].order, xml_name) for xml_name, hist in self.merging_result.history_items.items()])
        history = [(xml_name, self.merging_result.history_items[xml_name]) for order, xml_name in history]

        items = []
        for xml_name, hist in history:
            values = []

            registered = [item for item in hist if item[0] == 'registered article']
            package = [item for item in hist if item[0] == 'package']
            diff = ''
            if len(registered) == 1 and len(package) == 1:
                comparison = package_validations.ArticlesComparison(registered[0][1], package[0][1])
                diff = comparison.display_articles_differences() + '<hr/>'
            values.append(article_reports.display_article_data_in_toc(hist[-1][1]))
            values.append(article_reports.article_history(registered))
            values.append(diff + article_reports.article_history(package))
            values.append(article_reports.article_history([item for item in hist if not item[0] in ['registered article', 'package', 'rejected', 'converted', 'not converted']]))
            values.append(article_reports.article_history([item for item in hist if item[0] in ['rejected', 'converted', 'not converted']]))

            items.append(html_reports.label_values(labels, values))
        return html_reports.tag('h3', _('Conversion steps')) + html_reports.sheet(labels, items, html_cell_content=[_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('achieved results')], widths=widths)

    @property
    def registered_articles(self):
        if self.db is not None:
            return self.db.registered_articles

    @property
    def acron_issue_label(self):
        return self.pkg.pkgissuedata.acron_issue_label

    @property
    def total_to_convert(self):
        return self.merging_result.total_to_convert

    @property
    def total_converted(self):
        return len(self.conversion_status.get('converted', []))

    @property
    def total_not_converted(self):
        return len(self.conversion_status.get('not converted', []))

    @property
    def xc_status(self):
        if self.articles_validations_reports.blocking_errors > 0:
            result = 'rejected'
        elif self.total_to_convert == 0:
            result = 'ignored'
        elif self.articles_conversion_validations.blocking_errors > 0:
            result = 'rejected'
        elif self.articles_conversion_validations.fatal_errors > 0:
            result = 'accepted'
        else:
            result = 'approved'
        return result

    @property
    def conversion_status_report(self):
        return report_status(_('Conversion results'), self.conversion_status, 'conversion')

    @property
    def aop_status_report(self):
        if len(self.aop_status) == 0:
            return _('this journal has no aop. ')
        r = ''
        for status in sorted(self.aop_status.keys()):
            if status != 'aop':
                r += self.aop_report(status, self.aop_status[status])
        r += self.aop_report('aop', self.aop_status.get('aop'))
        return r

    def aop_report(self, status, status_items):
        if status_items is None:
            return ''
        r = ''
        if len(status_items) > 0:
            labels = []
            widths = {}
            if status == 'aop':
                labels = [_('issue')]
                widths = {_('issue'): '5'}
            labels.extend([_('filename'), 'order', _('article')])
            widths.update({_('filename'): '5', 'order': '2', _('article'): '88'})

            report_items = []
            for item in status_items:
                issueid = None
                article = None
                if status == 'aop':
                    issueid, name, article = item
                else:
                    name = item
                    article = self.articles_merger.merged_articles.get(name)
                if article is not None:
                    if not article.is_ex_aop:
                        values = []
                        if issueid is not None:
                            values.append(issueid)
                        values.append(name)
                        values.append(article.order)
                        values.append(article.title)
                        report_items.append(html_reports.label_values(labels, values))
            r = html_reports.tag('h3', _(status)) + html_reports.sheet(labels, report_items, table_style='reports-sheet', html_cell_content=[_('article')], widths=widths)
        return r

    @property
    def conclusion_message(self):
        text = ''.join(self.error_messages)
        app_site = self.web_app_site if self.web_app_site is not None else _('scielo web site')
        status = ''
        result = _('updated/published on {app_site}').format(app_site=app_site)
        reason = ''
        update = True
        if self.xc_status == 'rejected':
            update = False
            status = validation_status.STATUS_BLOCKING_ERROR
            if self.total_to_convert > 0:
                if self.total_not_converted > 0:
                    reason = _('because it is not complete ({value} were not converted). ').format(value=str(self.total_not_converted) + '/' + str(self.total_to_convert))
                else:
                    reason = _('because there are blocking errors in the package. ')
            else:
                reason = _('because there are blocking errors in the package. ')
        elif self.xc_status == 'ignored':
            update = False
            reason = _('because no document has changed. ')
        elif self.xc_status == 'accepted':
            status = validation_status.STATUS_WARNING
            reason = _(' even though there are some fatal errors. Note: These errors must be fixed in order to have good quality of bibliometric indicators and services. ')
        elif self.xc_status == 'approved':
            status = validation_status.STATUS_OK
            reason = ''
        else:
            status = validation_status.STATUS_FATAL_ERROR
            reason = _('because there are blocking errors in the package. ')
        action = _('will not be')
        if update:
            action = _('will be')
        text = u'{status}: {issueid} {action} {result} {reason}'.format(status=status, issueid=self.acron_issue_label, result=result, reason=reason, action=action)
        text = html_reports.p_message(_('converted') + ': ' + str(self.total_converted) + '/' + str(self.total_to_convert), False) + html_reports.p_message(text, False)
        return text


class PkgProcessor(object):

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
        self.report_result(pkg, pkg_validations, conversion=None)
        self.make_pmc_package(pkg, registered_issue_data)
        self.zip(pkg)

    def convert_package(self, input_xml_list):
        pkg = self.package(input_xml_list)
        registered_issue_data = registered.RegisteredIssueData(self.db_manager)
        registered_issue_data.get_data(pkg.pkgissuedata)
        pkg_validations = self.validate_package(pkg, registered_issue_data)
        conversion = ArticlesConverter(registered_issue_data, pkg, not self.config.interative_mode, not self.config.local_web_app_path, not self.config.web_app_site)
        scilista_items = conversion.convert()

        reports = self.report_result(pkg, pkg_validations, conversion)
        utils.display_message(_('Result of the processing:'))
        utils.display_message(reports.files_final_location.result_path)
        statistics_display = reports.validations.statistics_display(html_format=False)

        return (scilista_items, conversion.xc_status, statistics_display, reports.report_location)

    def validate_package(self, pkg, registered_issue_data):
        validator = package_validations.ArticlesValidator(
            self.version,
            registered_issue_data,
            pkg.pkgissuedata,
            self.is_xml_generation)
        return validator.validate(pkg.articles, pkg.outputs, pkg.package_folder.pkgfiles_items)

    def report_result(self, pkg, pkg_validations, conversion=None):
        serial_path = None if conversion is None else conversion.registered_issue_data.articles_db_manager.serial_path

        files_final_location = workarea.FilesFinalLocation(pkg.wk.scielo_package_path, pkg.pkgissuedata.acron, pkg.pkgissuedata.issue_label, self.config.web_app_path, self.config.web_app_site)
        pkgreports = package_validations.PackageReports(pkg.package_folder)
        articles_data_reports = package_validations.ArticlesDataReports(pkg.articles)

        reports = package_validations.ReportsMaker(pkgreports, articles_data_reports, pkg_validations, files_final_location, xpm_version(), conversion)
        if not self.is_xml_generation:
            reports.save_report(self.DISPLAY_REPORT or self.config.interative_mode)
        return reports

    def make_pmc_package(self, pkg):
        if not self.is_db_generation:
            # FIXME
            pmc_package_maker = pmc_pkgmaker.PMCPackageMaker(self.version)
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


def report_status(title, status, style=None):
    text = ''
    if status is not None:
        for category in sorted(status.keys()):
            _style = style
            if status.get(category) is None:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            elif len(status[category]) == 0:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            else:
                ltype = 'ol'
                list_items = status[category]
            text += html_reports.format_list(categories_messages.get(category, category), ltype, list_items, _style)
    if len(text) > 0:
        text = html_reports.tag('h3', title) + text
    return text
