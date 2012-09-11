import os

class XMLFoldersSet:

    def __init__(self, serial_path, server_serial_path, img_path, pdf_path, xml_path, scilista):
        self.serial_path = serial_path 

        self.server_serial_path = server_serial_path  
        self.pdf_path = pdf_path 
        self.img_path = img_path 
        self.xml_path = xml_path 
        self.scilista = scilista
        
        for f in [self.serial_path, self.server_serial_path, self.pdf_path, self.img_path, self.xml_path]:
            if not os.path.exists(f):
                os.makedirs(f)
        
        
    
    def add_to_scilista(self, journal_acron, issue_label):
        c = []
        if os.path.exists(self.scilista):
            f = open(self.scilista, 'r')
            c = f.read().split('\n')
            f.close()

        if not journal_acron + ' ' + issue_label in c:
            f = open(self.scilista, 'a+')
            f.write(journal_acron + ' ' + issue_label + '\n')
            f.close()
