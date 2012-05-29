from myXML import MyXML

import sys

#import chardet

class MKPXML:
    
    
    def __init__(self, xml_filename, debug=0):
        self.xml = MyXML(xml_filename, debug)
        self.debug = debug
    
    def return_filename(self):
        nodes = self.xml.get_nodes()
        acron = self.xml.get_text('journal-acron')[0]
        
        #print acron
        
        order = nodes[0].attrib['order']
        
        #print acron
        
        fpage = nodes[0].attrib['fpage']
        if fpage == '0':
            page_or_order ='e' + order
        else:
            page_or_order = fpage
        
        #print page_or_order
        
        return nodes[0].attrib['issn'] + '-' + acron + '-' + nodes[0].attrib['volid']+ '-' + nodes[0].attrib['issueno'] + '-' +  page_or_order
        
    def return_images(self, tags='figgrp | tabwrap | equation'):
        a = []
        
        names = tags.split(' | ')
        for tag in names:
            #print tag
            
            nodes = self.xml.get_nodes(tag)
            for node in nodes:
                #print node
                
                attr_filename = ''
                type = node.attrib['id']
                if type[0:1] == 'e':
                    type = 'e' + type
                else:
                    type = 'g' + type
                
                #print type
                
                try:
                    attr_filename = node.attrib['filename']
                except:
                    graphic_nodes = self.xml.get_nodes('graphic', node)
                    for gnode in graphic_nodes:
                        try:
                            attr_filename = gnode.attrib['href']
                        except:
                            attr_filename = ''
                        if attr_filename == '':
                            attr_filename = gnode.attrib['{http://www.w3.org/XML/1998/namespace}href']
                if attr_filename!='':
                    a.append( (attr_filename , type) )
        return a

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1]=='test':
            xml = MKPXML('samples/02-05.sgm.xml')
            print xml.return_filename()
            print xml.return_images()
       
   
        