import zipfile
import os
import re
import shutil
import logging
import tempfile
import threading
from ftplib import FTP, all_errors
from datetime import datetime


exp_logger = logging.getLogger(__name__)


class Exporter(object):

    def __init__(self, data):
        self._data = data

    @property
    def ftp_configuration(self):
        try:
            server = self._data["server"]
            user = self._data["user"]
            password = self._data["password"]
        except KeyError:
            exp_logger.info("Exporter: Missing FTP Configuration")
        else:
            return server, user, password, self._data.get("remote_path")

    @property
    def copy_configuration(self):
        try:
            destination_path = self._data["destination_path"]
            if not os.path.isdir(destination_path):
                os.makedirs(destination_path)
        except KeyError:
            exp_logger.info("Exporter: Missing Destination Configuration")
        else:
            return destination_path

    def _preppend_time_to_destination_filename(
        self, destination_dir:str, file_path: str
    ) -> str:
        """Adds the current datetime to a filename.

        Example of use:
        Exporter().preppend_time_to_destination_filename("/tmp/", "/home/user/file.txt")
        "/tmp/2020-05-22-10-00-34-480190_file.txt"

        Params:
            destination_dir (str): A system path to the directory where a file will be put
            file_path (str): The origin file path/name that should be preppend with time

        Returns:
            completed_destination_path (str): The full destionation path
        """

        data = re.sub(r"[\W\s]", "-", str(datetime.now()))
        _, file_name = os.path.split(file_path)
        return os.path.join(destination_dir, "%s_%s" % (data, file_name))

    def export(self, source_path, zip_filename):
        destination_path = self.copy_configuration
        ftp_configuration = self.ftp_configuration

        if not destination_path and not ftp_configuration:
            exp_logger.info("Exporter: Missing Configuration")
            return

        zip_file_path = self.zip(source_path, zip_filename)

        if zip_file_path:
            dest_path = destination_path or os.path.dirname(zip_file_path)

            final_file_path = self._preppend_time_to_destination_filename(
                dest_path, zip_file_path
            )
            shutil.move(zip_file_path, final_file_path)

            if not destination_path and ftp_configuration:
                server, user, password, remote_path = ftp_configuration
                self.export_by_ftp(final_file_path, server, user, password, remote_path)
                return {
                    "file": os.path.join(
                        remote_path, os.path.basename(final_file_path)),
                    "ftp": server, "user": user,
                }
            return {"file": final_file_path}

    def zip(self, source_path, zip_filename):
        try:
            dest_path = tempfile.mkdtemp()
        except IOError:
            exp_logger.info("Exporter: Unable to create temp dir")
        else:
            zip_file_path = os.path.join(dest_path, zip_filename)
            try:
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    exp_logger.info(
                        "Create %s from %s" % (zip_file_path, source_path))
                    for item in os.listdir(source_path):
                        file_path = os.path.join(source_path, item)
                        zipf.write(file_path, arcname=item)
            except IOError:
                exp_logger.info(
                    "Exporter: Unable to create zip: %s" % zip_filename
                )
            else:
                return zip_file_path

    def export_by_ftp(self, local_file_path, server, user, password, remote_path):
        background = AsyncFTP(local_file_path, server, user, password, remote_path)
        background.start()


class AsyncFTP(threading.Thread):
    def __init__(self, local_file_path, server, user, password, remote_path, timeout=60):
        threading.Thread.__init__(self)
        self.local_file_path = local_file_path
        self.server = server
        self.user = user
        self.password = password
        self.remote_path = remote_path
        self.timeout = timeout

    def run(self):
        exp_logger.info("FTP.START")
        try:
            ftp = FTP(self.server, self.user, self.password, self.timeout)
        except all_errors as e:
            exp_logger.info(e)
            return
        try:
            if self.remote_path:
                ftp.cwd(self.remote_path)
            exp_logger.info("ftp " + self.local_file_path)
            remote_name = os.path.basename(self.local_file_path)
            with open(self.local_file_path, 'rb') as f:
                try:
                    exp_logger.info("FTP.STOR %s - start" % remote_name)
                    ftp.storbinary('STOR {}'.format(remote_name), f)
                    exp_logger.info("FTP.STOR %s - end" % remote_name)
                except all_errors:
                    exp_logger.info(
                        'FTP: Unable to send %s to %s' %
                        (self.local_file_path, remote_name), exc_info=True)
        except all_errors as e:
            exp_logger.info("all_errors as e")

            exp_logger.info(e)
        finally:
            ftp.close()
            exp_logger.info("FTP.END")
            try:
                os.unlink(self.local_file_path)
                shutil.rmtree(os.path.dirname(self.local_file_path))
            except OSError:
                exp_logger.info(
                    "Exporter: Unable to delete temp: %s" % self.local_file_path)
