
import sys
import os

import pmc_markup_files as pmc_markup_files

from reuse.input_output.parameters import Parameters 

from reuse.xml.xml_tree.xml_tree import XMLTree
from reuse.encoding.table_entities import TableEntities
from reuse.input_output.report import Report 


required_parameters = ['', 'sgml xml filename', 'output path', 'err filename',  ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    #ign, java_path, jar_validator, xsl_path, sgm_xml_filename, output_filename, err_filename = sys.argv
    script, sgm_xml_filename, output_filename, err_filename = sys.argv

    
    # configuration
    ctrl_filename = output_filename
    if os.path.exists(ctrl_filename):
        os.unlink(ctrl_filename)

    if '/' in script:
        current_path = os.path.dirname(script).replace('\\', '/')
    else:
        current_path = os.getcwd()
    
    pmc_markup_files.xml_java.jar_transform = current_path + '/../jar/saxonb9-1-0-8j/saxon9.jar' 
    pmc_markup_files.xml_java.jar_validate = current_path + '/../jar/XMLCheck.jar'
    

    path_xsl = current_path + '/../pmc/v3.0/xsl/'
    entities_filename = current_path + '/reuse/encoding/entities'

    pmc_markup_files.xml_tree = XMLTree(TableEntities(entities_filename))

    pmc_markup_files.xsl_sgml2xml = path_xsl + '/sgml2xml/sgml2xml.xsl'
    pmc_markup_files.xsl_xml2pmc = path_xsl + '/sgml2xml/xml2pmc.xsl'
    pmc_markup_files.xsl_pmc = path_xsl + '/sgml2xml/pmc.xsl'
    pmc_markup_files.xsl_err = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
    pmc_markup_files.xsl_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
    pmc_markup_files.xsl_preview = path_xsl + '/web/scielo-html-previewer.xsl'
    
    report = Report(sgm_xml_filename + '.report.log', sgm_xml_filename + '.report.err', sgm_xml_filename + '.report.txt')
    
    markup_pmc = pmc_markup_files.MarkupPMC(sgm_xml_filename, current_path + '/../pmc/v3.0/dtd/journalpublishing3.dtd', report)
    
    markup_pmc.generate_xml(output_filename, err_filename)       
