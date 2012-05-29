from myXML import MyXML

#from title_item import TitleItem
#from title_id import TitleId
#from author import Author
#from TitleAndItems import TitleAndItems
#import chardet

class PMCXML:
    
    
    def __init__(self, xml_filename, debug=0):
        self.xml = MyXML(xml_filename, debug)
        self.debug = debug
    
    def return_lang(self):
        node = self.xml.get_nodes()
        return node[0].attrib['{http://www.w3.org/XML/1998/namespace}lang']
        
    def return_authors(self):
        a = []
        nodes = self.xml.get_nodes('article-meta//contrib')
        for node in nodes:
            a.append({'surname': self.xml.get_text('surname', node), 'fname': self.xml.get_text('given-names', node), })
        return a
