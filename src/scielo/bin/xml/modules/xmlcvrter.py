# coding=utf-8

import os
import shutil

from configuration import Configuration
from xml_utils import load_xml
from isis import IDFile, UCISIS, CISIS
from article import Article
from isis_models import ArticleISIS, IssueISIS

import files_manager
import xpmaker
import reports


class XMLConverter(object):

    def __init__(self, db_issue, serial_path, db_ahead):
        self.db_issue = db_issue
        self.db_ahead = db_ahead
        self.serial_path = serial_path
        self.msg = []

    def get_issue_record(self, issue_label, article_reports):
        issue_record = None
        for xml_name, data in article_reports.items():
            results, article = data
            issues_records = self.db_issue.search(issue_label, article.print_issn, article.e_issn)
            if len(issues_records) > 0:
                issue_record = issues_records[0]
                break
        return issue_record

    def display_statistic(self, f, e, w):
        self.msg.append('fatal errors: ' + str(len(f)))
        self.msg.append('errors: ' + str(len(e)))
        self.msg.append('warnings: ' + str(len(w)))

    def convert_package(self, xml_path, report_path, base_path, id_path, web_path):
        xml_names = {f.replace('.xml', ''):f.replace('.xml', '') for f in os.listdir(xml_path) if f.endswith('.xml')}

        toc_statistic, package_statistic, article_reports, issues = reports.generate_package_reports(xml_path, xml_names, report_path)
        toc_f, toc_e, toc_w = toc_statistic
        package_f, package_e, package_w = package_statistic

        self.msg.append('Validations reports in ' + report_path)
        self.msg.append('TOC Validations')
        display_statistic(toc_f, toc_e, toc_w)
        self.msg.append('Articles validations')
        display_statistic(package_f, package_e, package_w)

        if toc_f > 0:
            self.msg.append('FATAL ERROR: Unable to convert the issue.')
        else:
            db_article = None
            issue_record = None
            issue_isis = None
            issue_label = ''
            if len(issues) == 1:
                issue_label = issues[0]
                issue_record = self.get_issue_record(issue_label, article_reports)
                issue = IssueISIS(issue_record).issue
                journal_files = JournalFiles(self.serial_path, issue.acron)
                issue_files = IssueFiles(journal_files, issue_label)
                ahead_manager = AheadManager(db_ahead, journal_files)
            else:
                self.msg.append('FATAL ERROR: This package is invalid. ' + str(len(issues)) + ' issues found: \n' + ', '.join(issues))

            if issue_record is not None:
                total_not_ex_aheads = []
                total_ex_aheads = []
                for xml_name, data in article_reports.items():
                    results, article = data
                    f, e, w = results

                    article_files = ArticleFiles(issue_files, article.order, xml_name)
                    article_title = article.title[0] if len(article.title) > 0 else article_files.xml_name

                    self.msg.append(article_title)
                    if self.convert_article(issue_record, article, article_files, f, e, w):
                        not_ex_aheads, ex_aheads = self.manage_ex_ahead(ahead_manager, article, article_files)
                        total_not_ex_aheads += not_ex_aheads
                        total_ex_aheads += ex_aheads

                if len(total_ex_aheads) > 0:
                    self.msg.append('ex-aheads')
                    self.msg.append('\n'.join(total_ex_aheads))
                    ahead_manager.update_db()
                db_article.finish_conversion(issue_files)
                self.copy_files_to_web(xml_path, issue_files, web_path)

    def convert_article(self, issue_record, article, article_files, fatal_errors, errors, warnings):
        display_statistic(fatal_errors, errors, warnings)

        if fatal_errors > 0:
            self.msg.append('FATAL ERROR: Unable to convert because it has fatal errors.')
        else:
            section_code = issue_record.check_section(article.toc_section)
            if section_code is None:
                self.msg.append(article.toc_section + ' is not a valid section.')
            #create_db = (create_db and article.number != 'ahead')

            db_article.create_id_file(issue_record, article, section_code, article_files)
        return (os.path.isfile(article_files.id_filename))

    def manage_ex_ahead(self, ahead_manager, article, article_files):
        if article.number != 'ahead':
            deleted = ahead_manager.manage_ex_ahead(article.doi, article_files.xml_name)
            if deleted is None:
                not_ex_aheads.append(article.title)
            else:
                ex_aheads.append(article.title)
        return (not_ex_aheads, ex_aheads)

    def copy_files_to_web(self, xml_files_path, issue_files, web_path):
        if os.path.isdir(web_path):
            path = {}
            path['pdf'] = web_path + '/bases/pdf/' + issue_files.acron_and_issue_folder
            path['html'] = web_path + '/htdocs/img/revistas/' + issue_files.acron_and_issue_folder + '/html/'
            path['xml'] = web_path + '/bases/xml/' + issue_files.acron_and_issue_folder
            path['img'] = web_path + '/htdocs/img/revistas/' + issue_files.acron_and_issue_folder
            for p in path.values():
                if not os.path.isdir(p):
                    os.makedirs(p)
            for f in os.listdir(xml_files_path):
                if os.path.isfile(xml_files_path + '/' + f):
                    ext = f[f.rfind('.'):]
                    if path.get(ext) is not None:
                        shutil.copy(xml_files_path + '/' + f, path[ext])
                    else:
                        shutil.copy(xml_files_path + '/' + f, path['img'])
        else:
            print('Invalid value for Web path. ')
            print(web_path)


def validate_path(path):
    xml_path = ''
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


def convert(path, acron, version):
    #FIXME
    xml_path, report_path, base_path, id_path = validate_path(path)
    if len(xml_files) == 0:
        print('There is nothing to convert.\n')
        print(path)
        print(' must be an XML file or a folder which contains XML files.')
    else:
        config = Configuration()
        curr_path = os.getcwd().replace('\\', '/')
        if os.path.isfile(curr_path + '/./../scielo_paths.ini'):
            config.read(curr_path + '/./../scielo_paths.ini')

            cisis = UCISIS(CISIS(curr_path + '/./../cfg/'), CISIS(curr_path + '/./../cfg/cisis1660/'))
            fst_filename = curr_path + '/./../convert/library/scielo/scielo.fst'

            serial_path = config.data.get('Serial Directory')
            db_issue_filename = config.data.get('Issue Database')
            db_issue = files_manager.IssueDAO(cisis, db_issue_filename)
            xml_converter = XMLConverter(db_issue, serial_path, AheadDAO(cisis, fst_filename))

            web_path = config.data.get('SCI_LISTA_SITE')
            print(web_path)
            if web_path is not None:
                web_path = web_path.replace('\\', '/')
                web_path = web_path[0:web_path.find('/proc/')]
            print(web_path)
            xml_converter.convert(xml_path, report_path, base_path, id_path, web_path)
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
        print(args)
    return (path, acron)


def call_convert(args, version):
    path, acron = read_inputs(args)
    if path is None:
        print(acron)
    else:
        convert(path, acron, version)
