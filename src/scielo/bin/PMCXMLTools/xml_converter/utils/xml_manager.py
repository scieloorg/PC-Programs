import xml.etree.ElementTree as etree
from xml.etree.ElementTree import XMLTreeBuilder
import os
import shutil

class XMLManager:

    root = {}
    debug = True

    def __init__(self, table_ent):
        self.root = None
        self.REPLACE = '[NAME-ENT]&amp;[/NAME-ENT]'
        
        self.invalid = []
        self.table_ent = table_ent
        self.error_message = ''

        try:
            self.parser = etree.XMLParser(recover=True, remove_blank_text=True, resolve_entities=True) #recovers from bad characters.
        except:
            #self.parser = XMLTreeBuilder()
            #self.parser.doctype('article', '-//NLM//DTD Journal Publishing DTD v3.0 200800202//EN', 'http://dtd.nlm.nih.gov/publishing/3.0/journalpublishing.dtd')
            self.parser = None
        

    def __load__(self, xml_filename):
        self.ns = ''
        self.root = None
        self.report.write('__load__ ' + xml_filename)
        try:
            if self.parser != None:
                self.report.write('__load__ self.parser != None')
                self.root = etree.parse(xml_filename, self.parser).getroot()
            else:
                self.report.write('__load__ self.parser == None')
                self.root = etree.parse(xml_filename).getroot()
            
            if '{' in self.root.tag:
                self.ns = self.root.tag[0:self.root.tag.find('}')+1]
            else:
                self.ns = ''
            
            r = True
        except Exception as inst:
            self.report.write('Unable to load ' + xml_filename, True, True, False, inst)
            r = False
        return r

    def load(self, xml_filename, doctype, report):
        self.report = report

        r = False
        if os.path.exists(xml_filename):
            r = self.__load__(xml_filename)
            if not r:
                new_xml_filename = self.create_temp()
                shutil.copyfile(xml_filename, new_xml_filename)
                self.fix_doctype(new_xml_filename, doctype)
                r = self.__load__(new_xml_filename)
                if not r:
                    self.named2number(new_xml_filename)
                    r = self.__load__(new_xml_filename)
                    if not r:
                        self.ignore_named_entities(new_xml_filename)
                        r = self.__load__(new_xml_filename)
                if os.path.exists(new_xml_filename):                    
                    shutil.copyfile(new_xml_filename, xml_filename.replace('.xml', '.xml.fixed'))
                    self.report.write('Invalid XML file:' + xml_filename.replace('.xml', '.xml.fixed'), True, True)
                    os.unlink(new_xml_filename)
        else:
            self.report.write('Missing XML file:' + xml_filename, True, True)
        return r

    def create_temp(self):
        from tempfile import mkstemp
        _, new_xml_filename = mkstemp()
        return new_xml_filename
    

    def ignore_named_entities(self, xml_filename):
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        
        original = original.replace('&', self.REPLACE)
        original = original.replace(self.REPLACE + '#', '&#')

        f = open(xml_filename, 'w')
        f.write(original)
        f.close()


    def fix_doctype(self, xml_filename, new_doctype):
        
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        
        f = open(xml_filename, 'w')
        #<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "journalpublishing3.dtd">
        if '<!DOCTYPE' in original:
            p = original.find('<!DOCTYPE')
            doctype = original[p:]
            p = doctype.find('>')
            doctype = doctype[0:p+1]

            print(doctype)
            new_doctype = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "' + new_doctype  +  '">'
            
            print(new_doctype)
            original = original.replace(doctype, new_doctype)
        print( '-')
        print(original[0:300])
        print('-')
        f.write(original)
        f.close()


    def named2number(self, xml_filename):
        
        self.report.write('named2number:' + xml_filename)
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        
        self.report.write('named2number:' + xml_filename)
        f = open(xml_filename, 'w')
        f.write(self.table_ent.replace_to_numeric_entities(original.replace('\ufeff','')))
        f.close()
    
    def return_nodes(self, xpath = '', current_node = None):
        r = []
        n = current_node
        if n == None:
            n = self.root

        if n != None:
            if xpath != '':
                p = self.ns + xpath
                try:
            	    r = n.findall(p)
            	except:
            	    self.report.write('Invalid xpath: ' + p)
            else:
                p = '.'
                r.append(n)
            #n_str = ''
            #if len(n)>0:
            #    n_str = etree.tostring(n)
        return r

    def return_node_value(self, node):
        r = '' 
        s = ''
        if node != None:
            n = 0
            children = node.iter()
            for child in children:
                n +=1
            if n == 1:
                r = node.text
            if n > 1:
                r = etree.tostring(node)
                
                r = r[r.find('>')+1:]
                r = r[0:r.rfind('</')]
            try:
                s = r.strip()
            except:
                s = ''
                self.report.write('Empty element')
                self.report.write('node', False, False, False, node)
                self.report.write('n', False, False, False, n)
                self.report.write('r', False, False, False, r)    
            s = s.replace(self.REPLACE, '&')     
        return s
    
    def return_xml(self, node):
        r = '' 
        
        if node != None:
            r = etree.tostring(node)
            r = r.replace(self.REPLACE, '&')
        return r
    
    
    
    def return_node_attr_value(self, node, attr_name):
        attr = '' 
        if node != None:
            if len(node.attrib)>0:
                if ':' in attr_name:
                    aname = attr_name[attr_name.find(':')+1:]
                    for k,a in node.attrib.items():
                        if aname == k[k.find('}')+1:]:
                            attr = a 
                else:
                    if attr_name[0:1] == '@':
                        attr_name = attr_name[1:]
                    try:
                        attr = node.attrib[attr_name]
                    except:
                        attr = ''
        attr = attr.replace(self.REPLACE, '&')
        return attr  
