# coding=utf-8

import os
import shutil
from datetime import datetime

from ..__init__ import _
from ..useful import fs_utils
from ..useful import utils
from ..useful import xml_utils
from ..reports import html_reports
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


class Reception(object):

    def __init__(self, version, stage, DISPLAY_REPORT=True):
        configuration = config.Configuration()
        self.proc = pkg_processors.PkgProcessor(configuration, version, DISPLAY_REPORT, stage)

    def display_form(self):
        interface.display_form(self.proc.stage == 'xc', None, self.call_convert_package)

    def call_convert_package(self, xml_path, GENERATE_PMC=False):
        xml_list = [xml_path + '/' + item for item in os.listdir(xml_path) if item.endswith('.xml')]
        pkgfiles = pkg_processors.normalize_xml_packages(xml_list, self.proc.stage)
        self.convert_package(pkgfiles, GENERATE_PMC)
        return 'done', 'blue'

    def convert_package(self, pkgfiles, GENERATE_PMC=False):
        self.proc.convert_package([f.filename for f in pkgfiles], GENERATE_PMC)


def call_make_packages(args, version):
    script, xml_path, acron, DISPLAY_REPORT, GENERATE_PMC = read_inputs(args)
    pkgfiles = None
    stage = 'xpm'
    if any([xml_path, acron]):
        stage, pkgfiles = get_pkgfiles(version, script, xml_path, acron)

    reception = Reception(version, stage, DISPLAY_REPORT)
    if pkgfiles is None:
        reception.display_form()
    else:
        reception.make_package(pkgfiles, GENERATE_PMC)


def call_converter(args, version='1.0'):
    script, package_path, collection_acron = read_inputs(args)
    if all([package_path, collection_acron]):
        errors = xml_utils.is_valid_xml_path(package_path)
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

    reception = Reception(version, 'xc', DISPLAY_REPORT=False)
    if package_path is None:
        reception.display_form()
    else:
        reception.make_package(pkgfiles, GENERATE_PMC)


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

    proc = pkg_processors.PkgProcessor(config, version, DISPLAY_REPORT, stage)
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
