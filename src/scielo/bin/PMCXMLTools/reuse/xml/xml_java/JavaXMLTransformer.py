import shutil
import os
import sys

class JavaXMLTransformer:
    def __init__(self, java_path, path_jar_transformer, path_jar_validator):
        self.java_path = java_path
        self.path_jar_transformer = path_jar_transformer
        self.path_jar_validator = path_jar_validator
        
    def validate(self, xml_filename, use_dtd, result_filename, err_filename):
        valid = False
        validation_type = ''
        
        temp = xml_filename + '.validation.tmp'
        
        if os.path.exists(temp):
            os.remove(temp)
        if os.path.exists(result_filename):
            os.remove(result_filename)
        if os.path.exists(err_filename):
            os.remove(err_filename)
        
        if use_dtd:
            validation_type = '--validate'
        cmd = self.java_path + ' -cp ' +  self.path_jar_validator + '/XMLCheck.jar br.bireme.XMLCheck.XMLCheck ' + xml_filename + ' ' +  validation_type +  '>' + temp
        os.system(cmd)
        print cmd
        
        if os.path.exists(temp):
            f =open(temp, 'r')
            content = f.read()
            f.close()
        else:
            content = 'ERROR: Not valid. Unknown error.' + "\n" + cmd
            f =open(temp, 'w')
            f.write(content)
            f.close()
        
        
        if 'ERROR' in content.upper():
            print err_filename
            os.rename(temp, err_filename)
        else:
            valid = True
            print result_filename
            
            os.rename(temp, result_filename)
            
        
        return valid
        
    def transform(self, xml_filename, xsl_filename, result_filename, err_filename):
        r = False
        temp_result = result_filename + '.tmp'
        
        if os.path.exists(temp_result):
            os.remove(temp_result)
        if os.path.exists(result_filename):
            os.remove(result_filename)
        if os.path.exists(err_filename):
            os.remove(err_filename)
         
        if os.path.exists(self.path_jar_transformer + '/saxon9.jar'):
            jar_saxon = self.path_jar_transformer + '/saxon9.jar'
        else:
            jar_saxon = self.path_jar_transformer + '/saxon8.jar'
        cmd = self.java_path + ' -jar ' +  jar_saxon + ' -novw -w0 -o ' + temp_result + ' ' + xml_filename + ' ' + xsl_filename
        os.system(cmd)
        print cmd
        
        
        if os.path.exists(temp_result):
            r = True
        else:
            f =open(temp_result, 'w')
            f.write('ERROR: transformation error.')
            f.write(cmd)
            f.close()
            
        if r == True:
            os.rename(temp_result, result_filename)
            print(result_filename)
        else:
            os.rename(temp_result, err_filename)
            print(err_filename)
        return r