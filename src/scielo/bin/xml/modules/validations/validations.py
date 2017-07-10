# coding=utf-8

import os
from datetime import datetime

from ..__init__ import _
from ..useful import fs_utils
from ..useful import utils
from ..reports import html_reports
from . import validation_status
from . import article_data_reports


class ValidationsResultItems(dict):

    def __init__(self):
        dict.__init__(self)
        self.title = ''

    @property
    def total(self):
        return sum([item.total() for item in self.values()])

    @property
    def blocking_errors(self):
        return sum([item.blocking_errors for item in self.values()])

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in self.values()])

    @property
    def errors(self):
        return sum([item.errors for item in self.values()])

    @property
    def warnings(self):
        return sum([item.warnings for item in self.values()])

    def report(self, errors_only=False):
        _reports = ''
        for xml_name in sorted(self.keys()):
            results = self[xml_name]
            if results.total() > 0 or errors_only is False:
                _reports += html_reports.tag('h4', xml_name)
                _reports += results.message
        if len(_reports) > 0:
            _reports = self.title + _reports
        return _reports


class ValidationsResult(object):

    def __init__(self):
        self._message = ''
        self.numbers = {}

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self.calculate_numbers()

    def calculate_numbers(self):
        for status, style_checker_error_type in zip(validation_status.STATUS_LEVEL_ORDER, validation_status.STYLE_CHECKER_ERROR_TYPES):
            self.numbers[status] = word_counter(self.message, status)
            if style_checker_error_type != '':
                self.numbers[status] += number_after_words(self.message, style_checker_error_type)

    def total(self):
        return sum([item for item in self.numbers.values()])

    @property
    def statistics_label_and_number(self):
        items = []
        for status in validation_status.STATUS_LEVEL_ORDER:
            items.append((status, validation_status.STATUS_LABELS.get(status), str(self.numbers.get(status, 0))))
        return items

    @property
    def fatal_errors(self):
        return self.numbers.get(validation_status.STATUS_FATAL_ERROR, 0)

    @property
    def errors(self):
        return self.numbers.get(validation_status.STATUS_ERROR, 0)

    @property
    def blocking_errors(self):
        return self.numbers.get(validation_status.STATUS_BLOCKING_ERROR, 0)

    @property
    def warnings(self):
        return self.numbers.get(validation_status.STATUS_WARNING, 0)

    def statistics_display(self, inline=True, html_format=True):
        tag_name = 'span'
        text = ' | '.join([k + ': ' + v for ign, k, v in self.statistics_label_and_number if v != '0'])
        if not inline:
            tag_name = 'div'
            text = ''.join([html_reports.tag('p', html_reports.display_label_value(_('Total of ') + k, v)) for ign, k, v in self.statistics_label_and_number])
        if html_format:
            style = validation_status.message_style(self.statistics_label_and_number)
            r = html_reports.tag(tag_name, text, style)
        else:
            r = text
        return r


class ValidationsFile(ValidationsResult):

    def __init__(self, filename):
        ValidationsResult.__init__(self)
        self.filename = filename
        self._read()

    @ValidationsResult.message.setter
    def message(self, _message):
        self._message = _message
        self.calculate_numbers()
        self._write()

    def _write(self):
        m = self.message if self.message is not None else ''
        fs_utils.write_file(self.filename, m)

    def _read(self):
        if os.path.isfile(self.filename):
            self._message = fs_utils.read_file(self.filename)
        else:
            self._message = ''


