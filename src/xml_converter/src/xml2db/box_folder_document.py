import os


from datetime import datetime
from reuse.items_and_id import Items, id_generate

class AllFolders:
    def __init__(self, registered, not_registered, all_folders):
        self.registered = registered
        self.not_registered = not_registered
        self.all_folders = all_folders
        
    def template(self, folder):        
                
        found = self.registered.get(folder.id)
        #print('registered')
        if found == None:
            # folder is not registered (in folder db)
            found = self.not_registered.get(folder.id)
            #print('not registered')
            if found == None:
                # folder is new
                folder.status = 'new'
                self.not_registered.insert(folder, False)    
                found = folder             
            else:
                # folder was at least one processed
                found.status = 'not_registered'        
        else:
            found.status = 'registered'
        #print(found.display())
        #print(found.json_data)
        #print(found.toc.return_json())
        
        
        
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

class Folders(Items):
    def __init__(self):
        Items.__init__(self)
        
class Section:
    def __init__(self, title, code = '', lang = 'en'):
        section_code = self.normalized_title(title)
        self.id = self.generate_id(section_code)
        self.title = title
        if code == '':
            self.code = section_code
        else:
            self.code = code
        self.lang = lang

    def generate_id(self, title):
        return id_generate( title) 

    def normalized_title(self, title):
        return title.replace(' ','').upper()

class TOC(Items):
    def __init__(self):
        Items.__init__(self)

    

    def insert(self, item, replace):

        section = self.return_section(item)
        if section == None:
            section = Items.insert(self, item, replace)
        else:
            if replace:
                section = Items.insert(self, item, replace)
        return section


    def return_json(self):
        r = []
        for key, section in self.elements.items():
            r.append({'l' : section.lang, 'c': section.code, 't': section.title})
        return r

    def return_section(self, _section):
        test = _section.normalized_title(_section.title)
        print( 'teste secoes: ' + _section.title + ' (' + _section.code + ')')
        
        
        
        
        section = None
        for key, sec in self.elements.items():
            
            print(sec.code + ' - '  + sec.title)
            if sec.normalized_title(sec.title) == test:
                section = sec
                break
            elif sec.code == _section.code:
                section = sec
                break
        if section != None:
            print(_section.title)
            print(_section.code)
            print(section.title)
            print(section.code)
            print('matched')
        else:
            print('no match')
        return section

    def display(self):
        
        for key, sec in self.elements.items():
            print(sec.code + ' - '  + sec.title)
            
        
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
        Items.__init__(self)
        
        
    @property
    def count(self):
        return Items.count(self)
           

# abstraction of Journals
class Boxes(Items):
    def __init__(self):
        Items.__init__(self)

    
    def find(self, box_label):
        return self.get(Box(box_label).id)

   
    def return_registered(self, box_label, report):
        if len(box_label) == 0:
            report.write('Missing label in json', True, True)
        else:
            box = self.find(box_label)
            if box == None:
                labels = ''
                for k,t in Items.elements.items():
                    labels += ',' + t.title
                labels = labels[1:]
                report.write(box_label + ' is not registered. '+ '\n' + labels , True, True)
        return box

        