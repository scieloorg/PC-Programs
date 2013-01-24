from reuse.xml.xml_java.JavaXMLTransformer import JavaXMLTransformer
from reuse.input_output.configuration import Configuration
from reuse.input_output.parameters import Parameters 
from reuse.input_output.report import Report 

import sys
import os, shutil

required_parameters = ['', 'xml filename', 'ctrl filename', 'err filename', 'validate' ]



parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    ign, xml_filename, ctrl_filename,  err_filename, validate = sys.argv
    
    result_filename = err_filename + '.tmp'

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    if os.path.exists(err_filename):
        os.unlink(err_filename)
    if os.path.exists(ctrl_filename):
        os.unlink(ctrl_filename)
    
    current_path = os.getcwd()
    jar_saxon = current_path + '/../jar/saxonb9-1-0-8j/saxon9.jar' 
    jar_validator = current_path + '/../jar/XMLCheck.jar'
    xsl_path = current_path + '/../pmc/v3.0/xsl/'
    
    java_transformer = JavaXMLTransformer('java', jar_saxon, jar_validator)
    java_transformer.validate(xml_filename, validate, result_filename, err_filename)

    if os.path.exists(result_filename):
        shutil.copyfile(result_filename, ctrl_filename)
        os.unlink(result_filename)
    if os.path.exists(err_filename):
        shutil.copyfile(err_filename, ctrl_filename)
