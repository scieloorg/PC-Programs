# coding=utf-8
import os
import shutil
from datetime import datetime


class DocumentFiles(object):

    def __init__(self, xml_filename, report_path, wrk_path):
        self.ctrl_filename = None
        self.html_filename = None

        self.is_sgmxml = xml_filename.endswith('.sgm.xml')
        self.xml_filename = xml_filename
        self.xml_path = os.path.dirname(xml_filename)

        basename = os.path.basename(xml_filename).replace('.sgm.xml', '')
        self.xml_name = basename.replace('.xml', '')
        self.new_name = self.xml_name

        report_name = self.xml_name

        if self.is_sgmxml:
            wrk_path = wrk_path + '/' + self.xml_name
            if not os.path.isdir(wrk_path):
                os.makedirs(wrk_path)
            self.html_filename = wrk_path + '/' + self.xml_name + '.temp.htm'
            if not os.path.isfile(self.html_filename):
                self.html_filename += 'l'
            self.ctrl_filename = wrk_path + '/' + self.xml_name + '.ctrl.txt'

        if not os.path.isdir(report_path):
            os.makedirs(report_path)
        self.dtd_report_filename = report_path + '/' + report_name + '.dtd.txt'
        self.style_report_filename = report_path + '/' + report_name + '.rep.html'

        self.pmc_dtd_report_filename = report_path + '/' + report_name + '.pmc.dtd.txt'
        self.pmc_style_report_filename = report_path + '/' + report_name + '.pmc.rep.html'

        self.err_filename = report_path + '/' + report_name + '.err.txt'

        self.data_report_filename = report_path + '/' + report_name + '.contents.html'

    def clean(self):
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


class ArticleFiles(object):

    def __init__(self, issue_files, order, xml_name):
        self.issue_files = issue_files
        self.order = order
        self.filename = xml_name if xml_name.endswith('.xml') else xml_name + '.xml'
        self.xml_name = xml_name.replace('.xml', '')

    @property
    def id_filename(self):
        return self.issue_files.id_path + '/' + self.order + '.id'

    @property
    def relative_xml_filename(self):
        return self.issue_files.relative_issue_path + '/' + self.filename


class IssueFiles(object):

    def __init__(self, journal_files, issue_folder, xml_path, web_path):
        self.journal_files = journal_files
        self.issue_folder = issue_folder
        self.xml_path = xml_path
        self.web_path = web_path
        self.create_folders()

    def create_folders(self):
        for path in [self.id_path, self.base_path, self.base_reports_path, self.base_source_path]:
            if not os.path.isdir(path):
                os.makedirs(path)

    @property
    def issue_path(self):
        return self.journal_files.journal_path + '/' + self.issue_folder

    @property
    def relative_issue_path(self):
        return self.journal_files.acron + '/' + self.issue_folder

    @property
    def id_path(self):
        return self.issue_path + '/base_xml/id'

    @property
    def id_filename(self):
        return self.id_path + '/i.id'

    @property
    def base_path(self):
        return self.issue_path + '/base'

    @property
    def windows_base_path(self):
        return self.issue_path + '/windows'

    @property
    def base_reports_path(self):
        return self.issue_path + '/base_xml/base_reports'

    @property
    def base_source_path(self):
        return self.issue_path + '/base_xml/base_source'

    @property
    def base(self):
        return self.base_path + '/' + self.issue_folder

    @property
    def windows_base(self):
        return self.windows_base_path + '/' + self.issue_folder

    def copy_files_to_local_web_app(self):
        msg = ['\n']
        msg.append('copying files from ' + self.xml_path)
        path = {}
        path['pdf'] = self.web_path + '/bases/pdf/' + self.relative_issue_path
        path['xml'] = self.web_path + '/bases/xml/' + self.relative_issue_path
        path['html'] = self.web_path + '/htdocs/img/revistas/' + self.relative_issue_path + '/html/'
        path['img'] = self.web_path + '/htdocs/img/revistas/' + self.relative_issue_path

        for p in path.values():
            if not os.path.isdir(p):
                os.makedirs(p)
        for f in os.listdir(self.xml_path):
            if f.endswith('.xml.bkp') or f.endswith('.xml.replaced.txt'):
                pass
            elif os.path.isfile(self.xml_path + '/' + f):
                ext = f[f.rfind('.')+1:]
                if path.get(ext) is not None:
                    shutil.copy(self.xml_path + '/' + f, path[ext])
                    msg.append('  ' + f + ' => ' + path[ext])
                else:
                    if not f.endswith('.tif') and not f.endswith('.tiff'):
                        shutil.copy(self.xml_path + '/' + f, path['img'])
                        msg.append('  ' + f + ' => ' + path['img'])

        return '\n'.join(['<p>' + item + '</p>' for item in msg])

    def save_reports(self, report_path):
        if not self.base_reports_path == report_path:
            if not os.path.isdir(self.base_reports_path):
                os.makedirs(self.base_reports_path)
            for report_file in os.listdir(report_path):
                shutil.copy(report_path + '/' + report_file, self.base_reports_path)
                os.unlink(report_path + '/' + report_file)
        try:
            shutil.rmtree(report_path)
        except:
            pass

    def save_source_files(self, xml_path):
        if not self.base_source_path == xml_path:
            if not os.path.isdir(self.base_source_path):
                os.makedirs(self.base_source_path)
            for f in os.listdir(xml_path):
                try:
                    shutil.copy(xml_path + '/' + f, self.base_source_path)
                except:
                    pass


def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)


class JournalFiles(object):

    def __init__(self, serial_path, acron):
        if serial_path.endswith('/'):
            serial_path = serial_path[0:-1]
        self.acron = acron
        self.journal_path = serial_path + '/' + acron
        self.years = [str(int(datetime.now().isoformat()[0:4])+1 - y) for y in range(0, 5)]

    def ahead_base(self, year):
        path = self.journal_path + '/' + year + 'nahead/base/' + year + 'nahead'
        #create_path(os.path.dirname(path))
        return path

    def ahead_xml_markup_body(self, year, filename):
        m = self.journal_path + '/' + year + 'nahead/markup'
        b = self.journal_path + '/' + year + 'nahead/body'
        x = self.journal_path + '/' + year + 'nahead/base_xml/base_source'
        #create_path(m)
        #create_path(b)
        #create_path(x)
        return (x + '/' + filename, m + '/' + filename, b + '/' + filename)

    def ahead_id_filename(self, year, order):
        order = '00000' + order
        order = order[-5:]
        return self.ahead_id_path(year) + '/' + order + '.id'

    def ahead_i_id_filename(self, year):
        return self.ahead_id_path(year) + '/i.id'

    def ahead_id_path(self, year):
        path = self.journal_path + '/' + year + 'nahead/base_xml/id'
        #create_path(path)
        return path

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
