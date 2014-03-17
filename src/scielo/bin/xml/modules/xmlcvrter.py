# coding=utf-8

import os
import shutil
from datetime import datetime

from configuration import Configuration
from utils import load_xml
from isis import IDFile, CISIS
from article import Article
from isis_models import ArticleISIS, IssueISIS


class XMLConverter(object):

    def __init__(self, cisis, serial_path):
        self.cisis = cisis
        self.serial_path = serial_path
        self.issue_manager = IssuesManager(self.cisis, self.serial_path + '/issue/issue')
        #self.issue_manager.load_data()
        self.article_db = ArticleDB(self.cisis)

    def convert(self, xml_files_path, acron):
        journal_files = JournalFiles(self.serial_path, acron)

        ahead_manager = AheadManager(self.cisis, journal_files)
        ahead_manager.generate_indexes()

        issue_folder = None
        issue_record = None
        issue_files = None
        issue = None
        create_db = True

        for xml_file in os.listdir(xml_files_path):
            if os.path.isfile(xml_files_path + '/' + xml_file) and xml_file.endswith('.xml'):
                text_or_article = 'article'

                article = Article(load_xml(xml_files_path + '/' + xml_file))

                if article.tree is None:
                    print('Unable to load ' + xml_file)
                else:
                    article_files = ArticleFiles(journal_files, article, xml_file)

                    if issue_folder is None:
                        print('issue: ' + article_files.issue_folder)
                        issue_files = ArticleFiles(journal_files, article, xml_file)

                        issue_folder = article_files.issue_folder
                        # load issues record
                        self.issue_manager.load_selected_issues(article.journal_issns.get('epub'), article.journal_issns.get('ppub'), acron, article_files.issue_folder)

                        issue_record = self.issue_manager.record(acron, article.volume, article.number, article.volume_suppl, article.number_suppl)

                    print(xml_file)

                    if issue_record is None:
                        print(article_files.issue_folder + ' is not registered in issue database.')
                    else:
                        if issue_folder == article_files.issue_folder:
                            issue = IssueISIS(issue_record)
                            section_code = issue.section_code(article.toc_section)

                            #create_db = (create_db and article.number != 'ahead')
                            self.article_db.create_id_file(article_files, article, section_code, text_or_article, issue.record, create_db)

                            if article.number != 'ahead' and article.ahpdate is not None:
                                ahead_manager.exclude_ahead_record(article, xml_file)
                            create_db = False
                        else:
                            print('This article do not belongs to ' + issue_folder + '.\n It belongs to ' + article_files.issue_folder)
                    if xml_files_path != issue_files.xml_path:
                        if not os.path.isdir(issue_files.xml_path):
                            os.makedirs(issue_files.xml_path)
                        shutil.copy(xml_files_path + '/' + xml_file, issue_files.xml_path)
        if issue is not None:
            id_file = IDFile()
            id_file.save(issue_files.id_path + '/i.id', [issue.record])
            self.cisis.id2i(issue_files.id_path + '/i.id', issue_files.base)
            for f in os.listdir(issue_files.id_path):
                if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                    self.cisis.id2mst(issue_files.id_path + '/' + f, issue_files.base, False)


class IssuesManager(object):

    def __init__(self, cisis, issue_filename):
        self.issue_filename = issue_filename
        self.cisis = cisis
        self.records = {}

        import tempfile
        self.temp_dir = tempfile.mkdtemp()

    def load_all(self):
        id_filename = self.issue_filename + '.id'
        base = self.issue_filename

        self.cisis.i2id(base, id_filename)
        records = IDFile().read(id_filename)
        for rec in records:
            key = self._key(rec.get('930'), rec.get('31'), rec.get('32'), rec.get('131'), rec.get('132'))
            self.records[key] = rec

    def search(self, expr, issue_folder):
        temp_issue_db = self.temp_dir + '/' + issue_folder
        self.cisis.search(self.issue_filename, expr, temp_issue_db)
        temp_issue_id_file = temp_issue_db + '.id'
        self.cisis.i2id(temp_issue_db, temp_issue_id_file)

        return IDFile().read(temp_issue_id_file)

    def load_selected_issues(self, pissn, eissn, acron, issue_folder):
        expr = []

        if pissn is not None:
            expr.append(pissn + issue_folder)
        if eissn is not None:
            expr.append(eissn + issue_folder)

        records = self.search(' OR '.join(expr), issue_folder)
        if len(records) == 0:
            records = self.search(acron, issue_folder)

        for rec in records:
            key = self._key(rec.get('930'), rec.get('31'), rec.get('32'), rec.get('131'), rec.get('132'))
            self.records[key] = rec

    def _key(self, acron, volume, number, volume_suppl, number_suppl):
        i = [acron, volume, number, volume_suppl, number_suppl]
        i = [item if item is not None else '' for item in i]
        s = '-'.join(i)
        return s.lower()

    def record(self, acron, volume, number, volume_suppl, number_suppl):
        return self.records.get(self._key(acron, volume, number, volume_suppl, number_suppl))


