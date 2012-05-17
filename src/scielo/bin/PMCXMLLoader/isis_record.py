

class ISISRecord:

    def __init__(self):
        pass
        
    def build_subf(self, value, subf = ''):
        r = ''
        if subf != '*':
            r = '^' + subf
        return  r + value
        
    def build_tag(self, tag, value):
        
        return '!v' + tag + '!' + value + "\n" 
    
        