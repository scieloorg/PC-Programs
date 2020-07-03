# coding=utf-8
import logging
import os
import shutil

from prodtools import _
from prodtools import XPM_VERSION_FILE_PATH
from prodtools.utils import encoding
from prodtools.utils import fs_utils
from prodtools.utils.exporter import Exporter
from prodtools.reports import html_reports
from prodtools.reports import validation_status
from prodtools.validations import article_data_reports
from prodtools.validations import validations as validations_module
from prodtools.validations import reports_maker
from prodtools.validations.pkg_evaluation import (
    PackageEvaluator,
)
from prodtools.data import kernel_document
from prodtools.db import xc_models
from prodtools.db.serial import WebsiteFiles
from prodtools.db.pid_versions import(
    PIDVersionsManager,
    PIDVersionsDB,
)
from prodtools.processing import pmc_pkgmaker
from prodtools.db.pid_versions import PIDVersionsManager


logger = logging.getLogger()


EMAIL_SUBJECT_STATUS_ICON = {}
EMAIL_SUBJECT_STATUS_ICON['rejected'] = [u"\u274C", _(' REJECTED ')]
EMAIL_SUBJECT_STATUS_ICON['ignored'] = [u"\u274C", _('IGNORED')]
EMAIL_SUBJECT_STATUS_ICON['accepted'] = [u"\u2713" + ' ' + u"\u270D", _(' ACCEPTED but corrections required ')]
EMAIL_SUBJECT_STATUS_ICON['approved'] = [u"\u2705", _(' APPROVED ')]
EMAIL_SUBJECT_STATUS_ICON['not processed'] = ['', _(' NOT PROCESSED ')]


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
    version = '|'
    for f in [XPM_VERSION_FILE_PATH]:
        encoding.debugging('xpm_version', f)
        if os.path.isfile(f):
            version = fs_utils.read_file_lines(f)[0]
            break
    if '|' not in version:
        version += '|'
    encoding.debugging('version', version)
    major_version, minor_version = version.split('|')
    return major_version, minor_version


