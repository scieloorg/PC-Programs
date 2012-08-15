import hashlib

from datetime import datetime

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
        self.id = ID().generate( title)
        self.title = title
        self.code = self.title.replace(' ','_').upper()

    def generate_id(self, title):
        return ID().generate( title) 


class Journal:
    def __init__(self, journal_title, issn_id = '', acron = ''):
        self.title = journal_title
        
        self.id = ID().generate(journal_title)
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
                s = '0000' + suppl
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
        self.id = ID().generate( journal.title + volume + number + dateiso + suppl)
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
    
    def return_invalid_value_msg(self, label, invalid_value, correct_value = ''):
        r =  invalid_value + ' is not a valid ' + label 
        if len(correct_value) > 0:
            r += '. Expected: ' + correct_value
        return r 

    def is_valid(self, correct_issue):
        errors = []
        
        items = {}
        items['ISSN'] = (correct_issue.journal.issn_id, self.journal.issn_id)
        items['journal title'] = (correct_issue.journal.title, self.journal.title)
        items['acron'] = (correct_issue.journal.acron, self.journal.acron)
        items['issue'] = (correct_issue.journal.acron + ' ' + correct_issue.name, self.journal.acron + ' ' + self.name)
        items['dateiso'] = (correct_issue.dateiso, self.dateiso)
        
        for key, item in items.items():
            if item[0] != item[1]:
                errors.append(self.return_invalid_value_msg(key, item[1], item[0]))
        return errors
    
    

class Article:
    def __init__(self, issue, page, author):
        self.id = ID().generate( issue.id + page)
        self.issue = issue
        self.json_data = {}
        self.page = '0' * 10 + page
        self.page = self.page[-5:]
        self.xml_filename = ''

    def generate_id(self, issue, page, author):
        return ID().generate( issue.id + page + author)

    def is_valid(self):
        errors = [] 
        warnings = [] 
        if '70' in self.json_data['f'].keys():
            list = []
            if type(self.json_data['f']['70']) == type({}):
                list.append(self.json_data['f']['70'])
            elif type(self.json_data['f']['70']) == type([]):
                list = self.json_data['f']['70']
            for aff in list:
                if not 'p' in aff:
                    print(' ???? incomplete affiliation ????')
                    print(aff)
                    warnings.append('Incomplete affiliation' )
        return (errors, warnings)

class JournalList(Items):
    def __init__(self):
        Items.__init__(self)

        f = open('inputs/table_journals.seq', 'r')
        rows = f.readlines()
        f.close()

        for row in rows:
            if '|' in row:
                title, issn, acron = row.replace("\n", '').split('|')
                j = Journal(title.strip(), issn.strip(), acron.strip())
                self.insert(j, False)

    def find_journal(self, journal_title):
        return self.get(Journal(journal_title).id)

