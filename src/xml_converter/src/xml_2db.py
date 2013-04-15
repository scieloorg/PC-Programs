import os
import sys
import shutil
from datetime import date, datetime
    

from reuse.services.email_service.email_service import EmailService, EmailMessageTemplate
from reuse.services.email_service.report_sender_xml_process import ReportSender,ReportSenderConfiguration

from reuse.input_output.configuration import Configuration
from reuse.input_output.report import Report
from reuse.input_output.parameters import Parameters
from reuse.input_output.tracker import Tracker

from reuse.xml.xml_json.xml2json import XML2JSON
from reuse.xml.xml_json.xml2json_table import XML2JSONTable

from reuse.xml.xml_tree.xml_tree import XMLTree

from reuse.encoding.entities import Entities
from reuse.encoding.table_entities import  TableEntities
from reuse.encoding.converter_utf8_iso import ConverterUTF8_ISO

from reuse.tables.table_conversion import ConversionTables
from reuse.tables.locations import Locations
from reuse.tables.normalized_affiliations import NormalizedAffiliations

from reuse.files.img_converter import ImageConverter
from reuse.files.name_file import return_path_based_on_date

from reuse.db.isis.cisis import CISIS, IDFile
from reuse.db.isis.json2id import JSON2IDFile

from xml2db.json_functions import JSON_Normalizer 
from xml2db.box_folder_document import AllFolders, Folders

from xml2db.custom.articles.models.journal_issue_article import AllIssues, JournalIssuesList

from xml2db.custom.articles.db.isis.json2article import JSON2Article, AffiliationsHandler, return_journals_list, return_issues_list
from xml2db.custom.articles.db.isis.articles_isis import ISISManager4Articles, Paths
from xml2db.custom.articles.db.isis.articles_json2id import JSON2IDFile_Article


from xml2db.xml_to_db import PackagesProcessor, InformationAnalyst, DocumentsArchiver, QueueOrganizer, AheadArticles

import xml_toolbox as xml_toolbox

#from reuse.xml.xml_java.JavaXMLTransformer import JavaXMLTransformer
from reuse.xml.xml2output.fulltext_generator import FullTextGenerator

