import os


from datetime import datetime
from reuse.items_and_id import Items, id_generate


class AllFolders:
    def __init__(self, registered, not_registered, all_folders):
        self.registered = registered
        self.not_registered = not_registered
        self.all_folders = all_folders

    def template(self, folder):
        found = self.registered.find(folder)
        print('template')
        print(found)
        if found is None:
            # folder is not registered (in folder db)
            found = self.not_registered.find(folder)
            #print('not registered')
            if found is None:
                # folder is new
                folder.status = 'new'
                self.not_registered.insert(folder, False)
                found = folder
            else:
                # folder was at least one processed
                found.status = 'not_registered'
        else:
            found.status = 'registered'

        return found

    def return_incoherences(self, registered, in_the_file):

        def return_invalid_value_msg(label, in_test_value, registered_value):
            r = ' '*4 + in_test_value + ' is invalid for ' + label + '.'

            if len(registered_value) > 0:
                r += ' It should be: ' + registered_value
            return r 


        errors = []
        
        items = self.all_folders.compare(registered, in_the_file)
        
        for key, item in items.items():
            if item[0] != item[1]:
                errors.append(return_invalid_value_msg(key, item[1], item[0]))
                
        return errors


class Section:
    def __init__(self, title, code='', lang='en'):
        section_code = self.normalized_title(title)
        self.id = self.generate_id(section_code)
        self.title = title
        if code == '':
            self.code = section_code
        else:
            self.code = code
        self.lang = lang

    def generate_id(self, title):
        return id_generate(title) 

    def normalized_title(self, title):
        return title.replace(' ', '').upper()


# class TOC:
#     def __init__(self):
#         self.section_by_title = {}
#         self.section_by_code = {}

#     def insert(self, item, replace):
#         section = self.return_section(item)
#         if section is None or replace:
#             test = item.title.upper().replace(' ', '')
#             self.section_by_title[test] = item

#             if item.lang != '' and item.code != '':
#                 self.section_by_code[item.lang + item.code] = item
#         return section

#     def return_json(self):
#         r = []
#         for key, section in self.section_by_title.items():
#             r.append({'l': section.lang, 'c': section.code, 't': section.title})
#         return r

#     def return_section(self, _section):
#         section = None
#         if _section.title:
#             test = _section.title.upper().replace(' ', '')
#             section = self.section_by_title.get(test)
#         if not section and _section.code != '' and _section.lang != '':
#             section = self.section_by_code.get(_section.lang + _section.code)
#         return section

#     def return_sections(self):
#         return '\n'.join([section.title for section in self.section_by_code.values()])

#     def display(self):
#         for key, sec in self.section_by_title.items():
#             print(sec.code + ' - ' + sec.title)
class TOC:
    def __init__(self):
        self.section_by_title = {}
        self.section_by_langcode = {}

    def _normalize(self, s):
        s = s.upper().replace(' ', '')
        s = ''.join([c for c in s if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'])

        return s

    def insert(self, item, replace):
        section = self.return_section(item)
        if section is None or replace:
            self.section_by_title[self._normalize(item.title)] = item
            if item.lang:
                self.section_by_langcode[self._normalize(item.lang + item.code)] = item

    def return_json(self):
        r = []
        for key, section in self.section_by_title.items():
            r.append({'l': section.lang, 'c': section.code, 't': section.title})
        return r

    def return_section(self, _section):
        langcode = self._normalize(_section.lang + _section.code)
        title = self._normalize(_section.title)
        return self.section_by_title.get(title, self.section_by_langcode.get(langcode, None))

    def return_sections(self):
        return '; '.join([section.title for section in self.section_by_langcode.values()])

    def display(self):
        for key, sec in self.section_by_title.items():
            print(sec.code + ' - ' + sec.title)

class Box:
    def __init__(self, box):
        self.box = box
        self.id = box.id
        self.acron = box.acron
        self.title = box.title


class Document:
    def __init__(self, document):
        self.document = document
        self.section = document.section
        self.folder = document.folder

    def display(self):
        return self.document.display()


# abstract of issue
class Folder:
    def __init__(self, folder):
        self.folder = folder
        self.name = self.folder.name 
        self.toc = self.folder.toc 
        self.box = self.folder.box 
        self.id = self.folder.id 
        self.documents = self.folder.documents
        self.json_data = self.folder.json_data


class Documents(Items):
    def __init__(self):
        super(Documents, self).__init__()

    def key(self, item):
        return item.key.upper().replace(' ', '')


class Folders(Items):
    def __init__(self):
        super(Folders, self).__init__()


# abstraction of Journals
class Boxes(Items):
    def __init__(self):
        super(Boxes, self).__init__()

    def key(self, item):
        return item.title.upper().replace(' ', '')

    def return_registered(self, box, report):
        if box.title == '':
            report.write('Missing label in json', True, True)
        else:
            box = self.find(box)
            if box is None:
                report.write(box.title + ' is not registered.', True, True)
        return box
