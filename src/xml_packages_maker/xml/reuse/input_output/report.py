
from datetime import datetime
import os

class Report:

    def __init__(self, log_filename, err_filename, summary_filename, debug_depth = 0, display_output = False):
        self.debug_depth = debug_depth
        self.summary_filename = summary_filename
        self.display_output = display_output
        self.log_filename = log_filename
        if not self.garante_filename_path(log_filename, True):
            print('ERROR: there is no path for ' + log_filename)
        self.err_filename = err_filename
        if not self.garante_filename_path(err_filename, True):
            print('ERROR: there is no path for ' + err_filename)
        if not self.garante_filename_path(summary_filename, True):
            print('ERROR: there is no path for ' + summary_filename)
        

    def write(self, message, is_summary = False, is_error = False, display_on_screen = False, data = None):
        msg_type = 'INFO'
        if is_error:
            self.__write_error__(message, data)
            if 'ERROR' in message.upper():
                msg_type = 'ERROR'
            elif 'WARNING' in message.upper():
                msg_type = 'WARNING'
            else:
                msg_type = 'WARNING'

        if is_summary:
            self.__write_summary__(message)
            
        self.__write_event__(message, msg_type, data)

        if display_on_screen:
            print(message)
            if data != None:
                print(data)

    def __write_summary__(self, message, data = None):
        self.__write__(self.summary_filename, message)
        if data != None:
            try:
                self.__write__(self.summary_filename, str(data))
            except: 
                self.__write__(self.summary_filename, 'UNABLE TO CONVERT DATA TO STR')

    def __write_error__(self, message, data = None):
        self.__write__(self.err_filename, message)
        if data != None:
            try:
                self.__write__(self.err_filename, str(data))
            except: 
                self.__write__(self.err_filename, 'UNABLE TO CONVERT DATA TO STR')
    
    def __write_event__(self, message, msg_type, data = None):
        message = self.what_time() + '|' + msg_type + '|' + message.replace("\n", '_BREAK_')
        self.__write__(self.log_filename, message)
        if data != None:
            try:
                self.__write__(self.log_filename, str(data))
            except: 
                self.__write__(self.log_filename, 'UNABLE TO CONVERT DATA TO STR')
    

    
    def read(self, filename):
        f = open(filename, 'r')
        c = f.read()
        f.close()
        return c

    
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
    
    def __write__(self, filename, content):
        f = open(filename, 'a+')
        f.write(content + "\n")
        f.close()   
    
    def what_time(self):
        return datetime.now().isoformat() 
        
    

    
