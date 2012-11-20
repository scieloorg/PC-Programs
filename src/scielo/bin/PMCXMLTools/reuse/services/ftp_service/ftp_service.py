from ftplib import FTP
import os

class FTPService:

    def __init__(self, report, server, user, pswd):
        self.server = server
        self.user = user
        self.pswd = pswd
        self.report = report
        self.ftp = FTP(server)

    def download_files(self, local_path, path_in_ftp_server):
        if not os.path.isdir(local_path):
            os.makedirs(local_path)
        os.chdir(local_path)

        r = self.ftp.login(self.user, self.pswd)
        self.report.write(r, True, False, True)
        
        self.download_files_of_subdir(local_path, path_in_ftp_server, False)

        r = self.ftp.close()
        self.report.write('ftp finished', True, False, True)
    
    def download_files_of_subdir(self, local_path, path_in_ftp_server, delete_path_in_ftp_server = False):
        levels = len(path_in_ftp_server.split('/'))
        
        # go to ftp directory
        self.report.write('go to ' + path_in_ftp_server, True, False, True)
        r = self.ftp.cwd(path_in_ftp_server)
        self.report.write(r, True, False, True)

        # download files
        files_or_folders = self.ftp.nlst()
        self.report.write('Files/Folders to download:' + '\n'.join(files_or_folders) + '\n' + str(len(files_or_folders)) + ' files/folders', True, False, True)
        
        for folder_or_file in files_or_folders:
            if '.' in folder_or_file:
                # must be a file
                self.download_and_delete_file(local_path, folder_or_file)
            else:
                # supposed to be a folder
                self.download_files_of_subdir(local_path, folder_or_file, False)

        # up level
        for i in range(0,levels):
            r = self.ftp.cwd('..')
            self.report.write(r, True, False, True)

        if delete_path_in_ftp_server:
            r = self.ftp.rmd(path_in_ftp_server)
        self.report.write(r, True, False, True)
        
        
    def download_and_delete_file(self, local_path, file):
        r = self.ftp.retrbinary('RETR ' + file, open(file, 'wb').write)
        self.report.write(r, True, False, True)
        if os.path.exists(local_path + '/' + file):
            r = self.ftp.delete(file)
            self.report.write(r, True, False, True)

    





