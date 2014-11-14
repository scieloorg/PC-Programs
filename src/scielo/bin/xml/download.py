import os
import sys

import email_service
import ftp_service
import configuration


collection = sys.argv[1]
curr_path = os.path.dirname(__file__).replace('\\', '/')
config = configuration.Config(curr_path + '/./../config/' + collection + '.xmlproc.ini')

#CISIS_PATH=/bases/xml.000/proc/cisis
#JAVA_PATH=/usr/local/jre1.5.0_06/bin
#DB_ISSUE_FILENAME=/bases/xml.000/serial_proc/issue/issue
#COL_PROC_SERIAL_PATH=/bases/xml.000/xmldata/col/scl/4proc/serial
#XML_PATH=/bases/xml.000/xmldata/col/scl/4web/bases/xml
#PDF_PATH=/bases/xml.000/xmldata/col/scl/4web/bases/pdf
#IMG_PATH=/bases/xml.000/xmldata/col/scl/4web/htdocs/img
#COL_SCILISTA=/bases/xml.000/xmldata/col/scl/4proc/serial/scilista.lst
#EMAIL_SUBJECT_PREFIX=[SciELO-XML] [Brasil] XML evaluation report of
#EMAIL_TEXT=email.txt
#EMAIL_SUBJECT_WORK_PATH=[SciELO-XML] [Brasil] Packages not processed
#EMAIL_TEXT_WORK_PATH=/bases/xml.000/xmlproc/email_invalid_packages.txt

collection_download_path = config.data.get('DOWNLOAD_PATH')
collection_archive_path = config.data.get('DOWNLOAD_ARCHIVE_PATH')
collection_work_path = config.data.get('WORK_PATH')

email_to = config.data.get('BCC_EMAIL')

ftp_services = ftp_service.FTPService(config.data.get('FTP_SERVER'), config.data.get('FTP_USER'), config.data.get('FTP_PSWD'))

email_services = None
if config.data.get('IS_AVAILABLE_EMAIL_SERVICE') == 'yes':
    email_services = email_service.EmailService(config.data.get('SENDER_NAME'), config.data.get('SENDER_EMAIL'))

packages_files = ftp_services.download_files(config.data.get('FTP_DIR'), collection_download_path)

if len(packages_files) > 0:
    if email_services is not None:
        email_subject = config.data.get('EMAIL_SUBJECT_PREFIX_DOWNLOAD')
        email_text = config.data.get('EMAIL_TEXT_DOWNLOAD')
        email_text += ftp_service.registered_actions()
        email_service.send(email_to, email_subject, email_text)
