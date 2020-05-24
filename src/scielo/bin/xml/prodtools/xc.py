# coding=utf-8
import logging
import logging.config
import argparse
import os
import shutil
from datetime import datetime

from prodtools import _
from prodtools import form
from prodtools.utils import fs_utils
from prodtools.utils import encoding
from prodtools.processing import pkg_processors
from prodtools.processing.sps_pkgmaker import PackageMaker
from prodtools.server import mailer
from prodtools.server import filestransfer
from prodtools.server import xc_gerapadrao
from prodtools.config import config
from prodtools.utils import ftp_service


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class ForbiddenOperationError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser(
        description='XML Converter for Desktop cli utility')
    parser.add_argument(
        "package_path", nargs='?',
        help="filesystem path to the XML package folder")
    parser.add_argument('--loglevel', default='WARNING')

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    package_path = args.package_path

    reception = Reception()
    reception.receive_package(package_path)


class Reception(object):

    def __init__(self, collection_acron=None):
        self.collection_acron = collection_acron
        self.config = config.Configuration(
            config.get_configuration_filename(collection_acron))
        self.proc = pkg_processors.PkgProcessor(
            self.config, INTERATIVE=self.config.interative_mode, stage='xc')
        self.mailer = mailer.Mailer(self.config)
        self.transfer = filestransfer.SciELOWebFilesTransfer(self.config)

    def download_packages(self):
        configuration = self.config
        try:
            ftp = ftp_service.FTPService(
                configuration.ftp_server,
                configuration.ftp_user,
                configuration.ftp_pswd)
            if not os.path.isdir(configuration.download_path):
                os.makedirs(configuration.download_path)
            files = ftp.download_files(
                configuration.download_path, configuration.ftp_dir)

            if len(files) > 0 and configuration.mailer:
                configuration.mailer.send_message(
                    configuration.email_to,
                    configuration.email_subject_packages_receipt,
                    configuration.email_text_packages_receipt +
                    '\n' + ftp.registered_actions)
        except Exception as e:
            self.inform_failure(
                "", str(e),
                subject=_('Something went wrong as downloading packages'))

    def receive_package(self, package_path=None):
        if self.collection_acron:
            return self._receive_package_for_server()
        else:
            return self._receive_package_for_desktop(package_path)

    def _receive_package_for_desktop(self, package_path=None):
        if self.collection_acron:
            raise ForbiddenOperationError(
                "Not allowed to call receive_package_for_desktop")
        if package_path is None and self.config.interative_mode:
            self.display_form()
        elif package_path:
            try:
                self.convert_package(package_path)
            except Exception as e:
                encoding.report_exception('convert_package', e, package_path)
                raise

    def _receive_package_for_server(self):
        if not self.collection_acron:
            raise ForbiddenOperationError(
                "Not allowed to call _receive_package_for_server")
        for package_path in self._queued_packages():
            self.convert_package(package_path)

    def display_form(self):
        form.display_form(
            self.proc.stage == 'xc', None, self.call_convert_package)

    def call_convert_package(self, package_path):
        self.convert_package(package_path)
        return 'done', 'blue'

    def convert_package(self, package_path):
        if package_path is None:
            return False

        encoding.display_message(package_path)
        xml_path = package_path

        scilista_items = []
        xc_status = 'interrupted'
        mail_info = "subject", "message"
        result = scilista_items, xc_status, mail_info

        # FIXME
        output_path = xml_path + "_" + self.proc.stage

        pkg_maker = PackageMaker(xml_path, output_path)
        pkg = pkg_maker.pack()
        pkg_name = pkg.package_folder.name
        try:
            if len(pkg.articles) > 0:
                result = self.proc.convert_package(pkg)
                scilista_items, xc_status, mail_info = result
        except Exception as e:
            if self.config.queue_path is not None:
                fs_utils.delete_file_or_folder(package_path)
            self.inform_failure(pkg_name, e)
        else:
            if len(scilista_items) > 0:
                acron, issue_id = scilista_items[0].split(' ')
                if xc_status in ['accepted', 'approved']:
                    self._update_scilista(pkg_name, scilista_items)
                    self._update_website_files(pkg_name, acron, issue_id)
                self._mail_results(pkg_name, mail_info)
                self._update_report_files(pkg_name, acron, issue_id)

        encoding.display_message(_('finished'))

    def inform_failure(self, package_name, msg, subject=None):
        if self.mailer:
            subject = subject or _("Failure during or after conversion")
            self.mailer.mail_failure(subject, package_name, msg)

    def _update_scilista(self, package_name, scilista_items):
        if self.config.collection_scilista:
            try:
                content = '\n'.join(scilista_items) + '\n'
                fs_utils.append_file(
                    self.config.collection_scilista,
                    content)
            except Exception as e:
                msg = _("Unable to update scilista {} with {}: {}"
                        ).format(self.config.collection_scilista, content, e)
                self.inform_failure(package_name, msg)

    def _mail_results(self, pkg_name, mail_info):
        if self.mailer:
            if mail_info and self.config.email_subject_package_evaluation:
                mail_subject, mail_content = mail_info
                self.mailer.mail_results(pkg_name, mail_subject, mail_content)

    def _update_website_files(self, package_name, acron, issue_id):
        if self.transfer:
            try:
                self.transfer.transfer_website_files(acron, issue_id)
            except Exception as e:
                msg = _("Unable to transfer xml, pdf, images files"
                        " of {} {}: {}").format(acron, issue_id, e)
                self.inform_failure(package_name, msg)

    def _update_report_files(self, package_name, acron, issue_id):
        if self.transfer:
            try:
                self.transfer.transfer_report_files(acron, issue_id)
            except Exception as e:
                msg = _("Unable to transfer report files"
                        " of {} {}: {}").format(acron, issue_id, e)
                self.inform_failure(package_name, msg)

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

    def gerapadrao(self):
        _gerapadrao = xc_gerapadrao.GeraPadrao(
            self.collection_acron, self.config, self.mailer)
        _gerapadrao.run()


if __name__ == "__main__":
    main()
