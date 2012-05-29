
from isis_record import ISISRecord

from journal import Journal
from journal_issue import JournalIssue
from journal_article import JournalArticle

isis_record = ISISRecord()

class Article_ISISRecord:

    
    def __init__(self, param_journal, param_issue, param_article, control_info):
        self.journal = param_journal
        self.issue = param_issue
        self.article = param_article
        self.control_info = control_info
        
    
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
        r += isis_record.build_tag('706', 'o')
        r += isis_record.build_tag('004', self.control_info.get_issue_folder_name())
        r += isis_record.build_tag('702', self.control_info.get_issue_folder_name())
        
        return r
    def get_h(self):
        r = '' 
        r = r + isis_record.build_tag('706', 'h')
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
        