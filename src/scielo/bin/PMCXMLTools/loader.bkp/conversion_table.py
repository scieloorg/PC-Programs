class ConversionTable:

    def __init__(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        self.records = {}
        self.tables = {}
        for l in lines:
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
        self.print_structure()   
        
    def _build_structure_(self, xpath, elem, attr, default, data_conversion,  reg, tag, subf, mandatory, index):
        if subf == '':
            subf = '*'
            
        record_types = self.records.keys()
        if not reg in record_types:
            self.records[reg] = {}
        tags = self.records[reg].keys()
        if not tag in tags:
            self.records[reg][tag] = {}
        self.records[reg][tag][subf] = { 'xpath': xpath, 'elem': elem, 'attr': attr, 'default': default, 'mandatory': mandatory, 'index': index, 'data_conversion': data_conversion}
        
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
        
    def format_records(self, xml_manager):
        records = 'ioh'
        tagged = {}
        for r  in records:
            tagged[r] = self.format_record(self.records[r], xml_manager)
        return tagged   
    
    def _return_one_value_(self, xml_manager, xpath,  attr, default, data_conversion):
        
        value = default
        if value == '':
                 
            if attr != '':
                values = xml_manager.return_attr_values(xpath, attr)
            else:
                values = xml_manager.return_elem_values(xpath)
        
            value = xml_manager.return_array_or_str(values)
        value = self._convert_data_(value, data_conversion)         
        return value
        
    
        
    def _convert_data_(self, value, data_conversion):
        if value != '' and data_conversion !='':
            v = ''
            try:
                t = self.tables[data_conversion]
                try:
                    v = self.tables[data_conversion][value]
                except:
                    print('Expected data_conversion of ' + data_conversion + ': ' + value)
            except:
                print('Expected table ' + data_conversion) 
            if v != '':
                value = v                    
        return value
        
    def format_record(self, tags, xml_manager):
        record_content = ''
        first = '' 
        for tag, subfs in tags.items():
            value = ''
            if len(subfs) == 1:
                for subf, info in subfs.items():
                    value = self._return_one_value_(xml_manager, info['xpath'], info['attr'], info['default'], info['data_conversion'])
                    value = self._return_value_with_subf(value, info['mandatory'], subf, info['xpath'] + ' ' + info['attr'])
                record_content = record_content + self._tag_it_(tag, value)           
            else:
                subf_xpath = {}
                for subf, info in subfs.items():
                    subf_xpath[subf] = (info['elem'], info['attr'])
                occs = xml_manager.return_multi_values(info['xpath'], subf_xpath)
                for occ in occs:
                    value = ''
                    for subf, subf_content in occ.items():
                        subf_content = self._convert_data_(subf_content, info['data_conversion'])
                        v = self._return_value_with_subf(subf_content, info['mandatory'], subf, info['xpath'] + ' ' + info['elem'] + info['attr'])
                        if not '^' in v:
                            value = v + value
                        else:
                            value = value + v
                    record_content = record_content + self._tag_it_(tag, value)
            
        return record_content 
               
    def _return_value_with_subf(self, value, is_mandatory, subf, debug_message):
        if value == '' and is_mandatory == 'MANDATORY':
            print('Expected   ' + debug_message )
        if subf == '*':
            r = value
        else:
            r = '^' + subf + value
        return r         
    
    def _tag_it_(self, tag, value):
        field_tag = '00' + tag
        field_tag = field_tag[-3:]
        r = ''
        if value != '':
            r = '!v' + field_tag + '!' + value + "\r\n"
        return r
        
        
        