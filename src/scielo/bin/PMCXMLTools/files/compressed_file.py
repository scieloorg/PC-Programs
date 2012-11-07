import os
import shutil

from datetime import date

from files_extractor import extract_file, is_compressed_file


class CompressedFile:
    def __init__(self, report):
    	self.report = report

    def extract_files(self, compressed_path, destination_path, backup_path):
        """
        Extract files to destination_path from compressed files that are in compressed_path 
        """
        r = False

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        if os.path.exists(compressed_path):
            for filename in os.listdir(compressed_path):
                compressed_file = compressed_path + '/' + filename

                self.report.write('package file: ' + compressed_file, True, False, True)
                
                if os.path.isfile(compressed_file):
                    if is_compressed_file(compressed_file):
                        
                        
                        self.report.write('Extract ' + compressed_file + ' to ' + destination_path, True, False, True)  
                        extract_file(compressed_file, destination_path )

                        if not os.path.exists(backup_path):
                            os.makedirs(backup_path)
                        self.backup(compressed_file, backup_path)
                            
                    else:
                        self.report.write(compressed_file + ' is not a valid package file. It must be a compressed file.', True, True, True)

                else:
                    self.report.write(compressed_file + ' is not a valid package file. It must be a compressed file.', True, True, True)
        else:
            self.report.write('Invalid package path: ' + compressed_path, True, True, True)
            
        return r

    
    	
    def backup(self, package_file, backup_path):
        """
        Make a backup of package_file in compressed_path + '.bkp/' + date 
        """
        d = date.today().isoformat()

        backup_path = backup_path + '/' + d
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        if os.path.exists(backup_path):
            self.__copy_file_to_folder__(package_file, backup_path)
        

    def __copy_file_to_folder__(self, filename, dest_path):
        if os.path.isfile(filename) and os.path.isdir(dest_path):
            name = os.path.basename(filename)
            path = os.path.dirname(filename)
            if os.path.exists(dest_path + '/' + name):
                os.unlink(dest_path + '/' + name)
            shutil.copyfile(filename, dest_path + '/' + name)
