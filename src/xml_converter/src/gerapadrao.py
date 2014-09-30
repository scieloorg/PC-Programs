import os
import sys
import shutil

from datetime import date, datetime

from reuse.files.name_file import return_path_based_on_date

from reuse.services.email_service.email_service import EmailService, EmailMessageTemplate
from reuse.services.email_service.report_sender_xml_process import ReportSender, ReportSenderConfiguration

from reuse.input_output.configuration import Configuration
from reuse.input_output.report import Report
from reuse.input_output.parameters import Parameters

from reuse.db.isis.cisis import CISIS


log_messages = []


def update_files_content(scilista_items, source, user_and_host, destination):
    # 'rsync -CrvK xmldata/col/scl/4web/htdocs/img/* roberta.takenaka@poseidon:/var/www/xml_scielo_br/htdocs/img/revistas'
    # source = xmldata/col/scl/4web
    # user_and_host = user@host
    # destination = /var/www/xml_scielo_br
    commands = []
    for item in scilista_items:
        issue_id_path = item.replace(' ', '/').replace('\n', '').replace('\r', '')
        dest_path = destination + '/htdocs/img/revistas/' + issue_id_path
        commands.append('ssh ' + user_and_host + ' "mkdir -p ' + dest_path + '"')
        commands.append('rsync -CrvK ' + source + '/htdocs/img/' + issue_id_path + '/* ' + user_and_host + ':' + dest_path)
        commands.append('rm -rf ' + source + '/htdocs/img/' + issue_id_path)

        dest_path = destination + '/bases/pdf/' + issue_id_path
        commands.append('ssh ' + user_and_host + ' "mkdir -p ' + dest_path + '"')
        commands.append('rsync -CrvK ' + source + '/bases/pdf/' + issue_id_path + '/* ' + user_and_host + ':' + dest_path)
        commands.append('rm -rf ' + source + '/bases/pdf/' + issue_id_path)

        dest_path = destination + '/bases/xml/' + issue_id_path
        commands.append('ssh ' + user_and_host + ' "mkdir -p ' + dest_path + '"')
        commands.append('rsync -CrvK ' + source + '/bases/xml/' + issue_id_path + '/* ' + user_and_host + ':' + dest_path)
        commands.append('rm -rf ' + source + '/bases/xml/' + issue_id_path)

    return '\n'.join(commands)


def get_status(ctrl_filename):
    status = 'finished'

    if ctrl_filename != '':
        if os.path.exists(ctrl_filename):
            content = open(ctrl_filename, 'r').read()
            if 'finished' in content:
                status = 'finished'
            elif 'running' in content:
                status = 'running'
            if 'off' in content:
                status = 'finished'
            elif 'on' in content:
                status = 'running'

    return status


def set_status(ctrl_filename, status):
    open(ctrl_filename, 'w').write(status)



# read parameters of execution 
parameter_list = ['script' ]         
parameters = Parameters(parameter_list)
doit = False


