class Journal:
    def __init__(self):
        s = ['title', 'medline', 'iso', 'abbrev', ]
        self.titles = {}
        for k in s:
           self.titles[k] = '' 
        self.parallel_titles = ''
        self.issn = ''
        self.publisher = ''
        
        
    def get_title(self, type=''):
        t = ''
        if type=='':
            type = 'title'
        if type in self.titles.keys():
            t = self.titles[type]
        return t
        
    def set_title(self, v, type=''):
        if type=='':
            type = 'title'
        if type in self.titles.keys():
            self.titles[type] = v 
    
    def get_parallel_titles(self):
        return self.parallel_titles
        
    def set_parallel_titles(self, v):
        self.parallel_titles = v
        
    def get_issn(self):
        return self.issn
        
    def set_issn(self, v):
        self.issn = v
        
    def get_publisher(self):
        return self.publisher
        
    def set_publisher(self, v):
        self.publisher = v
        
        
    	