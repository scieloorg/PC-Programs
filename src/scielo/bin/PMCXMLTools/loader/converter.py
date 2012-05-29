from xml_manager import XMLManager
from conversion_table import ConversionTable


class Converter:

    def __init__(self, xml_filename):
        self.conversion_table = ConversionTable('xpath2isis.txt')
        self.xml_manager = XMLManager(xml_filename)
        
    def load(self):
        order = 'ohflpc'
        tagged = {}
        records = self.conversion_table.get_records_structure()
        for rec_type, rec_tags in records.items():
            tagged[rec_type] = self.format_record(rec_tags)
        print(tagged)    
        
    def format_record(self, tags):
        record_content = ''
        for tag, subfs in tags.items():
            r = ''
            print(tag)
            print(subfs)
            for subf, xpath in subfs.items():
                value = self.xml_manager.get_values(xpath)
                if subf == '*':
                    r = value
                else:
                    r = r + '^' + subf + value
            record_content = record_content + self.tag_it(tag, r)
        return record_content        
     
    def tag_it(self, tag, value):
        field_tag = '00' + tag
        field_tag = field_tag[-3:]
        r = ''
        if value != '':
            r = '!v' + field_tag + '!' + value + "\r\n"
        return r
        
        
filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml.local.xml'

converter = Converter(filename)
converter.load()
