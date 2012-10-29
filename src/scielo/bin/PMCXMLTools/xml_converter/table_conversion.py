class ConversionTables:
    def __init__(self):
        self.tables = {}
        f = open('inputs/tables', 'r')
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

    def return_fixed_value(self, table_name, key):
        v = key 
        if table_name in self.tables.keys():
            t = self.tables[table_name]
            if key in t.keys():
                v = t[key]
        return v

    def remove_formatting(self, value):
        new_value = value
        if '<' in value and '>' in value:
            for k, v in self.tables['formatting'].items():
                new_value = new_value.replace(k, v).strip()
                if not '<' in new_value:
                	break
                if not '>' in new_value:
                	break
                	
        return new_value

    
