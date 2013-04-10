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
        
        downloaded_files = self.download_files_of_subdir(local_path, path_in_ftp_server, False)

        r = self.ftp.close()
        self.report.write('ftp finished', True, False, True)

        print(';\n'.join(downloaded_files))
        return downloaded_files
    
    def download_files_of_subdir(self, local_path, path_in_ftp_server, delete_path_in_ftp_server = False):
        levels = len(path_in_ftp_server.split('/'))
        downloaded_files = []
        # go to ftp directory
        self.report.write('go to ' + path_in_ftp_server, True, False, True)
        r = self.ftp.cwd(path_in_ftp_server)
        self.report.write(r, True, False, True)

        # download files
        files_or_folders = self.ftp.nlst()
        self.report.write('Files/Folders to download:\n' + '\n'.join(files_or_folders) + '\n' + str(len(files_or_folders)) + ' files/folders', True, False, True)
        
        for folder_or_file in files_or_folders:
            if os.path.isfile( path_in_ftp_server + '/' + folder_or_file):
                # must be a file
                print('test file')
                downloaded_file = self.download_and_delete_file(local_path, folder_or_file)
                if len(downloaded_file)>0:
                    downloaded_files.append(downloaded_file)
            elif os.path.isdir( path_in_ftp_server + '/' + folder_or_file):
                print('test dir')
                # supposed to be a folder
                downloaded_files += self.download_files_of_subdir(local_path, folder_or_file, False)
            elif folder_or_file.endswith('.zip') or folder_or_file.endswith('.tgz'):
                print('test .zip')
                # must be a file
                downloaded_file = self.download_and_delete_file(local_path, folder_or_file)
                if len(downloaded_file)>0:
                    downloaded_files.append(downloaded_file)
            else:
                # supposed to be a folder
                print('test nothing')
                downloaded_files += self.download_files_of_subdir(local_path, folder_or_file, False)


        # up level
        for i in range(0,levels):
            r = self.ftp.cwd('..')
            self.report.write(r, True, False, True)

        if delete_path_in_ftp_server:
            r = self.ftp.rmd(path_in_ftp_server)
        self.report.write(r, True, False, True)
        return downloaded_files
        
        
    def download_and_delete_file(self, local_path, file):
        downloaded_file = ''
        r = self.ftp.retrbinary('RETR ' + file, open(file, 'wb').write)
        self.report.write(r, True, False, True)
        if os.path.exists(local_path + '/' + file):

            statinfo = os.stat(local_path + '/' + file)
            self.report.write(str(statinfo.st_size), True, False, True)

            downloaded_file = file
            r = self.ftp.delete(file)
            self.report.write(r, True, False, True)
        return downloaded_file

    def list_content(self, path_in_ftp_server):
        
        r = self.ftp.login(self.user, self.pswd)
        self.report.write(r, True, False, True)
        
        files_list = self.list_content_of_files_of_subdir(path_in_ftp_server)

        r = self.ftp.close()
        self.report.write('ftp finished', True, False, True)

        print(';\n'.join(files_list))
        return files_list
    
    def list_content_of_files_of_subdir(self, path_in_ftp_server):
        levels = len(path_in_ftp_server.split('/'))
        items_in_ftp = []
        # go to ftp directory
        self.report.write('go to ' + path_in_ftp_server, True, False, True)
        r = self.ftp.cwd(path_in_ftp_server)
        self.report.write(r, True, False, True)

        # download files
        files_or_folders = self.ftp.nlst()
        self.report.write('Files/Folders in FTP:' + '\n'.join(files_or_folders) + '\n' + str(len(files_or_folders)) + ' files/folders', True, False, True)
        
        for folder_or_file in files_or_folders:
            if os.path.isdir(folder_or_file):
                items_in_ftp += self.list_content_of_files_of_subdir(folder_or_file)
            else:
                items_in_ftp.append(folder_or_file)
            
        # up level
        for i in range(0,levels):
            r = self.ftp.cwd('..')
            self.report.write(r, True, False, True)

        
        self.report.write(r, True, False, True)
        return items_in_ftp
