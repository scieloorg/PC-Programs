# coding=utf-8
import os
import sys
import Tkinter

from __init__ import _
import utils
import xml_utils
import fs_utils
import java_xml_utils
import article
import dbm_isis
import xc_config


global ucisis


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


class InputForm(object):

    def __init__(self, tkFrame, default_path):

        self.tkFrame = tkFrame
        self.selected_xml_folder = None
        self.valid_xml_folder = None
        self.default_path = default_path
        self.issue_path = None
        self.acron = None
        self.issueid = None

        if default_path is None:
            self.default_path = CURRENT_PATH

        self.tkFrame.label_frame_xml_folder = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_xml_folder.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_issue_folder = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_issue_folder.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_message = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_message.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_from_date = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_from_date.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_buttons = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_buttons.pack(fill="both", expand="yes")

        #
        self.tkFrame.label_xml_folder = Tkinter.Label(self.tkFrame.label_frame_xml_folder, text=_('SciELO XML folder:'), font="Verdana 12 bold")
        self.tkFrame.label_xml_folder.pack(side='left')
        self.tkFrame.input_xml_folder = Tkinter.Label(self.tkFrame.label_frame_xml_folder, width=50, bd=1, bg='gray')
        self.tkFrame.input_xml_folder.pack(side='left')
        self.tkFrame.button_choose_xml_folder = Tkinter.Button(self.tkFrame.label_frame_xml_folder, text=_('choose folder'), command=self.select_xml_folder)
        self.tkFrame.button_choose_xml_folder.pack()

        self.tkFrame.label_issue_folder = Tkinter.Label(self.tkFrame.label_frame_issue_folder, text=_('issue folder:'), font="Verdana 12 bold")
        self.tkFrame.label_issue_folder.pack(side='left')
        self.tkFrame.input_issue_folder = Tkinter.Label(self.tkFrame.label_frame_issue_folder, width=50, bd=1, bg='gray')
        self.tkFrame.input_issue_folder.pack(side='left')
        self.tkFrame.button_choose_issue_folder = Tkinter.Button(self.tkFrame.label_frame_issue_folder, text=_('choose folder'), command=self.select_issue_folder)
        self.tkFrame.button_choose_issue_folder.pack()

        self.tkFrame.label_from_date = Tkinter.Label(self.tkFrame.label_frame_from_date, text=_('from date'))
        self.tkFrame.label_from_date.pack(side='left')
        self.tkFrame.input_from_date = Tkinter.Entry(self.tkFrame.label_frame_from_date, bd=5)
        self.tkFrame.input_from_date.pack(side='right')

        self.tkFrame.label_message = Tkinter.Label(self.tkFrame.label_frame_message)
        self.tkFrame.label_message.pack()

        self.tkFrame.button_ok = Tkinter.Button(self.tkFrame.label_frame_buttons, text=_('ok'), command=self.ok)
        self.tkFrame.button_ok.pack(side='right')

        self.tkFrame.button_cancel = Tkinter.Button(self.tkFrame.label_frame_buttons, text=_('cancel'), command=self.cancel)
        self.tkFrame.button_cancel.pack(side='right')

        #self.collection_name = None

    def select_xml_folder(self):
        from tkFileDialog import askdirectory
        if self.selected_xml_folder is not None:
            self.default_path = self.selected_xml_folder
        self.selected_xml_folder = askdirectory(parent=self.tkFrame, initialdir=self.default_path, title=_('Select the SciELO XML folder'))
        self.tkFrame.input_xml_folder.config(text=self.selected_xml_folder)
        if self.selected_xml_folder is None:
            self.selected_xml_folder = ''
        else:
            self.display_message(self.selected_xml_folder, '#EAFDE6')

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

    def validate_xml_folder(self):
        if self.selected_xml_folder != '':
            if os.path.isdir(self.selected_xml_folder):
                if len([item for item in os.listdir(self.selected_xml_folder) if item.endswith('.xml')]) > 0:
                    self.valid_xml_folder = self.selected_xml_folder

    def validate_issue_folder(self):
        self.acron = None
        self.issueid = None
        if self.selected_issue_folder != '':
            if os.path.isdir(self.selected_issue_folder):
                if '/serial/' in self.selected_issue_folder.lower():
                    path = self.selected_issue_folder[self.selected_issue_folder.find('/serial/') + len('/serial/'):]
                    folders = path.split('/')
                    if len(folders) == 2:
                        self.acron, self.issueid = folders
                        self.issue_path = self.selected_issue_folder

    def ok(self):
        self.validate_xml_folder()
        self.validate_issue_folder()
        self.from_date = self.tkFrame.input_from_date.get()
        if self.valid_xml_folder is None:
            self.display_message(_('Select a folder which contains the SPS XML Files.'), '#CE3B67')
        elif self.issue_path is None:
            self.display_message(_('Select the issue folder (serial/<acron>/<issue number>).'), '#CE3B67')
        else:
            self.tkFrame.quit()

    def cancel(self):
        self.valid_xml_folder = None
        self.issue_path = None
        self.tkFrame.quit()


