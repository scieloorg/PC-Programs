class ExtraData:

    def __init__(self):
        self.acron = '' 
        self.issue_status = '' 
        self.standard = '' 
        self.descriptor = '' 
        self.markup_done = '' 
        self.dateiso = '' 
        self.document_count = '' 
        self.bibstrip = {'pt': '', 'en': '', 'es':'', } 
    def get_acron(self):
        return self.acron
        
    
    def get_issue_status(self):
        return self.issue_status
        
    
    def get_standard(self):
        return self.standard
        
    
    def get_descriptor(self):
        return self.descriptor
        
    
    def get_is_markup_done(self):
        return self.markup_done
        
    
    def get_dateiso(self):
        return self.dateiso
        
    
    def get_document_count(self):
        return self.document_count
        
    
    
    
        
    
    def set_acron(self, v):
        self.acron = v
        
    
    def set_issue_status(self, v):
        self.issue_status = v
        
    
    def set_standard(self, v):
        self.standard = v
        
    
    def set_descriptor(self, v):
        self.descriptor = v
 
    
    def set_is_markup_done(self, v):
        self.markup_done = v
        
    
    def set_dateiso(self, v):
        self.dateiso = v
        
    def set_document_count(self, v):
        self.document_count = v


    def get_bibstrip(self, lang):
        return self.bibstrip[lang]
    def set_bibstrip(self, v, lang):
        
        self.bibstrip[lang] = v
            
    def set_issue_folder_name(self, v):
        self.issue_folder_name = v
    
    def get_issue_folder_name(self):
        return self.issue_folder_name
   
    