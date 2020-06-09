# coding=utf-8
import logging
import logging.config
import sys
import os
import argparse
import shutil
import tkinter as tk

"""
Usado pelo scielo/xml_scielo/...
para gerar XML para o PubMed
"""
from prodtools import _
from prodtools import DTD_AND_XSL_PATH
from prodtools.utils import utils
from prodtools.utils import xml_utils
from prodtools.utils import fs_utils
from prodtools.utils.dbm import dbm_isis
from prodtools.config import config as xc_config
from prodtools.utils.logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()

global ucisis

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
FST_ARTICLE = os.path.join(CURRENT_PATH, 'settings', 'fst', 'articles.fst')
XSL = os.path.join(
    DTD_AND_XSL_PATH, 'v3.0', 'xsl', 'xml2pubmed', 'xml2pubmed.xsl')


def find_xml_files_folders(path, folders=[]):
    for item in os.listdir(path):
        folder = os.path.join(path, item)
        if os.path.isdir(folder):
            xml_files = [f for f in os.listdir(folder) if f.endswith('.xml')]
            if len(xml_files) > 0:
                folders.append(folder)
            folders = find_xml_files_folders(folder, folders)
    return folders


def find_xml_files(filenames, folders):
    files = {}
    for filename in filenames:
        for xml_folder_path in folders:
            if filename in os.listdir(xml_folder_path):
                files[filename] = os.path.join(xml_folder_path, filename)
                break
    return files


def find_xml_files_in_alternative(filenames, main_path, found_files={}):
    for item in os.listdir(main_path):
        item_path = os.path.join(main_path, item)
        if os.path.isfile(item_path):
            if item in filenames:
                if item not in found_files.keys():
                    found_files[item] = item_path

        elif os.path.isdir(item_path):
            found_files = find_xml_files_in_alternative(
                filenames, item_path, found_files)
    return found_files


def load_articles(filenames):
    files = {}
    for name, f in filenames.items():
        xmltree, errors = xml_utils.load_xml(f)
        if xmltree is not None:
            files[name] = xml_utils.tostring(xmltree.getroot())
        else:
            print(' ERROR 1: {} - {}'.format(name, errors))
    return files


