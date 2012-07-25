class TableEntAndChar:
    def __inti__(self, filename = 'table_ent'):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        self.table_ent2chr = {}
        self.table_chr2ent = {}
        for line in lines:
            char, ent, ign1, ign2 = line.split('|')
            self.table_chr2ent[char] = ent
            self.table_ent2chr[ent] = char
    

    def convert_entities(self, content):
        for k,v in self.table_ent2chr:
            content = content.replace(k, v)
        return content
    def convert_chars(self, content):
        for k,v in self.table_chr2ent:
            content = content.replace(k, v)
        return content





