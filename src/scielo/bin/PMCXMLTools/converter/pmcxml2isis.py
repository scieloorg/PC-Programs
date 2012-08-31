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

    def __init__(self, records_order, cisis, xml2json_table_filename, report, debug_report, debug = False):
        self.records_order = records_order
        self.cisis = cisis
        self.db_issues_list = JournalIssues()
        self.journal_list = JournalList()
        self.issues_list = JournalIssues()
        self.img_converter = ImageConverter()
        self.report = report
        self.debug_report = debug_report
        self.xml2json_converter = XML2JSONConverter(xml2json_table_filename, debug_report, debug)
        self.json_article = JSON_Article(debug_report, report)

       
        
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

    def write_report_package(self, report_package, message, error_message, error_data, display_on_screen = False):
        if len(error_message) > 0:
            self.report.log_error(error_message, error_data, display_on_screen)
            self.report.log_summary(' ! Error: ' + error_message)
            report_package.log_error(error_message, error_data)
            report_package.log_summary(' ! Error: ' + error_message)
            
        else:
            self.report.log_event(message, display_on_screen)
            self.report.log_summary(message)
            report_package.log_event(message)
            report_package.log_summary(message)
            

    def generate_id_files(self, report_package, package_path, serial_data_path, server_serial_path, img_path, pdf_path, xml_path):
        list = os.listdir(package_path)
        xml_list = [ f for f in list if '.xml' in f ]
        issues = {}
        self.img_converter.img_to_jpeg(package_path, package_path)

        for f in xml_list:
            xml_filename = package_path + '/' + f
            
            self.write_report_package(report_package, '\n' + '-' * 80 + '\n' + 'XML filename: ' + xml_filename, '', '', True)

            json_data = self.xml2json_converter.convert(xml_filename)
            issue = None

            if type(json_data) == type({}):

                article = self.json_article.return_article(json_data, self.journal_list, xml_filename, report_package)
            
                create, issue_to_compare = self.return_issue_to_compare(article)
                errors = article.issue.is_valid(issue_to_compare)

                warnings = []
                if len(errors) == 0:
                    errors, warnings = self.json_article.article_is_valid()
                else:
                    self.report.log_error('Invalid issue data of ' + xml_filename, None, True)
                    for err in errors:
                        self.write_report_package(report_package, '', err, None, True)

                if len(errors) == 0:
                    self.write_report_package(report_package, ' Identified as ' + article.issue.journal.title + ' ' + article.issue.name + ' ' + article.page, '', None, True)

                    section = issue_to_compare.toc.insert(Section(article.section_title), False)
                    article.issue = issue_to_compare
                    issue_to_compare.articles.insert(article, True)
                    issues[article.issue.journal.title + ' ' + article.issue.name] = issue_to_compare
                    self.generate_id_file(report_package, article, serial_data_path, server_serial_path, img_path, pdf_path, xml_path)
                else:
                    #self.report.log_summary(' ! Error: Invalid article data')
                    for err in errors:
                        self.write_report_package(report_package, '', err, None, True)
            else:
                self.write_report_package(report_package, '   Invalid xml ' + xml_filename, '', None, True)

        for key, issue in issues.items():
            self.generate_db(report_package, serial_data_path, server_serial_path, img_path, pdf_path, xml_path, issue)

    def generate_id_file(self, report_package, article, serial_data_path, server_serial_path, img_path, pdf_path, xml_path):
        issue = article.issue

        journal_folder = issue.journal.acron
        issue_folder = issue.name 
        db_name = issue.name
            
        files_set = PMCXML_FilesSet(serial_data_path, server_serial_path, img_path, pdf_path, xml_path, journal_folder, issue_folder, db_name)

        id_filename = os.path.basename(article.xml_filename.replace('.xml', '.id'))
    
        id_file = JSON2IDFile_Article(files_set.id_path + '/' + id_filename, self.report)
        id_file.format_and_save_document_data(article.json_data, self.records_order, files_set.db_name)
        
        
        files_set.archive(article.xml_filename)


    def generate_db(self, report_package, serial_data_path, server_serial_path, img_path, pdf_path, xml_path, issue):
            
        self.write_report_package(report_package, 'Generating db ' + serial_data_path + ' ' + issue.name, '', '', True )
        
        journal_folder = issue.journal.acron
        issue_folder = issue.name 
        db_name = issue.name
            
        files_set = PMCXML_FilesSet(serial_data_path, server_serial_path, img_path, pdf_path, xml_path, journal_folder, issue_folder, db_name)
        files_set.delete_db()
        

        id_file = JSON2IDFile(files_set.id_path + '/i.id', report)
        issue.json_data['122'] = str(len(issue.articles.elements))
        issue.json_data['49'] = issue.toc.return_json()

        id_file.format_and_save_document_data(issue.json_data)
    
        self.cisis.id2mst(files_set.id_path + '/i.id', files_set.db_filename)
        if issue.status == 'not_registered':
            self.cisis.append(files_set.db_filename, 'new_issues')

        list = os.listdir(files_set.id_path)
        articles_id = [ f for f in list if '.id' in f and  f != 'i.id' ]
        
        
        self.write_report_package(report_package, ' Total of xml files: ' + str(len(issue.articles.elements)), '', '', False )
        self.write_report_package(report_package, ' Total of id files: ' + str(len(articles_id)) , '', '', False )
        self.write_report_package(report_package, ' Status of ' + journal_folder +  ' ' + issue_folder + ': ' + issue.status, '', '', False )
        


        if len(issue.articles.elements) != len(articles_id):
            self.write_report_package(report_package, ' ! WARNING: Check total of xml files and id files', '', '', True )
        
        if issue.status == 'not_registered':
            self.write_report_package(report_package, "\n" + ' ! WARNING: New issue '  + journal_folder +  ' ' + issue_folder + "\n" , '', '', True)
        for f in articles_id:        
            self.cisis.id2mst(files_set.id_path + '/' + f, files_set.db_filename)

    def process_packages(self,  work_path, report_path, serial_data_path, server_serial_path, img_path, pdf_path, xml_path):
        for folder in os.listdir(work_path):
            if os.path.isdir(work_path + '/' + folder):
                files = ['detailed.log', 'error.log', 'summarized.txt'] 
                log_filename, err_filename, summary_filename = [ report_path + folder + '_' + f for f in files ]
                report_package = Report(log_filename, err_filename, summary_filename, 0, False) 
        
                self.write_report_package(report_package, 'Processing package ' + work_path + '/' + folder, '', '', False )
        
                self.generate_id_files(report_package, work_path + '/' + folder, serial_data_path, server_serial_path, img_path, pdf_path, xml_path)
                

    def load_xml_issues_list(self, issue_db_filename, report):
        self.cisis.i2id(issue_db_filename, 'issue.id')
        issue_id_file = IDFile('issue.id')
        json_issues = issue_id_file.id2json()
        self.db_issues_list = JournalIssues()
        
        for json_issue in json_issues:

            j = self.journal_list.find_journal(json_issue['130'])
            if j != None:
                issue = self.json_article.return_issue(json_issue, j)
                issue.json_data = json_issue
                self.db_issues_list.insert(issue, False)
        

        
