import os
import shutil

from datetime import date

from files_extractor import extract_file, is_compressed_file


class UploadedFilesManager:
    def __init__(self, report, packages_path):
    	self.packages_path = packages_path
        self.report = report
    	
    def backup(self, package_file):
        """
        Make a backup of package_file in self.packages_path + '.bkp/' + date 
        """
        d = date.today().isoformat()

        backup_path = self.packages_path + '.bkp/' + d
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        if os.path.exists(backup_path):
            self.__copy_file_to_folder__(package_file, backup_path)
        

    def transfer_files(self, destination_path):
        """
        Transfer all the compressed files from self.packages_path to destination_path

        """
        r = False

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        if os.path.exists(self.packages_path):
            for filename in os.listdir(self.packages_path):
                package_file = self.packages_path + '/' + filename

                self.report.write('package file: ' + package_file, True, False, True)
                
                if os.path.isfile(package_file):
                    if is_compressed_file(package_file):

                        self.report.write('Move ' + package_file + ' to ' + destination_path, True, False, True)  
                        self.__move_file_to_folder__(package_file, destination_path)
                        
                        destination_filename = destination_path + '/' + filename
                        if os.path.exists(destination_filename):
                            r = True
                        else:
                            self.report.write('Unable to move ' + destination_filename, True, True, True) 
                            
                    else:
                        self.report.write(package_file + ' is not a valid package file. It must be a compressed file.', True, True, True)

                else:
                    self.report.write(package_file + ' is not a valid package file. It must be a compressed file.', True, True, True)
        else:
            self.report.write('Invalid package path: ' + self.packages_path, True, True, True)
            
        return r

    

    def extract_file(self, filename, destination_path):
        self.report.write('Extract file ' + filename, True, False, True)  
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        import tempfile
        tmp_path = tempfile.mkdtemp().replace('\\', '/')
        if os.path.isdir(tmp_path):
            extract_file(filename, tmp_path)
            
            self.report.write('Content extracted: ' + ','.join(os.listdir(tmp_path)), False, False, False)
            for file_or_folder in os.listdir(tmp_path):
                extracted_file_or_folder = tmp_path + '/' + file_or_folder
                if os.path.isdir(extracted_file_or_folder):
                    self.report.write('Content of ' + extracted_file_or_folder + ': ' + ','.join(os.listdir(extracted_file_or_folder)), False, False, False)
                    for file in os.listdir(extracted_file_or_folder):
                        self.__move_file_to_folder__(extracted_file_or_folder + '/' + file, destination_path)

                    print('apagar ' + extracted_file_or_folder)
                    shutil.rmtree(extracted_file_or_folder)
                elif os.path.isfile(extracted_file_or_folder):
                    self.__move_file_to_folder__(extracted_file_or_folder, destination_path)

            print('apagar ' + tmp_path)
            shutil.rmtree(tmp_path)
            
            self.report.write('Moved to ' + destination_path + ': ' + ','.join(os.listdir(destination_path)), False, False, False)


    def __move_file_to_folder__(self, filename, dest_path):
        if os.path.isfile(filename) and os.path.isdir(dest_path):
            name = os.path.basename(filename)
            path = os.path.dirname(filename)
            if os.path.exists(dest_path + '/' + name):
                os.unlink(dest_path + '/' + name)
            shutil.move(filename, dest_path)

    def __copy_file_to_folder__(self, filename, dest_path):
        if os.path.isfile(filename) and os.path.isdir(dest_path):
            name = os.path.basename(filename)
            path = os.path.dirname(filename)
            if os.path.exists(dest_path + '/' + name):
                os.unlink(dest_path + '/' + name)
            shutil.copyfile(filename, dest_path + '/' + name)
