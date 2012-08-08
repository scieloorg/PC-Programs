import os
import shutil

from datetime import datetime

from files_extractor import extract_file, is_compressed_file


class UploadedFilesManager:
    def __init__(self, packages_path, work_path, trash_path, bkp_path):
    	self.packages_path = packages_path
    	self.work_path = work_path
    	self.trash_path = trash_path
        self.bkp_path = bkp_path 
    
    def organize_files(self, report):
        #files_set = PMCXML_FilesSet(self.work_path, suppl_filename, self.output_path, db_name)
        dst = datetime.now().isoformat().replace(':', '')
        dst = self.bkp_path + '/' + dst[0:dst.find('.')] 
        print(dst)
        if not os.path.exists(dst):
            os.makedirs(dst)
                       
        
        if os.path.exists(self.packages_path):
            for filename in os.listdir(self.packages_path):
                package_file = self.packages_path + '/' + filename

                if os.path.isfile(package_file):
                    if is_compressed_file(package_file):
                        name = filename[0:filename.rfind('.')]
                        wrk_path = self.work_path + '/' + name
                        compressed = True 
                    else:
                        wrk_path = self.work_path + '/unpacked' 
                        compressed = False
                
                    # backup of package or file
                    report.log_event('Backup ' + package_file + ' to ' + dst + '/' + os.path.basename(package_file), True)  
                        
                    shutil.copyfile(package_file, dst + '/' + os.path.basename(package_file))
                        

                    if not os.path.exists(wrk_path):
                        os.makedirs(wrk_path)

                    if os.path.exists(wrk_path):  
                        report.log_event('Move ' + package_file + ' to ' + wrk_path)  
                        
                        
                        self.move_file_to_folder(package_file, wrk_path)
                        
                        moved_package_file = wrk_path + '/' + filename
                        if os.path.exists(moved_package_file):

                            if compressed:
                                report.log_event('Extract file ' + moved_package_file)  
                                extract_file(moved_package_file, wrk_path)
                                folders = os.listdir(wrk_path)

                                for folder in folders:
                                    if os.path.isdir(wrk_path + '/' + folder):
                                        files = os.listdir(wrk_path + '/' + folder)
                                        for file in files:
                                            self.move_file_to_folder(wrk_path + '/' + folder + '/' + file, wrk_path)
                            

                    else:
                        report.log_error('It was not possible to create the work path: ' + wrk_path)
                else:
                    report.log_error(package_file + ' is not a valid package file. It must be a file')
                    if not os.path.exists(self.trash_path):
                        os.makedirs(self.trash_path)
                    if os.path.exists(self.trash_path):  
                        report.log_event('Move ' + package_file + ' to ' + self.trash_path)
                        self.move_file_to_folder(package_file, self.trash_path)
               
        else:
            report.log_error('Invalid package path: ' + self.packages_path)
    
    def move_file_to_folder(self, file_or_folder, dest_path):
        if os.path.isfile(file_or_folder) and os.path.isdir(dest_path) :
            filename = os.path.basename(file_or_folder)
            path = os.path.dirname(file_or_folder)
            if os.path.exists(dest_path + '/' + filename):
            	os.unlink(dest_path + '/' + filename)
            shutil.move(file_or_folder, dest_path)







