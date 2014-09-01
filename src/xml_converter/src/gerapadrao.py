import os
import sys
import shutil
from datetime import date
    
from reuse.files.name_file import return_path_based_on_date

from reuse.services.email_service.email_service import EmailService, EmailMessageTemplate
from reuse.services.email_service.report_sender_xml_process import ReportSender, ReportSenderConfiguration

from reuse.input_output.configuration import Configuration
from reuse.input_output.report import Report
from reuse.input_output.parameters import Parameters
from reuse.input_output.tracker import Tracker

from reuse.db.isis.cisis import CISIS



# read parameters of execution 
parameter_list = ['script' ]         
parameters = Parameters(parameter_list)
doit = False

if parameters.check_parameters(sys.argv):
    
    
    ####################################
    # Checking configuration and parameters
    valid_conf = False

    required = ['PROC_DB_TITLE_FILENAME', 'PROC_DB_ISSUE_FILENAME','PROC_SERIAL_PATH', 'COLLECTIONS_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']
        
    if os.path.exists('gerapadrao.configuration.ini'):
        config = Configuration('gerapadrao.configuration.ini')
        valid_conf, msg = config.check(required)
    
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

        report_path = config.parameters['REPORT_PATH'] + '/' + return_path_based_on_date()
        if not os.path.exists(report_path):
            os.makedirs(report_path)
    
        files = [ log_filename, err_filename, summary_filename]
    
        log_filename, err_filename, summary_filename = [ report_path + '/' + f for f in files ]
        report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
    
        proc_title_db = config.parameters['PROC_DB_TITLE_FILENAME']
        proc_issue_db = config.parameters['PROC_DB_ISSUE_FILENAME']

        if not os.path.exists(os.path.dirname(proc_title_db)):
            os.makedirs(os.path.dirname(proc_title_db ))
            
        if not os.path.exists(os.path.dirname(proc_issue_db)):
            os.makedirs(os.path.dirname(proc_issue_db ))
                

        cisis = CISIS(config.parameters['CISIS_PATH'])

        tracker = Tracker(config.parameter('GERAPADRAO_TRACKER_PATH'), config.parameter('GERAPADRAO_TRACKER_NAME'))
        
        #message_type = MessageType(config.parameter('EMAIL_SUBJECT_PREFIX_GERAPADRAO'), config.parameter('EMAIL_TEXT_GERAPADRAO'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER'), config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        #report_sender = ReportSender(report, config.parameter('IS_AVAILABLE_EMAIL_SERVICE'), email_service, config.parameter('BCC_EMAIL').split(','), message_type)

        

        email_service = EmailService('', config.parameter('SENDER_EMAIL'), 'localhost', config.parameter('IS_AVAILABLE_EMAIL_SERVICE') == 'yes')
        report_sender_config = ReportSenderConfiguration(config.parameter('BCC_EMAIL'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER') == 'yes', config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        report_sender = ReportSender(email_service, report_sender_config)
        template = EmailMessageTemplate(config.parameter('EMAIL_SUBJECT_PREFIX_GERAPADRAO'), config.parameter('EMAIL_TEXT_GERAPADRAO'))
        
        status = 'off'
        if config.parameter('CTRL_FILE') != '':
            if os.path.exists(config.parameters['CTRL_FILE']):
                f = open(config.parameters['CTRL_FILE'], 'r')
                status = f.read()
                if 'off' in status:
                    status = 'off'
                elif 'on' in status:
                    status = 'on'
                f.close()
        doit = (status == 'off')
        if status == 'off':
            f = open(config.parameters['CTRL_FILE'], 'w')
            f.write('on')
            f.close()
print('status=.' + status + '.')
print('gerapadrao ?')
print(doit)

if doit: 
    tracker.register('GeraPadrao', 'preparation')
    ## -  
    report.write('Reset ' + proc_title_db, True, False, True)
    cisis.create('null count=0', proc_title_db)
    report.write('Reset ' + proc_issue_db, True, False, True)
    cisis.create('null count=0', proc_issue_db)
    proc_scilista = config.parameters['PROC_SERIAL_PATH'] + '/scilista.lst'
    report.write('delete scilista:' + proc_scilista, True, False, True)
    proc_scilista_del = config.parameters['PROC_SERIAL_PATH'] + '/scilista_del.lst'
    
    if os.path.exists(proc_scilista):
        os.unlink(proc_scilista)
    ## - 
    if os.path.isfile(proc_scilista_del):
        shutil.copyfile(proc_scilista_del, proc_scilista)

    
    path = config.parameters['COLLECTIONS_PATH']
    report.write('path of collections:' + path, True, False, True)

    for collection_folder in os.listdir(path):
        print(collection_folder)
        report.write('collection folder:' + collection_folder, True, False, True)

        if os.path.exists(collection_folder + '.configuration.ini'):
            collection_config = Configuration(collection_folder + '.configuration.ini')

            collection_serial_path = collection_config.parameter('COL_PROC_SERIAL_PATH')
            report.write('collection serial folder:' + collection_serial_path, True, False, True)
            
            
            shutil.copyfile(collection_config.parameter('DB_TITLE_FILENAME') + '.mst', proc_title_db + '.mst')
            shutil.copyfile(collection_config.parameter('DB_TITLE_FILENAME') + '.xrf', proc_title_db + '.xrf')
                
            ## ISSUE
            shutil.copyfile(collection_config.parameter('DB_ISSUE_FILENAME') + '.mst', proc_issue_db + '.mst')
            shutil.copyfile(collection_config.parameter('DB_ISSUE_FILENAME') + '.xrf', proc_issue_db + '.xrf')


            ## SCILISTA
            report.write('collection scilista:' + collection_config.parameter('COL_SCILISTA') , True, False, True)
        
            if os.path.exists(collection_config.parameter('COL_SCILISTA')):
                f = open(collection_config.parameter('COL_SCILISTA'), 'r')
                c = f.read()
                f.close()
                f = open(proc_scilista, 'a+')
                f.write(c)
                f.close()
            
            if collection_serial_path != config.parameters['PROC_SERIAL_PATH']:
                # copy col_serial to serial
                report.write('issues folders:' + collection_serial_path, True, False, True)
                for folder_in_serial in os.listdir(collection_serial_path):
                    if not folder_in_serial in [ 'title', 'issue', 'i' ] and os.path.isdir(collection_serial_path + '/' + folder_in_serial):
                        # journal folder
                        report.write('journal:' + folder_in_serial, True, False, True)

                        for issue_folder in os.listdir(collection_serial_path+ '/' + folder_in_serial):
                            # issue folder 
                            issue_base_path = folder_in_serial + '/' + issue_folder + '/base'
                            report.write(issue_folder, True, False, True) 

                            dbfiles = []
                            if os.path.exists(collection_serial_path + '/' + issue_base_path):
                                dbfiles = os.listdir(collection_serial_path + '/' + issue_base_path)
                            
                            if len(dbfiles)>0:
                                if not os.path.exists(config.parameters['PROC_SERIAL_PATH'] + '/' + issue_base_path):
                                    os.makedirs(config.parameters['PROC_SERIAL_PATH'] + '/' + issue_base_path)
                                for dbfile in dbfiles:
                                    shutil.copyfile(collection_serial_path + '/' + issue_base_path + '/' + dbfile, config.parameters['PROC_SERIAL_PATH'] + '/' + issue_base_path + '/' + dbfile)
                                print(issue_base_path + ' has ' + str(len(dbfiles)) + ' files')
                            else:
                                print(issue_base_path + ' has no files')

    scilista_items = []
    if os.path.exists(proc_scilista):
        f = open(proc_scilista, 'r')
        scilista_items = f.readlines()
        f.close()
    
    if ''.join(scilista_items) != '':
        tracker.register('Gerapadrao', 'inicio')
        
            
        os.system(config.parameters['RUN_GERAPADRAO_AND_UPDATE_BASES'])
        os.system(config.parameters['RUN_UPDATE_FILES'])
        tracker.register('Gerapadrao', 'fim')
        
        #report_sender.send_report('', '', c, [], [])
        
        print(report_sender.send_to_adm(template, '\n'.join(scilista_items)))
    else:
        f = open(config.parameters['CTRL_FILE'], 'w')
        f.write('off')
        f.close()

    
