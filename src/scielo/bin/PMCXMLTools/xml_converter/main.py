import os
import sys
import shutil
from datetime import date
    
from utils.report import Report
from utils.parameters import Parameters
from utils.cisis import CISIS, IDFile
from utils.json2id import JSON2IDFile
from utils.files_uploaded_manager import UploadedFilesManager

from xml2json_converter import XML2JSONConverter
from json2id_article import JSON2IDFile_Article
from json2models import JSON2Models
from journal_issue_article import JournalList, JournalIssues, Journal, Section
from xml_files_set import XMLFilesSet
from xml_folders_set import XMLFoldersSet

from utils.img_converter import ImageConverter
from utils.email_service import EmailService
from utils.configuration import Configuration

class DBManager:
    def __init__(self, report, xml_folders, cisis):
        self.report = report
        self.xml_folders = xml_folders
        
        self.cisis = cisis
        
        self.inproc_journal_titles = []    
        self.registered_issues = JournalIssues()
        self.not_registered_issues = JournalIssues()

        # issues of this processing
        self.inproc_issues = JournalIssues()
        

    def db2json(self, db):
        from tempfile import mkstemp
        import os
        r = []
        if os.path.exists(db + '.mst'):
            _, f = mkstemp()
            self.cisis.i2id(db, f)
            r = IDFile(f).id2json()
            os.remove(f)
        return r
      
    
    def create_issue_db_for_the_processing(self, proc_issue_db):
        self.cisis.create('null count=0', proc_issue_db)
        for f in os.listdir(self.xml_folders.id_folder):
            self.cisis.id2mst(self.xml_folders.id_folder + '/' + f, proc_issue_db, False)        
    
    def create_title_db_for_the_processing(self, json_registered_journals, proc_title_db):
        
        new = []
        for json_title in json_registered_journals:
            if '100' in json_title:
                if json_title['100'] in self.inproc_journal_titles:
                    new.append(json_title)
        print(json_title)
        from tempfile import mkstemp
        import os
        _, temp_title_id_filename = mkstemp()
                    
        print(json_registered_journals)
        print( '~' * 80)
        print(new)
        JSON2IDFile(temp_title_id_filename, self.report).format_and_save_document_data(new)   
        self.cisis.id2i(temp_title_id_filename, proc_title_db)
        os.remove(temp_title_id_filename)

    def copy_to_central_processing(self, proc_title_db, proc_issue_db, proc_serial_path, central_title_db, central_issue_db, central_serial_path):
        path = os.path.basename(central_title_db)
        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.basename(central_issue_db)
        if not os.path.exists(path):
            os.makedirs(path)

        print(proc_title_db + ' ' + central_title_db)
        self.cisis.append(proc_title_db, central_title_db)

        print(proc_issue_db + ' ' + central_issue_db)
        self.cisis.append(proc_issue_db, central_issue_db)

        for acron_folder in os.listdir(proc_serial_path):
            proc_acron_folder = proc_serial_path + '/' + acron_folder

            if os.path.isfile(proc_acron_folder):
                shutil.copy(proc_acron_folder, central_serial_path)

            elif os.path.isdir(proc_acron_folder):
                central_acron_folder = central_serial_path + '/' + acron_folder

                if not os.path.exists(central_acron_folder):
                    os.makedirs(central_acron_folder)

                for issue_folder in os.listdir(proc_acron_folder):

                    acron_issue_folder = acron_folder + '/' + issue_folder
                    proc_acron_issue_path = proc_serial_path + '/' + acron_issue_folder

                    if os.path.isdir(proc_serial_path + '/' + acron_issue_folder):
                        base_path = '/' + acron_issue_folder + '/base'

                        if os.path.exists(central_serial_path + base_path):
                            for file_in_base_folder in os.listdir(central_serial_path + base_path):
                                if os.path.isfile(file_in_base_folder):
                                    os.unlink(file_in_base_folder)
                        else:
                            os.makedirs(central_serial_path + base_path)
                        for file_in_base_folder in os.listdir(proc_serial_path + base_path):
                            if os.path.isfile(file_in_base_folder):
                                shutil.copyfile(file_in_base_folder, central_serial_path + base_path)
                

    def store_article(self, article, records_order, filename):
        
        # identify files and paths
        issue_files = XMLFilesSet(self.xml_folders, article.issue.journal.acron, article.issue.name , article.issue.name)
        id_filename = os.path.basename(article.xml_filename.replace('.xml', '.id'))
        
        # generate id file for one article
        id_file = JSON2IDFile_Article(issue_files.id_path + '/' + id_filename, self.report)
        id_file.format_and_save_document_data(article.json_data, records_order, issue_files.db_name, issue_files.xml_filename(article.xml_filename))
        
        # archive files
        issue_files.archive(filename)

        # for GeraPadrao
        if not article.issue.journal.title in self.inproc_journal_titles:
            self.inproc_journal_titles.append(article.issue.journal.title)

    def store_issue(self, issue, id_filename):
        # generate id filename
        id_file = JSON2IDFile(id_filename, self.report)
        issue.json_data['122'] = str(len(issue.articles.elements))
        issue.json_data['49'] = issue.toc.return_json()
        id_file.format_and_save_document_data(issue.json_data)
    
        # copy id filename to processing path
        fname = self.xml_folders.id_folder + '/' + issue.journal.acron + issue.name + '.id'
        if os.path.exists(fname):
            os.unlink(fname)
        shutil.copyfile(id_filename, fname)

        
    def store_issue_articles(self, issue):
        issue_files = XMLFilesSet(self.xml_folders, issue.journal.acron, issue.name , issue.name)
        
        self.report.write('\n' + '-' * 80 + '\n' + 'Generating db ' + issue_files.processing_serial_path + ' ' + issue.name, True, False, True )
        
        
        id_filename = issue_files.id_path + '/i.id'

        self.store_issue(issue, id_filename)

        # id 2 i
        self.cisis.id2mst(id_filename, issue_files.db_filename, True)

        # append to issue of processing
        if issue.status == 'not_registered':
            self.cisis.append(issue_files.db_filename, self.xml_folders.new_issues_db)
            self.report.write("\n" + ' ! WARNING: New issue '  + issue.journal.acron +  ' ' + issue.name  + "\n" , True, True, True )
        
        
        list = os.listdir(issue_files.id_path)
        articles_id = [ f for f in list if '.id' in f and  f != 'i.id' ]
        
        # generate db of all the articles
        for f in articles_id:        
            self.cisis.id2mst(issue_files.id_path + '/' + f, issue_files.db_filename, False)

        # report
        self.report.write(' Total of xml files: ' + str(len(issue.articles.elements)), True, False, False )
        self.report.write(' Total of id files: ' + str(len(articles_id)) , True, False, False  )
        self.report.write(' Status of ' + issue.journal.acron +  ' ' + issue.name  + ': ' + issue.status, True, False, False  )

        if len(issue.articles.elements) != len(articles_id):
            self.report.write(' ! WARNING: Check total of xml files and id files', True, True, True )

    def add_to_scilista(self, issue):
        self.xml_folders.add_to_scilista(issue.journal.acron, issue.name)


