class JournalIssue:
    def __init__(self):
        self.volume = '' 
        self.number = '' 
        self.volume_suppl = '' 
        self.number_suppl = '' 
        self.year_order = '' 
        self.acron = '' 
        self.issue_status = '' 
        self.standard = '' 
        self.descriptor = '' 
        self.markup_done = '' 
        self.dateiso = '' 
        self.document_count = '' 
        self.sections =  {'pt': [], 'en': [], 'es':[], } 
        
        
    def get_volume(self):
        return self.volume
        
    def get_number(self):
        return self.number
        
    
    def get_volume_suppl(self):
        return self.volume_suppl
        
    
    def get_number_suppl(self):
        return self.number_suppl
        
    
    def get_year_order(self):
        return self.year_order
        
    
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
        
    
    
    def get_sections(self, lang):
        return self.sections[lang]
        
    
        
    def set_volume(self, v):
        self.volume = v

    def set_number(self, v):
        self.number = v


    def set_volume_suppl(self, v):
        self.volume_suppl = v


    def set_number_suppl(self, v):
        self.number_supp = v
        
    
    def set_year_order(self, v):
        self.year_order = v
        
    
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



    def set_sections(self, v, lang):
        self.sections[lang] = v


