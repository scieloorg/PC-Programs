import os
import hashlib

from datetime import datetime
class Journals:
    def __init__(self, registered_journals):
        self.registered_journals = registered_journals

    def return_valid_publication_title(self, journal_title, report):
        journal = None
        if len(journal_title) == 0:
            report.write('Unable to identify journal title in the file', True, True)
        else:
            journal = self.registered_journals.find_journal(journal_title)
            if journal == None:
                titles = ''
                for t in self.journal_list:
                    titles += ',' + t.title
                titles = titles[1:]
                report.write(journal_title + ' was not found in title database. '+ '\n' + titles , True, True)
            
        return journal
    
class Issues:
    def __init__(self, registered_issues, not_registered_issues):
        self.registered_issues = registered_issues
        self.not_registered_issues = not_registered_issues

    def box(self, issue):        
        found = self.registered_issues.get(issue.id)
        if found == None:
            # issue is not registered (in issue db)
            found = self.not_registered_issues.get(issue.id)
            if found == None:
                # issue is new
                issue.status = 'new'
                self.not_registered_issues.insert(issue, False)    
                found = issue             
            else:
                # issue was at least one processed
                found.status = 'not_registered'        
        else:
            found.status = 'registered'
            
        return found


    def return_incoherences(self, issue_in_db, issue_in_file):

        def return_invalid_value_msg(self, label, invalid_value, correct_value = ''):
            r =  invalid_value + ' is not a valid ' + label 
            if len(correct_value) > 0:
                r += '. Expected: ' + correct_value
            return r 


        errors = []
        
        items = {}
        items['ISSN'] = (issue_in_db.journal.issn_id, issue_in_file.journal.issn_id)
        items['journal title'] = (issue_in_db.journal.title, issue_in_file.journal.title)
        items['acron'] = (issue_in_db.journal.acron, issue_in_file.journal.acron)
        items['issue'] = (issue_in_db.journal.acron + ' ' + issue_in_db.name, issue_in_file.journal.acron + ' ' + issue_in_file.name)
        items['dateiso'] = (issue_in_db.dateiso, issue_in_file.dateiso)
        
        for key, item in items.items():
            if item[0] != item[1]:
                errors.append(return_invalid_value_msg(key, item[1], item[0]))
        return errors

class ID:
    def __init__(self):
        pass

    def generate(self, s):
        return hashlib.md5(s).hexdigest()


class Items:
    def __init__(self):
        self.elements = {}
        
    def __iter__(self):
        for elem in self.elements.values():
            yield elem
        
    

    def insert(self, item, replace):
        try:
            id = item.id
        except:
            id = ID().generate( datetime.now().isoformat())
            item.id = id
        if id in self.elements.keys():
            if replace == True:
                self.elements[id] = item
        else:
            self.elements[id] = item
        return self.elements[id]
        

    def get(self, id):
        r = None
        if id in self.elements.keys():
            r = self.elements[id]
        return r
    
class TOC(Items):
    def __init__(self):
        Items.__init__(self)

    def return_json(self):
        r = []
        for key, section in self.elements.items():
            r.append({'l' : 'en', 'c': section.code, 't': section.title})
        return r




class JournalIssueArticles(Items):
    def __init__(self):
        Items.__init__(self)

    def return_sorted(self):
        elements = {}
        for k, elem in self.elements.items():
            elements[elem.page] = elem

        keys = elements.keys()
        sort(keys)

        r = []
        for key in keys:
            r.append(elements[key])
        return r

class JournalIssues(Items):
    def __init__(self):
        Items.__init__(self)

class Section:
    def __init__(self, title):
        self.id = self.generate_id( title)
        self.title = title
        self.code = self.title.replace(' ','_').upper()

    def generate_id(self, title):
        return ID().generate( title) 


class Journal:
    def __init__(self, journal_title, issn_id = '', acron = ''):
        self.title = journal_title
        
        self.id = self.generate_id(journal_title)
        self.issn_id = issn_id
        self.acron = acron

    def generate_id(self, journal_title):
        return ID().generate( journal_title)
 
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
    def __init__(self, journal, volume, number, dateiso, suppl, order):
        self.volume = volume
        self.number = number
        self.dateiso = dateiso
        self.suppl = suppl
        self.toc = TOC()
        self.journal = journal
        self.id = self.generate_id( journal, volume, number, dateiso, suppl)
        self.articles = JournalIssueArticles()
        
        self.status = ''
        

        self.json_from_db = {}
        if order != '':
            self.order = order
        else:
            self.order = dateiso[0:4] + JournalIssueOrder().generate(volume, number, suppl)

        label = ''
        if number in ['ahead', 'review']:
            label = dateiso[0:4]
        if volume != '':
            label += 'v' + volume
        if number != '':
            label += 'n' + number
        if suppl != '':
            label += 's' + suppl 

        self.name = label
        self.json_data = {}
    
    def generate_id(self, journal, volume, number, dateiso, suppl):
        return ID().generate( journal.title + volume + number + dateiso + suppl)
    
    @property 
    def documents(self):
        return self.articles


class Article:
    def __init__(self, first_page, last_page = ''):
        self.id = self.generate_id(first_page)
        self.issue = None
        self.json_data = {}
        self.xml_filename = xml_filename
        self.titles = []
        self.authors = []
        self.first_page = first_page
        self.last_page = last_page
        self.section_title = ''
        self.section_code = ''
    @property 
    def box(self):
        return self.issue 
    
    def generate_id(self, first_page):
        first_page = '0' * 10 + first_page
        first_page = first_page[-5:]
        
        return ID().generate( first_page)

    def display(self, display_labels = True):
        label_titles = 'Titles: '
        label_authors = 'Authors: '

        if not display_labels:
            label_titles = ''
            label_authors = ''

        text = '\n'

        if self.issue != None:
            text += self.issue.journal.title + ' ' + self.issue.name 

        text += ' ' + self.pages + '\n' * 2
        

        text += label_titles + '\n'.join(self.titles) + '\n' * 2
        text += label_authors + '; '.join(self.authors) + '\n' * 2

        return text

class JournalList(Items):
    def __init__(self):
        Items.__init__(self)

    
    def find_journal(self, journal_title):
        return self.get(Journal(journal_title).id)


    