class AheadManager(object):

    def __init__(self, cisis, journal_files):
        import tempfile
        self.journal_files = journal_files
        self.cisis = cisis
        self.temp_dir = tempfile.mkdtemp()

    @property
    def _all_aheads(self):
        return self.temp_dir + '/ahead'

    @property
    def fst_filename(self):
        f = open(self.temp_dir + '/ahead.fst', 'w')
        f.write("1 0 if v706='h' then v237/,v702/, fi")
        f.close()
        return self.temp_dir + '/ahead.fst'

    @property
    def _selected_record(self):
        return self.temp_dir + '/selected'

    @property
    def _id_filename(self):
        return self.temp_dir + '/selected.id'

    def generate_indexes(self):
        """
        Join all the journal ahead db which are in serial
        and generate the indexes
        """
        if len(self.journal_files.ahead_bases) > 0:
            self.cisis.new(self._all_aheads)
            for base in self.journal_files.ahead_bases:
                self.cisis.append(base, self._all_aheads)
            self.cisis.generate_indexes(self._all_aheads, self.fst_filename, self._all_aheads)

    def find_ahead_record(self, article_key):
        """
        Find ahead records, given a DOI
        """
        filename = None
        year = None
        rec = None
        order = None
        if len(self.journal_files.ahead_bases) > 0:
            self.cisis.search(self._all_aheads, article_key, self._selected_record)
            self.cisis.i2id(self._selected_record, self._id_filename)
            records = IDFile().read(self._id_filename)
            if len(records) > 4:
                rec = records[1]
                order = rec.get('121')
                filename = rec.get('702')
                year = rec.get('223')
                if year is not None:
                    year = year[0:4]
        return (rec, filename, order, year)

    def exclude_ahead_record(self, article, filename):
        """
        Exclude ISIS record of ahead database (serial)
        """
        if len(self.journal_files.ahead_bases) > 0:
            if filename.endswith('.xml'):
                rec, filename, order, year = self.find_ahead_record(article.doi)
            else:
                rec, filename, order, year = self.find_ahead_record(filename)
            if rec is not None:
                if year is not None and filename is not None:
                    print('Exclude ahead record of ' + filename)
                    self.exclude_records_by_filename(year, filename)

                    ex_ahead_markup_path, ex_ahead_body_path, ex_ahead_base_path = self.journal_files.ex_ahead_paths(year)
                    for path in [ex_ahead_markup_path, ex_ahead_body_path, ex_ahead_base_path]:
                        if not os.path.isdir(path):
                            os.makedirs(path)

                    # move files to ex-ahead folder
                    xml_file, markup_file, body_file = self.journal_files.ahead_xml_markup_body(year, filename)
                    if os.path.isfile(markup_file):
                        shutil.move(markup_file, ex_ahead_markup_path)
                    if os.path.isfile(body_file):
                        shutil.move(body_file, ex_ahead_body_path)
                    if os.path.isfile(xml_file):
                        shutil.move(xml_file, ex_ahead_markup_path)
                    if os.path.isfile(self.journal_files.ahead_id_filename(year, order)):
                        os.unlink(self.journal_files.ahead_id_filename(year, order))

                    # update ex-ahead base with the h record of ahead version
                    id_temp = self.temp_dir + '/exahead.id'
                    IDFile().save(id_temp, [rec])
                    self.cisis.id2mst(id_temp, self.journal_files.ahead_base('ex-' + year))

    def exclude_records_by_filename(self, year, filename):
        print('Exclude ahead record of ' + filename)
        base = self.journal_files.ahead_base(year)
        self.cisis.modify_record(base, "if v702='" + filename + "' then 'd*' fi")
        self.cisis.generate_indexes(base, base + '.fst', base)


