import reuse.xml.xml_java as xml_java


from reuse.input_output.parameters import Parameters 

import sys
import os, shutil

required_parameters = ['', 'xml filename', 'xsl filename', 'result filename', 'ctrl filename', 'err filename' ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    ign, xml_filename, xsl_filename, result_filename, ctrl_filename, err_filename = sys.argv
    
    if os.path.exists(ctrl_filename):
        os.unlink(ctrl_filename)

    if '/' in ign:
        current_path = os.path.dirname(ign).replace('\\', '/')
    else:
        current_path = os.getcwd()
    
    xml_java.jar_transform = current_path + '/../jar/saxonb9-1-0-8j/saxon9.jar' 
    xml_java.jar_validate = current_path + '/../jar/XMLCheck.jar'
    
    xml_java.transform(xml_filename, xsl_filename, result_filename, err_filename)
    
    if os.path.exists(result_filename):
        shutil.copyfile(result_filename, ctrl_filename)
        print(result_filename)
        
    if os.path.exists(err_filename):
        shutil.copyfile(err_filename, ctrl_filename)
        print(result_filename)

