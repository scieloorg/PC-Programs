from xml_manager import XMLManager
from conversion_table import ConversionTable


class Converter:

    def __init__(self, xml_filename):
        self.conversion_table = ConversionTable('xpath2isis.txt')
        self.xml_manager = XMLManager(xml_filename, 2)
        
    def load(self):
        records = self.conversion_table.format_records(self.xml_manager)
        for type, r in records.items():
            print(type)
            print(r)

    
        
        
filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml.local.xml'

converter = Converter(filename)
converter.load()
