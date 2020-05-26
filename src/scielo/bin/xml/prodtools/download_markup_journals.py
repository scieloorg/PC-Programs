# coding=utf-8
import os
import csv
import codecs
import shutil

import tkinter as tk
from tkinter import ttk

from prodtools.db import ws_journals
from prodtools.config import config
from prodtools import BIN_MARKUP_PATH
from prodtools import ICON
from prodtools import _


ROW_MSG = 9
ROW_SELECT_A_COLLECTION = 9
ROW_COMBOBOX = 10
ROW_SELECTED = 11
ROW_DOWNLOADING = 12
ROW_DOWNLOADED = 13
ROW_FINISHED = 14
ROW_DOWNLOAD_BUTTON = 21
ROW_CLOSE_BUTTON = 22


class MkpDownloadJournalListGUI(tk.Frame):
    def __init__(self, master, collections, filename, temp_filename):
        super().__init__(master)
        self.master = master

        self.collections = collections
        self.filename = filename
        self.temp_filename = temp_filename

    def configure(self):
        self.master.minsize(400, 200)
        self.master.title(_('Download journals data'))
        self.master.wm_iconbitmap(ICON)
        self.pack()

        label = ttk.Label(self, text=_('Select a collection:'))
        label.grid(column=0, row=ROW_SELECT_A_COLLECTION)

        options = ['All']
        options.extend(sorted(self.collections.keys()))
        self.choice = tk.StringVar(self)
        self.choice.set(options[0])
        combobox = ttk.Combobox(
            self, width=30, textvariable=self.choice)
        combobox['values'] = tuple(options)
        combobox.grid(column=0, row=ROW_COMBOBOX)

        execute_button = ttk.Button(
            self, text=_('download'), command=self.download)
        execute_button.grid(column=0, row=ROW_DOWNLOAD_BUTTON)

        close_button = ttk.Button(
            self, text=_('close'),
            command=lambda: self.master.destroy())
        close_button.grid(column=0, row=ROW_CLOSE_BUTTON)
        self.mainloop()

    def download(self):
        choice = self.choice.get()

        msg = ttk.Label(self,
                        text=_("Select one collection to use its journals "
                               "data for the Markup Program"))
        msg.grid(column=0, row=ROW_MSG)

        label1 = ttk.Label(
            self, text=_("Selecionado: {}".format(choice)))
        label1.grid(column=0, row=ROW_SELECTED)

        if choice == 'All':
            choice = None
        label2 = ttk.Label(self, text=_("Downloading.."))
        label2.grid(column=0, row=ROW_DOWNLOADING)
        journals = get_journals_list(self.collections, choice)
        generate_input_for_markup(journals, self.temp_filename, self.filename)

        label4 = ttk.Label(
            self, text=_("Downloaded: {} journals").format(len(journals)))
        label4.grid(column=0, row=ROW_DOWNLOADED)

        label3 = ttk.Label(self, text=_("Finished"))
        label3.grid(column=0, row=ROW_FINISHED)


def open_main_window(
        collections, destination_filename, temp_filename):
    root = tk.Tk()
    app = MkpDownloadJournalListGUI(
        root, collections, destination_filename, temp_filename)
    app.configure()
    #app.mainloop()


def journals_by_collection(filename):
    collections = {}
    with open(filename, 'r', encoding="utf-8") as csvfile:
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
                    if len(item) >= 12:
                        j['license'] = item[11]
                    _col = j.get('collection-name')
                    if _col == '':
                        _col = j.get('collection')
                    if _col not in collections.keys():
                        collections[_col] = []
                    collections[_col].append(j)
        if 'Symbol' in collections.keys():
            del collections['Symbol']
        if 'Collection Name' in collections.keys():
            del collections['Collection Name']

    return collections


def get_journals_list(collections, collection_name=None):
    journals = {}

    if collection_name:
        journals = get_collection_journals_list(collections, collection_name)

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


def generate_input_for_markup(journals, tmp_filepath, journals_filepath):
    if os.path.isfile(tmp_filepath):
        os.unlink(tmp_filepath)

    content = "\r\n".join(journals)
    with codecs.open(tmp_filepath.replace(".csv", ".utf8.csv"),
                     mode='w+', encoding="utf-8") as fp:
        fp.write(content)

    content = content.encode("cp1252")
    content = content.decode("cp1252")
    with codecs.open(tmp_filepath, mode='w+', encoding="cp1252") as fp:
        fp.write(content)

    if os.path.isfile(tmp_filepath):
        shutil.copyfile(tmp_filepath, journals_filepath)


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
        tmp_mkp_journal_filepath)


if __name__ == "__main__":
    main()