class Loader:
    def __init__(self, xml2json_converter, records_order, json2model, registered_journals, db_manager, xml_folders):
        self.xml2json_converter = xml2json_converter
        self.records_order = records_order

        self.json2model = json2model
        
        self.db_manager = db_manager

        self.xml_folders = xml_folders

        self.registered_journals = registered_journals
        self.inproc_issues = JournalIssues()
        self.not_registered_issues = JournalIssues()
        self.registered_issues = JournalIssues()


    def return_issue(self, issue):        
        found = self.inproc_issues.get(issue.id)
        if found == None:
            # issue is registered
            found = self.registered_issues.get(issue.id)
            if found == None:
                # issue is in new_issues
                found = self.not_registered_issues.get(issue.id)
                if found == None:
                    found = self.inproc_issues.insert(issue, False)
                    found.status = 'not_registered'
                else:
                    found = self.inproc_issues.insert(issue, False)
                    found.status = 'new_issues'
            else:
                found = self.inproc_issues.insert(issue, False)
                found.status = 'registered'        
        return found

    def return_invalid_value_msg(self, label, invalid_value, correct_value = ''):
        r =  invalid_value + ' is not a valid ' + label 
        if len(correct_value) > 0:
            r += '. Expected: ' + correct_value
        return r 

    def validate_issue(self, correct_issue, issue):
        errors = []
        
        items = {}
        items['ISSN'] = (correct_issue.journal.issn_id, issue.journal.issn_id)
        items['journal title'] = (correct_issue.journal.title, issue.journal.title)
        items['acron'] = (correct_issue.journal.acron, issue.journal.acron)
        items['issue'] = (correct_issue.journal.acron + ' ' + correct_issue.name, issue.journal.acron + ' ' + issue.name)
        items['dateiso'] = (correct_issue.dateiso, issue.dateiso)
        
        for key, item in items.items():
            if item[0] != item[1]:
                errors.append(self.return_invalid_value_msg(key, item[1], item[0]))
        return errors

    def load(self, package):
        loaded_issues = {}
        
        package.fix_xml_extension()
        package.convert_img_to_jpg()

        package_files = os.listdir(package.work_path)
        
        package_pdf_files = [ f for f in package_files if f.endswith('.pdf') ]

        package_xml_files = [ f for f in package_files if f.endswith('.xml') ]

        unmatched_pdf = [ pdf for pdf in package_pdf_files if not pdf.replace('.pdf', '.xml') in package_xml_files ]

        package.report.write('XML Files: ' + str(len(package_xml_files)), True)
        package.report.write('PDF Files: ' + str(len(package_pdf_files)), True)

        if len(package_xml_files) == 0:
            package.report.write('All the files in the package: ' + '\n' + '\n'.join(package_files), False, True, False)

        if len(unmatched_pdf) > 0:
            package.report.write('PDF files which there is no corresponding XML file: ' + '\n' + '\n'.join(unmatched_pdf), True, True, False)

        # load all xml files of the package
        for xml_fname in package_xml_files:
            issue = None
            xml_filename = package.work_path + '/' + xml_fname
            
            package.report.write('\n' + '-' * 80 + '\n' + 'File: ' + xml_fname + '\n', True, True, True)
            pdf_filename = xml_filename.replace('.xml', '.pdf')
            if not os.path.exists(pdf_filename):
                package.report.write(' ! WARNING: Missing ' + os.path.basename(pdf_filename), True, True)

            json_data = self.xml2json_converter.convert(xml_filename, package.report)
            
            article = self.load_article(json_data, package, xml_fname)
            if article != None:
                package.report.write(article.display(), True, False, False)
                self.db_manager.store_article(article, self.records_order, xml_filename)
                
                # loaded issue
                loaded_issues[article.issue.journal.acron + article.issue.name] = article.issue
        
        # finish loading, checking issue data
        for key, issue in loaded_issues.items():
            # store articles 
            self.db_manager.store_issue_articles(issue)

            # for GeraPadrao
            self.db_manager.add_to_scilista(issue)

            # archive files
            self.archive_package(package, issue)
            
        
        if len(loaded_issues) > 1:
            package.report.write(' ! ERROR: This package contains data of more than one issue:' + ','.join(loaded_issues.keys()), True, True, True)
    

    def load_article(self, json_data, package, xml_filename):
        article = None
        if type(json_data) != type({}):
            package.report.write(' ! ERROR: Invalid JSON ' + xml_filename, True, True, True, json_data)
        else:
            img_files = package.return_xml_images(xml_filename)

            journal_title = self.json2model.return_article_journal_title(json_data)
            if len(journal_title) == 0:
                package.report.write('Missing journal title in json', True, True)
            else:
                journal = self.registered_journals.find_journal(journal_title)
                if journal == None:
                    titles = ''
                    for t in self.journal_list:
                        titles += ',' + t.title
                    titles = titles[1:]
                    package.report.write(journal_title + ' was not found in title database. '+ '\n' + titles , True, True)
                else:
                    article = self.json2model.return_article(json_data, journal, img_files, xml_filename, package.report)
                    if article == None:
                        package.report.write(' ! ERROR: Invalid ARTICLE JSON ' + xml_filename, True, True, True, json_data)
                        print(json_data)
                    else:
                        package_issue = self.return_issue(article.issue)
                        errors_in_issue = self.validate_issue(package_issue, article.issue)

                        warnings = []
                        if len(errors_in_issue) == 0:
                            article.issue = package_issue
                    
                            section = article.issue.toc.insert(Section(article.section_title), False)
                    
                            article.issue.articles.insert(article, True)
                        else:
                            package.report.write(' ! ERROR: Invalid issue data of ' + xml_filename, True, True, True)
                            for err in errors_in_issue:
                                package.report.write(err, True, True, True)
        
        return article
    
    def archive_package(self, package, issue):
        issue_files = XMLFilesSet(self.xml_folders, issue.journal.acron, issue.name, issue.name)
        
        issue_files.archive_package_file(package.package_file)
        files = os.listdir(package.work_path)
        for filename in files:
            issue_files.move_file_to_path(package.work_path + '/' + filename, issue_files.extracted_package_path)

        files = os.listdir(package.work_path)
        if len(files) == 0:
            package.report.write(' Deleting ' + package.work_path, True, False, True)
            shutil.rmtree(package.work_path)



