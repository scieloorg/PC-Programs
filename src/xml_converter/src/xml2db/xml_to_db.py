import os, shutil, sys
from reuse.input_output.report import Report 

from xml2db.box_folder_document import Document, Documents 
from reuse.files.compressed_file import CompressedFile

import reuse.xml.xml_java as xml_java
from reuse.files.name_file import add_date_to_filename

xml_tree = None
xml_packer = None



class QueueOrganizer:
    def __init__(self, report, tracker, queue_path):
        self.tracker = tracker
        self.report = report
        self.queue_path = queue_path
        self.compressed_file_manager = CompressedFile(self.report)


    def archive_and_extract_files(self, archive_path, extracted_path, report_sender):   
        for compressed in os.listdir(self.queue_path):
            self.tracker.register(compressed, 'begin-queue')
            
            self.report.write('Archive ' + self.queue_path + ' in ' + extracted_path + '/' + compressed, True, False, True)
            self.archive(self.queue_path + '/' + compressed, archive_path)
            
            self.report.write('Extract files from ' + self.queue_path + ' to ' + extracted_path + '/' + compressed, True, False, True)
            self.compressed_file_manager.extract_files(self.queue_path + '/' + compressed, extracted_path + '/' + compressed)
            
            attached_files = []
            text =  'Files in the package\n' + '\n'.join(os.listdir(extracted_path + '/' + compressed))
            self.report.write(text, True, False, False)

            if os.path.exists(archive_path + '/' + compressed):
                self.report.write('Delete ' + self.queue_path + '/' + compressed, True, False, False)
                os.remove(self.queue_path + '/' + compressed)
            self.tracker.register(compressed, 'end-queue')

    def archive(self, filename, archive_path):
        """
        Archive a copy of filename 
        """
        archive_path2 = archive_path + '_previous'
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
        if not os.path.exists(archive_path2):
            os.makedirs(archive_path2)

        if os.path.exists(archive_path):
            name = os.path.basename(filename)
            archived_file = archive_path + '/' + name
            if os.path.exists(archived_file):
                new_name = add_date_to_filename(name, False)
                shutil.copyfile(archived_file, archive_path2 + '/' + new_name)
            shutil.copy(filename, archive_path)

class Reception:
    def __init__(self, input_path, report_sender, msg_template, report_path, tracker, xmlpacker):
        self.input_path = input_path
        self.report_sender = report_sender
        self.report_path  = report_path
        self.tracker = tracker
        self.msg_template = msg_template
        self.xml_packer = xmlpacker
        
    def report_not_processed_packages(self, template_msg):
        items = ''
        for package in os.listdir(self.input_path):
            #items += package + '\n'
            for xml in os.listdir(self.input_path + '/' + package):
                if xml.endswith('.xml'):
                    items += package + '/' + xml + '\n'
        if len(items)>0:
            self.report_sender.send_to_adm(template_msg, items)

    def open_packages(self, document_analyst, document_archiver, img_converter, fulltext_generator):
        for folder in os.listdir(self.input_path):
            package_folder = self.input_path + '/' + folder
            if os.path.isdir(package_folder):
                print('?????????????????')

                package = Package(package_folder, self.report_path + '/' + folder)
                
                self.tracker.register(package.name, 'begin-open_package')
                package.read_package_sender_email()
                
                img_converter.img_to_jpeg(package.package_path, package.package_path)
                
                self.tracker.register(package.name, 'analyze_package')
                folders = document_analyst.analyze_package(package, document_archiver.folder_table_name)
                
                self.tracker.register(package.name, 'put_in_the_box')
                
                for folder in folders:
                    acron = folder.box.acron
                    issue_label = folder.name
                
                    if len(acron) > 0:
                        report_list = package.generate_pmc_folder_and_validation_reports(self.xml_packer, '/img/revistas/' + acron + '/' + issue_label + '/' )

                document_archiver.put_in_the_box(folders, package)
                print('report_list')
                print(folders)
                report_list = document_archiver.return_validation_report_filenames(folders)
                print(report_list)
                
                

                self.tracker.register(package.name, 'send report')
                
                package.report.write(self.report_sender.send_package_evaluation_report(self.msg_template, package.name, [ package.report.summary_filename], report_list, package.package_sender_email))
        

                q_xml = [ f for f in os.listdir(package.package_path) if f.endswith('.xml') ]
                
                if len(q_xml) == 0:
                    for f in os.listdir(package.package_path):
                        os.unlink(package.package_path + '/' + f)
                    package.report.write('Delete work area ' + package.package_path)
                    os.rmdir(package.package_path)
                
                

                self.tracker.register(package.name, 'end-open_package')
   
    
