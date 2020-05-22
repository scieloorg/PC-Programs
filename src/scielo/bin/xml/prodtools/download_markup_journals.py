# coding=utf-8
import os
import csv
import codecs
import shutil


try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


from prodtools.db import ws_journals
from prodtools.config import config
from prodtools import BIN_MARKUP_PATH
from prodtools import BIN_PATH


class MkpDownloadJournalListGUI(tk.Frame):

    def __init__(self, tk_root, collections, filename, temp_filename, updated):
        tk.Frame.__init__(self, tk_root)
        self.tk_root = tk_root
        self.collections = collections
        self.filename = filename
        self.temp_filename = temp_filename

        collection_frame = tk.Frame(self)
        collection_frame.pack(padx=10, pady=5)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(padx=10, pady=5)

        message_frame = tk.Frame(self)
        message_frame.pack(padx=10, pady=5)

        collection_label = tk.Label(collection_frame, text='Select a collection: ', font="Verdana 12 bold")
        collection_label.pack(side='left')

        execute_button = tk.Button(collection_frame, text='download', command=self.download)
        execute_button.pack(side='right')

        options = ['All']
        options.extend(sorted(collections.keys()))

        self.choice = tk.StringVar(self)
        self.choice.set(options[0])
        #options_menu = tk.OptionMenu(collection_frame, self.choice, *options, command=self.download)
        #options_menu.pack()

        menu_options = apply(tk.OptionMenu, (collection_frame, self.choice) + tuple(options))
        menu_options.pack()

        close_button = tk.Button(buttons_frame, text='close', command=lambda: self.tk_root.destroy())
        close_button.pack(side='right')

        self.message = tk.Message(message_frame)
        self.message.pack(padx=10, pady=5)


    def download(self):
        choice = self.choice.get()
        self.message.config(text=choice, bg='white')
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

        self.message.config(text='done!', bg='white')
        #self.message.update_idletasks()


def open_main_window(collections, destination_filename, temp_filename, updated):
    tk_root = tk.Tk()
    tk_root.iconbitmap(BIN_PATH + '/cfg/Scielo.ico')

    tk_root.title('Download journals data')

    app = MkpDownloadJournalListGUI(tk_root, collections, destination_filename, temp_filename, updated)
    app.pack(side="top", fill="both", expand=True)
    app.focus_set()
    app.mainloop()


def journals_by_collection(filename):
    collections = {}
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for item in spamreader:
            if len(item) >= 10:
                item = [e.decode('utf-8') for e in item]
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
                    if len(item) >= 12:
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


def main():
    configuration = config.Configuration()
    markup_journals_filename = BIN_MARKUP_PATH + '/markup_journals.csv'
    tmp_mkp_journal_filepath = BIN_MARKUP_PATH + '/temp_markup_journals.csv'

    for filename in [markup_journals_filename, tmp_mkp_journal_filepath]:
        temp_path = os.path.dirname(filename)
        if not os.path.isdir(temp_path):
            os.makedirs(temp_path)

    _ws_journals = ws_journals.Journals(configuration.app_ws_requester)
    _ws_journals.update_journals_file()

    journals_collections = journals_by_collection(
        _ws_journals.downloaded_journals_filename)
    open_main_window(
        journals_collections, markup_journals_filename,
        tmp_mkp_journal_filepath, True)


if __name__ == "__main__":
    main()
