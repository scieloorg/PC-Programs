# coding=utf-8
import os
import shutil


CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')
CONFIG_PATH = CURRENT_PATH + '/../config/'


class XMLConverterConfiguration(object):

    def __init__(self, filename):
        self._data = {}
        for item in open(filename, 'r').readlines():
            s = item.strip()
            if '=' in s:
                if ',' in s:
                    s = s[0:s.rfind(',')]
                key, value = s.split('=')
                value = value.replace('\\', '/').strip()
                if value == '':
                    self._data[key] = None
                else:
                    self._data[key] = value
                if 'PATH' in key:
                    if not os.path.isdir(value):
                        os.makedirs(value)
        self.is_windows = self._data.get('Serial Directory') is not None

    @property
    def cisis1030(self):
        return self._data.get('PATH_CISIS', CURRENT_PATH + '/../../cfg/')

    @property
    def cisis1660(self):
        return self._data.get('PATH_CISIS', CURRENT_PATH + '/../../cfg/cisis1660/')

    @property
    def web_app_path(self):
        path = self._data.get('SCI_LISTA_SITE')
        if path is not None:
            path = path.replace('\\', '/')
            if '/proc/' in path:
                path = path[0:path.find('/proc/')]
        if path is None:
            path = self._data.get('WEB_APP_PATH')
        return path

    @property
    def serial_path(self):
        return self._data.get('PROC_SERIAL_PATH', self._data.get('Serial Directory'))

    @property
    def issue_db(self):
        return self._data.get('SOURCE_ISSUE_DB', self._data.get('Issue Database'))

    @property
    def issue_db_copy(self):
        copy = self._data.get('Issue Database')
        if copy is not None:
            copy = copy.replace('/issue/', '/issue.tmp/')
        return self._data.get('ISSUE_DB_COPY', copy)

    @property
    def update_title_and_issue(self):
        for item in [self._data.get('SOURCE_TITLE_DB'), self._data.get('SOURCE_ISSUE_DB')]:
            for ext in ['.mst', '.xrf']:
                if os.path.isfile(item + ext):
                    name = os.path.basename(item)
                    itemdirs = self.serial_path + '/' + name
                    if not os.path.isdir(itemdirs):
                        os.makedirs(itemdirs)
                    shutil.copyfile(item + ext, itemdirs + '/' + name + ext)
                    print('updating:')
                    print(item + ext)
                    print(' ==> ' + itemdirs + '/' + name + ext)
                else:
                    print('WARNING: Unable to find ' + item + ext)

    @property
    def valid(self):
        r = True
        if not os.path.isdir(self.cisis1030):
            r = False
            print('ERROR: Unable to find ' + self.cisis1030)
        if not os.path.isdir(self.cisis1660):
            r = False
            print('ERROR: Unable to find ' + self.cisis1660)
        if not os.path.isfile(self.issue_db + '.mst'):
            r = False
            print('ERROR: Unable to find ' + self.issue_db + '.mst')
        if not os.path.isdir(self.web_app_path):
            print('WARNING: Unable to find ' + self.web_app_path)
        if not os.path.isdir(self.serial_path):
            r = False
            print('ERROR: Unable to find ' + self.serial_path)
        if not self.is_windows:
            if self.download_path is None:
                r = False
                print('ERROR: Missing DOWNLOAD_PATH')
            if self.temp_path is None:
                r = False
                print('ERROR: Missing TEMP_PATH')
            if self.queue_path is None:
                r = False
                print('ERROR: Missing QUEUE_PATH')
            if self.archive_path is None:
                r = False
                print('ERROR: Missing ARCHIVE_PATH')
            if self.collection_scilista is None:
                r = False
                print('ERROR: Missing COL_SCILISTA')
            if not self.is_available_email_service:
                r = False
            if not self.is_available_download:
                r = False
        return r

    @property
    def collection_scilista(self):
        if self._data.get('COL_SCILISTA') != self.gerapadrao_scilista:
            return self._data.get('COL_SCILISTA')
        else:
            return self._data.get('COL_SCILISTA') + '.collection'

    @property
    def is_available_gerapadrao(self):
        return self.gerapadrao_status == 'on' and self.is_valid_gerapadrao_configuration

    @property
    def gerapadrao_status(self):
        return self._data.get('GERAPADRAO_STATUS')

    @property
    def gerapadrao_permission_file(self):
        return self._data.get('GERAPADRAO_PERMISSION')

    @property
    def gerapadrao_proc_path(self):
        return self._data.get('PROC_PATH')

    @property
    def gerapadrao_scilista(self):
        return self.serial_path + '/scilista.lst' if self.serial_path is not None else None

    @property
    def download_path(self):
        return self._data.get('DOWNLOAD_PATH')

    @property
    def temp_path(self):
        return self._data.get('TEMP_PATH')

    @property
    def queue_path(self):
        return self._data.get('QUEUE_PATH')

    @property
    def archive_path(self):
        return self._data.get('ARCHIVE_PATH')

    @property
    def is_available_email_service(self):
        is_on = False
        if self._data('EMAIL_SERVICE_STATUS') == 'on':
            errors = self.is_valid_email_configuration()
            if len(errors) > 0:
                print('\n'.join(errors))
            else:
                is_on = True
        return is_on

    @property
    def email_sender_name(self):
        return self._data('SENDER_NAME')

    @property
    def email_sender_email(self):
        return self._data('SENDER_EMAIL')

    @property
    def email_to(self):
        return self._data('EMAIL_TO')

    @property
    def email_subject_packages_receipt(self):
        return self._data('EMAIL_SUBJECT_PACKAGES_RECEIPT')

    @property
    def email_subject_invalid_packages(self):
        return self._data('EMAIL_SUBJECT_INVALID_PACKAGES')

    @property
    def email_subject_package_evaluation(self):
        return self._data('EMAIL_SUBJECT_PACKAGE_EVALUATION')

    @property
    def email_subject_gerapadrao(self):
        return self._data('EMAIL_SUBJECT_GERAPADRAO')

    @property
    def email_text_packages_receipt(self):
        return self.email_header(self._data('EMAIL_TEXT_PACKAGES_RECEIPT'))

    @property
    def email_text_invalid_packages(self):
        return self.email_header(self._data('EMAIL_TEXT_INVALID_PACKAGES'))

    @property
    def email_text_package_evaluation(self):
        return self.email_header(self._data('EMAIL_TEXT_PACKAGE_EVALUATION'))

    @property
    def email_text_gerapadrao(self):
        return self.email_header(self._data('EMAIL_TEXT_GERAPADRAO'))

    @property
    def ftp_server(self):
        return self._data('FTP_SERVER')

    @property
    def ftp_user(self):
        return self._data('FTP_USER')

    @property
    def ftp_pswd(self):
        return self._data('FTP_PSWD')

    @property
    def ftp_dir(self):
        return self._data('FTP_DIR')

    @property
    def email_header(self, filename):
        header = ''
        if filename is not None:
            filename = CONFIG_PATH + '/' + filename
            if os.path.isfile(filename):
                header = open(filename, 'r').read()
        return header

    @property
    def is_valid_email_configuration(self):
        errors = []
        if self.email_sender_name is None:
            errors.append('Missing SENDER_NAME')
        if self.email_sender_email is None:
            errors.append('Missing SENDER_EMAIL')
        if self.email_to is None:
            errors.append('Missing EMAIL_TO')

        if self.email_subject_packages_receipt is None:
            errors.append('Missing EMAIL_SUBJECT_PACKAGES_RECEIPT')
        if self.email_subject_invalid_packages is None:
            errors.append('Missing EMAIL_SUBJECT_INVALID_PACKAGES')
        if self.email_subject_package_evaluation is None:
            errors.append('Missing EMAIL_SUBJECT_PACKAGE_EVALUATION')
        if self.email_subject_gerapadrao is None:
            errors.append('Missing EMAIL_SUBJECT_GERAPADRAO')
        return errors

    @property
    def is_valid_gerapadrao_configuration(self):
        errors = []
        if self.gerapadrao_permission_file is None:
            errors.append('Missing GERAPADRAO_PERMISSION')
        if self.gerapadrao_proc_path is None:
            errors.append('Missing PROC_PATH')
        if self.gerapadrao_scilista is None:
            errors.append('Missing PROC_SERIAL_PATH')
        if self.collection_scilista is None:
            errors.append('Missing COL_SCILISTA')
        return errors

    @property
    def is_valid_transference_configuration(self):
        errors = []
        if self.web_app_path is None:
            errors.append('Missing WEB_APP_PATH')
        return errors
