
from ..input_output.report import Report 

class Reception:
    def __init__(self, input_path, report_sender, report_path, tracker):
        self.input_path = input_path
        self.report_sender = report_sender
        self.report_path  = report_path
        self.tracker = tracker

    def open_packages(self, document_analyst, shelves_organizer):
        for folder in os.listdir(self.input_path):
            package_folder = self.input_path + '/' + folder
            if os.path.isdir(package_folder):
                package = Package(package_folder, self.report_path + '/' + folder )
                
                self.tracker.register(package.name, 'open package')
                package.read_package_sender_email()
                
                self.tracker.register(package.name, 'analyze_package')
                boxes = document_analyst.analyze_package(package)
                
                self.tracker.register(package.name, 'put_on_the_shelves')
                shelves_organizer.put_on_the_shelf(boxes, package)

                self.tracker.register(package.name, 'send report')
                self.send_report(package)
                
                self.tracker.register(package.name, 'end')
                
    
    def send_report(self, package):
        self.report_sender.send_report(package.name, package.package_sender_email, '', [ package.report.summary_filename, package.report.err_filename ], [] )

class ShelvesOrganizer:
    def __init__(self, db):
        self.db = db

    def put_on_the_shelf(self, box, package):
        self.db.put_on_the_shelf(box, package)

    #def archive_package(self, package):
    #    self.db.archive_package(package)

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
        if '/' in startswith:
            startswith = os.path.basename(startswith) 
        if extension[0:1] != '.':
            extension = '.' + extension
        if len(startswith)>0 and len(extension)>0:
            filenames = [ filename for filename in os.listdir(self.package_path) if filename.startswith(startswith) and filename.endswith(extension) ]
        elif len(startswith) == 0 and len(extension) == 0:
            filenames = os.listdir(self.package_path)
        elif len(extension)> 0 :
            filenames = [ filename for filename in os.listdir(self.package_path) if  filename.endswith(extension) ]
        elif len(startswith) == 0:
            filenames = [ filename for filename in os.listdir(self.package_path) if filename.startswith(startswith) ]

        return list(set(filenames))



class DocumentAnalyst:
    def __init__(self, xml2json, json2model, registered_titles, boxes):
        self.xml2json = xml2json
        self.json2model = json2model
        self.registered_titles = registered_titles
        self.boxes = boxes
        
        
    def analyze_package(self, package):

        loaded_boxes = {}
        
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
            
            xml_filename = package.package_path + '/' + xml_fname
            
            package.report.write('\n' + '-' * 80 + '\n' + 'File: ' + xml_fname + '\n', True, True, True)
            pdf_filename = xml_filename.replace('.xml', '.pdf')
            if not os.path.exists(pdf_filename):
                package.report.write(' ! WARNING: Expected ' + os.path.basename(pdf_filename), True, True)

            
            document = self.analyze_document(xml_filename, package)

        
            if document != None:
                loaded_boxes[document.box.title.acron + document.box.name] = document.box
            
        return loaded_boxes

    def analyze_document(self, xml_filename, package):
        json_data = self.xml2json.convert(xml_filename, package.report)
        if type(json_data) != type({}):
            package.report.write(' ! ERROR: Invalid JSON ' + xml_filename, False, False, False, json_data)
        else:
            img_files = package.return_matching_files(xml_filename, '.jpg')

            self.json2model.set_data(json_data, xml_filename, package.report)

            publication_title = self.json2model.publication_title
            
            publication = self.registered_titles.return_valid_publication_title(publication_title, package.report)
            
            document = None             
            if publication != None:
                document, errors, warnings, refcount = self.json2model.return_document(publication, img_files)
                

                if document != None:
                    package.report.write(document.display(), True, False, False)

                    box = self.boxes.box_template(document.box)
                    if box.status == 'not_registered':
                        package.report.write("\n" + ' ! WARNING: '  + issue.journal.acron +  ' ' + issue.name  + ' is not registered yet.' + "\n" , True, True, True )
     

                    incoherences = self.boxes.return_incoherences(box, document.box)

                    if len(incoherences) == 0:
                        document.box = box
                
                        section = document.box.toc.insert(document.section, False)
                
                        document.box.documents.insert(document, True)
                    else:
                        package.report.write(' ! ERROR: There are inconsistencies of data ' + xml_filename, True, True, True)
                        for err in incoherences:
                            package.report.write(err, True, True, True)
        
                    document.box.json_data['122'] = str(len(document.box.documents.elements))
                    document.box.json_data['49'] = document.box.toc.return_json()
        return document




#JSON_Conversion

