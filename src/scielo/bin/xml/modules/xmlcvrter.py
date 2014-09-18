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


class Issue(object):

    def __init__(self):
        pass


class XMLConverter(object):

    def __init__(self, db_issue):
        self.db_issue = db_issue
        self.msg = []

    def get_issue_record(self, issue_label, article_reports):
        issue_record = None
        for xml_name, data in article_reports.items():
            results, article = data
            issue_schema = files_manager.IssueSchema(None, issue_label, article.print_issn, article.e_issn)
            records = self.db_issue.select_records(issue_schema.expr())
            issue_records = files_manager.Records()
            issue_records.load_records(records)
            issue_records.index_records(issue_schema)
            if len(issue_records.records) == 1:
                issue_record = issue_records.records[0]
            if issue_record is not None:
                break
        return issue_record

    def get_issue(self, issue_record):
        issue = Issue()
        issue.dateiso = issue_record.get('65')
        issue.volume = issue_record.get('31')
        issue.number = issue_record.get('32')
        issue.volume_suppl = issue_record.get('131')
        issue.volume_suppl = issue_record.get('132')
        issue.acron = issue_record.get('930').lower()
        return issue

    def display_statistic(self, f, e, w):
        self.msg.append('fatal errors: ' + str(len(f)))
        self.msg.append('errors: ' + str(len(e)))
        self.msg.append('warnings: ' + str(len(w)))

    def convert(self, xml_path, report_path, base_path, id_path, web_path):
        xml_names = {f.replace('.xml', ''):f.replace('.xml', '') for f in os.listdir(xml_path) if f.endswith('.xml')}

        toc_statistic, article_reports, issues = reports.generate_package_reports(xml_path, xml_names, report_path)
        toc_f, toc_e, toc_w = toc_statistic

        self.msg.append('Validations reports in ' + report_path)
        display_statistic(toc_f, toc_e, toc_w)

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
                issue_isis = IssueISIS(issue_record)
                db_article = ArticleDB(issue_record)
                issue = get_issue(issue_record)
                issue_files = IssueFiles(JournalFiles(serial_path, issue.acron), issue_label)
            else:
                self.msg.append('FATAL ERROR: This package is invalid. Issues found in it: ' + ', '.join(issues))

            if issue_record is not None:
                for xml_name, data in article_reports.items():
                    results, article = data
                    f, e, w = results

                    article_files = ArticleFiles(issue_files, article.order, xml_name)
                    article_title = article.title[0] if len(article.title) > 0 else article_files.xml_name

                    self.msg.append(article_title)
                    if self.convert_article(db_issue, db_article, article_files, article, f, e, w):
                        self.handle_ahead(article, article_files)

    def convert_article(self, db_issue, db_article, article_files, article, fatal_errors, errors, warnings):
        display_statistic(fatal_errors, errors, warnings)

        if fatal_errors > 0:
            self.msg.append('FATAL ERROR: Unable to convert because it has fatal errors.')
        else:
            section_code = db_issue.check_section(article.toc_section)
            if section_code is None:
                self.msg.append(article.toc_section + ' is not a valid section.')
            #create_db = (create_db and article.number != 'ahead')

            db_article.create_id_file(article, section_code, article_files)
        return (os.path.isfile(article_files.id_filename))

    def handle_ahead(self, article, article_files):
        if article.number != 'ahead':
            deleted = ahead_manager.exclude_ahead_record(article, article_files.xml_name)
            if deleted is None:
                not_ex_aheads.append(article_title)
            else:
                ex_aheads.append(article_title)
        return (not_ex_aheads, ex_aheads)

    def __convert(self, xml_files_path, acron, web_path):
        journal_files = JournalFiles(self.serial_path, acron)

        ahead_manager = AheadManager(self.cisis, journal_files, self.fst_filename)

        issue, issue_files = self.create_article_id_files(xml_files_path, journal_files, ahead_manager)
        ahead_manager.update_db()
        self.create_db(issue, issue_files)
        self.copy_files_to_web(xml_files_path, issue_files, web_path)

    def create_article_id_files(self, xml_files_path, journal_files, ahead_manager):
        issue_folder = None
        issue_record = None
        issue_files = None
        issue = None
        create_db = True
        ex_aheads = []
        not_ex_aheads = []

        for xml_file in os.listdir(xml_files_path):
            if os.path.isfile(xml_files_path + '/' + xml_file) and xml_file.endswith('.xml'):
                text_or_article = 'article'

                article = Article(load_xml(xml_files_path + '/' + xml_file))

                if article.tree is None:
                    print('ERROR: Unable to load ' + xml_file)
                else:
                    article_files = ArticleFiles(journal_files, article, xml_file)

                    # dados do fasciculo
                    if issue_folder is None:
                        print('=' * 10)
                        print('issue: ' + article_files.issue_folder)
                        print('=' * 10)
                        issue_files = ArticleFiles(journal_files, article, xml_file)
                        issue_folder = article_files.issue_folder
                        self.issue_manager.load_selected_issues(article.journal_issns.get('epub'), article.journal_issns.get('ppub'), journal_files.acron, article_files.issue_folder)
                        issue_record = self.issue_manager.record(journal_files.acron, article.volume, article.number, article.volume_suppl, article.number_suppl)

                    print('-' * 10)
                    print(xml_file + '\n')

                    if issue_record is None:
                        print('ERROR: ' + article_files.issue_folder + ' is not registered in issue database.')
                    else:
                        if issue_folder == article_files.issue_folder:
                            issue = IssueISIS(issue_record)
                            section_code = issue.section_code(article.toc_section)

                            article_title = article.titles[0].get('article-title', '')
                            print(article_title)

                            #create_db = (create_db and article.number != 'ahead')
                            self.article_db.create_id_file(article_files, article, section_code, text_or_article, issue.record, create_db)
                            if article.number != 'ahead':
                                deleted = ahead_manager.exclude_ahead_record(article, xml_file)
                                if deleted is None:
                                    not_ex_aheads.append(article_title)
                                else:
                                    ex_aheads.append(article_title)

                            create_db = False
                        else:
                            print('ERROR: This article does not belong to ' + issue_folder + '.\n It belongs to ' + article_files.issue_folder)

                    #if xml_files_path != issue_files.xml_path:
                    #    if not os.path.isdir(issue_files.xml_path):
                    #        os.makedirs(issue_files.xml_path)
                    #    shutil.copy(xml_files_path + '/' + xml_file, issue_files.xml_path)

        if len(ex_aheads) > 0:
            print('ex-aheads')
            print('\n'.join(ex_aheads))

        return (issue, issue_files)

    def create_db(self, issue, issue_files):
        if issue is not None:
            id_file = IDFile()
            id_file.save(issue_files.id_path + '/i.id', [issue.record], 'iso-8859-1')
            self.cisis.id2i(issue_files.id_path + '/i.id', issue_files.base)
            for f in os.listdir(issue_files.id_path):
                if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                    self.cisis.id2mst(issue_files.id_path + '/' + f, issue_files.base, False)

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

            db_issue_filename = config.data.get('Issue Database')
            db_issue = files_manager.DB(cisis, db_issue_filename)
            xml_converter = XMLConverter(db_issue)

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
