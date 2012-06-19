import xml.etree.ElementTree as etree


class XMLManager:

    root = {}
    debug = True

    def __init__(self, xml_filename, report):
        try:
            self.root = etree.parse(xml_filename).getroot()
            
            
            self.report = report
            self.report.debugging(self.root, 'XMLManager.init: root')
            self.report.debugging(self.root.tag, 'XMLManager.init: root tag')
            self.report.debugging(self.root.attrib, 'XMLManager.init: root attributes')
            
            if '{' in self.root.tag:
                self.ns = self.root.tag[0:self.root.tag.find('}')+1]
            else:
                self.ns = ''
        except:
            self.report.register('Unable to load ' + xml_filename, '')

    
    
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
            	    self.report.register(p, 'Invalid xpath:')
            else:
                p = '.'
                r.append(n)
            self.report.debugging(etree.tostring(n), 'XMLManager.return_nodes: xml of current node:', 2)
            self.report.debugging(p, 'XMLManager.return_nodes: xpath:')
            self.report.debugging(r, 'XMLManager.return_nodes: resultado:')
                
        return r
        
    def return_multi_values(self, result, start, subfs, parent_node):
        # subfs = lista de tupla ( parent_elem, elem, attr, default)
        self.report.display_data('begin_return_multi_values', '')
        self.report.display_data('subfs:', subfs)
                
        tag_occs = []
        nodes = [None]
        
        if start != '':
            nodes = self.return_nodes('.//'+start, parent_node)
            parent_node = nodes[0]
            
        parent_elem = subfs[0][0]
        if parent_elem != '':
            nodes = self.return_nodes('.//' + parent_elem, parent_node)
        for node in nodes:
            saved_values = []
            saved_values = self._return_multi_values_for_group(saved_values, subfs, node)
            for item in saved_values:
                tag_occs.append(item)
                 
        self.report.display_data('retorno', tag_occs)
        self.report.display_data('end_return_multi_values','')
        return tag_occs
    
    def _return_multi_values_for_group(self, saved_values, subfs, parent_node):
        
        
        self.report.display_data('_return_multi_values_for_group:', '')
        self.report.display_data('node:', parent_node)
        
        for subf_xpath in subfs:
            ign, subf_name, elem, attr, default = subf_xpath
            self.report.display_data('subf_name:', subf_name)
            self.report.display_data('subf_xpath:', subf_xpath)
            subf_occs = self._return_multi_values_for_subf(parent_node, elem, attr, default)
    
            if len(saved_values) >= len(subf_occs):
                saved_values = self._append1(saved_values, subf_occs, subf_name)
            else:
                saved_values = self._append2(saved_values, subf_occs, subf_name)
                
        return saved_values
        
    def _return_multi_values_for_subf(self, parent_node, elem, attr, default):
        
        subf_occs = []
        if default != '':
            subf_occs.append(default)
        else: 
            if elem != '': 
                nodes = self.return_nodes('.//' + elem, parent_node)
                
                for node in nodes:
                    r = self._return_multi_values_for_subf(node, '', attr, default)
                    subf_occs.append(r[0])
            else:
                if attr != '':
                    value = self.return_node_attr_value(parent_node, attr)
                else:
                    value = parent_node.text
                subf_occs.append(value)
        return subf_occs
               
   
    def _append1(self, list_of_dict, list, dict_key):
        
        print('begin_append1', '')
        
        self.report.display_data('list_of_dict:', list_of_dict)
        self.report.display_data('list:', list)
        

        for dict in list_of_dict:
            # occ tem subfs
            self.report.display_data('dict', dict)
            self.report.display_data('list', list)
            for list_item in list:
                self.report.display_data('list_item in list:', list_item)
                dict[dict_key] = list_item
                
        self.report.display_data('retorno', list_of_dict)
        self.report.display_data('end_append1', '')
        return list_of_dict     

    def _append2(self, list_of_dict, list, dict_key):
        
        print('begin_append2', '')
        
            
        self.report.display_data('list_of_dict:', list_of_dict)
        self.report.display_data('list:', list)
        
        for list_item in list:
            self.report.display_data('listitem', list_item)
            dict = {}
            dict[dict_key] = list_item
            list_of_dict.append(dict)
            self.report.display_data('retorno', list_of_dict)
                    
        self.report.display_data('retorno', list_of_dict)
        self.report.display_data('end_append2', '')
        return list_of_dict     
        
    
    
    def return_node_attr_value(self, node, attr_name):
        self.report.debugging(node, 'XMLManager.return_node_attr_value: node')
        self.report.debugging(attr_name, 'XMLManager.return_node_attr_value: attr_name')
        
        attr = '' 
        if ':' in attr_name:
            aname = attr_name[attr_name.find(':')+1:]
            for k,a in node.attrib.items():
                if aname == k[k.find('}')+1:]:
                    attr = a 
                    self.report.debugging(k, 'XMLManager.return_node_attr_value: attr')
        else:
            attr_name = attr_name[1:]
            try:
                attr = node.attrib[attr_name]
            except:
                self.report.debugging(node.attrib, 'XMLManager.return_node_attr_value: node.attrib')
                
        
        return attr  
   
#filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/0004-282X-anp-69-859.xml'
#filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml.local.xml'
#x = XMLManager(filename)
#self.report.register(x.return_nodes('.//xref[@rid="r07"]'))
#self.report.register(x.return_nodes())
#self.report.register(x.return_nodes('.//article-meta//volume[../issue]'))