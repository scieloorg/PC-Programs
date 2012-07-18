from xml_manager import XMLManager
from xml2json_table import XML2JSONTable
import json

class XML2JSONConverter:

    def __init__(self, xml2json_table_filename, report):
        self.conversion_table = XML2JSONTable(xml2json_table_filename, report)
        self.report = report
    
    def convert(self, xml_filename):
        self.xml_manager = XMLManager(xml_filename, self.report)
        converted = self.__convert__(self.conversion_table.start, None)
        return converted  
         
    def pretty_print(self, json_data):
        j = json.dumps(json_data, sort_keys=True, indent=4)
        print(j)
        
    def __convert__(self, table_node, xml_parent_node):
        sep = ''
        s = ''
        a = []
        print('') 
        print('__convert__ ' + table_node.xpath)
        print('xml_parent_node: ')
        print(xml_parent_node)
        
        xpath = table_node.xpath
        
        if xpath == '.':
            xml_nodes = self.xml_manager.return_nodes('', xml_parent_node)
        else:
            if xpath[0:1] == '@':
                xml_nodes = self.xml_manager.return_nodes('', xml_parent_node)
            else:
                if not '[@' in xpath and '@' in xpath:
                    xml_nodes = self.xml_manager.return_nodes('.//' + xpath[0:xpath.find('@')], xml_parent_node)
                    table_node.xpath = xpath[xpath.find('@'):]
                    print(table_node.xpath)
                else:
                    xml_nodes = self.xml_manager.return_nodes('.//' + xpath, xml_parent_node)
                
        print('xml_nodes')    
        print(xml_nodes)
        if len(table_node.children) == 0:
            print(xpath + ' has no children')
            a = self.return_values(table_node, xml_nodes)
            s = self.format_json(table_node.to, a)
        else:
            for xml_node in xml_nodes:
                r = ''
                for child in table_node.children:
                    print('child')
                    print(xpath + '/' + child.xpath)
                    print(xml_node)
                    v = self.__convert__(child, xml_node)
                    if len(v) > 0:
                        r += ',' + v 
                    
                if len(r) > 0:
                    r = r[1:]
                if ':' in r:
                    r = '{' + r + '}'
                a.append(r)        
            s = self.format_json(table_node.to, a)
        print('result:' + s)  
        return s
    
    def format_json(self, key, list_of_values):
        s = ''
        if len(list_of_values) == 1:
            s = list_of_values[0]
        else:
            for item in list_of_values:
                s += ',' + item 
                
            if len(s) > 0:
                s = s[1:]
            if len(list_of_values) > 1:    
                s = '[' + s  + ']' 
                
        if len(s) > 0:
            if not s[0:1] in "{['":
                s = "'" + s + "'"
            if key != '' :
                s = "'" + key + "':" + s 
        return s
        
    
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
        if value != '':
            try:
                value = value.encode('iso-8859-1')
            except:
                
                v = ''
                for c in value:
                    try:
                        v += c.encode('iso-8859-1')
                    except:
                        v += '&#' + str(hex(ord(c))) + ';' 
                value = v
            
        return value
 
        