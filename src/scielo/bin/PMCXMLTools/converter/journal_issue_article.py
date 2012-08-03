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
            r.append({'l' : 'en'})
        return json_data




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
    

class JournalIssue:
    def __init__(self, journal, volume, number, dateiso, suppl = None):
        self.volume = volume
        self.number = number
        self.dateiso = dateiso
        self.suppl = suppl
        self.toc = TOC()
        self.journal = journal
        self.id = ID().generate( journal.title + volume + number + dateiso + suppl)
        self.articles = JournalIssueArticles()

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
    

    


class Article:
    def __init__(self, issue, page, author):
        self.id = ID().generate( issue.id + page)
        self.issue = issue
        self.json_data = {}
        self.page = '0' * 10 + page
        self.page = self.page[-5:]

    def generate_id(self, issue, page, author):
        return ID().generate( issue.id + page + author)

class JournalList(Items):
    def __init__(self):
        Items.__init__(self)

        f = open('table_journals.seq', 'r')
        rows = f.readlines()
        f.close()

        for row in rows:
            if '|' in row:
                title, issn, acron = row.replace("\n", '').split('|')
                j = Journal(title.strip(), issn.strip(), acron.strip())
                self.insert(j, False)

    def find_journal(self, journal_title):
        return self.get(Journal(journal_title).id)

