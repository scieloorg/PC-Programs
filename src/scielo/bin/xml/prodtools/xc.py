# coding=utf-8
import logging
import logging.config
import argparse
import os
import shutil
import traceback

from tempfile import TemporaryDirectory
from datetime import datetime

from prodtools import _
from packtools.utils import SPPackage

try:
    from prodtools import form
except ImportError as e:
    print(e)
    print("It is ok if running on a server without GUI")

from prodtools.utils import fs_utils
from prodtools.utils import encoding
from prodtools.processing import pkg_processors
from prodtools.processing.sps_pkgmaker import PackageMaker
from prodtools.server import mailer
from prodtools.server import filestransfer
from prodtools.server import xc_gerapadrao
from prodtools.config import config
from prodtools.utils import ftp_service
from prodtools.utils.logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()

os_path_join = os.path.join


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

    logger.setLevel(args.loglevel.upper())

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

            if len(files) > 0 and self.mailer:
                self.mailer.send_message(
                    configuration.email_to,
                    configuration.email_subject_packages_receipt,
                    configuration.email_text_packages_receipt +
                    '\n' + ftp.registered_actions)
        except Exception as e:
            logger.exception(
                "Could not download packages. The following traceback was captured: "
            )
            self.mailer.mail_failure(
                subject="Could not download packages", text=traceback.format_exc(),
            )
            raise e

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
                logger.exception(
                    "Could not receive packages for desktop of path '%s'",
                    package_path,
                )
                self.mailer.mail_failure(
                    subject="Could not receive packages for desktop",
                    text=traceback.format_exc(),
                    package=package_path,
                )
                raise

    def _receive_package_for_server(self):
        if not self.collection_acron:
            raise ForbiddenOperationError(
                "Not allowed to call _receive_package_for_server")
        for package_path in self._queued_packages():
            self.convert_package(package_path)
            fs_utils.delete_file_or_folder(package_path)

    def display_form(self):
        form.display_form(
            self.proc.stage == 'xc', None, self.call_convert_package)

    def call_convert_package(self, package_path):
        self.convert_package(package_path)
        return 'done', 'blue'

    def _create_package_instance(self, source: str, output: str) -> SPPackage:
        """Cria instância da classe SPPackage para o pacote de entrada"""

        try:
            package_name = os.path.splitext(os.path.basename(source))[0]
        except (IndexError, TypeError):
            package_name = None

        package_maker = PackageMaker(source, output, package_name=package_name)
        return package_maker.pack()

    def convert_package(self, package_path):
        if package_path is None:
            return False

        encoding.display_message(package_path)
        xml_path = package_path

        scilista_items = []
        xc_status = 'interrupted'
        mail_info = "subject", "message"
        result = scilista_items, xc_status, mail_info

        with TemporaryDirectory() as output_path:
            try:
                package = self._create_package_instance(source=xml_path, output=output_path)
                scilista_items, xc_status, mail_info = self.proc.convert_package(package)
            except Exception:
                logger.exception(
                    "Could not convert the package '%s'. The following traceback was captured: ",
                    package_path,
                )
                self.mailer.mail_failure(
                    subject="Could not convert the package",
                    text=traceback.format_exc(),
                    package=package_path,
                )
            else:
                if scilista_items is None or len(scilista_items) == 0:
                    logger.debug("The scilista is empty. Skipping website update, report step and email sending.")
                    return None

                package_name = package.package_folder.name
                acron, issue_id = scilista_items[0].split(" ")

                if xc_status in ["accepted", "approved"]:
                    self._update_scilista(package_name, scilista_items)
                    self._update_website_files(package_name, acron, issue_id)

                self._mail_results(package_name, mail_info)
                self._update_report_files(package_name, acron, issue_id)

        encoding.display_message(_('finished'))

    def _update_scilista(self, package_name, scilista_items):
        """Atualiza a scilista da coleção no path configurado"""
        if self.config.collection_scilista:
            try:
                content = '\n'.join(list(set(scilista_items))) + '\n'
                fs_utils.append_file(
                    self.config.collection_scilista,
                    content)
            except Exception as e:
                subject = _("Unable to update scilista {} with {}").format(
                    self.config.collection_scilista, content
                )
                logger.exception(
                    "Could not update the scilista '%s' with '%s",
                    self.config.collection_scilista,
                    content,
                )
                self.mailer.mail_failure(
                    subject=subject, text=traceback.format_exc(), package=package_name
                )
                raise e

    def _mail_results(self, pkg_name, mail_info):
        if (
            mail_info is not None
            and len(mail_info) == 2
            and self.config.is_enabled_email_service
            and self.config.email_subject_package_evaluation
        ):
            mail_subject, mail_content = mail_info
            self.mailer.mail_results(pkg_name, mail_subject, mail_content)
        else:
            logger.info('Package "%s" mail - "%s"', pkg_name, mail_info)

    def _update_website_files(self, package_name, acron, issue_id):
        if self.transfer:
            try:
                self.transfer.transfer_website_files(acron, issue_id)
            except Exception as e:
                subject = _(
                    "Unable to transfer xml, pdf, images files of {} {}"
                ).format(acron, issue_id)
                logger.exception(subject)
                self.mailer.mail_failure(
                    subject=subject, text=traceback.format_exc(), package=package_name
                )
                raise e

    def _update_report_files(self, package_name, acron, issue_id):
        if self.transfer:
            try:
                self.transfer.transfer_report_files(acron, issue_id)
            except Exception as e:
                subject = _("Unable to transfer report files of {} {}").format(
                    acron, issue_id
                )
                logger.exception(subject)
                self.mailer.mail_failure(
                    subject=subject, text=traceback.format_exc(), package=package_name
                )
                raise e

    def _queued_packages(self):
        pkg_paths, invalid_pkg_files = self._queue_packages()
        if pkg_paths is None:
            pkg_paths = []
        if len(invalid_pkg_files) > 0:
            self.mailer.mail_invalid_packages(invalid_pkg_files)
        return pkg_paths

    def _queue_packages(self):
        download_path = self.config.download_path
        temp_path = self.config.temp_path
        queue_path = self.config.queue_path
        archive_path = self.config.archive_path

        invalid_pkg_files = []
        proc_id = datetime.now().isoformat()[11:16].replace(':', '')
        temp_path = os_path_join(temp_path, proc_id)
        queue_path = os_path_join(queue_path, proc_id)
        pkg_paths = []

        for path in (temp_path, queue_path):
            if os.path.isdir(path):
                fs_utils.delete_file_or_folder(path)

        for path in (temp_path, archive_path):
            if path and not os.path.isdir(path):
                os.makedirs(path)

        for pkg_name in os.listdir(download_path):
            downloaded_pkg_file_path = os_path_join(download_path, pkg_name)
            if os.path.isfile(downloaded_pkg_file_path):
                shutil.move(downloaded_pkg_file_path, temp_path)
            else:
                invalid_pkg_files.append(pkg_name)
                fs_utils.delete_file_or_folder(downloaded_pkg_file_path)

        for pkg_name in os.listdir(temp_path):
            tmp_pkg_path = os_path_join(temp_path, pkg_name)

            queued_pkg_path = os_path_join(queue_path, pkg_name)
            if not os.path.isdir(queued_pkg_path):
                os.makedirs(queued_pkg_path)

            if fs_utils.extract_package(tmp_pkg_path, queued_pkg_path):
                if archive_path and os.path.isdir(archive_path):
                    shutil.copy(tmp_pkg_path, archive_path)
                pkg_paths.append(queued_pkg_path)
            else:
                invalid_pkg_files.append(pkg_name)
                fs_utils.delete_file_or_folder(queued_pkg_path)
        fs_utils.delete_file_or_folder(temp_path)

        return (pkg_paths, invalid_pkg_files)

    def gerapadrao(self):
        _gerapadrao = xc_gerapadrao.GeraPadrao(
            self.collection_acron, self.config, self.mailer)
        _gerapadrao.run()


if __name__ == "__main__":
    main()
