import os
import sys

class IDFile2ISIS:
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
        
    def id2mst(self, id_filename, mst_filename):
        self.id2i(id_filename, mst_filename + '.tmp')
        self.append(mst_filename + '.tmp', mst_filename)

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

    def __init__(self, id_filename):
        self.id_filename = id_filename

    def id2json(self):
        f = open(self.id_filename, 'r')
        c = f.readlines()
        f.close()

        a = []

        r = []
        rec = {} 
        for l in c:
            l = l.replace('\n', '')

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
                    
        
    