from myXML import MyXML

from journal import Journal
from journal_issue import JournalIssue
from journal_article import JournalArticle

#import chardet

class PMCXML:
    
    
    def __init__(self, xml_filename, debug=0):
        self.xml = MyXML(xml_filename, debug)
        self.debug = debug
    
    def return_article(self):
        article = JournalArticle()
        return article
        
    def return_journal(self):
        title = Journal()
        return title

    def return_issue(self):
        issue = JournalIssue()
        return issue
        