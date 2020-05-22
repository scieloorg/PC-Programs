import zipfile
import os
import shutil
import logging
import tempfile
from ftplib import FTP, all_errors


class Exporter(object):

    def __init__(self, data):
        self._data = data

    @property
    def ftp_config(self):
        try:
            server = self._data["server"]
            user = self._data["user"]
            password = self._data["password"]
            remote_path = self._data.get("remote_path")
        except KeyError:
            raise KeyError("Exporter: Configuration failure")
        else:
            return server, user, password, remote_path

    def export(self, files_path, zip_filename):
        zip_file_path = self.zip(files_path, zip_filename)
        if zip_file_path:
            self.export_by_ftp(zip_file_path)
            try:
                os.unlink(zip_file_path)
                shutil.rmtree(os.path.dirname(zip_file_path))
            except OSError:
                logging.info(
                    "Exporter: Unable to delete temp: %s" % zip_file_path)

    def zip(self, files_path, zip_filename):
        try:
            dest_path = tempfile.mkdtemp()
        except IOError:
            logging.info("Exporter: Unable to create temp dir")
        else:
            zip_file_path = os.path.join(dest_path, zip_filename)
            try:
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    for item in os.listdir(files_path):
                        file_path = os.path.join(files_path, item)
                        zipf.write(file_path, arcname=item)
            except IOError:
                logging.info(
                    "Exporter: Unable to create zip: %s" % zip_filename
                )
            else:
                return zip_file_path

    def export_by_ftp(self, local_file_path):
        try:
            config = self.ftp_config
        except KeyError:
            logging.info("Export: Invalid configuration")
        else:
            server, user, password, remote_path = config
            try:
                with FTP(server, timeout=60) as ftp:
                    ftp.login(user, password)
                    if remote_path:
                        ftp.cwd(remote_path)
                    remote_name = os.path.basename(local_file_path)
                    with open(local_file_path, 'rb') as f:
                        try:
                            ftp.storbinary('STOR {}'.format(remote_name), f)
                        except all_errors:
                            logging.info(
                                'FTP: Unable to send %s to %s' %
                                (local_file_path, remote_name), exc_info=True)
            except all_errors:
                logging.info("Unable to transfer: %s" % local_file_path)
