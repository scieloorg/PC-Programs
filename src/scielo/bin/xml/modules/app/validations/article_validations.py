# coding=utf-8

import os

from ...__init__ import _
from ...generics import fs_utils
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from ..validations import sps_xml_validators
from . import article_data_reports
from . import article_content_validations
from . import validations as validations_module
from ..pkg_processors import xml_versions


class XMLJournalDataValidator(object):

    def __init__(self, journal_data):
        self.journal_data = journal_data

    def validate(self, article):
        if self.journal_data is None:
            r = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to identify {unidentified}. ').format(unidentified=_('journal'))
        else:
            items = []
            license_url = None
            if len(article.article_licenses) > 0:
                license_url = list(article.article_licenses.values())[0].get('href')

            items.append([_('NLM title'), article.journal_id_nlm_ta, self.journal_data.nlm_title, validation_status.STATUS_FATAL_ERROR])
            #items.append([_('journal-id (publisher-id)'), article.journal_id_publisher_id, self.journal_data.acron, validation_status.STATUS_FATAL_ERROR])
            items.append([_('e-ISSN'), article.e_issn, self.journal_data.e_issn, validation_status.STATUS_FATAL_ERROR])
            items.append([_('print ISSN'), article.print_issn, self.journal_data.p_issn, validation_status.STATUS_FATAL_ERROR])
            items.append([_('publisher name'), article.publisher_name, self.journal_data.publisher_name, validation_status.STATUS_ERROR])
            items.append([_('license'), license_url, self.journal_data.license, validation_status.STATUS_ERROR])
            r = evaluate_journal_data(items)

        result = validations_module.ValidationsResult()
        result.message = r
        return result


class XMLIssueDataValidator(object):

    def __init__(self, registered_issue_data):
        self.issue_error_msg = registered_issue_data.issue_error_msg
        self.issue_models = registered_issue_data.issue_models
        self.is_db_generation = registered_issue_data.articles_db_manager is not None

    def validate(self, article):
        r = ''
        if self.is_db_generation:
            if self.issue_error_msg is not None:
                r = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to identify {unidentified}. ').format(unidentified=_('issue'))
                r += self.issue_error_msg
            elif self.issue_models:
                r = self.issue_models.validate_article_issue_data(article)

        result = validations_module.ValidationsResult()
        result.message = r
        return result


class XMLStructureValidator(object):

    def __init__(self, dtd_files):
        self.xml_validator = sps_xml_validators.XMLValidator(dtd_files)

    def validate(self, xml_filename, outputs):
        separator = '\n\n\n' + '.........\n\n\n'
        name_error = ''
        new_name, ign = os.path.splitext(os.path.basename(xml_filename))
        if '_' in new_name or '.' in new_name:
            name_error = rst_title(_('Name errors')) + _('{value} has forbidden characters, which are {forbidden_characters}').format(value=new_name, forbidden_characters='_.') + separator

        fs_utils.write_file(outputs.err_filename, fs_utils.read_file(outputs.mkp2xml_report_filename) or '')

        for f in [outputs.dtd_report_filename, outputs.style_report_filename, outputs.data_report_filename, outputs.pmc_style_report_filename]:
            fs_utils.delete_file_or_folder(f)
        xml, valid_dtd, valid_style = self.xml_validator.validate(xml_filename, outputs.dtd_report_filename, outputs.style_report_filename)
        xml_f, xml_e, xml_w = valid_style

        dtd_errors = fs_utils.read_file(outputs.dtd_report_filename) or ''
        if len(dtd_errors) > 0:
            dtd_errors = rst_title(_('DTD errors')) + dtd_errors

        report_title = ''
        report_content = ''
        if xml is None:
            xml_f += 1
            report_title += validation_status.STATUS_FATAL_ERROR + ' ' + _('XML file is invalid') + '\n'
        if not valid_dtd:
            xml_f += 1
            report_title += validation_status.STATUS_FATAL_ERROR + ' ' + _('XML file has DTD errors') + '\n'
        if len(name_error) > 0:
            xml_f += 1
            report_title += validation_status.STATUS_FATAL_ERROR + ' ' + _('XML file has name errors') + '\n'

        if len(report_title) > 0:
            report_title = rst_title(_('Summary')) + report_title + separator
            report_title = report_title.replace('\n', '<br/>')

        if xml_f > 0:
            fs_utils.append_file(outputs.err_filename, name_error + dtd_errors)
        if outputs.ctrl_filename is None:
            if xml_f + xml_e + xml_w == 0:
                fs_utils.delete_file_or_folder(outputs.style_report_filename)
        else:
            fs_utils.write_file(outputs.ctrl_filename, 'Finished')
        for rep_file in [outputs.err_filename, outputs.style_report_filename]:
            if os.path.isfile(rep_file):
                report_content += extract_report_core(fs_utils.read_file(rep_file))

        r = validations_module.ValidationsResult()
        r.message = report_title + report_content
        return r


