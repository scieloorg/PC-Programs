# coding=utf-8
import logging

from prodtools import _
from prodtools.reports import html_reports
from prodtools.reports import validation_status
from . import article_data_reports
from . import validations as validations_module
from prodtools.validations.pkg_articles_validations import (
    PkgArticlesValidationsReports,
)
from prodtools.data import merged


class IssueArticlesValidationsReports(object):

    def __init__(self, pkg, registered_issue_data, is_db_generation,
                 is_xml_generation, config):
        if len(registered_issue_data.registered_articles) > 0:
            logging.info(_('Previously registered: ({n} files)').format(
                n=len(registered_issue_data.registered_articles)))
        self.registered_issue_data = registered_issue_data
        self.is_xml_generation = is_xml_generation

        conflicts_reports = ConflictsReports(
            pkg, registered_issue_data, is_db_generation)
        self.report_articles_data_conflicts = conflicts_reports.report_articles_data_conflicts
        self.report_articles_data_changes = conflicts_reports.report_articles_data_changes
        self.articles_mergence = conflicts_reports.articles_mergence

        self.group_integrity_reports = GroupCoherenceReports(
            conflicts_reports.merged_articles, is_db_generation)

        self.pkg_validations_reports = PkgArticlesValidationsReports(
            pkg, registered_issue_data, is_db_generation,
            is_xml_generation, config)

        self.blocking_errors = sum(
            [self.validations.blocking_errors,
             self.pkg_validations_reports.blocking_errors])
        self.issue_error_msg = registered_issue_data.issue_error_msg or ''

    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.group_integrity_reports.journal_issue_header_report)
        errors_only = not self.is_xml_generation
        report.append(self.pkg_validations_reports.pkg_journal_validations.report(errors_only))
        report.append(self.pkg_validations_reports.pkg_issue_validations.report(errors_only))
        report.append(self.content)
        return ''.join(report)

    @property
    def issue_validations(self):
        return (
            self.registered_issue_data.issue_error_msg or '' +
            self.group_integrity_reports.content
        )

    @property
    def content(self):
        if not hasattr(self, '_content'):
            r = []
            r.append(self.issue_validations)
            r.append(self.report_articles_data_conflicts)
            r.append(self.report_articles_data_changes)
            self._content = ''.join(r)
        return self._content

    @property
    def validations(self):
        if not hasattr(self, '_validations'):
            self._validations = validations_module.ValidationsResult()
            self._validations.message = self.content
        return self._validations


