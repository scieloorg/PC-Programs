class ConversionTable:

    def __init__(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        
        
        
        self.records = {}
        self.table = {}
        for l in lines:
            a = l.replace("\r\n","").split('|')
            d = {}
            d['xpath'] = a[5]
            
            
            d['reg'] = a[0]
            d['index'] = a[1]
            d['tag'] = a[2]
            d['subf'] = a[3]
            d['mandatory'] = a[4]
           
            self.table[a[0]] = d
            
            self._build_(d['xpath'], d['reg'], d['tag'], d['subf'], d['mandatory'] )
        print(self.records)   
    def _build_(self, xpath, reg, tag, subf, mandatory):
        if subf == '':
            subf = '*'
            
        record_types = self.records.keys()
        if not reg in record_types:
            self.records[reg] = {}
        
        tags = self.records[reg].keys()
        if not tag in tags:
            self.records[reg][tag] = {}
            
             
        self.records[reg][tag][subf] = { 'xpath': xpath, 'mandatory': mandatory}
        
    
        
    def format_records(self, xml_manager):
        
        tagged = {}
        
        for rec_type, rec_tags in self.records.items():
            tagged[rec_type] = self.format_record(rec_tags, xml_manager)
        return tagged   
        
    def format_record(self, tags, xml_manager):
        record_content = ''
        for tag, subfs in tags.items():
            r = ''
            for subf, info in subfs.items():
                value = xml_manager.get_values(info['xpath'])
                if value == '' and info['mandatory'] == 'MANDATORY':
                    print('Expected   ' + "\n    " + info['xpath'] )
                if subf == '*':
                    r = value
                else:
                    r = r + '^' + subf + value
            record_content = record_content + self.tag_it(tag, r)
        return record_content        
     
    def tag_it(self, tag, value):
        field_tag = '00' + tag
        field_tag = field_tag[-3:]
        r = ''
        if value != '':
            r = '!v' + field_tag + '!' + value + "\r\n"
        return r