from reuse.xml.xml_java.JavaXMLTransformer import JavaXMLTransformer
from reuse.input_output.configuration import Configuration
from reuse.input_output.parameters import Parameters 
from reuse.input_output.report import Report 

import sys
import os

required_parameters = ['', 'xml filename', 'xsl filename', 'result filename', 'ctrl filename', 'err filename' ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    ign, xml_filename, ctrl_filename, err_filename, validate = sys.argv
    


    if os.path.exists(result_filename):
        os.unlink(result_filename)
    
    if os.path.exists(err_filename):
        os.unlink(err_filename)
    if os.path.exists(ctrl_filename):
        os.unlink(ctrl_filename)

    saxon_path = os.getcwd() + '/reuse/xml/xml_java/jar/saxonb9-1-0-8j' 
    validator_path = os.getcwd() + '/reuse/xml/xml_java/jar'

    java_transformer = JavaXMLTransformer('java', saxon_path, validator_path)
    java_transformer.transform(xml_filename, xsl_filename, result_filename, err_filename)
    
    os.copyfile(result_filename, ctrl_filename)
# java reuse/xml/xml_java/jar/saxonb9-1-0-8j reuse/xml/xml_java/jar pmc/versions/v3.0/jpub3-preview-xslt xmlfilename output errfile  