from xml2json_converter import XML2JSONConverter
from report import Report

class IDFile:

    def __init__(self, filename, report):
        self.filename = filename
        f = open(filename, 'w')
        f.close()
        self.report = report
        
    def write(self, content, context):
        f = open(self.filename, 'a+')
        try:
            f.write(content)
        except:
            try:
                self.report.register('ERROR:' + content + '('+ context + ')', 'Unable to write id filename')
            except:
                pass
        f.close()

class PMCXML2ISIS:

    def __init__(self, records_order, xml2json_table_filename = 'pmcxml2isis.txt'):
       self.xml2json_table_filename = xml2json_table_filename
       self.records_order = records_order
       self.tables = {}
       self.record_number = 0
       
       
    def convert(self, xml_filename, supplementary_xml_filename, id_filename, report_filename, debug):
        self.report = Report(report_filename, debug)
        self.id_file = IDFile(id_filename, debug)
        
        xml2json_converter = XML2JSONConverter(self.xml2json_table_filename, self.report)
        main_json = xml2json_converter.convert(xml_filename)
        
        suppl_json =  {}
        if supplementary_xml_filename != '':
            suppl_json = xml2json_converter.convert(supplementary_xml_filename)
        
        r = self.format_records(main_json, suppl_json)
        
        #self.report.register(r)
        
        
        
    def format_records(self, main_json, suppl_json):
        rec_content =  ''
        
        for record_name in self.records_order:
            for rec_occ in main_json[record_name]:
                
                self.record_number += 1
                record_id = '000000' + str(self.record_number)
                record_id = record_id[-6:]
            
                rec_content += '!ID ' + record_id + "\n"
                self.id_file.write('!ID ' + record_id + "\n", '')
                for tag, tag_occs in rec_occ.items():
                    t = '000' + tag
                    if tag_occs != None:
                        for tag_occ in tag_occs:
                            tagged = '' 
                            for subf_name, subf_content in tag_occ.items():
                                if subf_name == 'value': 
                                    tagged = subf_content + tagged
                                else:
                                    #print(subf_content)
                                    tagged += '^' + subf_name + self._convert_subfields_(subf_content, '') #FIXME
                        
                            rec_content += '!v' + t[-3:] + '!' + tagged + "\n"
                            self.id_file.write('!v' + t[-3:] + '!' + tagged + "\n", ''  )
        return rec_content
                    
    def _convert_subfields_(self, value, data_conversion):
        if value != '':
            try:
                value = value.encode('iso-8859-1')
            except:
                self.report.register('encode failure', 'Unable to convert to iso') 
        if value != '' and data_conversion != '':
            v = ''
            try:
                t = self.tables[data_conversion]
                try:
                    v = self.tables[data_conversion][value]
                except:
                    self.report.register('Expected data_conversion of ' + data_conversion + ': ' + value, '')
            except:
                self.report.register('Expected table ' + data_conversion, '') 
            if v != '':
                value = v                    
        return value

    def _convert_value_(self, value, data_conversion):
        if value != '':
            try:
                value = value.encode('iso-8859-1')
            except:
                self.report.register('encode failure', 'Unable to convert to iso') 
        if value != '' and data_conversion != '':
            v = ''
            try:
                t = self.tables[data_conversion]
                try:
                    v = self.tables[data_conversion][value]
                except:
                    self.report.register('Expected data_conversion of ' + data_conversion + ': ' + value, '')
            except:
                self.report.register('Expected table ' + data_conversion, '') 
            if v != '':
                value = v                    
        return value

    def old_convert_value_(self, value, data_conversion):
        if value != '':
            try:
                value = value.encode('iso-8859-1')
            except:
                self.report.register('encode failure', 'Unable to convert to iso') 
        if value != '' and data_conversion != '':
            v = ''
            try:
                t = self.tables[data_conversion]
                try:
                    v = self.tables[data_conversion][value]
                except:
                    self.report.register('Expected data_conversion of ' + data_conversion + ': ' + value, '')
            except:
                self.report.register('Expected table ' + data_conversion, '') 
            if v != '':
                value = v                    
        return value
                   
    
filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml.local.xml'
suppl_filename = ''
id_filename = 'v49n1.id'

log_filename = 'v49n1.log'
debug = 0

converter = PMCXML2ISIS('hr')
converter.convert(filename, suppl_filename, id_filename, log_filename, debug)
