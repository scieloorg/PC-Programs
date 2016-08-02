import os

from __init__ import _
from . import article
from . import article_reports
from . import article_validations
from . import fs_utils
from . import html_reports
from . import validation_status
from . import xpchecker


class ValidationsResults(object):

    def __init__(self, message):
        self.fatal_errors, self.errors, self.warnings = html_reports.statistics_numbers(message)
        self.message = message

    @property
    def total(self):
        return sum([self.fatal_errors, self.errors, self.warnings])

    def statistics_message(self):
        return '[' + ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(self.fatal_errors)), ('errors', str(self.errors)), ('warnings', str(self.warnings))]]) + ']'

    def block_report(self, new_name, label, id):
        if self.total > 0:
            a_name = 'view-reports-' + new_name
            status = html_reports.statistics_display(self)
            links = html_reports.report_link(id + new_name, '[ ' + _('Structure Validations') + ' ]', id, a_name)
            links += html_reports.tag('span', status, 'smaller')
            block = html_reports.report_block(id + new_name, self.message, id, a_name)
        return (links, block)


class ArticlesSetValidations(object):

    def __init__(self, dtd_files, articles, doc_files_info_items, journals, issues, previous_registered_articles, new_names):
        self.articles = articles
        self.doc_files_info_items = doc_files_info_items
        self.new_names = new_names
        self.journal = journals
        self.pkg_xml_structure_validations = None
        self.pkg_xml_content_validations = None
        self.invalid_xml_name_items = []

        self.expected_equal_values = ['journal-title', 'journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'issue label', 'issue pub date', 'license']
        self.expected_unique_value = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']
        self.journal_check_list_labels = ['journal-id (publisher-id)', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'publisher name', 'license']
        self.required_journal_data = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]

        self.journal_and_issue_data_validations()

    def validate(self, pkg_path, is_xml_generation, is_db_generation):
        for name, a in self.articles.items():
            self.validations[name] = ArticleValidations(self.journal, a, self.doc_files_info_items[name], self.dtd_files, pkg_path, self.new_names[name], is_xml_generation, is_db_generation)

            if self.validations[name].xml_structure_validations.message is not None:
                if len(self.validations[name].xml_structure_validations.message) > 0:
                    fs_utils.write_file(self.report_path + '/xmlstr-' + name, self.validations[name].xml_structure_validations.message)

            if self.validations[name].xml_content_validations.message is not None:
                if len(self.validations[name].xml_content_validations.message) > 0:
                    fs_utils.write_file(self.report_path + '/xmlcon-' + name, self.validations[name].xml_content_validations.message)

    def issue_id_data(self):
        journals = [[a.journal_title, a.print_issn, a.e_issn, a.issue_label] for a in self.articles.values()]
        journals = list(set(journals))
        j = article.Journal()
        if len(journals) > 0:
            j.journal_title, j.p_issn, j.e_issn, issue_label = journals[0]
        return (j, issue_label)

    def journal_and_issue_data_validations(self):
        self.pkg_missing_items = {}
        self.journal_and_issue_data = {}
        labels = self.expected_equal_values + self.expected_unique_value
        for xml_name, article in self.articles.items():
            if article.tree is None:
                self.invalid_xml_name_items.append(xml_name)
            else:
                art_data = article.summary()
                for label in labels:
                    if art_data[label] is None:
                        if label in self.required_journal_data:
                            if not label in self.pkg_missing_items.keys():
                                self.pkg_missing_items[label] = []
                            self.pkg_missing_items[label].append(xml_name)
                    else:
                        if not label in self.journal_and_issue_data.keys():
                            self.journal_and_issue_data[label] = {}
                        if not art_data[label] in self.journal_and_issue_data[label].keys():
                            self.journal_and_issue_data[label][art_data[label]] = []
                        self.journal_and_issue_data[label][art_data[label]].append(xml_name)


