from xml_manager import XMLManager
from xml2json_table import XML2JSONTable
import json

class XML2JSONConverter:

    def __init__(self, xml2json_table_filename, report, debug = False):
        self.conversion_table = XML2JSONTable(xml2json_table_filename, report)
        self.report = report
        self.debug = debug
    
    def convert(self, xml_filename):
        self.xml_manager = XMLManager(xml_filename, self.report)
        converted = {}
        converted['doc'] = self.__convert__(self.conversion_table.start, None)
        self.report.display_data('converted', a)  
        return converted 

    def pretty(self, json_data):
        return json.dumps(json_data, sort_keys=True, indent=4)
        
    def pretty_print(self, json_data):
        print(self.pretty(json_data))
        
    def __convert__(self, table_node, xml_parent_node):
        sep = ''
        s = ''
        a = []
        if self.debug:
            self.report.display_data('__convert__ ', table_node.xpath)
        xpath = table_node.xpath
        
        if table_node.xpath == '.' or  table_node.xpath[0:1] == '@':
            xpath = ''
        else:
            if not '[@' in xpath and '@' in xpath:
                xpath = './/' + table_node.xpath[0:table_node.xpath.find('@')]
                table_node.xpath = xpath[xpath.find('@'):]
            else:
                xpath = './/' + table_node.xpath
        xml_nodes = self.xml_manager.return_nodes(xpath, xml_parent_node)
                
        if len(table_node.children) == 0:
            r = self.return_values(table_node, xml_nodes)
            if len(r) == 1:
                a = r[0]
            else:
                a = r
        else:
            r = []
            for xml_node in xml_nodes:
                d = {}
                for child in table_node.children:
                    v = self.__convert__(child, xml_node)
                    if len(v)>0:
                        if child.to == '':
                            d['_'] = v
                        else:
                            d[child.to] = v
                r.append(d)        
            if len(r) == 1:
               a = r[0]
            else:
               a = r
        if self.debug:
            self.report.display_data('result', a)  
        return a
    
    
    def return_values(self, table_node, xml_nodes):
        a = []
        for xml_node in xml_nodes:
            if table_node.default != '':
                v = table_node.default
            else:
                if table_node.xpath[0:1] == '@':
                    
                    v = self.xml_manager.return_node_attr_value(xml_node, table_node.xpath[1:])
                else:
                    v = self.xml_manager.return_node_value(xml_node)
                
            a.append(self._convert_value_(v))
        return a
         
    def _convert_value_(self, value):
        enc = 'utf-8'
        if value != '':
            try:
                value = value.encode(enc)
            except:
                
                v = ''
                for c in value:
                    try:
                        v += c.encode(enc)
                    except:
                        v += '&#' + str(hex(ord(c))) + ';' 
                value = v
            
        return value
 
        