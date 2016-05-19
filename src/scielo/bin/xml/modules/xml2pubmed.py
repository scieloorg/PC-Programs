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


class IssueAssets(object):

    def __init__(self, issue_path):
        self.issue_path = issue_path
        self.serial_path = os.path.dirname(os.path.dirname(issue_path))
        folders = issue_path.split('/')
        self.acron = folders[-2]
        self.issueid = folders[-1]
        self.pubmed_path = issue_path + '/PubMed'
        if not os.path.isdir(self.pubmed_path):
            os.makedirs(self.pubmed_path)
        self.articles_db_filename = issue_path + '/base/' + self.issueid


class ArticleDB(object):

    def __init__(self, ucisis, issue_assets):
        self.articles_db = None
        if os.path.isfile(issue_assets.articles_db_filename + '.mst'):
            self.articles_db = dbm_isis.IsisDB(ucisis, issue_assets.articles_db_filename, './articles.fst')

    @property
    def article_pid_items(self):
        items = {}
        if self.articles_db is not None:
            h_records = self.articles_db.get_records('tp=i')
            issn_id = h_records[0].get('35')
            pid = '0'*4 + h_records[0].get('36')[4:]
            issue_pid = h_records[0].get('36')[:4] + pid[-4:]
            h_records = self.articles_db.get_records('tp=h')
            for item in h_records:
                a_pid = '0'*5 + item.get('121')
                items[os.path.basename(item.get('702'))] = 'S' + issn_id + issue_pid + a_pid[-5:]
        return items


class ArticlesFiles(object):

    def __init__(self, path, from_date):
        self.path = path
        self.from_date = from_date

    @property
    def selected_xml_files(self):
        files = {}
        start_date = self.from_date
        if start_date is None:
            start_date = '0'
        for item in [item for item in os.listdir(self.path) if item.endswith('.xml')]:
            xml, e = xml_utils.load_xml(os.path.join(self.path, item))
            a = article.Article(xml, item)
            if int(a.epub_dateiso) >= int(start_date):
                files[item] = xml_utils.node_xml(a.tree.find('.'))
        return files

    @property
    def suffix(self):
        return '' if self.from_date is None else self.from_date + '-' + str(utils.now()[0])


class PubMedXMLMaker(object):

    def __init__(self, articles_files, article_db, issue_assets, xsl_filename):
        self.issue_assets = issue_assets
        self.articles_files = articles_files
        self.article_db = article_db
        self.xsl_filename = xsl_filename

    @property
    def pubmed_filename(self):
        return os.path.join(self.issue_assets.pubmed_path, self.issue_assets.acron + self.issue_assets.issueid + self.articles_files.suffix + '.xml')

    @property
    def temp_xml_filename(self):
        temp_filename = self.pubmed_filename[:-4] + 'tmp.xml'
        xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml_content += '<root>'
        xml_content += self.articles_filenames_xml_content
        xml_content += self.articles_pids_xml_content
        xml_content += '</root>'
        fs_utils.write_file(temp_filename, xml_content)
        return temp_filename

    @property
    def articles_filenames_xml_content(self):
        return '<article-set>' + ''.join(['<article-item filename="' + filename + '">' + item + '</article-item>' for filename, item in self.articles_files.selected_xml_files.items()]) + '</article-set>'

    @property
    def articles_pids_xml_content(self):
        return '<pid-set>' + ''.join(['<pid filename="' + k + '">' + v + '</pid>' for k, v in self.article_db.article_pid_items.items()]) + '</pid-set>'

    def execute_procedures(self):
        self.build_pubmed_xml()
        import webbrowser
        webbrowser.open('file:///' + self.pubmed_filename, new=2)
        # validate
        # envia ftp

    def build_pubmed_xml(self):
        java_xml_utils.xml_transform(self.temp_xml_filename, self.xsl_filename, self.pubmed_filename)


def call_execute_pubmed_procedures(args):

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
        config = xc_config.XMLConverterConfiguration(CURRENT_PATH + '/../../scielo_paths.ini')
        ucisis = dbm_isis.UCISIS(dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660))
        issue_assets = IssueAssets(issue_path)
        article_db = ArticleDB(ucisis, issue_assets)
        articles_files = ArticlesFiles(path, from_date)
        pubmed_xml_maker = PubMedXMLMaker(articles_files, article_db, issue_assets, CURRENT_PATH + '/../../pmc/v3.0/xsl/xml2pubmed/xml2pubmed.xsl')
        pubmed_xml_maker.execute_procedures()


def read_inputs(args):
    #args = [arg.decode(encoding=sys.getfilesystemencoding()) for arg in args]
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
