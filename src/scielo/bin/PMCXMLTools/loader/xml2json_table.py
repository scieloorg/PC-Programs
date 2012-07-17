
class FieldInfo:
    def __init__(self, xpath_start, xpath_for_level1, level2_rename):
        self.level3_data = {}
        self.xpath_for_level1 = xpath_for_level1
        self.xpath_start = xpath_start
        self.level2_rename = level2_rename

class XML2JSONTable:

    def __init__(self, filename, report):
        self.report = report
        
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        self.level1 = {}
        self.xpath_for_level1 = {}
        
        for l in lines:
            l = l.replace("\n", "").replace("\r", "")
            if '|' in l:
                # s = [ level1_label, xpath_for_level1, level2_label, level3_label, level2_rename, x, x, 0-6
                #        mandatory, x, x,             7-9
                #        xpath_start,xpath_parent_elem, xpath_elem, xpath_attr, x, x, x,   10-16 
                #        default_value, table, ]             17-18
	            a = l.replace("\n","").replace("\r","").split('|')
	            d = {}
	            
	            
	            level1_label = a[0]
	            xpath_for_level1 = a[1]
	            if xpath_for_level1 == '1':
	                xpath_for_level1 = ''
	            level2_label = a[2]
	            level3_label = a[3]
	            level2_rename = a[4]
	            mandatory = a[6]
	            
	            xpath_start = a[10]
	            xpath_parent_elem = a[11].replace('.//', '')
	            xpath_elem = a[12]
	            xpath_attr = a[13]
	            
	            default_value = a[17]
	            conversion_function = a[18]
	           
	            self._build_structure_(xpath_start, xpath_parent_elem, xpath_elem, xpath_attr, default_value, conversion_function,  level1_label, level2_label, level3_label, level2_rename, mandatory, xpath_for_level1)
        #self.print_structure()   
        
    def _build_structure_(self, xpath_start, xpath_parent_elem, xpath_elem, xpath_attr, default_value, conversion_function,  level1_label, level2_label, level3_label, level2_rename, mandatory, xpath_for_level1):
        if level3_label == '':
            level3_label = 'value'
            
        label1_labels = self.level1.keys()
        if not level1_label in label1_labels:
            self.level1[level1_label] = {}
            self.xpath_for_level1[level1_label] = xpath_for_level1
        level2_labels = self.level1[level1_label].keys()
        if not level2_label in level2_labels:
            self.level1[level1_label][level2_label] = FieldInfo(xpath_start, xpath_for_level1, level2_rename)
            
        self.level1[level1_label][level2_label].level3_data[level3_label] = { 'xpath_parent_elem': xpath_parent_elem, 'xpath_elem': xpath_elem, 'xpath_attr': xpath_attr, 'default_value': default_value, 'mandatory': mandatory,  'conversion_function': conversion_function}
        
    def print_structure(self):
        for k,level2_labels in self.level1.items():
            self.report.display_data('level1 label', k)
            
            for level2_label,level3_spec in level2_labels.items():
                self.reporter.display_data('level2 label', level2_label)
                for level3_label, info in level3_spec.items():
                    s = "    " + level3_label
                    for k, i in info.items():
                        s += ' ' + i
                    self.report.display_data('level3 label', s)
        
    
        