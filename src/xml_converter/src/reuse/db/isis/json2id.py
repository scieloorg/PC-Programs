# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime




class JSON2IDFile:
    """
    Class which creates an ID file from JSON (ISIS) document
    """
    def __init__(self, converter_utf8_iso, convert2iso=True):
        """
        Arguments: 
        converter_utf8_iso -- converter utf8 to iso
        convert2iso   -- True or False
        """
        self.converter_utf8_iso = converter_utf8_iso
        self.convert2iso = convert2iso
        

    def set_file_data(self, filename, report):
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
            ##print(fields_info.keys())
            tag_list = [ int(tag) for tag in fields_info.keys() if tag.isdigit()]
            

            tag_list.sort()
            ##print(tag_list)
            for t in tag_list:
                
                tag = str(t)
                field_occs = fields_info[tag]
                if type(field_occs) == type([]):
                    for field_occ in field_occs:
                        self.__format_field_occ__(tag, field_occ)
                else:
                    self.__format_field_occ__(tag, field_occs)            
        
    def __format_field_occ__(self, t, field_occ):
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
                        s = self.__convert_value__(subf_occ)
                        s = self.__format_subfield__(subf_label, s, '')
                        s = self.__tag_it__(t, s)
                        self.__write__(s)
                else:
                    # campo com varios subcampos
                    s = self.__convert_value__(subf_occs)
                    tagged = self.__format_subfield__(subf_label, s, tagged)
            if len(tagged)>0:
                s = self.__tag_it__(t, tagged)
                self.__write__(s)
        else:
            if type(field_occ) == type([]):  
                for tagged in field_occ:
                    self.__format_field_occ__(t, tagged)
            else:    
                if type(field_occ) == type(''):
                    s = self.__convert_value__(field_occ)
                    s = self.__tag_it__(t, s)
                    self.__write__(s)
        
    def __format_subfield__(self, subf_label, subf_content, content):
        if subf_label == '_':
            content = subf_content + content
        else:
            content += '^' + subf_label + subf_content
            
        return content
        
    def __tag_it__(self, tag, content):
        tag = '000' + tag
        r = ''
        if tag[-3:].isdigit():
            r = '!v' + tag[-3:] + '!' + content.replace('\n', ' ') + "\n"
        return r
            
           
    def __convert_value__(self, value):
        value = value.replace('\n', ' ')
        if self.convert2iso:
            r = self._iso(value)
        else:
            r = value
        r = r.replace('& ', '&amp; ')
        return r

    def _iso(self, content):
        if type(content) is unicode:
            try:
                iso = content.encode('iso-8859-1', 'replace')
            except:
                try:
                    iso = content.encode('iso-8859-1', 'xmlcharrefreplace')
                except:
                    iso = content.encode('iso-8859-1', 'ignore')
        else:
            iso = content
        return iso
                        
    def __write__(self, content):
        f = open(self.filename, 'a+')
        try:
            f.write(content)
        except:
            self.report.write('Unable to write content in id filename. ', True, True, True,  content )
            
        f.close()
    
