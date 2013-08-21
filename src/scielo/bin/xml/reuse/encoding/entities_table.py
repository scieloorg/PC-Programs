
class EntitiesTable:
    def __init__(self, filename='entities'):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        self.table_number2char = {}
        self.table_named2char = {}

        for line in lines:
            values = line.replace("\n", "").split('|')
            if len(values) != 5:
                print(line)
            else:
                char, number_ent, named_ent, ign2, no_accent = values
                if self.is_valid_char(char) and self.is_valid_named(named_ent):
                    #entity_char = named_ent.replace('&','').replace(';','')
                    if self.table_number2char.get(number_ent, None) is None:
                        self.table_number2char[number_ent] = char
                    if self.table_named2char.get(named_ent, None) is None
                        self.table_number2char[named_ent] = char


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

    
    def ent2chr(self, ent):
        r = ent
        if ent in self.table_number2char.keys():
            r = self.table_number2char[ent]
        elif ent in self.table_named2char.keys():
            r = self.table_named2char[ent]
        return r
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
    



