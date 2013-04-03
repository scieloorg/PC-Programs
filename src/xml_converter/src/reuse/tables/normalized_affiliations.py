# -*- coding: utf-8 -*-

import os.path 

class NormalizedAffiliations:

    #def __init__(self, filename = 'inputs/valid_affiliations.seq', location_table = Locations('inputs/valid_locations.seq')):
    def __init__(self, filename, location_table):
        self.filename = filename
        self.institution_names = {}
        self.table_location = location_table
        self.table_location.load_locations()
        if os.path.exists(filename):
            self.load_affiliations()



    def read_file(self, filename):
    	f = open(filename, 'r')
        content = f.readlines()
        f.close()
        return content
    
    def load_affiliations(self):
        rows = self.read_file(self.filename)
        for row in rows:
            affiliation = row.replace('\n', '')
            if len(affiliation) > 0:
                loc = affiliation.split('|')
                
                
                self.institution_names[loc[0].upper()] = loc[0]

    def is_institution_name(self, might_be):
        return might_be.upper() in self.institution_names.keys()

    
    def generate_valid_table(self, input_filename, err_filename):
        rows = self.read_file(input_filename)
        
        f = open(err_filename, 'w')

        affiliations = {}
        print(len(rows))
        for row in rows:
            affiliation = row.replace('\n', '')
            if len(affiliation) > 0:
                affiliation = affiliation[0:affiliation.find('|')]
                
                err_type = self.check_affiliation(affiliation)
                if err_type == '':
                    affiliations[affiliation] = affiliation
                elif err_type == 'critical':
                    f.write(row)

        f.close()
        
        print(len(affiliations))
        f = open(self.filename, 'w')
        s = affiliations.keys()
        s.sort()
        for items in s:
            f.write(items + '\n')
        f.close()
   
    def check_affiliation(self, affiliation):
        err_type = ''
        
        
        if err_type == '':
            for c in ',;-/':
                if affiliation.endswith(c) or affiliation.startswith(c):
                    err_type = 'critical'
                    break
        if err_type == '':
            for c in '@<>':
                if c in affiliation:
                    err_type = 'critical'
                    break
        if err_type == '':
            if not ' - ' in affiliation:
                if ' -' in affiliation or '- ' in affiliation:
                    err_type = 'critical'
        if err_type == '':
            if 'epart' in affiliation and not 'nivers' in affiliation :
                err_type = 'critical'

        return err_type
       
    def remove_tags(self, text):
        
        while '</' in text:
            p = text.find('</')
            close_tag = text[p:]
            p = close_tag.find('>')
            previous = text
            if p>0: 
                close_tag = close_tag[0:p+1]
                text = text.replace(close_tag, '[AFFSEP]')
                tag = close_tag.replace('</', '<')
                
                text = text.replace(tag, '')
                tag = tag[0:len(tag)-1]
                while tag in text:
                    p = text.find(tag)
                    tag = text[p:]
                    p = tag.find('>')
                    if p>0: 
                        tag = tag[0:p+1]
                        text = text.replace(tag, '')  
            if text == previous:
                text = text.replace('<', '&lt;').replace('>', '&gt;')
        return text       

    def return_missing_data(self, aff, check_data = '_cp'):
        
        missing = []

        for item in check_data:
            if not item in aff.keys():
                missing.append(item)
        return missing

    

    def return_identified_data(self, aff):
        unidentified = []
        if '9' in aff.keys():           
            full_affiliation = aff['9']
            if '</label>' in full_affiliation:
                full_affiliation = full_affiliation[full_affiliation.find('</label>')+len('</label>'):]
            
            if not '</' in full_affiliation:
                unidentified = full_affiliation.split(',')
            unidentified = [ i.strip() for i in unidentified ]
        return unidentified

    def return_the_institution(self, list):
        r = ''
        for item in list:
            
            if self.is_institution_name(item):
                r = item
                #print(r)
                break
        return r
    def oldcomplete_affiliation(self, aff):
        # l,i,9,institution,p,c,s,3,2,1,_
        unidentified = []
        print('~'*80)
        print('aff')
        print(aff)
        missing = self.return_missing_data(aff, 'cspe_1')
        if len(missing) > 0:
            unidentified = self.return_identified_data(aff)
        print('missing')
        print(missing)

        print('unidentified')
        print(unidentified)

        for missing_item in missing:
            if missing_item == '_':                   
                if 'institution' in aff.keys():
                    if type(aff['institution']) == type(''):
                        aff['_'] = aff['institution']
                    elif type(aff['institution']) == type([]):
                        aff['_'] = ', '.join(aff['institution'])
                    del aff['institution']
                if not '_' in aff.keys():
                    item = self.return_the_institution(unidentified)
                    if item != '' :
                        aff['_'] = item
                        unidentified.remove(item)
                        
            elif missing_item == 'p':
                item = self.table_location.return_the_country(unidentified)
                if item != '' :
                    aff['p'] = item
                    unidentified.remove(item)
                if not 'p' in aff.keys():
                    if 'c' in aff.keys() and 's' in aff.keys():
                        country = self.table_location.return_country(aff['c'], aff['s'])
                        if country != '':
                            aff['p'] = country
                
            elif missing_item == 'c':
                item = self.table_location.return_the_city(unidentified)
                if item != '' :
                    aff['c'] = item
                    unidentified.remove(item)
            elif missing_item == 's':
                item = self.table_location.return_the_state(unidentified)
                if item != '' :
                    aff['s'] = item
                    unidentified.remove(item)
            elif missing_item == 'e':
                for item in unidentified:
                    if '@' in item and '.' in item:
                        aff['e'] = item
                        unidentified.remove(item)
                        break
            elif missing_item == '1':
                aff['1'] = ', '.join(unidentified)
            print('missing_item')
            print(missing_item)
            print('aff modificado')
            print(aff)

        if not '_' in aff.keys():
            if '1' in aff.keys():
                aff['_'] = aff['1']
                del aff['1']
        print(aff)
        print('*'*80)
        return aff 



    def complete_affiliation(self, aff):
        # l,i,9,institution,p,c,s,3,2,1,_

        unidentified = self.return_identified_data(aff)
        test = 'epcs_1'
        
        for t in test:
            item = ''
            if not t in aff.keys():
                if t == 'p':
                    item = self.table_location.return_the_country(unidentified)
                    if len(item) == 0:
                        if 'c' in aff.keys() and 's' in aff.keys():
                            item = self.table_location.return_country(aff['c'], aff['s'])
                elif t == 'c':
                    item = self.table_location.return_the_city(unidentified)
                elif t == 's':
                    item = self.table_location.return_the_state(unidentified)
                elif t == 'e':
                    for u in unidentified:
                        if '@' in u and '.' in u:
                            item = u
                            break
                elif t == '1':
                    item = ', '.join(unidentified)

                if len(item) > 0:
                    aff[t] = item 
                    if item in unidentified:
                        unidentified.remove(item)
                    
                    if not '8' in aff.keys():
                        aff['8'] = ''
                    aff['8'] += t


        if not '_' in aff.keys():
            if '1' in aff.keys():
                aff['_'] = aff['1']
                del aff['1']
 
        return aff 
    
    def complete_affiliations(self, affiliations):
        # several cases, the country is suppressed
        # 
        new = []
        country = ''
        state = ''
        city = ''
        affiliations.reverse()
        for aff in affiliations:
            for k, v in aff.items():
                if type(v) != type(''):
                    if type(v) == type([]):
                        aff[k] = ', '.join(v)
            if 'p' in aff.keys():
                country = aff['p']
            else:
                if country != '':
                    aff['p'] = country
            if 'c' in aff.keys():
                city = aff['c']
            else:
                if city != '':
                    aff['c'] = city
            if 's' in aff.keys():
                state = aff['s']
            else:
                if state != '':
                    aff['s'] = state
            new.append(aff)

        new.reverse()

        
        return new
        
    def print_aff(self, affs):
        for a in affs:
            print('-' * 30)
            for k,i in a.items():
                print(k + ' | ' + i)
        							
if __name__ == '__main__':
    import os
    t = NormalizedAffiliations('inputs/valid_affiliations.seq')
    if not os.path.exists('inputs/valid_affiliations.seq'): 
        t.generate_valid_table('inputs/aff-city-state-country.seq', 'inputs/invalid_affiliations.csv')
    