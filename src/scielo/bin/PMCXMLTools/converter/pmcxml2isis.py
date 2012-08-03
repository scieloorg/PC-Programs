import os
import sys
import json
import shutil

from files_uploaded_manager import UploadedFilesManager

from xml2json_converter import XML2JSONConverter
from json2id import JSON2IDFile
from json2id_article import JSON2IDFile_Article
from id2isis import IDFile2ISIS, IDFile

from report import Report
from parameters import Parameters
from my_files import MyFiles

from json_article import JSON_Article


from journal_issue_article import JournalList, JournalIssues, Journal
from pmcxml_files_set import PMCXML_FilesSet

my_files = MyFiles()


class PMCXML2ISIS:

    def __init__(self, records_order, id2isis, xml2json_table_filename = '_pmcxml2isis.txt'):
        self.xml2json_table_filename = xml2json_table_filename
        self.records_order = records_order
        self.id2isis = id2isis
        self.json_article = JSON_Article()
        self.issues_list_from_isis = JournalIssues()
        self.journal_list = JournalList()

       
    def generate_json(self, xml_filename, report):
        xml2json_converter = XML2JSONConverter(self.xml2json_table_filename, report)
        return xml2json_converter.convert(xml_filename)
        
            
    def generate_id_file(self, json_data, id_filename, report, db_name):
        id_file = JSON2IDFile_Article(id_filename, report)
        id_file.format_and_save_document_data(json_data, self.records_order, db_name)
        
    def generate_db(self, xml_path, output_path, report):
        issues_list_from_article_xml = JournalIssues()
        
        
        list = os.listdir(xml_path)
        xml_list = [ f for f in list if '.xml' in f ]

        for f in xml_list:
            xml_filename = xml_path + '/' + f
            report.log_event('Loading ' + xml_filename, True)
            json_data = self.generate_json(xml_filename, report)
            issues_list_from_article_xml = self.json_article.return_issues(json_data, self.journal_list, issues_list_from_article_xml, xml_filename)
         
        for issue in issues_list_from_article_xml:   
            journal_folder = issue.journal.acron
            issue_folder = issue.name 
            db_name = issue.name

            files_set = PMCXML_FilesSet(output_path, journal_folder, issue_folder, db_name)
            files_set.prepare_db_folder()
        
            id_file = JSON2IDFile(files_set.db_path + '/i', report)
            
            issue_from_isis = self.issues_list_from_isis.get(issue.id)

            id_file.format_and_save_document_data(issue_from_isis.json_data)
            self.id2isis.id2mst(files_set.db_path + '/i', files_set.db_filename)
        
            for article in issue.articles:
                files_set.move_extracted_files_to_their_paths(article.xml_filename)
                id_filename = os.path.basename(article.xml_filename.replace('.xml', '.id'))
        
                self.generate_id_file(article.json_data, files_set.db_path + '/' + id_filename, report, files_set.db_name)
                self.id2isis.id2mst(files_set.db_path + '/' + id_filename, files_set.db_filename)
            
    def process_packages(self,  work_path, output_path, report):
        for folder in os.listdir(work_path):
            if os.path.isdir(work_path + '/' + folder):
                self.generate_db(work_path + '/' + folder, output_path, report)

    def load_issues_list_from_article_xml(self, issue_db_filename):
        self.id2isis.i2id(issue_db_filename, 'issue.id')
        issue_id_file = IDFile('issue.id')
        json_issues = issue_id_file.id2json()
        self.issues_list_from_isis = JournalIssues()
        json_article = JSON_Article()
     
        for json_issue in json_issues:

            j = self.journal_list.find_journal(json_issue['130'])
            if j != None:
                issue = json_article.return_issue(json_issue, j)
                issue.json_data = json_issue
                self.issues_list_from_isis.insert(issue, False)
        

        
if __name__ == '__main__':
    parameter_list = ['', 'db_issue_filename', 'packages path', 'work path', 'trash path', 'output path', 'cisis path', 'log filename', 'error filename', 'debug_depth', 'display messages on screen? yes|no']
    parameters = Parameters(parameter_list)
    if parameters.check_parameters(sys.argv):
    	this_script_name, db_issue_filename, packages_path, work_path, trash_path, output_path, cisis_path, log_filename, err_filename, debug_depth, display_on_screen = sys.argv
        
        packages_path = packages_path.replace('\\', '/')
        work_path = work_path.replace('\\', '/')
        trash_path = trash_path.replace('\\', '/')
        output_path = output_path.replace('\\', '/')
        cisis_path = cisis_path.replace('\\', '/')
        log_filename = log_filename.replace('\\', '/')
        err_filename = err_filename.replace('\\', '/')
        
        pmcxml2isis = PMCXML2ISIS('ohflc', IDFile2ISIS(cisis_path), '_pmcxml2isis.txt')
        report = Report(log_filename, err_filename, int(debug_depth), (display_on_screen == 'yes')) 
        uploaded_files_manager = UploadedFilesManager(packages_path, work_path, trash_path)
        uploaded_files_manager.organize_files(report)

        pmcxml2isis.load_issues_list_from_article_xml(db_issue_filename)

        pmcxml2isis.process_packages(uploaded_files_manager.work_path, output_path, report)
        
        
    
    