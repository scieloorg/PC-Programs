
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
        

    def write(self, message, is_summary, is_error, display_on_screen = False, error_data = None):
        
        if is_error:
            self.log_error(message, error_data)
            
        if is_summary:
            self.log_summary( message)
            
        self.log_event(message, display_on_screen)
        

    def log_summary(self, content):
        self.__write__(self.summary_filename, content)

    def log_error(self, error_msg, data = None, display_on_screen = False):
        if display_on_screen:
            
            print(' ! ERROR: ' + error_msg)
            if data != None:
                print(data)
            
            
        if data != None:
            
            try:
                self.__write_err__(error_msg + ': '+ str(data))
                self.__write_all__(error_msg + ': '+ str(data), 'ERROR')
            except: 
                self.__write_err__(error_msg + ': UNABLE TO PRINT DATA**')
                self.__write_all__(error_msg + ': UNABLE TO PRINT DATA**', 'ERROR')
        else:
            self.__write_err__(error_msg)
            self.__write_all__(error_msg, 'ERROR')
            
        
    def log_event(self, event, display_output = False):
        self.__write_all__(event, 'EVENT')
        if self.display_output == True or display_output == True:
            
            print(event)
            print('')

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
        
    def __write_all__(self, content, msg_type):
        content = self.what_time() + '|' + msg_type + '|' + content.replace("\n", '_BREAK_')
        self.__write__(self.log_filename, content)
    
    def __write_err__(self, content):
        content = self.what_time() + '|' + content.replace("\n", '_BREAK_')
        self.__write__(self.err_filename, content)
        

        

    def debugging(self, data, label, level=0):
        doit = False
        
        
        if self.debug_depth >= level: 
            doit = True
        
        if doit:
            if self.display_output == True:
                print("\n"  + '[DEBUG]')
                print(label)
                print(data)
                print('[/DEBUG]' )
            try:
                self.__write_all__(label + "\n" + str(data), 'DEBUG')
            except:
                self.__write_all__(label + "\n" + "UNABLE TO PRINT DATA", 'DEBUG')
            
    def display_data(self, label, data = '' ):
        try:
            self.__write_all__(label + ":" + str(data), 'DISPLAY_DATA')
            
        except:
            self.__write_all__(label + ": UNABLE TO PRINT DATA" , 'DISPLAY_DATA')
            
        if self.display_output == True:
            print('[DISPLAY_DATA]')
            print(label + ':') 
            try: 
                print(data)
            except:
                print('unabled to print data')
            print('[/DISPLAY_DATA]')
            
     
