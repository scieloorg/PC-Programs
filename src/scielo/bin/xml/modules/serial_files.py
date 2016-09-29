# coding=utf-8
import os
import shutil
from datetime import datetime

import fs_utils
from article import Article


def filename_language_suffix(filename):
    name, ext = os.path.splitext(filename)
    parts = name.split('-')
    suffix = parts[-1]
    lang = None
    if len(suffix) == 2:
        if not suffix[0].isdigit() and not suffix[1].isdigit():
            lang = suffix
    return lang


def new_name_for_pdf_filename(pdf_filename):
    lang_suffix = filename_language_suffix(pdf_filename)
    if lang_suffix is not None:
        return lang_suffix + '_' + pdf_filename.replace('-' + lang_suffix + '.pdf', '.pdf')


class ArticleWorkArea(object):

    def __init__(self, xml_filename, report_path, wrk_path=None):
        self.ctrl_filename = None
        self.html_filename = None
        self.report_path = report_path
        self.wrk_path = wrk_path
        self.related_files = []
        self.is_sgmxml = xml_filename.endswith('.sgm.xml')
        self.xml_filename = xml_filename
        self.new_xml_filename = self.xml_filename
        self.xml_path = os.path.dirname(xml_filename)

        basename = os.path.basename(xml_filename).replace('.sgm.xml', '')
        self.xml_name = basename.replace('.xml', '')
        self.new_name = self.xml_name

        if self.is_sgmxml:
            self.wrk_path = wrk_path + '/' + self.xml_name
            if not os.path.isdir(self.wrk_path):
                os.makedirs(self.wrk_path)
            self.html_filename = self.wrk_path + '/' + self.xml_name + '.temp.htm'
            if not os.path.isfile(self.html_filename):
                self.html_filename += 'l'
            self.ctrl_filename = self.wrk_path + '/' + self.xml_name + '.ctrl.txt'

    @property
    def report_path(self):
        return self._report_path

    @report_path.setter
    def report_path(self, _report_path):
        if not os.path.isdir(_report_path):
            os.makedirs(_report_path)
        self._report_path = _report_path

    @property
    def dtd_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.dtd.txt'

    @property
    def style_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.rep.html'

    @property
    def pmc_dtd_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.pmc.dtd.txt'

    @property
    def pmc_style_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.pmc.rep.html'

    @property
    def err_filename(self):
        return self.report_path + '/' + self.xml_name + '.err.txt'

    @property
    def err_filename_html(self):
        return self.report_path + '/' + self.xml_name + '.err.html'

    @property
    def data_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.contents.html'

    @property
    def images_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.images.html'

    @property
    def xml_structure_validations_filename(self):
        return self.report_path + '/xmlstr-' + self.xml_name

    @property
    def xml_content_validations_filename(self):
        return self.report_path + '/xmlcon-' + self.xml_name

    @property
    def journal_validations_filename(self):
        return self.report_path + '/journal-' + self.xml_name

    @property
    def issue_validations_filename(self):
        return self.report_path + '/issue-' + self.xml_name

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
        if xml_name is None:
            self.filename = None
            self.xml_name = None
        else:
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
        self.move_old_id_folder()
        self._articles_files = None
        self.is_aop = issue_folder.endswith('ahead') and not issue_folder.startswith('ex-')
        self.is_ex_aop = issue_folder.endswith('ahead') and issue_folder.startswith('ex-')
        self.is_pr = issue_folder.endswith('pr') and not issue_folder.startswith('ex-')
        self.is_regular = not self.is_aop and not self.is_ex_aop and not self.is_pr

    @property
    def articles_files(self):
        if self._articles_files is None:
            self._articles_files = {}
            for item in os.listdir(self.id_path):
                if os.path.isfile(self.id_path + '/' + item) and item.endswith('.id'):
                    order = item.replace('.id', '')
                    self._articles_files[order] = ArticlesFiles(self, order, None)
        return self._articles_files

    def create_folders(self):
        for path in [self.id_path, self.base_path, self.base_reports_path, self.base_source_path]:
            if not os.path.isdir(path):
                os.makedirs(path)

    def move_old_id_folder(self):
        if os.path.isdir(self.old_id_path):
            if not os.path.isdir(self.id_path):
                os.makedirs(self.id_path)
            for item in os.listdir(self.old_id_path):
                if not os.path.isfile(self.id_path + '/' + item):
                    shutil.copyfile(self.old_id_path + '/' + item, self.id_path + '/' + item)
            try:
                fs_utils.delete_file_or_folder(self.old_id_path)
            except:
                pass

    @property
    def issue_path(self):
        return self.journal_files.journal_path + '/' + self.issue_folder

    @property
    def relative_issue_path(self):
        return self.journal_files.acron + '/' + self.issue_folder

    @property
    def old_id_path(self):
        return self.issue_path + '/id'

    @property
    def id_path(self):
        return self.base_xml_path + '/id'

    @property
    def id_filename(self):
        return self.id_path + '/i.id'

    @property
    def base_path(self):
        return self.issue_path + '/base'

    @property
    def markup_path(self):
        return self.issue_path + '/markup'

    @property
    def body_path(self):
        return self.issue_path + '/body'

    @property
    def windows_base_path(self):
        return self.issue_path + '/windows'

    @property
    def base_xml_path(self):
        return self.issue_path + '/base_xml'

    @property
    def base_reports_path(self):
        return self.base_xml_path + '/base_reports'

    @property
    def base_source_path(self):
        return self.base_xml_path + '/base_source'

    @property
    def base_source_xml_files(self):
        return [self.base_source_path + '/' + item for item in os.listdir(self.base_source_path) if item.endswith('.xml')]

    @property
    def xml_files(self):
        return {item: self.base_source_path + '/' + item for item in os.listdir(self.base_source_path) if item.endswith('.xml')}

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
        xml_files = [f for f in os.listdir(self.xml_path) if f.endswith('.xml') and not f.endswith('.rep.xml')]
        xml_content = ''.join([fs_utils.read_file(self.xml_path + '/' + xml_filename) for xml_filename in os.listdir(self.xml_path) if xml_filename.endswith('.xml')])

        for p in path.values():
            if not os.path.isdir(p):
                os.makedirs(p)
        for f in os.listdir(self.xml_path):
            if f.endswith('.xml.bkp') or f.endswith('.xml.replaced.txt') or f.endswith('.rep.xml'):
                pass
            elif os.path.isfile(self.xml_path + '/' + f):
                ext = f[f.rfind('.')+1:]

                if path.get(ext) is None:
                    if not f.endswith('.tif') and not f.endswith('.tiff'):
                        shutil.copy(self.xml_path + '/' + f, path['img'])
                        msg.append('  ' + f + ' => ' + path['img'])
                elif ext == 'pdf':
                    pdf_filenames = [f]
                    new_pdf_filename = new_name_for_pdf_filename(f)
                    if new_pdf_filename is not None:
                        pdf_filenames.append(new_pdf_filename)
                    for pdf_filename in pdf_filenames:
                        if os.path.isfile(path[ext] + '/' + pdf_filename):
                            os.unlink(path[ext] + '/' + pdf_filename)
                        shutil.copyfile(self.xml_path + '/' + f, path[ext] + '/' + pdf_filename)
                        msg.append('  ' + f + ' => ' + path[ext] + '/' + pdf_filename)
                else:
                    shutil.copy(self.xml_path + '/' + f, path[ext])
                    msg.append('  ' + f + ' => ' + path[ext])
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
                if f.endswith('.rep.xml'):
                    pass
                elif f.endswith('.xml'):
                    try:
                        shutil.copy(xml_path + '/' + f, self.base_source_path)
                    except:
                        pass

    def delete_id_files(self, delete_id_items):
        errors = []
        if len(delete_id_items) > 0:
            if self.backup_id_folder():
                for item in delete_id_items:
                    if os.path.isfile(self.id_path + '/' + item + '.id'):
                        os.unlink(self.id_path + '/' + item + '.id')
                    if os.path.isfile(self.id_path + '/' + item + '.id'):
                        errors.append(item + '.id')
        return errors

    def backup_folder(self, src_path, dest_path):
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        for fname in os.listdir(dest_path):
            os.unlink(dest_path + '/' + fname)
        for fname in os.listdir(src_path):
            shutil.copyfile(src_path + '/' + fname, dest_path + '/' + fname)
        return (len(os.listdir(src_path)) == len(os.listdir(dest_path)))

    def backup_id_folder(self, backup_name='.bkp'):
        return self.backup_folder(self.id_path, self.id_path + backup_name)

    def restore_backup_id_folder(self, backup_name='.bkp'):
        r = self.backup_folder(self.id_path + backup_name, self.id_path)
        for fname in os.listdir(self.id_path + backup_name):
            os.unlink(self.id_path + backup_name + '/' + fname)
        return r


