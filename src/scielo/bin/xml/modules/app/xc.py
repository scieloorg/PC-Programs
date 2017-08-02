# coding=utf-8

import os
import shutil
from datetime import datetime

from ..__init__ import _
from ..generics import fs_utils
from ..generics import utils
from ..generics import xml_utils
from ..generics.reports import html_reports
from .pkg_processors import pkg_processors
from .data import workarea
from ..generics.server import mailer
from ..generics.server import filestransfer
from . import interface


EMAIL_SUBJECT_STATUS_ICON = {}
EMAIL_SUBJECT_STATUS_ICON['rejected'] = [u"\u274C", _(' REJECTED ')]
EMAIL_SUBJECT_STATUS_ICON['ignored'] = ['', _('IGNORED')]
EMAIL_SUBJECT_STATUS_ICON['accepted'] = [u"\u2713" + ' ' + u"\u270D", _(' ACCEPTED but corrections required ')]
EMAIL_SUBJECT_STATUS_ICON['approved'] = [u"\u2705", _(' APPROVED ')]
EMAIL_SUBJECT_STATUS_ICON['not processed'] = ['', _(' NOT PROCESSED ')]


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

    reception = XC_Reception(config.Configuration(config.get_configuration_filename(collection_acron)), version, 'xc')
    if package_path is None:
        reception.display_form()
    else:
        reception.convert_package(package_path)


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


class XC_Reception(object):

    def __init__(self, configuration, version):
        self.configuration = configuration
        self.mailer = mailer.Mailer(configuration)
        self.transfer = filestransfer.FilesTransfer(configuration)
        self.proc = pkg_processors.PkgProcessor(configuration, version, DISPLAY_REPORT=True, stage='xc')

    def display_form(self):
        interface.display_form(self.proc.stage == 'xc', None, self.call_convert_package)

    def call_convert_package(self, package_path):
        self.convert_package(package_path)
        return 'done', 'blue'

    def convert_packages(self, package_paths):
        self.organize_packages_locations(package_paths)
        for package_path in package_paths:
            self.convert_package(package_path)

    def convert_package(self, package_path):
        package_name = os.path.basename(package_path)
        utils.display_message(package_path)
        xc_status = 'interrupted'
        stats_msg = ''
        report_location = None
        pkgfolder = workarea.PackageFolder(package_path)

        pkg = self.proc.normalized_package(pkgfolder.xml_list)
        scilista_items = []

        try:

            if len(pkg.articles) > 0:
                scilista_items, xc_status, stats_msg, report_location = self.proc.convert_package(pkg)
                print(scilista_items)
        except Exception as e:
            if self.configuration.queue_path is not None:
                fs_utils.delete_file_or_folder(package_path)
            self.mailer.mail_step1_failure(package_name, e)
        if len(scilista_items) > 0:
            acron, issue_id = scilista_items[0].split(' ')
            try:
                if xc_status in ['accepted', 'approved']:
                    if self.configuration.collection_scilista is not None:
                        fs_utils.append_file(self.configuration.collection_scilista, '\n'.join(scilista_items) + '\n')
                    self.transfer.transfer_website_files(acron, issue_id)
            except Exception as e:
                self.mailer.mail_step2_failure(package_name, e)
            try:
                if report_location is not None and self.configuration.email_subject_package_evaluation is not None:
                    results = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(xc_status, [])) + ' ' + stats_msg
                    link = self.configuration.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
                    mail_content = '<html><body>' + html_reports.link(link, link) + '</body></html>'
                    self.transfer.transfer_report_files(acron, issue_id)
                    self.mailer.mail_results(package_name, results, mail_content)
            except Exception as e:
                self.mailer.mail_step3_failure(package_name, e)
                if len(package_paths) == 1:
                    print('exception as step 3')
                    raise
        utils.display_message(_('finished'))

    def organize_packages_locations(self, pkg_path):
        if pkg_path is None:
            pkg_path, invalid_pkg_files = self.queue_packages()
        if pkg_path is None:
            pkg_path = []
        if not isinstance(pkg_path, list):
            pkg_path = [pkg_path]
        if len(invalid_pkg_files) > 0:
            self.mailer.mail_invalid_packages(invalid_pkg_files)

    def queue_packages(self):
        download_path = self.configuration.download_path
        temp_path = self.configuration.temp_path
        queue_path = self.configuration.queue_path
        archive_path = self.configuration.archive_path

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
            if fs_utils.is_compressed_file(download_path + '/' + pkg_name):
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
