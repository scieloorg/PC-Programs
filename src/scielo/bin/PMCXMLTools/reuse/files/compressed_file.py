import os
import shutil



from files_extractor import extract_file, is_compressed_file


class CompressedFile:
    def __init__(self, report):
    	self.report = report

    def extract_files(self, compressed_file, destination_path):
        """
        Extract files to destination_path from compressed files that are in compressed_path 
        """
        r = False
        

        
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        
        self.report.write('package file: ' + compressed_file, True, False, True)
        
        if os.path.isfile(compressed_file):
            if is_compressed_file(compressed_file):

                self.report.write('Extract ' + compressed_file + ' to ' + destination_path, True, False, True)  
                self.__extract__(compressed_file, destination_path)

                
                    
            else:
                self.report.write(compressed_file + ' is not a valid package file. It must be a compressed file.', True, True, True)

        else:
            self.report.write(compressed_file + ' is not a valid package file. It must be a compressed file.', True, True, True)
    
        return r

    def __extract__(self, compressed_file, destination_path):
        # create destination path
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        # delete content of destination path
        if os.path.exists(destination_path):
            for i in os.listdir(destination_path):
                os.unlink(destination_path + '/' + i)
        # create tempdir
        temp_dir = self.create_temp_dir()
        # extract in tempdir
        extract_file(compressed_file, temp_dir)
        # eliminate folders
        for i in os.listdir(temp_dir):
            if os.path.isfile(temp_dir + '/' + i):
                shutil.copy(temp_dir + '/' + i, destination_path)
                os.unlink(temp_dir + '/' + i)
            elif os.path.isdir(temp_dir + '/' + i):
                for f in os.listdir(temp_dir + '/' + i ):
                    shutil.copy(temp_dir + '/' + i + '/' + f, destination_path)
                    os.unlink(temp_dir + '/' + i + '/' + f)
                shutil.rmtree(temp_dir + '/' + i)
        shutil.rmtree(temp_dir)

    def create_temp_dir(self):
        import tempfile
        return tempfile.mkdtemp().replace('\\', '/')
        
    

    
    def backup(self, package_file, backup_path):
        """
        Make a backup of package_file in compressed_path + '.bkp/' + date 
        """
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
