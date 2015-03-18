import os, shutil, sys
from reuse.input_output.report import Report 

from xml2db.box_folder_document import Document, Documents, Box
from reuse.files.compressed_file import CompressedFile

from reuse.files.name_file import add_date_to_filename

xml_tree = None

import xmlpkgmker

xmlpkgmker.DEBUG = 'ON'
xml_validations = xmlpkgmker.XMLValidations('scielo', None, xmlpkgmker.entities_table)


class QueueOrganizer:
    def __init__(self, report, tracker, queue_path):
        self.tracker = tracker
        self.report = report
        self.queue_path = queue_path
        self.compressed_file_manager = CompressedFile(self.report)
        self.temp_dir = os.path.dirname(self.queue_path) + '/tmp'

    def archive_and_extract_files(self, archive_path, work_path, report_sender):   

        for package_folder in os.listdir(work_path):
            to_delete = work_path + '/' + package_folder
            if os.path.isfile(to_delete):
                os.unlink(to_delete)
            elif os.path.isdir(to_delete):
                shutil.rmtree(to_delete)

        for zip_filename in os.listdir(self.queue_path):
            self.tracker.register(zip_filename, 'begin-queue')

            package_filename = self.queue_path + '/' + zip_filename
            package_path = work_path + '/' + zip_filename

            if os.path.exists(package_path):
                for f in os.listdir(package_path):
                    os.unlink(package_path + '/' + f)
                
            self.report.write('Archive ' + package_filename + ' in ' + archive_path, True, False, True)

            self.report.write(str(os.stat(package_filename).st_size), True, False, True)
            self.archive(package_filename, archive_path)
            
            self.report.write('Extract files from ' + package_filename + ' to ' + package_path, True, False, True)
            self.compressed_file_manager.extract_files(package_filename, package_path, self.temp_dir)
            
            
            text =  'Files in the package\n' + '\n'.join(os.listdir(package_path))
            self.report.write(text, True, False, False)

            if os.path.exists(archive_path + '/' + zip_filename):
                self.report.write('Delete ' + package_filename, True, False, False)
                os.unlink(package_filename)
            self.tracker.register(zip_filename, 'end-queue')

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
                #shutil.copyfile(archived_file, archive_path2 + '/' + new_name)
            shutil.copy(filename, archive_path)

