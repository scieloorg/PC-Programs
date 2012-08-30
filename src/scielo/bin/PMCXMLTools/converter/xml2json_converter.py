from utils.xml_manager import XMLManager
from xml2json_table import XML2JSONTable
import json

class XML2JSONConverter:

    def __init__(self, xml2json_table_filename, debug_report, debug = False):
        self.conversion_table = XML2JSONTable(xml2json_table_filename)
        self.debug_report = debug_report
        self.debug = debug
        

    def convert(self, xml_filename):
        self.dict = {}
        self.xml_manager = XMLManager(xml_filename, self.debug_report)
        converted = self.__convert__(self.conversion_table.start, None, None)
        self.debug_report.display_data('converted', converted)  
        return converted 

    def pretty(self, json_data):
        return json.dumps(json_data, sort_keys=True, indent=4)
        
    def pretty_print(self, json_data):
        print(self.pretty(json_data))
        


    def __convert__(self, table_node, xml_parent_node, parent_xml_parent_node, num = 1):
        
        if self.debug:
            self.debug_report.log_event('__convert__ ')
            self.debug_report.display_data('table_node.xpath', table_node.xpath)
        
        xml_nodes = self.xml_manager.return_nodes(table_node.xpath, xml_parent_node)
        if self.debug: 
            self.debug_report.display_data('xml_nodes', xml_nodes)
        
        if len(table_node.children) == 0:
            if self.debug: 
                self.debug_report.display_data('leaf', xml_nodes)  
            result = self.return_leaf_content(table_node, xml_nodes)            
        else:
            if self.debug: 
                self.debug_report.display_data('branch', xml_nodes) 
            result = self.return_branch_content(table_node, xml_nodes, xml_parent_node, num)
        
        if self.debug: 
            self.debug_report.display_data('result before __format__', result)  
        
        result = self.__format__(table_node, result, num)
        
        if self.debug: 
            self.debug_report.display_data('result', result)  
        return result

    def return_leaf_content(self, table_node, xml_nodes, debug = False):
        a = []
        for xml_node in xml_nodes:
            
            if table_node.attr != '':
                v = self.xml_manager.return_node_attr_value(xml_node, table_node.attr[1:])
                
            else:
                v = self.xml_manager.return_node_value(xml_node)
            if self.debug: 
                self.debug_report.display_data('v', v)  
            if v == '' or v == None:
                v = table_node.default
                
            if v != '':
                a.append(self._convert_value_(v))
            
        #return self.__format__(table_node, a)
        return a

    def return_branch_content(self, table_node, xml_nodes, xml_parent_node, num, debug = False):
        occs = []
        number = 0
        for xml_node in xml_nodes:
            # FIXME pode haver mais de uma instancia d{12}
            occ = {}
            number += 1
            for child in table_node.children:
                if self.debug:
                    self.debug_report.log_event(table_node.xpath + '=>' + child.xpath)
                v = self.__convert__(child, xml_node, xml_parent_node, number)
                if len(v)>0:
                    if child.to == '' or child.to == '_':
                        occ['_'] = v
                    else:
                        occ[child.to] = v
            if occ != {}:
                occs.append(occ)        
        
        return occs  

    def __format__(self, table_node, result, num = None):
        r = result
        if type(result) == type([]):

            if len(result) == 1:
                r = result[0]
            elif len(result) == 0:
                r = ''
            
        #r = self.__control_occ__(table_node, num, r)
        return r

    
    def old__format__(self, table_node, result, num = None):
        if len(result) == 0:
            r = ''
        else:
            r = result
            if type(result) == type([]) and len(result) == 1:
                r = result[0]
            if num != None:
                r = self.__control_occ__(table_node, num, r)
        return r

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


    def x_convert_value_(self, value):
         return value
         
    def _convert_value_(self, value):
        enc = 'utf-8'
        if value != '':
            try:
                test = value.encode(enc)
            except:
                
                test = self.convert_chr(value)
            if type(test) == type(''):
                value = test
        return value

    def convert_chr(self, value):
        v = ''
        for c in value:
            try:
                v += c.encode('utf-8')
            except:
                try: 
                    n = ord(c)
                    
                except:

                    n = 256*ord(c[0]) + ord(c[1])
                    

                v += '&#' + str(hex(n)) + ';'
        return v
     
    def __old__convert__(self, table_node, xml_parent_node, parent_xml_parent_node, num = 1):
        sep = ''
        s = ''
        a = []

        test = False
        if self.debug:
            self.debug_report.display_data('__convert__ ', table_node.xpath)
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
                    ##xpath = './/' + table_node.xpath[0:table_node.xpath.find('@')]
                    xpath = table_node.xpath[0:table_node.xpath.find('@')]
                    if not './/' in xpath:
                        xpath = './' + xpath
                    #test = True
                table_node.xpath = table_node.xpath[table_node.xpath.find('@'):]
                
            else:
                ##xpath = './/' + table_node.xpath
                xpath = table_node.xpath
                if not './/' in xpath:
                    xpath = './' + xpath
        if xpath != None:
            xml_nodes = self.xml_manager.return_nodes(xpath, xml_parent_node)

        if test:
            print(xpath)
            print(xml_nodes)
            print(table_node.xpath)
            test = False

        if len(table_node.children) == 0:
            content = self.return_end_node_content(table_node, xml_nodes)
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
                        if child.to == '' or child.to == '_':
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
            self.debug_report.display_data('result', result)  
        return result   