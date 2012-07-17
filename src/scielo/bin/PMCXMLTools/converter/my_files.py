import os
#import sys

class MyFiles:
    def __init__(self):
        pass
    
    def garante_path(self, path):
        r = os.path.exists(path)
        if not r:
            os.makedirs(path)
            r = os.path.exists(path)
        return r
            
    def garante_filename_path(self, filename, delete):
        r = os.path.exists(filename)
        if not r:
            if filename.rfind('/')>0:
                path = filename[0:filename.rfind('/')]
                r = os.path.exists(path)
                if not r:
                    print('Created ' +  path)
                    os.mkdir(path)
                    r = os.path.exists(path)
            else:
                r = True
        if delete:
            self.delete_filename(filename)    
        return r
            
    def delete_filename(self, filename):
        if os.path.isfile(filename):
            try:
            	os.remove(filename)
            except:
                print('Unable to delete ' + filename)
        return (not os.path.isfile(filename))
            
    def clean_directory(self, path):
        r = False
        if os.path.exists(path):
            try:
            	files = os.listdir(path)
            	for f in files:
            	    self.delete_filename(path + '/' + f)
            	
            except:
                print('Unable to clean ' + path)
            r = (len(os.listdir(path)) == 0)
        return r
            
                   