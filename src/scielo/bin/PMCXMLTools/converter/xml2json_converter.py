from xml_manager import XMLManager
from xml2json_table import XML2JSONTable
import json

class XML2JSONConverter:

    def __init__(self, xml2json_table_filename, report, debug = False):
        self.conversion_table = XML2JSONTable(xml2json_table_filename, report)
        self.report = report
        self.debug = debug
        self.dict = {}

    def convert(self, xml_filename):
        self.xml_manager = XMLManager(xml_filename, self.report)
        converted = {}
        converted = self.__convert__(self.conversion_table.start, None, None)
        self.report.display_data('converted', converted)  
        return converted 

    def pretty(self, json_data):
        return json.dumps(json_data, sort_keys=True, indent=4)
        
    def pretty_print(self, json_data):
        print(self.pretty(json_data))
        
    def __convert__(self, table_node, xml_parent_node, parent_xml_parent_node, num = 1):
        sep = ''
        s = ''
        a = []

        test = False
        if self.debug:
            self.report.display_data('__convert__ ', table_node.xpath)
        xpath = table_node.xpath
        
        if table_node.xpath == '.' or  table_node.xpath[0:1] == '@':
            xpath = ''
        else:
            if not '[@' in xpath and '@' in xpath:
                if '../' in table_node.xpath:
                    xpath = ''
                    xml_parent_node = parent_xml_parent_node
                    table_node.xpath = table_node.xpath[table_node.xpath.find('../')+3:]
                    

                else:
                    xpath = './/' + table_node.xpath[0:table_node.xpath.find('@')]
                    test = True
                table_node.xpath = table_node.xpath[table_node.xpath.find('@'):]
                
            else:
                xpath = './/' + table_node.xpath
        if xpath != None:
            xml_nodes = self.xml_manager.return_nodes(xpath, xml_parent_node)

        if test:
            print(xpath)
            print(xml_nodes)
            print(table_node.xpath)
            test = False

        if len(table_node.children) == 0:
            content = self.return_content(table_node, xml_nodes)
            if len(content) == 1:
                result = content[0]
            else:
                result = content 
        else:
            occs = []
            number = 0
            for xml_node in xml_nodes:
                # FIXME pode haver mais de uma instancia d{12}
                occ = {}
                number += 1
                for child in table_node.children:
                    #print(table_node.xpath + '=>' + child.xpath)
                    v = self.__convert__(child, xml_node, xml_parent_node, number)
                    if len(v)>0:
                        if child.to == '':
                            occ['_'] = v
                        else:
                            occ[child.to] = v
                if occ != {}:
                    occs.append(occ)        

            if len(occs) == 0:
                result = ''
            else:
                if len(occs) == 1:
                    result = occs[0]
                else:
                    result = occs
                result = self.__control_occ__(table_node, num, result)
                
        if self.debug:
            self.report.display_data('result', result)  
        return result
    
    def __control_occ__(self, table_node, num, result):
        key = table_node.parent.to + '_' +  str(num) + '_' + table_node.to
        
        if key in self.dict.keys():
            if type(self.dict[key]) != type([]):
                s = self.dict[key]
                self.dict[key] = []
                self.dict[key].append(s)
                
            
            self.dict[key].append(result)
            result = self.dict[key]
            
        else:
            self.dict[key] = result
        return result

    def return_content(self, table_node, xml_nodes):
        a = []
        for xml_node in xml_nodes:
            
            if table_node.xpath[0:1] == '@':
                v = self.xml_manager.return_node_attr_value(xml_node, table_node.xpath[1:])
                
            else:
                v = self.xml_manager.return_node_value(xml_node)
            if v == '':
                v = table_node.default
                
            if v != '':
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
 
        