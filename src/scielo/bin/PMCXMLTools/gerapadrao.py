import os
import sys
import shutil
from datetime import date
    


from reuse.services.email_service.email_service import EmailService
from reuse.services.email_service.report_sender import ReportSender, MessageType

from reuse.input_output.configuration import Configuration
from reuse.input_output.report import Report
from reuse.input_output.parameters import Parameters
from reuse.input_output.tracker import Tracker

from reuse.db.isis.cisis import CISIS


# read parameters of execution 
parameter_list = ['script' ]         
parameters = Parameters(parameter_list)
if parameters.check_parameters(sys.argv):
    script_name, collection = sys.argv
    
    ####################################
    # Checking configuration and parameters
    valid_conf = False

    required = ['PROC_DB_TITLE_FILENAME', 'PROC_DB_ISSUE_FILENAME','SERIAL_PROC_PATH', 'COLLECTIONS_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']
        
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

        report_path = config.parameters['REPORT_PATH'] + '/' + date.today().isoformat()
        if not os.path.exists(report_path):
            os.makedirs(report_path)
    
        files = [ log_filename, err_filename, summary_filename]
    
        log_filename, err_filename, summary_filename = [ report_path + '/' + f for f in files ]
        report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
    
        proc_title_db = config.parameters['PROC_DB_TITLE_FILENAME']
        proc_issue_db = config.parameters['PROC_DB_ISSUE_FILENAME']

        cisis = CISIS(config.parameters['CISIS_PATH'])

        tracker = Tracker(config.parameter('GERAPADRAO_TRACKER_PATH'))
        email_service = EmailService('', config.parameter('SENDER_EMAIL'))
        message_type = MessageType(config.parameter('EMAIL_SUBJECT_PREFIX_GERAPADRAO'), config.parameter('EMAIL_TEXT_GERAPADRAO'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER'), config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        report_sender = ReportSender(report, config.parameter('IS_AVAILABLE_EMAIL_SERVICE'), email_service, config.parameter('BCC_EMAIL').split(','), message_type)



        tracker.register('GeraPadrao', 'preparation')

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
            
            for idfile in os.listdir(collection_serial_path + '/i'):
                cisis.id2mst(collection_serial_path + '/i/' + idfile, collection_serial_path + '/issue/issue')

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

        f = open(config.parameters['SERIAL_PROC_PATH'] + '/scilista.lst', 'r')
        c = f.read()
        f.close()
        

        
        tracker.register('Gerapadrao', c)
        os.system('cd ../proc;./GeraPadrao.bat')
        tracker.register('Gerapadrao', 'in progress')
            
        report_sender.send_report('', '', c, [], [])