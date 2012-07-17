import xml.etree.ElementTree as etree


class XMLManager:

    root = {}
    debug = True

    def __init__(self, xml_filename, report):
        self.report = report
        self.ns = ''
        try:
            self.root = etree.parse(xml_filename).getroot()
            
            
            
            self.report.debugging(self.root, 'XMLManager.init: root', 1)
            self.report.debugging(self.root.tag, 'XMLManager.init: root tag', 1)
            self.report.debugging(self.root.attrib, 'XMLManager.init: root attributes', 1)
            
            if '{' in self.root.tag:
                self.ns = self.root.tag[0:self.root.tag.find('}')+1]
            else:
                self.ns = ''
        except:
            self.report.log_error('Unable to load ' + xml_filename)

    
    
    def return_nodes(self, xpath = '', current_node = None):
        #'//{http://www.w3.org/2005/Atom}link'
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
            	    self.report.log_error('Invalid xpath: ' + p)
            else:
                p = '.'
                r.append(n)
                
            
        
            n_str = ''
            if len(n)>0:
                n_str = etree.tostring(n)
                
            
            self.report.debugging(n_str, 'XMLManager.return_nodes: xml of current node:', 2)
            self.report.debugging(p, 'XMLManager.return_nodes: xpath:', 1)
            self.report.debugging(r, 'XMLManager.return_nodes: resultado:', 1)
                
        return r
        
    def return_multi_values(self, result, start, level3_parameters_list, parent_node):
        # level3_parameters_list = lista de tupla ( parent_elem, elem, attr, default)
        self.report.log_event('begin_return_multi_values')
        self.report.display_data('level3_parameters_list', level3_parameters_list)
                
        level2_occs = []
        nodes = self.return_nodes('', parent_node)
        
        
        if start != '':
            nodes = self.return_nodes('.//'+start, parent_node)
            if len(nodes)>0:
                parent_node = nodes[0]
            else:
                parent_node = None
            
        parent_elem = level3_parameters_list[0][0]
        if parent_elem != '':
            nodes = self.return_nodes('.//' + parent_elem, parent_node)
        for node in nodes:
            saved_values = []
            saved_values = self._return_multi_values_for_group(saved_values, level3_parameters_list, node)
            for item in saved_values:
                level2_occs.append(item)
                 
        self.report.display_data('_return_multi_values return (level2 occs)', level2_occs)
        self.report.log_event('end_return_multi_values')
        return level2_occs
    
    def _return_multi_values_for_group(self, saved_values, level3_parameters_list, parent_node):
        
        
        self.report.log_event('begin_return_multi_values_for_group')
        self.report.display_data('node', parent_node)
        
        for level3_parameters_listitem in level3_parameters_list:
            ign, level3_label, elem, attr, default = level3_parameters_listitem
            
            self.report.display_data('node', parent_node)
            self.report.display_data('level3_parameters_list', level3_parameters_list)
            self.report.display_data('level3_parameters_listitem', level3_parameters_listitem)
            
            level3_occs = self._return_multi_values_for_level3(parent_node, elem, attr, default)
    
            if len(saved_values) >= len(level3_occs):
                saved_values = self._append1(saved_values, level3_occs, level3_label)
            else:
                saved_values = self._append2(saved_values, level3_occs, level3_label)
                
        self.report.log_event('end_return_multi_values_for_group')
        return saved_values
        
    def _return_multi_values_for_level3(self, parent_node, elem, attr, default):
        self.report.log_event('begin _return_multi_values_for_level3')
        self.report.display_data('begin _return_multi_values_for_level3: partent_node', parent_node)
        self.report.display_data('begin _return_multi_values_for_level3: elem', elem)
        self.report.display_data('begin _return_multi_values_for_level3: attr', attr)
        
        level3_occs = []
        if default != '':
            self.report.display_data('_return_multi_values_for_level3: default value used: ', default )
            level3_occs.append(default)
        else: 
            if elem != '': 
                self.report.display_data('_return_multi_values_for_level3: elem: ', elem )
                nodes = self.return_nodes('.//' + elem, parent_node)
                
                self.report.display_data('_return_multi_values_for_level3: nodes ', nodes )
                for node in nodes:
                    self.report.display_data('_return_multi_values_for_level3: nodes ', nodes )
                    self.report.display_data('_return_multi_values_for_level3: node ', node )
                    r = self._return_multi_values_for_level3(node, '', attr, default)
                    self.report.display_data('_return_multi_values_for_level3: r[0] ', r[0] )
                    level3_occs.append(r[0])
                    self.report.display_data('_return_multi_values_for_level3: level3_occs ', level3_occs )
            else:
                if attr != '':
                    self.report.display_data('_return_multi_values_for_level3: attr ', attr )
                    value = self.return_node_attr_value(parent_node, attr)
                else:
                    self.report.display_data('_return_multi_values_for_level3: text ', parent_node )
                    value = self.return_content( parent_node)
                    
                    
                level3_occs.append(value)
                
        self.report.display_data('return of _return_multi_values_for_level3', level3_occs)
        
        self.report.log_event('end _return_multi_values_for_level3')
        return level3_occs
               
    
    
    def return_content(self, node):
        
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
                print(node)
                print(n)
                print(r)
        
        return s
    
    
    def _append1(self, list_of_dict, list, dict_key):
        
        self.report.log_event('begin_append1')
        self.report.display_data('list_of_dict:', list_of_dict)
        self.report.display_data('list:', list)
        

        for dict in list_of_dict:
            # occ tem level3_parameters_list
            self.report.display_data('dict', dict)
            self.report.display_data('list', list)
            for list_item in list:
                self.report.display_data('list_item in list:', list_item)
                dict[dict_key] = list_item
                
        self.report.display_data('end_append1 return ', list_of_dict)
        self.report.log_event('end_append1')
        return list_of_dict     

    def _append2(self, list_of_dict, list, dict_key):
        
        self.report.log_event('begin_append2')
        
            
        self.report.display_data('list_of_dict:', list_of_dict)
        self.report.display_data('list:', list)
        
        for list_item in list:
            self.report.display_data('listitem', list_item)
            dict = {}
            dict[dict_key] = list_item
            list_of_dict.append(dict)
            
                    
        self.report.display_data('retorno', list_of_dict)
        self.report.log_event('end_append2')
        return list_of_dict     
        
    
    
    def return_node_attr_value(self, node, attr_name):
        self.report.debugging(node, 'XMLManager.return_node_attr_value: node', 1)
        self.report.debugging(attr_name, 'XMLManager.return_node_attr_value: attr_name', 1)
        attr = '' 
        if len(node)>0:
            if len(node.attrib)>0:
                if ':' in attr_name:
                    aname = attr_name[attr_name.find(':')+1:]
                    for k,a in node.attrib.items():
                        if aname == k[k.find('}')+1:]:
                            attr = a 
                            self.report.debugging(k, 'XMLManager.return_node_attr_value: attr', 1)
                else:
                    attr_name = attr_name[1:]
                    try:
                        attr = node.attrib[attr_name]
                    except:
                        self.report.debugging(node.attrib, 'XMLManager.return_node_attr_value: node.attrib', 1)
                
            else:
                self.report.debugging(node.attrib, 'XMLManager.return_node_attr_value: node.attrib', 1)
        else:
            self.report.debugging(node, 'XMLManager.return_node_attr_value: node', 1)
        
        return attr  
 
    
   
