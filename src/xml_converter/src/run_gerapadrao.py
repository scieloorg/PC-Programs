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

def is_allowed_to_run(control_filename):
    status = 'off'
    if control_filename != '':
        if os.path.exists(control_filename):
            f = open(control_filename, 'r')
            status = f.read()
            f.close()

            if 'off' in status:
                status = 'off'
            elif 'on' in status:
                status = 'on'

    return status

def change_status(control_filename, status):
    f = open(control_filename, 'w')
    f.write(status)
    f.close()

    

# read parameters of execution 
parameter_list = ['script', 'collection_acron' ]         
parameters = Parameters(parameter_list)
ALLOWED_TO_RUN = False

if parameters.check_parameters(sys.argv):
    script_name, collection_acron = sys.argv
    config_filename = collection_acron + '.gerapadrao.configuration.ini'
    
    ####################################
    # Checking configuration and parameters
    valid_conf = False

    required = ['PROC_DB_TITLE_FILENAME', 'PROC_DB_ISSUE_FILENAME','PROC_SERIAL_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']
        
    if os.path.exists(config_filename):
        config = Configuration(config_filename)
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

        cisis = CISIS(config.parameters['CISIS_PATH'])

        tracker = Tracker(config.parameter('GERAPADRAO_TRACKER_PATH'), config.parameter('GERAPADRAO_TRACKER_NAME'))
        
        email_service = EmailService('', config.parameter('SENDER_EMAIL'), 'localhost', config.parameter('IS_AVAILABLE_EMAIL_SERVICE') == 'yes')
        report_sender_config = ReportSenderConfiguration(config.parameter('BCC_EMAIL'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER') == 'yes', config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        report_sender = ReportSender(email_service, report_sender_config)
        template = EmailMessageTemplate(config.parameter('EMAIL_SUBJECT_PREFIX_GERAPADRAO'), config.parameter('EMAIL_TEXT_GERAPADRAO'))
        
        control_filename = config.parameters['CTRL_FILE']
        ALLOWED_TO_RUN = is_allowed_to_run(config.parameters['CTRL_FILE'])

        if ALLOWED_TO_RUN:
            change_status(control_filename, 'on')
            tracker.register('GeraPadrao', 'preparation')
        
            proc_scilista = config.parameters['PROC_SERIAL_PATH'] + '/scilista.lst'
            proc_scilista_del = config.parameters['PROC_SERIAL_PATH'] + '/scilista_del.lst'
    
            if os.path.isfile(proc_scilista_del):
                if os.path.isfile(proc_scilista):
                    f = open(proc_scilista, 'r')
                    scilista_items = f.read()
                    f.close()

                    f = open(proc_scilista_del, 'a+')
                    f.write(scilista_items)
                    f.close()

                    shutil.copyfile(proc_scilista_del, proc_scilista)
                    os.unlink(proc_scilista_del)

            if os.path.exists(proc_scilista):
                f = open(proc_scilista, 'r')
                scilista_items = f.readlines()
                f.close()
    
            if ''.join(scilista_items) != '':
    
                if os.path.exists(collection_acron + '.configuration.ini'):
                    collection_config = Configuration(collection_acron + '.configuration.ini')
                    collection_serial_path = collection_config.parameter('COL_PROC_SERIAL_PATH')
                    
                    if not os.path.exists(os.path.dirname(proc_title_db)):
                        os.makedirs(os.path.dirname(proc_title_db ))
                        
                    if not os.path.exists(os.path.dirname(proc_issue_db)):
                        os.makedirs(os.path.dirname(proc_issue_db ))
                    
        
                    ## TITLE
                    shutil.copyfile(collection_config.parameter('DB_TITLE_FILENAME') + '.mst', proc_title_db + '.mst')
                    shutil.copyfile(collection_config.parameter('DB_TITLE_FILENAME') + '.xrf', proc_title_db + '.xrf')
                        
                    ## ISSUE
                    shutil.copyfile(collection_config.parameter('DB_ISSUE_FILENAME') + '.mst', proc_issue_db + '.mst')
                    shutil.copyfile(collection_config.parameter('DB_ISSUE_FILENAME') + '.xrf', proc_issue_db + '.xrf')

                tracker.register('Gerapadrao', 'inicio')
                os.system(config.parameters['GENERATE_AND_PUBLISH'])
                tracker.register('Gerapadrao', 'fim')
                report_sender.send_to_adm(template, '\n'.join(scilista_items))

        
            else: 
                change_status(control_filename, 'off')
        
    
