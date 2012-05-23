import xml.etree.ElementTree as etree


class MyXML:
    root = {}
    def __init__(self, xml_filename, debug=0):
        
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

    def get_nodes(self, xpath = '', current_node = None):
        #'//{http://www.w3.org/2005/Atom}link'
        r = []
        n = current_node
        if n == None:
            n = self.root

        if n != None:
            if xpath != '':
                p = './/' + self.ns + xpath
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
        
    def get_text(self, xpath, current_node = None):
        #'//{http://www.w3.org/2005/Atom}link'
        n = current_node
        if n == None:
            n = self.root

        r =[]
        if n != None:
            if self.debug > 0:
                print('---- DEBUG get_text')
                print('xml of current node:')
                print(etree.tostring(n))
                print('xpath:' + xpath)

            entries = self.get_nodes(xpath, n)

            for e in entries:
                test = e.text
                if test == None:
                    test = ''
                r.append(test)
            if entries == None:
                r.append('')

            if self.debug > 0:
                print('resultado:')
                print(r)

                print('---- FIM DEBUG get_text')
        return r

    
