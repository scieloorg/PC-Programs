# coding=utf-8

import os
import shutil
from datetime import datetime

from . import email_service

from __init__ import _
from . import validation_status
from . import fs_utils
from . import utils
from . import html_reports
from . import xml_utils
from . import xc_config


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

CONFIG_PATH = CURRENT_PATH + '/../config/'
converter_env = None

ALTERNATIVE_WEB_PATH = os.path.dirname(os.path.dirname(CURRENT_PATH)) + '/web'


categories_messages = {
    'converted': _('converted'), 
    'rejected': _('rejected'), 
    'not converted': _('not converted'), 
    'skipped': _('skipped conversion'), 
    'excluded ex-aop': _('excluded ex-aop'), 
    'excluded incorrect order': _('excluded incorrect order'), 
    'not excluded incorrect order': _('not excluded incorrect order'), 
    'not excluded ex-aop': _('not excluded ex-aop'), 
    'new aop': _('aop version'), 
    'regular doc': _('doc has no aop'), 
    'ex aop': _('aop is published in an issue'), 
    'matched aop': _('doc has aop version'), 
    'partially matched aop': _('doc has aop version partially matched (title/author are similar)'), 
    'aop missing PID': _('doc has aop version which has no PID'), 
    'unmatched aop': _('doc has an invalid aop version (title/author are not the same)'), 
}

CONVERSIONS_STATUS = ['converted', 'not converted', 'rejected', 'skipped', 'excluded incorrect order', 'not excluded incorrect order']

EMAIL_SUBJECT_STATUS_ICON = {}
EMAIL_SUBJECT_STATUS_ICON['rejected'] = [u"\u274C", _(' REJECTED ')]
EMAIL_SUBJECT_STATUS_ICON['ignored'] = ['', _('IGNORED')]
EMAIL_SUBJECT_STATUS_ICON['accepted'] = [u"\u2713" + ' ' + u"\u270D", _(' ACCEPTED but corrections required ')]
EMAIL_SUBJECT_STATUS_ICON['approved'] = [u"\u2705", _(' APPROVED ')]
EMAIL_SUBJECT_STATUS_ICON['not processed'] = ['', _(' NOT PROCESSED ')]


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


def xc_get_configuration(collection_acron):
    config = None
    f = xc_configuration_filename(collection_acron)
    errors = is_xc_configuration_file(f)
    if len(errors) > 0:
        print('\n'.join(errors))
    else:
        config = xc_read_configuration_file(f)
    return config


def xc_read_configuration_file(filename):
    r = None
    if os.path.isfile(filename):
        r = xc_config.XMLConverterConfiguration(filename)
        if not r.valid:
            r = None
    return r


def xc_configuration_filename(collection_acron):
    if collection_acron is None:
        f = CURRENT_PATH + '/../../scielo_paths.ini'
        if os.path.isfile(f):
            filename = f
        else:
            filename = CURRENT_PATH + '/../config/default.xc.ini'
    else:
        filename = CURRENT_PATH + '/../config/' + collection_acron + '.xc.ini'

    return filename


def is_xc_configuration_file(configuration_filename):
    messages = []
    if configuration_filename is None:
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: No configuration file was informed')
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: unable to read the configuration file: ' + configuration_filename)
    return messages


def run_cmd(cmd, log_filename=None):
    print(cmd)
    if log_filename is not None:
        fs_utils.append_file(log_filename, datetime.now().isoformat() + ' ' + cmd)
    try:
        os.system(cmd)
        if log_filename is not None:
            fs_utils.append_file(log_filename, 'done')
    except:
        if log_filename is not None:
            fs_utils.append_file(log_filename, 'failure')


def run_remote_mkdirs(user, server, path, log_filename=None):
    cmd = 'ssh ' + user + '@' + server + ' "mkdir -p ' + path + '"'
    run_cmd(cmd, log_filename)


def run_rsync(source, user, server, dest, log_filename=None):
    cmd = 'nohup rsync -CrvK ' + source + '/* ' + user + '@' + server + ':' + dest + '&\n'
    run_cmd(cmd, log_filename)


def run_scp(source, user, server, dest, log_filename=None):
    cmd = 'nohup scp -r ' + source + ' ' + user + '@' + server + ':' + dest + '&\n'
    run_cmd(cmd, log_filename)


def call_converter(args, version='1.0'):
    script, package_path, collection_acron = read_inputs(args)
    if package_path is None and collection_acron is None:
        # FIXME
        # GUI
        import xml_gui
        xml_gui.open_main_window(True, None)

    elif package_path is not None and collection_acron is not None:
        errors = validate_inputs(package_path, collection_acron)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
            messages.append(validation_status.STATUS_ERROR + ': ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python xml_converter.py <xml_folder> | <collection_acron>')
            messages.append(_('where') + ':')
            messages.append('  <xml_folder> = ' + _('path of folder which contains'))
            messages.append('  <collection_acron> = ' + _('collection acron'))
            messages.append('\n'.join(errors))
            utils.display_message('\n'.join(messages))
        else:
            execute_converter(package_path, collection_acron)
    elif collection_acron is not None:
        execute_converter(package_path, collection_acron)
    elif package_path is not None:
        execute_converter(package_path)


