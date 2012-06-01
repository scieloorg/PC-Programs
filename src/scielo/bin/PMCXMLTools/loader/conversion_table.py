class ConversionTable:

    def __init__(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        self.records = {}
        self.index = {}
        
        for l in lines:
            l = l.replace("\n", "").replace("\r", "")
            if '|' in l:
                # s = [ reg, index, tag, subf, x, x, x, 0-6
                #        mandatory, x, x, x,            7-10
                #        xpath, elem, attr, x, x, x,   11-16 
                #        default, table, ]             17-18
	            a = l.replace("\n","").replace("\r","").split('|')
	            d = {}
	            
	            
	            reg = a[0]
	            index = a[1]
	            tag = a[2]
	            subf = a[3]
	            
	            mandatory = a[6]
	            
	            xpath = a[11]
	            elem = a[12]
	            attr = a[13]
	            
	            default = a[17]
	            data_conversion = a[18]
	           
	            self._build_structure_(xpath, elem, attr, default, data_conversion,  reg, tag, subf, mandatory, index)
        #self.print_structure()   
        
    def _build_structure_(self, xpath, elem, attr, default, data_conversion,  reg, tag, subf, mandatory, index):
        if subf == '':
            subf = 'value'
            
        record_types = self.records.keys()
        if not reg in record_types:
            self.records[reg] = {}
            if index == '1':
                index = ''
            self.index[reg] = index
        tags = self.records[reg].keys()
        if not tag in tags:
            self.records[reg][tag] = {}
        
        self.records[reg][tag][subf] = { 'xpath': xpath, 'elem': elem, 'attr': attr, 'default': default, 'mandatory': mandatory,  'data_conversion': data_conversion}
        
    def print_structure(self):
        for k,tags in self.records.items():
            print(k)
            
            for tag,tag_subfs in tags.items():
                print("  " + tag)
                for subf, info in tag_subfs.items():
                    s = "    " + subf
                    for k, i in info.items():
                        s += ' ' + i
                    print(s)
        
    
        