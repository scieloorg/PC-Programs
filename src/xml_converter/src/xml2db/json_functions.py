from unicodedata import normalize

#from tables.entities import Entities
def return_multval(json_data, key):
    r = []
    
    if key in json_data.keys():
        r = json_data[key]

    if type(r) != type([]):
        r = [r]
    return r 

def return_singleval(json_data, key=''):
    r = json_data
    if key != '':
        r = json_data.get(key, '')
    
    if type(r) == type([]):
        r = r[0]
    return r 

class JSON_Normalizer:
    def __init__(self, conversion_tables):
        #self.general_report = general_report
        self.conversion_tables = conversion_tables
        
        

    def format_for_indexing(self, json_record):
        # FIXME
        if type(json_record) == type({}):
            json_record_dest = {}
            for key, json_data in json_record.items():
                json_record_dest[key] = self.format_for_indexing(json_data)
        else:
            if type(json_record) == type(''):
                a = self.conversion_tables.remove_formatting(json_record)
                a = normalize('NFKD', a.decode('utf-8', errors='ignore')).encode(errors='ignore')
                json_record_dest = a
            else:
                if type(json_record) == type([]):
                    a = []
                    for json_data in json_record:
                        r = self.format_for_indexing(json_data)
                        a.append(r)
                    json_record_dest = a
        
        return json_record_dest

    def convert_value(self, json_data, tag, table_name):
        a = return_singleval(json_data, tag)
        if len(a)>0:
            json_data[tag] = self.conversion_tables.normalize(table_name, a)
    
        return json_data
    
    def normalize(self, table_name, value):
        return self.conversion_tables.normalize(table_name, value)

    def normalize_role(self, value):
        return self.conversion_tables.normalize('role', value)
        
    def fill_number_with_zeros(self, number, quantity):
        if not number.isdigit():
            number = ''
        number = '0' * quantity + number
        number = number[-quantity:]

        return number

    def normalize_dates(self, json_data, tag, tag_iso, tag_not_iso):
        #print(json_data)
        

        publication_dates = return_multval(json_data, tag)
        #print('dates')
        #print(tag)
        #print(publication_dates)


        r = ''
        s = ''
        display = ''
        
        for d in publication_dates:
            pdate = ''

            if 'y' in d.keys():
                s = d['y']
                pdate = self.fill_number_with_zeros(d['y'], 4)
            else:
                pdate = '0000'
            if 'm' in d.keys():
                s = d['m'] + '/' + s
                pdate += self.return_month_number(d['m'])
            elif 's' in d.keys():
                s = d['s'] + '/' + s
                pdate += self.return_month_number(d['s'])
            else:
                pdate += '00'
            if 'd' in d.keys():
                s = d['d'] + '/' + s
                pdate += self.fill_number_with_zeros(d['d'], 2)
            else:
                pdate += '00'
            
            if r == '':
                r = pdate
                display = s
            else:
                if pdate > r:
                    r = pdate
                    display = s
        if len(r)>0:
            json_data[tag_iso] = r
            json_data[tag_not_iso] = display
            #print(r)
            #print(s)
        return json_data     

    def normalize_citation_dates(self, json_data, tag, tag_iso, tag_not_iso):
        #print(json_data)
        day = return_singleval(json_data, tag + 'd')
        month = return_singleval(json_data, tag + 'm')
        season = return_singleval(json_data, tag + 's')
        year = return_singleval(json_data, tag )
        
        if len(year)>0:
            isodate = year
            if len(month)>0:
                isodate += self.return_month_number(month)
            elif len(season) >0:
                isodate += self.return_month_number(season)
            else:
                isodate += '00'
            if len(day)>0:
                isodate += self.fill_number_with_zeros(day, 2)
            else:
                isodate += '00'
            del json_data[tag]
            json_data[tag_iso] = isodate
        
        if len(month)>0:
            del json_data[tag + 'm']
        if len(season)>0:
            del json_data[tag + 's']
        if len(day)>0:
            del json_data[tag + 'd']

        return json_data     

    def return_month_number(self, number_or_text_month):
        r = '00'
        if number_or_text_month.isdigit():
            m = '00' + number_or_text_month
            m = m[-2:]
            if 0 <= int(m) <=12:
                r = m
        else:
            r = self.conversion_tables.return_month_number(number_or_text_month)
        return r
