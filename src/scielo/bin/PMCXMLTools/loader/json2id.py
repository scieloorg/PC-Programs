import os
import sys

class JSON2IDFile:

    def __init__(self, filename, report):
        self.filename = filename
        self.report = report
        
    def format_records_and_save(self, records_order, json_data):
        rec_content =  ''
        record_number = 0
        f = open(self.filename, 'w')
        f.close()
        for record_name in records_order:
            for rec_occ in json_data[record_name]:
                
                record_number += 1
                record_id = '000000' + str(record_number)
                record_id = record_id[-6:]
            
                #rec_content += '!ID ' + record_id + "\n"
                self.__write__('!ID ' + record_id + "\n")
                #rec_content += '!v' + t[-3:] + '!' + tagged + "\n"
                self.__write__('!v706!' + record_name + "\n")
                            
                for tag, tag_occs in rec_occ.items():
                    t = '000' + tag
                    if tag_occs != None:
                        for tag_occ in tag_occs:
                            tagged = '' 
                            for subf_name, subf_content in tag_occ.items():
                                if subf_name == 'value': 
                                    tagged = self._convert_value_(subf_content) + tagged
                                else:
                                    tagged += '^' + subf_name + self._convert_value_(subf_content) #FIXME
                            #rec_content += '!v' + t[-3:] + '!' + tagged + "\n"
                            self.__write__('!v' + t[-3:] + '!' + tagged + "\n")
                            
        return rec_content
                    
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
