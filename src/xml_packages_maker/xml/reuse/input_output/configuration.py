import os

class Configuration:

    def __init__(self, filename = 'configuration.ini'):
        f = open(filename, 'r')
        self.parameters = {}
        for c in f.readlines():
            if '=' in c and not c.startswith('#'):
                c = c.strip('\n').split('=')
                self.parameters[c[0]] = c[1].replace('\\', '/')
                if '_PATH' in c[0] and '/' in self.parameters[c[0]]:
                    paths = self.parameters[c[0]].split(';')
                    for path in paths:
                        if not os.path.exists(path):
                            os.makedirs(path)
        f.close()
    

    
    def parameter(self, name):
        r = ''
        if name in self.parameters.keys():
            r = self.parameters[name]
        return r 
        
    def check(self, config_parameters):
        valid = True
        msg = [] 
        for i in config_parameters:
            if i in self.parameters.keys():
                if len(self.parameters[i]) == 0:
                    msg.append('No value for ' + i)
            else:
                msg.append('Missing ' + i)
                valid = False
        return valid, '\n'.join(msg)
