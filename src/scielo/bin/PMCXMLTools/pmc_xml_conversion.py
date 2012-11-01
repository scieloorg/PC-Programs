from xml_java.JavaXMLTransformer import JavaXMLTransformer

from xml_pmc.xml_pmc import XML_PMC

from input_output.configuration import Configuration
from input_output.parameters import Parameters 
from input_output.report import Report 


import sys
import os

required_parameters = ['', 'Java path', 'transformer jar path', 'validator jar path' , 'XSL path', 'xml filename', 'output path', 'err filename',  ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    ign, java_path, saxon_path, validator_path, xsl_path, pmc_xml, output_filename, err_filename = sys.argv

    
    pmc = XML_PMC(JavaXMLTransformer(java_path, os.getcwd() + '/' + saxon_path , os.getcwd() + '/' + validator_path), xsl_path)
    
    report = Report(pmc_xml + '.report.log', pmc_xml + '.report.err', pmc_xml + '.report.txt')
    pmc.generate_preview(pmc_xml, output_filename, err_filename, report)       


# java xml_java/jar/saxonb9-1-0-8j xml_java/jar xml_pmc/jpub3-preview-xslt xmlfilename output errfile  