class ArticleValidations(object):

    def __init__(self, journal, article, doc_files_info, dtd_files, new_name, pkg_path, is_xml_generation, is_db_generation):
        self.new_name = new_name
        self.article = article
        self.doc_files_info = doc_files_info
        self.dtd_files = dtd_files
        self.pkg_path = pkg_path
        self.journal = journal

    @property
    def xml_structure_validations(self):
        for f in [self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename, self.doc_files_info.data_report_filename, self.doc_files_info.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)
        xml_filename = self.doc_files_info.new_xml_filename

        xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, self.dtd_files, self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename)
        xml_f, xml_e, xml_w = valid_style

        if os.path.isfile(self.doc_files_info.dtd_report_filename):
            separator = ''
            if os.path.isfile(self.doc_files_info.err_filename):
                separator = '\n\n\n' + '.........\n\n\n'
            open(self.doc_files_info.err_filename, 'a+').write(separator + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(self.doc_files_info.dtd_report_filename, 'r').read())

        if xml is None:
            xml_f += 1
        if not valid_dtd:
            xml_f += 1
        if self.doc_files_info.ctrl_filename is None:
            if xml_f + xml_e + xml_w == 0:
                os.unlink(self.doc_files_info.style_report_filename)
        else:
            open(self.doc_files_info.ctrl_filename, 'w').write('Finished')

        if os.path.isfile(self.doc_files_info.dtd_report_filename):
            os.unlink(self.doc_files_info.dtd_report_filename)

        report_content = ''
        for rep_file in [self.doc_files_info.err_filename, self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename]:
            if os.path.isfile(rep_file):
                report_content += extract_report_core(fs_utils.read_file(rep_file))
                #if self.is_xml_generation is False:
                #    fs_utils.delete_file_or_folder(rep_file)
        return ValidationsResults(report_content)

    @property
    def xml_structure_block_report(self):
        return self.xml_structure_validations.block_report(self.new_name, _('Structure Validations'), 'xmlrep')

    @property
    def xml_content_block_report(self):
        return self.xml_content_validations.block_report(self.new_name, _('Contents Validations'), 'datarep')

    @property
    def xml_content_validations(self):
        if self.article.tree is None:
            sheet_data = None
            article_display_report = None
            article_validation_report = None
            content = validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to get data of ') + self.new_name + '.'
        else:
            article_validation = article_validations.ArticleContentValidation(self.journal, self.article, self.is_db_generation, False)
            sheet_data = article_reports.ArticleSheetData(article_validation)
            article_display_report = article_reports.ArticleDisplayReport(sheet_data, self.pkg_path, self.new_name)
            article_validation_report = article_reports.ArticleValidationReport(article_validation)

            content = []

            img_report_content = ''
            if os.path.isfile(self.doc_files_info.images_report_filename):
                img_report_content = fs_utils.read_file(self.doc_files_info.images_report_filename)
            if len(img_report_content) > 0:
                content.append(html_reports.tag('h1', _('ATTENTION'), 'warning'))
                content.append(html_reports.tag('h1', _('New report: Images Report at the bottom'), 'warning'))

            if self.is_xml_generation:
                content.append(article_display_report.issue_header)
                content.append(article_display_report.article_front)

                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.table_tables)

                content.append(article_display_report.article_body)
                content.append(article_display_report.article_back)

            else:
                content.append(article_validation_report.validations(display_all_message_types=False))
                content.append(article_display_report.table_tables)
                content.append(sheet_data.files_and_href(self.pkg_path))

            if len(img_report_content) > 0:
                content.append(img_report_content)

            content = html_reports.join_texts(content)
        data_validations = ValidationsResults(content)
        if self.is_xml_generation:
            stats = html_reports.statistics_display(data_validations, False)
            title = [_('Data Quality Control'), self.new_name]
            fs_utils.write_file(self.doc_files_info.data_report_filename, html_reports.html(title, stats + content))
        return data_validations

    def 



class PkgReportsMaker(object):

    def __init__(self, pkg_path):
        self.pkg_path = pkg_path
        self.xml_filenames = sorted([self.pkg_path + '/' + name for name in os.listdir(self.pkg_path) if name.endswith('.xml')])
        self.xml_names = [name for name in os.listdir(self.pkg_path) if name.endswith('.xml')]

    @property
    def xml_list(self):
        r = ''
        r += '<p>' + _('XML path') + ': ' + self.pkg_path + '</p>'
        r += '<p>' + _('Total of XML files') + ': ' + str(len(self.xml_names)) + '</p>'
        r += html_reports.format_list('', 'ol', self.xml_names)
        return '<div class="xmllist">' + r + '</div>'

    @property
    def overview_report(self):
        r = ''
        r += html_reports.tag('h4', _('Dates overview'))
        labels, items = self.tabulate_dates()
        r += html_reports.sheet(labels, items, 'dbstatus')

        r += html_reports.tag('h4', _('Affiliations overview'))
        items = []
        affs_compiled = self.compile_affiliations()
        for label, occs in affs_compiled.items():
            items.append({'label': label, 'quantity': str(len(occs)), _('files'): sorted(list(set(occs)))})

        r += html_reports.sheet(['label', 'quantity', _('files')], items, 'dbstatus')
        return r


def extract_report_core(content):
    report = ''
    if 'Parse/validation finished' in content and '<!DOCTYPE' in content:
        part1 = content[0:content.find('<!DOCTYPE')]
        part2 = content[content.find('<!DOCTYPE'):]

        l = part1[part1.rfind('Line number:')+len('Line number:'):]
        l = l[0:l.find('Column')]
        l = ''.join([item.strip() for item in l.split()])
        if l.isdigit():
            l = str(int(l) + 1) + ':'
            if l in part2:
                part2 = part2[0:part2.find(l)] + '\n...'

        part1 = part1.replace('\n', '<br/>')
        part2 = part2.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>').replace('\t', '&nbsp;'*4)
        report = '<p>' + part1 + part2 + '</p>'
    elif '</body>' in content:
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
        content = content[content.find('<body'):]
        content = content[0:content.rfind('</body>')]
        report = content[content.find('>')+1:]
    elif '<body' in content:
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
        content = content[content.find('<body'):]
        report = content[content.find('>')+1:]
    return report
