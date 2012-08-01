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
        if os.path.exists(filename):
            r = True
        else:
            path = os.path.dirname(filename)
            if not os.path.exists(path):
                os.makedirs(path)
            r = os.path.exists(path)
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
            
                   