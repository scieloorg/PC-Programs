import shutil
import os

class PMCXML_FilesSet:

    def __init__(self, main_path, journal_folder, issue_folder, db_name):
        path = main_path + '/' + journal_folder + '/' + issue_folder + '/pmc'
        
        self.package_path = path + '/pmc_package_source' 
        self.extracted_package_path = path + '/pmc_package_extracted' 
        self.db_path = path + '/pmc_base' 
        
        #self.xml_path = path + '/xml' 
        #self.img_path = path + '/pmc_img' 
        #self.pdf_path = path + '/pmc_pdf' 
        

        self.db_name = db_name

        self.db_filename = self.db_path + '/' + db_name
        
        self.log_filename = self.db_path + '/' + db_name + '.log'
        self.err_filename = self.db_path + '/' + db_name + '.err.log'
        
    def prepare_db_folder(self):
        self.clean_folder(self.db_path, ['.id', '.mst', '.xrf', '.log', ])
    
    def copy_file_to_path(self, filename, dest_path):
        f = os.path.basename(filename)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        shutil.copyfile(filename, dest_path + '/' + f)
        return os.path.exists(dest_path + '/' + f)
    
    def copy_extracted_files_to_their_paths(self, xml_filename):
        count = 0
        f = os.path.basename(xml_filename).replace('.xml', '')
        path = os.path.dirname(xml_filename)
        matched_files = [ filename for filename in os.listdir(path) if f in filename ]
        for matched_file in matched_files:
            if self.copy_file_to_path(path + '/' + matched_file, self.extracted_package_path):
                count += 1
        return (count == len(matched_files))

    def move_file_to_path(self, filename, dest_path):
        f = os.path.basename(filename)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        if os.path.exists(dest_path + '/' + f):
            os.unlink(dest_path + '/' + f)
        shutil.move(filename, dest_path)
        return os.path.exists(dest_path + '/' + f)
    
    def move_extracted_files_to_their_paths(self, xml_filename):
        count = 0
        f = os.path.basename(xml_filename).replace('.xml', '') + '-'
        path = os.path.dirname(xml_filename)
        matched_files = [ filename for filename in os.listdir(path) if f in filename ]
        matched_files.append(os.path.basename(xml_filename))
        for matched_file in matched_files:
            if self.move_file_to_path(path + '/' + matched_file, self.extracted_package_path):
                count += 1
        return (count == len(matched_files))

    def clean_folder(self, path, array_extension):
        if os.path.exists(path):
            files = os.listdir(path)
            for f in files:
                print('deleting ' + path + '/' + f + '?')
                ext = f[f.rfind('.'):]
                if ext in array_extension:
                    print('deleting ' + path + '/' + f)
                    os.remove(path + '/' + f)
        else:
            os.makedirs(path)
    