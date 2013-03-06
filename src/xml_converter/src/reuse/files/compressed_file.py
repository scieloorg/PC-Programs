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
                if self.__extract__(compressed_file, destination_path):
                    r = True
        if not r:
            self.report.write(compressed_file + ' is not a valid file. It must be a compressed file.', True, True, True)
    
        return r

    def __extract__(self, compressed_file, destination_path):
        r = False
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
        if extract_file(compressed_file, temp_dir):
            # eliminate folders
            for i in os.listdir(temp_dir):
                if os.path.isfile(temp_dir + '/' + i):
                    shutil.copy(temp_dir + '/' + i, destination_path)
                    os.unlink(temp_dir + '/' + i)
                elif os.path.isdir(temp_dir + '/' + i):
                    for f in os.listdir(temp_dir + '/' + i ):
                        if os.path.isfile(temp_dir + '/' + i + '/' + f):
                            shutil.copy(temp_dir + '/' + i + '/' + f, destination_path)
                            os.unlink(temp_dir + '/' + i + '/' + f)
                        else:
                            self.report.write(f + ' is directory and its contents will be ignored.', True, True, True)
                    shutil.rmtree(temp_dir + '/' + i)
            shutil.rmtree(temp_dir)
            r = True
        return r

    def create_temp_dir(self):
        import tempfile
        return tempfile.mkdtemp().replace('\\', '/')
        
    

    