class ArticleDB(object):

    def __init__(self, cisis):
        self.cisis = cisis

    def create_id_file(self, article_files, article, section_code, text_or_article, i_record, create_db=False):
        if not os.path.isdir(article_files.id_path):
                os.makedirs(article_files.id_path)
        if not os.path.isdir(os.path.dirname(article_files.base)):
            os.makedirs(os.path.dirname(article_files.base))

        if article.order != '00000':
            article_isis = ArticleISIS(article_files, article, i_record, section_code, text_or_article)

            id_file = IDFile()
            id_file.save(article_files.id_filename, article_isis.records)
        
        else:
            print('Invalid value for order.')


class ArticleFiles(object):

    def __init__(self, journal_files, article, xml_name):
        self.journal_files = journal_files
        self.article = article
        self.xml_name = xml_name

    @property
    def issue_folder(self):
        s = ''
        if self.article.volume is not None:
            s += 'v' + self.article.volume
        if self.article.volume_suppl is not None:
            s += 's' + self.article.volume_suppl
        if self.article.number is not None:
            s += 'n' + self.article.number
        if self.article.number_suppl is not None:
            s += 's' + self.article.number_suppl
        return s

    @property
    def base(self):
        return self.journal_files.journal_path + '/' + self.issue_folder + '/base/' + self.issue_folder

    @property
    def id_filename(self):
        return self.id_path + self.article.order + '.id'

    @property
    def id_path(self):
        return self.journal_files.journal_path + '/' + self.issue_folder + '/id/'

    @property
    def relative_xml_filename(self):
        return self.journal_files.acron + '/' + self.issue_folder + '/' + self.xml_name

    @property
    def xml_path(self):
        return self.journal_files.journal_path + '/' + self.issue_folder + '/xml_markup'

class JournalFiles(object):

    def __init__(self, serial_path, acron):
        self.acron = acron
        self.journal_path = serial_path + '/' + acron
        self.years = [str(int(datetime.now().isoformat()[0:4])+1 - y) for y in range(0, 5)]

    def ahead_base(self, year):
        return self.journal_path + '/' + year + 'nahead' + '/base/' + year + 'nahead'

    def ahead_xml_markup_body(self, year, filename):
        m = self.journal_path + '/' + year + 'nahead' + '/markup/' + filename
        b = self.journal_path + '/' + year + 'nahead' + '/body/' + filename
        return (self.journal_path + '/' + year + 'nahead' + '/xml/' + filename, m, b)

    def ahead_id_filename(self, year, order):
        order = '00000' + order
        order = order[-5:]
        return self.journal_path + '/' + year + 'nahead' + '/id/' + order + '.id'

    def ex_ahead_paths(self, year):
        path = self.journal_path + '/ex-' + year + 'nahead'
        m = path + '/markup/'
        b = path + '/body/'
        base = path + '/base/'
        return (m, b, base)

    @property
    def ahead_bases(self):
        bases = []
        for y in self.years:
            if os.path.isfile(self.ahead_base(y) + '.mst'):
                bases.append(self.ahead_base(y))
        return bases


def check_inputs(args):
    args = [arg.replace('\\', '/') for arg in args]
    script_name = args[0] if len(args) > 0 else ''
    r = False

    src = ''
    acron = ''
    message = ''

    if len(args) == 3:
        ign, src, acron = args
        r = os.path.isdir(src) and len([f for f in os.listdir(src) if f.endswith('.xml')]) > 0

    if not r:
        messages = []
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python converter <src> <acron>')
        messages.append('where:')
        messages.append('  <src> = path which contains XML files')
        messages.append('  <acron> = journal acronym')
        message = '\n'.join(messages)
        print(args)
    return (r, src, acron, message)


def convert(args):
    def curr_path():
        return os.getcwd().replace('\\', '/')

    r, xml_path, acron, message = check_inputs(args)
    if r:
        config = Configuration()
        print(curr_path() + '/./../cfg/')
        config.read(curr_path() + '/./../scielo_paths.ini')
        xml_converter = XMLConverter(CISIS(curr_path() + '/./../cfg/'), config.data['Serial Directory'])
        xml_converter.convert(xml_path, acron)
    else:
        print(message)