class Reception:
    def __init__(self, config, report):
        self.config = config 
        self.report = report

    def download(self, my_ftp, subdir_in_ftp_server, download_path):
        self.report.write('Before downloading. Files in ' + download_path, True)
        for f in os.listdir(download_path):
            self.report.write(f, True, False, True)
        self.report.write('Downloading...', True, False, True)

        my_ftp.download_files(download_path, subdir_in_ftp_server)

        self.report.write('After downloading. Files in ' + download_path, True, False, True)
        for f in os.listdir(download_path):
            self.report.write(f, True, False, True)

    def put_files_in_queue(self, download_path, queue_path):   
        uploaded_files_manager = UploadedFilesManager(self.report, download_path)
        uploaded_files_manager.transfer_files(queue_path)

        self.report.write('Downloaded files in ' + queue_path, True, False, True)
        for f in os.listdir(queue_path):
            self.report.write(f, True, False, True)
    
        self.report.write('Read '+ self.report.summary_filename, True, False, True)
        

    def open_packages(self, loader, email_service, email_data, package_path, work_path, report_path):
        for filename in os.listdir(package_path):
            package_file = package_path + '/' + filename

            package = Package(package_file, work_path, report_path)
            package.open_package()
            package.read_package_sender_email()

            # processa
            loader.load(package)

            self.send_report(email_service, email_data, package)

        
    def send_report(self, email_service, email_data, package):        
        emails = package.package_sender_email
        

        if email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] == 'yes':
            to = emails.split(',')
            text = ''
            bcc = email_data['BCC_EMAIL']
        else:

            to = email_data['BCC_EMAIL']
            if len(emails) > 0:
                foward_to = emails
            else:
                foward_to = '(e-mail ausente no pacote)'
            text = email_data['ALERT_FORWARD'] + ' ' +  foward_to + '\n'  + '-' * 80 + '\n\n'
            bcc = []

        if len(email_data['EMAIL_TEXT']) > 0:
            if os.path.isfile(email_data['EMAIL_TEXT']):
                f = open(email_data['EMAIL_TEXT'], 'r')
                text += f.read()
                f.close()

                text = text.replace('REPLACE_PACKAGE', package.package_name)

        attached_files = package.report_files_to_send
        if email_data['FLAG_ATTACH_REPORTS'] == 'yes':
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'em anexo')

        else:
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'abaixo')
            
            for item in attached_files:
                f = open(item, 'r')
                text += '-'* 80 + '\n'+ f.read() + '-'* 80 + '\n' 
                f.close()
            attached_files = []

        self.report.write('Email data:' + package.package_name)
        self.report.write('to:' + ','.join(to))
        self.report.write('bcc:' + ','.join(bcc))
        self.report.write('files:' + ','.join(attached_files))
        self.report.write('text:' + text)

        if email_data['IS_AVAILABLE_EMAIL_SERVICE'] == 'yes':
            email_service.send(to, [], email_data['BCC_EMAIL'], email_data['EMAIL_SUBJECT_PREFIX'] + package.package_name, text, attached_files)

    


