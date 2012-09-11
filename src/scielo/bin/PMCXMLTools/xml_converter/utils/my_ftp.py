from ftplib import FTP
import os

class MyFTP:

    def __init__(self, report, server, user, pswd):
        self.server = server
        self.user = user
        self.pswd = pswd
        self.report = report
        self.ftp = FTP(server)

    def download_files(self, local_path, dirname):
        if not os.path.isdir(local_path):
            os.makedirs(local_path)
        os.chdir(local_path)

        r = self.ftp.login(self.user, self.pswd)
        self.report.write(r, True, False, True)
        
        self.download_files_of_subdir(local_path, dirname, False)

        r = self.ftp.close()
        self.report.write('ftp finished', True, False, True)
    
    def download_files_of_subdir(self, local_path, folder, delete_folder):
        r = self.ftp.cwd(folder)
        self.report.write(r, True, False, True)

        files_or_folders = self.ftp.nlst()
        
        for folder_or_file in files_or_folders:
            if '.' in folder_or_file:
                # must be a file
                self.download_and_delete_file(local_path, folder_or_file)
            else:
                # supposed to be a folder
                self.download_files_of_subdir(local_path, folder_or_file, False)
        r = self.ftp.cwd('..')
        self.report.write(r, True, False, True)

        if delete_folder:
            r = self.ftp.rmd(folder)
        self.report.write(r, True, False, True)
        
        
    def download_and_delete_file(self, local_path, file):
        r = self.ftp.retrbinary('RETR ' + file, open(file, 'wb').write)
        self.report.write(r, True, False, True)
        if os.path.exists(local_path + '/' + file):
            r = self.ftp.delete(file)
            self.report.write(r, True, False, True)

    





