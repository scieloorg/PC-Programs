from table_ent_and_char import TableEntAndChar
from table_conversion import ConversionTables


class ArticleFixer:
    def __init__(self):
        self.conversion_tables = ConversionTables()
        self.table_entity_and_char = TableEntAndChar()
        self.sections = {}
    
    

    def get(self, doc, rec_name, tag):
        if tag in doc['doc'][rec_name].keys():
            v = doc['doc'][rec_name][tag]
        else:
            v = None
        return v

    def replace_value(self, doc, table_name, rec_name, tag):
        a = self.get(doc, rec_name, tag)
        if a != None:
            doc['doc'][rec_name][tag] = self.conversion_tables.return_fixed_value(table_name, a)
        return doc
                
    

    def fix_keywords(self, doc):
        list = self.get(doc, 'f', '085')
        
        #print(list)
        lang = ''
        new = [{}]
        if list != None:
            for item in list:
                if 'l' in item.keys():
                    lang = item['l']
                for kw in item['k']:
                    new.append({'k': kw, 'l': lang})
            doc['doc']['f']['085'] = new    
        return doc
    
    

    def fix_data(self, doc):
        doc = self.fix_keywords(doc)
        doc = self.replace_value(doc, 'doctopic', 'f', '71')
        doc['doc']['f']['42'] = '1'
        
        if len(doc['doc']['f']['065']) == 4:
            doc['doc']['f']['065'] = doc['doc']['f']['065'] + self.return_month_number(doc['doc']['f']['064']) + '00'
        doc = self.fix_38(doc)

        doc = self.fix_affiliations(doc)

        return doc
    
    def fix_affiliations(self, doc):
        aff = self.get(doc, 'f', '070')
        if aff != None:
            if type(aff) == type([]):
                new_aff = []
                for a in aff:
                    r = self.fix_aff(a)
                    new_aff.append(r)

            else:
                new_aff = self.fix_aff(aff)
            if len(new_aff) > 0:
                doc['doc']['f']['070'] = new_aff
        return doc

    def fix_aff(self, aff):

        new_aff = aff 
        list = []
        unmatched = []
        if ',' in aff['_']:
            aff_parts = aff['_'].split(',')
            for key, s in self.conversion_tables.tables['aff'].items():
                for part in aff_parts:
                    if key in part:
                        new_aff[s] = part.strip() 
                        list.append(part)
            for part in aff_parts:
                if not part in list:
                    unmatched.append(part)
            if len(unmatched) > 0:
                new_aff['2'] = ', '.join(unmatched)
            aff = new_aff
        return aff 



    
    def fix_38(self, doc):
        v38 = []
        fig_count = self.get(doc, 'f', '901')
        if fig_count != None:

            if int(fig_count)>0:
                v38.append('GRA')
            del doc['doc']['f']['901']
        tab_count = self.get(doc, 'f', '900')
        if tab_count != None:
            if int(tab_count)>0:
                v38.append('TAB')
            del doc['doc']['f']['900']
        if len(v38) > 0:
            doc['doc']['f']['38'] = v38
        return doc
    
    def return_month_number(self, month_range):
        m = month_range
        if '-' in m:
            m = m[m.find('-')+1:]

        return self.conversion_tables.return_fixed_value('month', m) 

    def format_for_indexing(self, json_record):
        if type(json_record) == type({}):
            json_record_dest = {}
            for key, json_data in json_record.items():
                json_record_dest[key] = self.format_for_indexing(json_data)
        else:
            if type(json_record) == type(''):
                json_record_dest = self.table_entity_and_char.remove_accent(self.conversion_tables.remove_formatting(json_record))
            else:
                if type(json_record) == type([]):
                    a = []
                    for json_data in json_record:
                        r = self.format_for_indexing(json_data)
                        a.append(r)
                    json_record_dest = a
        
        return json_record_dest

    
    def get_section_id(self, json_data):
        if '49' in json_data['doc']['f']:   
            section = json_data['doc']['f']['49']
            if not section in self.sections.keys():
                self.sections[section] = 'SECTION' + str(len(self.sections))
            json_data['doc']['f']['49'] = self.sections[section]
        if not '49' in json_data['doc']['f']: 
            json_data['doc']['f']['49'] = 'nd'
        return json_data 

          

    