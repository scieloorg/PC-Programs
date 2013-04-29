from unicodedata import normalize

class TableEntities:
    def __init__(self, filename = 'entities'):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        self.table_number2char = {}
        self.table_char2number = {}
        self.table_noaccent = {}
        self.table_named2number = {}
        self.table_named2char = {}

        for line in lines:
            values = line.replace("\n", "").split('|')
            if len(values) != 5:
                print(line)
            else:
                char, number_ent, named_ent, ign2, no_accent = values

                
                if self.is_valid_char(char) and self.is_valid_named(named_ent):
                    entity_char = named_ent.replace('&','').replace(';','')
                    if not char in  self.table_char2number.keys():
                        self.table_char2number[char] = number_ent
                        self.table_noaccent[char] = no_accent
                
                    if  not named_ent in self.table_named2number.keys():
                        self.table_named2number[named_ent] = number_ent
                    
                        if char != entity_char:
                            self.table_named2char[named_ent] = char

                    if number_ent != '' and not number_ent in self.table_noaccent.keys():
                        if char != entity_char:
                            self.table_number2char[number_ent] = char
                        self.table_noaccent[number_ent] = no_accent

    def is_valid_char(self, char):
        r = False
        if char != '':
            if not char in [ '>', '<', '&']:
                r = True
        return  r

    def is_valid_named(self, named):
        r = False
        if named != '':
            if not named in [ '&gt;', '&lt;', '&amp;']:
                r = True
        return  r

    def number2char(self, content):
        for k,v in self.table_number2char.items():
            k2 = k.replace('&', '&amp;')
            content = content.replace(k2, v)
            content = content.replace(k, v)
            

        return content

    def name2number(self, content):
        for k,v in self.table_named2number.items():
            k2 = k.replace('&', '&amp;')
            content = content.replace(k2, v)
            content = content.replace(k, v)
            
            
        return content

    def name2char(self, content):
        for k,v in self.table_named2char.items():            
            k2 = k.replace('&', '&amp;')
            content = content.replace(k2, v)
            content = content.replace(k, v)
            
        return content

    #def find_number_entities(self, content):
    #    l = []
    #    if '&#' in content and ';' in content:
    #        p = content.find('&#')
    #        ent = content[p:]
    #        ent = ent[0:ent.find(';')+1]
    #        if ent in self.table_number2char.keys():
    #            l.append(ent)
    #    return l
        
    #def chr2ent(self, content):

    #    for k,v in self.table_char2number.items():
    #        content = content.replace(k, v)
    #    return content

    #def ent2chr(self, content):
    #    entities = self.find_number_entities(content)
    #    for ent in entities:
    #        content = content.replace(ent, self.table_number2char[ent])
    #    return content
    