def call_execute_pubmed_procedures(args):
    config = xc_config.XMLConverterConfiguration(CURRENT_PATH + '/../scielo_paths.ini')
    global ucisis
    ucisis = dbm_isis.UCISIS(dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660))

    script, path, issue_path, from_date = read_inputs(args)

    if path is None:
        # GUI
        path, issue_path, from_date = read_form_inputs()
    else:
        errors = xml_utils.is_valid_xml_path(path)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ATTENTION =====\n')
            messages.append('ERROR: ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python ' + script + ' <xml_src>')
            messages.append(_('where') + ':')
            messages.append('  <xml_src> = ' + _('XML filename or path which contains XML files'))
            messages.append('\n'.join(errors))
            utils.display_message('\n'.join(messages))

    if path is not None:
        _from_date = None
        if from_date is not None:
            if from_date != '':
                _from_date = from_date

        pubmed_path = issue_path + '/PubMed'
        if not os.path.isdir(pubmed_path):
            os.makedirs(pubmed_path)
        folders = issue_path.split('/')
        acron = folders[-1]
        issueid = folders[-2]
        execute_pubmed_procedures(path, pubmed_path, acron, issueid, _from_date)


def read_inputs(args):
    args = [arg.decode(encoding=sys.getfilesystemencoding()) for arg in args]
    from_date = None
    if len(args) == 3:
        script, path, issue_path = args
    elif len(args) == 4:
        script, path, issue_path, from_date = args
    return (script, path, issue_path, from_date)


def read_form_inputs(default_path=None):
    tk_root = Tkinter.Tk()
    tk_root.title('XML 2 PubMed')

    tkFrame = Tkinter.Frame(tk_root)

    form = InputForm(tkFrame, default_path)
    form.tkFrame.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
    tk_root.focus_set()
    return form.valid_xml_folder


def execute_pubmed_procedures(path, pubmed_path, acron, issueid, from_date):
    articles_xml_content = create_article_set_xml_content(select_xml_files(path, from_date))
    articles_pids_xml_content = create_articles_pids_xml_content(pubmed_path, issueid)

    pubmed_filename = generate_pubmed_filename(pubmed_path, acron, issueid, from_date)
    build_pubmed_xml(articles_xml_content, articles_pids_xml_content, pubmed_filename)
    # validate
    # envia ftp


def generate_pubmed_filename(pubmed_path, acron, issueid, from_date):
    suffix = '' if from_date is None else from_date + '-' + utils.now()[0]
    return os.path.join(pubmed_path, acron + issueid + suffix + '.xml')


def select_xml_files(path, from_date):
    files = []
    if from_date is None:
        from_date = 0
    for item in [item for item in os.listdir(path) if item.endswith('.xml')]:
        xml, e = xml_utils.load_xml(os.path.join(path, item))
        a = article.Article(xml)
        if int(a.epub_dateiso) >= int(from_date):
            files.append(xml_utils.node_xml(a.find('.')))
    return files


def create_article_set_xml_content(files):
    return '<article-set>' + ''.join(files) + '</article-set>'


def temp_xml_filename(pubmed_filename, article_set_xml_content, articles_pids_xml_content):
    temp_filename = pubmed_filename[:-4] + 'tmp.xml'
    xml_content = '<?xml encoding="utf-8"?>\n'
    xml_content += '<root>'
    xml_content += article_set_xml_content
    xml_content += articles_pids_xml_content
    xml_content += '</root>'
    fs_utils.write_file(temp_filename, xml_content)
    return temp_filename


def article_pid_items(articles_db_filename):
    articles_db = dbm_isis.IsisDB(ucisis, articles_db_filename, './articles.fst')

    items = {}
    h_records = articles_db.get_records('tp=i')
    issn_id = h_records[0].get('35')

    pid = '0'*4 + h_records[0].get('36')[4:]

    issue_pid = h_records[0].get('36')[:4] + pid[-4:]
    h_records = articles_db.get_records('tp=h')
    for item in h_records:
        a_pid = '0'*5 + item.get('121')

        items[os.path.basename(item.get('702'))] = 'S' + issn_id + issue_pid + a_pid[-5:]
    return items


def create_articles_pids_xml_content(article_pid_items):
    articles_db_filename = os.path.dirname(pubmed_path) + '/base/' + issueid
    for k, v in article_pid_items(articles_db_filename):
        print(k)


def build_pubmed_xml(article_set_xml_content, articles_pids_xml_content, pubmed_filename):
    temp_filename = temp_xml_filename(pubmed_filename, article_set_xml_content, articles_pids_xml_content)
    java_xml_utils.xml_transform(temp_filename, xsl_filename, pubmed_filename)

