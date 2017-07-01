# coding=utf-8

import os

try:
    import tkinter as tk
    from tkinter.filedialog import askdirectory
except ImportError:
    import Tkinter as tk
    from tkFileDialog import askdirectory

from ..__init__ import _


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
XML_FOLDER_DEFAULT = CURRENT_PATH + '/../../'


class XMLAppGUI(tk.Frame):

    def __init__(self, tk_root, default_xml_path, is_converter_enabled):
        tk.Frame.__init__(self, tk_root)
        self.tk_root = tk_root
        self.tk_root.iconbitmap('../../../cfg/Scielo.ico')
        if default_xml_path is None:
            self.default_xml_path = XML_FOLDER_DEFAULT
        else:
            self.default_xml_path = default_xml_path

        self.is_converter_enabled = is_converter_enabled
        self.xml_package_maker = xml_package_maker
        self.xml_converter = xml_converter

        self.tk_root.resizable(True, False)
        self.tk_root.protocol('WM_DELETE_WINDOW', self.click_close)
        self.tk_root.bind('<Escape>', self.click_close)

        folder_frame = tk.Frame(self)
        folder_frame.pack(padx=20, pady=15)

        message_frame = tk.Frame(self)
        message_frame.pack(padx=20, pady=15)

        pmc_frame = tk.Frame(self)
        pmc_frame.pack(padx=20, pady=15)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(padx=20, pady=15)

        folder_label = tk.Label(folder_frame, text=_('SPS XML Package Folder:'))
        folder_label.pack(side='left')

        self.selected_folder = tk.StringVar(value='')
        self.input_folder = tk.Label(folder_frame, textvariable=self.selected_folder, anchor='e')
        self.input_folder.pack(side='left')

        choose_button = tk.Button(folder_frame, text=_('choose folder'), command=self.open_file_explorer)
        choose_button.pack()

        if not self.is_converter_enabled:
            self.pmc_var = tk.IntVar()
            self.pmc_checkbutton = tk.Checkbutton(pmc_frame, text=_('generate PMC Package'), variable=self.pmc_var)
            self.pmc_checkbutton.pack()

        self.message = tk.Message(message_frame, font='System 14 bold')
        self.message.pack()

        close_button = tk.Button(buttons_frame, text=_('close'), command=self.click_close)
        close_button.pack(side='right')

        if self.is_converter_enabled:
            xc_button = tk.Button(buttons_frame, default='active', text='XML Converter', command=self.run_xml_converter)
            xc_button.pack(side='right')
        else:
            xpm_button = tk.Button(buttons_frame, default='active', text='XML Package Maker', command=self.run_xml_package_maker)
            xpm_button.pack(side='right')

        self.selected_folder = None

    def click_close(self):
        self.tk_root.destroy()

    def open_file_explorer(self):
        if self.selected_folder is not None:
            self.default_xml_path = self.selected_folder
        self.selected_folder = askdirectory(parent=self.tk_root, initialdir=self.default_xml_path, title=_('Select a SPS XML package folder'))
        self.input_folder.config(text=self.selected_folder)
        self.read_inputs()
        self.display_message(self.selected_folder, 'green')

    def read_inputs(self):
        if self.selected_folder is None:
            self.selected_folder = ''

    def display_message(self, msg, color):
        if len(msg) > 0:
            self.message.config(text=msg, bg=color)
            self.message.update_idletasks()

    def is_valid_folder(self):
        r = (self.selected_folder != '')
        if r:
            r = os.path.isdir(self.selected_folder)
            if r:
                r = (len([item for item in os.listdir(self.selected_folder) if item.endswith('.xml')]) > 0)
            if not r:
                self.selected_folder = ''
        return r

    def run_xml_package_maker(self):
        self.read_inputs()
        color = 'green' if self.is_valid_folder() else 'red'
        msg = ''
        if self.selected_folder == '':
            msg += _('Select a folder which contains the SPS XML Files. ') + '\n'
        if len(msg) == 0:
            msg = _('Executing XML Package Maker for ') + self.selected_folder + '\n'
        self.display_message(msg, color)
        if color == 'green':
            pmc = (self.pmc_var.get() == 1)
            xml_package_maker(self.selected_folder, pmc)

    def run_xml_converter(self):
        self.read_inputs()
        color = 'green' if self.is_valid_folder() else 'red'
        msg = ''
        if self.selected_folder == '':
            msg += _('Select a folder which contains the SPS XML Files. ') + '\n'
        if len(msg) == 0:
            msg = _('Executing XML Converter for ') + self.selected_folder + '\n'
        self.display_message(msg, color)
        if color == 'green':
            xml_converter(self.selected_folder)


def open_main_window(is_converter_enabled, configurations):
    if configurations is None:
        t = 'SPS XML Package Maker'
        if is_converter_enabled:
            t = 'SPS XML Converter'
        configurations = {'title': t}

    tk_root = tk.Tk()
    tk_root.title(configurations['title'])

    app = XMLAppGUI(tk_root, configurations.get('default_xml_path'), is_converter_enabled)
    app.pack(side="top", fill="both", expand=True)

    app.mainloop()
    app.focus_set()


def xml_package_maker(path, pmc=False):
    import xpmaker
    xpmaker.make_packages(path, None, pmc=pmc)


#def xml_converter(path, collection_name):
#    import xmlcvrter
#
#    xmlcvrter.execute_converter(path, COLLECTIONS.get(collection_name))


def xml_converter(path):
    import xmlcvrter

    xmlcvrter.execute_converter(path)


#if __name__ == "__main__":
#    open_main_window()
