from reuse.xml.xml_java.JavaXMLTransformer import JavaXMLTransformer

from reuse.xml.xml_tree.xml_tree import XMLTree
from reuse.encoding.entities import Entities

from pmc.markup_pmc.markup_pmc_files import MarkupPMC

from reuse.input_output.configuration import Configuration
from reuse.input_output.parameters import Parameters 
from reuse.input_output.report import Report 


import sys
import os

required_parameters = ['', 'Java path', 'jar path', 'XSL path', 'sgml xml filename', 'output path', 'err filename',  ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    ign, java_path, jar_path, xsl_path, sgm_xml_filename, output_filename, err_filename = sys.argv

    jar_path = jar_path.replace('core','reuse/xml/xml_java/jar')
    jar_saxon = jar_path + '/saxonb9-1-0-8j'
    app_path = os.path.dirname(jar_path)
    if app_path + '/' == jar_path:
        app_path = os.path.dirname(os.path.dirname(app_path))
    
    pmc = MarkupPMC(JavaXMLTransformer(java_path, jar_saxon , jar_path),  XMLTree(Entities()), xsl_path)
    
    report = Report(sgm_xml_filename + '.report.log', sgm_xml_filename + '.report.err', sgm_xml_filename + '.report.txt')
    pmc.generate_xml(sgm_xml_filename, output_filename, err_filename, report)       
