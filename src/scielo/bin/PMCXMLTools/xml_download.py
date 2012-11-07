import os
import sys
import shutil
from datetime import date
    

from email_service.email_service import EmailService
from ftp_service.ftp_service import FTPService

from input_output.configuration import Configuration
from input_output.report import Report
from input_output.parameters import Parameters

from files.compressed_file import CompressedFile

from files_reception.reception import Reception

# read parameters of execution 
parameter_list = ['script', 'collection' ]         
parameters = Parameters(parameter_list)
if parameters.check_parameters(sys.argv):
    script_name, collection = sys.argv
    
    required = ['FTP_SERVER', 'FTP_USER', 'FTP_PSWD', 'FTP_DIR', 'FTP_PATH', 'QUEUE_PATH']

    required += ['SENDER_NAME', 'EMAIL_TEXT_DOWNLOAD' , 'EMAIL_SUBJECT_PREFIX_DOWNLOAD', 'FLAG_ATTACH_REPORTS','ALERT_FORWARD', 'IS_AVAILABLE_EMAIL_SERVICE', 'EMAIL_TEXT', 'SENDER_EMAIL', 'BCC_EMAIL', ]
    valid_conf = False
    if os.path.exists(collection + '.configuration.ini'):
        config = Configuration(collection + '.configuration.ini')
        valid_conf, msg = config.check(required)
    else:
        what_to_do = 'nothing'

        msg = 'There is no ' + collection + '.configuration.ini'
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
    
        log_filename, err_filename, summary_filename = [ report_path + '/ftp_' + f for f in files ]
        report_ftp = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
    
        work_path = config.parameters['WORK_PATH']
        download_path = config.parameters['FTP_PATH']


        email_data = {}
        email_data['SENDER_EMAIL'] = config.parameters['SENDER_EMAIL']
        email_data['BCC_EMAIL'] = config.parameters['BCC_EMAIL'].split(',')
        email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] = config.parameters['FLAG_SEND_EMAIL_TO_XML_PROVIDER']
        email_data['EMAIL_TEXT'] = config.parameters['EMAIL_TEXT_DOWNLOAD']
        email_data['IS_AVAILABLE_EMAIL_SERVICE'] = config.parameters['IS_AVAILABLE_EMAIL_SERVICE']
        email_data['ALERT_FORWARD'] = config.parameters['ALERT_FORWARD']
        email_data['FLAG_ATTACH_REPORTS'] = config.parameters['FLAG_ATTACH_REPORTS']
        email_data['EMAIL_SUBJECT_PREFIX'] = config.parameters['EMAIL_SUBJECT_PREFIX_DOWNLOAD']
        
        email_data['XML_PROVIDER_EMAIL'] = ''

        server = config.parameters['FTP_SERVER']
        user = config.parameters['FTP_USER']
        pasw = config.parameters['FTP_PSWD']
        folder = config.parameters['FTP_DIR']
    
        fservice = FTPService(report_ftp, server, user, pasw)
        compressed_file = CompressedFile(self.report)
        
        email_service = EmailService('', email_data['SENDER_EMAIL'])

        report_sender = ReportSender(email_service, email_data)

        reception = Reception(report_ftp)
        reception.download_files(fservice, folder, download_path)
        reception.extract_files(compressed_file, download_path, work_path, work_path + '.bkp', report_sender)

            