class PackagesProcessor:
    def __init__(self, input_path, report_sender, msg_template, report_path, tracker, xmlpacker):
        self.input_path = input_path
        self.report_sender = report_sender
        self.report_path  = report_path
        self.tracker = tracker
        self.msg_template = msg_template
        self.xml_packer = xmlpacker
        
    def report_not_processed_packages(self, template_msg):
        items = []
        for package_folder in os.listdir(self.input_path):            
            for xml in os.listdir(self.input_path + '/' + package_folder):
                if xml.endswith('.xml'):
                    items.append( self.input_path + '/' + package_folder + '/' + xml )
                os.unlink(self.input_path + '/' + package_folder + '/' + xml)
            os.rmdir(self.input_path + '/' + package_folder)
        if len(items)>0:
            self.report_sender.send_to_adm(template_msg, '\n'.join(items))
            

    def open_packages(self, information_analyst, documents_archiver, img_converter, fulltext_generator):
        information_analyst.xml_packer = self.xml_packer
        from datetime import datetime
        for folder in os.listdir(self.input_path):
            package_folder = self.input_path + '/' + folder
            if os.path.isdir(package_folder):
                package = Package(package_folder, self.report_path + '/' + folder)
                self.tracker.register(package.name, 'begin-open_package')
                now = datetime.now().isoformat()
                package.read_package_sender_email()
                self.tracker.register(package.name, 'img to jpg')
                errors = img_converter.img_to_jpeg(package.package_path, package.package_path)
                if len(errors) > 0:
                    package.report.write('Some files were unable to convert:\n' + '\n'.join(errors), True, True)
                self.tracker.register(package.name, 'analyze_package')
                fatal_errors, folders = information_analyst.analyze_package(package, documents_archiver.folder_table_name)

                package.report.write('='*80, True, True)

                if len(fatal_errors) == 0:
                    documents_archiver.put_in_the_box(folders, package)
                else:
                    package.report.result += 'FATAL ERRORS: ' + str(len(fatal_errors)) + '\nUNABLE TO PUBLISH THIS PACKAGE.'

                package.report.write('='*80 + '\n' + now + '\n' + datetime.now().isoformat(), True, True)

                result = '\n' + '='*80 + '\n' + package.report.result + '\n' + '='*80 + '\n'
                package.report.write(result, True)
                result += open(package.report.summary_filename, 'r').read()

                open(package.report.summary_filename, 'w').write(result)

                self.tracker.register(package.name, 'send report')
                package.report.write(self.report_sender.send_package_evaluation_report(self.msg_template, package.name, [package.report.summary_filename], information_analyst.reports_to_attach, package.package_sender_email))

                q_xml = [f for f in os.listdir(package.package_path) if f.endswith('.xml')]
                if len(q_xml) == 0:
                    for f in os.listdir(package.package_path):
                        os.unlink(package.package_path + '/' + f)
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
        self.report_files = [report_path + '/' + self.name + '_' + f for f in files]
        log_filename, err_filename, summary_filename = self.report_files
        self.report = Report(log_filename, err_filename, summary_filename, 0, False)
        self.report_files_to_send = [summary_filename, err_filename]
        self.identify_files()
        
    def read_package_sender_email(self):
        if os.path.exists(self.package_path + '/email.txt'):
            f = open(self.package_path + '/email.txt', 'r')
            content = f.readlines()
            f.close()

            content = [item for item in content if item]
            self.package_sender_email = ','.join(content).replace('\n', '').replace('\r', '').replace(';', ',').replace('\xef\xbb\xbf', '').rstrip()

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
        def filename_matches(filename, startswith):
            return filename.startswith(startswith + '.') or filename.startswith(startswith + '-')
            
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
            filenames = [ filename for filename in os.listdir(self.package_path) if filename_matches(filename, startswith) and filename.endswith(extension) ]
        elif len(startswith) == 0 and len(extension) == 0:
            filenames = os.listdir(self.package_path)
        elif len(extension)> 0 :
            filenames = [ filename for filename in os.listdir(self.package_path) if filename.endswith(extension) ]
        elif len(startswith) > 0:
            filenames = [ filename for filename in os.listdir(self.package_path) if filename_matches(filename, startswith) ]
        self.report.write(','.join(filenames))
        return filenames



    def identify_files(self):
        self.fix_extensions()
        
        self.package_files = os.listdir(self.package_path)        
        self.package_pdf_files = self.return_matching_files('', '.pdf')
        self.package_xml_files = self.return_matching_files('', '.xml')

        unmatched_pdf = [ pdf for pdf in self.package_pdf_files if not pdf.replace('.pdf', '.xml') in self.package_xml_files ]

        self.report.write('XML Files: ' + str(len(self.package_xml_files)), True)
        self.report.write('PDF Files: ' + str(len(self.package_pdf_files)), True)

        if len(self.package_xml_files) == 0:
            self.report.write('All the files in the package: ' + '\n' + '\n'.join(self.package_files), True, True, False)

        if len(unmatched_pdf) > 0:
            self.report.write('PDF files which there is no corresponding XML file: ' + '\n' + '\n'.join(unmatched_pdf), True, True, False)

        self.report.write('XML Files: \n' + '\n'.join(sorted(self.package_xml_files)), True)
        
    
    def check_pdf_file(self, xml_filename):
        pdf_filename = xml_filename.replace('.xml', '.pdf')
        if not os.path.exists(pdf_filename):
            self.report.write(' ! WARNING: Expected ' + os.path.basename(pdf_filename), True, True)