class ConflictsReports(object):

    def __init__(self, pkg, registered_issue_data, is_db_generation):
        self.articles_mergence = merged.ArticlesMergence(
            registered_issue_data.registered_articles,
            pkg.articles, is_db_generation)
        self.merged_articles = self.articles_mergence.merged_articles

    def report_articles_merging_conflicts(self):
        if not hasattr(self, '_report_articles_merging_conflicts'):
            merging_errors = []
            if len(self.articles_mergence.titaut_conflicts) + len(self.articles_mergence.name_order_conflicts) > 0:

                keys = list(self.articles_mergence.titaut_conflicts.keys()) + list(self.articles_mergence.name_order_conflicts.keys())
                keys = sorted(list(set(keys)))

                merging_errors = [html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to update because the registered article data and the package article data do not match. '))]

                articles = self.articles_mergence.articles
                registered_articles = self.articles_mergence.registered_articles
                for name in keys:
                    labels = [name, _('title/author conflicts'), _('name/order conflicts')]
                    values = [article_data_reports.display_article_data_to_compare(articles.get(name))]

                    articles_in_conflict = []
                    for reg_name, art in self.articles_mergence.titaut_conflicts.get(name, {}).items():
                        articles_in_conflict.append(article_data_reports.display_article_data_to_compare(art))
                    values.append(''.join(articles_in_conflict))

                    articles_in_conflict = []
                    for pkg_name, art in self.articles_mergence.name_order_conflicts.get(name, {}).items():
                        articles_in_conflict.append(article_data_reports.display_article_data_to_compare(art))
                    values.append(''.join(articles_in_conflict))

                    merging_errors.append(html_reports.sheet(labels, [html_reports.label_values(labels, values)], table_style='dbstatus', html_cell_content=labels))
            self._report_articles_merging_conflicts = ''.join(merging_errors)
        return self._report_articles_merging_conflicts

    def report_articles_order_conflicts(self):
        if not hasattr(self, '_report_articles_order_conflicts'):
            r = []
            if len(self.articles_mergence.pkg_order_conflicts) > 0:
                html_reports.tag('h2', _('Order conflicts'))
                for order, names in self.articles_mergence.pkg_order_conflicts.items():
                    r.append(html_reports.tag('h3', order))
                    r.append(html_reports.format_html_data(names))
            self._report_articles_order_conflicts = ''.join(r)
        return self._report_articles_order_conflicts

    @property
    def report_articles_changed_names(self):
        if not hasattr(self, '_report_articles_changed_names'):
            r = []
            if len(self.articles_mergence.name_changes) > 0:
                r.append(html_reports.tag('h3', _('Names changes')))
                for old, new in self.articles_mergence.name_changes.items():
                    r.append(html_reports.tag('p', '{old} => {new}'.format(old=old, new=new), 'info'))
            self._report_articles_changed_names = ''.join(r)
        return self._report_articles_changed_names

    @property
    def report_articles_changed_orders(self):
        if not hasattr(self, '_report_articles_changed_orders'):
            r = []
            if len(self.articles_mergence.order_changes) > 0:
                r.append(html_reports.tag('h3', _('Orders changes')))
                for name, changes in self.articles_mergence.order_changes.items():
                    r.append(html_reports.tag('p', '{name}: {old} => {new}'.format(name=name, old=changes[0], new=changes[1]), 'info'))
            if len(self.articles_mergence.excluded_orders) > 0:
                r.append(html_reports.tag('h3', _('Orders exclusions')))
                for name, order in self.articles_mergence.excluded_items.items():
                    r.append(html_reports.tag('p', '{order} ({name})'.format(name=name, order=order), 'info'))
            self._report_articles_changed_orders = ''.join(r)
        return self._report_articles_changed_orders

    @property
    def report_rejected_articles(self):
        if self.articles_mergence.rejected_articles:
            r = [html_reports.tag('h3', _('Rejected documents'))]
            r.append(
                html_reports.tag(
                    'p',
                    _('These documents were rejected because they are not '
                      '"ahead of print" anymore, they were published in a '
                      'regular issue, '
                      'so they are not allowed to be reinserted as '
                      '"ahead of print".'),
                    'blockingerror'))
            for name in self.articles_mergence.rejected_articles:
                r.append(html_reports.tag('p', name))
            return ''.join(r)
        return ''

    @property
    def report_articles_data_changes(self):
        if not hasattr(self, '_report_articles_data_changes'):
            r = ''
            r += self.report_articles_changed_orders
            r += self.report_articles_changed_names
            if len(r) > 0:
                r = html_reports.tag('h2', _('Changes Report')) + r
            self._report_articles_data_changes = r
        return self._report_articles_data_changes

    @property
    def report_articles_data_conflicts(self):
        if not hasattr(self, '_report_articles_data_conflicts'):
            self._report_articles_data_conflicts = ''
            r = ''.join([self.report_articles_order_conflicts() + self.report_articles_merging_conflicts()])
            if len(r) > 0:
                self._report_articles_data_conflicts = html_reports.tag('h2', _('Data Conflicts Report')) + r
        return self._report_articles_data_conflicts + self.report_rejected_articles


class GroupCoherenceReports(object):
    """
    Avalia os dados do conjunto de documentos
    Verifica se os dados em comum estão idênticos entre todos os documentos
    Verifica os dados que devem ser únicos se o são entre todos os documentos
    etc
    """

    def __init__(self, group, is_db_generation):
        self.group = merged.GroupedDocuments(group, is_db_generation)

    @property
    def journal_issue_header_report(self):
        if not hasattr(self, '_journal_issue_header_report'):
            common_data = ''
            for label, values in self.group.common_data.items():
                if len(values.keys()) == 1:
                    common_data += html_reports.tag('p', html_reports.display_label_value(label, list(values.keys())[0]))
                else:
                    common_data += html_reports.format_list(label + ':', 'ol', values.keys())
            self._journal_issue_header_report = html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', common_data, 'issue-data')
        return self._journal_issue_header_report

    @property
    def content(self):
        reports = (
            self.report_missing_required_issue_data,
            self.report_issue_data_conflicting_values,
            self.report_issue_data_duplicated_values,
            self.report_issue_page_values,
        )
        return (
            html_reports.tag('h2', _('Checking issue data consistency')) +
            html_reports.tag('div', ''.join(reports), 'issue-messages'))

    @property
    def report_missing_required_issue_data(self):
        if not hasattr(self, '_report_missing_required_issue_data'):
            r = ''
            for label, items in self.group.missing_required_data.items():
                r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_BLOCKING_ERROR, label=label)))
                r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
            self._report_missing_required_issue_data = r
        return self._report_missing_required_issue_data

    @property
    def report_issue_data_conflicting_values(self):
        if not hasattr(self, '_report_issue_data_conflicting_values'):
            parts = []
            for label, values in self.group.conflicting_values.items():
                _status = validation_status.STATUS_BLOCKING_ERROR
                if self.group.is_rolling_pass or self.group.is_aop_issue:
                    _status = validation_status.STATUS_WARNING
                elif label == 'license':
                    _status = validation_status.STATUS_WARNING
                _m = _('{status}: same value for {label} is required for all the documents in the package. ').format(status=_status, label=label)
                parts.append(html_reports.p_message(_m))
                parts.append(html_reports.tag('div', html_reports.format_html_data(values), 'issue-problem'))
            self._report_issue_data_conflicting_values = ''.join(parts)
        return self._report_issue_data_conflicting_values

    @property
    def report_issue_data_duplicated_values(self):
        if not hasattr(self, '_report_issue_data_duplicated_values'):
            parts = []
            for label, values in self.group.duplicated_values.items():
                status = self.group.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
                _m = _('Unique value for {label} is required for all the documents in the package').format(label=label)
                parts.append(html_reports.p_message(status + ': ' + _m))
                for value, xml_files in values.items():
                    parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
            self._report_issue_data_duplicated_values = ''.join(parts)
        return self._report_issue_data_duplicated_values

    @property
    def report_issue_page_values(self):
        # FIXME separar validacao e relatório
        if not hasattr(self, '_report_issue_page_values'):
            results = []
            previous = None

            error_level = validation_status.STATUS_BLOCKING_ERROR
            fpage_and_article_id_other_status = [all([a.fpage, a.lpage, a.article_id_other]) for xml_name, a in self.group.articles]
            if all(fpage_and_article_id_other_status):
                error_level = validation_status.STATUS_ERROR

            for xml_name, article in self.group.articles:
                msg = []
                status = ''
                if article.pages == '':
                    msg.append(_('no pagination was found. '))
                    if not article.is_ahead:
                        status = validation_status.STATUS_ERROR
                if all([article.fpage_number, article.lpage_number]):
                    if previous is not None:
                        if previous.lpage_number > article.fpage_number:
                            status = error_level if not article.is_rolling_pass else validation_status.STATUS_WARNING
                            msg.append(_('Invalid value for fpage and lpage. Check lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous.prefix, xml_name=xml_name, lpage=previous.lpage, fpage=article.fpage))
                        elif previous.lpage_number + 1 < article.fpage_number:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('There is a gap between lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous.prefix, xml_name=xml_name, lpage=previous.lpage, fpage=article.fpage))
                        if previous.fpage_number == article.fpage_number:
                            if all([previous.fpage_seq, article.fpage_seq]) is False:
                                msg.append(_('Same value for fpage={fpage} ({previous_article} and {xml_name}) requires @seq for both fpage. ').format(previous_article=previous.prefix, xml_name=xml_name, lpage=previous.fpage, fpage=article.fpage))
                            elif previous.fpage_seq > article.fpage_seq:
                                msg.append(_('fpage/@seq must be a and b: {a} ({previous_article}) and {b} ({xml_name}). ').format(previous_article=previous.prefix, xml_name=xml_name, a=previous.fpage_seq, b=article.fpage_seq))
                    if article.fpage_number > article.lpage_number:
                        status = error_level
                        msg.append(_('Invalid page range: {fpage} (fpage) > {lpage} (lpage). '.format(fpage=article.fpage_number, lpage=article.lpage_number)))
                    previous = article

                msg = '\n'.join(msg)
                results.append({'label': xml_name, 'status': status, 'pages': article.pages, 'message': msg, _('why it is not a valid message?'): ''})
            self._report_issue_page_values = html_reports.tag('h2', _('Pages Report')) + html_reports.tag('div', html_reports.sheet(['label', 'status', 'pages', 'message', _('why it is not a valid message?')], results, table_style='validation_sheet', widths={'label': '10', 'status': '10', 'pages': '5', 'message': '75'}))
        return self._report_issue_page_values

