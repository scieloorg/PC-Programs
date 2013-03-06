import os

class Parameters:
    def __init__(self, required):
        self.required = required
        
    def check_parameters(self, sys_argv):
        
        if len(sys_argv) == len(self.required):
            r = True
            i = 0
            for param in self.required:                
                if i > 0:
                    print('Parameter ' + str(i) +': ' +  param + ' = ' + sys_argv[i])
                i += 1
        else:
            r = False
            print('Usage:')
            i = 0
            for param in self.required:
                if i > 0:
                    print('Parameter ' + str(i) +': ' +  param)
                i += 1
        return r

def get_script_path(script):
    script = script.replace('\\', '/')
    if '..' in script:
        path = os.getcwd().replace('\\', '/') + '/' + os.path.dirname(script)
    elif script.startswith('/') or script[1:2] == ':':
        path = os.path.dirname(script)
    else:
        path = os.getcwd().replace('\\', '/')
    return path