def read_inputs(args):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    package_path = None
    script = None
    collection_acron = None
    if len(args) == 2:
        script, param = args
        if os.path.isfile(param) or os.path.isdir(param):
            package_path = param
        else:
            collection_acron = param

    return (script, package_path, collection_acron)


def validate_inputs(package_path, collection_acron):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    errors = []
    if package_path is None:
        if collection_acron is None:
            errors.append(_('Missing collection acronym'))
    else:
        errors = xml_utils.is_valid_xml_path(package_path)
    return errors


def get_config(collection_name):
    collection_names = {}
    collection_acron = collection_names.get(collection_name)
    if collection_acron is None:
        collection_acron = collection_name
    #FIXME
    return xc.xc_get_configuration(collection_acron)


def organize_packages_locations(pkg_path, config, mailer):
    if pkg_path is None:
        pkg_path, invalid_pkg_files = queue_packages(config.download_path, config.temp_path, config.queue_path, config.archive_path)
    if pkg_path is None:
        pkg_path = []
    if not isinstance(pkg_path, list):
        pkg_path = [pkg_path]
    if len(invalid_pkg_files) > 0:
        mailer.mail_invalid_packages(invalid_pkg_files)


def execute_converter(package_paths, collection_name):
    config = get_config(collection_name)
    mailer = Mailer(config)
    transfer = FilesTransfer(config)
    organize_packages_locations(package_paths, config, mailer)

    proc = PkgProcessor(config, version, DISPLAY_REPORT, GENERATE_PMC, stage)
    scilista_items = []
    for package_path in package_paths:
        package_name = os.path.basename(package_path)
        utils.display_message(package_path)
        xc_status = 'interrupted'
        stats_msg = ''
        report_location = None

        pkgfolder = workarea.PackageFolder(package_path)
        pkgfiles = package.normalize_xml_packages(pkgfolder.xml_list, 'xc')

        try:
            scilista_items, xc_status, stats_msg, report_location = proc.convert_package([f.filename for f in pkgfiles])
            print(scilista_items)
        except Exception as e:
            if config.queue_path is not None:
                fs_utils.delete_file_or_folder(package_path)
            mailer.mail_step1_failure(package_name, e)
            if len(package_paths) == 1:
                raise
        if len(scilista_items) > 0:
            acron, issue_id = scilista_items[0].split(' ')
            try:
                if xc_status in ['accepted', 'approved']:
                    if config.collection_scilista is not None:
                        fs_utils.append_file(config.collection_scilista, '\n'.join(scilista_items) + '\n')
                    transfer.transfer_website_files(acron, issue_id)
            except Exception as e:
                mailer.mail_step2_failure(package_name, e)
                if len(package_paths) == 1:
                    print('exception as step 2')
                    raise
            try:
                if report_location is not None and config.email_subject_package_evaluation is not None:
                    results = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(xc_status, [])) + ' ' + stats_msg
                    link = config.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
                    mail_content = '<html><body>' + html_reports.link(link, link) + '</body></html>'
                    transfer.transfer_report_files(acron, issue_id)
                    mailer.mail_results(package_name, results, mail_content)
            except Exception as e:
                mailer.mail_step3_failure(package_name, e)
                if len(package_paths) == 1:
                    print('exception as step 3')
                    raise
    utils.display_message(_('finished'))
    """
    if tmp_result_path != conversion.results_path:
        fs_utils.delete_file_or_folder(tmp_result_path)
    os.unlink(log_package)
    """


class Mailer(object):

    def __init__(self, config):
        self.config = config
        self.mailer = email_service.EmailService(config.email_sender_name, config.email_sender_email)

    def send_message(self, to, subject, text, attaches):
        if self.mailer is not None:
            self.mailer.send_message(to, subject, text, attaches)

    def mail_invalid_packages(self, invalid_pkg_files):
        self.send_message(self.config.email_to, self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n'.join(invalid_pkg_files))

    def mail_step1_failure(self, package_folder, e):
        self.send_message(self.config.email_to_adm, '[Step 1]' + self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))

    def mail_results(self, package_folder, results, report_location):
        self.send_message(self.config.email_to, self.config.email_subject_package_evaluation + u' ' + package_folder + u': ' + results, report_location)

    def mail_step2_failure(self, package_folder, e):
        self.send_message(self.config.email_to_adm, '[Step 2]' + self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))

    def mail_step3_failure(self, package_folder, e):
        self.send_message(self.config.email_to_adm, '[Step 3]' + self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))


