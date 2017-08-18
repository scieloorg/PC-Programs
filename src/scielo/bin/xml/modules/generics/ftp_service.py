# coding=utf-8
from ftplib import FTP
import os

from . import encoding


actions = []


def register_action(action):
    encoding.display_message(action)
    actions.append(action)


class FTPService(object):

    def __init__(self, server, user, pswd):
        self.user = user
        self.pswd = pswd
        self.ftp = FTP(server)

    @property
    def registered_actions(self):
        return '\n'.join(actions)

    def download_files(self, local_path, path_in_ftp_server):
        if not os.path.isdir(local_path):
            os.makedirs(local_path)
        os.chdir(local_path)

        r = self.ftp.login(self.user, self.pswd)
        register_action(r)
        downloaded_files = self.download_files_of_subdir(local_path, path_in_ftp_server, False)

        r = self.ftp.close()
        register_action('ftp finished')

        register_action(';\n'.join(downloaded_files))
        return downloaded_files

    def download_files_of_subdir(self, local_path, path_in_ftp_server, delete_path_in_ftp_server=False):
        levels = len(path_in_ftp_server.split('/'))
        downloaded_files = []

        exist_ftp_folder = False
        if '/' in path_in_ftp_server:
            exist_ftp_folder = True
        else:
            if path_in_ftp_server in self.ftp.nlst():
                exist_ftp_folder = True

        if exist_ftp_folder:
            # go to ftp directory
            try:
                register_action('try to go to ' + path_in_ftp_server)
                r = self.ftp.cwd(path_in_ftp_server)
                register_action(r)

                # download files
                files_or_folders = self.ftp.nlst()
                register_action('Files/Folders to download:\n' + '\n'.join(files_or_folders) + '\n' + str(len(files_or_folders)) + ' files/folders')
                for item in files_or_folders:
                    if item.endswith('.zip') or item.endswith('.tgz'):
                        # must be a file
                        downloaded_file = self.download_and_delete_file(local_path, item)
                        if len(downloaded_file) > 0:
                            downloaded_files.append(downloaded_file)
                    else:
                        # supposed to be a folder
                        downloaded_files += self.download_files_of_subdir(local_path, item, False)

                # up level
                for i in range(0, levels):
                    r = self.ftp.cwd('..')
                    register_action(r)

                if delete_path_in_ftp_server:
                    r = self.ftp.rmd(path_in_ftp_server)
                register_action(r)
            except:
                register_action('not found: ' + path_in_ftp_server)
        else:
            register_action('not found: ' + path_in_ftp_server)

        return downloaded_files

    def download_and_delete_file(self, local_path, file):
        downloaded_file = ''
        r = self.ftp.retrbinary('RETR ' + file, open(file, 'wb').write)
        register_action(r)
        if os.path.exists(local_path + '/' + file):

            statinfo = os.stat(local_path + '/' + file)
            register_action(str(statinfo.st_size))

            downloaded_file = file
            r = self.ftp.delete(file)
            register_action(r)
        return downloaded_file

    def list_content(self, path_in_ftp_server):
        r = self.ftp.login(self.user, self.pswd)
        register_action(r)
        files_list = self.list_content_of_files_of_subdir(path_in_ftp_server)

        r = self.ftp.close()
        register_action('ftp finished')

        encoding.display_message(';\n'.join(files_list))
        return files_list

    def list_content_of_files_of_subdir(self, path_in_ftp_server):
        levels = len(path_in_ftp_server.split('/'))
        items_in_ftp = []
        # go to ftp directory
        register_action('go to ' + path_in_ftp_server)
        r = self.ftp.cwd(path_in_ftp_server)
        register_action(r)

        # download files
        files_or_folders = self.ftp.nlst()
        register_action('Files/Folders in FTP:' + '\n'.join(files_or_folders) + '\n' + str(len(files_or_folders)) + ' files/folders')
        for folder_or_file in files_or_folders:
            if os.path.isdir(folder_or_file):
                items_in_ftp += self.list_content_of_files_of_subdir(folder_or_file)
            else:
                items_in_ftp.append(folder_or_file)
            # up level
        for i in range(0, levels):
            r = self.ftp.cwd('..')
            register_action(r)

        register_action(r)
        return items_in_ftp


def download_files(ftp_server, user, password, ftp_folder, destination_path):
    ftp = FTPService(ftp_server, user, password)
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)
    files = ftp.download_files(destination_path, ftp_folder)
    log = ftp.registered_actions
    return (files, log)