def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)


class JournalFiles(object):

    def __init__(self, serial_path, acron):
        if serial_path.endswith('/'):
            serial_path = serial_path[0:-1]
        self.acron = acron
        self.journal_path = serial_path + '/' + acron
        if not os.path.isdir(self.journal_path):
            os.makedirs(self.journal_path)
        self._issues_files = {}
        for issue_id in os.listdir(self.journal_path):
            if os.path.isdir(self.journal_path + '/' + issue_id):
                if os.path.isfile(self.journal_path + '/' + issue_id + '/base/' + issue_id + '.mst'):
                    self._issues_files[issue_id] = IssueFiles(self, issue_id, None, None)

    @property
    def issues_files(self):
        return self._issues_files

    def publishes_aop(self):
        return len(self.aop_issue_files) > 0

    @property
    def pr_issues_files(self):
        return {k:v for k, v in self.issues_files.items() if v.is_pr}

    @property
    def regular_issues_files(self):
        return {k:v for k, v in self.issues_files.items() if v.is_regular}

    @property
    def aop_issue_files(self):
        return {k:v for k, v in self.issues_files.items() if v.is_aop}

    @property
    def ex_aop_issues_files(self):
        return {k:v for k, v in self.issues_files.items() if v.is_ex_aop}

    def archive_ex_aop_files(self, aop, db_name):
        aop_issue_files = None
        ex_aop_issues_files = None
        done = False
        errors = []
        if self.ex_aop_issues_files is not None:
            ex_aop_db_name = 'ex-' + db_name
            ex_aop_issues_files = self.ex_aop_issues_files.get(ex_aop_db_name)
            if ex_aop_issues_files is None:
                self._issues_files[ex_aop_db_name] = IssueFiles(self, ex_aop_db_name, None, None)
                ex_aop_issues_files = self._ex_aop_issues_files[ex_aop_db_name]
        if self.aop_issue_files is not None:
            aop_issue_files = self.aop_issue_files.get(db_name)
        if aop_issue_files is not None and ex_aop_issues_files is not None:
            errors += fs_utils.move_file(aop_issue_files.markup_path + '/' + aop.filename, ex_aop_issues_files.markup_path + '/' + aop.filename)
            errors += fs_utils.move_file(aop_issue_files.body_path + '/' + aop.filename, ex_aop_issues_files.body_path + '/' + aop.filename)
            errors += fs_utils.move_file(aop_issue_files.base_source_path + '/' + aop.filename, ex_aop_issues_files.base_source_path + '/' + aop.filename)
            errors += fs_utils.move_file(aop_issue_files.id_path + '/' + aop.order + '.id', ex_aop_issues_files.id_path + '/' + aop.order + '.id')
        if aop_issue_files is not None:
            done = (not os.path.isfile(aop_issue_files.id_path + '/' + aop.order + '.id'))
        return (done, errors)

