import os
import sys
import shutil
from datetime import date
    

from reuse.services.email_service.email_service import EmailService
from reuse.services.email_service.report_sender import ReportSender, MessageType

from reuse.services.ftp_service.ftp_service import FTPService

from reuse.input_output.configuration import Configuration
from reuse.input_output.report import Report
from reuse.input_output.parameters import Parameters
from reuse.input_output.tracker import Tracker


from reuse.downloader.downloader import Downloader

from reuse.files.name_file import return_path_based_on_date

# read parameters of execution 
parameter_list = ['script', 'collection' ]         
parameters = Parameters(parameter_list)
if parameters.check_parameters(sys.argv):
    script_name, collection = sys.argv
    
    required = ['FTP_SERVER', 'FTP_USER', 'FTP_PSWD', 'FTP_DIR', 'DOWNLOAD_PATH', 'WORK_PATH', 'DOWNLOAD_ARCHIVE_PATH']

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

         
        report_path = config.parameters['REPORT_PATH'] + '/' + return_path_based_on_date()
        if not os.path.exists(report_path):
            os.makedirs(report_path)
    
        files = [ log_filename, err_filename, summary_filename]
    
        log_filename, err_filename, summary_filename = [ report_path + '/ftp_' + f for f in files ]
        report_ftp = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
    
        work_path = config.parameters['WORK_PATH']
        download_path = config.parameters['DOWNLOAD_PATH']


        server = config.parameter('FTP_SERVER')
        user = config.parameter('FTP_USER')
        pasw = config.parameter('FTP_PSWD')
        folder = config.parameter('FTP_DIR')
    
       
        

        fservice = FTPService(report_ftp, server, user, pasw)
        tracker = Tracker(config.parameter('DOWNLOAD_TRACKER_PATH'), config.parameter('DOWNLOAD_TRACKER_NAME'))
        email_service = EmailService('', config.parameter('SENDER_EMAIL'))
        
        message_type = MessageType(config.parameter('EMAIL_SUBJECT_PREFIX_DOWNLOAD'), config.parameter('EMAIL_TEXT_DOWNLOAD'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER'), config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        report_sender = ReportSender(report_ftp, config.parameter('IS_AVAILABLE_EMAIL_SERVICE'), email_service, config.parameter('BCC_EMAIL').split(','), message_type)

        
        downloader = Downloader(report_ftp, tracker, download_path)
        downloader.download(fservice, folder,  True)
        