# read parameters of execution 
parameter_list = ['script', 'collection' ]         
parameters = Parameters(parameter_list)
if parameters.check_parameters(sys.argv):
    script_name, collection = sys.argv
    
    required = ['SENDER_EMAIL', 'EMAIL_SUBJECT_PREFIX',
     'EMAIL_TEXT', 'FLAG_SEND_EMAIL_TO_XML_PROVIDER', 'ALERT_FORWARD', 
     'FLAG_ATTACH_REPORTS', 'IS_AVAILABLE_EMAIL_SERVICE', 
     'BCC_EMAIL', 'LOG_FILENAME' , 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN', 
     'REPORT_PATH', 'WORK_PATH', 'COL_PROC_SERIAL_PATH', 'PDF_PATH', 'IMG_PATH', 'XML_PATH', 'CISIS_PATH', 'XML2DB_TRACKER_PATH' ]

    valid_conf = False
    if os.path.exists(collection + '.configuration.ini'):
        config = Configuration(collection + '.configuration.ini')
        valid_conf, msg = config.check(required)
    else:
        what_to_do = 'nothing'

        msg = 'There is no ' + collection + '.configuration.ini'
    ####################################

    if not valid_conf:
        print(msg)
    else:
        ####################################
        # instancing reports
        log_filename = config.parameters['LOG_FILENAME']
        err_filename = config.parameters['ERROR_FILENAME']
        summary_filename = config.parameters['SUMMARY_REPORT']

        debug_depth = config.parameters['DEBUG_DEPTH']
        display_on_screen = config.parameters['DISPLAY_MESSAGES_ON_SCREEN']

        report_path = config.parameter('REPORT_PATH') + '/' + return_path_based_on_date()
        if not os.path.exists(report_path):
            os.makedirs(report_path)
    
        files = [ log_filename, err_filename, summary_filename]
        log_filename, err_filename, summary_filename = [ report_path + '/xmlproc_' + f for f in files ]
        report = Report(log_filename, err_filename, summary_filename, int(debug_depth), (display_on_screen == 'yes')) 
    
        # work path
        work_path = config.parameter('WORK_PATH')
        batch_work_path = work_path + '/' + datetime.now().isoformat()[11:16].replace(':','')
        if not os.path.exists(batch_work_path):
            os.makedirs(batch_work_path)

        processing_serial_path = config.parameters['COL_PROC_SERIAL_PATH']

        web_pdf_path = config.parameters['PDF_PATH']
        web_img_path = config.parameters['IMG_PATH']
        web_xml_path = config.parameters['XML_PATH']

        cisis_path = config.parameters['CISIS_PATH']
        

        tracker = Tracker(config.parameter('XML2DB_TRACKER_PATH'), config.parameter('XML2DB_TRACKER_NAME'))

        archive_path = config.parameters['DOWNLOAD_ARCHIVE_PATH'] 
        download_path = config.parameters['DOWNLOAD_PATH'] 
        
        # Tables
        table_entities = TableEntities('reuse/encoding/entities')
        

        #entities = Entities()
        tables = ConversionTables('reuse/tables/tables')
        locations = Locations('reuse/tables/valid_locations.seq')
        normalized_affiliations = NormalizedAffiliations('reuse/tables/valid_affiliations.seq', locations)
        
        xml_tree = XMLTree(table_entities)
        xml2json_table = XML2JSONTable('xml2db/custom/articles/db/isis/_pmcxml2isis.txt')
        xml2json = XML2JSON(xml2json_table, xml_tree)
        
        
        json_normalizer = JSON_Normalizer(tables)
    

        aff_handler = AffiliationsHandler(normalized_affiliations)
        json2articlemodel = JSON2Article(aff_handler, json_normalizer)

        xml_packer = xml_toolbox.XMLPacker(os.getcwd() + '/pmc', os.getcwd() + '/jar')

        #FIXME
        #cisis, idfile, paths, records_order, json2idfile, json2idfile_article
        converter_utf8_iso = ConverterUTF8_ISO()

        app_paths = Paths(processing_serial_path, web_pdf_path, web_xml_path, web_img_path, config.parameter('COL_SCILISTA'))
        db_manager = ISISManager4Articles(CISIS(cisis_path), IDFile(), app_paths, 'ohflc', JSON2IDFile(converter_utf8_iso), JSON2IDFile_Article(JSON2IDFile(converter_utf8_iso)))
        

        documents_archiver = DocumentsArchiver(db_manager, tracker, 'issue')
        documents_archiver.create_table('title', config.parameter('DB_TITLE_FILENAME'))
        documents_archiver.create_table('issue', config.parameter('DB_ISSUE_FILENAME'))
        documents_archiver.create_table('proc_title', config.parameter('COL_PROC_DB_TITLE_FILENAME'))
        documents_archiver.create_table('proc_issue', config.parameter('COL_PROC_DB_ISSUE_FILENAME'))

        
        json_titles = documents_archiver.db2json('title')
        json_boxes = documents_archiver.db2json('issue')
                
        #
        registered_titles = return_journals_list(json_titles)
        registered_boxes = return_issues_list(json_boxes, registered_titles)
        

        all_boxes = AllFolders(registered_boxes, JournalIssuesList(), AllIssues())

        
        email_service = EmailService('', config.parameter('SENDER_EMAIL'), 'localhost', config.parameter('IS_AVAILABLE_EMAIL_SERVICE') == 'yes')
        report_sender_config = ReportSenderConfiguration(config.parameter('BCC_EMAIL'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER') == 'yes', config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        report_sender = ReportSender(email_service, report_sender_config)

        package_eval_msg_template = EmailMessageTemplate(config.parameter('EMAIL_SUBJECT_PREFIX'), config.parameter('EMAIL_TEXT'))
        adm_msg_template = EmailMessageTemplate(config.parameter('EMAIL_SUBJECT_WORK_PATH'), config.parameter('EMAIL_TEXT_WORK_PATH'))
        

        information_analyst = InformationAnalyst(xml2json, json2articlemodel, registered_titles, all_boxes, AheadArticles(config.parameter('AHEAD_LIST')))

        queue_organizer = QueueOrganizer(report, tracker, download_path)
        queue_organizer.archive_and_extract_files(archive_path, batch_work_path, report_sender)

        
        #java_xml_transformer = JavaXMLTransformer(config.parameter('JAVA_PATH'), config.parameter('SAXON_PATH'), config.parameter('VALIDATOR_PATH'))

        pmc_xsl_and_output = Configuration( 'pmc.article.xsl.ini')
        
        xsl_and_output_list = {}
        for k, item in pmc_xsl_and_output.parameters.items():
            pair = item.split(',')
            xsl_and_output_list[k] = {'xsl': pair[0], 'output': pair[1]}
        
        fulltext_generator = FullTextGenerator(xsl_and_output_list)
        if os.path.exists(config.parameter('COL_SCILISTA')):
            os.unlink(config.parameter('COL_SCILISTA'))
        reception = PackagesProcessor(batch_work_path, report_sender, package_eval_msg_template, report_path, tracker, xml_packer)
        reception.open_packages(information_analyst, documents_archiver, ImageConverter(), fulltext_generator)
        reception.report_not_processed_packages(adm_msg_template)


        print('-' * 80)
        print('Check report files:  ')
        print('Errors report: ' + err_filename)
        print('Summarized report: ' + summary_filename)

        print('Detailed report: ' + log_filename)
        print('Reports for each package of XML files in ' + batch_work_path)



