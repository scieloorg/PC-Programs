
from isis_record import ISISRecord

from journal import Journal
from journal_issue import JournalIssue
from journal_article import JournalArticle

class Article_ISISRecord:

    isisRecord = ISISRecord()

    def __init__(self, param_journal, param_issue, param_articles):
        self.journal = param_journal
        self.issue = param_issue
        self.articles = param_articles
        
    
    def generate_records(self):
        r = []
        r.append(self.get_o())
        r.append(self.get_h())
        r.append(self.get_f())
        r.append(self.get_l())
        r.append(self.get_p())
        r.append(self.get_c())
        
        return r
    
    def get_o(self):
        r = '' 
        r = r + self.isisRecord.build_tag('706', 'o')
        return r
    def get_h(self):
        r = '' 
        r = r + self.isisRecord.build_tag('706', 'h')
        return r
    def get_f(self):
        r = ''
        return r
    def get_l(self):
        r = ''
        return r
    def get_p(self):
        r = ''
        return r
    def get_c(self):
        r = ''
        return r
        