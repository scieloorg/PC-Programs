# coding=utf-8

import os

import Tkinter
import ttk


CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')
XML_FOLDER_DEFAULT = CURRENT_PATH + '/../../'

COLLECTIONS_NAMES = ('Brasil', 'Salud Publica')
COLLECTIONS = {'Brasil': 'scl', 'Salud Publica': 'spa', }


class XMLAppGUI(object):

    def __init__(self, tkFrame, default_xml_path, is_converter_enabled):

        self.tkFrame = tkFrame

        if default_xml_path is None:
            self.default_xml_path = XML_FOLDER_DEFAULT
        else:
            self.default_xml_path = default_xml_path

        self.is_converter_enabled = is_converter_enabled
        self.xml_package_maker = xml_package_maker
        self.xml_converter = xml_converter

        if self.is_converter_enabled:
            self.tkFrame.collection_name_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
            self.tkFrame.collection_name_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.acron_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.acron_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.folder_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.folder_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.msg_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.msg_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.buttons_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.buttons_labelframe.pack(fill="both", expand="yes")

        if self.is_converter_enabled:
            self.tkFrame.label_collection_name = Tkinter.Label(self.tkFrame.collection_name_labelframe, text='Collection:', font="Verdana 12 bold")
            self.tkFrame.label_collection_name.pack(side='left')
            self.tkFrame.input_collection_name = ttk.Combobox(self.tkFrame.collection_name_labelframe, values=COLLECTIONS_NAMES)
            self.tkFrame.input_collection_name.pack(side='left')

        self.tkFrame.label_acron = Tkinter.Label(self.tkFrame.acron_labelframe, text='Journal acronym:', font="Verdana 12 bold")
        self.tkFrame.label_acron.pack(side='left')
        self.tkFrame.input_acron = Tkinter.Entry(self.tkFrame.acron_labelframe)
        self.tkFrame.input_acron.pack(side='left')

        self.tkFrame.label_folder = Tkinter.Label(self.tkFrame.folder_labelframe, text='SPS XML Package Folder:', font="Verdana 12 bold")
        self.tkFrame.label_folder.pack(side='left')
        self.tkFrame.input_folder = Tkinter.Label(self.tkFrame.folder_labelframe, width=50, bd=1, bg='gray')
        self.tkFrame.input_folder.pack(side='left')
        self.tkFrame.button_choose = Tkinter.Button(self.tkFrame.folder_labelframe, text='choose folder', command=self.open_file_explorer)
        self.tkFrame.button_choose.pack()

        self.tkFrame.label_msg = Tkinter.Label(self.tkFrame.msg_labelframe)
        self.tkFrame.label_msg.pack()

        self.tkFrame.button_close = Tkinter.Button(self.tkFrame.buttons_labelframe, text='close', command=lambda: self.tkFrame.quit())
        self.tkFrame.button_close.pack(side='right')

        if self.is_converter_enabled:
            self.tkFrame.button_xml_converter = Tkinter.Button(self.tkFrame.buttons_labelframe, text='XML Converter', command=self.run_xml_converter)
            self.tkFrame.button_xml_converter.pack(side='right')

        self.tkFrame.button_xml_package_maker = Tkinter.Button(self.tkFrame.buttons_labelframe, text='XML Package Maker', command=self.run_xml_package_maker)
        self.tkFrame.button_xml_package_maker.pack(side='right')

        self.selected_folder = None
        self.collection_name = None

    def open_file_explorer(self):
        from tkFileDialog import askdirectory
        self.selected_folder = askdirectory(parent=self.tkFrame, initialdir=self.default_xml_path, title='Select a SPS XML package folder')
        self.tkFrame.input_folder.config(text=self.selected_folder)
        self.display_message(self.acron + '\n' + self.selected_folder, 'green')

    def read_inputs(self):
        if self.selected_folder is None:
            self.selected_folder = ''
        self.acron = self.tkFrame.input_acron.get()
        if self.is_converter_enabled:
            self.collection_name = self.tkFrame.input_collection_name.current()

    def display_message(self, msg, color):
        if len(msg) > 0:
            self.tkFrame.label_msg.config(text=msg, bg=color)
            self.tkFrame.label_msg.update_idletasks()

    def get_message(self, action_name, result):
        if result:
            msg = 'Executing ' + action_name + ' for ' + self.acron + ' using the files in ' + self.selected_folder + '\n'
        else:
            msg = ''
            if self.acron == '':
                msg += 'Inform the acronym.\n'
            if self.selected_folder == '':
                msg += 'Select a folder which contains the SPS XML Files.\n'
        return msg

    def check_inputs(self):
        r = (self.acron != '' and self.selected_folder != '')
        if r:
            r = os.path.isdir(self.selected_folder)
            if r:
                r = (len([item for item in os.listdir(self.selected_folder) if item.endswith('.xml')]) > 0)
            if not r:
                self.selected_folder = ''
        return r

    def is_app_ready(self, title):
        self.read_inputs()
        is_valid = self.check_inputs()
        result = self.check_inputs()
        color = 'green' if result else 'red'
        self.display_message(self.get_message(title, result), color)
        return is_valid

    def run_xml_package_maker(self):
        if self.is_app_ready('XML Package Maker'):
            xml_package_maker(self.selected_folder, self.acron)

    def run_xml_converter(self):
        if self.is_app_ready('XML Converter'):
            xml_converter(self.selected_folder, self.collection_name)


def open_main_window(is_converter_enabled, configurations):
    if configurations is None:
        configurations = {'title': 'SPS XML Package Maker', }

    tk_root = Tkinter.Tk()
    tk_root.title(configurations['title'])

    tkFrame = Tkinter.Frame(tk_root)

    main = XMLAppGUI(tkFrame, configurations.get('default_xml_path'), is_converter_enabled)
    main.tkFrame.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
    tk_root.focus_set()


def xml_package_maker(path, acron):
    import xpmaker

    xpmaker.make_packages(path, acron)


def xml_converter(path, collection_name):
    import xmlcvrter

    xmlcvrter.execute_converter(path, COLLECTIONS.get(collection_name))


#if __name__ == "__main__":
#    open_main_window()
