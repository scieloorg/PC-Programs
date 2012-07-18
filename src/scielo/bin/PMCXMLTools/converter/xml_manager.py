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
        
    
    
    def return_node_value(self, node):
        
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
    
    
    
    def return_node_attr_value(self, node, attr_name):
        self.report.debugging(node, 'XMLManager.return_node_attr_value: node', 1)
        self.report.debugging(attr_name, 'XMLManager.return_node_attr_value: attr_name', 1)
        attr = '' 
        if node != None:
            if len(node.attrib)>0:
                if ':' in attr_name:
                    aname = attr_name[attr_name.find(':')+1:]
                    for k,a in node.attrib.items():
                        if aname == k[k.find('}')+1:]:
                            attr = a 
                            self.report.debugging(k, 'XMLManager.return_node_attr_value: attr', 1)
                else:
                    if attr_name[0:1] == '@':
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
 
    
   
