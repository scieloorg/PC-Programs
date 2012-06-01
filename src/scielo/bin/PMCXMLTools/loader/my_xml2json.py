from xml_manager import XMLManager
from conversion_table import ConversionTable


class MyXML2JSON:

    def __init__(self, xml_filename):
        self.conversion_table = ConversionTable('xml2json.txt')
        self.xml_manager = XMLManager(xml_filename, 0)
        
    
    def convert(self):
        tagged = {}
        for rec_name, record  in self.conversion_table.records.items():
            tagged[rec_name] = self.convert_record(record, self.conversion_table.index[rec_name], rec_name)
            print('-------------------')
            print(rec_name)
            print(tagged[rec_name])
        return tagged   
    
    def convert_record(self, record_tags, parent_elem, rec_name):
        record_occurrences = []
        occ = 0
        if parent_elem == '':
            parent_nodes = [None]
        else:
            parent_nodes = self.xml_manager.return_nodes(parent_elem)
        for parent_node in parent_nodes:
            # para cada .//ref ou para o documento todo
            occ += 1
            record_content = {}
            print(rec_name + ' ' + str(occ))
            for tag, subfs in record_tags.items():
                subf_xpath = {}
                for subf, subf_info in subfs.items():
                    subf_xpath[subf] = (subf_info['elem'], subf_info['attr'], subf_info['default'])
                record_content[tag] = self.xml_manager.return_multi_values(subf_info['xpath'], subf_xpath, parent_node)
            print(record_content)
            record_occurrences.append(record_content)
        return record_occurrences
        
   
    
                   
    
