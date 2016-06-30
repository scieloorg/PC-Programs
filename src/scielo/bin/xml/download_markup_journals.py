# coding=utf-8
import os
import csv
import codecs
import shutil

import Tkinter

from modules import ws_requester


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


class MkpDownloadJournalListGUI(object):

    def __init__(self, tkFrame, collections, filename, temp_filename, updated):

        self.tkFrame = tkFrame
        self.collections = collections
        self.filename = filename
        self.temp_filename = temp_filename

        self.tkFrame.folder_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.folder_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.options_frame = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.options_frame.pack(fill="both", expand="yes")

        self.tkFrame.msg_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.msg_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.buttons_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.buttons_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.label_folder = Tkinter.Label(self.tkFrame.folder_labelframe, text=' '*10 + 'Select collection' + ' '*10, font="Verdana 12 bold")
        self.tkFrame.label_folder.pack(side='left')

        #options = collections.keys()
        #self.choice = Tkinter.StringVar(self.tkFrame)
        #self.choice.set(options[0])
        #self.tkFrame.option_menu = apply(Tkinter.OptionMenu, (self.tkFrame.options_frame, self.choice) + tuple(options))
        #self.tkFrame.option_menu.pack()

        options = collections.keys()
        options.append('All')

        self.choice = Tkinter.StringVar(self.tkFrame)
        self.choice.set(options[0])
        self.tkFrame.option_menu = apply(Tkinter.OptionMenu, (self.tkFrame.options_frame, self.choice) + tuple(options))
        self.tkFrame.option_menu.pack()

        self.tkFrame.label_msg = Tkinter.Label(self.tkFrame.msg_labelframe)
        self.tkFrame.label_msg.pack()

        self.tkFrame.button_close = Tkinter.Button(self.tkFrame.buttons_labelframe, text='close', command=lambda: self.tkFrame.quit())
        self.tkFrame.button_close.pack(side='right')

        self.tkFrame.button_execute = Tkinter.Button(self.tkFrame.buttons_labelframe, text='download', command=self.download)
        self.tkFrame.button_execute.pack(side='right')

    def download(self):
        choice = self.choice.get()
        if choice == 'All':
            choice = None
        journals = get_journals_list(self.collections, choice)
        if os.path.isfile(self.temp_filename):
            os.unlink(self.temp_filename)
        generate_input_for_markup(journals, self.temp_filename)
        while not os.path.isfile(self.temp_filename):
            pass

        if os.path.isfile(self.temp_filename):
            shutil.copyfile(self.temp_filename, self.filename)

        self.tkFrame.label_msg.config(text='updated: ' + self.filename, bg='dark green')
        self.tkFrame.label_msg.update_idletasks()


def open_main_window(collections, destination_filename, temp_filename, updated):
    tk_root = Tkinter.Tk()
    tk_root.title('Download journals data')

    tkFrame = Tkinter.Frame(tk_root)
    main = MkpDownloadJournalListGUI(tkFrame, collections, destination_filename, temp_filename, updated)
    main.tkFrame.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
    tk_root.focus_set()


def journals_by_collection(filename):
    collections = {}
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for item in spamreader:
            if len(item) >= 10:
                if item[1] != 'ISSN':
                    j = {}
                    j['collection'] = item[0]
                    j['collection-name'] = item[4]
                    j['issn-id'] = item[1]
                    j['pissn'] = item[2]
                    j['eissn'] = item[3]
                    j['acron'] = item[5]
                    j['short-title'] = item[6]
                    j['journal-title'] = item[7]
                    j['nlm-title'] = item[8]
                    j['publisher-name'] = item[9]
                    if len(item) == 12:
                        j['license'] = item[11]
                    _col = j.get('collection-name')
                    if _col == '':
                        _col = j.get('collection')
                    if not _col in collections.keys():
                        collections[_col] = []
                    collections[_col].append(j)
        if 'Symbol' in collections.keys():
            del collections['Symbol']
        if 'Collection Name' in collections.keys():
            del collections['Collection Name']

    return collections


def get_journals_list(collections, collection_name=None):
    journals = {}
    if collection_name is not None:
        journals = get_collection_journals_list(collections, collection_name)
        if len(journals) == 0:
            _k = collections.keys()[0]
            journals = get_collection_journals_list(collections, _k)
    if len(journals) == 0:
        journals = get_all_journals_list(collections)
    c = []
    for k in sorted(journals.keys()):
        c.append(journals[k])
    return c


def generate_row(item):
    column = []
    column.append(item['journal-title'])
    column.append(item['nlm-title'])
    column.append(item['short-title'])
    column.append(item['acron'])
    column.append(item['issn-id'])
    column.append(item['pissn'])
    column.append(item['eissn'])
    column.append(item['publisher-name'])
    if item.get('license'):
        column.append(item.get('license'))
    return '|'.join(column)


def get_collection_journals_list(collections, collection_name):
    journals = {}
    for item in collections.get(collection_name, []):
        journals[item['journal-title'].lower()] = collection_name + '|' + generate_row(item)
    return journals


def get_all_journals_list(collections):
    journals = {}
    for collection_key, collection_journals in collections.items():
        for item in collection_journals:
            journals[item['journal-title'].lower() + ' | ' + item['collection-name'].lower()] = collection_key + '|' + generate_row(item)
    return journals


def generate_input_for_markup(journals, filename):
    new_items = []
    for item in journals:
        if not isinstance(item, unicode):
            item = item.decode('utf-8')
        new_items.append(item.encode('cp1252'))
    codecs.open(filename, mode='w+').write('\n\r'.join(new_items))


markup_journals_filename = CURRENT_PATH + '/../markup/markup_journals.csv'
temp_markup_journals_filename = CURRENT_PATH + '/../markup/temp_markup_journals.csv'

for filename in [markup_journals_filename, temp_markup_journals_filename]:
    temp_path = os.path.dirname(filename)
    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)

ws_requester.wsr.update_journals_file()

journals_collections = journals_by_collection(ws_requester.wsr.downloaded_journals_filename)
open_main_window(journals_collections, markup_journals_filename, temp_markup_journals_filename, True)
