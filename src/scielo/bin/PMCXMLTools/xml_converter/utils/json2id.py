# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime


class JSON2IDFile:
    """
    Class which creates an ID file from JSON (ISIS) document
    """
    def __init__(self, filename, report, convert2iso=True):
        """
        Arguments: 
        filename -- path and file name for ID file
        report   -- object Report
        """
        self.convert2iso = convert2iso
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
            #print(fields_info.keys())
            tag_list = [ int(tag) for tag in fields_info.keys() if tag.isdigit()]
            

            tag_list.sort()
            #print(tag_list)
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
        return '!v' + tag[-3:] + '!' + content + "\n"
            
           
    def __convert_value__(self, value):
        #print(value)
        if value != '':
            if self.convert2iso:
                value = self.utf8_2_iso(value)
        return value

    def __convert_chr__(self, value):
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
            self.report.write('Unable to write content in id filename. ', True, True, True,  content )
            
        f.close()
    def utf8_2_iso(self, utf8):
        utf8 = utf8.replace('\ufeff','')
        
        try:
            print('try 1')
            b = utf8.encode('iso-8859-1')
            iso = b.decode('iso-8859-1')
        except:
            print('except 1')

            if ' ' in utf8:
                words = utf8.split(' ')
                sep = ' '
            else:
                words = utf8 
                sep = ''
            new = []
            for w in words:
                if len(w)==1:
                    print('char')
                    try: 
                        print('try ord')
                        n = ord(w)
                        i = w 
                    except:
                        print('except ord')
                        try:
                            print('try num ent')
                            n = 256*ord(w[0]) + ord(w[1])

                            i = '&#' + str(hex(n)) + ';'
                        except:
                            print('except num ent')
                            i = '?'
                else:
                    print('word')
                    i = self.utf8_2_iso(w)
                
                    
                new.append(i)
            iso = sep.join(new)
        
        
        return iso