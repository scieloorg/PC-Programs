# coding=utf-8

import os
import shutil

from configuration import Configuration
from xml_utils import load_xml
from isis import IDFile, UCISIS, CISIS, IsisDAO
from article import Article
from isis_models import ArticleISIS, IssueISIS

import files_manager
import xpmaker
import reports


class XMLConverter(object):

    def __init__(self, serial_path, db_issue, db_ahead, db_article):
        self.db_issue = db_issue
        self.db_ahead = db_ahead
        self.db_article = db_article
        self.serial_path = serial_path
        self.msg = []

    def get_issue_record(self, validation_results):
        issue_record = None
        issue_label = ''
        for xml_name, data in validation_results.items():
            results, article = data
            if article is not None:
                issue_label = article.issue_label
                if issue_label is not None:
                    issues_records = self.db_issue.search(article.issue_label, article.print_issn, article.e_issn)
                    if len(issues_records) > 0:
                        issue_record = issues_records[0]
                    break
        return (issue_label, issue_record)

    def display_statistic(self, f, e, w):
        self.msg.append('fatal errors: ' + str(f))
        self.msg.append('errors: ' + str(e))
        self.msg.append('warnings: ' + str(w))

    def evaluate_package(self, xml_path, report_path):
        if not os.path.isdir(report_path):
            os.makedirs(report_path)
        xml_names = {f.replace('.xml', ''):f.replace('.xml', '') for f in os.listdir(xml_path) if f.endswith('.xml')}

        toc_statistic, package_statistic, validation_results, issues = reports.generate_package_reports(xml_path, xml_names, report_path)
        toc_f, toc_e, toc_w = toc_statistic
        package_f, package_e, package_w = package_statistic

        self.msg.append('Validations reports in ' + report_path)
        self.msg.append('\nTOC Validations')
        self.display_statistic(toc_f, toc_e, toc_w)
        self.msg.append('\nArticles validations')
        self.display_statistic(package_f, package_e, package_w)

        return (toc_f == 0, validation_results)

    def convert_package(self, xml_path, report_path, base_path, id_path, web_path):
        is_valid_package, validation_results = self.evaluate_package(xml_path, report_path)

        if not is_valid_package:
            self.msg.append('\nFATAL ERROR: Unable to generate base because of fatal errors in TOC report.')
        else:
            issue_label, issue_record = self.get_issue_record(validation_results)
            if issue_record is None:
                self.msg.append('\nFATAL ERROR: ' + issue_label + ' is not registered.')
            else:
                issue = IssueISIS(issue_record).issue
                journal_files = JournalFiles(self.serial_path, issue.acron)
                issue_files = IssueFiles(journal_files, issue.issue_label)
                ahead_manager = AheadManager(self.db_ahead, journal_files)

                self.msg.append('\nTotal of articles in package: ' + str(len(validation_results)))
                total_new_articles, total_ex_aheads = self.convert_articles(issue_record, issue_files, validation_results)

                self.msg.append('.'*80)

                self.msg.append('\nTotal of articles in package: ' + str(len(validation_results)))
                self.msg.append('\nnew articles: ' + str(len(total_new_articles)))
                self.msg.append('\n'.join(total_new_articles))
                self.msg.append('\nex-aheads: ' + str(len(total_ex_aheads)))
                self.msg.append('\n'.join(total_ex_aheads))

                loaded = self.db_article.finish_conversion(issue_record, issue_files)
                q = len(validation_results) - len(loaded)
                if q > 0:
                    self.msg.append('\nFATAL ERROR: ' + str(q) + ' were not loaded.')
                self.msg.append('\nLoaded: ' + str(len(loaded)))
                self.msg.append('\n'.join(loaded))

                if len(total_ex_aheads) > 0:
                    self.msg += ahead_manager.finish_manage_ex_ahead()

                self.msg += issue_files.copy_files_to_web()
        open(report_path + '/conversion.log', 'w').write('\n'.join(self.msg))
        print(report_path + '/conversion.log')
        print('-- end --')

    def convert_articles(self, issue_record, issue_files, validation_results):
        total_new_articles = []
        total_ex_aheads = []

        for xml_name, data in validation_results.items():
            results, article = data
            f, e, w = results

            article_title = article.title[0] if len(article.title) > 0 else xml_name
            self.msg.append('.'*80)
            self.msg.append(xml_name)
            if article_title != xml_name:
                self.msg.append(article_title)
            self.display_statistic(fatal_errors, errors, warnings)

            if fatal_errors > 0:
                self.msg.append('FATAL ERROR: XML file has fatal errors.')
            else:
                article_files = ArticleFiles(issue_files, article.order, xml_name)
                if self.convert_article(issue_record, article, article_files):
                    new_articles, ex_aheads = self.manage_ex_ahead(ahead_manager, article, xml_name)
                    total_new_articles += new_articles
                    total_ex_aheads += ex_aheads
                else:
                    self.msg.append('FATAL ERROR: Unable to generate ' + article_files.id_filename)

    def convert_article(self, issue_record, article, article_files):
        r = False
        section_code = issue_record.check_section(article.toc_section)
        if section_code is None:
            self.msg.append('FATAL ERROR: ' + article.toc_section + ' is not a valid section.')
        else:
            r = db_article.create_id_file(issue_record, article, section_code, article_files)
        return r

    def manage_ex_ahead(self, ahead_manager, article, xml_name):
        if article.number != 'ahead':
            is_ex_ahead = ahead_manager.manage_ex_ahead(article.doi, xml_name)
            if is_ex_ahead is None:
                new_articles.append(xml_name + ' ' + article.title)
            else:
                ex_aheads.append(xml_name + ' ' + article.title)
        return (new_articles, ex_aheads)


