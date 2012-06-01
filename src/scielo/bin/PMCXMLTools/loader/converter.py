from my_xml2json import MyXML2JSON


class Converter:

    def __init__(self, xml_filename):
       self.xml_filename = xml_filename
       self.data = {}
       self.tables = {}
       
    def load(self):
        my_xml2json = MyXML2JSON(self.xml_filename)
        self.data = my_xml2json.convert()
        
    
    def convert(self):
        #print(self.data)
        pass
                   
    def _convert_value_(self, value, data_conversion):
        if value != '' and data_conversion != '':
            v = ''
            try:
                t = self.tables[data_conversion]
                try:
                    v = self.tables[data_conversion][value]
                except:
                    print('Expected data_conversion of ' + data_conversion + ': ' + value)
            except:
                print('Expected table ' + data_conversion) 
            if v != '':
                value = v                    
        return value
                   
    
filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml.local.xml'

converter = Converter(filename)
converter.load()
converter.convert()
