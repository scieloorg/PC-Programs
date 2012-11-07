import os
import sys
import shutil
from datetime import date
    
from images.img_converter import ImageConverter


from ftp_service.email_service import EmailService

from input_output.configuration import Configuration
from input_output.report import Report
from input_output.parameters import Parameters

from db.cisis import CISIS, IDFile
from db.json2id import JSON2IDFile

from files.files_uploaded_manager import UploadedFilesManager

from xml_json.xml2json_converter import XML2JSONConverter

from xml2db.json2id_article import JSON2IDFile_Article
from xml2db.json2models import JSON2Models
from xml2db.journal_issue_article import JournalList, JournalIssues, Journal, Section
from xml2db.xml_files_set import XMLFilesSet
from xml2db.xml_folders_set import XMLFoldersSet


# read parameters of execution 
parameter_list = ['script', 'collection' ]         
parameters = Parameters(parameter_list)
if parameters.check_parameters(sys.argv):
    script_name, collection = sys.argv
    
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