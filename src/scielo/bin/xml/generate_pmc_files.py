from reuse.xml.xml_java.JavaXMLTransformer import JavaXMLTransformer

from reuse.xml.xml_tree.xml_tree import XMLTree
from reuse.encoding.table_entities import TableEntities

from markup_pmc.markup_pmc_files import MarkupPMC, XSLFiles

from reuse.input_output.configuration import Configuration
from reuse.input_output.parameters import Parameters 
from reuse.input_output.report import Report 


import sys
import os

required_parameters = ['', 'sgml xml filename', 'output path', 'err filename',  ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    #ign, java_path, jar_validator, xsl_path, sgm_xml_filename, output_filename, err_filename = sys.argv
    ign, sgm_xml_filename, output_filename, err_filename = sys.argv

    
    # configuration
    java_path = 'java'
    current_path = os.path.dirname(ign).replace('\\', '/')
    jar_saxon = current_path + '/reuse/xml/xml_java/jar/saxonb9-1-0-8j/saxon9.jar' 
    jar_validator = current_path + '/reuse/xml/xml_java/jar/XMLCheck.jar'
    path_xsl = current_path + '/../pmc/v3.0/xsl/'
    entities_filename = current_path + '/reuse/encoding/entities'

    xsl_sgml2xml = path_xsl + '/sgml2xml/sgml2xml.xsl'
    xsl_xml2pmc = path_xsl + '/sgml2xml/xml2pmc.xsl'
    xsl_pmc = path_xsl + '/sgml2xml/pmc.xsl'
    xsl_err = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
    xsl_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
    xsl_preview = path_xsl + '/web/caller-scielo-html-previewer.xsl'
    
    xsl_files = XSLFiles(xsl_sgml2xml, xsl_xml2pmc, xsl_pmc, xsl_err, xsl_report, xsl_preview)

    pmc = MarkupPMC(JavaXMLTransformer(java_path, jar_saxon , jar_validator),  XMLTree(TableEntities(entities_filename)), xsl_files)
    
    report = Report(sgm_xml_filename + '.report.log', sgm_xml_filename + '.report.err', sgm_xml_filename + '.report.txt')
    pmc.generate_xml(sgm_xml_filename, output_filename, err_filename, report)       