class ReportsMaker(object):

    def __init__(self, pkg_reports, pkg_articles_data_report, articles_validations_reports, files_location, stage=None, xpm_version=None, conversion=None):
        self.files_final_location.result_path = None
        self.pkg_reports = pkg_reports
        self.pkg_articles_data_report = pkg_articles_data_report
        self.articles_validations_reports = articles_validations_reports
        self.conversion = conversion
        self.xpm_version = xpm_version
        self.files_location = files_location
        self.stage = stage
        self.report_title = None
        if self.stage == 'xpm':
            self.report_title = _('XML Package Maker Report')
        elif self.stage == 'xc':
            self.report_title = _('XML Conversion (XML to Database)')

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
        self.validations = ValidationsResult()

    @property
    def report_components(self):
        components = {}
        components['pkg-files'] = self.pkg_reports.xml_list
        if self.files_final_location.result_path is not None:
            components['pkg-files'] += self.processing_result_location

        components['summary-report'] = self.pkg_reports.orphan_files_report + self.pkg_articles_data_report.invalid_xml_report
        components['group-validations-report'] = self.pkg_reports.orphan_files_report + self.pkg_articles_data_report.invalid_xml_report
        components['individual-validations-report'] = self.articles_validations_reports.detailed_report
        components['aff-report'] = self.pkg_articles_data_report.articles_affiliations_report
        components['dates-report'] = self.pkg_articles_data_report.articles_dates_report
        components['references'] = (self.pkg_articles_data_report.references_overview_report +
            self.pkg_articles_data_report.sources_overview_report)

        if not self.articles_validations_reports.is_xml_generation:
            components['group-validations-report'] += self.articles_validations_reports.journal_and_issue_report

        if self.conversion is None:
            components['website'] = toc_extended_report(self.pkg_articles_data_report.pkg_articles)
        else:
            components['website'] = self.conversion.conclusion_message + toc_extended_report(self.conversion.registered_articles)
            if self.articles_validations_reports.registered_issue_data.issue_error_msg is not None:
                components['group-validations-report'] += self.articles_validations_reports.registered_issue_data.issue_error_msg

            #components['xc-validations'] = self.conversion.conclusion_message + self.conversion.articles_merger.changes_report + self.conversion.conversion_status_report + self.conversion.aop_status_report + self.conversion.articles_conversion_validations.report(True) + self.conversion.conversion_report
            components['xc-validations'] = html_reports.tag('h3', _('Conversion Result')) + self.conversion.conclusion_message + self.articles_validations_reports.merged_articles_reports.changes_report + self.conversion.aop_status_report + self.conversion.articles_conversion_validations.report(True) + self.conversion.conversion_report

        self.validations.message = html_reports.join_texts(components.values())

        components['summary-report'] += error_msg_subtitle() + self.validations.statistics_display(False)
        if self.conversion is not None:
            components['summary-report'] += html_reports.tag('h2', _('Summary report')) + self.conversion.conclusion_message

        components = {k: label_errors(v) for k, v in components.items() if v is not None}
        return components

    @property
    def footnote(self):
        content = html_reports.tag('p', _('finished'))
        if self.xpm_version is not None:
            content += html_reports.tag('p', _('report generated by XPM ') + self.xpm_version)
        return content

    @property
    def report_version(self):
        version = ''
        if self.stage == 'xc':
            version = '_' + datetime.now().isoformat()[0:19].replace(':', '').replace('T', '_')
        return version

    @property
    def report_filename(self):
        return self.stage + self.report_version + '.html'

    @property
    def report_path(self):
        return self.files_final_location.report_path

    @property
    def report_location(self):
        return self.report_path + '/' + self.stage + '.html'

    def save_report(self, display=False):
        reports.save_report(self.report_path, self.report_filename, self.report_title)
        if display is True:
            html_reports.display_report(self.report_location)
        msg = _('Saved report: {f}').format(f=self.report_location)
        utils.display_message(msg)

    @property
    def content(self):
        tabbed_report = html_reports.TabbedReport(self.labels, self.tabs, self.report_components, 'summary-report')
        content = tabbed_report.report_content
        origin = ['{IMG_PATH}', '{PDF_PATH}', '{XML_PATH}', '{RES_PATH}', '{REP_PATH}']
        replac = [self.files_location.img_link, self.files_location.pdf_link, self.files_location.xml_link, self.files_location.result_path, self.files_location.report_path]
        for o, r in zip(origin, replac):
            content = content.replace(o, r)
        return content + self.footnote

    @property
    def processing_result_location(self):
        result_path = self.files_final_location.result_path
        return '<h5>' + _('Result of the processing:') + '</h5>' + '<p>' + html_reports.link('file:///' + result_path, result_path) + '</p>'


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


def word_counter(content, word):
    return len(content.split(word)) - 1


def number_after_words(content, text='Total of errors = '):
    n = 0
    if text in content:
        content = content[content.find(text) + len(text):]
        finished = False
        n = ''
        while not finished and len(content) > 0:
            if content[0].isdigit():
                n += content[0]
                content = content[1:]
            else:
                finished = True

        if len(n) > 0:
            n = int(n)
        else:
            n = 0
    return n


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

