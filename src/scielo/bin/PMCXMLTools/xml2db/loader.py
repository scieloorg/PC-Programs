import os
import sys
import shutil
from datetime import date
    
from utils.report import Report
from utils.parameters import Parameters
from utils.cisis import CISIS, IDFile
from utils.json2id import JSON2IDFile
from utils.files_uploaded_manager import UploadedFilesManager

from xml2json_converter import XML2JSONConverter
from json2id_article import JSON2IDFile_Article
from json2models import JSON2Models
from journal_issue_article import JournalList, JournalIssues, Journal, Section
from xml_files_set import XMLFilesSet
from xml_folders_set import XMLFoldersSet

from utils.img_converter import ImageConverter
from utils.email_service import EmailService
from utils.configuration import Configuration

class Loader:
    def __init__(self, xml2json_converter, doctype, records_order, json2model, registered_journals, db_manager, xml_folders):
        self.xml2json_converter = xml2json_converter
        self.records_order = records_order

        self.json2model = json2model
        
        self.db_manager = db_manager

        self.xml_folders = xml_folders
        self.doctype = doctype
        self.registered_journals = registered_journals
        self.inproc_issues = JournalIssues()
        

    def return_issue(self, issue):        
        found = self.inproc_issues.get(issue.id)
        if found == None:
            # issue is registered
            found = self.db_manager.registered_issues.get(issue.id)
            if found == None:
                # issue is in new_issues
                # ???
                found = self.db_manager.not_registered_issues.get(issue.id)
                if found == None:
                    found.status = 'not_registered'
                    self.db_manager.not_registered_issues.insert(issue, False)                
            else:
                found.status = 'registered'        
            found = self.inproc_issues.insert(issue, False)
            
        return found

    def return_invalid_value_msg(self, label, invalid_value, correct_value = ''):
        r =  invalid_value + ' is not a valid ' + label 
        if len(correct_value) > 0:
            r += '. Expected: ' + correct_value
        return r 

    def validate_issue(self, correct_issue, issue):
        errors = []
        
        items = {}
        items['ISSN'] = (correct_issue.journal.issn_id, issue.journal.issn_id)
        items['journal title'] = (correct_issue.journal.title, issue.journal.title)
        items['acron'] = (correct_issue.journal.acron, issue.journal.acron)
        items['issue'] = (correct_issue.journal.acron + ' ' + correct_issue.name, issue.journal.acron + ' ' + issue.name)
        items['dateiso'] = (correct_issue.dateiso, issue.dateiso)
        
        for key, item in items.items():
            if item[0] != item[1]:
                errors.append(self.return_invalid_value_msg(key, item[1], item[0]))
        return errors

    def load(self, package):
        loaded_issues = {}
        
        package.fix_xml_extension()
        package.convert_img_to_jpg()

        package_files = os.listdir(package.work_path)
        
        package_pdf_files = [ f for f in package_files if f.endswith('.pdf') ]

        package_xml_files = [ f for f in package_files if f.endswith('.xml') ]

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
            xml_filename = package.work_path + '/' + xml_fname
            
            package.report.write('\n' + '-' * 80 + '\n' + 'File: ' + xml_fname + '\n', True, True, True)
            pdf_filename = xml_filename.replace('.xml', '.pdf')
            if not os.path.exists(pdf_filename):
                package.report.write(' ! WARNING: Missing ' + os.path.basename(pdf_filename), True, True)

            json_data = self.xml2json_converter.convert(xml_filename, self.doctype, package.report)
            
            article = self.load_article(json_data, package, xml_fname)
            if article != None:
                package.report.write(article.display(), True, False, False)
                self.db_manager.store_article(article, self.records_order, xml_filename)
                
                # loaded issue
                loaded_issues[article.issue.journal.acron + article.issue.name] = article.issue
        
        # finish loading, checking issue data
        for key, issue in loaded_issues.items():
            # store articles 
            self.db_manager.store_issue_articles(issue)

            # for GeraPadrao
            self.db_manager.add_to_scilista(issue)

            # archive files
            self.archive_package(package, issue)
            
        
        if len(loaded_issues) > 1:
            package.report.write(' ! ERROR: This package contains data of more than one issue:' + ','.join(loaded_issues.keys()), True, True, True)
    

    def load_article(self, json_data, package, xml_filename):
        article = None
        if type(json_data) != type({}):
            package.report.write(' ! ERROR: Invalid JSON ' + xml_filename, True, True, True, json_data)
        else:
            img_files = package.return_xml_images(xml_filename)

            journal_title = self.json2model.return_article_journal_title(json_data)
            if len(journal_title) == 0:
                package.report.write('Missing journal title in json', True, True)
            else:
                journal = self.registered_journals.find_journal(journal_title)
                if journal == None:
                    titles = ''
                    for t in self.journal_list:
                        titles += ',' + t.title
                    titles = titles[1:]
                    package.report.write(journal_title + ' was not found in title database. '+ '\n' + titles , True, True)
                else:
                    article = self.json2model.return_article(json_data, journal, img_files, xml_filename, package.report)
                    if article == None:
                        package.report.write(' ! ERROR: Invalid ARTICLE JSON ' + xml_filename, True, True, True, json_data)
                        print(json_data)
                    else:
                        package_issue = self.return_issue(article.issue)
                        errors_in_issue = self.validate_issue(package_issue, article.issue)

                        warnings = []
                        if len(errors_in_issue) == 0:
                            article.issue = package_issue
                    
                            section = article.issue.toc.insert(Section(article.section_title), False)
                    
                            article.issue.articles.insert(article, True)
                        else:
                            package.report.write(' ! ERROR: Invalid issue data of ' + xml_filename, True, True, True)
                            for err in errors_in_issue:
                                package.report.write(err, True, True, True)
        
        return article
    
    def archive_package(self, package, issue):
        issue_files = XMLFilesSet(self.xml_folders, issue.journal.acron, issue.name, issue.name)
        
        issue_files.archive_package_file(package.package_file)
        files = os.listdir(package.work_path)
        for filename in files:
            issue_files.move_file_to_path(package.work_path + '/' + filename, issue_files.extracted_package_path)

        files = os.listdir(package.work_path)
        if len(files) == 0:
            package.report.write(' Deleting ' + package.work_path, True, False, True)
            shutil.rmtree(package.work_path)



