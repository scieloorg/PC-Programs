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

         
        
        
       
        
    