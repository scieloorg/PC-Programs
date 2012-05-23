
from isis_record_article import Article_ISISRecord

class Articles_ISISDB:

    
    def __init__(self, param_title, param_issue, param_articles):
        self.title = param_title
        self.issue = param_issue
        self.articles = param_articles
        
    def generate_i_record(self):
    	return '!ID 000001' + "\n" 
    	
    def generate_article_records(self):
        r = self.generate_i_record()
        id = 2
        for a in self.articles:
            record_a = Article_ISISRecord(self.title, self.issue, a)
            records = record_a.generate_records()
            for rec in records:
    		    n = '000000' + str(id) 
    		    r = r + '!ID ' + n[-6:] + "\n"
    		    r = r + rec
    		    id += 1
        return r
        