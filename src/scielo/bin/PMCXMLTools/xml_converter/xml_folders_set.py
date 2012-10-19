import os

class XMLFoldersSet:

    def __init__(self, archive_serial_path, processing_serial_path, web_img_path, web_pdf_path, web_xml_path, scilista):
        self.archive_serial_path = archive_serial_path 

        self.processing_serial_path = processing_serial_path  
        self.web_pdf_path = web_pdf_path 
        self.web_img_path = web_img_path 
        self.web_xml_path = web_xml_path 
        self.scilista = scilista
        self.id_folder = processing_serial_path + '/i'
        for f in [self.id_folder, self.archive_serial_path, self.processing_serial_path, self.web_pdf_path, self.web_img_path, self.web_xml_path]:
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
