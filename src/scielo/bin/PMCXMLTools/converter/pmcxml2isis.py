import os
import sys

from xml2json_converter import XML2JSONConverter
from json2id import JSON2IDFile
from id2isis import IDFile2ISIS

from article import ArticleFixer
from report import Report
from parameters import Parameters
from my_files import MyFiles

my_files = MyFiles()


class PMCXML2ISIS:

    def __init__(self, records_order, id2isis, xml2json_table_filename = '_pmcxml2isis.txt'):
        self.xml2json_table_filename = xml2json_table_filename
        self.records_order = records_order
        self.tables = {}
        self.id2isis = id2isis
       
        f = open('tables', 'r')
        lines = f.readlines()
        f.close()

        for l in lines:
            table_name, key, value = l.replace("\n",'').split('|')
            if len(table_name) > 0:
                if not table_name in self.tables.keys():
                    self.tables[table_name] = {}
            if len(key)>0:
                self.tables[table_name][key] = value


       
    def generate_json(self, xml_filename, supplementary_xml_filename, report):
        xml2json_converter = XML2JSONConverter(self.xml2json_table_filename, report)
        json_data = xml2json_converter.convert(xml_filename)
        
        article = ArticleFixer(json_data, self.tables)
        article.fix_data()
        return article.doc
            
    def generate_id_file(self, json_data, id_filename, report, db_name):
        id_file = JSON2IDFile(id_filename, report)
        id_file.format_and_save_document_data(self.records_order, json_data, db_name)
        
    def generate_db(self, files_set, report):
        cmd = ''
        files_set.prepare()
        id_filename_list = []
        docs = []

        sections = {}

        list = os.listdir(files_set.xml_path)
        for f in list:
            if '.xml' in f:
                print(f)
                xml_filename = files_set.xml_path + '/' + f
                id_filename = f.replace('.xml', '.id')
                
                json_data = self.generate_json(xml_filename, files_set.suppl_filename, report)

                if '49' in json_data['doc']['f']:   
                    section = json_data['doc']['f']['49']
                    if not section in sections.keys():
                        sections[section] = 'SECTION' + str(len(sections))
                    json_data['doc']['f']['49'] = sections[section]
                if not '49' in json_data['doc']['f']: 
                    json_data['doc']['f']['49'] = 'MISSING'
                docs.append((id_filename, json_data))

        for doc in docs:
            id_filename, json_data = doc
            json_data = self.generate_record(json_data, 'f', 'h')
            json_data = self.generate_record(json_data, 'f', 'l')
                
            self.generate_id_file(json_data['doc'], files_set.output_path + '/' + id_filename, report, files_set.db_name)
            self.id2isis.id2mst(files_set.output_path + '/' + id_filename, files_set.db_filename)
    
    def generate_record(self, json_data, src, dest):
        #print(json_data)
        d = json_data['doc'][src]
        json_data['doc'][dest] = self.convert_record(d)
        return json_data
    
    def convert_record(self, json_record):
        return json_record
                
    
            
    def execute(self, xml_path, suppl_filename, output_path, db_name, script_filename, debug_depth, display_on_screen):
        files_set = PMCXML_FilesSet(xml_path, suppl_filename, output_path, db_name)
        report = Report(files_set.log_filename, files_set.err_filename, debug_depth, display_on_screen) 
        self.generate_db(files_set, report)
        

class PMCXML_FilesSet:

    def __init__(self, xml_path, suppl_filename, output_path, db_name):
        self.xml_path = xml_path
        self.output_path = output_path
        self.db_name = db_name
        self.db_filename = output_path + '/' + db_name
        self.suppl_filename = suppl_filename
        self.log_filename = output_path + '/' + db_name + '.log'
        self.err_filename = output_path + '/' + db_name + '.err.log'
        
    
    def prepare(self):
        if os.path.exists(self.output_path):
            files = os.listdir(self.output_path)
            for f in files:
                print('deleting ' + self.output_path + '/' + f + '?')
                ext = f[f.rfind('.'):]
                if ext in ['.id', '.mst', '.xrf', '.log', ]:
                    print('deleting ' + self.output_path + '/' + f)
                    os.remove(self.output_path + '/' + f)
        else:
            os.makedirs(self.output_path)
    
                
if __name__ == '__main__':
    parameter_list = ['', 'path of XML files', 'supplementary XML', 'output path', 'database name (no extension)', 'batch and shell script filename to generate .mst database name (no extension)', 'cisis path', 'debug_depth', 'display messages on screen? yes|no']
    parameters = Parameters(parameter_list)
    if parameters.check_parameters(sys.argv):
    	this_script_name, xml_path, suppl_xml, output_path, db_name, script_filename, cisis_path, debug_depth, display_on_screen = sys.argv
        
        output_path = output_path.replace('\\', '/')
        xml_path = xml_path.replace('\\', '/')
        
        pmcxml2isis = PMCXML2ISIS('ohflc', IDFile2ISIS(cisis_path), '_pmcxml2isis.txt')
        pmcxml2isis.execute(xml_path, suppl_xml, output_path, db_name, script_filename, int(debug_depth), (display_on_screen == 'yes'))
        
        
    
    