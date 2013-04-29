import reuse.xml.xml_java as xml_java


from reuse.input_output.parameters import Parameters 
from reuse.input_output.parameters import get_script_path as get_script_path

import sys
import os, shutil

required_parameters = ['', 'xml filename', 'xsl filename', 'result filename', 'ctrl filename', 'err filename' ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    script, xml_filename, xsl_filename, result_filename, ctrl_filename, err_filename = sys.argv
    if os.path.exists(ctrl_filename):
        os.unlink(ctrl_filename)

    current_path = get_script_path(script) 
    
    xml_java.jar_transform = current_path + '/../jar/saxonb9-1-0-8j/saxon9.jar' 
    xml_java.jar_validate = current_path + '/../jar/XMLCheck.jar'
    
    xml_java.transform(xml_filename, xsl_filename, result_filename, err_filename)
    
    if os.path.exists(result_filename):
        shutil.copyfile(result_filename, ctrl_filename)
        print(result_filename)
        
    if os.path.exists(err_filename):
        shutil.copyfile(err_filename, result_filename)
        shutil.copyfile(err_filename, ctrl_filename)
        print(result_filename)

