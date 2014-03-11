# coding=utf-8

import os
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

        create_i_id = True

        for xml_file in os.listdir(xml_files_path):
            if os.path.isfile(xml_files_path + '/' + xml_file):
                print(xml_files_path + '/' + xml_file)
                text_or_article = 'article'

                article = Article(load_xml(xml_files_path + '/' + xml_file))
                article_files = ArticleFiles(journal_files, article, xml_file)

                # load issues record
                self.issue_manager.load_selected_issues(article.journal_issns.get('epub', article.journal_issns.get('ppub', '')), acron, article_files.issue_folder)

                issue_record = self.issue_manager.record(acron, article.volume, article.number, article.volume_suppl, article.number_suppl)
                if issue_record is None:
                    print(self.issue_manager._key(acron, article.volume, article.number, article.volume_suppl, article.number_suppl))
                    print(sorted(self.issue_manager.records.keys()))
                else:
                    issue = IssueISIS(issue_record)
                    section_code = issue.section_code(article.toc_section)
                    print('section code: ')
                    print(section_code)

                    print(article_files.base)
                    if create_i_id:
                        i_record = issue.record
                    else:
                        i_record = None

                    self.article_db.save_article(article_files, article, section_code, text_or_article, i_record)
                    ahead_manager.exclude_ahead_record(article.doi)
                    create_i_id = False


class IssuesManager(object):

    def __init__(self, cisis, issue_filename):
        self.issue_filename = issue_filename
        self.cisis = cisis
        self.records = {}

    def load_all(self):
        id_filename = self.issue_filename + '.id'
        base = self.issue_filename

        self.cisis.i2id(base, id_filename)
        records = IDFile().read(id_filename)
        for rec in records:
            key = self._key(rec.get('930'), rec.get('31'), rec.get('32'), rec.get('131'), rec.get('132'))
            self.records[key] = rec

    def load_selected_issues(self, issn, acron, issue_folder):
        self.selected_issue_db = self.issue_filename + '_' + acron + issue_folder
        self.cisis.search(self.issue_filename, issn + issue_folder + ' OR ' + acron, self.selected_issue_db)
        self.selected_issue_id_file = self.selected_issue_db + '.id'
        self.cisis.i2id(self.selected_issue_db, self.selected_issue_id_file)

        records = IDFile().read(self.selected_issue_id_file)
        for rec in records:
            key = self._key(rec.get('930'), rec.get('31'), rec.get('32'), rec.get('131'), rec.get('132'))
            self.records[key] = rec

    def _key(self, acron, volume, number, volume_suppl, number_suppl):
        i = [acron, volume, volume_suppl, number, number_suppl]
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
        f.write("1 0 if v706='h' then v237/ fi")
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

    def find_ahead_record(self, doi):
        """
        Find ahead records, given a DOI
        """
        xml_file = None
        year = None

        if os.path.isfile(self._all_aheads + '.mst'):
            self.cisis.search(self._all_aheads, doi, self._selected_record)
            self.cisis.i2id(self._selected_record, self._id_filename)
            records = IDFile().read(self._id_filename)
            for rec in records:
                xml_file = rec.get('702')
                year = rec.get('223')
                if year is not None:
                    year = year[0:4]

        else:
            print('This journal has no ahead articles.')

        return (xml_file, year)

    def exclude_ahead_record(self, doi):
        """
        Exclude ISIS record of ahead database (serial)
        """
        filename, year = self.find_ahead_record(doi)
        if filename is not None:
            if year is not None:
                print('Exclude ahead record of ' + filename)
                base = self.journal_files.ahead_base(year)
                self.cisis.modify_record(base, "if v702='" + filename + "' then 'd*' fi")
                self.cisis.generate_indexes(base, base + '.fst', base)


class ArticleDB(object):

    def __init__(self, cisis):
        self.cisis = cisis

    def save_article(self, article_files, article, section_code, text_or_article, i_record=None):
        if i_record is not None:
            print(article_files.id_path)
            if not os.path.isdir(article_files.id_path):
                os.makedirs(article_files.id_path)

            for item in os.listdir(article_files.id_path):
                os.unlink(article_files.id_path + '/' + item)
            id_file = IDFile()
            id_file.save(article_files.id_path + '/i.id', [i_record])

            if not os.path.isdir(os.path.dirname(article_files.base)):
                os.makedirs(os.path.dirname(article_files.base))
            self.cisis.id2mst(article_files.id_path + '/i.id', article_files.base, True)

        article_isis = ArticleISIS(article_files, article, section_code, text_or_article)

        id_file = IDFile()
        id_file.save(article_files.id_filename, article_isis.records)
        print(article_files.id_filename)
        print(article_files.base)
        self.cisis.id2mst(article_files.id_filename, article_files.base, False)


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
        return self.journal_files.serial_path + '/' + self.journal_files.acron + '/' + self.issue_folder + '/base/' + self.issue_folder

    @property
    def id_filename(self):
        return self.id_path + self.xml_name + '.id'

    @property
    def id_path(self):
        return self.journal_files.serial_path + '/' + self.journal_files.acron + '/' + self.issue_folder + '/id/'

    @property
    def relative_xml_filename(self):
        return 'xml/' + self.journal_files.acron + '/' + self.issue_folder + '/' + self.xml_name


class JournalFiles(object):

    def __init__(self, serial_path, acron):
        self.acron = acron
        self.serial_path = serial_path
        self.years = [str(int(datetime.now().isoformat()[0:4])+1 - y) for y in range(0, 5)]

    def ahead_base(self, year):
        return self.serial_path + '/' + self.acron + '/' + year + 'nahead' + '/base/' + year + 'nahead'

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
        messages.append('python ' + script_name + ' <src> <acron>')
        messages.append('where:')
        messages.append('  <src> = path which contains XML files')
        messages.append('  <acron> = journal acronym')
        message = '\n'.join(messages)
    return (r, src, acron, message)


def convert(args, cisis_path, serial_path):
    
    r, xml_path, acron, message = check_inputs(args)
    if r:
        xml_converter = XMLConverter(CISIS(cisis_path), serial_path)
        xml_converter.convert(xml_path, acron)
    else:
        print(message)
