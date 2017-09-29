# coding=utf-8

import os
import shutil

from ...__init__ import _
from ...__init__ import BIN_PATH
from ...__init__ import FST_PATH

from ...generics.dbm import dbm_isis
from ...generics import encoding
from ...generics import fs_utils
from ...generics import doi_validations
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from ..ws import institutions_manager
from ..ws import ws_journals
from ..validations import article_data_reports
from ..validations import pkg_articles_validations
from ..validations import article_validations as article_validations_module
from ..validations import validations as validations_module
from ..validations import reports_maker
from ..validations import merged_articles_validations
from ..data import package
from ..data import merged
from ..data import workarea
from ..data import aff_normalization
from ..db import registered
from ..db import xc_models
from . import pmc_pkgmaker
from . import sps_pkgmaker


EMAIL_SUBJECT_STATUS_ICON = {}
EMAIL_SUBJECT_STATUS_ICON['rejected'] = [u"\u274C", _(' REJECTED ')]
EMAIL_SUBJECT_STATUS_ICON['ignored'] = ['', _('IGNORED')]
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
    version_files = [
        BIN_PATH + '/xpm_version.txt',
        BIN_PATH + '/cfg/xpm_version.txt',
    ]
    version = '|'
    for f in version_files:
        encoding.debugging('xpm_version', f)
        if os.path.isfile(f):
            version = fs_utils.read_file_lines(f)[0]
            break
    if '|' not in version:
        version += '|'
    encoding.debugging('version', version)
    major_version, minor_version = version.split('|')
    return major_version, minor_version


def normalize_xml_packages(xml_list, dtd_location_type, stage):
    article_files_items = [workarea.PkgArticleFiles(item) for item in xml_list]

    path = article_files_items[0].path + '_' + stage

    if not os.path.isdir(path):
        os.makedirs(path)

    wk = workarea.Workarea(path)
    outputs = {}
    dest_path = wk.scielo_package_path
    dest_article_files_items = [workarea.PkgArticleFiles(dest_path + '/' + item.basename) for item in article_files_items]
    for src, dest in zip(article_files_items, dest_article_files_items):
        src.convert_images()
        xmlcontent = sps_pkgmaker.SPSXMLContent(fs_utils.read_file(src.filename))
        xmlcontent.normalize()
        xmlcontent.doctype(dtd_location_type)
        fs_utils.write_file(dest.filename, xmlcontent.content)
        src.copy_files_except_xml(dest_path)

        outputs[dest.name] = workarea.OutputFiles(dest.name, wk.reports_path, None)

    return dest_article_files_items, outputs