class Package:
    def __init__(self, package_path, report_path):
        
        self.report_path = report_path
        if not os.path.exists(report_path):
            os.makedirs(report_path)

        self.package_path = package_path
        self.name = os.path.basename(package_path)
        
        self.package_sender_email = ''
        
        files = ['detailed.log', 'error.log', 'summarized.txt'] 
        self.report_files = [ report_path + '/' +  self.name + '_' + f for f in files ]
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

    
    def fix_extensions(self):        
        for f in os.listdir(self.package_path):
            extension = f[f.rfind('.'):]
            if extension != extension.lower():
                new_f = f[0:len(f)-len(extension)] + f[len(f)-len(extension):].lower()
                new_name = self.package_path + '/' + new_f
                os.rename(self.package_path + '/' + f, new_name)
                if os.path.exists(new_name):
                    self.report.write('Fixed extension of ' + new_name, False, False, False)
                else:
                    self.report.write('Unable to fix extension of ' + new_name, True, False, False)

    def return_matching_files(self, startswith, extension = ''):
        #pattern = xml_name.replace('.xml', '-')

        startswith = startswith.replace('.fixed', '')
        if '/' in startswith:
            startswith = os.path.basename(startswith) 
        startswith = startswith[0:startswith.rfind('.')]

        if len(extension)>0 and extension[0:1] != '.':
            extension = '.' + extension 

        self.report.write('startswith=' + startswith)
        self.report.write('extension=' + extension)
        self.report.write('files in ' + self.package_path)
        self.report.write('\n'.join(os.listdir(self.package_path)))

        if len(startswith)>0 and len(extension)>0:
            filenames = [ filename for filename in os.listdir(self.package_path) if filename.startswith(startswith) and filename.endswith(extension) ]
        elif len(startswith) == 0 and len(extension) == 0:
            filenames = os.listdir(self.package_path)
        elif len(extension)> 0 :
            filenames = [ filename for filename in os.listdir(self.package_path) if  filename.endswith(extension) ]
        elif len(startswith) > 0:
            filenames = [ filename for filename in os.listdir(self.package_path) if filename.startswith(startswith) ]
        self.report.write(','.join(filenames))
        return filenames

    def generate_pmc_folder_and_validation_reports(self, xml_packer, jpg_path):
        files = []

        self.pmc_package_path = self.package_path.replace('/work/', '/4pmc/')
        self.reports_path = self.package_path.replace('/work/', '/4check/')

        
        
        xml_packer.generate_validation_reports(self.report, self.package_path, self.pmc_package_path, self.reports_path, jpg_path)

        for f in os.listdir(self.reports_path):
            if f.endswith('.html'):
                shutil.move(self.reports_path + '/' + f, self.package_path + '/' + f)
                if  f.endswith('.rep.html'):
                    files.append(self.package_path + '/' + f)
            else:
                print(self.reports_path + '/' + f)
        return files

    def check_files(self):
        self.fix_extensions()
        
        package_files = os.listdir(self.package_path)        
        package_pdf_files = self.return_matching_files('', '.pdf')
        package_xml_files = self.return_matching_files('', '.xml')

        unmatched_pdf = [ pdf for pdf in package_pdf_files if not pdf.replace('.pdf', '.xml') in package_xml_files ]

        self.report.write('XML Files: ' + str(len(package_xml_files)), True)
        self.report.write('PDF Files: ' + str(len(package_pdf_files)), True)

        if len(package_xml_files) == 0:
            self.report.write('All the files in the package: ' + '\n' + '\n'.join(package_files), True, True, False)

        if len(unmatched_pdf) > 0:
            self.report.write('PDF files which there is no corresponding XML file: ' + '\n' + '\n'.join(unmatched_pdf), True, True, False)

        self.report.write('XML Files: \n' + '\n'.join(package_xml_files), True)
        return package_xml_files
    
    
    def check_pdf_file(self, xml_filename):
        pdf_filename = xml_filename.replace('.xml', '.pdf')
        if not os.path.exists(pdf_filename):
            package.report.write(' ! WARNING: Expected ' + os.path.basename(pdf_filename), True, True)


