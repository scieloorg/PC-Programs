# coding=utf-8

from ..__init__ import _
from . import validation_status
from . import article_data_reports
from . import validations as validations_module
from ..reports import html_reports
from ..data import merged


class IssueArticlesValidationsReports(object):

    def __init__(self, pkg_validations_reports, merged_articles_reports, is_xml_generation=False):
        self.pkg_validations_reports = pkg_validations_reports
        self.merged_articles_reports = merged_articles_reports
        self.is_xml_generation = is_xml_generation

    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.merged_articles_reports.journal_issue_header_report)
        errors_only = not self.is_xml_generation
        report.append(self.pkg_validations_reports.pkg_journal_validations.report(errors_only))
        report.append(self.pkg_validations_reports.pkg_issue_validations.report(errors_only))
        report.append(self.merged_articles_reports.report)
        return ''.join(report)

    @property
    def blocking_errors(self):
        return sum([self.merged_articles_reports.validations.blocking_errors,
            self.pkg_validations_reports.pkg_issue_validations.blocking_errors])


class MergedArticlesReports(object):

    def __init__(self, articles_merge, registered_issue_data):
        self.merged_articles_data = merged.MergedArticlesData(articles_merge.merged_articles, registered_issue_data.articles_db_manager is not None)
        self.articles_merge = articles_merge
        self.registered_issue_data = registered_issue_data

    @property
    def journal_issue_header_report(self):
        common_data = ''
        for label, values in self.merged_articles_data.common_data.items():
            if len(values.keys()) == 1:
                common_data += html_reports.tag('p', html_reports.display_label_value(label, list(values.keys())[0]))
            else:
                common_data += html_reports.format_list(label + ':', 'ol', values.keys())
        return html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', common_data, 'issue-data')

    @property
    def report_data_consistency(self):
        text = ''
        if self.registered_issue_data.issue_error_msg is not None:
            text = self.registered_issue_data.issue_error_msg

        reports = []
        reports += self.report_missing_required_data
        reports += self.report_conflicting_values
        reports += self.report_duplicated_values

        text += html_reports.tag('h2', _('Checking issue data consistency'))
        text += html_reports.tag('div', ''.join(reports), 'issue-messages')
        text += self.report_page_values
        return text

    @property
    def report_missing_required_data(self):
        r = ''
        for label, items in self.merged_articles_data.missing_required_data.items():
            r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_BLOCKING_ERROR, label=label)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
        return r

    @property
    def report_conflicting_values(self):
        parts = []
        for label, values in self.merged_articles_data.conflicting_values.items():
            _status = validation_status.STATUS_BLOCKING_ERROR
            if label == 'issue pub date':
                if self.merged_articles_data.is_rolling_pass:
                    _status = validation_status.STATUS_WARNING
            elif label == 'license':
                _status = validation_status.STATUS_WARNING
            _m = _('{status}: same value for {label} is required for all the documents in the package. ').format(status=_status, label=label)
            parts.append(html_reports.p_message(_m))
            parts.append(html_reports.tag('div', html_reports.format_html_data(values), 'issue-problem'))
        return ''.join(parts)

    @property
    def report_duplicated_values(self):
        parts = []
        for label, values in self.merged_articles_data.duplicated_values.items():
            status = self.merged_articles_data.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
            _m = _('Unique value for {label} is required for all the documents in the package').format(label=label)
            parts.append(html_reports.p_message(status + ': ' + _m))
            for value, xml_files in values.items():
                parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def report_page_values(self):
        # FIXME separar validacao e relatório
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        error_level = validation_status.STATUS_BLOCKING_ERROR
        fpage_and_article_id_other_status = [all([a.fpage, a.lpage, a.article_id_other]) for xml_name, a in self.merged_articles_data.articles]
        if all(fpage_and_article_id_other_status):
            error_level = validation_status.STATUS_ERROR

        for xml_name, article in self.merged_articles_data.articles:
            fpage = article.fpage
            lpage = article.lpage
            msg = []
            status = ''
            if article.pages == '':
                msg.append(_('no pagination was found. '))
                if not article.is_ahead:
                    status = validation_status.STATUS_ERROR
            if fpage is not None and lpage is not None:
                if fpage.isdigit() and lpage.isdigit():
                    int_fpage = int(fpage)
                    int_lpage = int(lpage)

                    #if not article.is_rolling_pass and not article.is_ahead:
                    if int_previous_lpage is not None:
                        if int_previous_lpage > int_fpage:
                            status = error_level if not article.is_epub_only else validation_status.STATUS_WARNING
                            msg.append(_('Invalid value for fpage and lpage. Check lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage == int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}) are the same. ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage + 1 < int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('There is a gap between lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                    if int_fpage > int_lpage:
                        status = error_level
                        msg.append(_('Invalid page range: {fpage} (fpage) > {lpage} (lpage). '.format(fpage=int_fpage, lpage=int_lpage)))
                    int_previous_lpage = int_lpage
                    previous_lpage = lpage
                    previous_xmlname = xml_name
            #dates = '|'.join([item if item is not None else 'none' for item in [article.epub_ppub_dateiso, article.collection_dateiso, article.epub_dateiso]])
            msg = '\n'.join(msg)
            results.append({'label': xml_name, 'status': status, 'pages': article.pages, 'message': msg, _('why it is not a valid message?'): ''})
        return html_reports.tag('h2', _('Pages Report')) + html_reports.tag('div', html_reports.sheet(['label', 'status', 'pages', 'message', _('why it is not a valid message?')], results, table_style='validation_sheet', widths={'label': '10', 'status': '10', 'pages': '5', 'message': '75'}))

    def report_merging_conflicts(self):
        merging_errors = []
        if len(self.articles_merge.titaut_conflicts) + len(self.articles_merge.name_order_conflicts) > 0:
            merge_conflicts = self.articles_merge.titaut_conflicts.copy()
            merge_conflicts.update(self.articles_merge.name_order_conflicts)
            merging_errors = [html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to update because the registered article data and the package article data do not match. '))]
            for name, conflicts in merge_conflicts.items():
                labels = []
                #values = [article_data_reports.display_article_data_to_compare(self.)]
                for k, articles in conflicts.items():
                    labels.append(k)
                    if isinstance(articles, dict):
                        data = []
                        for article in articles.values():
                            data.append(article_data_reports.display_article_data_to_compare(article))
                        values.append(''.join(data))
                    else:
                        values.append(article_data_reports.display_article_data_to_compare(articles))
                merging_errors.append(html_reports.sheet(labels, [label_values(labels, values)], table_style='dbstatus', html_cell_content=labels))
        return ''.join(merging_errors)

    def report_order_conflicts(self):
        r = []
        if len(self.articles_merge.pkg_order_conflicts) > 0:
            html_reports.tag('h2', _('Order conflicts'))
            for order, names in self.articles_merge.pkg_order_conflicts.items():
                r.append(html_reports.tag('h3', order))
                r.append(html_reports.format_html_data(names))
        return ''.join(r)

    @property
    def report_changed_names(self):
        r = []
        if len(self.articles_merge.name_changes) > 0:
            r.append(html_reports.tag('h3', _('Names changes')))
            for old, new in self.articles_merge.name_changes.items():
                r.append(html_reports.tag('p', '{old} => {new}'.format(old=old, new=new), 'info'))
        return ''.join(r)

    @property
    def report_changed_orders(self):
        r = []
        if len(self.articles_merge.order_changes) > 0:
            r.append(html_reports.tag('h3', _('Orders changes')))
            for name, changes in self.articles_merge.order_changes.items():
                r.append(html_reports.tag('p', '{name}: {old} => {new}'.format(name=name, old=changes[0], new=changes[1]), 'info'))
        if len(self.articles_merge.excluded_orders) > 0:
            r.append(html_reports.tag('h3', _('Orders exclusions')))
            for name, order in self.articles_merge.excluded_orders.items():
                r.append(html_reports.tag('p', '{order} ({name})'.format(name=name, order=order), 'info'))
        return ''.join(r)

    @property
    def report_changes(self):
        r = ''
        r += self.report_changed_orders
        r += self.report_changed_names
        if len(r) > 0:
            r = html_reports.tag('h2', _('Changes Report')) + r
        return r

    @property
    def report_conflicts(self):
        r = ''.join([self.report_order_conflicts() + self.report_merging_conflicts()])
        if len(r) > 0:
            return html_reports.tag('h2', _('Data Conflicts Report'))
        return ''

    @property
    def validations(self):
        v = validations_module.ValidationsResult()
        v.message = self.report
        return v

    @property
    def report(self):
        r = []
        r.append(self.report_data_consistency)
        r.append(self.report_conflicts)
        r.append(self.report_changes)
        return ''.join(r)