class InputForm(object):

    def __init__(self, tkFrame, default_path):

        self.tkFrame = tkFrame
        self.selected_xml_folder = None
        self.valid_xml_folder = None
        self.default_path = default_path
        self.issue_path = None
        self.acron = None
        self.issueid = None
        self.from_date = None
        self.selected_issue_folder = None

        if default_path is None:
            self.default_path = CURRENT_PATH

        self.tkFrame.label_frame_xml_folder = tk.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_xml_folder.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_issue_folder = tk.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_issue_folder.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_message = tk.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_message.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_from_date = tk.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_from_date.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_buttons = tk.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_buttons.pack(fill="both", expand="yes")

        #
        self.tkFrame.label_issue_folder = tk.Label(self.tkFrame.label_frame_issue_folder, text=_('issue folder (located in serial folder):'), font="Verdana 12 bold")
        self.tkFrame.label_issue_folder.pack(side='left')
        self.tkFrame.input_issue_folder = tk.Label(self.tkFrame.label_frame_issue_folder, width=50, bd=1, bg='gray')
        self.tkFrame.input_issue_folder.pack(side='left')
        self.tkFrame.button_choose_issue_folder = tk.Button(self.tkFrame.label_frame_issue_folder, text=_('choose folder'), command=self.select_issue_folder)
        self.tkFrame.button_choose_issue_folder.pack()

        self.tkFrame.label_from_date = tk.Label(self.tkFrame.label_frame_from_date, text=_('from date'))
        self.tkFrame.label_from_date.pack(side='left')
        self.tkFrame.input_from_date = tk.Entry(self.tkFrame.label_frame_from_date, bd=5)
        self.tkFrame.input_from_date.pack(side='right')

        self.tkFrame.label_message = tk.Label(self.tkFrame.label_frame_message)
        self.tkFrame.label_message.pack()

        self.tkFrame.button_ok = tk.Button(self.tkFrame.label_frame_buttons, text=_('ok'), command=self.ok)
        self.tkFrame.button_ok.pack(side='right')

        self.tkFrame.button_cancel = tk.Button(self.tkFrame.label_frame_buttons, text=_('cancel'), command=self.cancel)
        self.tkFrame.button_cancel.pack(side='right')

        #self.collection_name = None

    def select_issue_folder(self):
        from tkFileDialog import askdirectory
        if self.selected_issue_folder is not None:
            self.default_path = self.selected_issue_folder
        self.selected_issue_folder = askdirectory(parent=self.tkFrame, initialdir=self.default_path, title=_('Select the issue folder'))
        self.tkFrame.input_issue_folder.config(text=self.selected_issue_folder)
        if self.selected_issue_folder is None:
            self.selected_issue_folder = ''
        else:
            self.display_message(self.selected_issue_folder, '#EAFDE6')

    def display_message(self, msg, color):
        if len(msg) > 0:
            self.tkFrame.label_message.config(text=msg, bg=color)
            self.tkFrame.label_message.update_idletasks()

    def validate_issue_folder(self):
        if self.selected_issue_folder:
            if os.path.isdir(self.selected_issue_folder):
                basenames = fs_utils.splitpath(self.select_issue_folder)
                if basenames[-3].lower() == "serial":
                    self.issue_path = self.selected_issue_folder

    def ok(self):
        self.validate_issue_folder()
        self.from_date = self.tkFrame.input_from_date.get()
        if self.issue_path is None:
            self.display_message(_('Select the issue folder (serial/<acron>/<issue number>).'), '#CE3B67')
        else:
            self.tkFrame.quit()

    def cancel(self):
        self.issue_path = None
        self.tkFrame.quit()


class IssueStuff(object):

    def __init__(self, ucisis, issue_path, from_date, final_date):
        self.from_date = from_date
        self.final_date = final_date
        self.ucisis = ucisis
        self._articles_meta = None
        self._articles_files = None

        self.issue_path = issue_path

        basenames = fs_utils.splitpath(issue_path)
        self.issueid = basenames[-1]
        self.acron = basenames[-2]

        self.serial_path = os.path.dirname(os.path.dirname(issue_path))

        self.pubmed_path = os.path.join(issue_path, 'PubMed')
        if not os.path.isdir(self.pubmed_path):
            os.makedirs(self.pubmed_path)

        self.temp_path = os.path.join(issue_path,  'TMP')
        if not os.path.isdir(self.temp_path):
            os.makedirs(self.temp_path)

        self.articles_db_filename = os.path.join(
            issue_path, 'base', self.issueid)

        self.tmp_db_filename = os.path.join(
            self.temp_path, 'pubmed_tmp_' + self.issueid)
        self.pubmed_folder_in_serial = os.path.join(self.serial_path, 'PubMed')
        self.pubmed_folder_in_acron = os.path.join(
            self.serial_path, self.acron, 'PubMed')

        for ext in ('.mst', '.xrf'):
            shutil.copyfile(
                self.articles_db_filename + ext, self.tmp_db_filename + ext)

    @property
    def articles_metadata(self):
        if self._articles_meta is None:
            self._articles_meta = ArticlesDB(self.ucisis, self.tmp_db_filename).articles(self.from_date, self.final_date)
        return self._articles_meta

    @property
    def articles_files(self):
        if self._articles_files is None:
            if self.articles_metadata is not None:
                self._articles_files = ArticlesFiles(self.issue_path, self.articles_metadata)
        return self._articles_files


