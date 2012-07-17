from xml_manager import XMLManager
from xml2json_table import XML2JSONTable


class XML2JSONConverter:

    def __init__(self, xml2json_table_filename, report):
        self.conversion_table = XML2JSONTable(xml2json_table_filename, report)
        self.report = report
        
        
    
    def convert(self, xml_filename):
        xml_manager = XMLManager(xml_filename, self.report)
        converted = {}
        for level_one_label, level_two_labels  in self.conversion_table.level1.items():
            converted[level_one_label] = self._convert_label1_(xml_manager, level_two_labels, self.conversion_table.xpath_for_level1[level_one_label], level_one_label)
        self.report.display_data('converted', converted)    
        return converted   
    
    def _convert_label1_(self, xml_manager, level_two_labels, xpath_for_level1, level_one_label):
        level1_occurences = []
        occ = 0
        if xpath_for_level1 == '':
            parent_nodes = [None]
        else:
            parent_nodes = xml_manager.return_nodes('.//' + xpath_for_level1)
        for parent_node in parent_nodes:
            # para cada .//ref ou para o documento todo
            occ += 1
            level1_content = {}
            self.report.debugging(level_one_label + ' ' + str(occ), 'XML2JSONConverter._convert_label1_: level1 and occ ', 2)
            
            for level2_label, level2_info in level_two_labels.items():
                level3_data = []
                for level3_label, level3_info in level2_info.level3_data.items():
                    level3_data.append( (level3_info['xpath_parent_elem'], level3_label, level3_info['xpath_elem'] , level3_info['xpath_attr'], level3_info['default_value'] ) )
                result = {}
                
                label2_content = xml_manager.return_multi_values(result, level2_info.xpath_start, level3_data, parent_node)
                if label2_content != []:
                    if level2_info.level2_rename != '':
                        if level2_info.level2_rename in level1_content.keys():
                            for label2_content_occ in label2_content:
                                level1_content[level2_info.level2_rename].append(label2_content_occ)
                    else:
                        level1_content[level2_label] = label2_content
                
            self.report.debugging(level1_content, 'XML2JSONConverter._convert_label1_: level1_content ', 2)
            level1_occurences.append(level1_content)
            
            
            
        return level1_occurences
        
   
    
     
    
