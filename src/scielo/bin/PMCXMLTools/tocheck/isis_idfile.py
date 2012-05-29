
class idfile:
    def __init__(self, filename, mfn, encoding):
        self.filename = filename
        self.mfn = mfn
        self.encoding = encoding
        self.f = open(filename,'ab')

class ConvertionTable:
    def __init__(self, ent_table, new_ent_filename):
        self.new_ent_list = open(new_ent_filename,'a')
        self.table = {}

        f = open(ent_table,'r')
        t = f.readlines()
        f.close()


        for item in t:
            a = item.strip("\n").split('|')
            if len(a)==1:
                a.append(a[0])
            self.table[str(a[0])] = str(a[1])
        #print(self.table)
        
    def close(self):
        self.new_ent_list.close()
        
    def convert_utf8_to_ent(self, text):
        for c in text:
            chnum = ord(c)
            if chnum>256:
                ent = '&#' + str(chnum) + ';'
                text = text.replace(c, ent)

        return text

    def list_ent(self, text):
        if '&#' in text:
            parts = text.split('&#')
            i=''
            for part in parts:
                if i=='x':
                    ent = '&#' + part[0:part.find(';')+1]
                    self.new_ent_list.write(ent)
                i='x'


    def convert(self, text):
        #print('convert (1): ' +text)
        text = self.convert_utf8_to_ent(text)
        #print('convert (2): ' +text)
        for k,v in self.table.items():
            text = text.replace(k,v)
        #print('convert (3): ' +text)
        self.list_ent(text)
        return text
        
class ISIS_IDFile:

    def __init__(self, id_filename):
        self.file_key = ['iso-8859-1','utf-8']
        self.file  = {}
        for key in self.file_key:
            self.file[key] = idfile(id_filename + '_' + key, 0, key)
        self.table = ConvertionTable('utf2iso.seq', 'ent2check.txt')

    def save(self, r):
        r_encoded = ''
        selected = 'iso-8859-1'
        try:
            r_encoded = r.encode(selected)            
        except:
            r2 = self.table.convert(r)
            try:
                r_encoded = r2.encode(selected)
                r = r2
            except:
                selected = 'utf-8'
        
        if not selected =='':
            #e = bytes(data, selected)
            e = r_encoded
            self.file[selected].f.write(e)


    def close_files(self):
        for k,v in self.file.items():
            v.f.close()
        self.table.close()
