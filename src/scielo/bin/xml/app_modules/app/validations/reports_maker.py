# coding=utf-8
import os
from datetime import datetime

from ...__init__ import _
from ...generics import utils
from ...generics import encoding
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from . import article_data_reports
from . import pkg_articles_validations
from . import validations as validations_module


class ReportsMaker(object):

    def __init__(self, pkg, articles_validations_reports, files_location, stage, xpm_version=None, conversion=None):
        self.articles_validations_reports = articles_validations_reports
        self.conversion = conversion
        self.xpm_version = xpm_version
        self.stage = stage
        self.report_title = None
        self.report_version = ''
        if self.stage == 'xc':
            self.report_version = '_' + datetime.now().isoformat()[0:19].replace(':', '').replace('T', '_')
        self.files_location = files_location
        self.pkg = pkg
        self.pkg_reports = pkg_articles_validations.PackageReports(pkg.package_folder)
        self.pkg_articles_data_report = pkg_articles_validations.PkgArticlesDataReports(pkg.articles)

        self.tab = 'summary-report'
        if self.stage == 'xpm':
            self.report_title = _('XML Package Maker Report')
        elif self.stage == 'xc':
            self.report_title = _('XML Conversion (XML to Database)')
            self.tab = 'xc-validations'

        self.tabs = ['pkg-files', 'summary-report', 'group-validations-report', 'individual-validations-report', 'references', 'dates-report', 'aff-report', 'xc-validations', 'website']
        self.labels = {
            'pkg-files': _('Files/Folders'),
            'summary-report': _('Summary'),
            'group-validations-report': _('Group Validations'),
            'individual-validations-report': _('Individual Validations'),
            'xc-validations': _('Converter Validations'),
            'aff-report': _('Affiliations'),
            'dates-report': _('Dates'),
            'references': _('References'),
            'website': _('Website'),
        }
        self.validations = validations_module.ValidationsResult()

    @property
    def report_components(self):
        components = {}
        components['pkg-files'] = self.full_xpm_version + self.pkg_files
        components['summary-report'] = self.summary_report
        components['group-validations-report'] = self.group_validations_report
        components['individual-validations-report'] = self.individual_validations_report
        components['aff-report'] = self.aff_report
        components['dates-report'] = self.dates_report
        components['references'] = self.references
        components['website'] = self.website_message
        if self.conversion is not None:
            components['xc-validations'] = self.xc_validations

        self.validations.message = ''.join(list(components.values()))

        components['summary-report'] += error_msg_subtitle() + self.validations.statistics_display(False)
        if self.conversion is not None:
            components['summary-report'] += html_reports.tag('h2', _('Summary report')) + self.conversion.conclusion_message

        components = {k: label_errors(v) for k, v in components.items() if v is not None}
        return components

    @property
    def pkg_files(self):
        r = self.pkg_reports.xml_list
        if self.files_location.result_path is not None:
            r += self.processing_result_location
        return r

    @property
    def summary_report(self):
        return self.pkg_reports.orphan_files_report + self.pkg_articles_data_report.invalid_xml_report

    @property
    def group_validations_report(self):
        r = self.pkg_reports.orphan_files_report + self.pkg_articles_data_report.invalid_xml_report
        if not self.articles_validations_reports.is_xml_generation:
            r += self.articles_validations_reports.journal_and_issue_report
        if self.conversion is not None:
            if self.articles_validations_reports.merged_articles_reports.registered_issue_data.issue_error_msg is not None:
                r += self.articles_validations_reports.merged_articles_reports.registered_issue_data.issue_error_msg
        return r

    @property
    def individual_validations_report(self):
        return self.articles_validations_reports.pkg_validations_reports.detailed_report

    @property
    def aff_report(self):
        return self.pkg_articles_data_report.articles_affiliations_report

    @property
    def dates_report(self):
        return self.pkg_articles_data_report.articles_dates_report

    @property
    def references(self):
        return self.pkg_articles_data_report.references_overview_report + self.pkg_articles_data_report.sources_overview_report

    @property
    def website_message(self):
        if self.conversion is None:
            return toc_extended_report(self.pkg.articles)
        return self.conversion.conclusion_message + toc_extended_report(self.conversion.registered_articles)

    @property
    def xc_validations(self):
        r = []
        r.append(html_reports.tag('h3', _('Frequency')))
        r.append(
            html_reports.tag('h4', _(self.pkg.issue_data.journal.frequency)))

        r.append(html_reports.tag('h3', _('Conversion Result')))
        r.append(self.conversion.conclusion_message)
        r.append(self.articles_validations_reports.merged_articles_reports.report_articles_data_conflicts)
        r.append(self.articles_validations_reports.merged_articles_reports.report_articles_data_changes)
        r.append(self.conversion.aop_status_report)
        r.append(self.conversion.articles_conversion_validations.report())
        r.append(self.conversion.conversion_report)
        return ''.join(r)

    @property
    def full_xpm_version(self):
        if self.xpm_version is not None:
            return '<!-- XPM 2017/2 --> <!-- {} --> <!-- {} --> '.format(self.xpm_version[0], self.xpm_version[1])
        return ''

    @property
    def footnote(self):
        content = html_reports.tag('p', _('finished'))
        if self.xpm_version is not None:
            content += html_reports.tag('p', _('report generated by XPM ') + self.xpm_version[0])
        return content

    @property
    def report_location(self):
        return os.path.join(
            self.files_location.report_path,
            self.stage + self.report_version + '.html')

    @property
    def report_link(self):
        return os.path.join(
            self.files_location.report_link,
            os.path.basename(self.report_location))

    def save_report(self, display=True):
        html_reports.save(
            self.report_location, self.report_title, self.content, self.stage)
        if display is True:
            html_reports.display_report(self.report_location)
        msg = _('Saved report: {f}').format(f=self.report_location)
        encoding.display_message(msg)

    @property
    def content(self):
        tabbed_report = html_reports.TabbedReport(self.labels, self.tabs, self.report_components, self.tab)
        content = tabbed_report.report_content
        origin = ['{IMG_PATH}', '{PDF_PATH}', '{XML_PATH}', '{RES_PATH}', '{REP_PATH}']
        replac = [self.files_location.img_link, self.files_location.pdf_link,
                  self.files_location.xml_link,
                  self.files_location.result_path,
                  self.files_location.report_path]
        for o, r in zip(origin, replac):
            print(o, r)
            content = content.replace(o, r)
        return content + self.footnote

    @property
    def processing_result_location(self):
        result_path = self.files_location.result_path
        return (
            '<h5>' + _('Result of the processing:') + '</h5>' + '<p>' +
            html_reports.link(os.path.join('file:///', result_path), result_path) + '</p>')


