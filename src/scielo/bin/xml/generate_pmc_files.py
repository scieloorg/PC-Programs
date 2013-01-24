
import sys
import os

import markup_pmc as markup_pmc

from reuse.input_output.parameters import Parameters 

from reuse.xml.xml_tree.xml_tree import XMLTree
from reuse.encoding.table_entities import TableEntities
from reuse.input_output.report import Report 


required_parameters = ['', 'sgml xml filename', 'output filename', 'err filename',  ]

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
    
    markup_pmc.css = current_path + '/../pmc/v3.0/xsl/previewer/preview.css'
    markup_pmc.xml_java.jar_transform = current_path + '/../jar/saxonb9-1-0-8j/saxon9.jar' 
    markup_pmc.xml_java.jar_validate = current_path + '/../jar/XMLCheck.jar'
    

    path_xsl = current_path + '/../pmc/v3.0/xsl/'
    entities_filename = current_path + '/reuse/encoding/entities'

    markup_pmc.xml_tree = XMLTree(TableEntities(entities_filename))

    markup_pmc.xsl_sgml2xml = path_xsl + '/sgml2xml/sgml2xml.xsl'
    markup_pmc.xsl_xml2pmc = path_xsl + '/sgml2xml/xml2pmc.xsl'
    markup_pmc.xsl_pmc = path_xsl + '/sgml2xml/pmc.xsl'
    markup_pmc.xsl_err = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
    markup_pmc.xsl_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
    #markup_pmc.xsl_preview = path_xsl + '/web/scielo-html-previewer.xsl'
    markup_pmc.xsl_preview = path_xsl + '/previewer/preview.xsl'
    
    report = Report(sgm_xml_filename + '.report.log', sgm_xml_filename + '.report.err', sgm_xml_filename + '.report.txt')
    
    markup_pmc = markup_pmc.MarkupPMC(sgm_xml_filename, current_path + '/../pmc/v3.0/dtd/journalpublishing3.dtd', report)
    
    markup_pmc.generate_xml(output_filename, err_filename)       
