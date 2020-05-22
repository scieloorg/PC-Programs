# coding=utf-8
import os
import shutil

from ...generics import fs_utils
from ...generics import encoding
from ...generics.ws import ws_requester

from ...__init__ import XC_SERVER_CONFIG_PATH
from ...__init__ import BIN_PATH
from ...__init__ import EMAIL_TEMPLATE_MESSAGES_PATH


def get_configuration_filename(collection_acron=None):
    filename = None
    if collection_acron is None:
        f = os.path.join(BIN_PATH, 'scielo_paths.ini')
        if os.path.isfile(f):
            filename = f
    else:
        filename = os.path.join(
            XC_SERVER_CONFIG_PATH, collection_acron + '.xc.ini')

    return filename


class Configuration(object):

    def __init__(self, filename=None):
        self.filename = filename
        if filename is None:
            self.filename = get_configuration_filename()
        if self.filename is not None and not os.path.isfile(self.filename):
            encoding.display_message('Not found {}'.format(self.filename))
            self.filename = None
        self.load()

    def load(self):
        self._data = {}
        config_items = []
        for item in ['scielo_env.ini', 'scielo_collection.ini']:
            if os.path.isfile(os.path.join(BIN_PATH, item)):
                config_items += fs_utils.read_file_lines(
                    os.path.join(BIN_PATH, item))

        if self.filename is not None:
            coding = 'utf-8'
            if self.filename.endswith('scielo_paths.ini'):
                coding = 'iso-8859-1'
            config_items.extend(
                fs_utils.read_file_lines(self.filename, coding))
        for item in config_items:
            if '=' in item:
                if ',' in item and '@' not in item:
                    item = item[0:item.rfind(',')]
                key, value = item.split('=')
                value = value.replace('\\', '/').strip()
                if value == '':
                    self._data[key] = None
                else:
                    self._data[key] = value
        self.interative_mode = self._data.get('Serial Directory') is not None
        self.is_windows = self.interative_mode

    @property
    def cisis1030(self):
        return self._data.get('PATH_CISIS_1030', os.path.join(BIN_PATH, 'cfg'))

    @property
    def cisis1660(self):
        return self._data.get(
            'PATH_CISIS_1660', os.path.join(BIN_PATH, 'cfg', 'cisis1660'))

    @property
    def local_web_app_path(self):
        path = self._data.get('SCI_LISTA_SITE')
        if path is not None:
            path = path.replace('\\', '/')
            if '/proc/' in path:
                path = path[0:path.find('/proc/')]
        if path is None:
            path = self._data.get('LOCAL_WEB_APP_PATH')
        return path

    @property
    def kernel_gate(self):
        return {key[3:].lower(): self._data.get(key)
                for key in self._data.keys()
                if key.startswith("KG_")
                }

    @property
    def remote_web_app_path(self):
        return self._data.get('REMOTE_WEB_APP_PATH')

    @property
    def serial_path(self):
        return self._data.get('PROC_SERIAL_PATH', self._data.get('Serial Directory'))

    @property
    def pid_manager_info(self):
        return self._data.get(
            'PID_MANAGER',
            os.path.join(self.serial_path, "pid_manager.db"))

    @property
    def issue_db(self):
        return self._data.get('SOURCE_ISSUE_DB', self._data.get('Issue Database'))

    @property
    def issue_db_copy(self):
        copy = self._data.get('Issue Database')
        if copy is not None:
            copy = copy.lower().replace('\\', '/')
            copy = copy.replace('/issue/', '/issue.tmp/')
        return self._data.get('ISSUE_DB_COPY', copy)

    @property
    def title_db(self):
        return self._data.get('SOURCE_TITLE_DB', self._data.get('Title Database'))

    @property
    def title_db_copy(self):
        copy = self._data.get('Title Database')
        if copy is not None:
            copy = copy.lower().replace('\\', '/')
            copy = copy.replace('/title/', '/title.tmp/')
        return self._data.get('TITLE_DB_COPY', copy)

    @property
    def max_fatal_error(self):
        return self._data.get('MAX_FATAL_ERROR')

    @property
    def max_error(self):
        return self._data.get('MAX_ERROR')

    @property
    def max_warning(self):
        return self._data.get('MAX_WARNING')

    def update_title_and_issue(self):
        for item in [self._data.get('SOURCE_TITLE_DB'), self._data.get('SOURCE_ISSUE_DB')]:
            for ext in ['.mst', '.xrf']:
                if os.path.isfile(item + ext):
                    name = os.path.basename(item)
                    itemdirs = os.path.join(self.serial_path, name)
                    if not os.path.isdir(itemdirs):
                        os.makedirs(itemdirs)
                    shutil.copyfile(
                        item + ext, os.path.join(itemdirs, name + ext))
                    encoding.debugging('update_title_and_issue', 'updating:')
                    encoding.debugging('update_title_and_issue', item + ext)
                    encoding.debugging('update_title_and_issue', ' ==> ' + itemdirs + '/' + name + ext)
                else:
                    encoding.debugging('update_title_and_issue', 'WARNING: Unable to find ' + item + ext)

    @property
    def valid(self):
        problems = []
        if self.cisis1030 is None:
            problems.append('ERROR: Missing cisis1030')
        else:
            if not os.path.isdir(self.cisis1030):
                problems.append('ERROR: Unable to find ' + self.cisis1030)
        if self.cisis1660 is None:
            problems.append('ERROR: Missing cisis1660')
        else:
            if not os.path.isdir(self.cisis1660):
                problems.append('ERROR: Unable to find ' + self.cisis1660)

        if self.issue_db is None:
            problems.append('ERROR: Missing SOURCE_ISSUE_DB or Issue Database')
        else:
            if not os.path.isfile(self.issue_db + '.mst'):
                problems.append('ERROR: Unable to find ' + self.issue_db + '.mst')

        if self.title_db is None:
            problems.append('ERROR: Missing SOURCE_TITLE_DB or Title Database')
        else:
            if not os.path.isfile(self.title_db + '.mst'):
                problems.append('ERROR: Unable to find ' + self.title_db + '.mst')

        if self.issue_db_copy is None:
            problems.append('ERROR: Missing ISSUE_DB_COPY or Issue Database')

        if self.title_db_copy is None:
            problems.append('ERROR: Missing TITLE_DB_COPY or Title Database')

        if self.local_web_app_path is None:
            problems.append('ERROR: Missing LOCAL_WEB_APP_PATH')
        else:
            if not os.path.isdir(self.local_web_app_path):
                problems.append('WARNING: Unable to find ' + self.local_web_app_path)

        if self.serial_path is None:
            problems.append('ERROR: Missing PROC_SERIAL_PATH or Serial Directory')
        else:
            if not os.path.isdir(self.serial_path):
                problems.append('ERROR: Unable to find ' + self.serial_path)
        if not self.interative_mode:
            if not self.is_enabled_package_receipt:
                problems.append('WARNING: Package receipt is not enabled.')
            if not self.is_enabled_email_service:
                problems.append('WARNING: Email service is not enabled.')
            if not self.is_enabled_gerapadrao:
                problems.append('WARNING: Gerapadrao is not enabled.')
            if not self.is_enabled_transference:
                problems.append('WARNING: Files Transference is not enabled.')
        encoding.display_message('\n'.join(problems))
        errors = [e for e in problems if 'ERROR:' in e]
        return len(errors) == 0

    @property
    def skip_identical_xml(self):
        return self._data.get('SKIP_IDENTICAL_XML', 'no') == 'yes'

    @property
    def web_app_site(self):
        return self._data.get('WEB_APP_SITE')

    @property
    def collection_scilista(self):
        if self._data.get('COL_SCILISTA') != self.gerapadrao_scilista:
            return self._data.get('COL_SCILISTA')
        else:
            return self._data.get('COL_SCILISTA') + '.collection'

    @property
    def gerapadrao_script(self):
        return self._data.get('GERAPADRAO_SCRIPT')

    @property
    def gerapadrao_permission_file(self):
        return self._data.get('GERAPADRAO_PERMISSION')

    @property
    def gerapadrao_proc_path(self):
        return self._data.get('PROC_PATH')

    @property
    def gerapadrao_scilista(self):
        if self.serial_path:
            return os.path.join(self.serial_path, 'scilista.lst')

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
    def email_sender_name(self):
        return self._data.get('SENDER_NAME')

    @property
    def email_sender_email(self):
        return self._data.get('SENDER_EMAIL')

    @property
    def email_to_adm(self):
        return self._data.get('EMAIL_TO_ADM')

    @property
    def email_to(self):
        return self._data.get('EMAIL_TO')

    @property
    def email_subject_packages_receipt(self):
        return self._data.get('EMAIL_SUBJECT_PACKAGES_RECEIPT')

    @property
    def email_subject_invalid_packages(self):
        return self._data.get('EMAIL_SUBJECT_INVALID_PACKAGES')

    @property
    def email_subject_package_evaluation(self):
        return self._data.get('EMAIL_SUBJECT_PACKAGE_EVALUATION')

    @property
    def email_subject_gerapadrao(self):
        return self._data.get('EMAIL_SUBJECT_GERAPADRAO')

    @property
    def email_subject_website_update(self):
        return self._data.get('EMAIL_SUBJECT_WEBSITE')

    @property
    def email_text_packages_receipt(self):
        return self.email_header(self._data.get('EMAIL_TEXT_PACKAGES_RECEIPT'))

    @property
    def email_text_invalid_packages(self):
        return self.email_header(self._data.get('EMAIL_TEXT_INVALID_PACKAGES'))

    @property
    def email_text_package_evaluation(self):
        return self.email_header(self._data.get('EMAIL_TEXT_PACKAGE_EVALUATION'))

    @property
    def email_text_gerapadrao(self):
        return self.email_header(self._data.get('EMAIL_TEXT_GERAPADRAO'))

    @property
    def email_text_website_update(self):
        return self.email_header(self._data.get('EMAIL_TEXT_WEBSITE'))

    @property
    def ftp_server(self):
        return self._data.get('FTP_SERVER')

    @property
    def ftp_user(self):
        return self._data.get('FTP_USER')

    @property
    def ftp_pswd(self):
        return self._data.get('FTP_PSWD')

    @property
    def ftp_dir(self):
        return self._data.get('FTP_DIR')

    def email_header(self, filename):
        header = ''
        if filename is not None:
            filename = os.path.join(EMAIL_TEMPLATE_MESSAGES_PATH, filename)
            header = fs_utils.read_file(filename)
        return header

    @property
    def transference_user(self):
        return self._data.get('TRANSFER_USER')

    @property
    def transference_servers(self):
        servers = self._data.get('TRANSFER_SERVER')
        if servers is not None:
            servers = servers.split(';')
        return servers

    @property
    def is_enabled_email_service(self):
        return self.is_activated('EMAIL_SERVICE_STATUS') and self.is_valid_email_configuration

    @property
    def is_enabled_package_receipt(self):
        return self.is_activated('RECEIPT_STATUS') and self.is_valid_package_receipt_configuration

    @property
    def is_enabled_gerapadrao(self):
        return self.is_activated('GERAPADRAO_STATUS') and self.is_valid_gerapadrao_configuration

    @property
    def is_enabled_transference(self):
        return self.is_activated('TRANSFERENCE_STATUS') and self.is_valid_transference_configuration

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
        encoding.display_message('\n'.join(errors))
        return len(errors) == 0

    @property
    def is_valid_package_receipt_configuration(self):
        errors = []
        if self.ftp_dir is None:
            errors.append('Missing FTP_DIR')
        if self.ftp_user is None:
            errors.append('Missing FTP_USER')
        if self.ftp_server is None:
            errors.append('Missing FTP_SERVER')
        if self.ftp_pswd is None:
            errors.append('Missing FTP_PASSWORD')
        if self.temp_path is None:
            errors.append('Missing TEMP_PATH')
        if self.queue_path is None:
            errors.append('Missing QUEUE_PATH')
        if self.download_path is None:
            errors.append('Missing DOWNLOAD_PATH')
        encoding.display_message('\n'.join(errors))
        return len(errors) == 0

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
        if self._data.get('SOURCE_TITLE_DB') is None:
            errors.append('Missing SOURCE_TITLE_DB')
        if self._data.get('SOURCE_ISSUE_DB') is None:
            errors.append('Missing SOURCE_ISSUE_DB')
        encoding.display_message('\n'.join(errors))
        return len(errors) == 0

    @property
    def is_valid_transference_configuration(self):
        errors = []
        if self.local_web_app_path is None:
            errors.append('Missing LOCAL_WEB_APP_PATH')
        if self.remote_web_app_path is None:
            errors.append('Missing REMOTE_WEB_APP_PATH')
        if self.transference_servers is None:
            errors.append('Missing TRANSFER_SERVER')
        if self.transference_user is None:
            errors.append('Missing TRANSFER_USER')
        if self.web_app_site is None:
            errors.append('Missing WEB_APP_SITE')
        encoding.display_message('\n'.join(errors))
        return len(errors) == 0

    @property
    def is_web_access_enabled(self):
        return self.is_activated('ENABLED_WEB_ACCESS')

    @property
    def proxy_info(self):
        return self._data.get('PROXY_ADDRESS')

    @property
    def app_ws_requester(self):
        if self.is_web_access_enabled is False:
            encoding.display_message('ENABLED_WEB_ACCESS=off')
        return ws_requester.WebServicesRequester(self.is_web_access_enabled, self.proxy_info)

    @property
    def xml_structure_validator_preference(self):
        preference = self._data.get('XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER', 'packtools').split('|')
        encoding.display_message(preference)
        return preference

    @property
    def coded_formula_required(self):
        return self.is_activated('CODED_FORMULA_REQUIRED')

    @property
    def coded_table_required(self):
        return self.is_activated('CODED_TABLE_REQUIRED')

    @property
    def BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA(self):
        return self.is_activated('BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA')

    def is_activated(self, label, default='TRUE'):
        return self._data.get(label, default).upper() in ['ON', 'TRUE', 'YES']