class ArticlesConversion(object):

    def __init__(self, registered_issue_data, pkg, pkg_eval_result, create_windows_base, web_app_path, web_app_site):
        self.create_windows_base = create_windows_base
        self.registered_issue_data = registered_issue_data
        self.db = self.registered_issue_data.articles_db_manager
        self.local_web_app_path = web_app_path
        self.web_app_site = web_app_site
        self.pkg = pkg
        self.pkg_eval_result = pkg_eval_result
        self.error_messages = []
        self.conversion_status = {}

    def convert(self):
        self.articles_conversion_validations = validations_module.ValidationsResultItems()
        scilista_items = [self.pkg.issue_data.acron_issue_label]
        if self.pkg_eval_result.blocking_errors == 0 and (self.accepted_articles == len(self.pkg.articles) or len(self.pkg_eval_result.excluded_orders) > 0):
            self.error_messages = self.db.exclude_articles(self.pkg_eval_result.excluded_orders)

            _scilista_items = self.db.convert_articles(self.pkg.issue_data.acron_issue_label, self.pkg_eval_result.accepted_articles, self.registered_issue_data.issue_models.record, self.create_windows_base)
            scilista_items.extend(_scilista_items)
            self.conversion_status.update(self.db.db_conversion_status)

            for name, message in self.db.articles_conversion_messages.items():
                self.articles_conversion_validations[name] = validations_module.ValidationsResult()
                self.articles_conversion_validations[name].message = message

            if len(_scilista_items) > 0:
                # IMPROVEME
                if self.local_web_app_path:
                    website_files = WebsiteFiles(
                        self.local_web_app_path,
                        self.pkg.issue_data.acron,
                        self.pkg.issue_data.issue_label)
                    website_files.get_files(self.pkg.package_folder.path)
                self.registered_issue_data.issue_files.save_source_files(self.pkg.package_folder.path)
                self.replace_ex_aop_pdf_files()

        return scilista_items

    def register_pids_and_update_xmls(self, pid_manager: PIDVersionsManager) -> None:
        """Invoca o registro de PIDs em um banco de dados e logo após registra
        os PIDs nos documentos XMLs presentes no pacote."""
        issue_models = self.registered_issue_data.issue_models

        if not issue_models:
            return

        kernel_document.add_article_id_to_received_documents(
            pid_manager=pid_manager,
            issn_id=issue_models.issue.issn_id,
            year_and_order=issue_models.record.get("36"),
            received_docs=self.pkg.articles,
            documents_in_isis=self.registered_issue_data.registered_articles,
            file_paths=self.pkg.file_paths,
            update_article_with_aop_status=self.db.get_valid_aop,
        )
        logger.debug("Articles that compose this package were updated with SciELO Pids (v2, and v3)")

    def export_package_to_spf_directory(self, exporter: callable, package_name: str):
        """Exporta o pacote SPS de acordo com a estratégia utilizada"""
        if exporter is None:
            logger.debug(
                "Could not export this package because the none exporter was used."
            )
            return None
        elif package_name is None or len(package_name) == 0:
            logger.debug(
                "Could not export this package because the name of package is blank."
            )
            return None

        package_zip_name = "{}.zip".format(package_name.replace(" ", "_"))
        exporter(self.pkg.package_folder.path, package_zip_name)

    @property
    def aop_status(self):
        if self.db is not None:
            return self.db.db_aop_status
        return {}

    def replace_ex_aop_pdf_files(self):
        # IMPROVEME
        """
        substitui o pdf do aop pelo conteúdo do pdf do issue, mantendo o
        nome do arquivo aop
        """
        encoding.debugging(
            'replace_ex_aop_pdf_files()', self.db.aop_pdf_replacements)

        bases_dir = os.path.join(self.local_web_app_path, "bases")
        pdf_dir = os.path.join(bases_dir, "pdf")
        acron, issue = self.pkg.issue_data.acron_issue_label.split(" ")
        issue_pdf_path = os.path.join(pdf_dir, acron, issue)

        for xml_name, aop_location_data in self.db.aop_pdf_replacements.items():
            folder, aop_name = aop_location_data

            aop_pdf_path = os.path.join(pdf_dir, folder)
            if not os.path.isdir(aop_pdf_path):
                os.makedirs(aop_pdf_path)

            issue_pdf_files = [f
                               for f in os.listdir(issue_pdf_path)
                               if (
                                f.startswith(xml_name) or
                                f[2:].startswith('_'+xml_name))]

            for pdf in issue_pdf_files:
                aop_pdf = pdf.replace(xml_name, aop_name)
                src = os.path.join(issue_pdf_path, pdf)
                dest = os.path.join(aop_pdf_path, aop_pdf)
                shutil.copyfile(src, dest)

    @property
    def conversion_report(self):
        #resulting_orders
        labels = [_('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('article')]
        widths = {_('article'): '20', _('registered') + '/' + _('before conversion'): '20', _('package'): '20', _('executed actions'): '20'}

        for status, status_items in self.aop_status.items():
            for status_data in status_items:
                if status != 'aop':
                    name = status_data
                    self.pkg_eval_result.history_items[name].append(status)
        for status, names in self.conversion_status.items():
            for name in names:
                self.pkg_eval_result.history_items[name].append(status)

        items = []
        db_articles = self.registered_articles or {}
        for xml_name in sorted(self.pkg_eval_result.history_items.keys()):
            pkg = self.pkg.articles.get(xml_name)
            registered = self.pkg_eval_result.registered_articles.get(xml_name)
            merged = db_articles.get(xml_name)

            diff = ''
            if registered is not None and pkg is not None:
                comparison = article_data_reports.ArticlesComparison(registered, pkg)
                diff = comparison.display_articles_differences()
                if diff != '':
                    diff += '<hr/>'

            values = []
            values.append(article_data_reports.display_article_data_to_compare(registered) if registered is not None else '')
            values.append(article_data_reports.display_article_data_to_compare(pkg) if pkg is not None else '')
            values.append(article_data_reports.article_history(self.pkg_eval_result.history_items[xml_name]))
            values.append(diff + article_data_reports.display_article_data_to_compare(merged) if merged is not None else '')

            items.append(html_reports.label_values(labels, values))
        return html_reports.tag('h3', _('Conversion steps')) + html_reports.sheet(labels, items, html_cell_content=[_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions')], widths=widths)

    @property
    def registered_articles(self):
        if self.db is not None:
            return self.db.registered_articles

    @property
    def acron_issue_label(self):
        return self.pkg.issue_data.acron_issue_label

    @property
    def accepted_articles(self):
        return len(self.pkg_eval_result.accepted_articles)

    @property
    def total_converted(self):
        return len(self.conversion_status.get('converted', []))

    @property
    def total_not_converted(self):
        return len(self.conversion_status.get('not converted', []))

    @property
    def xc_status(self):
        if self.pkg_eval_result.blocking_errors > 0:
            result = 'rejected'
        elif self.articles_conversion_validations.blocking_errors > 0:
            result = 'rejected'
        elif self.accepted_articles == 0 and len(self.pkg_eval_result.excluded_orders) == 0:
            result = 'ignored'
        elif self.articles_conversion_validations.fatal_errors > 0:
            result = 'accepted'
        else:
            result = 'approved'
        return result

    @property
    def conversion_status_report(self):
        title = _('Conversion results')
        status = self.conversion_status
        style = 'conversion'
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
                    article = self.pkg_eval_result.merged_articles.get(name)
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
            if self.accepted_articles > 0:
                if self.total_not_converted > 0:
                    reason = _('because it is not complete ({value} were not converted). ').format(value=str(self.total_not_converted) + '/' + str(self.accepted_articles))
                else:
                    reason = _('because there are blocking errors in the package. ')
            else:
                reason = _('because there are blocking errors in the package. ')
        elif self.xc_status == 'ignored':
            update = False
            reason = _('because there is no document allowed to convert. ')
            status = validation_status.STATUS_BLOCKING_ERROR
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
        text = html_reports.p_message(_('converted') + ': ' + str(self.total_converted) + '/' + str(self.accepted_articles), False) + html_reports.p_message(text, False)
        return text


class PkgProcessor(object):

    def __init__(self, config, INTERATIVE, stage='xpm'):
        self.config = config
        self.INTERATIVE = INTERATIVE
        self.stage = stage
        self.is_xml_generation = stage == 'xml'
        self.is_db_generation = stage == 'xc'
        self.xpm_version = xpm_version() if stage == 'xpm' else None
        self.registered_issues_manager = xc_models.RegisteredIssuesManager(
            self.config, self.is_db_generation)
        self._pid_manager = None


    @property
    def export_documents_package(self):
        if self.config.kernel_gate:
            return Exporter(self.config.kernel_gate).export

    def evaluate_package(self, pkg):
        logger.info("Analize package")
        registered_issue_data = self.registered_issues_manager.get_registered_issue_data(pkg.issue_data)

        if len(registered_issue_data.registered_articles) > 0:
            logging.info(_('Previously registered: ({n} files)').format(
                n=len(registered_issue_data.registered_articles)))

        evaluator = PackageEvaluator(
            pkg, registered_issue_data, self.is_db_generation,
            self.is_xml_generation, self.config
        )
        pkg_eval_result = evaluator.evaluate()
        return registered_issue_data, pkg_eval_result

    def make_package(self, pkg, GENERATE_PMC=False):
        registered_issue_data, pkg_eval_result = self.evaluate_package(pkg)
        self.report_result(pkg, pkg_eval_result, conversion=None)
        self.make_pmc_package(pkg, GENERATE_PMC)
        if not self.is_xml_generation:
            pkg.zip()

    def convert_package(self, pkg):
        registered_issue_data, pkg_eval_result = self.evaluate_package(pkg)

        conversion = ArticlesConversion(registered_issue_data, pkg, pkg_eval_result, not self.config.interative_mode, self.config.local_web_app_path, self.config.web_app_site)

        if self.config.pid_manager_info:
            with PIDVersionsDB(self.config.pid_manager_info) as db:
                conversion.register_pids_and_update_xmls(PIDVersionsManager(db))

        scilista_items = conversion.convert()

        # A scilista sempre terá um item mas o pacote só será
        # exportado se a scilista tiver mais de um item, isso
        # indica que o pacote está válido
        if scilista_items is not None and len(scilista_items) > 1:
            conversion.export_package_to_spf_directory(
                self.export_documents_package, package_name=scilista_items[0]
            )

        reports = self.report_result(pkg, pkg_eval_result, conversion)
        statistics_display = reports.validations.statistics_display(html_format=False)

        subject = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(conversion.xc_status, [])) + ' ' + statistics_display
        mail_content = '<html><body>' + html_reports.link(reports.report_link, reports.report_link) + '</body></html>'
        mail_info = subject, mail_content
        return (scilista_items, conversion.xc_status, mail_info)

    def report_result(self, pkg, pkg_eval_result, conversion=None):
        logger.info("Generate reports")
        files_location = reports_maker.AssetsInReport(
            pkg.wk.scielo_package_path)
        if conversion is not None:
            files_location = reports_maker.AssetsInReport(
                pkg.wk.scielo_package_path,
                pkg.issue_data.acron,
                pkg.issue_data.issue_label,
                self.config.serial_path,
                self.config.local_web_app_path,
                self.config.web_app_site)
        reports = reports_maker.ReportsMaker(
            pkg, pkg_eval_result, files_location, self.stage,
            self.xpm_version, conversion)
        if not self.is_xml_generation:
            reports.save_report(self.INTERATIVE)
        if conversion is not None:
            if conversion.registered_issue_data.issue_files is not None:
                conversion.registered_issue_data.issue_files.save_reports(
                    files_location.report_path)
        if self.config.web_app_site is not None:
            for article_files in pkg.package_folder.pkgfiles_items.values():
                # copia os xml para report path
                article_files.copy_xml(reports.files_location.report_path)
        return reports

    def make_pmc_package(self, pkg, GENERATE_PMC):
        if GENERATE_PMC:
            logger.info("Make PMC Package")
            pmc_package_maker = pmc_pkgmaker.PMCPackageMaker(pkg)
            pmc_package_maker.make_package()
        else:
            logger.info(
                _('To generate PMC package, add -pmc as parameter'))
