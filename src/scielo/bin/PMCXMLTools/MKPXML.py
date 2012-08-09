from myXML import MyXML

import sys

#import chardet

class MKPXML:
    
    
    def __init__(self, xml_filename, debug=0):

        
        self.xml = MyXML(xml_filename, debug)
        self.xml_filename = xml_filename
        self.debug = debug
    
    def return_filename(self):
        nodes = self.xml.get_nodes()
        
        folders = self.xml_filename[0:self.xml_filename.find('/pmc/')]
        folders = folders[0:folders.rfind('/')]
        
        
        acron = folders[folders.rfind('/')+1:]
        
        

        order = '00' + nodes[0].attrib['order']
        order = order[-3:]
        
        fpage = '000' + nodes[0].attrib['fpage']
        fpage = fpage[-4:]
        if fpage == '0000':
            page_or_order ='e' + order
        else:
            page_or_order = fpage
        
        #print page_or_order
        
        issueno = '0' + nodes[0].attrib['issueno']
        issueno = issueno[-2:]

        
        #print page_or_order
        
        return nodes[0].attrib['issn'] + '-' + acron + '-' + nodes[0].attrib['volid']+ '-' + issueno + '-' +  page_or_order
    
    def return_images(self, tags='figgrp | tabwrap | equation'):
        a = []
        
        names = tags.split(' | ')
        print('return_images ')
        print(names)
        for tag in names:
            #print tag
            self.xml.debug = 3
            nodes = self.xml.get_nodes(tag)
            print(nodes)
            for node in nodes:
                print(node)
                
                attr_filename = ''
                type = node.attrib['id']
                print('type=' + type)
                if type[0:1] == 'e':
                    type = 'e' + type
                else:
                    type = 'g' + type
                
                #print type
                
                try:
                    attr_filename = node.attrib['filename']
                except:
                    graphic_nodes = self.xml.get_nodes('graphic', node)
                    print(graphic_nodes)
                    
                    for gnode in graphic_nodes:
                        print(gnode.attrib)
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
       
   
        