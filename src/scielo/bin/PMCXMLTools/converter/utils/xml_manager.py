import xml.etree.ElementTree as etree
import os

class XMLManager:

    root = {}
    debug = True

    def __init__(self, xml_filename, table_ent, debug_report):
        self.root = None
        self.debug_report = debug_report


        if os.path.exists(xml_filename):
            f = open(xml_filename, 'r')
            c = f.read()
            f.close()
            c = table_ent.replace_to_numeric_entities(c)
            f = open(xml_filename, 'w')
            f.write(c)
            f.close()
        if os.path.exists(xml_filename):
            
            self.ns = ''
            try:
                self.root = etree.parse(xml_filename).getroot()
                if '{' in self.root.tag:
                    self.ns = self.root.tag[0:self.root.tag.find('}')+1]
                else:
                    self.ns = ''
            except:

                self.debug_report.log_error('Unable to load ' + xml_filename)
                
        else:
            self.debug_report.log_error('Missing XML file:' + xml_filename)
            
    
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
            	    self.debug_report.log_error('Invalid xpath: ' + p)
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
                self.debug_report.log_event('Empty element')
                self.debug_report.display_data('node', node)
                self.debug_report.display_data('n', n)
                self.debug_report.display_data('r', r)        
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
 
    
   
