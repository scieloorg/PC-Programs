import os
import shutil
import tempfile
from datetime import datetime

import isis
import isis_models


class DocFilesInfo(object):

    def __init__(self, xml_filename, report_path, wrk_path):
        self.xml_filename = xml_filename
        self.xml_path = os.path.dirname(xml_filename)

        xml_file = os.path.basename(xml_filename)
        self.xml_name = xml_file.replace('.sgm.xml', '').replace('.xml', '')
        self.new_name = self.xml_name

        self.xml_wrk_path = wrk_path + '/' + self.xml_name

        self.dtd_report_filename = report_path + '/' + self.xml_name + '.dtd.txt'
        self.style_report_filename = report_path + '/' + self.xml_name + '.rep.html'

        self.pmc_dtd_report_filename = report_path + '/' + self.xml_name + '.pmc.dtd.txt'
        self.pmc_style_report_filename = report_path + '/' + self.xml_name + '.pmc.rep.html'

        self.err_filename = report_path + '/' + self.xml_name + '.err.txt'
        self.html_filename = self.xml_wrk_path + '/' + self.xml_name + '.temp.htm'
        if not os.path.isfile(self.html_filename):
            self.html_filename += 'l'

        self.is_sgmxml = xml_filename.endswith('.sgm.xml')
        self.ctrl_filename = self.xml_wrk_path + '/' + self.xml_name + '.ctrl.txt' if self.is_sgmxml else None

    def clean(self):
        #clean_folder(self.xml_wrk_path)
        delete_files([self.err_filename, self.dtd_report_filename, self.style_report_filename, self.pmc_dtd_report_filename, self.pmc_style_report_filename, self.ctrl_filename])


def clean_folder(path):
    if os.path.isdir(path):
        for f in os.listdir(path):
            if os.path.isfile(path + '/' + f):
                os.unlink(path + '/' + f)
    else:
        os.makedirs(path)


def delete_files(files):
    for f in files:
        if f is not None:
            if os.path.isfile(f):
                os.unlink(f)


class Ahead(object):

    def __init__(self, record, ahead_db_name):
        self.record = record
        self.ahead_db_name = ahead_db_name

    @property
    def doi(self):
        return self.record.get('237')

    @property
    def filename(self):
        return self.record.get('2')

    @property
    def order(self):
        return self.record.get('121')


class AheadManager(object):

    def __init__(self, dao, journal_files, fst_filename):
        self.journal_files = journal_files
        self.fst_filename = fst_filename
        self.dao = dao
        self.load()
        self.deleted = {}

    def load(self):
        self.ahead_doi = {}
        self.ahead_filename = {}
        self.ahead_list = []
        for db_filename in self.journal_files.ahead_bases:
            h_records = self.h_records(db_filename)
            for h_record in h_records:
                ahead = Ahead(h_record, os.path.basename(db_filename))
                self.ahead_doi[ahead.doi] = len(self.ahead_list)
                self.ahead_filename[ahead.filename] = len(self.ahead_list)
                self.ahead_list.append(ahead)

    def h_records(self, db_filename):
        return self._select_h(self.dao.get_records(db_filename))

    def _select_h(self, records):
        return [rec for rec in records if rec.get('706') == 'h']

    def name(self, db_filename):
        return os.path.basename(db_filename)

    def find_ahead_data(self, doi, filename):
        data = None
        i = self.ahead_doi.get(doi, None)
        if i is None:
            i = self.ahead_filename.get(filename, None)
        if i is not None:
            data = self.ahead_list[i]
        return data

    def mark_ahead_as_deleted(self, ahead):
        """
        Mark as deleted
        """
        if not ahead.ahead_db_name is self.deleted.keys():
            self.deleted[ahead.ahead_db_name] = []
        self.deleted[ahead.ahead_db_name].append(ahead)

    def manage_ex_ahead_files(self, ahead):
        print('Exclude ahead record of ' + ahead.filename)
        year = ahead.ahead_db_name[0:4]

        ex_ahead_markup_path, ex_ahead_body_path, ex_ahead_base_path = self.journal_files.ex_ahead_paths(year)
        for path in [ex_ahead_markup_path, ex_ahead_body_path, ex_ahead_base_path]:
            if not os.path.isdir(path):
                os.makedirs(path)

        # move files to ex-ahead folder
        xml_file, markup_file, body_file = self.journal_files.ahead_xml_markup_body(year, ahead.filename)
        if os.path.isfile(markup_file):
            shutil.move(markup_file, ex_ahead_markup_path)
        if os.path.isfile(body_file):
            shutil.move(body_file, ex_ahead_body_path)
        if os.path.isfile(xml_file):
            shutil.move(xml_file, ex_ahead_markup_path)
        if os.path.isfile(self.journal_files.ahead_id_filename(year, ahead.order)):
            os.unlink(self.journal_files.ahead_id_filename(year, ahead.order))

    def save_ex_ahead_record(self, ahead):
        self.dao.append_records([ahead.record], self.journal_files.ahead_base('ex-' + ahead.ahead_db_name[0:4]))

    def manage_ex_ahead(self, doi, filename):
        """
        Exclude ISIS record of ahead database (serial)
        """
        ahead = self.find_ahead_data(doi, filename)
        if ahead is not None:
            self.mark_ahead_as_deleted(ahead)
            self.manage_ex_ahead_files(ahead)
            self.save_ex_ahead_record(ahead)
        return ahead

    def update_db(self):
        for ahead_db_name, ahead_list in self.deleted.items():
            excluded_filenames = [ahead.filename for ahead in ahead_list]

            ahead_db_filename = self.journal_files.ahead_base(ahead_db_name[0:4])
            ex_ahead_db_filename = self.journal_files.ahead_base('ex-' + ahead_db_name[0:4])

            records = self.dao.get_records(ahead_db_filename)
            records = [r for r in records if not r.get('2') in excluded_filenames]

            self.dao.save_records(records, ahead_db_filename, self.fst_filename)
            self.dao.update_indexes(ex_ahead_db_filename, self.fst_filename)


