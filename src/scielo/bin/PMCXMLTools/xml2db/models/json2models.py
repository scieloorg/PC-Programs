# -*- coding: utf-8 -*-


class JSON_Models:
    def __init__(self, json2models):
        self.json2models = json2models
        

    def set_data(json_data, xml_filename, document_report):
        self.json2models.set_data(json_data, xml_filename, document_report)
        

    @property
    def publication_title(self):
        return self.json2models.publication_title
   
    def return_document(self, publication, img_files):
        document, errors, warnings, refcount = self.json2models.return_document(publication, img_files)
        return (document, errors, warnings, refcount)

    def return_publication_item(self, json_data, publication):
        return self.json2model.return_publication_item(publication)

    def return_publications_list(self, json):
        return self.json2models.return_publications_list(json)

    def return_publication_items_list(self, json_publication_items, publication):
        
        return self.json2models.return_publication_items(json_publication_items, publication)
    
    