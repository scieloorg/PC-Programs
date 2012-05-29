class ConversionTable:

    def __init__(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        self.records = {}
        self.table = {}
        for l in lines:
            a = l.replace("\n","").split('|')
            d = {}
            d['xpath'] = a[0]
            
            
            d['reg'] = a[1]
            d['index'] = a[2]
            d['tag'] = a[3]
            d['subf'] = a[4]
            self.table[a[0]] = d
            
            self._build_(d['xpath'], d['reg'], d['tag'], d['subf'])
            
    def _build_(self, xpath, reg, tag, subf='*'):
        if subf == '':
            subf = '*'
            
        record_types = self.records.keys()
        if not reg in record_types:
            self.records[reg] = {}
        
        tags = self.records[reg].keys()
        if not tag in tags:
            self.records[reg][tag] = {}
         
        self.records[reg][tag][subf] = xpath
        
    def get_records_structure(self):
        return self.records
                        
    def get_storage_info(self, xpath):
        return self.table[xpath]
        
    def get_table(self):
        return self.table
        
    