class ArticleFiles(object):

    def __init__(self, issue_files, order, xml_name):
        self.issue_files = issue_files
        self.order = order
        self.xml_name = xml_name

    @property
    def id_filename(self):
        return self.issue_files.id_path + self.order + '.id'

    @property
    def relative_xml_filename(self):
        return self.issue_files.acron_and_issue_folder + '/' + self.xml_name + '.xml'


class IssueFiles(object):

    def __init__(self, journal_files, issue_folder):
        self.journal_files = journal_files
        self.issue_folder = issue_folder

    @property
    def id_filename(self):
        return self.issue_path + '/id/i.id'

    @property
    def id_path(self):
        return self.issue_path + '/id/'

    @property
    def issue_path(self):
        return self.journal_files.journal_path + '/' + self.issue_folder

    @property
    def base(self):
        return self.issue_path + '/base/' + self.issue_folder

    @property
    def acron_and_issue_folder(self):
        return self.journal_files.acron + '/' + self.issue_folder

    @property
    def xml_path(self):
        return self.issue_path + '/xml_markup'


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


class IssueDAO(object):

    def __init__(self, dao, db_filename):
        self.dao = dao
        self.db_filename = db_filename

    def expr(self, issue_id, pissn, eissn, acron=None):
        _expr = []
        if pissn is not None:
            _expr.append(pissn + issue_id)
        if eissn is not None:
            _expr.append(eissn + issue_id)
        if acron is not None:
            _expr.append(acron)
        r = ' OR '.join(_expr) if len(_expr) > 0 else None
        return r

    def search(self, issue_label, pissn, eissn):
        expr = self.expr(issue_label, pissn, eissn)
        return self.dao.get_records(self.db_filename, expr)


class ArticleDAO(object):

    def __init__(self, cisis):
        self.cisis = cisis

    def create_id_file(self, i_record, article, section_code, article_files):
        if not os.path.isdir(article_files.id_path):
            os.makedirs(article_files.id_path)
        if not os.path.isdir(os.path.dirname(article_files.issue_files.base)):
            os.makedirs(os.path.dirname(article_files.issue_files.base))

        if article.order != '00000':
            article_isis = isis.ArticleISIS(article, i_record, section_code, article_files)

            id_file = isis.IDFile()
            id_file.save(article_files.id_filename, article_isis.records, 'utf-8')

        else:
            print('Invalid value for order.')

    def finish_conversion(self, issue_record, issue_files):
        id_file = isis.IDFile()
        id_file.save(issue_files.id_filename, [issue_record], 'iso-8859-1')
        self.cisis.id2i(issue_files.id_filename, issue_files.base)
        for f in os.listdir(issue_files.id_path):
            if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                self.cisis.id2mst(issue_files.id_path + '/' + f, issue_files.base, False)