class ArticlesDB(object):

    def __init__(self, ucisis, db_filename):

        self.isis_db = None
        self.db_filename = db_filename
        if os.path.isfile(db_filename + '.mst'):
            self.isis_db = ucisis
            self.isis_db.update_indexes(db_filename, FST_ARTICLE)
        else:
            print('Not found: ' + db_filename)

    def articles(self, from_date=None, final_date=None):
        items = {}
        int_from_date = 0
        int_final_date = int(utils.now()[0])

        if from_date is not None:
            if from_date != '':
                int_from_date = int(from_date)
        if final_date is not None:
            if final_date != '':
                int_final_date = int(final_date)
        if self.isis_db is not None:
            h_records = self.isis_db.get_records(
                self.db_filename, 'tp=i or tp=h')
            #h_records = [record for record in h_records if record.get('706') in 'ih']

            issn_id = h_records[0].get('35')
            pid = '0'*4 + h_records[0].get('36')[4:]
            issue_pid = h_records[0].get('36')[:4] + pid[-4:]

            unmatched = []
            matched = []

            for item in h_records:
                if item.get('706') == 'o':
                    a_date = int(item.get('91'))
                elif item.get('706') == 'h':
                    a_date = int(item.get('223', 0))
                    if int_from_date <= a_date <= int_final_date:
                        a_pid = '0'*5 + item.get('121')
                        v702 = os.path.basename(item.get('702'))
                        v880 = 'S' + issn_id + issue_pid + a_pid[-5:]
                        v881 = item.get('881', item.get('882'))
                        items[v702] = (v880, v881)
                        matched.append(a_date)
                    else:
                        unmatched.append(a_date)

            if len(matched) > 0:
                print(str(len(matched)) + ' items')
        return items


class ArticlesFiles(object):

    def __init__(self, issue_path, selected_pids):
        self.issue_path = issue_path
        self.selected_pids = selected_pids

    @property
    def selected_articles(self):
        found = find_xml_files(self.selected_pids.keys(), self.standard_xml_folder_paths)
        if len(found) < len(self.selected_pids.keys()):
            failed = [item for item in self.selected_pids.keys() if not item in found.keys()]
            found = find_xml_files_in_alternative(failed, self.issue_path, found)
            failed = [item for item in failed if not item in found.keys()]

            if len(failed) > 0:
                print('Not found: ')
                print('\n'.join(failed))
        return load_articles(found)

    @property
    def standard_xml_folder_paths(self):
        xml_path_list = []
        base_source_path = os.path.join(
            self.issue_path, 'base_xml', 'base_source')
        scielo_package_path = os.path.join(
            self.issue_path, 'markup_xml', 'scielo_package')
        for path in [base_source_path, scielo_package_path]:
            if os.path.isdir(path):
                if len([item for item in os.listdir(path) if item.endswith('.xml')]) > 0:
                    xml_path_list.append(path)
        return xml_path_list


