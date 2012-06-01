import xml.etree.ElementTree as etree


class XMLManager:

    root = {}

    def __init__(self, xml_filename, debug=0):
        self.root = etree.parse(xml_filename).getroot()
        self.debug = debug
        if debug > 0:
            print('root')
            print(self.root)
            print('root tag')
            print(self.root.tag)
            print('root attributes')
            print(self.root.attrib)
            
        if '{' in self.root.tag:
            self.ns = self.root.tag[0:self.root.tag.find('}')+1]
        else:
            self.ns = ''
        

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
            	    print('Invalid xpath: ' + "\n    " + p)
            else:
                p = '.'
                r.append(n)
                
            if self.debug > 0:
                print('---- DEBUG get_nodes')
                if self.debug == 2:
                    print('xml of current node:')
                    print(etree.tostring(n))
                print('xpath:' + p)
                print('resultado:')
                print(r)
                
                print('---- FIM DEBUG get_nodes')
        return r
        
    def return_multi_values(self, xpath, subf_xpaths, parent_node):
        
        values = []
        nodes = self.return_nodes(xpath, parent_node)
        for node in nodes:
            occ = {}
            for subf, subf_xpath in subf_xpaths.items():
                elem, attr, default = subf_xpath
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
                    if default !=  '' :
                        value = default
                    else:
                        value = node.text
                    
                occ[subf] = value
            values.append(occ)
	        
        return values
    
    def return_node_attr_value(self, node, attr_name):
        attr = '' 
        if ':' in attr_name:
            aname = attr_name[attr_name.find(':')+1:]
            for k,a in node.attrib.items():
                if aname == k[k.find('}')+1:]:
                    attr = a 
                    if self.debug >0:
                        print(k)
        else:
            try:
                attr = node.attrib[attr_name]
            except:
                if self.debug >0:
                    print(node.attrib)
                
        
        return attr  
   
#filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/0004-282X-anp-69-859.xml'
filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml.local.xml'
x = XMLManager(filename)
#print(x.return_nodes('.//xref[@rid="r07"]'))
#print(x.return_nodes())
#print(x.return_nodes('.//article-meta//volume[../issue]'))