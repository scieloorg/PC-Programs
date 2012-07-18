from xml2json_converter import XML2JSONConverter
from report import Report

import json

class PMCXML2JSON:

    def __init__(self, xml2json_table_filename = 'pmcxml2json.txt'):
       self.xml2json_table_filename = xml2json_table_filename
       
    def convert(self, xml_filename, report):
        xml2json_converter = XML2JSONConverter(self.xml2json_table_filename, report)
        return xml2json_converter.convert(xml_filename)
   
    def pretty_print(self, json_data):
        j = json.dumps(json_data, sort_keys=True, indent=4)
        print(j)
        
        
if __name__ == '__main__':                   
    filename = '02-05.sgm.xml.local.xml'

    log_filename = 'v49n1.log'
    debug = 0
    report = Report(log_filename, log_filename + '.err', 0, True)
    
    converter = PMCXML2JSON()
    json_data = converter.convert(filename, report)
    converter.pretty_print(json_data)