class ArticlesConversion(object):

    def __init__(self, registered_issue_data, pkg, validations_reports, create_windows_base, web_app_path, web_app_site):
        self.create_windows_base = create_windows_base
        self.registered_issue_data = registered_issue_data
        self.db = self.registered_issue_data.articles_db_manager
        self.local_web_app_path = web_app_path
        self.web_app_site = web_app_site
        self.pkg = pkg
        self.validations_reports = validations_reports
        self.articles_mergence = validations_reports.merged_articles_reports.articles_mergence
        self.error_messages = []
        self.conversion_status = {}

    def convert(self):
        self.articles_conversion_validations = validations_module.ValidationsResultItems()
        scilista_items = [self.pkg.issue_data.acron_issue_label]
        if self.validations_reports.blocking_errors == 0 and self.accepted_articles == len(self.pkg.articles):
            self.error_messages = self.db.exclude_articles(self.articles_mergence.excluded_orders)

            _scilista_items = self.db.convert_articles(self.pkg.issue_data.acron_issue_label, self.articles_mergence.accepted_articles, self.registered_issue_data.issue_models.record, self.create_windows_base)
            scilista_items.extend(_scilista_items)
            self.conversion_status.update(self.db.db_conversion_status)

            for name, message in self.db.articles_conversion_messages.items():
                self.articles_conversion_validations[name] = validations_module.ValidationsResult()
                self.articles_conversion_validations[name].message = message

            if len(_scilista_items) > 0:
                # IMPROVEME
                self.registered_issue_data.issue_files.copy_files_to_local_web_app(self.pkg.package_folder.path, self.local_web_app_path)
                self.registered_issue_data.issue_files.save_source_files(self.pkg.package_folder.path)
                self.replace_ex_aop_pdf_files()

        return scilista_items

    @property
    def aop_status(self):
        if self.db is not None:
            return self.db.db_aop_status
        return {}

    def replace_ex_aop_pdf_files(self):
        # IMPROVEME
        encoding.debugging('replace_ex_aop_pdf_files()', self.db.aop_pdf_replacements)
        for xml_name, aop_location_data in self.db.aop_pdf_replacements.items():
            folder, aop_name = aop_location_data

            aop_pdf_path = self.local_web_app_path + '/bases/pdf/' + folder
            if not os.path.isdir(aop_pdf_path):
                os.makedirs(aop_pdf_path)
            issue_pdf_path = self.local_web_app_path + '/bases/pdf/' + self.pkg.issue_data.acron_issue_label.replace(' ', '/')

            issue_pdf_files = [f for f in os.listdir(issue_pdf_path) if f.startswith(xml_name) or f[2:].startswith('_'+xml_name)]

            for pdf in issue_pdf_files:
                aop_pdf = pdf.replace(xml_name, aop_name)
                encoding.debugging('replace_ex_aop_pdf_files()', (issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf))
                shutil.copyfile(issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf)

    @property
    def conversion_report(self):
        #resulting_orders
        labels = [_('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('article')]
        widths = {_('article'): '20', _('registered') + '/' + _('before conversion'): '20', _('package'): '20', _('executed actions'): '20'}

        for status, status_items in self.aop_status.items():
            for status_data in status_items:
                if status != 'aop':
                    name = status_data
                    self.articles_mergence.history_items[name].append(status)
        for status, names in self.conversion_status.items():
            for name in names:
                self.articles_mergence.history_items[name].append(status)

        items = []
        db_articles = self.registered_articles or {}
        for xml_name in sorted(self.articles_mergence.history_items.keys()):
            pkg = self.articles_mergence.articles.get(xml_name)
            registered = self.articles_mergence.registered_articles.get(xml_name)
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
            values.append(article_data_reports.article_history(self.articles_mergence.history_items[xml_name]))
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
        return len(self.articles_mergence.accepted_articles)

    @property
    def total_converted(self):
        return len(self.conversion_status.get('converted', []))

    @property
    def total_not_converted(self):
        return len(self.conversion_status.get('not converted', []))

    @property
    def xc_status(self):
        if self.validations_reports.blocking_errors > 0:
            result = 'rejected'
        elif self.accepted_articles == 0:
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
                    article = self.articles_mergence.merged_articles.get(name)
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
        self._db_manager = None
        self.ws_journals = ws_journals.Journals(self.config.app_ws_requester)
        self.ws_journals.update_journals_file()
        self.journals_list = xc_models.JournalsList(self.ws_journals.downloaded_journals_filename)
        self.app_institutions_manager = institutions_manager.InstitutionsManager(self.config.app_ws_requester)
        self.aff_normalizer = aff_normalization.Aff(self.app_institutions_manager)
        self.doi_validator = doi_validations.DOIValidator(self.config.app_ws_requester)
        self.registered_issues_manager = xc_models.RegisteredIssuesManager(self.db_manager, self.journals_list)

    @property
    def db_manager(self):
        if self._db_manager is None and self.is_db_generation:
            cisis1030 = dbm_isis.CISIS(self.config.cisis1030)
            if cisis1030.cisis_path is not None:
                cisis1660 = dbm_isis.CISIS(self.config.cisis1660)
                ucisis = dbm_isis.UCISIS(cisis1030, cisis1660)
                db_isis = dbm_isis.IsisDAO(ucisis)
                titles = [self.config.title_db, self.config.title_db_copy, FST_PATH + '/title.fst']
                issues = [self.config.issue_db, self.config.issue_db_copy, FST_PATH + '/issue.fst']
                self._db_manager = xc_models.DBManager(
                    db_isis,
                    titles,
                    issues,
                    self.config.serial_path)
        return self._db_manager

    def normalized_package(self, xml_list):
        dtd_location_type = 'remote'
        if self.is_db_generation:
            dtd_location_type = 'local'
        pkgfiles, outputs = normalize_xml_packages(xml_list, dtd_location_type, self.stage)
        workarea_path = os.path.dirname(pkgfiles[0].path)
        return package.Package(pkgfiles, outputs, workarea_path)

    def evaluate_package(self, pkg):
        registered_issue_data = registered.RegisteredIssue()
        self.registered_issues_manager.get_registered_issue_data(pkg.issue_data, registered_issue_data)
        for xml_name in sorted(pkg.articles.keys()):
            a = pkg.articles[xml_name]
            if a is not None:
                institutions_results = {}
                for aff_xml in a.affiliations:
                    if aff_xml is not None:
                        institutions_results[aff_xml.id] = self.aff_normalizer.query_institutions(aff_xml)
                pkg.articles[xml_name].institutions_query_results = institutions_results
                pkg.articles[xml_name].normalized_affiliations = {aff_id: info[0] for aff_id, info in institutions_results.items()}
        pkg_validations = self.validate_pkg_articles(pkg, registered_issue_data)
        articles_mergence = self.validate_merged_articles(pkg, registered_issue_data)
        pkg_reports = pkg_articles_validations.PkgArticlesValidationsReports(pkg_validations, registered_issue_data.articles_db_manager is not None)
        mergence_reports = merged_articles_validations.MergedArticlesReports(articles_mergence, registered_issue_data)
        validations_reports = merged_articles_validations.IssueArticlesValidationsReports(pkg_reports, mergence_reports, self.is_xml_generation)
        return registered_issue_data, validations_reports

    def make_package(self, pkg, GENERATE_PMC=False):
        registered_issue_data, validations_reports = self.evaluate_package(pkg)
        self.report_result(pkg, validations_reports, conversion=None)
        self.make_pmc_package(pkg, GENERATE_PMC)
        self.zip(pkg)

    def convert_package(self, pkg):
        registered_issue_data, validations_reports = self.evaluate_package(pkg)

        conversion = ArticlesConversion(registered_issue_data, pkg, validations_reports, not self.config.interative_mode, self.config.local_web_app_path, self.config.web_app_site)
        scilista_items = conversion.convert()

        reports = self.report_result(pkg, validations_reports, conversion)
        statistics_display = reports.validations.statistics_display(html_format=False)

        subject = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(conversion.xc_status, [])) + ' ' + statistics_display
        mail_content = '<html><body>' + html_reports.link(reports.report_link, reports.report_link) + '</body></html>'
        mail_info = subject, mail_content
        return (scilista_items, conversion.xc_status, mail_info)

    def validate_pkg_articles(self, pkg, registered_issue_data):
        xml_journal_data_validator = article_validations_module.XMLJournalDataValidator(pkg.issue_data.journal_data)
        xml_issue_data_validator = article_validations_module.XMLIssueDataValidator(registered_issue_data)
        xml_content_validator = article_validations_module.XMLContentValidator(pkg.issue_data, registered_issue_data, self.is_xml_generation, self.app_institutions_manager, self.doi_validator, self.config)
        article_validator = article_validations_module.ArticleValidator(xml_journal_data_validator, xml_issue_data_validator, xml_content_validator, self.config.xml_structure_validator_preference)

        encoding.display_message(_('Validate package ({n} files)').format(n=len(pkg.articles)))
        results = {}
        for name in sorted(pkg.articles.keys()):
            article = pkg.articles[name]
            encoding.display_message(_('Validate {name}').format(name=name))
            results[name] = article_validator.validate(article, pkg.outputs[name], pkg.package_folder.pkgfiles_items[name])
        return results

    def validate_merged_articles(self, pkg, registered_issue_data):
        if len(registered_issue_data.registered_articles) > 0:
            encoding.display_message(_('Previously registered: ({n} files)').format(n=len(registered_issue_data.registered_articles)))
        return merged.ArticlesMergence(
            registered_issue_data.registered_articles,
            pkg.articles)

    def report_result(self, pkg, validations_reports, conversion=None):
        files_location = workarea.AssetsDestinations(pkg.wk.scielo_package_path, pkg.issue_data.acron, pkg.issue_data.issue_label, self.config.serial_path, self.config.local_web_app_path, self.config.web_app_site)
        reports = reports_maker.ReportsMaker(pkg, validations_reports, files_location, self.stage, self.xpm_version, conversion)
        if not self.is_xml_generation:
            reports.save_report(self.INTERATIVE)
        if conversion is not None:
            if conversion.registered_issue_data.issue_files is not None:
                conversion.registered_issue_data.issue_files.save_reports(files_location.report_path)
        if self.config.web_app_site is not None:
            for article_files in pkg.package_folder.pkgfiles_items.values():
                # copia os xml para report path
                article_files.copy_xml(reports.files_location.report_path)
        return reports

    def make_pmc_package(self, pkg, GENERATE_PMC):
        if not self.is_db_generation:
            pmc_package_maker = pmc_pkgmaker.PMCPackageMaker(pkg.wk, pkg.articles, pkg.outputs)
            if self.is_xml_generation:
                pmc_package_maker.make_report()
            if pkg.is_pmc_journal:
                if GENERATE_PMC:
                    pmc_package_maker.make_package()
                else:
                    encoding.display_message(_('To generate PMC package, add -pmc as parameter'))

    def zip(self, pkg):
        if not self.is_xml_generation and not self.is_db_generation:
            pkg.package_folder.zip()
            for name, pkgfiles in pkg.package_folder.pkgfiles_items.items():
                pkgfiles.zip(pkg.package_folder.path + '_zips')
