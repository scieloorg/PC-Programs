# -*- coding: utf-8 -*-

class LocationTable:

    def __init__(self, filename):
        self.filename = filename
        self.location_parts = {}
        self.city_state = {} 
        
        self.part_order = ['city', 'state', 'country']


        self.location_parts['country'] = {}
        self.location_parts['city'] = {}
        self.location_parts['state'] = {}

    def read_file(self, filename):
    	f = open(filename, 'r')
        content = f.readlines()
        f.close()
        return content
    
    def load_locations(self):
        rows = self.read_file(self.filename)
        for row in rows:
            location = row.replace('\n', '')
            if len(location) > 0:
                loc = location.split('|')
                loc_upper = location.upper().split('|')
                 
                if len(loc[1]) > 0:
                    self.city_state[loc[0] + loc[1]] = loc[2]

                i = 0
                for part_name in self.part_order:
                    if not loc_upper[i] in self.location_parts[part_name].keys():
                        self.location_parts[part_name][loc_upper[i]] = 0
                    self.location_parts[part_name][loc_upper[i]] += 1
                
                    i += 1

                
    
    def return_the_city(self, list):
        r = ''
        for item in list:
            if self.is_city(item):
                r = item
                break
        return r
    
    def return_the_state(self, list):
        r = ''
        for item in list:
            if self.is_state(item):
                r = item
                break
        return r

    def return_the_country(self, list):
        r = ''
        for item in list:
            if self.is_country(item):
                r = item
                break
        return r

    def is_what(self, might_be):
        be = might_be.upper()
        count = {'country':0, 'state': 0, 'city': 0}
        for part_name in self.part_order:
            if be in self.location_parts[part_name].keys():
                count[part_name] = self.location_parts[part_name][be]

        greater = 0
        key = ''
        for k, c in count.items():
            if c > greater:
                greater = c
                key = k
        return key 


    def is_country(self, might_be):
        r = self.is_what(might_be)
        return  (r == 'country')

    
    def is_city(self, might_be):
        r = self.is_what(might_be)
        return  (r == 'city')

    
    def is_state(self, might_be):
        r = self.is_what(might_be)
        return  (r == 'state')


    def return_country(self, city, state):
        r = ''
        if len(state) > 0 and len(city) > 0:
            k = city + state
        
            if k in self.city_state.keys():
                r = self.city_state[k]
        return r

    def generate_valid_table(self, input_filename, err_filename):
        rows = self.read_file(input_filename)
        

        f = open(err_filename, 'w')

        locations = {}
        print(len(rows))
        for row in rows:
            location = row.replace('\n', '')
            if len(location) > 0:
                pid = location[location.rfind('|')+1:]
                pid = pid[0:23]
                year = pid[10:14]

                
                location = location[0:location.rfind('|')]
                
                err_type = self.check_location(location)
                if err_type == '':
                    locations[location] = location.split('|')
                elif err_type == 'critical':
                    f.write(year + '|' + pid + '|' + location.replace('|', ', ') + '\n')

        f.close()
        
        print(len(locations))
        f = open(self.filename, 'w')
        for items in locations.keys():
            f.write(items + '\n')
        f.close()
   
    def check_location(self, location):
        err_type = ''
        
        for i in range(0,10):
            if str(i) in location:
                err_type = 'critical'
                break
        if err_type == '':
            for c in ',@:()<>;':
                if c in location:
                    err_type = 'critical'
                    break
        if err_type == '':
            if ' -' in location or '- ' in location:
                err_type = 'critical'
                

        if err_type == '':
            location_splited = location.split('|')
            if len(location_splited) == 3:
                if (len(location_splited[0]) < 3) or (len(location_splited[2]) < 2):
                    err_type = 'incomplete'
            else:
                print(location)
        
        return err_type
            							
if __name__ == '__main__':
    import os
    t = LocationTable('inputs/valid_locations.seq')
    if not os.path.exists('inputs/valid_locations.seq'): 
        t.generate_valid_table('inputs/city-state-country-pid.seq', 'inputs/invalid_locations.csv')
    t.load_locations()
    l = ['São PauloSP', 'Madri', '?', 'Paris', 'España', 'United States', 'GB', '?', 'Colombia', 'España', 'BotucatuSão Paulo',  'Santa MariaRS', 'São CarlosSP', 'BrasiliaDF', 'São LuisMA', 'Brasil', 'UK', 'Lima', 'São Paulo', 'Madri', '?', 'Rio de JaneiroRJ', 'España', 'SalvadorBA', 'BA', '?', 'Colombia', 'España', 'São Paulo', 'Madri', '?', ]    
    for c in l:
        if t.is_country(c) == True:
            print(c + ' is country.')
        else:
            print(c + ' is not country.')

    for c in l:
        if t.is_city(c) == True:
            print(c + ' is city.')
        else:
            print(c + ' is not city.')

    for c in l:
        if t.is_state(c) == True:
            print(c + ' is state.')
        else:
            print(c + ' is not state.')

    l = [('São Paulo', 'SP'), ('Madri', '?'), ('Paris', 'España'), ('United States', 'GB'), ('?', 'Colombia'), ('Madri','España'), ('Botucatu', 'São Paulo'),  ('Santa Maria', 'RS'), ('São Carlos', 'SP'), ('Brasilia', 'DF'), ('São Luis', 'MA'), ('Rio de Janeiro', 'RJ'),  ('Salvador', 'BA'), ]    
    
    for c in l:
        print(c)
        print(t.return_country(c[0], c[1]))