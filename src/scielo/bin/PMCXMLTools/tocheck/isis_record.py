

class ISISRecord:

    def __init__(self):
        pass
        
    def build_subf(self, value, subf = ''):
        r = ''
        if subf != '*':
            r = '^' + subf
        return  r + value
        
    def build_tag(self, tag, value):
        r = ''
        if value != '':
            r = '!v' + tag + '!' + value + "\n" 
        return r
    
    def build_tag_with_subf(self, tag, list_of_tuples_subf_value):
        r = ''
        for l in list_of_tuples_subf_value:
            r = r + self.build_subf(l[0], l[1])
        return self.build_tag(tag, r)    

    def build_content_with_subf(self, tag, list_of_tuples_subf_value):
        r = ''
        for l in list_of_tuples_subf_value:
            r = r + self.build_subf(l[0], l[1])
        return r    
        
    def build_record(self, list_of_tuples_tag_value):
        r = ''
        for l in list_of_tuples_tag_value:
            
                
            if len(l[1])>0:
                test = '' 
                for c in l[1]:
                    test = test + c
                
                if test == l[1]:
                    # is string
                    r = r + self.build_tag(l[0], l[1])
                else:
                    for item in l[1]:
                        r = r + self.build_tag(l[0], item)
        return r 
        