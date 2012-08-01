import os
import sys
import json
import shutil

from files_counter import FilesCounter

from xml2json_converter import XML2JSONConverter
from json2id_article import JSON2IDFile_Article
from id2isis import IDFile2ISIS

from report import Report
from parameters import Parameters
from my_files import MyFiles

from json_article import JSON_Article

from journal_issue_article import JournalList, JournalIssues

my_files = MyFiles()


class PMCXML2ISIS:

    def __init__(self, records_order, id2isis, xml2json_table_filename = '_pmcxml2isis.txt'):
        self.xml2json_table_filename = xml2json_table_filename
        self.records_order = records_order
        self.id2isis = id2isis
        self.json_article = JSON_Article()
        self.all_issues = JournalIssues()
        self.journal_list = JournalList()

       
    def generate_json(self, xml_filename, supplementary_xml_filename, report):
        xml2json_converter = XML2JSONConverter(self.xml2json_table_filename, report)
        return xml2json_converter.convert(xml_filename)
        
            
    def generate_id_file(self, json_data, id_filename, report, db_name):
        id_file = JSON2IDFile_Article(id_filename, report)
        id_file.format_and_save_document_data(json_data, self.records_order, db_name)
        
    def generate_db(self, xml_path, output_path, report):
        
        list = os.listdir(xml_path)
        xml_list = [ f for f in list if '.xml' in f ]

        for f in xml_list:
            xml_filename = xml_path + '/' + f
            report.log_event('Loading ' + xml_filename, True)
            
            id_filename = f.replace('.xml', '.id')
            
            json_data = self.generate_json(xml_filename, '', report)
            journal, issue, article = self.json_article.extract_journal_issue_article(json_data)
            
            find_journal = None 
            failed = False 

            if (article == None):
                report.log_error('  Invalid article data', True)
                failed = True

            if (issue == None):
                report.log_error('  Invalid issue data', True)
                failed = True
            
            if (journal == None):
                report.log_error('  Invalid journal data', True)
                failed = True
            else:
                find_journal = JournalList.find_journal(journal.title)
                if find_journal == None:
                    report.log_error('Invalid journal title: ' + journal.title, True)
                    failed = True
            
            if not failed :
                find_issue = self.all_issues.get(issue.id)
                
                issue.articles.insert(article, False)
            
                journal_folder = journal.acron
                issue_folder = issue.name 
                db_name = issue.name

                files_set = PMCXML_FilesSet(output_path, journal_folder, issue_folder, db_name)
                if find_issue == None:
                    find_issue = self.all_issues.insert(issue, False)
                    files_set.prepare_db_folder()
                files_set.copy_extracted_files_to_their_paths(xml_filename)
            
                self.generate_id_file(article.json_data, files_set.db_path + '/' + id_filename, report, files_set.db_name)
                self.id2isis.id2mst(files_set.db_path + '/' + id_filename, files_set.db_filename)
            
    def process_packages(self, work_path, output_path, report):
        for folder in os.path.listdir(work_path):
            self.generate_db(work_path + '/' + folder, output_path, report)
        

    
      
    

                
if __name__ == '__main__':
    parameter_list = ['', 'packages path', 'work path', 'trash path' 'output path', 'cisis path', 'log filename', 'error filename', 'debug_depth', 'display messages on screen? yes|no']
    parameters = Parameters(parameter_list)
    if parameters.check_parameters(sys.argv):
    	this_script_name, packages_path, xml_path, trash_path, output_path, cisis_path, log_filename, err_filename, debug_depth, display_on_screen = sys.argv
        
        output_path = output_path.replace('\\', '/')
        xml_path = xml_path.replace('\\', '/')
        
        pmcxml2isis = PMCXML2ISIS('ohflc', IDFile2ISIS(cisis_path), '_pmcxml2isis.txt')
        report = Report(log_filename, err_filename, int(debug_depth), (display_on_screen == 'yes')) 
        files_counter = FilesCounter(packages_path, work_path, trash_path)
        files_counter.orgazine_files(report)

        pmcxml2isis.process_packages(files_counter.work_path, output_path, report)
        
        
    
    