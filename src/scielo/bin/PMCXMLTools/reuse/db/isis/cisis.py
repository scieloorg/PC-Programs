import os
import sys

class CISIS:
    def __init__(self, cisis_path):
        cisis_path = cisis_path.replace('\\', '/')
        
        if os.path.exists(cisis_path):
            self.cisis_path = cisis_path
        else:
            print('Invalid cisis path: ' + cisis_path)


    def id2i(self, id_filename, mst_filename):
        cmd = self.cisis_path + '/id2i ' + id_filename + ' create=' + mst_filename
        os.system(cmd)
    
    def append(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + '  append=' + dest + ' now -all'
        os.system(cmd)
        
    def create(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + '  create=' + dest + ' now -all'
        os.system(cmd)
        
    def id2mst(self, id_filename, mst_filename, reset):
        from tempfile import mkstemp
    
        _, temp = mkstemp()
        self.id2i(id_filename, temp)

        if reset:
            self.create('null count=0', mst_filename)
        self.append(temp, mst_filename)
        os.remove(temp)

    def i2id(self, mst_filename, id_filename):
        cmd = self.cisis_path + '/i2id ' + mst_filename + ' > ' + id_filename 
        os.system(cmd)

    def copy_record(self, src_mst_filename, mfn, dest_mst_filename):
        cmd = self.cisis_path + '/mx ' + src_mst_filename + ' from=' + mfn + ' count=1 ' + ' append=' + dest_mst_filename + ' now -all'
        os.system(cmd)
        
    def find_record(self, mst_filename, expression):
        r = mst_filename + expression
        cmd = self.cisis_path + '/mx ' + mst_filename + ' bool="' + expression + '"  lw=999 "pft=mfn/" now > ' + r

        os.system(cmd)
        f = open(r, 'r')
        c = f.readlines()
        f.close()

        a = []
        for l in c:
            a.append(l.replace('\n', ''))

        return a

class IDFile:

    def __init__(self, convert2utf8 = True):
        self.convert2utf8 = convert2utf8

    def id2json(self, id_filename):
        f = open(id_filename, 'r')
        c = f.readlines()
        f.close()

        a = []

        r = []
        rec = {} 
        for l in c:
            l = l.replace('\n', '')
            if self.convert2utf8:
                l = l.decode('iso-8859-1').encode('utf-8')
            if '!ID ' in l:
                if len(rec) > 0:
                    r.append(rec)
                rec = {}
                
            else:

                tag = str(int(l[2:5]))
                field = l[6:]
                if '^' in l:
                    s_content = {} 
                    if field.find('^') > 0:
                        s_content['_'] = field[0:field.find('^')]
                    subfields = field.split('^')
                    for s in subfields:
                        if len(s) > 0:
                            s_content[s[0:1]] = s[1:]
                    content = s_content
                else:
                    content = field
                if tag in rec.keys():
                    
                    rec[tag] = self.add_content(content, rec[tag])
                else:      
                    rec[tag] = content
            
        if len(rec) > 0:
            r.append(rec)
        return r
        

    def add_content(self, data, rec):

        if type(rec) == type('') or  type(rec)==type({}):
            r = rec
            v = []
            v.append(rec)
            v.append(data)

        elif type(rec) == type([]):
            rec.append(data)
            v = rec
        return v
                    
        
    