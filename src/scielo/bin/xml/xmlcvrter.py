# coding=utf-8

from modules import utils
from modules import isis
from modules.article import Article
from modules.isis_models import ArticleISIS


class Issue(object):

    def __init__(self, sections):
        self.sections = [{'title': 'nd'}]

    def section_code(self, section_title):
        r = [section.get('code') for section in self.sections if section.get('title') == section_title]
        return r[0] if len(r) > 0 else None


class XMLConverter(object):

    def __init__(self, dbmanager, serial_path):
        self.dbmanager = dbmanager
        self.serial_path = serial_path

    def convert(self, xml_files_path, acron):

        for xml_file in os.listdir(xml_files_path):
            article = Article(load_xml(xml_files_path + '/' + xml_file))

            issue = IssueISISDB(article)
            section_code = issue.section_code(article.toc_section)

            files_info = FilesInfo(self.serial_path, article, acron, xml_file)

            text_or_article = 'article'

            self.dbmanager.save(article, section_code, text_or_article, files_info)
            self.dbmanager.exclude_ahead(article)


class DBManager(object):

    def __init__(self, cisis):
        self.cisis = cisis

    def save(self, article, section_code, text_or_article, files_info):
        article_isis = ArticleISIS(article, section_code, text_or_article, files_info)

        id_file = IDFile()
        id_file.save(id_filename, article_isis.records)
        self.exclude_ahead(article)
        self.id2mst(os.path.dirname(id_filename), files_info.base)

    def id2mst(self, id_path, base_filename):
        if os.path.exists(base_filename + '.mst'):
            os.unlink(base_filename + '.mst')
            os.unlink(base_filename + '.xrf')
        #FIXME
        if os.path.isfile(id_path + '/i.id'):
            self.cisis.id2mst(id_path + '/i.id', base_filename, False)
        for id_file in os.listdir(id_path):
            if id_file != 'i.id' and id_file != '00000.id':
                self.cisis.id2mst(id_path + '/' + id_file, base_filename, False)

    def exclude_ahead(self, article):
        if article.ahpdate and article.number != 'ahead':
            # ex-ahead?


    def find_ahead(self, doi, ahead_bases):
        for base in ahead_bases:
            article_base = Base(base)
            article = article_base.article


class Base(object):

    def __init__(self, base):
        self.base = base

    @property
    def article(self):
        return ''


class FilesInfo(object):

    def __init__(self, serial_path, article, acron, xml_name):
        self.article = article
        self.acron = acron
        self.serial_path = serial_path
        self.years = [datetime.now().isoformat()[0:4]+1 - y for y in range(0, 5)]
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

    def ahead_base(self, year):
        return self.serial_path + '/' + self.acron + '/' + year + 'nahead' + '/base/' + self.issue_folder

    @property
    def base(self):
        return self.serial_path + '/' + self.acron + '/' + self.issue_folder + '/base/' + self.issue_folder

    @property
    def id_filename(self):
        return self.serial_path + '/' + self.acron + '/' + self.issue_folder + '/id/' + self.xml_name + '.id'

    @property
    def ahead_bases(self):
        bases = []
        for y in self.years:
            if os.path.isfile(self.ahead_base(y) + '.mst'):
                bases.append(self.ahead_base(y))
        return bases

    @property
    def relative_xml_filename(self):
        return 'xml/' + self.acron + '/' + self.issue_folder + '/' + self.xml_filename

