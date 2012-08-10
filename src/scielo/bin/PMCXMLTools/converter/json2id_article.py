import os
import sys

from datetime import datetime
from utils.json2id import JSON2IDFile


class JSON2IDFile_Article(JSON2IDFile):
    """
    Class which creates an ID file from JSON (ISIS) document
    """
    def __init__(self, filename, report):
        """
        Arguments: 
        filename -- path and file name for ID file
        report   -- object Report
        """
        JSON2IDFile.__init__(self, filename, report)
        
    def format_and_save_document_data(self, json_data, records_order, db_name):
        """
        Arguments: 
        records_order -- list of dictionary keys of json data that are related to each record
        json_data   -- data in json format
        """
        
        rec_content =  ''
        record_number = 0
        
        f = open(self.filename, 'w')
        f.close()
        
        total = 0
        for record_name in records_order:
            if record_name in json_data.keys():
                total += len(json_data[record_name])
            
        for record_name in records_order:
            record_index = 0
            if record_name in json_data.keys():
                data = json_data[record_name]
            else:
                data = None
            
            if data == None:
                record_index += 1
                record_number += 1
                self.save_record_number(record_number)
                self.save_record_data(record_name, record_number, record_index, 1, total)
                self.save_file_data(db_name)
                #self.save_document_data(data)
            else:
                if type([]) == type(data):
                    # is a list of record of same type
                    for rec_occ in data:
                        record_index += 1
                        record_number += 1
                        self.save_record_number(record_number)
                        self.save_record_data(record_name, record_number, record_index, len(data), total)
                        self.save_file_data(db_name)
                        self.save_document_data(rec_occ)
                    
                else:
                    if type({}) == type(data):
                        # is one occurence of a type of record
                        record_index += 1
                        record_number += 1
                        self.save_record_number(record_number)
                        self.save_record_data(record_name, record_number, record_index, 1, total)
                        self.save_file_data(db_name)
                        self.save_document_data(data)
                
    
     
    def save_file_data(self, db_name):
        f = self.filename.replace('.id', '.xml')
        r = self.tag_it('2', os.path.basename(f))
        r += self.tag_it('702', f)
        r += self.tag_it('4', db_name)
        #r += self.tag_it('1', center_code)
        
        self.__write__(r)
                
    def save_record_data(self, record_name, record_number, record_index, total_of_record_type, total_of_records ):
        record_data = ''
        record_data += self.tag_it('700', str(record_number))
        record_data += self.tag_it('701', str(record_index))
        record_data += self.tag_it('705', 'S')
        record_data += self.tag_it('706', record_name)
        record_data += self.tag_it('708', str(total_of_record_type))

        if record_name == 'o':
            record_data += self.tag_it('91', datetime.now().isoformat()[0:10].replace('-', ''))
            record_data += self.tag_it('92', datetime.now().isoformat()[11:19].replace(':',''))
            record_data += self.tag_it('703', str(total_of_records))
        

        self.__write__(record_data)
        
    
    
