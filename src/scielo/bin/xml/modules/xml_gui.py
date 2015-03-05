import Tkinter


class XMLAppGUI(object):

    def __init__(self, tkFrame, is_converter_enabled, default_xml_path):

        self.tkFrame = tkFrame
        self.default_xml_path = default_xml_path
        self.is_converter_enabled = is_converter_enabled

        self.tkFrame.acron_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.acron_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.folder_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.folder_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.msg_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.msg_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.buttons_labelframe = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.buttons_labelframe.pack(fill="both", expand="yes")

        self.tkFrame.label_acron = Tkinter.Label(self.tkFrame.acron_labelframe, text='Journal acronym:', font="Verdana 12 bold")
        self.tkFrame.label_acron.pack(side='left')
        self.tkFrame.input_acron = Tkinter.Entry(self.tkFrame.acron_labelframe)
        self.tkFrame.input_acron.pack()

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

        if is_converter_enabled:
            self.tkFrame.button_xml_converter = Tkinter.Button(self.tkFrame.buttons_labelframe, text='XML Converter', command=self.run_xml_converter)
            self.tkFrame.button_xml_converter.pack(side='right')

        self.tkFrame.button_xml_package_maker = Tkinter.Button(self.tkFrame.buttons_labelframe, text='XML Package Maker', command=self.run_xml_package_maker)
        self.tkFrame.button_xml_package_maker.pack(side='right')

        self.selected_folder = None

    def open_file_explorer(self):
        from tkFileDialog import askdirectory
        self.selected_folder = askdirectory(parent=self.tkFrame, initialdir=self.default_xml_path, title='Select a SPS XML package folder')
        self.tkFrame.input_folder.config(text=self.selected_folder)

    def read_inputs(self):
        if self.selected_folder is None:
            self.selected_folder = ''
        self.acron = self.tkFrame.input_acron.get()

    def display_message(self, action_name):
        result = self.check_inputs()
        color = 'green' if result else 'red'

        if result:
            msg = 'Executing ' + action_name + ' for ' + self.acron + ' using the files in ' + self.selected_folder + '\n'
        else:
            msg = ''
            if self.acron == '':
                msg += 'Inform the acronym.\n'
            if self.selected_folder == '':
                msg += 'Select a folder which contains the SPS XML Files.\n'
        if len(msg) > 0:
            self.tkFrame.label_msg.config(text=msg, bg=color)
        return result

    def check_inputs(self):
        return (self.acron != '' and self.selected_folder != '')

    def run_xml_package_maker(self):
        self.read_inputs()
        is_valid = self.check_inputs()
        self.display_message('XML Package Maker')
        if is_valid:
            print('xml package maker')

    def run_xml_converter(self):
        self.read_inputs()
        is_valid = self.check_inputs()
        self.display_message('XML Converter')
        if is_valid:
            print('XML Converter')


def open_main_window(configurations=None):
    if configurations is None:
        configurations = {'title': 'SPS XML Package Maker', 'is_converter_enabled': True, 'default_xml_path': '/Users/robertatakenaka/Documents/xml/'}

    tk_root = Tkinter.Tk()
    tk_root.title(configurations['title'])

    tkFrame = Tkinter.Frame(tk_root)

    main = XMLAppGUI(tkFrame, configurations['is_converter_enabled'], configurations['default_xml_path'])
    main.tkFrame.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
    tk_root.focus_set()


if __name__ == "__main__":
    open_main_window()
