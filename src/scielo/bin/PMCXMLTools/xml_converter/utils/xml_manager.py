import xml.etree.ElementTree as etree
import os

class XMLManager:

    root = {}
    debug = True

    def __init__(self, xml_filename, table_ent, report, debug_report):
        self.root = None
        self.debug_report = debug_report
        self.report = report
        self.invalid = []
        self.table_ent = table_ent
        r = self.load(xml_filename)

        if not r:
            if self.insert_isolat2_decl(xml_filename):
                r = self.load(xml_filename)

        self.error_message = ''


    def load(self, xml_filename):
        r = False
        if os.path.exists(xml_filename):
            self.ns = ''
            try:
                self.root = etree.parse(xml_filename).getroot()
                if '{' in self.root.tag:
                    self.ns = self.root.tag[0:self.root.tag.find('}')+1]
                else:
                    self.ns = ''
                r = True
            except:
                self.report.write('Unable to load ' + xml_filename, True, True)
                
        else:
            self.report.write('Missing XML file:' + xml_filename, True, True)
        return r

    def insert_isolat2_decl(self, xml_filename):
        f = open(xml_filename, 'r')
        c = f.read()
        f.close()

        f = open(xml_filename, 'w')

        ent_decl = '<!ENTITY % ISOLat2' + '\n'
        ent_decl += ' SYSTEM "http://www.xml.com/iso/isolat2-xml.entities" >' + '\n'
        ent_decl += '%ISOLat2;' + '\n'

        f.write(c.replace('<article', ent_decl + '<article'))
        f.close()



    def fix(self, xml_filename):
        error = [] 
    
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        c = self.table_ent.replace_to_numeric_entities(original)

        test = c.split('&')
        test = test[1:]


        if os.path.exists('invalid_chars.txt'):
            f = open('invalid_chars.txt', 'r')
            lines = f.readlines()
            for l in lines:
                e = l.split('|')
                
                self.invalid.append(e[2])
            f.close()

        f = open('invalid_chars.txt', 'a+')
        for item in test:
            if item[0:1] != '#':
                ent = '&' + item[0:item.find(';')+1]
                if not ent in self.invalid:
                    self.invalid.append(ent)
                    f.write('||'+ ent + '|\n')
                if not ent in error:
                    error.append(ent)
        f.close()
        fixed = (original != c and len(error)==0)
        if fixed:
            f = open(xml_filename, 'w')
            f.write(c)
            f.close()
        else:
            self.report.write( 'Invalid entities:' + ' '.join(error), True, True)
        return fixed


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
            	    self.debug_report.write('Invalid xpath: ' + p)
            else:
                p = '.'
                r.append(n)
            n_str = ''
            if len(n)>0:
                n_str = etree.tostring(n)
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
                self.debug_report.write('Empty element')
                self.debug_report.write('node', False, False, False, node)
                self.debug_report.write('n', False, False, False, n)
                self.debug_report.write('r', False, False, False, r)        
        return s
    
    def return_xml(self, node):
        r = '' 
        
        if node != None:
            r = etree.tostring(node)
             
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
            
        return attr  
 
    
   