class InformationAnalyst:
    def __init__(self, xml2json, json2model, registered_titles, all_folders, ahead_articles):
        self.xml2json = xml2json
        self.json2model = json2model
        self.registered_titles = registered_titles
        self.all_folders = all_folders
        self.ahead_articles = ahead_articles

    def analyze_package(self, package, folder_table_name):
        fatal_errors = []
        loaded_folders = {}

       # load all xml files of the package
        self.reports_to_attach = []
        for xml_fname in package.package_xml_files:
            xml_filename = package.package_path + '/' + xml_fname        
            package.report.write('\n' + '-' * 80 + '\n' + 'File: ' + xml_fname + '\n', True, True, True)
            package.check_pdf_file(xml_filename)
            if self.check_and_load(xml_filename, package):
                fe, document = self.process_document(xml_filename, package, folder_table_name)
                fatal_errors += fe
                if document != None:
                    loaded_folders[document.folder.box.acron + document.folder.name] = document.folder
        return (fatal_errors, loaded_folders.values())

    def check_and_load(self, xml_filename, package):
        is_valid_xml = self.check_xml_file(xml_filename, package)
        
        is_well_formed = self.extract_data(xml_filename, package.report)
        
        if not is_well_formed:
            package.report.write('XML file was not well formed. Unable to read it', True, True)
            #validation_path = package.package_path.replace('/work/', '/4check/')
            #shutil.copyfile(xml_filename, validation_path)
            #self.reports_to_attach.append(validation_path + '/' + os.path.basename(xml_filename))
            self.reports_to_attach.append(xml_filename)
        return is_well_formed

    def check_xml_file(self, xml_filename, package):
        """
        """
        validation_path = package.package_path.replace('/work/', '/4check/')
        xml_pkg_path = validation_path
        report_path = validation_path
        preview_path = validation_path

        curr_name = os.path.basename(xml_filename).replace('.xml', '')
        pkg_files = xmlpkgmker.ValidationFiles(xml_pkg_path, report_path, preview_path)
        pkg_files.name(curr_name, new_name=curr_name)
        pkg_files.html_preview = None
        pkg_files.xml_output = None
        img_path = ''

        is_w, is_dtd_valid, is_style_valid = xml_validations.check_list(xml_filename, pkg_files, img_path)
        if is_dtd_valid:
            package.report.write('is_valid_xml')
            if not is_style_valid:
                package.report.write('not is_valid_style')
                if os.path.exists(pkg_files.style_checker_report):
                    package.report.write('XML file has style errors. Read the attached file ' + os.path.basename(pkg_files.style_checker_report), True, True)
                    self.reports_to_attach.append(pkg_files.style_checker_report)
        else:
            package.report.write('not is_valid_xml')
            if os.path.exists(pkg_files.dtd_validation_report):
                package.report.write('XML file is not according to DTD. Read the attached file ' + os.path.basename(pkg_files.dtd_validation_report), True, True)
                self.reports_to_attach.append(pkg_files.dtd_validation_report)
        return is_style_valid

    def old_check_xml_file(self, xml_filename, package):               
        validation_path = package.package_path.replace('/work/', '/4check/')
        
        scielo_html_validation_report  = validation_path + '/' + os.path.basename(xml_filename).replace('.xml', '.rep.html')
        scielo_html_preview  =  validation_path + '/' + 'preview.html'
        pmc_xml_local =  validation_path + '/' + 'pmc.xml'


        
        self.xml_packer.checker.validator_scielo.set_output_filenames(xml_filename, validation_path, scielo_html_validation_report, scielo_html_preview, pmc_xml_local)
        err_filename = self.xml_packer.checker.validator_scielo.err_filename.replace('.err.tmp', '.err.txt')
        if os.path.exists(err_filename):
            os.unlink(err_filename)

        is_valid_xml, is_valid_style = self.xml_packer.checker.validator_scielo.validate_xml_and_style(package.report)

        if is_valid_xml:
            package.report.write('is_valid_xml')
            if not is_valid_style:
                package.report.write('not is_valid_style')
                if os.path.exists(self.xml_packer.checker.validator_scielo.html_report):
                    package.report.write('XML file has style errors. Read the attached file ' + os.path.basename(self.xml_packer.checker.validator_scielo.html_report), True, True)
                    self.reports_to_attach.append(self.xml_packer.checker.validator_scielo.html_report)
                else:
                    package.report.write('Unable to create style report ' + os.path.basename(self.xml_packer.checker.validator_scielo.html_report), True, True)
                    if os.path.exists(self.xml_packer.checker.validator_scielo.err_filename):
                        self.reports_to_attach.append(self.xml_packer.checker.validator_scielo.err_filename)

        else:
            package.report.write('not is_valid_xml')
            if os.path.exists(self.xml_packer.checker.validator_scielo.err_filename):
                err_filename = self.xml_packer.checker.validator_scielo.err_filename.replace('.err.tmp', '.err.txt')
                package.report.write('XML file is not according to DTD. Read the attached file ' + os.path.basename(err_filename), True, True)
                shutil.copyfile(self.xml_packer.checker.validator_scielo.err_filename, err_filename)
                self.reports_to_attach.append(err_filename)

        return is_valid_xml


    def extract_data(self, xml_filename, package_report):
        r = False
        json_data = self.xml2json.convert(xml_filename, package_report)
        if type(json_data) != type({}):
            package_report.write(' ! ERROR: Invalid JSON ' + xml_filename, False, False, False, json_data)
        else:            
            self.json2model.set_data(json_data, xml_filename, package_report)

            r = True
        return r


    def process_document(self, xml_filename, package, folder_table_name):
        fatal_errors = []
        generic_document = None
        if self.extract_data(xml_filename, package.report):
            publication_title = self.json2model.publication_title
            registered = None
            if len(publication_title) > 0:
                registered = self.registered_titles.return_registered(publication_title)
            if registered == None:
                package.report.write('Invalid publication title:' + publication_title, True, True)
            else:
                document_folder = self.json2model.return_folder(registered)

                selected_folder = self.check_folder(document_folder, package)
                if selected_folder.status == 'registered':
                    specific_document = self.json2model.return_doc(selected_folder)

                    if specific_document != None:
                        if not specific_document.doi == '':
                            if not 'ahead' in specific_document.issue.name:
                                pid, fname = self.ahead_articles.return_id_and_filename(specific_document.doi, specific_document.issue.journal.issn_id, specific_document.titles)
                                specific_document.set_previous_id(pid)
                        generic_document = Document(specific_document)
                        package.report.write(generic_document.display(), True, True, False)

                        img_files = package.return_matching_files(xml_filename, '.jpg')
                        fatal_errors, e, w, ref_count = self.json2model.evaluate_data(img_files)
                        if generic_document.folder.documents == None:
                            generic_document.folder.documents = Documents()

                        if specific_document.doi == '' and specific_document.issue.name[-2:] != 'pr':
                            fatal_errors.append('FATAL ERROR: Missing DOI')
                            package.report.write('FATAL ERROR: Missing DOI', True, True)
                        else:
                            if not generic_document.folder.documents.insert(generic_document.document, False):
                                package.report.write('FATAL ERROR: This document has doi (' + generic_document.document.doi + ') or order(' + generic_document.document.order + ') of another document.', True, True)
                                fatal_errors.append('FATAL ERROR: This document has doi (' + generic_document.document.doi + ') or order(' + generic_document.document.order + ') of another document.')

                else:
                    package.report.write('', True, True)
        return (fatal_errors, generic_document)

    def check_folder(self, document_folder, package, folder_table_name = 'issue'):
        
        selected_folder = self.all_folders.template(document_folder)
        
        package.report.write(selected_folder.status)

        if selected_folder.status != 'registered':
            package.report.write("\n" + ' ! ERROR: '  + selected_folder.display()  + ' is not registered in ' + folder_table_name + '. It must be registered before sending the package to the outsourcing company.' + "\n" , True, True, True )

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


#JSON_Conversion

class AheadArticles:
    def __init__(self, filename):
        self.filename = filename
        self.doi = {}
        
        self.issn = {}
        self.data = []
        lines = []
        if os.path.isfile(self.filename):
            f = open(self.filename, 'r')
            lines = f.readlines()
            f.close()

        k = 0
        for l in lines:
            if '|' in l:
                splited = l.split('|')
                if len(splited) == 5:
                    pid, issn, doi, title, filename = l.replace('\n', '').split('|')

                    self.data.append((pid, issn, doi, title, filename))
                    self.doi[doi] = k
                

                    if not issn in self.issn.keys():
                        self.issn[issn] = {}

                    if issn in self.issn.keys():
                        self.issn[issn][title] = k

                    k += 1

    def return_id_and_filename(self, doi, issn, titles):
        print(doi)
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
        
        if not len(r) == 23:
            r = ''
        print(r)

        return r , filename