if parameters.check_parameters(sys.argv):
    ####################################
    # Checking configuration and parameters
    valid_conf = False

    required = ['PROC_DB_TITLE_FILENAME', 'PROC_DB_ISSUE_FILENAME', 'PROC_SERIAL_PATH', 'COLLECTIONS_PATH', 'CISIS_PATH', 'LOG_FILENAME', 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN']

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

        now = datetime.now().isoformat()[11:16].replace(':', '-')
        report_path = config.parameters['REPORT_PATH'] + '/' + now

        if not os.path.exists(report_path):
            os.makedirs(report_path)

        files = [log_filename, err_filename, summary_filename]

        log_filename, err_filename, summary_filename = [report_path + '/gerapadrao-' + f for f in files]
        report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes'))

        proc_title_db = config.parameters['PROC_DB_TITLE_FILENAME']
        proc_issue_db = config.parameters['PROC_DB_ISSUE_FILENAME']

        if not os.path.exists(os.path.dirname(proc_title_db)):
            os.makedirs(os.path.dirname(proc_title_db))

        if not os.path.exists(os.path.dirname(proc_issue_db)):
            os.makedirs(os.path.dirname(proc_issue_db))

        cisis = CISIS(config.parameters['CISIS_PATH'])
        email_service = EmailService('', config.parameter('SENDER_EMAIL'), 'localhost', config.parameter('IS_AVAILABLE_EMAIL_SERVICE') == 'yes')
        report_sender_config = ReportSenderConfiguration(config.parameter('BCC_EMAIL'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER') == 'yes', config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        report_sender = ReportSender(email_service, report_sender_config)
        template = EmailMessageTemplate(config.parameter('EMAIL_SUBJECT_PREFIX_GERAPADRAO'), config.parameter('EMAIL_TEXT_GERAPADRAO'))
        status = get_status(config.parameter('CTRL_FILE'))
        doit = (status == 'finished')

        if doit:
            set_status(config.parameter('CTRL_FILE'), 'running')
            report.write('Start', True, False, False)

            cisis.create('null count=0', proc_title_db)
            cisis.create('null count=0', proc_issue_db)
            proc_scilista = config.parameters['PROC_SERIAL_PATH'] + '/scilista.lst'
            proc_scilista_del = config.parameters['PROC_SERIAL_PATH'] + '/scilista_del.lst'

            path = config.parameters['COLLECTIONS_PATH']
            report.write('path of collections:' + path, True, False, False)

            all_the_scilista_items = []
            scilista_files = []

            for collection_folder in os.listdir(path):
                report.write(collection_folder, True, False, False)

                if os.path.exists(collection_folder + '.configuration.ini'):
                    collection_config = Configuration(collection_folder + '.configuration.ini')

                    collection_serial_path = collection_config.parameter('COL_PROC_SERIAL_PATH')
                    report.write('collection serial folder:' + collection_serial_path, True, False, False)

                    shutil.copyfile(collection_config.parameter('DB_TITLE_FILENAME') + '.mst', proc_title_db + '.mst')
                    shutil.copyfile(collection_config.parameter('DB_TITLE_FILENAME') + '.xrf', proc_title_db + '.xrf')
                    shutil.copyfile(collection_config.parameter('DB_ISSUE_FILENAME') + '.mst', proc_issue_db + '.mst')
                    shutil.copyfile(collection_config.parameter('DB_ISSUE_FILENAME') + '.xrf', proc_issue_db + '.xrf')

                    ## SCILISTA
                    report.write('collection scilista:' + collection_config.parameter('COL_SCILISTA'), True, False, False)

                    if os.path.exists(collection_config.parameter('COL_SCILISTA')):
                        col_scilista_items = [f.replace('\n', '').replace('\r', '') for f in open(collection_config.parameter('COL_SCILISTA'), 'r').readlines() if ' ' in f]
                        scilista_files.append(collection_config.parameter('COL_SCILISTA'))
                        all_the_scilista_items += col_scilista_items
                        report.write('collection scilista:' + '\n'.join(col_scilista_items), True, False, False)

                        if collection_serial_path != config.parameters['PROC_SERIAL_PATH']:
                            report.write(collection_serial_path, True, False, False)
                            report.write(config.parameters['PROC_SERIAL_PATH'], True, False, False)

                            for scilista_item in col_scilista_items:
                                acron, issue_folder = scilista_item.split(' ')

                                proc_issue_base_path = config.parameters['PROC_SERIAL_PATH'] + '/' + acron + '/' + issue_folder + '/base'
                                issue_base_path = collection_serial_path + '/' + acron + '/' + issue_folder + '/base'
                                report.write(scilista_item, True, False, False)

                                dbfiles = []
                                if os.path.exists(issue_base_path):
                                    dbfiles = os.listdir(issue_base_path)
                                if len(dbfiles) > 0:
                                    if not os.path.exists(proc_issue_base_path):
                                        os.makedirs(proc_issue_base_path)
                                    for dbfile in dbfiles:
                                        shutil.copyfile(issue_base_path + '/' + dbfile, proc_issue_base_path + '/' + dbfile)
                                    report.write(acron + ' ' + issue_folder + ' has ' + str(len(dbfiles)) + ' files', True, False, False)
                                else:
                                    report.write(acron + ' ' + issue_folder + ' has no files', True, False, False)

            if os.path.isfile(proc_scilista_del):
                all_the_scilista_items = open(proc_scilista_del, 'r').readlines() + all_the_scilista_items
                scilista_files.append(proc_scilista_del)

            all_the_scilista_items = list(set([f.replace('\n', '').replace('\r', '') for f in all_the_scilista_items if ' ' in f]))

            if len(all_the_scilista_items) > 0:
                for scilista_file in scilista_files:
                    if os.path.isfile(scilista_file):
                        os.unlink(scilista_file)

                open(proc_scilista, 'w').write('\n'.join(all_the_scilista_items + '\n'))

                report.write('scilista content:', True, False, False)
                report.write('.' + '\n'.join(all_the_scilista_items) + '\n.', True, False, False)
                report.write('---', True, False, False)
                report.write(open(proc_scilista, 'r').read(), True, False, False)
                report.write('---', True, False, False)
                report.write(config.parameters['RUN_GERAPADRAO_AND_UPDATE_BASES'], True, False, False)

                os.system(config.parameters['RUN_GERAPADRAO_AND_UPDATE_BASES'])

                try:
                    report.write('writing transf_files.sh', True, False, False)
                    open('./transf_files.sh', 'w').write(update_files_content(all_the_scilista_items, config.parameters['TRANSF_SOURCE'], config.parameters['USERATHOST'], config.parameters['TRANSF_DEST']))
                    report.write('chmod 777 ./transf_files.sh', True, False, False)
                    os.system('chmod 777 ./transf_files.sh')
                    report.write('./transf_files.sh', True, False, False)
                    os.system('./transf_files.sh')
                    report.write('tranferiu', True, False, False)
                except Exception as e:
                    report.write('deu erro', True, False, False)
                    report.write(str(e), True, False, False)

                report.write('set status as finished', True, False, False)
                set_status(config.parameters['CTRL_FILE'], 'finished')
                report.write('status:', True, False, False)
                report.write(get_status(config.parameters['CTRL_FILE']), True, False, False)
                report.write('envia email', True, False, False)
                print(report_sender.send_to_adm(template, '\n'.join(all_the_scilista_items)))
                report.write('fim', True, False, False)
            else:
                report.write('set status as finished. No item in scilista.', True, False, False)
                set_status(config.parameters['CTRL_FILE'], 'finished')
                report.write('status:', True, False, False)
                report.write(get_status(config.parameters['CTRL_FILE']), True, False, False)
                report.write('fim', True, False, False)
        else:
            report.write('start', True, False, False)
            report.write('end', True, False, False)
