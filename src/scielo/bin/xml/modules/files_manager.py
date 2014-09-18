import os
import shutil
import tempfile
from datetime import datetime

import isis


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


class SerialFolder(object):

    def __init__(self, serial_path):
        self.issue_db_filename = serial_path + '/issue/issue'
        self.title_db_filename = serial_path + '/title/title'
        self.serial_path = serial_path


class DB(object):

    def __init__(self, cisis, db_filename):
        self.cisis = cisis
        self.db_filename = db_filename

    def select_records(self, expr=None):
        temp_filename = None
        if expr is None:
            base = self.db_filename
        else:
            temp_filename = tempfile.NamedTemporaryFile(delete=False)
            base = temp_filename
            self.cisis.search(self.db_filename, expr, base)
        id_filename = base + '.id'
        self.cisis.i2id(base, id_filename)
        r = isis.IDFile().read(base)
        if temp_filename is not None:
            os.unlink(temp_filename)
        return r


class Records(object):

    def __init__(self):
        self.records = []
        self.indexed = {}

    def index_records(self, db_schema):
        self.indexed = {}
        for rec in self.records:
            self.indexed[db_schema.key(rec)] = rec

    def get_record(self, key):
        return self.indexed.get(key, None)

    def load_records(self, records):
        self.records = records


class IssueSchema(object):

    def __init__(self, acron, issue_id, pissn, eissn):
        self.acron = acron
        self.issue_id = issue_id
        self.pissn = pissn
        self.eissn = eissn

    def expr(self):
        _expr = []
        if self.pissn is not None:
            _expr.append(self.pissn + self.issue_id)
        if self.eissn is not None:
            _expr.append(self.eissn + self.issue_id)
        if self.acron is not None:
            _expr.append(self.acron)
        r = ' OR '.join(_expr) if len(_expr) > 0 else None
        return r

    def key(self, rec):
        return self.generate_key(rec.get('930'), rec.get('65')[0:4], rec.get('31'), rec.get('32'), rec.get('131'), rec.get('132'), rec.get('41'))

    def generate_key(self, acron, year, volume, number, volume_suppl, number_suppl, complement):
        i = [acron, year, volume, number, volume_suppl, number_suppl, complement]
        i = [item if item is not None else '' for item in i]
        s = '-'.join(i)
        return s.lower()

    def index_records(self, records):
        _records = {}
        for rec in records:
            _records[self._key(rec)] = rec
        return _records


class AheadManager(object):

    def __init__(self, cisis, journal_files, fst_filename):
        import tempfile
        self.journal_files = journal_files
        self.cisis = cisis
        self.temp_dir = tempfile.mkdtemp().replace('\\', '/')
        self.ahead_db_records = {}
        self.changed = []
        self.fst_filename = fst_filename

        for db_filename in self.journal_files.ahead_bases:
            self.cisis.i2id(db_filename, self.temp_dir + '/ahead.id')
            self.ahead_db_records[self.name(db_filename)] = isis.IDFile().read(self.temp_dir + '/ahead.id')

    def name(self, db_filename):
        return os.path.basename(db_filename)

    def find_ahead_record(self, doi, filename):
        """
        Find ahead records, given a DOI
        """
        if doi is None:
            doi = '-'
        if filename is None:
            filename = '-'
        fname = None
        db = None
        order = None
        for ahead_db_name, records in self.ahead_db_records.items():
            for rec in records:
                if rec.get('706') == 'h' and (doi == rec.get('237') or filename == rec.get('2')):
                    fname = rec.get('2')
                    db = ahead_db_name
                    order = rec.get('121')
                    break
        return (db, fname, order)

    def mark_records_as_deleted(self, ahead_db_name, filename):
        """
        Mark as deleted
        """
        deleted = None
        current_records = []
        deleted_records = []
        records = self.ahead_db_records[ahead_db_name]
        for rec in records:
            if rec.get('2') == filename:
                deleted_records.append(rec)
            else:
                current_records.append(rec)
        if len(deleted_records) > 1:
            deleted = deleted_records[1]
            self.ahead_db_records[ahead_db_name] = current_records
        return deleted

    def exclude_ahead_record(self, article, filename):
        """
        Exclude ISIS record of ahead database (serial)
        """
        deleted = None

        ahead_db_name, fname, order = self.find_ahead_record(article.doi, filename)
        if ahead_db_name is not None:
            if fname is not None:
                deleted = self.mark_records_as_deleted(ahead_db_name, fname)

        if not deleted is None:
            print('Exclude ahead record of ' + fname)
            year = ahead_db_name[0:4]
            if not ahead_db_name in self.changed:
                self.changed.append(ahead_db_name)

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
            isis.IDFile().save(id_temp, [deleted], 'iso-8859-1')
            self.cisis.id2mst(id_temp, self.journal_files.ahead_base('ex-' + year), False)
        return deleted

    def update_db(self):
        for db_filename in self.journal_files.ahead_bases:
            name = self.name(db_filename)
            if name in self.changed:
                id_file = self.temp_dir + '/ahead.id'
                isis.IDFile().save(id_file, self.ahead_db_records[name], 'iso-8859-1')
                self.cisis.id2i(id_file, db_filename)
                print('Updating ' + db_filename)
                if not os.path.isfile(db_filename + '.fst'):
                    shutil.copy(self.fst_filename, db_filename + '.fst')
                self.cisis.generate_indexes(db_filename, db_filename + '.fst', db_filename)

                ex_db_filename = self.journal_files.ahead_base('ex-' + name[0:4])
                self.cisis.generate_indexes(ex_db_filename, ex_db_filename + '.fst', ex_db_filename)


class ArticleDB(object):

    def __init__(self, i_record):
        self.i_record = i_record

    def create_id_file(self, article, section_code, article_files):
        if not os.path.isdir(article_files.id_path):
            os.makedirs(article_files.id_path)
        if not os.path.isdir(os.path.dirname(article_files.issue_files.base)):
            os.makedirs(os.path.dirname(article_files.issue_files.base))

        if article.order != '00000':
            article_isis = isis.ArticleISIS(article, self.i_record, section_code, article_files)

            id_file = isis.IDFile()
            id_file.save(article_files.id_filename, article_isis.records, 'utf-8')

        else:
            print('Invalid value for order.')


class ArticleFiles(object):

    def __init__(self, issue_files, order, xml_name):
        self.issue_files = issue_files
        self.order = order
        self.xml_name = xml_name

    @property
    def id_filename(self):
        return self.id_path + self.order + '.id'

    @property
    def id_path(self):
        return self.issue_files.issue_path + '/id/'

    @property
    def relative_xml_filename(self):
        return self.issue_files.acron_and_issue_folder + '/' + self.xml_name + '.xml'


class IssueFiles(object):

    def __init__(self, journal_files, issue_folder):
        self.journal_files = journal_files
        self.issue_folder = issue_folder

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
