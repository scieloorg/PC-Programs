from xml_manager import XMLManager
from xml2json_table import XML2JSONTable


class XML2JSONConverter:

    def __init__(self, xml2json_table_filename, report):
        self.conversion_table = XML2JSONTable(xml2json_table_filename, report)
        self.report = report
        
        
    
    def convert(self, xml_filename):
        xml_manager = XMLManager(xml_filename, self.report)
        tagged = {}
        for rec_name, record_tags  in self.conversion_table.records.items():
            tagged[rec_name] = self._convert_record_(xml_manager, record_tags, self.conversion_table.grouped_by[rec_name], rec_name)
        self.report.display_data('converted', tagged)    
        return tagged   
    
    def _convert_record_(self, xml_manager, record_tags, grouped_by, rec_name):
        record_occurrences = []
        occ = 0
        if grouped_by == '':
            parent_nodes = [None]
        else:
            parent_nodes = xml_manager.return_nodes('.//' + grouped_by)
        for parent_node in parent_nodes:
            # para cada .//ref ou para o documento todo
            occ += 1
            record_content = {}
            self.report.debugging(rec_name + ' ' + str(occ), 'XML2JSONConverter._convert_record_: rec and index ', 2)
            
            for tag, tag_info in record_tags.items():
                subfs = []
                for subf_name, subf_info in tag_info.subfs.items():
                    subfs.append( (subf_info['parent_elem'], subf_name, subf_info['elem'] , subf_info['attr'], subf_info['default'] ) )
                result = {}
                
                tag_content = xml_manager.return_multi_values(result, tag_info.start, subfs, parent_node)
                
                if tag_info.retag != '':
                    if tag_info.retag in record_content.keys():
                        for tag_content_occ in tag_content:
                            record_content[tag_info.retag].append(tag_content_occ)
                else:
                    record_content[tag] = tag_content
                
            self.report.debugging(record_content, 'XML2JSONConverter._convert_record_: record_content ', 2)
            record_occurrences.append(record_content)
            
            
            
        return record_occurrences
        
   
    
                   
    
