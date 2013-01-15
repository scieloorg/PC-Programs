
import json

class XML2JSON:

    def __init__(self, xml2json_table, xml_tree, debug = False):
        #self.xml2json_table = XML2JSONTable(xml2json_table_filename)
        #self.debug = debug
        #self.xml_tree = XMLManager(TableEntAndChar())
        self.xml2json_table = xml2json_table
        
        self.debug = debug
        
        self.xml_tree = xml_tree
        

    def convert(self, xml_filename, report):
        self.dict = {}
        self.report = report 

        self.xml_tree.load(xml_filename, report)
        #if self.xml_filename.error_message

        converted = self.__convert__(self.xml2json_table.start, None, None)

        report.write('converted', False, False, False, converted)  
        return converted 

    def pretty(self, json_data):
        return json.dumps(json_data, sort_keys=True, indent=4)
        
    def pretty_print(self, json_data):
        print(self.pretty(json_data))
        


    def __convert__(self, table_node, xml_parent_node, parent_xml_parent_node, num = 1):
        
        if self.debug:
            self.report.write('__convert__ ')
            self.report.write('table_node.xpath', False, False, False, table_node.xpath)
        
        xml_nodes = self.xml_tree.return_nodes(table_node.xpath, xml_parent_node)
        if self.debug: 
            self.report.write('xml_nodes', False, False, False, xml_nodes)
        
        if len(table_node.children) == 0:
            if self.debug: 
                self.report.write('leaf',False, False, False, xml_nodes)  
            result = self.return_leaf_content(table_node, xml_nodes)            
        else:
            if self.debug: 
                self.report.write('branch', False, False, False, xml_nodes) 
            result = self.return_branch_content(table_node, xml_nodes, xml_parent_node, num)
        
        if self.debug: 
            self.report.write('result before __format__', False, False, False, result)  
        
        result = self.__format__(table_node, result, num)
        
        if self.debug: 
            self.report.write('result', False, False, False, result)  
        return result

    def return_leaf_content(self, table_node, xml_nodes, debug = False):
        a = []
        for xml_node in xml_nodes:
            
            if table_node.attr != '':
                v = self.xml_tree.return_node_attr_value(xml_node, table_node.attr[1:])
            elif table_node.xml:
                v = self.xml_tree.return_xml(xml_node)
            else:
                v = self.xml_tree.return_node_value(xml_node)
            if self.debug: 
                self.report.write('v', False, False, False, v)  
            if v == '' or v == None:
                v = table_node.default
                
            if v != '':
                a.append(self._convert_value_(v))
            
        a = self.__format__(table_node, a)
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
                    self.report.write(table_node.xpath + '=>' + child.xpath)
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
     
    