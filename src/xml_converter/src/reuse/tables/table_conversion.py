class ConversionTables:
    def __init__(self, table_filename = 'tables/tables'):
        self.tables = {}
        f = open(table_filename, 'r')
        lines = f.readlines()
        f.close()
        for l in lines:
            table_name, key, value = l.replace("\n",'').split('|')
            if len(table_name) > 0:
                if not table_name in self.tables.keys():
                    self.tables[table_name] = {}
            if len(key)>0:
                self.tables[table_name][key] = value
    
    def return_month_number(self, textual_month):
        r = '00'
        months = self.tables['month'].keys()
        if textual_month in months:
            r = self.tables['month'][textual_month]
        else:
            for m in months:
                if m in textual_month:
                    r = self.tables['month'][m]
        return r

    def normalize(self, table_name, key):
        v = key 
        if table_name in self.tables.keys():
            t = self.tables[table_name]
            if key in t.keys():
                v = t[key]
        return v

    def remove_formatting(self, text):
        new_value = text
        if '>' in text and '<' in text:        
            text = text.replace('>', '>-BREAK-')
            text = text.replace('<', '-BREAK-<')
            parts = text.split('-BREAK-')
            new_value = ''
            for part in parts:
                if '<' in part and '>' in part:
                    pass
                else:
                    new_value += part                    
        return new_value

    def table(self, table_name):
        return self.tables.get(table_name, {}) 
