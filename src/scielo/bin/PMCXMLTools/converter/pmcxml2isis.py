import os
import sys

from utils.report import Report
from utils.parameters import Parameters
from utils.cisis import CISIS, IDFile
from utils.json2id import JSON2IDFile
from utils.files_uploaded_manager import UploadedFilesManager

from xml2json_converter import XML2JSONConverter
from json2id_article import JSON2IDFile_Article
from json_article import JSON_Article
from journal_issue_article import JournalList, JournalIssues, Journal, Section
from pmcxml_files_set import PMCXML_FilesSet

from utils.img_converter import ImageConverter


class PMCXML2ISIS:

    def __init__(self, records_order, cisis, xml2json_table_filename = 'inputs/_pmcxml2isis.txt'):
        self.xml2json_table_filename = xml2json_table_filename
        self.records_order = records_order
        self.cisis = cisis
        self.db_issues_list = JournalIssues()
        self.journal_list = JournalList()
        self.issues_list = JournalIssues()
        self.img_converter = ImageConverter()
        

       
    def generate_json(self, xml_filename, report):
        xml2json_converter = XML2JSONConverter(self.xml2json_table_filename, report)
        return xml2json_converter.convert(xml_filename)
        
            
        
    def list_issues(self):
        for issue in self.issues_list:   
            journal_folder = issue.journal.acron
            issue_folder = issue.name 
            db_name = issue.name
            print(journal_folder + ' ' + issue_folder + ' ' + issue.order + ' ' + issue.status)
            
    

    def return_issue_to_compare(self, article):
        create_i_record = False
        issue = self.issues_list.get(article.issue.id)
        if issue == None:
            create_i_record = True
            # issue is not in issues_list, check db_list
            db_issue = self.db_issues_list.get(article.issue.id)
            if db_issue == None:
                # issue is new
                issue = self.issues_list.insert(article.issue, False)
                issue.status = 'not_registered'
            else:
                issue = self.issues_list.insert(db_issue, False)
                issue.status = 'registered'

        return (create_i_record, issue)


    def generate_id_files(self, package_path, serial_path, report):
        json_article = JSON_Article(report)
        
        list = os.listdir(package_path)
        xml_list = [ f for f in list if '.xml' in f ]
        
        issues = {}
        
        self.img_converter.img_to_jpeg(package_path, package_path)

         

        for f in xml_list:
            xml_filename = package_path + '/' + f
            report.log_event('XML filename: ' + xml_filename, True)
            report.log_summary("\n " + 'XML filename: ' + xml_filename)
            
            json_data = self.generate_json(xml_filename, report)
            issue = None
            if type(json_data) == type({}):

                article = json_article.load_article(json_data, self.journal_list, xml_filename)
            
                create, issue_to_compare = self.return_issue_to_compare(article)
                errors = article.issue.is_valid(issue_to_compare)
                warnings = []
                if len(errors) == 0:
                    errors, warnings = article.is_valid()
                else:
                    report.log_error('Invalid issue data of ' + xml_filename, None, True)
                    for err in errors:
                        report.log_error(err, None, True)
                        report.log_summary(' ! Error: ' + err)
                

                if len(errors) == 0:
                    report.log_event(article.issue.journal.title + ' ' + article.issue.name  + ' ' + article.page, True)
                    report.log_summary('  ' + article.issue.journal.title + ' ' + article.issue.name + ' ' + article.page)

                    section = issue_to_compare.toc.insert(Section(article.section_title), False)
                    article.issue = issue_to_compare
                    issue_to_compare.articles.insert(article, True)
                    issues[article.issue.journal.title + ' ' + article.issue.name] = issue_to_compare
                    self.generate_id_file(article, serial_path, report)
                else:
                    #report.log_summary(' ! Error: Invalid article data')
                    for err in errors:
                        report.log_error(err, None, True)
                        report.log_summary(' ! Error: ' + err)
                if len(warnings) > 0:
                    for err in warnings:
                        report.log_error(err, None, True)
                        report.log_summary(' ! Warning: ' + err)

            else:
                report.log_error('Invalid xml ' + xml_filename, None, True)
                report.log_summary(' ! Error: Invalid xml')
        for key, issue in issues.items():
            self.generate_db(serial_path, issue)

    def generate_id_file(self, article, serial_path, report):
        issue = article.issue

        journal_folder = issue.journal.acron
        issue_folder = issue.name 
        db_name = issue.name
            
        files_set = PMCXML_FilesSet(serial_path, journal_folder, issue_folder, db_name)
        

        id_filename = os.path.basename(article.xml_filename.replace('.xml', '.id'))
    
        id_file = JSON2IDFile_Article(files_set.db_path + '/' + id_filename, report)
        id_file.format_and_save_document_data(article.json_data, self.records_order, files_set.db_name)
        
        
        #files_set.archive(article.xml_filename)


    def generate_db(self, serial_path, issue):
        journal_folder = issue.journal.acron
        issue_folder = issue.name 
        db_name = issue.name
            
        files_set = PMCXML_FilesSet(serial_path, journal_folder, issue_folder, db_name)
        files_set.delete_db()
        
        
        id_file = JSON2IDFile(files_set.db_path + '/i.id', report)
        issue.json_data['122'] = str(len(issue.articles.elements))
        issue.json_data['49'] = issue.toc.return_json()

        id_file.format_and_save_document_data(issue.json_data)
    
        self.cisis.id2mst(files_set.db_path + '/i.id', files_set.db_filename)
        if issue.status == 'not_registered':
            self.cisis.append(files_set.db_filename, 'new_issues')

        list = os.listdir(files_set.db_path)
        articles_id = [ f for f in list if '.id' in f and  f != 'i.id' ]
        
        report.log_summary("\n" + ' Total of xml files: ' + str(len(issue.articles.elements)))
        report.log_summary(' Total of id files: ' + str(len(articles_id)) + "\n")
        report.log_summary(' Status of ' + journal_folder +  ' ' + issue_folder + ': ' + issue.status)

        if len(issue.articles.elements) != len(articles_id):
            report.log_summary("\n" + ' ! WARNING: Check total of xml files and id files' + "\n")
        if issue.status == 'not_registered':
            report.log_summary("\n" + ' ! WARNING: New issue '  + journal_folder +  ' ' + issue_folder + "\n" )



        for f in articles_id:        
            self.cisis.id2mst(files_set.db_path + '/' + f, files_set.db_filename)

    def receive_packages(self,  work_path, issues_path, report):
        for folder in os.listdir(work_path):
            if os.path.isdir(work_path + '/' + folder):
                self.generate_id_files(work_path + '/' + folder, issues_path, report)

    def load_xml_issues_list(self, issue_db_filename, report):
        self.cisis.i2id(issue_db_filename, 'issue.id')
        issue_id_file = IDFile('issue.id')
        json_issues = issue_id_file.id2json()
        self.db_issues_list = JournalIssues()
        json_article = JSON_Article(report)
     
        for json_issue in json_issues:

            j = self.journal_list.find_journal(json_issue['130'])
            if j != None:
                issue = json_article.return_issue(json_issue, j)
                issue.json_data = json_issue
                self.db_issues_list.insert(issue, False)
        

        