class Package:
    def __init__(self, package_file, work_path, report_path):
        self.package_sender_email = ''
        self.package_file = package_file 
        self.report_path = report_path
        self.package_path = os.path.dirname(package_file)
        self.package_filename = os.path.basename(package_file)

        self.package_name = self.package_filename
        self.package_name = self.package_name[0:self.package_name.rfind('.')]

        self.work_path = work_path + '/' + self.package_name
        
        files = ['detailed.log', 'error.log', 'summarized.txt'] 
        self.report_files = [ report_path + '/' +  self.package_name + '_' + f for f in files ]
        log_filename, err_filename, summary_filename = self.report_files
        self.report = Report(log_filename, err_filename, summary_filename, 0, False) 
        self.report_files_to_send = [ summary_filename, err_filename ]
        #self.files = os.listdir(self.work_path)

    def open_package(self):
        self.report.write('\n' +'=' * 80 + '\n' +  'Package: ' + self.package_filename, True, False, True )
        uploaded_files_manager = UploadedFilesManager(self.report, self.package_path)
        uploaded_files_manager.backup(self.package_file)
        uploaded_files_manager.extract_file(self.package_file, self.work_path)
        self.files = os.listdir(self.work_path)
        
    def read_package_sender_email(self):
        if os.path.exists(work_path + '/email.txt'):
            f = open(work_path + '/email.txt', 'r')
            self.package_sender_email = f.read()
            self.package_sender_email = self.package_sender_email.replace(';', ',')
            f.close()
        return self.package_sender_email

    def fix_xml_extension(self):
        xml_list = [ f for f in self.files if f.endswith('.XML') ]
        if len(xml_list)>0:
            self.report.write('Program will convert .XML to .xml', True, False, False)
            for f in xml_list:
                new_name = self.work_path +'/' + f.replace('.XML','.xml')
                shutil.copyfile(self.work_path+'/'+f, new_name)
                if os.path.exists(new_name):
                    self.report.write('Converted ' + new_name, False, False, False)
                    os.unlink(self.work_path+'/'+f)
                else:
                    self.report.write('Unable to convert ' + new_name, True, False, False)

    def convert_img_to_jpg(self):
        ImageConverter().img_to_jpeg(self.work_path, self.work_path)

    def return_xml_images(self, xml_name):
        img_files = [ img_file[0:img_file.rfind('.')] for img_file in self.files if img_file.startswith(xml_name.replace('.xml', '-'))  ]
        return list(set(img_files))


