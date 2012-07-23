import os
import sys
from datetime import datetime

class JSON2IDFile:
    """
    Class which creates an ID file from JSON (ISIS) document
    """
    def __init__(self, filename, report):
        """
        Arguments: 
        filename -- path and file name for ID file
        report   -- object Report
        """
        self.filename = filename
        self.report = report
        
    def format_and_save_document_data(self, records_order, json_data, db_name):
        """
        Arguments: 
        records_order -- list of dictionary keys of json data that are related to each record
        json_data   -- data in json format
        """
        list = []
        
        rec_content =  ''
        record_number = 0
        
        f = open(self.filename, 'w')
        f.close()
        
        total = 0
        for record_name in records_order:
            try:
                total += len(json_data[record_name])
            except:
                total += 1

        for record_name in records_order:
            record_index = 0
            try:
                data = json_data[record_name]
            except:
                data = None 
            
            
            if type([]) == type(data):
                # is a list of record of same type
                for rec_occ in data:
                    record_index += 1
                    record_number = self.save_record_data(record_name, record_number, record_index, len(data), total)
                    self.save_file_data(db_name)
                    self.save_document_data(rec_occ)
            else:
                # is one occurence of a type of record
                record_index += 1
                record_number = self.save_record_data(record_name, record_number, record_index, 1, total)
                self.save_file_data(db_name)
                self.save_document_data(data)
     
    def save_file_data(self, db_name, center_code = 'br1.1'):
        f = self.filename.replace('.id', '.xml')
        r = self.tag_it('2', f[f.rfind('/')+1:])
        r += self.tag_it('702', f)
        r += self.tag_it('4', db_name)
        r += self.tag_it('1', center_code)
        
        self.__write__(r)
                
    def save_record_data(self, record_name, record_number, record_index, total_of_record_type, total_of_records ):
        record_number += 1
        record_id = '000000' + str(record_number)
        record_id = record_id[-6:]
        self.__write__('!ID ' + record_id + "\n")
        
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
        return record_number
    
    def save_document_data(self, fields_info):
        if fields_info != None:
            for tag, field_occs in fields_info.items():
                t = '000' + tag
                if type(field_occs) == type([]):
                    for field_occ in field_occs:
                        self.format_field_occ(t, field_occ)
                else:
                    self.format_field_occ(t, field_occs)            
        
    def format_field_occ(self, t, field_occ):
        """
        field_occ -- str (string) or [] (repetitive field (with/without subf) or {} (field with subfields)
        """ 
        if type(field_occ) == type({}):
            tagged = ''
            for subf_label, subf_occs in field_occ.items():
                # subf_content = str or []
                if type(subf_occs) == type([]):
                    for subf_occ in subf_occs:
                        self.__write__(self.tag_it(t[-3:], self.format_subfield(t, subf_label, self._convert_value_(subf_occ), '')))
                else:
                    tagged = self.format_subfield(t, subf_label, self._convert_value_(subf_occs), tagged)
            if len(tagged)>0:
                self.__write__(self.tag_it(t[-3:], tagged))
        else:
            if type(field_occ) == type([]):  
                for tagged in field_occ:
                    self.format_field_occ(t, tagged)
            else:    
                if type(field_occ) == type(''):
                    self.__write__(self.tag_it(t[-3:], self._convert_value_(field_occ)))
        
    def format_subfield(self, t, subf_label, subf_content, content):
        if subf_label == '_':
            content = subf_content + content
        else:
            content += '^' + subf_label + subf_content
        return content
        
    def tag_it(self, tag, content):
        return '!v' + tag[-3:] + '!' + content + "\n"
            
           
    def _convert_value_(self, value):
        if value != '':
            try:
                value = value.encode('iso-8859-1')
            except:
                
                v = ''
                for c in value:
                    try:
                        v += c.encode('iso-8859-1')
                    except:
                        v += '&#' + str(hex(ord(c))) + ';' 
                value = v
        return value
 
    def __write__(self, content):
        f = open(self.filename, 'a+')
        try:
            f.write(content)
        except:
            self.report.log_error('Unable to write content in id filename. ',  content )
            
        f.close()
