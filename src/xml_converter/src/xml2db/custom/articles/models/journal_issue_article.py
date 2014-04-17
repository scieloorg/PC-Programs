import os
import hashlib

from reuse.items_and_id import id_generate, Items
from xml2db.box_folder_document import Documents, TOC
from datetime import datetime


class JournalsList(Items):
    def __init__(self):
        super(JournalsList, self).__init__()

    def key(self, item):
        return item.title.upper().replace(' ', '')

    def return_registered(self, journal_title):
        return self.find(Journal(journal_title))


class JournalIssuesList(Items):
    def __init__(self):
        super(JournalIssuesList, self).__init__()

    def key(self, item):
        k = item.journal.title + item.name
        return k.upper().replace(' ', '')


class AllIssues:
    def __init__(self):
        pass
        
    def compare(self, issue_in_db, issue_in_file):
        items = {}
        #items['order'] = (issue_in_db.order, issue_in_file.order)
        items['ISSN'] = (issue_in_db.journal.issn_id, issue_in_file.journal.issn_id)
        items['journal title'] = (issue_in_db.journal.title, issue_in_file.journal.title)
        items['publishers'] = (issue_in_db.journal.publishers, issue_in_file.journal.publishers)
        items['acron'] = (issue_in_db.journal.acron, issue_in_file.journal.acron)
        items['issue'] = (issue_in_db.journal.acron + ' ' + issue_in_db.name, issue_in_file.journal.acron + ' ' + issue_in_file.name)
        
        if not 'ahead' in issue_in_file.name:
            items['dateiso'] = (issue_in_db.dateiso, issue_in_file.dateiso)
        
        return items

    

class Journal:
    def __init__(self, journal_title, issn_id = '', acron = ''):
        self.title = journal_title
        
        self.id = self.generate_id(journal_title)
        self.issn_id = issn_id
        self.acron = acron
        self.publishers = ''
        self.abbrev_title = ''

    def generate_id(self, journal_title):
        return id_generate( journal_title.strip())
 
class JournalIssueOrder:
    def __init__(self):
        #self.order = ( [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23], [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24], range(37,49))
        #self.order = ( [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23], range(25,37), range(37,49), [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],)
        #self.order = range(1,50)
        pass

    def generate(self, volume, number, suppl):
        
        if number == 'ahead':
            r = '9050'

        elif number == 'review':
            r = '9075'
        else:
            if suppl != '':
                if suppl.isdigit():
                    s = '0000' + suppl
                else:
                    digits = [ digit for digit in suppl if digit.isdigit()]
                    s = '0000' + ''.join(digits)

                if number != '':
                    r = '3'
                else:
                    r = '2'
            else:
                r = '1'
                s = '0000' + number
            r = r + s[-3:]
        return r

class JournalIssue:
    def __init__(self, journal, volume, number, dateiso, suppl, compl, order):
        self.volume = volume
        self.number = number
        self.dateiso = dateiso
        self.suppl = suppl
        self.toc = TOC()
        self.journal = journal
        self.articles = None
        self.compl = compl
        self.status = ''
        
        if volume.replace('0', '') == '':
            self.volume = ''
        if number.replace('0', '') == '':
            self.number = ''
        if self.volume == '' and self.number == '':
            self.number = 'ahead'
            if self.journal.acron == 'bjmbr' and int(self.dateiso[0:4]) <= 2012:
                self.number = 'review'

        self.json_from_db = {}

        self.id = self.generate_id( journal, self.volume, self.number, self.suppl, self.compl, self.dateiso[0:4])
        

        if order != '':
            self.order = order
        else:
            self.order = dateiso[0:4] + JournalIssueOrder().generate(self.volume, self.number, self.suppl)

        label = ''
        if self.number in ['ahead', 'review']:
            label = dateiso[0:4]
        if self.volume != '':
            label += 'v' + self.volume
        if self.number != '':
            label += 'n' + self.number
        if self.suppl != '':
            label += 's' + self.suppl 
        if self.compl != '':
            label += self.compl
        self.name = label
        self.json_data = {}
    
    def generate_id(self, journal, volume, number, suppl, compl, year):
        return id_generate( journal.title + '-' +  volume + '-' +  number  + '-' +  suppl + '-' +  compl + '-' +  year)
    
    @property 
    def box(self):
        return self.journal

    @property
    def documents(self):
        return self.articles
        
    @documents.setter
    def documents(self, articles):
        self.articles = articles



    def display(self):
        return self.journal.acron + ' ' + self.name

    @property 
    def json_data(self):
        if self.articles == None:
            count = 0
        else:
            count = len(self.articles.elements)
        self.json_data['122'] = str(count) #str(len(document.folder.documents.elements))
        self.json_data['49'] = self.toc.return_json()
        self.json_data['36'] = self.order
        self.json_data['65'] = self.dateiso
        return self.json_data


class Article:
    def __init__(self, doi, order, first_page, last_page):
        #self.id = self.generate_id(data4id)
        self.issue = None
        self.json_data = {}
        self.xml_filename = ''
        self.titles = []
        self.authors = []
        self.first_page = first_page
        self.last_page = last_page
        self.section = None
        self.doi = doi
        self.order = order
        self.display_data = {}
        self.display_order = []
        self.previous_id = ''

    @property
    def key(self):
        if self.doi:
            return self.doi
        else:
            return self.issue.journal.title + self.issue.name + self.order

    @property
    def folder(self):
        return self.issue 

    @folder.setter
    def folder(self, folder):
        self.issue = folder 

    

    def set_previous_id(self, prev_id):
        if len(prev_id) == 23 and not '.' in prev_id:
            self.previous_id = prev_id
            self.json_data['f']['881'] = prev_id
            self.json_data['h']['881'] = prev_id
            

    @property 
    def pages(self):
        return self.first_page + '-' + self.last_page

    def generate_id(self, data4id):
        
        return id_generate( data4id)

    def display(self, display_labels = True):
        r = '\n'
        if len(self.display_order) == 0:
            for label, value in self.display_data.items():
                r += label + ': ' + value + '\n'
        else:
            for key in self.display_order:
                r += key  + ': ' 
                if key in self.display_data.keys():
                    if '\n' in self.display_data[key]:
                        r += '\n'
                    r += self.display_data[key]  
                r += '\n'
        return r