if __name__ == '__main__':
    parameter_list = ['', 'db_issue_filename', 'packages path', 'work path', 'trash path', 'serial path', 'cisis path', 'log filename', 'error filename', 'summary report', 'debug_depth', 'display messages on screen? yes|no']
    parameters = Parameters(parameter_list)
    if parameters.check_parameters(sys.argv):
    	this_script_name, db_issue_filename, packages_path, work_path, trash_path,  serial_path, cisis_path, log_filename, err_filename, summary_filename, debug_depth, display_on_screen = sys.argv
        
        packages_path = packages_path.replace('\\', '/')
        work_path = work_path.replace('\\', '/')
        trash_path = trash_path.replace('\\', '/')
        #issues_path = issues_path.replace('\\', '/')
        serial_path = serial_path.replace('\\', '/')
        cisis_path = cisis_path.replace('\\', '/')
        log_filename = log_filename.replace('\\', '/')
        err_filename = err_filename.replace('\\', '/')
        summary_filename = summary_filename.replace('\\', '/')

        bkp_path = packages_path + '.bkp'
        print(bkp_path)


        report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        
        pmcxml2isis = PMCXML2ISIS('ohflc', CISIS(cisis_path), 'inputs/_pmcxml2isis.txt')
        uploaded_files_manager = UploadedFilesManager(packages_path, work_path, trash_path, bkp_path)
        uploaded_files_manager.organize_files(report)

        pmcxml2isis.load_xml_issues_list(db_issue_filename, report)

        pmcxml2isis.receive_packages(uploaded_files_manager.work_path, serial_path, report)
        print(log_filename)
        print(err_filename)
        print(summary_filename)

        
        
    
    