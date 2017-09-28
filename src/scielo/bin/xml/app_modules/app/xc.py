# coding=utf-8

import os
import shutil
from datetime import datetime

from ..__init__ import _
from ..generics import fs_utils
from ..generics import encoding
from ..generics import xml_utils
from .pkg_processors import pkg_processors
from .data import workarea
from .server import mailer
from .server import filestransfer
from .config import config


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
            encoding.display_message('\n'.join(messages))

    reception = XC_Reception(config.Configuration(config.get_configuration_filename(collection_acron)))
    if package_path is None and collection_acron is None:
        reception.display_form()
    else:
        package_paths = [package_path]
        if collection_acron is not None:
            package_paths = reception.queued_packages()
        for package_path in package_paths:
            try:
                reception.convert_package(package_path)
            except Exception as e:
                encoding.report_exception('convert_package', e, package_path)
                raise


def read_inputs(args):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    args = encoding.fix_args(args)
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

    def __init__(self, configuration):
        self.configuration = configuration

        self.mailer = mailer.Mailer(configuration)
        self.transfer = filestransfer.FilesTransfer(configuration)
        self.proc = pkg_processors.PkgProcessor(configuration, INTERATIVE=configuration.interative_mode, stage='xc')

    def display_form(self):
        if self.configuration.interative_mode is True:
            from . import interface
            interface.display_form(self.proc.stage == 'xc', None, self.call_convert_package)

    def call_convert_package(self, package_path):
        self.convert_package(package_path)
        return 'done', 'blue'

    def convert_package(self, package_path):
        if package_path is None:
            return False
        pkgfolder = workarea.PackageFolder(package_path)
        encoding.display_message(package_path)
        xc_status = 'interrupted'

        pkg = self.proc.normalized_package(pkgfolder.xml_list)
        scilista_items = []

        try:
            if len(pkg.articles) > 0:
                scilista_items, xc_status, mail_info = self.proc.convert_package(pkg)
                encoding.display_message(scilista_items)
        except Exception as e:

            if self.configuration.queue_path is not None:
                fs_utils.delete_file_or_folder(package_path)
            self.mailer.mail_step1_failure(pkgfolder.name, e)
            raise
        if len(scilista_items) > 0:
            acron, issue_id = scilista_items[0].split(' ')
            try:
                if xc_status in ['accepted', 'approved']:
                    if self.configuration.collection_scilista is not None:
                        fs_utils.append_file(self.configuration.collection_scilista, '\n'.join(scilista_items) + '\n')
                    self.transfer.transfer_website_files(acron, issue_id)
            except Exception as e:
                self.mailer.mail_step2_failure(pkgfolder.name, e)
                raise
            try:
                if mail_info is not None and self.configuration.email_subject_package_evaluation is not None:
                    mail_subject, mail_content = mail_info
                    self.mailer.mail_results(pkgfolder.name, mail_subject, mail_content)
                self.transfer.transfer_report_files(acron, issue_id)

            except Exception as e:
                self.mailer.mail_step3_failure(pkgfolder.name, e)
                if len(package_path) == 1:
                    encoding.report_exception('convert_package()', e, 'exception as step 3')
        encoding.display_message(_('finished'))

    def queued_packages(self):
        pkg_paths, invalid_pkg_files = self.queue_packages()
        if pkg_paths is None:
            pkg_paths = []
        if len(invalid_pkg_files) > 0:
            self.mailer.mail_invalid_packages(invalid_pkg_files)
        return pkg_paths

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
