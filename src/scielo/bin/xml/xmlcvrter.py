# coding=utf-8

import os
from datetime import datetime

from modules.utils import load_xml
from modules.isis import IDFile
from modules.article import Article
from modules.isis_models import ArticleISIS


class XMLConverter(object):

    def __init__(self, cisis, serial_path):
        self.cisis = cisis
        self.serial_path = serial_path
        self.issue_manager = IssuesManager(self.cisis, self.serial_path + '/issue/issue')
        self.issue_manager.load_data()
        self.article_db = ArticleDB(self.cisis)

    def convert(self, xml_files_path, acron):
        journal_files = JournalFiles(self.serial_path, acron)
        ahead_manager = AheadManager(self.cisis, journal_files)

        for xml_file in os.listdir(xml_files_path):
            article = Article(load_xml(xml_files_path + '/' + xml_file))
            text_or_article = 'article'

            issue = Issue(self.issue_manager.record(acron, article.volume, article.number, article.volume_suppl, article.number_suppl))
            section_code = issue.section_code(article.toc_section)

            article_files = ArticleFiles(journal_files, article, xml_file)

            self.article_db.save_article(article, section_code, text_or_article, article_files)
            ahead_manager.exclude_ahead_file(article.doi)

        ahead_manager.update_ahead_database()


class IssuesManager(object):

    def __init__(self, cisis, issue_filename):
        self.issue_filename = issue_filename
        self.cisis = cisis
        self.records = {}

    def load_data(self):
        id_filename = self.issue_filename + '.id'
        base = self.issue_filename

        self.cisis.mst2id(base, id_filename)

        for rec in IDFile().read(id_filename):
            key = self._key(rec.get('930', ''), rec.get('31', ''), rec.get('32', ''), rec.get('131', ''), rec.get('132', ''))
            self.records[key] = rec

    def _key(self, acron, volume, number, volume_suppl, number_suppl):
        return '-'.join([acron, volume, volume_suppl, number, number_suppl])

    def record(self, acron, volume, number, volume_suppl, number_suppl):
        return self.records.get(self._key(acron, volume, number, volume_suppl, number_suppl))


class Issue(object):
    def __init__(self, record):
        self.record = record

    def section_code(self, section_title):
        seccode = None
        for sec in self.record.get('49', []):
            if sec.get('t') == section_title:
                seccode = sec.get('c')
        return seccode


class AheadManager(object):

    def __init__(self, cisis, journal_files):
        self.journal_files = journal_files
        self.cisis = cisis
        self.ahead_lists = {}
        self.records = {}
        self.deleted_base = []

    def load_data(self):
        for base in self.journal_files.ahead_bases:
            id_filename = base + '.id'
            self.cisis.mst2id(base, id_filename)
            records = IDFile().read(id_filename)
            rec_index = 0
            doi = None
            start = 0
            xml_file = None
            for rec in records:
                rec_index += 1
                if rec.get('706') == 'o':
                    if rec_index != 1:
                        if doi is not None:
                            self.ahead_lists[doi] = (base, xml_file, start, rec_index-1)
                    start = rec_index
                elif rec.get('706') == 'h':
                    doi = rec.get('237')
                    xml_file = rec.get('702')
            if doi is not None:
                self.ahead_lists[doi] = (base, xml_file, start, rec_index)
            self.records[base] = records

    def exclude_ahead_file(self, doi):
        base, xml_file, start, end = self.ahead_lists[doi]
        for i in range(start, end+1):
            self.records[base][i] = None
        self.deleted_base.append(base)
        self.deleted_base = list(set(self.deleted_base))

    def update_ahead_database(self):
        for base in self.deleted_base:
            IDFile().save(base + '.id', self.records[base])
            self.cisis.id2i(base + '.id', base)


class ArticleDB(object):

    def __init__(self, cisis):
        self.cisis = cisis

    def save_article(self, article, section_code, text_or_article, article_files, new=False):
        if new:
            self.cisis.id2mst(os.path.dirname(article_files.id_filename) + '/i.id', article_files.base, True)

        article_isis = ArticleISIS(article, section_code, text_or_article, article_files)

        id_file = IDFile()
        id_file.save(article_files.id_filename, article_isis.records)
        self._append(os.path.dirname(article_files.id_filename), article_files.base)

    def _append(self, id_path, base_filename):
        if os.path.exists(base_filename + '.mst'):
            os.unlink(base_filename + '.mst')
            os.unlink(base_filename + '.xrf')
        #FIXME
        for id_file in os.listdir(id_path):
            if id_file != 'i.id' and id_file != '00000.id':
                self.cisis.id2mst(id_path + '/' + id_file, base_filename, False)


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
        return self.journal_files.serial_path + '/' + self.journal_files.acron + '/' + self.issue_folder + '/id/' + self.xml_name + '.id'

    @property
    def relative_xml_filename(self):
        return 'xml/' + self.journal_files.acron + '/' + self.issue_folder + '/' + self.xml_name


class JournalFiles(object):

    def __init__(self, serial_path, acron):
        self.acron = acron
        self.serial_path = serial_path
        self.years = [datetime.now().isoformat()[0:4]+1 - y for y in range(0, 5)]

    def ahead_base(self, year):
        return self.serial_path + '/' + self.acron + '/' + year + 'nahead' + '/base/' + year + 'nahead'

    @property
    def ahead_bases(self):
        bases = []
        for y in self.years:
            if os.path.isfile(self.ahead_base(y) + '.mst'):
                bases.append(self.ahead_base(y))
        return bases