if __name__ == '__main__':

    f = open('configuration.ini', 'r')
    configuration = {}
    for c in f.readlines():
        if '=' in c:
            c = c.strip('\n').split('=')
            configuration[c[0]] = c[1]
    f.close()

    parameters = ['DB_ISSUE_FILENAME', 'INCOMING_PACKAGES_PATH', 'WORK_PATH', 'TRASH_PATH', 'SERIAL_DATA_PATH', 'SERIAL_PROC_PATH', 'PDF_PATH', 'IMG_PATH', 'XML_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']
    error = False
    for i in parameters:
        if not i in configuration.keys():
            print('Missing ' + i)
            error = True
            break

            


    if not error:
        db_issue_filename = configuration['DB_ISSUE_FILENAME']
        incoming_path = configuration['INCOMING_PACKAGES_PATH'].replace('\\', '/')
        work_path = configuration['WORK_PATH'].replace('\\', '/')

        report_path = work_path + '/reports'  
        if not os.path.exists(report_path):
            os.makedirs(report_path)

        from datetime import datetime 
        report_path += '/' + datetime.now().isoformat().replace('T', '-').replace(':', '-')[0:16] + '_'

        trash_path = configuration['TRASH_PATH'].replace('\\', '/')
        #issues_path = issues_path.replace('\\', '/')
        serial_data_path = configuration['SERIAL_DATA_PATH'].replace('\\', '/')
        server_serial_path = configuration['SERIAL_PROC_PATH'].replace('\\', '/')
        web_pdf_path = configuration['PDF_PATH'].replace('\\', '/')
        web_img_path = configuration['IMG_PATH'].replace('\\', '/')
        web_xml_path = configuration['XML_PATH'].replace('\\', '/')

        cisis_path = configuration['CISIS_PATH'].replace('\\', '/')
        
        log_filename = configuration['LOG_FILENAME'].replace('\\', '/')
        err_filename = configuration['ERROR_FILENAME'].replace('\\', '/')
        summary_filename = configuration['SUMMARY_REPORT'].replace('\\', '/')

        debug_depth = configuration['DEBUG_DEPTH']
        display_on_screen = configuration['DISPLAY_MESSAGES_ON_SCREEN']

        bkp_path = incoming_path + '.bkp'
        print(bkp_path)

        files = [ log_filename, err_filename, summary_filename]
        
        debug_log_filename, debug_err_filename, debug_summary_filename =  [ report_path + 'debug_' + f for f in files ]
        debug_report = Report(debug_log_filename, debug_err_filename, debug_summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        
        log_filename, err_filename, summary_filename = [ report_path +  f for f in files ]
        report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        
        pmcxml2isis = PMCXML2ISIS('ohflc', CISIS(cisis_path), 'inputs/_pmcxml2isis.txt', report, debug_report)
        uploaded_files_manager = UploadedFilesManager(incoming_path, work_path, trash_path, bkp_path)
        uploaded_files_manager.organize_files(report)

        pmcxml2isis.load_xml_issues_list(db_issue_filename, report)

        pmcxml2isis.process_packages(uploaded_files_manager.work_path, report_path , serial_data_path, server_serial_path, web_img_path, web_pdf_path, web_xml_path)

        print('-' * 80)
        print('Check report files:  ')
        print('Errors report: ' + err_filename)
        print('Summarized report: ' + summary_filename)
        
        print('Detailed report: ' + log_filename)
        print('Reports for each package of XML files in ' + work_path)

        
        
        
    
    