class PubMedXMLMaker(object):

    def __init__(self, issue_stuff, xsl_filename):
        self.issue_stuff = issue_stuff
        self.xsl_filename = xsl_filename
        self.debug = False

    @property
    def pubmed_filename(self):
        suffix = '' if self.issue_stuff.from_date is None else self.issue_stuff.from_date + '-' + self.issue_stuff.final_date
        return os.path.join(self.issue_stuff.pubmed_path, self.issue_stuff.acron + self.issue_stuff.issueid + suffix + '.xml')

    @property
    def temp_xml_filename(self):
        temp_filename = os.path.join(
            self.issue_stuff.temp_path,
            'pubmed_tmp_' + os.path.basename(self.pubmed_filename))
        xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml_content += '<root>'
        xml_content += self.articles_filenames_xml_content
        xml_content += self.articles_pids_xml_content
        xml_content += '</root>'
        fs_utils.write_file(temp_filename, xml_content)
        return temp_filename

    @property
    def articles_filenames_xml_content(self):
        return '<article-set>' + ''.join(['<article-item filename="' + filename + '">' + item + '</article-item>' for filename, item in self.issue_stuff.articles_files.selected_articles.items()]) + '</article-set>'

    @property
    def articles_pids_xml_content(self):
        return '<pid-set>' + ''.join(['<pid filename="' + k + '">' + format_pids(v) + '</pid>' for k, v in sorted(self.issue_stuff.articles_files.selected_pids.items())]) + '</pid-set>'

    def execute_procedures(self):
        self.build_pubmed_xml()

        valid = self.validate_pubmed_xml()
        if valid:
            shutil.copy(
                self.pubmed_filename,
                self.issue_stuff.pubmed_folder_in_acron)
            shutil.copy(
                self.pubmed_filename,
                self.issue_stuff.pubmed_folder_in_serial)

        if self.debug is False and valid:
            self.clean_temporary_files()
        # validate
        # envia ftp

    def build_pubmed_xml(self):
        xml_obj = xml_utils.get_xml_object(self.temp_xml_filename)
        result = xml_utils.transform(xml_obj, self.xsl_filename)
        xml_utils.write(self.pubmed_filename, result)

    def validate_pubmed_xml(self):
        r = False
        err_filepath = self.pubmed_filename + '.err'
        if os.path.isfile(err_filepath):
            os.unlink(err_filepath)
        xml, error = xml_utils.load_xml(self.pubmed_filename, validate=True)
        if error:
            with open(err_filepath, "w") as fp:
                fp.write(error)
            print('Validation error: ' + err_filepath)
        else:
            print('Validates fine')
        return r

    def clean_temporary_files(self):
        for item in os.listdir(self.issue_stuff.temp_path):
            if item.startswith('pubmed_'):
                os.unlink(
                    os.path.join(self.issue_stuff.temp_path, item))


def main():

    parser = argparse.ArgumentParser(description='XML PubMed cli utility')
    parser.add_argument(
        "issue_path", nargs="?", default='',
        help="filesystem path or URL to the issue directory")
    parser.add_argument(
        "from_date", nargs="?", default='',
        help="date iso YYYYMMDD, filter to get selected documents"
    )
    parser.add_argument(
        "final_date", nargs="?", default='',
        help="date iso YYYYMMDD, filter to name file"
    )
    parser.add_argument('--debug', action='store_true',
                        help='to register log')
    parser.add_argument('--loglevel', default='WARNING')

    args = parser.parse_args()

    logger.setLevel(args.loglevel.upper())

    issue_path = args.issue_path
    from_date = args.from_date
    final_date = args.final_date
    debug = args.debug

    if not issue_path:
        issue_path, from_date = read_form_inputs()
        if issue_path is None:
            sys.exit("No issue path was informed. Unable to continue. ")
        final_date = utils.now()[0]
        debug = False

    errors = []
    if not os.path.isdir(issue_path):
        errors.append(_('issue path is not a folder'))

    if len(errors) == 0:
        config = xc_config.Configuration()
        ucisis = dbm_isis.UCISIS(
            dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660))

        if ucisis.is_available:
            issue_stuff = IssueStuff(ucisis, issue_path, from_date, final_date)

            pubmed_xml_maker = PubMedXMLMaker(issue_stuff, XSL)
            pubmed_xml_maker.debug = debug
            pubmed_xml_maker.execute_procedures()
        else:
            errors.append(_('cisis expected'))

    if len(errors) > 0:
        print('\n'.join(errors))


def read_form_inputs(default_path=None):
    tk_root = tk.Tk()
    tk_root.title('XML 2 PubMed')

    tkFrame = tk.Frame(tk_root)

    form = InputForm(tkFrame, default_path)
    form.tkFrame.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
    tk_root.focus_set()
    return (form.issue_path, form.from_date)


def format_pids(pids):
    pid, old_pid = pids
    return '<pid>{}</pid>{}'.format(
        pid,
        '' if old_pid is None else '<old-pid>{}</old-pid>'.format(old_pid)
    )


if __name__ == "__main__":
    main()
