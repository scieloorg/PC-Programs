import xml.etree.ElementTree as etree


class MyXML:
    root = {}
    def __init__(self, xml_filename, debug=0):
        try:
            self.root = etree.parse(xml_filename).getroot()
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
            self.debug = debug
        except:
            print('XML IS NOT WELL-FORMED!!!')

    def _get_nodes_(self, xpath = '', current_node = None):
        #'//{http://www.w3.org/2005/Atom}link'
        r = []
        n = current_node
        if n == None:
            n = self.root

        if n != None:
            if xpath != '':
                p = './/' + self.ns + xpath
                print(p)
            	r = n.findall(p)
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
        
    
        
    
    
    def get_value(self, xpath = '', parent_element = None, attr_name = None, attr_value = None):
        parent_nodes = [None]
        if parent_element != None:
             parent_nodes = self._get_nodes_(parent_element)
        
        values = []  
        for current_node in parent_nodes:
            nodes = self.get_nodes(xpath, current_node, attr_name, attr_value)
            for node in nodes:
                if attr_name != None:
                    v = nodes[0].attrib[attr_name]
                    if attr_value != None:
                        if v == attr_value:
                            values.append(nodes[0].text)
                        else:
                            pass 
                    else:
                        values.append(v)
                else:
                    values.append(nodes[0].text)
        if len(values)==1:
            r = values[0]            
        else:
            if len(values)==0:
                r = ''
            else:
                r = values
        return r
    
    def get_nodes(self, xpath = '', current_node = None, attr_name = None, attr_value = None):
        nodes = self._get_nodes_(xpath, current_node)
        r = []
        
        if attr_value!= None:
            if attr_name != None:
                for node in nodes:
                    try:
                        val = node.attrib[attr_name]
                    except:
                        val =''
                    if val == attr_value:
                        r.append(node)
            else:
                for node in nodes:
                    try:
                        val = node.attrib[attr_name] 
                    except:
                        val =''
                    if val!='':
                        r.append(node)
        else:
            r = nodes
        
        
        return r