class FilesTransfer(object):

    def __init__(self, config):
        self.config = config

    def transfer_website_files(self, acron, issue_id):
        if self.config.is_enabled_transference:
            issue_id_path = acron + '/' + issue_id
            folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']
            for folder in folders:
                dest_path = self.config.remote_web_app_path + folder + issue_id_path
                source_path = self.config.local_web_app_path + folder + issue_id_path
                for server in self.config.transference_servers:
                    xc.run_remote_mkdirs(self.config.user, server, dest_path)
                    xc.run_rsync(source_path, self.config.user, server, dest_path)

    def transfer_report_files(self, acron, issue_id):
        # 'rsync -CrvK img/* self.config.user@server:/var/www/...../revistas'
        if self.config.is_enabled_transference:
            issue_id_path = acron + '/' + issue_id
            folders = ['/htdocs/reports/']
            for folder in folders:
                dest_path = self.config.remote_web_app_path + folder + issue_id_path
                source_path = self.config.local_web_app_path + folder + issue_id_path
                log_filename = './transfer_report_' + issue_id_path.replace('/', '-') + '.log'
                for server in self.config.transference_servers:
                    xc.run_remote_mkdirs(self.config.user, server, dest_path, log_filename)
                    xc.run_rsync(source_path, self.config.user, server, dest_path, log_filename)


def report_status(title, status, style=None):
    text = ''
    if status is not None:
        for category in sorted(status.keys()):
            _style = style
            if status.get(category) is None:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            elif len(status[category]) == 0:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            else:
                ltype = 'ol'
                list_items = status[category]
            text += html_reports.format_list(categories_messages.get(category, category), ltype, list_items, _style)
    if len(text) > 0:
        text = html_reports.tag('h3', title) + text
    return text


def queue_packages(download_path, temp_path, queue_path, archive_path):
    invalid_pkg_files = []
    proc_id = datetime.now().isoformat()[11:16].replace(':', '')
    temp_path = temp_path + '/' + proc_id
    queue_path = queue_path + '/' + proc_id
    pkg_paths = []

    if os.path.isdir(temp_path):
        fs_utils.delete_file_or_folder(temp_path)
    if os.path.isdir(queue_path):
        fs_utils.delete_file_or_folder(queue_path)

    if archive_path is not None:
        if not os.path.isdir(archive_path):
            os.makedirs(archive_path)

    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)

    for pkg_name in os.listdir(download_path):
        if is_valid_pkg_file(download_path + '/' + pkg_name):
            shutil.copyfile(download_path + '/' + pkg_name, temp_path + '/' + pkg_name)
        else:
            pkg_paths.append(pkg_name)
        fs_utils.delete_file_or_folder(download_path + '/' + pkg_name)

    for pkg_name in os.listdir(temp_path):
        queued_pkg_path = queue_path + '/' + pkg_name
        if not os.path.isdir(queued_pkg_path):
            os.makedirs(queued_pkg_path)

        if fs_utils.extract_package(temp_path + '/' + pkg_name, queued_pkg_path):
            if archive_path is not None:
                if os.path.isdir(archive_path):
                    shutil.copyfile(temp_path + '/' + pkg_name, archive_path + '/' + pkg_name)
            pkg_paths.append(queued_pkg_path)
        else:
            invalid_pkg_files.append(pkg_name)
            fs_utils.delete_file_or_folder(queued_pkg_path)
        fs_utils.delete_file_or_folder(temp_path + '/' + pkg_name)
    fs_utils.delete_file_or_folder(temp_path)

    return (pkg_paths, invalid_pkg_files)


def xml_converter_read_configuration(filename):
    r = None
    if os.path.isfile(filename):
        r = xc_config.XMLConverterConfiguration(filename)
        if not r.valid:
            r = None
    return r


def xml_config_filename(collection_acron):
    filename = CURRENT_PATH + '/../../scielo_paths.ini'

    if not os.path.isfile(filename):
        if not collection_acron is None:
            filename = CURRENT_PATH + '/../config/' + collection_acron + '.xc.ini'
    return filename


def is_valid_configuration_file(configuration_filename):
    messages = []
    if configuration_filename is None:
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append(validation_status.STATUS_ERROR + ': ' + _('No configuration file was informed'))
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append(validation_status.STATUS_ERROR + ': ' + _('unable to read XML Converter configuration file: ') + configuration_filename)
    return messages


def is_valid_pkg_file(filename):
    return os.path.isfile(filename) and (filename.endswith('.zip') or filename.endswith('.tgz'))


def send_message(mailer, to, subject, text, attaches=None):
    if mailer is not None:
        #utils.debugging('sending message ' + subject)
        mailer.send_message(to, subject, text, attaches)
