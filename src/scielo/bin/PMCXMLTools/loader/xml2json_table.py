
class FieldInfo:
    def __init__(self, start, grouped_by, retag):
        self.subfs = {}
        self.grouped_by = grouped_by
        self.start = start
        self.retag = retag

class XML2JSONTable:

    def __init__(self, filename, report):
        self.report = report
        
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        self.records = {}
        self.grouped_by = {}
        
        for l in lines:
            l = l.replace("\n", "").replace("\r", "")
            if '|' in l:
                # s = [ reg, index, tag, subf, retag, x, x, 0-6
                #        mandatory, x, x,             7-9
                #        start,parent_elem, elem, attr, x, x, x,   10-16 
                #        default, table, ]             17-18
	            a = l.replace("\n","").replace("\r","").split('|')
	            d = {}
	            
	            
	            reg = a[0]
	            grouped_by = a[1]
	            if grouped_by == '1':
	                grouped_by = ''
	            tag = a[2]
	            subf = a[3]
	            retag = a[4]
	            mandatory = a[6]
	            
	            start = a[10]
	            parent_elem = a[11].replace('.//', '')
	            elem = a[12]
	            attr = a[13]
	            
	            default = a[17]
	            data_conversion = a[18]
	           
	            self._build_structure_(start, parent_elem, elem, attr, default, data_conversion,  reg, tag, subf, retag, mandatory, grouped_by)
        #self.print_structure()   
        
    def _build_structure_(self, start, parent_elem, elem, attr, default, data_conversion,  reg, tag, subf, retag, mandatory, grouped_by):
        if subf == '':
            subf = 'value'
            
        record_types = self.records.keys()
        if not reg in record_types:
            self.records[reg] = {}
            self.grouped_by[reg] = grouped_by
        tags = self.records[reg].keys()
        if not tag in tags:
            self.records[reg][tag] = FieldInfo(start, grouped_by, retag)
            
        self.records[reg][tag].subfs[subf] = { 'parent_elem': parent_elem, 'elem': elem, 'attr': attr, 'default': default, 'mandatory': mandatory,  'data_conversion': data_conversion}
        
    def print_structure(self):
        for k,tags in self.records.items():
            self.report.register(k)
            
            for tag,tag_subfs in tags.items():
                self.reporter.register("  " + tag, '')
                for subf, info in tag_subfs.items():
                    s = "    " + subf
                    for k, i in info.items():
                        s += ' ' + i
                    self.report.register(s, '')
        
    
        