class XMLContentValidator(object):

    def __init__(self, pkgissuedata, registered_issue_data, is_xml_generation, app_institutions_manager, doi_validator):
        self.registered_issue_data = registered_issue_data
        self.pkgissuedata = pkgissuedata
        self.is_xml_generation = is_xml_generation
        self.doi_validator = doi_validator
        self.app_institutions_manager = app_institutions_manager

    def validate(self, article, outputs, pkgfiles):
        article_display_report = None
        article_validation_report = None

        if article.tree is None:
            content = validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to get data from {item}. ').format(item=article.new_prefix)
        else:
            content_validation = article_content_validations.ArticleContentValidation(self.pkgissuedata.journal, article, pkgfiles, (self.registered_issue_data.articles_db_manager is not None), False, self.app_institutions_manager, self.doi_validator)
            article_display_report = article_data_reports.ArticleDisplayReport(content_validation)
            article_validation_report = article_data_reports.ArticleValidationReport(content_validation)

            content = []

            if self.is_xml_generation:
                content.append(article_display_report.issue_header)
                content.append(article_display_report.article_front)
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.display_formulas)
                content.append(article_display_report.table_tables)
                r = fs_utils.read_file(outputs.images_report_filename) or ''
                r = r[r.find('<body'):]
                r = r[r.find('>')+1:]
                r = r[:r.find('</body>')]
                content.append(r)
                content.append(article_display_report.article_body)
                content.append(article_display_report.article_back)

            else:
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.display_formulas)
                content.append(article_display_report.table_tables)
                r = fs_utils.read_file(outputs.images_report_filename) or ''

                r = r[r.find('<body'):]
                r = r[r.find('>')+1:]
                r = r[:r.find('</body>')]
                content.append(r)
                content.append(article_display_report.files_and_href())
            content = ''.join(content)
        r = validations_module.ValidationsResult()
        r.message = content
        return r, article_display_report


class ArticleValidator(object):

    def __init__(self, xml_journal_data_validator, xml_issue_data_validator, xml_content_validator):
        self.xml_journal_data_validator = xml_journal_data_validator
        self.xml_issue_data_validator = xml_issue_data_validator
        self.xml_content_validator = xml_content_validator

    def validate(self, article, outputs, pkgfiles):
        scielo_dtd_files, pmc_dtd_files = xml_versions.identify_dtd_files(fs_utils.read_file(pkgfiles.filename))
        xml_structure_validator = XMLStructureValidator(scielo_dtd_files)

        artval = ArticleValidations()
        artval.journal_validations = self.xml_journal_data_validator.validate(article)
        artval.issue_validations = self.xml_issue_data_validator.validate(article)
        artval.xml_structure_validations = xml_structure_validator.validate(pkgfiles.filename, outputs)
        artval.xml_content_validations, artval.article_display_report = self.xml_content_validator.validate(article, outputs, pkgfiles)
        if self.xml_content_validator.is_xml_generation:
            stats = artval.xml_content_validations.statistics_display(False)
            title = [_('Data Quality Control'), article.new_prefix]
            fs_utils.write_file(outputs.data_report_filename, html_reports.html(title, stats + artval.xml_content_validations.message))
        return artval


class ArticleValidations(object):

    def __init__(self):
        self.journal_validations = None
        self.issue_validations = None
        self.xml_structure_validations = None
        self.xml_content_validations = None

    @property
    def fatal_errors(self):
        return sum([item.fatal_errors for item in [self.xml_structure_validations, self.xml_content_validations]])

    def hide_and_show_block(self, report_id, new_name):
        blocks = []
        block_parent_id = report_id + new_name
        blocks.append((_('Structure Validations'), 'xmlrep', self.xml_structure_validations))
        blocks.append((_('Contents Validations'),  'datarep', self.xml_content_validations))
        if self.issue_validations:
            blocks.append((_('Converter Validations'), 'xcrep', self.issue_validations))
        _blocks = []
        for label, style, validations_file in blocks:
            if validations_file.total() > 0:
                status = validations_file.statistics_display()
                _blocks.append(html_reports.HideAndShowBlockItem(block_parent_id, label, style + new_name, style, validations_file.message, status))
        return html_reports.HideAndShowBlock(block_parent_id, _blocks)


def extract_report_core(content):
    if content.strip().lower().endswith('</html>') or content.strip().lower().startswith('<html'):
        if '<body' in content:
            content = content[content.find('<body'):]
            content = content[content.find('>')+1:]
        if '</body>' in content:
            content = content[:content.rfind('</body>')]
        report = content
    elif 'Parse/validation finished' in content:
        part1 = ''
        part2 = content
        if '1:' in content:
            part1 = content[0:content.find('1:')]
            part2 = content[content.find('1:'):]
        if 'Line number:' in part1:
            l = part1[part1.rfind('Line number:')+len('Line number:'):]
            l = l[0:l.find('Column')]
            l = ''.join([c for c in list(l) if c.isdigit()])
            if l.isdigit():
                l = str(int(l) + 1) + ':'
                if l in part2:
                    part2 = part2[0:part2.find(l)] + '\n...'
        report = part1 + part2
        report = report.replace('<', '&lt;').replace('>', '&gt;').replace('\t', '&nbsp;'*4).replace('\n', '<br/>')
    else:
        report = ''
    return report


def evaluate_journal_data(items):
    unmatched = []
    for label, value, expected_values, default_status in items:
        if expected_values is None:
            expected_values = [None]
        if len(expected_values) == 0:
            expected_values.extend([None, ''])
        status = validation_status.STATUS_OK
        if value not in expected_values:
            status = default_status
            for expected_value in expected_values:
                if expected_value is not None and value is not None:
                    if '/' + expected_value.lower() + '/' in value.lower() + '/':
                        status = validation_status.STATUS_OK
                        break

        if status != validation_status.STATUS_OK:
            if None in expected_values:
                expected_values = [item for item in expected_values if item is not None]
                expected_values.append(_('none'))
            unmatched.append({_('data'): label, 'status': status, 'XML': value, _('registered journal data') + '*': _(' or ').join(expected_values), _('why it is not a valid message?'): ''})

    validations_result = ''
    if len(unmatched) > 0:
        validations_result = html_reports.sheet([_('data'), 'status', 'XML', _('registered journal data') + '*', _('why it is not a valid message?')], unmatched, table_style='dbstatus')
    return validations_result


def rst_title(title):
    return '\n\n' + title + '\n' + '-'*len(title) + '\n'
