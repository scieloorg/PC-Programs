import xml.etree.ElementTree as etree
import os, shutil

import xml_utils as xml_utils


class XMLTree:

    root = {}
    debug = True

    def __init__(self, table_ent):
        self.root = None
        self.invalid = []
        self.table_ent = table_ent
        self.error_message = ''

        try:
            self.parser = etree.XMLParser(recover=True, remove_blank_text=True, resolve_entities=False) #recovers from bad characters.
        except:
            self.parser = None

    def _load(self, xml_filename, show_message=False):
        self.ns = ''
        self.report.write('_load ' + xml_filename)
        self.root = xml_utils.load_xml(xml_filename)

        return (self.root is not None)

    def load(self, xml_filename, report):
        self.report = report

        r = False
        if os.path.exists(xml_filename):
            r = self._load(xml_filename)
            if not r:
                self.report.write('Unable to load XML', True, True)
        else:
            self.report.write('Missing XML file:' + xml_filename, True, True)
        return r

    def find_entities(self, xml_filename):
        self.report.write('named2char:' + xml_filename)
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        original = original.replace('&#', '#NUMBERENT#')
        original = original.replace('&', '-BREAK-&')
        return list(set([e[0:e.find(';')+1] for e in original.split('-BREAK-') if e.startswith('&')]))
        
    def named2char(self, xml_filename, new_xml_filename):
        self.report.write('named2char:' + xml_filename)
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        
        self.report.write('named2char:' + new_xml_filename)
        f = open(new_xml_filename, 'w')
        f.write(self.table_ent.name2char(original.replace('\ufeff','')))
        f.close()
        
    def number2char(self, xml_filename, new_xml_filename):
        self.report.write('number2char:' + xml_filename)
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        
        self.report.write('number2char:' + new_xml_filename)
        f = open(new_xml_filename, 'w')
        f.write(self.table_ent.number2char(original.replace('\ufeff','')))
        f.close()

    def named2number(self, xml_filename, new_xml_filename):
        self.report.write('named2number:' + xml_filename)
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()

        self.report.write('named2number:' + new_xml_filename)
        f = open(new_xml_filename, 'w')
        f.write(self.table_ent.name2number(original.replace('\ufeff', '')))
        f.close()

    def return_nodes(self, xpath='', current_node=None):
        r = []
        n = current_node
        if n is None:
            n = self.root.find('.')

        if n is not None:
            if xpath != '':
                p = self.ns + xpath
                try:
                    r = n.findall(p)
                except:
                    self.report.write('Invalid xpath: ' + p, False, True, True)
            else:
                p = '.'
                r.append(n)
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
        return s
    
    def return_xml(self, node):
        r = '' 
        
        if node != None:
            r = etree.tostring(node)
            
             
        return r
    
    
    def pretty(self, r):
        try:
            import xml.dom.minidom

            xml = xml.dom.minidom.parseString(r) # or xml.dom.minidom.parseString(xml_string)
            r = xml.toprettyxml()
            if '?>' in r:
                r = r[r.find('?>')+2:]
            r = r.replace('\n', '').replace('\r', '')
        except:
            pass
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
