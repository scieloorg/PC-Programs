class ArticleFixer:
    def __init__(self, json_data, tables):
        self.doc = json_data
        self.conversion_tables = tables
    
    def get(self, rec_name, tag):
        if tag in self.doc['doc'][rec_name].keys():
            v = self.doc['doc'][rec_name][tag]
        else:
            v = None
        return None

        
    def fix_keywords(self):

        list = self.get('f', '085')
        lang = ''
        new = [{}]
        if list != None:
            for item in list:
                print(item)
                if 'l' in item.keys():
                    lang = item['l']
                for kw in item['k']:
                    new.append({'k': kw, 'l': lang})
            self.doc['doc']['f']['085'] = new    
        #print(self.doc['doc']['f']['085'])
    
    def get_fixed_value(self, table_name, key):
        v = key 
        if table_name in self.conversion_tables.keys():
            t = self.conversion_tables[table_name]
            if key in t.keys():
                v = t[key]
        return v
    
    def fix_value(self, table_name, rec_name, tag):
        a = self.get(rec_name, tag)
        if a != None:
            if type(a) == type(''):
                self.doc[rec_name][tag] = self.get_fixed_value(table_name, a)
            if type(a) == type([]):
                c = []
                for item in a:
                    c.append(self.get_fixed_value(table_name, item))
                self.doc[rec_name][tag] = c
                
    def fix_data(self):
    	self.fix_keywords()
        self.fix_value('doctopic', 'f', '71')

            

    