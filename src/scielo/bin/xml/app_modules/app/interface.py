# coding=utf-8

import os

import tkinter as tk
from tkinter.filedialog import askdirectory

from ..__init__ import _
from ..__init__ import BIN_PATH
from ..generics import encoding


XML_FOLDER_DEFAULT = BIN_PATH


class XMLAppGUI(tk.Frame):

    def __init__(self, tk_root, default_xml_path, is_converter_enabled, function):
        super().__init__(tk_root)
        self.tk_root = tk_root
        self.tk_root.iconbitmap(BIN_PATH+'/cfg/Scielo.ico')
        if default_xml_path is None:
            self.default_xml_path = XML_FOLDER_DEFAULT
        else:
            self.default_xml_path = default_xml_path

        self.is_converter_enabled = is_converter_enabled
        self.generate_pmc_package = False
        self.xml_path = None
        self.function = function

        self.tk_root.resizable(True, False)
        self.tk_root.protocol('WM_DELETE_WINDOW', self.click_close)
        #self.tk_root.bind('<Escape>', self.click_close)

        folder_label_frame = tk.Frame(self)
        folder_label_frame.pack(padx=10, pady=5)

        message_frame = tk.Frame(self)
        message_frame.pack(padx=10, pady=5)

        pmc_frame = tk.Frame(self)
        pmc_frame.pack(padx=10, pady=5)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(padx=10, pady=5)

        folder_label = tk.Label(folder_label_frame, text=_('SPS XML Package Folder:'))
        folder_label.pack(side='left')

        self.selected_folder = tk.StringVar(value='')
        self.input_folder = tk.Label(folder_label_frame, textvariable=self.selected_folder, anchor='e', width=100, bd=1, bg='gray')
        self.input_folder.pack(side='left')

        choose_button = tk.Button(folder_label_frame, text=_('choose folder'), command=self.open_file_explorer)
        choose_button.pack(side='left')

        if not self.is_converter_enabled:
            self.pmc_var = tk.IntVar()
            self.pmc_checkbutton = tk.Checkbutton(pmc_frame, text=_('generate PMC Package'), variable=self.pmc_var)
            self.pmc_checkbutton.pack()

        self.message = tk.Label(message_frame, width=100, bd=1, bg='gray')
        self.message.pack(side='left')

        close_button = tk.Button(self.buttons_frame, text=_('close'), command=self.click_close)
        close_button.pack(side='right')

        if self.is_converter_enabled:
            self.xc_button = tk.Button(self.buttons_frame, default='active', text='XML Converter', command=self.run_xml_converter)
            self.xc_button.pack(side='right')
        else:
            self.xpm_button = tk.Button(self.buttons_frame, default='active', text='XML Package Maker', command=self.run_xml_package_maker)
            self.xpm_button.pack(side='right')

        self.selected_folder = None

    def click_close(self):
        self.tk_root.destroy()

    def open_file_explorer(self):
        if self.selected_folder is not None:
            self.default_xml_path = self.selected_folder
        self.selected_folder = askdirectory(parent=self.tk_root, initialdir=self.default_xml_path, title=_('Select a SPS XML package folder'))
        msg, color = self.validate_folder()
        self.display_message(msg, color)

    def display_message(self, msg, color):
        if len(msg) > 0:
            self.message.config(text=msg, bg=color)
            self.message.update_idletasks()

    def is_valid_folder(self):
        if self.selected_folder is not None:
            if os.path.isdir(self.selected_folder) is True:
                items = [item for item in os.listdir(self.selected_folder) if item.endswith('.xml')]
                return len(items) > 0
        return False

    def validate_folder(self):
        msg = self.selected_folder
        color = 'white'
        if not self.is_valid_folder():
            msg = _('Invalid folder. ') + _('No .xml files was found')
            color = 'yellow'
        return msg, color

    def run_xml_package_maker(self):
        if self.is_valid_folder():
            self.started()
            self.generate_pmc_package = self.pmc_var.get() == 1
            msg, color = self.function(self.selected_folder, self.generate_pmc_package)
            self.display_message(msg, color)
            self.finished(color)

    def run_xml_converter(self):
        if self.is_valid_folder():
            self.started()
            msg, color = self.function(self.selected_folder)
            self.finished(color)

    def started(self):
        encoding.display_message(_('Processing...'))
        self.display_message(_('Processing...'), 'white')
        self.tk_root.config(cursor="wait")

    def finished(self, color):
        encoding.display_message(_('Finished!'))
        self.display_message(_('Finished!'), color)
        self.tk_root.config(cursor="")


def display_form(is_converter_enabled, configurations, function):
    if configurations is None:
        t = 'SPS XML Package Maker'
        if is_converter_enabled:
            t = 'SPS XML Converter'
        configurations = {'title': t}

    tk_root = tk.Tk()
    tk_root.title(configurations['title'])

    app = XMLAppGUI(tk_root, configurations.get('default_xml_path'), is_converter_enabled, function)
    app.pack(side="top", fill="both", expand=True)
    app.focus_set()
    app.mainloop()
    return app
