import os

from PMCXML import PMCXML
from isis_db_articles import Articles_ISISDB
from isis_idfile import ISIS_IDFile

class PMCXML_loader:
   
    def __init__(self):
        pass
        
        
    def load_xml_files(self, path, id_filename):
        dir_list = os.listdir(path)
        articles = []
        for f in dir_list:
            if '.xml' in f:
                pmcxml = PMCXML(path + '/' + f)
                articles.append( pmcxml.return_article() )
        
        journal = pmcxml.return_journal()
        issue = pmcxml.return_issue()
        
        articles_db = Articles_ISISDB(journal, issue, articles)
        id_file = ISIS_IDFile(id_filename)
        
        id_file.save(articles_db.generate_article_records())
        id_file.close_files()