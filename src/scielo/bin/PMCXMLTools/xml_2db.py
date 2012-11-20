import os
import sys
import shutil
from datetime import date
    

from reuse.services.email_service.email_service import EmailService
from reuse.services.email_service.report_sender import ReportSender, MessageType


from reuse.input_output.configuration import Configuration
from reuse.input_output.report import Report
from reuse.input_output.parameters import Parameters
from reuse.input_output.tracker import Tracker

from reuse.xml.xml_json.xml2json import XML2JSON
from reuse.xml.xml_json.xml2json_table import XML2JSONTable

from reuse.xml.xml_tree.xml_tree import XMLTree

from reuse.encoding.entities import Entities
from reuse.encoding.converter_utf8_iso import ConverterUTF8_ISO

from reuse.tables.table_conversion import ConversionTables
from reuse.tables.locations import Locations
from reuse.tables.normalized_affiliations import NormalizedAffiliations


from reuse.db.isis.cisis import CISIS, IDFile
from reuse.db.isis.json2id import JSON2IDFile


from xml2db.models.json2models import JSON_Models
from xml2db.models.json_functions import JSON_Normalizer, JSON_Dates, JSON_Values

from xml2db.articles.models.json2article import JSON_Articles_Models, AffiliationsHandler
from xml2db.articles.db.isis.articles_isis import ISISArticle, Paths
from xml2db.articles.db.isis.articles_json2id import JSON2IDFile_Article
from xml2db.articles.db.articles_db import DBArticles
from xml2db.reception import Reception, DocumentAnalyst, ShelvesOrganizer



# read parameters of execution 
parameter_list = ['script', 'collection' ]         
parameters = Parameters(parameter_list)
if parameters.check_parameters(sys.argv):
    script_name, collection = sys.argv
    
    required = ['SENDER_EMAIL', 'EMAIL_SUBJECT_PREFIX',
     'EMAIL_TEXT', 'FLAG_SEND_EMAIL_TO_XML_PROVIDER', 'ALERT_FORWARD', 
     'FLAG_ATTACH_REPORTS', 'IS_AVAILABLE_EMAIL_SERVICE', 
     'BCC_EMAIL', 'LOG_FILENAME' , 'ERROR_FILENAME', 'SUMMARY_REPORT', 'DEBUG_DEPTH', 'DISPLAY_MESSAGES_ON_SCREEN', 
     'REPORT_PATH', 'WORK_PATH', 'SERIAL_PROC_PATH', 'PDF_PATH', 'IMG_PATH', 'XML_PATH', 'CISIS_PATH', 'XML2DB_TRACKER_PATH' ]

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

        report_path = config.parameter('REPORT_PATH') + '/' + date.today().isoformat()
        if not os.path.exists(report_path):
            os.makedirs(report_path)
    
        files = [ log_filename, err_filename, summary_filename]
    
        # work path
        work_path = config.parameter('WORK_PATH')
        

        processing_serial_path = config.parameters['SERIAL_PROC_PATH']

        web_pdf_path = config.parameters['PDF_PATH']
        web_img_path = config.parameters['IMG_PATH']
        web_xml_path = config.parameters['XML_PATH']

        cisis_path = config.parameters['CISIS_PATH']
        

        tracker = Tracker(config.parameter('XML2DB_TRACKER_PATH'))


        # Tables
        entities = Entities('reuse/encoding/entities')
        tables = ConversionTables('reuse/tables/tables')
        locations = Locations('reuse/tables/valid_locations.seq')
        normalized_affiliations = NormalizedAffiliations('reuse/tables/valid_affiliations.seq', locations)
        
        xml_tree = XMLTree(entities)
        xml2json_table = XML2JSONTable('reuse/xml/xml_json/_pmcxml2isis.txt')
        xml2json = XML2JSON(xml2json_table, xml_tree)
        
        
        json_values = JSON_Values()
        json_dates = JSON_Dates(tables, json_values)
        json_normalizer = JSON_Normalizer(tables, entities, json_values)
    

        aff_handler = AffiliationsHandler(normalized_affiliations)
        json2articlemodel = JSON_Articles_Models(aff_handler, json_normalizer, json_dates)

        json2models = JSON_Models(json2articlemodel)
        
        #FIXME
        #cisis, idfile, paths, records_order, json2idfile, json2idfile_article
        converter_utf8_iso = ConverterUTF8_ISO()

        app_paths = Paths(processing_serial_path, web_pdf_path, web_xml_path, web_img_path, processing_serial_path + '/scilista.lst')
        db_manager = ISISArticle(CISIS(cisis_path), IDFile(), app_paths, 'ohflc', JSONIDFile(converter_utf8_iso), JSON2IDFile_Article(JSONIDFile(converter_utf8_iso)))
        

        db_articles = DBArticles(db_manager)
        db_articles.create_table('title', db_title_filename)
        db_articles.create_table('issue', db_issue_filename)

        
        json_titles = db_articles.db2json('title')
        json_boxes = db_articles.db2json('issue')
                
        #
        registered_titles = json2models.return_publications_list(json_titles)
        registered_boxes = json2models.return_publication_items_list(json_boxes, registered_titles)
        
        all_boxes = Issues(registered_issues, JournalIssues())

        email_service = EmailService('', config.parameter('SENDER_EMAIL'))
        message_type = MessageType(config.parameter('EMAIL_SUBJECT_PREFIX'), config.parameter('EMAIL_TEXT'), config.parameter('FLAG_SEND_EMAIL_TO_XML_PROVIDER'), config.parameter('ALERT_FORWARD'), config.parameter('FLAG_ATTACH_REPORTS'))
        report_sender = ReportSender(report, config.parameter('IS_AVAILABLE_EMAIL_SERVICE'), email_service, config.parameter('BCC_EMAIL').split(','), message_type)
     

        document_analyst = DocumentAnalyst(xml2json, json2models, registered_titles, all_boxes)
        shelves_organizer = ShelvesOrganizer(db_articles)

        reception = Reception(config.parameter('WORK_PATH'), report_sender, report_path, tracker)
        reception.open_packages(document_analyst, shelves_organizer)

        print('-' * 80)
        print('Check report files:  ')
        print('Errors report: ' + err_filename)
        print('Summarized report: ' + summary_filename)

        print('Detailed report: ' + log_filename)
        print('Reports for each package of XML files in ' + work_path)



