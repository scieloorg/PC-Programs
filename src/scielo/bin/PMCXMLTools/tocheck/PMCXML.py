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
        journal = Journal()
        
        journal.set_title(self.xml.get_value('journal-title'))
        
        journal.set_title(self.xml.get_value('journal-id' , None, 'journal-id-type', 'nlm-ta'), 'medline')
        journal.set_title(self.xml.get_value('abbrev-journal-title'), 'iso')
        journal.set_title(self.xml.get_value('abbrev-journal-title'), 'abbrev')
        #journal.set_parallel_titles(self.xml.get_value('abbrev-journal-title'))
        journal.set_issn(self.xml.get_value('issn'))
        
        journal.set_publisher(self.xml.get_value('publisher-name', 'journal-meta'))
        
    	
        return journal

    def return_issue(self):
        issue = JournalIssue()
        
        vol = self.xml.get_value('volume', 'article-meta')
        num = self.xml.get_value('issue', 'article-meta')
        
        issue.set_volume(vol)
        issue.set_number(num)
        
        suppl = self.xml.get_value('suppl', 'article-meta')
        if suppl!='':
            if num!='':
                issue.set_number_suppl(suppl)
            else:
                issue.set_volume_suppl(suppl)
        pid = self.xml.get_value('article-id', 'article-meta', 'pub-id-type', 'publisher-id' ) 
        
        
        issue.set_year_order(pid[10:14] + str(int(pid[14:18])))
        
        
        
        return issue
        
        
    	
        