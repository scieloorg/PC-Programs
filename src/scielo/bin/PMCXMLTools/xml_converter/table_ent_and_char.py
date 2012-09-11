class TableEntAndChar:
    def __init__(self, filename = 'inputs/table_ent_char'):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        self.table_ent2chr = {}
        self.table_chr2ent = {}
        self.table_noaccent = {}
        self.table_nonum = {}
        for line in lines:
            char, ent, entnonum, ign2, no_accent = line.replace("\n", "").split('|')
            self.table_chr2ent[char] = ent
            self.table_ent2chr[ent] = char
            self.table_noaccent[ent] = no_accent
            self.table_noaccent[char] = no_accent
            self.table_nonum[entnonum] = ent
    
    def ent2chr(self, content):
        entities = self.find_entities(content)
        for ent in entities:
            content = content.replace(ent, self.table_ent2chr[ent])
        return content
    
    def remove_accent(self, content):
        for k,v in self.table_noaccent.items():
            content = content.replace(k, v)
        return content

    def replace_to_numeric_entities(self, content):
        for k,v in self.table_nonum.items():
            content = content.replace(k, v)
        return content        

    def find_entities(self, content):
        l = []
        if '&#' in content and ';' in content:
            p = content.find('&#')
            ent = content[p:]
            ent = ent[0:ent.find(';')+1]
            if ent in self.table_ent2chr.keys():
                l.append(ent)
        return l
    def chr2ent(self, content):

        for k,v in self.table_chr2ent.items():
            content = content.replace(k, v)
        return content




