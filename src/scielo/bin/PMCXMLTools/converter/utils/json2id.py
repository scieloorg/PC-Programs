# -*- coding: utf-8 -*-

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
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        
        
    def format_and_save_document_data(self, json_data):
        """
        Arguments: 
        records_order -- list of dictionary keys of json data that are related to each record
        json_data   -- data in json format
        """
        record_number = 0

        f = open(self.filename, 'w')
        f.close()
        
        
        if type([]) == type(json_data):
            # is a list of record of same type
            for rec_occ in json_data:
                record_number += 1
                self.save_record_number(record_number)
                self.save_document_data(rec_occ)
        else:
            if type({}) == type(json_data):            
                record_number += 1
                self.save_record_number(record_number)
                self.save_document_data(json_data)
                
    
                
    def save_record_number(self, record_number):
        record_id = '000000' + str(record_number)
        record_id = record_id[-6:]
        self.__write__('!ID ' + record_id + "\n")
        
    
    
    def save_document_data(self, fields_info):
        if type(fields_info) == type({}):
            for tag, field_occs in fields_info.items():
                if tag.isdigit():
                    if type(field_occs) == type([]):
                        for field_occ in field_occs:
                            self.format_field_occ(tag, field_occ)
                    else:
                        self.format_field_occ(tag, field_occs)            
        
    def format_field_occ(self, t, field_occ):
        """
        field_occ -- str (string) or [] (repetitive field (with/without subf) or {} (field with subfields)
        """ 
        if type(field_occ) == type({}):
            tagged = ''
            for subf_label, subf_occs in field_occ.items():
                # subf_content = str or []
                if type(subf_occs) == type([]):
                    # campo repetitivo 
                    for subf_occ in subf_occs:
                        s = self._convert_value_(subf_occ)
                        s = self.format_subfield(subf_label, s, '')
                        s = self.tag_it(t, s)
                        self.__write__(s)
                else:
                    # campo com varios subcampos
                    s = self._convert_value_(subf_occs)
                    tagged = self.format_subfield(subf_label, s, tagged)
            if len(tagged)>0:
                s = self.tag_it(t, tagged)
                self.__write__(s)
        else:
            if type(field_occ) == type([]):  
                for tagged in field_occ:
                    self.format_field_occ(t, tagged)
            else:    
                if type(field_occ) == type(''):
                    s = self._convert_value_(field_occ)
                    s = self.tag_it(t, s)
                    self.__write__(s)
        
    def format_subfield(self, subf_label, subf_content, content):
        if subf_label == '_':
            content = subf_content + content
        else:
            content += '^' + subf_label + subf_content
            
        return content
        
    def tag_it(self, tag, content):
        tag = '000' + tag
        return '!v' + tag[-3:] + '!' + content + "\n"
            
           
    def _convert_value_(self, value):
        #print(value)
        if value != '':
            try:
                value = value.encode('iso-8859-1')
            except:
                try:
                    value = value.decode('utf-8')
                    value = value.encode('iso-8859-1')
                except:
                
                    value = self.convert_chr(value)
        return value

    def convert_chr(self, value):
        v = ''
        for c in value:
            try:
                v += c.encode('iso-8859-1')
            except:
                try: 
                    n = ord(c)
                    
                except:

                    n = 256*ord(c[0]) + ord(c[1])
                    print(n)

                v += '&#' + str(hex(n)) + ';'
        return v
                     
                        
    def __write__(self, content):
        f = open(self.filename, 'a+')
        try:
            f.write(content)
        except:
            self.report.log_error('Unable to write content in id filename. ',  content )
            
        f.close()