class PackageAnalyzer:
    def __init__(self, xml2json, json2model, registered_titles, all_folders, ahead_articles):
        self.xml2json = xml2json
        self.json2model = json2model
        self.registered_titles = registered_titles
        self.all_folders = all_folders
        self.ahead_articles = ahead_articles
        
        
        
    def analyze_package(self, package, folder_table_name):

        loaded_folders = {}
        
        package_xml_files = package.check_files()
        # load all xml files of the package
        for xml_fname in package_xml_files:
            
            xml_filename = package.package_path + '/' + xml_fname
        
            package.report.write('\n' + '-' * 80 + '\n' + 'File: ' + xml_filename + '\n', True, True, True)
        
            package.check_pdf_file(xml_filename)

            document = self.analyze_document(xml_filename, package, folder_table_name)

        
            if document != None:
                
                loaded_folders[document.folder.box.acron + document.folder.name] = document.folder
                
                if document.folder.documents == None:
                    print('Creating ' + document.folder.box.acron + document.folder.name)
                else:
                    print(document.folder.box.acron + document.folder.name + '=' + str(document.folder.documents.count))
                #document.folder.json_data['122'] = document.folder.documents.count #str(len(document.folder.documents.elements))
                #document.folder.json_data['49'] = document.folder.toc.return_json()
                
            #print(loaded_folders)
        return loaded_folders.values()


    def analyze_document(self, xml_filename, package, folder_table_name):


        generic_document = None


        json_data = self.xml2json.convert(xml_filename, package.report)
        if type(json_data) != type({}):
            package.report.write(' ! ERROR: Invalid JSON ' + xml_filename, False, False, False, json_data)
        else:
            img_files = package.return_matching_files(xml_filename, '.jpg')

            self.json2model.set_data(json_data, xml_filename, package.report)

            publication_title = self.json2model.publication_title
            
            registered = self.registered_titles.return_registered(publication_title, package.report)

            if registered != None:
                selected_folder = self.check_folder(registered, package)
                specific_document = self.json2model.return_doc(selected_folder)
                if not 'ahead' in specific_document.issue.name:
                    specific_document.set_previous_id(self.ahead_articles.return_id(specific_document.doi, specific_document.issue.journal.issn_id, specific_document.titles))
                    
                if specific_document != None:
                    generic_document = Document(specific_document)
                    package.report.write(generic_document.display(), True, True, False)

                    self.json2model.evaluate_data(img_files)
                
                    if generic_document.folder.documents == None:
                        generic_document.folder.documents = Documents()
                    generic_document.folder.documents.insert(generic_document.document, True)
        return generic_document

    def check_folder(self, registered, package, folder_table_name = 'issue'):
        document_folder = self.json2model.return_folder(registered)

        selected_folder = self.all_folders.template(document_folder)
        if selected_folder.status == 'not_registered':
            package.report.write("\n" + ' ! WARNING: '  + selected_folder.display()  + ' is not registered in ' + folder_table_name + '. It must be registered before sending the package to the outsourcing company.' + "\n" , True, True, True )

        incoherences = self.all_folders.return_incoherences(selected_folder, document_folder)
        if len(incoherences) > 0:
            package.report.write(' ! ERROR: There are inconsistencies of data: ', True, True, True)
            for err in incoherences:
                package.report.write(err, True, True, True)

        return selected_folder



class DocumentsArchiver:
    def __init__(self, db_manager, tracker, folder_table_name):
        self.db_manager = db_manager
        self.tracker = tracker
        self.folder_table_name = folder_table_name
        
    def create_table(self, table_name, filename):
        self.db_manager.create_table(table_name, filename)

    def db2json(self, table_name):
        return self.db_manager.db2json(table_name)
   

    def put_in_the_box(self, folders, package):
        return self.db_manager.update(folders, package)

    def return_validation_report_filenames(self, folders):
        print('1')
        return self.db_manager.return_validation_report_filenames(folders)
    #def generate_issue_db_for_proc(self, table_name):
    #    self.db_manager.generate_issue_db_for_proc(table_name)       
    


#JSON_Conversion

class AheadArticles:
    def __init__(self, filename):
        self.filename = filename
        self.doi = {}
        
        self.issn = {}
        self.data = []

        if os.path.isfile(self.filename):
            f = open(self.filename, 'r')
            lines = f.readlines()
            f.close()

        k = 0
        for l in lines:
            if '|' in l:
                pid, issn, doi, title, filename = l.replace('\n', '').split('|')

                self.data.append((pid, issn, doi, title, filename))
                self.doi[doi] = k
                

                if not issn in self.issn.keys():
                    self.issn[issn] = {}

                if issn in self.issn.keys():
                    self.issn[issn][title] = k

                k += 1


    def return_id(self, doi, issn, titles):
        
        if type(titles) == type(''):
            titles = [ titles ]
        
        r = ''
        filename = ''
        if doi in self.doi.keys():
            k = self.doi[doi]
            r = self.data[k][0]
            filename = self.data[k][4]
        elif issn in self.issn.keys():
            for t in titles:
                if t in self.issn[issn].keys():
                    k = self.issn[issn][t]
                    r = self.data[k][0]
                    filename = self.data[k][4]
                    break
        else:
            print(self.doi)

        return r , filename
