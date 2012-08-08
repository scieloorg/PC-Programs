
class Parameters:
    def __init__(self, parameter_list):
        self.params = parameter_list
        
    def check_parameters(self, sys_argv):
        
        if len(sys_argv) == len(self.params):
            r = True
            i = 0
            for param in self.params:
                
                if i > 0:
                    print('Parameter ' + str(i) +': ' +  param)
                    
                    if len(sys_argv) > i:
                        print(sys_argv[i])
                i += 1
        else:
            r = False
            print('Usage:')
            i = 0
            for param in self.params:
                
                if i > 0:
                    print('Parameter ' + str(i) +': ' +  param)
                    
                    if len(sys_argv) > i:
                        print(sys_argv[i])
                i += 1
            
        return r
