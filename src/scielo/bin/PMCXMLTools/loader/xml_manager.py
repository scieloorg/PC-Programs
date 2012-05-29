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
            	    print('Invalid xpath: ' + p)
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
    def get_values(self, xpath):
        v = []
        nodes = self.return_nodes(xpath)
        for node in nodes:
            v.append(node.text)
        if len(v)==1:
            r = v[0]
        else:
            if len(v)==0:
                r = ''
            else:
                r = v
        return r
    def get_attr_values(self, xpath, attr_name):
        v = []
        nodes = self.return_nodes(xpath)
        for node in nodes:
            try:
                attr = node.attrib[attr_name]
            except:
                attr = ''
            if attr != '': 
                v.append(attr)
        if len(v)==1:
            r = v[0]
        else:
            if len(v)==0:
                r = ''
            else:
                r = v
        return r
         
   
#filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/0004-282X-anp-69-859.xml'
filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml.local.xml'
x = XMLManager(filename)
#print(x.return_nodes('.//xref[@rid="r07"]'))
#print(x.return_nodes())
#print(x.return_nodes('.//article-meta//volume[../issue]'))