if __name__ == '__main__':
    # read parameters of execution 
    parameter_list = ['script', 'operation = ftp (to download the packages from ftp)|  load (to process the packages)', 'collection' ]         
    parameters = Parameters(parameter_list)
    if parameters.check_parameters(sys.argv):
        script_name, what_to_do, collection = sys.argv
        
        ####################################
        # Checking configuration and parameters
        valid_conf = False

        if what_to_do in 'load, ftp, gerapadrao':
            if what_to_do == 'load':
                required = ['SENDER_NAME', 'EMAIL_SUBJECT_PREFIX', 'PROC_DB_TITLE_FILENAME', 'PROC_DB_ISSUE_FILENAME', 'DB_TITLE_FILENAME', 'FTP_SERVER',  'FTP_USER','FTP_PSWD',  'FTP_DIR', 'FLAG_ATTACH_REPORTS','ALERT_FORWARD', 'IS_AVAILABLE_EMAIL_SERVICE', 'EMAIL_TEXT', 'SENDER_EMAIL', 'BCC_EMAIL', 'FLAG_SEND_EMAIL_TO_XML_PROVIDER', 'DB_ISSUE_FILENAME', 'FTP_PATH', 'QUEUE_PATH', 'IN_PROC_PATH',  'WORK_PATH', 'TRASH_PATH', 'SERIAL_DATA_PATH', 'SERIAL_PROC_PATH', 'PDF_PATH', 'IMG_PATH', 'XML_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']
            elif what_to_do == 'gerapadrao':
                required = ['PROC_DB_TITLE_FILENAME', 'PROC_DB_ISSUE_FILENAME','SERIAL_PROC_PATH', 'COLLECTIONS_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']
            
                collection = 'gerapadrao'
            elif what_to_do == 'ftp':
                required = ['FTP_SERVER', 'FTP_USER', 'FTP_PSWD', 'FTP_DIR', 'FTP_PATH', 'QUEUE_PATH']
            
            if os.path.exists(collection + '.configuration.ini'):
                config = Configuration(collection + '.configuration.ini')
                valid_conf, msg = config.check(required)
            else:
                what_to_do = 'nothing'

                msg = 'There is no ' + collection + '.configuration.ini'
            
        else:
            msg = 'Invalid operation ' + what_to_do + '. Try load or ftp.'
        ####################################

        if not valid_conf:
            print(msg)
            
        else:
            ####################################
            # instancing reports
            log_filename = config.parameters['LOG_FILENAME']
            err_filename = config.parameters['ERROR_FILENAME']
            summary_filename = config.parameters['SUMMARY_REPORT']

            debug_depth = config.parameters['DEBUG_DEPTH']
            display_on_screen = config.parameters['DISPLAY_MESSAGES_ON_SCREEN']

            report_path = config.parameters['REPORT_PATH'] + '/' + date.today().isoformat()
            if not os.path.exists(report_path):
                os.makedirs(report_path)
        
            files = [ log_filename, err_filename, summary_filename]
        
            debug_log_filename, debug_err_filename, debug_summary_filename =  [ report_path + '/debug_' + f for f in files ]
            debug_report = Report(debug_log_filename, debug_err_filename, debug_summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        
            log_filename, err_filename, summary_filename = [ report_path + '/' + f for f in files ]
            report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        
            log_filename, err_filename, summary_filename = [ report_path + '/ftp_' + f for f in files ]
            report_ftp = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
        
            if what_to_do == 'ftp' or  what_to_do == 'load':
                queue_path = config.parameters['QUEUE_PATH']
                download_path = config.parameters['FTP_PATH']

            
            ####################################
            # execution of the operation
            if what_to_do == 'ftp':
                from utils.my_ftp import MyFTP
                

                server = config.parameters['FTP_SERVER']
                user = config.parameters['FTP_USER']
                pasw = config.parameters['FTP_PSWD']
                folder = config.parameters['FTP_DIR']
            
                reception = Reception(config, report_ftp)
                reception.download(MyFTP(report_ftp, server, user, pasw), folder, download_path)

            elif what_to_do == 'gerapadrao':
                db_title_filename = config.parameters['DB_TITLE_FILENAME']

                
                proc_title_db = config.parameters['PROC_DB_TITLE_FILENAME']
                proc_issue_db = config.parameters['PROC_DB_ISSUE_FILENAME']

                cisis = CISIS(config.parameters['CISIS_PATH'])
                cisis.create('null count=0', proc_title_db)
                cisis.create('null count=0', proc_issue_db)

                
                if os.path.exists(config.parameters['SERIAL_PROC_PATH'] + '/scilista.lst'):
                    os.unlink(config.parameters['SERIAL_PROC_PATH'] + '/scilista.lst')

                path = config.parameters['COLLECTIONS_PATH']
                for collection_folder in os.listdir(path):
                    print(collection_folder)
                    collection_serial_path = path + '/' + collection_folder + '/proc/serial'
                    if os.path.exists(collection_serial_path + '/title/title.mst'):
                        cisis.append(collection_serial_path + '/title/title', proc_title_db)
                        os.system('ls ' + proc_title_db + '*')
                    if os.path.exists(collection_serial_path + '/issue/issue.mst'):
                        cisis.append(collection_serial_path + '/issue/issue', proc_issue_db)
                        os.system('ls ' + proc_issue_db + '*')
                    if os.path.exists(collection_serial_path + '/scilista.lst'):
                        f = open(collection_serial_path + '/scilista.lst', 'r')
                        c = f.read()
                        f.close()
                        f = open(config.parameters['SERIAL_PROC_PATH'] + '/scilista.lst', 'a+')
                        f.write(c)
                        f.close()
                        
                    for folder in os.listdir(collection_serial_path):
                        if os.path.isdir(collection_serial_path + '/' + folder):
                            
                            for issue_folder in os.listdir(collection_serial_path+ '/' + folder):

                                issue_base_path = folder + '/' + issue_folder + '/base'
                                dbfiles = []
                                if os.path.exists(collection_serial_path + '/' + issue_base_path):
                                    dbfiles = os.listdir(collection_serial_path + '/' + issue_base_path)
                                
                                if len(dbfiles)>0:
                                    if not os.path.exists(config.parameters['SERIAL_PROC_PATH'] + '/' + issue_base_path):
                                        os.makedirs(config.parameters['SERIAL_PROC_PATH'] + '/' + issue_base_path)
                                    for dbfile in dbfiles:
                                        shutil.copyfile(collection_serial_path + '/' + issue_base_path + '/' + dbfile, config.parameters['SERIAL_PROC_PATH'] + '/' + issue_base_path + '/' + dbfile)
                                    print(issue_base_path + ' has ' + str(len(dbfiles)) + ' files')
                                else:
                                    print(issue_base_path + ' has no files')


                os.system('cd ../proc;./GeraPadrao.bat')
                    
            elif what_to_do == 'load':
        
                # setting configuration
                db_issue_filename = config.parameters['DB_ISSUE_FILENAME']
                db_title_filename = config.parameters['DB_TITLE_FILENAME']


                proc_title_db = config.parameters['PROC_DB_TITLE_FILENAME']
                proc_issue_db = config.parameters['PROC_DB_ISSUE_FILENAME']

                if not os.path.exists(os.path.dirname(proc_issue_db)):
                    os.makedirs(os.path.dirname(proc_issue_db))

                if not os.path.exists(os.path.dirname(proc_title_db)):
                    os.makedirs(os.path.dirname(proc_title_db))

                inproc_path = config.parameters['IN_PROC_PATH']
                work_path = config.parameters['WORK_PATH']
                trash_path = config.parameters['TRASH_PATH']
                
                'cisis.append(db_title_filename)
                
        
                archive_serial_path = config.parameters['SERIAL_DATA_PATH']
                processing_serial_path = config.parameters['SERIAL_PROC_PATH']

                web_pdf_path = config.parameters['PDF_PATH']
                web_img_path = config.parameters['IMG_PATH']
                web_xml_path = config.parameters['XML_PATH']

                cisis_path = config.parameters['CISIS_PATH']
        
        
                email_data = {}
                email_data['SENDER_EMAIL'] = config.parameters['SENDER_EMAIL']
                email_data['BCC_EMAIL'] = config.parameters['BCC_EMAIL'].split(',')
                email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] = config.parameters['FLAG_SEND_EMAIL_TO_XML_PROVIDER']
                email_data['EMAIL_TEXT'] = config.parameters['EMAIL_TEXT']
                email_data['IS_AVAILABLE_EMAIL_SERVICE'] = config.parameters['IS_AVAILABLE_EMAIL_SERVICE']
                email_data['ALERT_FORWARD'] = config.parameters['ALERT_FORWARD']
                email_data['FLAG_ATTACH_REPORTS'] = config.parameters['FLAG_ATTACH_REPORTS']
                email_data['EMAIL_SUBJECT_PREFIX'] = config.parameters['EMAIL_SUBJECT_PREFIX']
                
                xml_folders = XMLFoldersSet(archive_serial_path, processing_serial_path, web_img_path, web_pdf_path, web_xml_path, processing_serial_path + '/scilista.lst')
        
                db_manager = DBManager(report, xml_folders, CISIS(cisis_path))
                json_titles = db_manager.db2json(db_title_filename)

                json2models = JSON2Models(report)
                registered_journals = json2models.return_journals_list(json_titles)

                json_issues = db_manager.db2json(db_issue_filename)
                db_manager.registered_issues = json2models.return_issues_list(json_issues, registered_journals)
                
                
                xml2json_converter = XML2JSONConverter('inputs/_pmcxml2isis.txt')
            
                loader = Loader(xml2json_converter, 'ohflc', json2models, registered_journals, db_manager, xml_folders)

                reception = Reception(config, report)
                reception.put_files_in_queue(download_path, queue_path)
                reception.open_packages(loader, EmailService(config.parameters['SENDER_NAME'], email_data['SENDER_EMAIL']), email_data, queue_path, work_path, report_path)

                db_manager.create_issue_db_for_the_processing(proc_issue_db)
                db_manager.create_title_db_for_the_processing(json_titles, proc_title_db)
                
                
                
                print('-' * 80)
                print('Check report files:  ')
                print('Errors report: ' + err_filename)
                print('Summarized report: ' + summary_filename)
        
                print('Detailed report: ' + log_filename)
                print('Reports for each package of XML files in ' + work_path)
            
        
            elif what_to_do == 'process':
        
                # setting configuration
                db_issue_filename = config.parameters['DB_ISSUE_FILENAME']
                db_title_filename = config.parameters['DB_TITLE_FILENAME']
                proc_title_db = config.parameters['PROC_DB_TITLE_FILENAME']
                proc_issue_db = config.parameters['PROC_DB_ISSUE_FILENAME']

                if not os.path.exists(os.path.dirname(proc_issue_db)):
                    os.makedirs(os.path.dirname(proc_issue_db))

                if not os.path.exists(os.path.dirname(proc_title_db)):
                    os.makedirs(os.path.dirname(proc_title_db))

                inproc_path = config.parameters['IN_PROC_PATH']
                work_path = config.parameters['WORK_PATH']
                trash_path = config.parameters['TRASH_PATH']

        
                archive_serial_path = config.parameters['SERIAL_DATA_PATH']
                processing_serial_path = config.parameters['SERIAL_PROC_PATH']

                web_pdf_path = config.parameters['PDF_PATH']
                web_img_path = config.parameters['IMG_PATH']
                web_xml_path = config.parameters['XML_PATH']

                cisis_path = config.parameters['CISIS_PATH']
        
        
                email_data = {}
                email_data['SENDER_EMAIL'] = config.parameters['SENDER_EMAIL']
                email_data['BCC_EMAIL'] = config.parameters['BCC_EMAIL'].split(',')
                email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] = config.parameters['FLAG_SEND_EMAIL_TO_XML_PROVIDER']
                email_data['EMAIL_TEXT'] = config.parameters['EMAIL_TEXT']
                email_data['IS_AVAILABLE_EMAIL_SERVICE'] = config.parameters['IS_AVAILABLE_EMAIL_SERVICE']
                email_data['ALERT_FORWARD'] = config.parameters['ALERT_FORWARD']
                email_data['FLAG_ATTACH_REPORTS'] = config.parameters['FLAG_ATTACH_REPORTS']
                email_data['EMAIL_SUBJECT_PREFIX'] = config.parameters['EMAIL_SUBJECT_PREFIX']


                xml_folders = XMLFoldersSet(archive_serial_path, processing_serial_path, web_img_path, web_pdf_path, web_xml_path, processing_serial_path + '/scilista.lst')
        
                # Load XML data into ISIS Database
        
                # Move files from download_path to inproc_path
                uploaded_files_manager = UploadedFilesManager(report, queue_path)
                uploaded_files_manager.transfer_files(inproc_path)

                proc = Proc(config, report)
                pmcxml2isis = PMCXML2ISIS('ohflc', 'inputs/_pmcxml2isis.txt', CISIS(cisis_path), xml_folders, EmailService(email_data['SENDER_EMAIL']), report, debug_report)
                pmcxml2isis.load_journals(db_title_filename, report)
                # load journal titles which are in proc
                pmcxml2isis.load_proc_journal_list(proc_title_db)

                # load data of all the issues registered in issue database
                pmcxml2isis.load_issues_lists(db_issue_filename, report)
        

                # process the package of XML files. Each package file is a compressed file and must contains all the articles of an issue
                pmcxml2isis.process_packages(inproc_path, work_path, report_path, email_data)

                pmcxml2isis.create_proc_title_and_issue_db(db_title_filename,  proc_title_db, db_issue_filename,  proc_issue_db, report)

                print('-' * 80)
                print('Check report files:  ')
                print('Errors report: ' + err_filename)
                print('Summarized report: ' + summary_filename)
        
                print('Detailed report: ' + log_filename)
                print('Reports for each package of XML files in ' + work_path)
            