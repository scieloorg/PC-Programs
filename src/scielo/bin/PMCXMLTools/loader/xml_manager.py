import xml.etree.ElementTree as etree


class XMLManager:

    root = {}

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
        
    def return_multi_values(self, result, group, xpath, subf_xpaths, parent_node):
        
        values = []
        s = {} 
        
        nodes = self.return_nodes(xpath, parent_node)
        for node in nodes:
            occ = {}
            for subf, subf_xpath in subf_xpaths.items():
                elem, attr, default = subf_xpath
                if default != '':
                    value = default
                    occ[subf] = value
                else: 
                    if elem != '': 
                        s[subf] = ('', attr, '')
                        occ[subf] = self.return_multi_values(acum, group, './/' + elem, s, node)
                        if len(values) != len(occ[subf]):
                            values = self._fix_(values, occ, subf)
                    else:
                        if attr != '':
                            value = self.return_node_attr_value(node, attr)
                        else:
                            value = node.text
                        occ[subf] = value
                
                        
                
            values.append(occ)
	    return values
        
    def _fix_(self, occs, new_values, subf_name):
        new_occs = []
        if len(occs) > len(new_values):
            new_occs = self._fix_occs_are_greater(occs, new_values, subf_name)
        else:
            new_occs = self._fix_new_values_are_greater(occs, new_values, subf_name)
         
        return new_occs
        
    def _fix_new_values_are_greater(self, occs, new_values, subf_name):
        new_occs = []
        for value in new_values:
            new_occ = {}
            for occ in occs:
            
                new_occ[subf_name] = value
                for occ_k, occ_i in occ.items():
                    new_occ[occ_k] = occ_i
                new_occs.append(new_occ)
        return new_occs
        
    def _fix_occs_are_greater(self, occs, new_values, subf_name):
        r = []
        new_occs = []
        
        for occ in occs:
            for value in new_values:
                occ[subf_name] = value
            new_occs.append(occ)
        return new_occs    
        
    
    def old_return_multi_values(self, xpath, subf_xpaths, parent_node):
        
        values = []
        nodes = self.return_nodes(xpath, parent_node)
        for node in nodes:
            occ = {}
            for subf, subf_xpath in subf_xpaths.items():
                elem, attr, default = subf_xpath
                if default != '':
                    value = default
                else: 
                    if elem != '': 
                        elem_node = self.return_nodes('.//' + elem, node)
                        if len(elem_node)>0:
                            value = elem_node[0].text
                        else:
                            value = '' 
                    if attr != '':
                        if elem != '' and  len(elem_node)>0:
                            value = self.return_node_attr_value(elem_node, attr)
                        else:
                            value = self.return_node_attr_value(node, attr)
                    if attr == '' and elem == '':
                        value = node.text
                    
                occ[subf] = value
            values.append(occ)
	        
        return values
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