def validate_path(path):
    xml_path = None
    base_path = ''
    id_path = ''
    if path is not None:
        path = path.replace('\\', '/')
        if path.endswith('/'):
            path = path[0:-1]
        if len(path) > 0:
            if os.path.isdir(path):
                xml_files = [path + '/' + f for f in os.listdir(path) if f.endswith('.xml')]
                if len(xml_files) > 0:
                    xml_path = path
                    name = os.path.basename(path)
                    parent_path = os.path.dirname(path)
                    if name == 'scielo_package' and os.path.basename(parent_path) == 'markup_xml':
                        issue_path = os.path.dirname(parent_path)
                    else:
                        issue_path = parent_path
                    base_path = issue_path + '/base'
                    if not os.path.isdir(base_path):
                        os.makedirs(base_path)
                    id_path = issue_path + '/id'
                    if not os.path.isdir(id_path):
                        os.makedirs(id_path)
                    report_path = issue_path + '/base_reports'
                    if not os.path.isdir(id_path):
                        os.makedirs(id_path)
    return (xml_path, report_path, base_path, id_path)


def convert(path, acron):
    #FIXME
    xml_path, report_path, base_path, id_path = validate_path(path)
    if xml_path is None:
        print('There is nothing to convert.\n')
        print(' must be an XML file or a folder which contains XML files.')
    else:
        config = Configuration()
        curr_path = os.getcwd().replace('\\', '/')
        if os.path.isfile(curr_path + '/./../scielo_paths.ini'):
            config.read(curr_path + '/./../scielo_paths.ini')

            cisis = UCISIS(CISIS(curr_path + '/./../cfg/'), CISIS(curr_path + '/./../cfg/cisis1660/'))
            dao = IsisDAO(cisis)

            fst_filename = curr_path + '/./../convert/library/scielo/scielo.fst'

            serial_path = config.data.get('Serial Directory')
            db_issue_filename = config.data.get('Issue Database')
            xml_converter = XMLConverter(serial_path, files_manager.IssueDAO(dao, db_issue_filename), dao, files_manager.ArticleDAO(dao))

            web_path = config.data.get('SCI_LISTA_SITE')
            if web_path is not None:
                web_path = web_path.replace('\\', '/')
                web_path = web_path[0:web_path.find('/proc/')]
                if not os.path.isdir(web_path):
                    web_path = base_path.replace('/base', '/4web')
            xml_converter.convert_package(xml_path, report_path, base_path, id_path, web_path)
        else:
            print('Configuration file was not found.')


def read_inputs(args):
    path = None
    acron = ''
    if len(args) == 3:
        script, path, acron = args
        path = path.replace('\\', '/')
        if not os.path.isfile(path) and not os.path.isdir(path):
            path = None

    if path is None:
        messages = []
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python ' + script + ' <xml_src> <acron>')
        messages.append('where:')
        messages.append('  <xml_src> = XML filename or path which contains XML files')
        messages.append('  <acron> = journal acronym')
        acron = '\n'.join(messages)

    return (path, acron)


def call_converter(args):
    path, acron = read_inputs(args)
    if path is None:
        print(acron)
    else:
        convert(path, acron)
