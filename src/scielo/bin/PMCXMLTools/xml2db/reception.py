
from .. import input_output.report 

class Reception:
    def __init__(self, input_path, report_sender, report_path):
        self.input_path = input_path
        self.report_sender = report_sender
        self.report_path  = report_path

    def open_packages(self, loader, db):
        for folder in os.listdir(self.input_path):
            package_folder = self.input_path + '/' + folder
            if os.path.isdir(package_folder):
                package = Package(package_folder, self.report_path + '/' + folder )
                package.open_package()
                package.read_package_sender_email()
                issue = loader.load_package(package)
                db.store(issue)

class Package:
    def __init__(self, package_path, report_path, img_converter):
        self.img_converter = img_converter
        self.report_path = report_path
        if not os.path.exists(report_path):
            os.makedirs(report_path)

        self.package_path = package_path
        
        self.package_sender_email = ''
        

        files = ['detailed.log', 'error.log', 'summarized.txt'] 
        self.report_files = [ report_path + '/' +  self.package_name + '_' + f for f in files ]
        log_filename, err_filename, summary_filename = self.report_files
        self.report = Report(log_filename, err_filename, summary_filename, 0, False) 
        self.report_files_to_send = [ summary_filename, err_filename ]
        
        
    def read_package_sender_email(self):
        if os.path.exists(self.package_path + '/email.txt'):
            f = open(self.package_path + '/email.txt', 'r')
            self.package_sender_email = f.read()
            self.package_sender_email = self.package_sender_email.replace(';', ',')
            f.close()
        return self.package_sender_email

    def convert_img_to_jpg(self):
        self.img_converter.img_to_jpeg(self.package_path, self.package_path)

    def fix_extensions(self):
        
        for f in os.listdir(self.package_path):
            extension = f[f.rfind('.'):]
            if extension != extension.lower():
                new_f = f[0:len(f)-len(extension)] + f[len(f)-len(extension):].lower()
                new_name = self.package_path + '/' + new_f
                shutil.rename(self.package_path + '/' + f, new_name)
                if os.path.exists(new_name):
                    self.report.write('Fixed extension of ' + new_name, False, False, False)
                else:
                    self.report.write('Unable to fix extension of ' + new_name, True, False, False)

    def return_matching_files(self, startswith, extension):
        #pattern = xml_name.replace('.xml', '-')
        if len(startswith)>0 and len(extension)>0:
            filenames = [ filename for filename in os.listdir(self.package_path) if filename.startswith(startswith) and filename.endswith(extension) ]
        elif len(startswith) == 0 and len(extension) == 0:
            filenames = os.listdir(self.package_path)
        elif len(extension)> 0 :
            filenames = [ filename for filename in os.listdir(self.package_path) if  filename.endswith(extension) ]
        elif len(startswith) == 0:
            filenames = [ filename for filename in os.listdir(self.package_path) if filename.startswith(startswith) ]

        return list(set(filenames))

class Loader:
    def __init__(self, xml2json, json2model, registered_journals):
        self.xml2json = xml2json
        self.json2model = json2model
        self.registered_journals = registered_journals
        
        
    def load_package(self, package):

        loaded_issues = {}
        
        package.fix_extensions()
        package.convert_img_to_jpg()

        package_files = os.listdir(package.package_path)
        
        package_pdf_files = package.return_matching_files('', '.pdf')

        package_xml_files = package.return_matching_files('', '.xml')

        unmatched_pdf = [ pdf for pdf in package_pdf_files if not pdf.replace('.pdf', '.xml') in package_xml_files ]

        package.report.write('XML Files: ' + str(len(package_xml_files)), True)
        package.report.write('PDF Files: ' + str(len(package_pdf_files)), True)

        if len(package_xml_files) == 0:
            package.report.write('All the files in the package: ' + '\n' + '\n'.join(package_files), False, True, False)

        if len(unmatched_pdf) > 0:
            package.report.write('PDF files which there is no corresponding XML file: ' + '\n' + '\n'.join(unmatched_pdf), True, True, False)

        # load all xml files of the package
        for xml_fname in package_xml_files:
            issue = None
            xml_filename = package.package_path + '/' + xml_fname
            
            package.report.write('\n' + '-' * 80 + '\n' + 'File: ' + xml_fname + '\n', True, True, True)
            pdf_filename = xml_filename.replace('.xml', '.pdf')
            if not os.path.exists(pdf_filename):
                package.report.write(' ! WARNING: Expected ' + os.path.basename(pdf_filename), True, True)

            json_data = self.xml2json.convert(xml_filename, package.report)
            
            document = self.load_document(json_data, package, xml_fname)
            if document != None:
                package.report.write(document.display(), True, False, False)
                #self.db_manager.store_document(document, self.records_order, xml_filename)
                
                # loaded issue
                loaded_issues[document.issue.journal.acron + document.issue.name] = document.issue
        
        # finish loading, checking issue data
        #for key, issue in loaded_issues.items():
            # store documents 
            #self.db_manager.store_issue_documents(issue)

            # for GeraPadrao
            #self.db_manager.add_to_scilista(issue)

            # archive files
            #self.archive_package(package, issue)
            
        
        #if len(loaded_issues) > 1:
        #    package.report.write(' ! ERROR: This package contains data of more than one issue:' + ','.join(loaded_issues.keys()), True, True, True)
        return loaded_issues