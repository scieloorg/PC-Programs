# coding=utf-8

import os
import shutil
from datetime import datetime

from ..__init__ import _
from ..utils import fs_utils
from ..utils import utils
from ..reports import html_reports
from ..utils import xml_utils
from ..pkg_processors import pkg_processors
from ..data import package
from ..server import mailer
from ..server import filestransfer
from . import interface


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


def call_converter(args, version='1.0'):
    script, package_path, collection_acron = read_inputs(args)
    if package_path is None and collection_acron is None:
        interface.open_main_window(True, None)

    elif package_path is not None and collection_acron is not None:
        errors = validate_inputs(package_path, collection_acron)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
            messages.append('ERROR: ' + _('Incorrect parameters'))
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
    return xc_get_configuration(collection_acron)


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
    xc_mailer = mailer.Mailer(config)
    transfer = filestransfer.FilesTransfer(config)
    organize_packages_locations(package_paths, config, xc_mailer)

    proc = pkg_processors.PkgProcessor(config, version, DISPLAY_REPORT, GENERATE_PMC, stage)
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
            xc_mailer.mail_step1_failure(package_name, e)
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
                xc_mailer.mail_step2_failure(package_name, e)
                if len(package_paths) == 1:
                    print('exception as step 2')
                    raise
            try:
                if report_location is not None and config.email_subject_package_evaluation is not None:
                    results = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(xc_status, [])) + ' ' + stats_msg
                    link = config.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
                    mail_content = '<html><body>' + html_reports.link(link, link) + '</body></html>'
                    transfer.transfer_report_files(acron, issue_id)
                    xc_mailer.mail_results(package_name, results, mail_content)
            except Exception as e:
                xc_mailer.mail_step3_failure(package_name, e)
                if len(package_paths) == 1:
                    print('exception as step 3')
                    raise
    utils.display_message(_('finished'))
    """
    if tmp_result_path != conversion.results_path:
        fs_utils.delete_file_or_folder(tmp_result_path)
    os.unlink(log_package)
    """

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


def is_valid_pkg_file(filename):
    return os.path.isfile(filename) and (filename.endswith('.zip') or filename.endswith('.tgz'))
