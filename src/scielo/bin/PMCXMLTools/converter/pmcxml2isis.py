import os
import sys
import shutil

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
from utils.email_sender import EmailSender

class PMCXML2ISIS:

    def __init__(self, records_order, cisis, xml2json_table_filename, email_sender, report, debug_report, debug = False):
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
        self.email_sender = email_sender

       
        
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

    def write_report_package(self, report_package, message, is_summary, is_error, display_on_screen = False, error_data = None):
        self.report.write(message, is_summary, is_error, display_on_screen, error_data)
        report_package.write(message, is_summary, is_error, False, error_data)
        


    def generate_id_files(self, report_package, package_file, work_path, serial_data_path, server_serial_path, img_path, pdf_path, xml_path):
        list = os.listdir(work_path)
        xml_list = [ f for f in list if '.xml' in f ]
        issues = {}
        self.img_converter.img_to_jpeg(work_path, work_path)

        files_set_list = {}
        files_set = None

        for f in xml_list:
            xml_filename = work_path + '/' + f
            
            self.write_report_package(report_package, '\n' + '-' * 80 + '\n' + 'Processing ' + f, True, True, True)

            json_data = self.xml2json_converter.convert(xml_filename)
            issue = None

            if type(json_data) == type({}):

                article = self.json_article.return_article(json_data, self.journal_list, xml_filename, report_package)
            
                create, issue_to_compare = self.return_issue_to_compare(article)
                issue_errors = article.issue.is_valid(issue_to_compare)

                warnings = []
                if len(issue_errors) == 0:
                    issue = article.issue
                    
                    journal_folder = issue.journal.acron
                    issue_folder = issue.name 
                    db_name = issue.name
            
                    if journal_folder + db_name in files_set_list.keys():
                        files_set = files_set_list[journal_folder + db_name]
                    else:
                        files_set = PMCXML_FilesSet(serial_data_path, server_serial_path, img_path, pdf_path, xml_path, journal_folder, issue_folder, db_name)
                        files_set_list[journal_folder + db_name] = files_set

                    self.write_report_package(report_package, ' => ' + article.issue.journal.title + ' ' + article.issue.name + ' ' + article.page, True, False, False)

                    section = issue_to_compare.toc.insert(Section(article.section_title), False)
                    article.issue = issue_to_compare
                    issue_to_compare.articles.insert(article, True)
                    issues[article.issue.journal.acron + article.issue.name] = issue_to_compare

                    self.generate_id_file(report_package, article, files_set)
                else:
                    self.write_report_package(report_package, ' ! ERROR: Invalid issue data of ' + xml_filename, True, True, True)
                    for err in issue_errors:
                        self.write_report_package(report_package, err, True, True, True)

            else:
                self.write_report_package(report_package, ' ! ERROR: Invalid xml ' + xml_filename, True, True, True)

        
        for key, issue in issues.items():
            files_set = files_set_list[key]

            files_set.archive_package_file(package_file)
            self.generate_db(report_package, issue, files_set)

            list = os.listdir(work_path)
            if len(list)>0:
                for file in list:
                    files_set.move_file_to_path(work_path + '/' + file, files_set.extracted_package_path)
            list = os.listdir(work_path)
            if len(list) == 0:
                self.write_report_package(report_package, ' Deleting ' + work_path, True, False, True)
                shutil.rmtree(work_path)
        


        if len(issues) > 1:
            self.write_report_package(report_package, ' ! ERROR: This package contains data of more than one issue:' + ','.join(issues.keys()), True, True, True)


    def generate_id_file(self, report_package, article, files_set):
        #, serial_data_path, server_serial_path, img_path, pdf_path, xml_path
        
        id_filename = os.path.basename(article.xml_filename.replace('.xml', '.id'))
    
        id_file = JSON2IDFile_Article(files_set.id_path + '/' + id_filename, self.report)
        id_file.format_and_save_document_data(article.json_data, self.records_order, files_set.db_name)
        
        
        files_set.archive(article.xml_filename)


    def generate_db(self, report_package, issue, files_set):
        
        self.write_report_package(report_package, 'Generating db ' + files_set.serial_path + ' ' + issue.name, True, False, True )
        
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
        
        
        self.write_report_package(report_package, ' Total of xml files: ' + str(len(issue.articles.elements)), True, False, False )
        self.write_report_package(report_package, ' Total of id files: ' + str(len(articles_id)) , True, False, False  )
        self.write_report_package(report_package, ' Status of ' + issue.journal.acron +  ' ' + issue.name  + ': ' + issue.status, True, False, False  )
        


        if len(issue.articles.elements) != len(articles_id):
            self.write_report_package(report_package, ' ! WARNING: Check total of xml files and id files', True, True, True )
        
        if issue.status == 'not_registered':
            self.write_report_package(report_package, "\n" + ' ! WARNING: New issue '  + issue.journal.acron +  ' ' + issue.name  + "\n" , True, True, True )
        for f in articles_id:        
            self.cisis.id2mst(files_set.id_path + '/' + f, files_set.db_filename)

    def process_packages(self, package_path, work_path, report_path, serial_data_path, server_serial_path, img_path, pdf_path, xml_path, email_data):
        for filename in os.listdir(package_path):
            package_file = package_path + '/' + filename
            self.process_package(package_file, work_path, report_path, serial_data_path, server_serial_path, img_path, pdf_path, xml_path, email_data)

    def process_package(self, package_file, work_path, report_path, serial_data_path, server_serial_path, img_path, pdf_path, xml_path, email_data):
        package_path = os.path.dirname(package_file)
        folder = os.path.basename(package_file)
        folder = folder[0:folder.rfind('.')]

        work_path += '/' + folder 


        files = ['detailed.log', 'error.log', 'summarized.txt'] 
        log_filename, err_filename, summary_filename = [ report_path + '/' +  folder + '_' + f for f in files ]
        report_package = Report(log_filename, err_filename, summary_filename, 0, False) 

        self.write_report_package(report_package, 'Processing package ' + package_file, True, False, True )
        

        uploaded_files_manager = UploadedFilesManager(report_package, package_path)
        uploaded_files_manager.extract_file(package_file, work_path)
        uploaded_files_manager.backup(package_file)

        emails = ''
        package_name = os.path.basename(package_file)
        if os.path.exists(work_path + '/email.txt'):
            f = open(work_path + '/email.txt', 'r')
            emails = f.read()
            f.close()

        self.generate_id_files(report_package, package_file, work_path, serial_data_path, server_serial_path, img_path, pdf_path, xml_path)
        
        self.send_email(email_data, emails, package_name, [summary_filename,err_filename, ])

    def send_email(self, email_data, emails, package_name, report_files):        
        emails = emails.replace(';', ',')
        

        if email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] == 'yes':
            to = emails.split(',')
            text = ''
            bcc = email_data['BCC_EMAIL']
        else:
            to = email_data['BCC_EMAIL']
            text = email_data['ALERT_FORWARD'] + emails + '\n'  + '-' * 80
            bcc = []

        if len(email_data['EMAIL_TEXT']) > 0:
            if os.path.isfile(email_data['EMAIL_TEXT']):
                f = open(email_data['EMAIL_TEXT'], 'r')
                text = f.read()
                f.close()

                text = text.replace('REPLACE_PACKAGE', package_name)
        
        if email_data['FLAG_ATTACH_REPORTS'] == 'yes':
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'em anexo')

            for item in report_files:
                f = open(item, 'r')
                text += '-'* 80 + '\n'+ f.read() + '-'* 80 + '\n' 
                f.close()

        else:
            report_files = []
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'abaixo')
        

        if email_data['IS_AVAILABLE_EMAIL_SERVICE'] == 'yes':
            email_sender.send(to, [], email_data['BCC_EMAIL'], 'XML SciELO ' + package_name, text, report_files)
        else:
            self.report.write('Email data:' + package_name)
            
            self.report.write('to:' + ','.join(to))
            self.report.write('bcc:' + ','.join(bcc))
            self.report.write('text:' + text)
            self.report.write('files:' + ','.join(report_files))


        
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
    # read configuration data
    f = open('configuration.ini', 'r')
    configuration = {}
    for c in f.readlines():
        if '=' in c:
            c = c.strip('\n').split('=')
            configuration[c[0]] = c[1].replace('\\', '/')
            if '_PATH' in c[0] and '/' in configuration[c[0]]:
                if not os.path.exists(configuration[c[0]]):
                    os.makedirs(configuration[c[0]])
    f.close()
    config_parameters = ['FLAG_ATTACH_REPORTS','ALERT_FORWARD', 'IS_AVAILABLE_EMAIL_SERVICE', 'EMAIL_TEXT', 'SENDER_EMAIL', 'BCC_EMAIL', 'FLAG_SEND_EMAIL_TO_XML_PROVIDER', 'DB_ISSUE_FILENAME', 'FTP_PATH', 'IN_PROC_PATH',  'WORK_PATH', 'TRASH_PATH', 'SERIAL_DATA_PATH', 'SERIAL_PROC_PATH', 'PDF_PATH', 'IMG_PATH', 'XML_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']
    
    error = False
    for i in config_parameters:
        if not i in configuration.keys():
            print('Missing ' + i)
            error = True
            break

    what_to_do = ''
    if not error:
        from datetime import date
        
        # read parameters of execution 
        parameter_list = ['script', 'operation = ftp (to download the packages from ftp)|  process (to process the packages)' ]         
        parameters = Parameters(parameter_list)
        if parameters.check_parameters(sys.argv):
            script_name, what_to_do = sys.argv
        else:
            what_to_do = 'process'
        # setting configuration
        db_issue_filename = configuration['DB_ISSUE_FILENAME']
        
        ftp_path = configuration['FTP_PATH']
        inproc_path = configuration['IN_PROC_PATH']
        work_path = configuration['WORK_PATH']
        trash_path = configuration['TRASH_PATH']

        report_path = work_path + '/reports/' + date.today().isoformat()
        if not os.path.exists(report_path):
            os.makedirs(report_path)
        
        serial_data_path = configuration['SERIAL_DATA_PATH']
        server_serial_path = configuration['SERIAL_PROC_PATH']

        web_pdf_path = configuration['PDF_PATH']
        web_img_path = configuration['IMG_PATH']
        web_xml_path = configuration['XML_PATH']

        cisis_path = configuration['CISIS_PATH']
        
        log_filename = configuration['LOG_FILENAME']
        err_filename = configuration['ERROR_FILENAME']
        summary_filename = configuration['SUMMARY_REPORT']

        debug_depth = configuration['DEBUG_DEPTH']
        display_on_screen = configuration['DISPLAY_MESSAGES_ON_SCREEN']

        bkp_path = inproc_path + '.bkp'
        
        email_data = {}
        email_data['SENDER_EMAIL'] = configuration['SENDER_EMAIL']
        email_data['BCC_EMAIL'] = configuration['BCC_EMAIL'].split(',')
        email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] = configuration['FLAG_SEND_EMAIL_TO_XML_PROVIDER']
        email_data['EMAIL_TEXT'] = configuration['EMAIL_TEXT']
        email_data['IS_AVAILABLE_EMAIL_SERVICE'] = configuration['IS_AVAILABLE_EMAIL_SERVICE']
        email_data['ALERT_FORWARD'] = configuration['ALERT_FORWARD']
        email_data['FLAG_ATTACH_REPORTS'] = configuration['FLAG_ATTACH_REPORTS']

        # instancing reports
        files = [ log_filename, err_filename, summary_filename]
        
        debug_log_filename, debug_err_filename, debug_summary_filename =  [ report_path + '/debug_' + f for f in files ]
        debug_report = Report(debug_log_filename, debug_err_filename, debug_summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        
        log_filename, err_filename, summary_filename = [ report_path + '/' + f for f in files ]
        report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        


    if what_to_do == 'process':
        # Load XML data into ISIS Database
        
        # Move files from ftp_path to inproc_path
        uploaded_files_manager = UploadedFilesManager(report, ftp_path)
        uploaded_files_manager.transfer_files(inproc_path)

        pmcxml2isis = PMCXML2ISIS('ohflc', CISIS(cisis_path), 'inputs/_pmcxml2isis.txt', EmailSender(email_data['SENDER_EMAIL']), report, debug_report)
        
        # load data of all the issues registered in issue database
        pmcxml2isis.load_xml_issues_list(db_issue_filename, report)

        # process the package of XML files. Each package file is a compressed file and must contains all the articles of an issue
        pmcxml2isis.process_packages(inproc_path, work_path, report_path, serial_data_path, server_serial_path, web_img_path, web_pdf_path, web_xml_path, email_data)

        print('-' * 80)
        print('Check report files:  ')
        print('Errors report: ' + err_filename)
        print('Summarized report: ' + summary_filename)
        
        print('Detailed report: ' + log_filename)
        print('Reports for each package of XML files in ' + work_path)

    elif what_to_do == 'ftp':
        # baixar do servidor de ftp e apagar de la
        # TODO
        from utils.my_ftp import MyFTP

        print(what_to_do)
    
        
        
    
    