def error_msg_subtitle():
    msg = html_reports.tag('p', _('Blocking error - indicates errors of data consistency'))
    msg += html_reports.tag('p', _('Fatal error - indicates errors which impact on the quality of the bibliometric indicators and other services'))
    msg += html_reports.tag('p', _('Error - indicates the other kinds of errors'))
    msg += html_reports.tag('p', _('Warning - indicates that something can be an error or something needs more attention'))
    return html_reports.tag('div', msg, 'subtitle')


def label_errors(content):
    if content is None:
        content = ''
    else:
        content = label_errors_type(content, validation_status.STATUS_BLOCKING_ERROR, 'B')
        content = label_errors_type(content, validation_status.STATUS_FATAL_ERROR, 'F')
        content = label_errors_type(content, validation_status.STATUS_ERROR, 'E')
        content = label_errors_type(content, validation_status.STATUS_WARNING, 'W')
    return content


def label_errors_type(content, error_type, prefix):
    new = []
    i = 0
    content = content.replace(error_type, '~BREAK~' + error_type)
    for part in content.split('~BREAK~'):
        if part.startswith(error_type):
            i += 1
            part = part.replace(error_type, error_type + ' [' + prefix + str(i) + ']')
        new.append(part)
    return ''.join(new)


def articles_sorted_by_order(articles):
    l = sorted([(article.order, xml_name) for xml_name, article in articles.items()])
    l = [(xml_name, articles[xml_name]) for order, xml_name in l]
    return l


def toc_extended_report(articles):
    if articles is None:
        return ''
    else:
        labels = [_('filename'), 'order', _('last update'), _('article')]
        widths = {_('filename'): '5', 'order': '2', _('last update'): '5', _('article'): '88'}
        items = []
        for new_name, article in articles_sorted_by_order(articles):
            if not article.is_ex_aop:
                values = []
                values.append(new_name)
                values.append(article.order)
                last_update_display = article.last_update_display
                if last_update_display is None:
                    last_update_display = ''
                if last_update_display[:10] == utils.display_datetime(utils.now()[0]):
                    last_update_display = html_reports.tag('span', last_update_display, 'report-date')
                values.append(last_update_display)
                values.append(article_data_reports.display_article_data_in_toc(article))
                items.append(html_reports.label_values(labels, values))
        return html_reports.sheet(labels, items, table_style='reports-sheet', html_cell_content=[_('article'), _('last update')], widths=widths)
