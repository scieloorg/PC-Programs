from xml_manager import XMLManager
from xml2json_table import XML2JSONTable


class XML2JSONConverter:

    def __init__(self, xml2json_table_filename, report):
        self.conversion_table = XML2JSONTable(xml2json_table_filename, report)
        self.report = report
        
        
    
    def convert(self, xml_filename):
        xml_manager = XMLManager(xml_filename, self.report)
        tagged = {}
        for rec_name, record  in self.conversion_table.records.items():
            tagged[rec_name] = self._convert_record_(xml_manager, record, self.conversion_table.index[rec_name], rec_name)
            
        return tagged   
    
    def _convert_record_(self, xml_manager, record_tags, parent_elem, rec_name):
        record_occurrences = []
        occ = 0
        if parent_elem == '':
            parent_nodes = [None]
        else:
            parent_nodes = xml_manager.return_nodes(parent_elem)
        for parent_node in parent_nodes:
            # para cada .//ref ou para o documento todo
            occ += 1
            record_content = {}
            self.report.debugging(rec_name + ' ' + str(occ), 'XML2JSONConverter._convert_record_: rec and index ', 2)
            for tag, subfs in record_tags.items():
                subf_xpath = {}
                result = {}
                for subf, subf_info in subfs.subfs.items():
                    subf_xpath[subf] = (subf_info['elem'], subf_info['attr'], subf_info['default'])
                record_content[tag] = xml_manager.return_multi_values(result, subfs.group, subf_info['xpath'], subf_xpath, parent_node)
            self.report.debugging(record_content, 'XML2JSONConverter._convert_record_: record_content ', 2)
            record_occurrences.append(record_content)
        return record_occurrences
        
   
    
                   
    
