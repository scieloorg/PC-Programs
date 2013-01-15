import shutil
import os
import sys

class JavaXMLTransformer:
    def __init__(self, java_path, saxon_jar, validator_jar):
        self.java_path = java_path
        self.saxon_jar = saxon_jar
        self.validator_jar = validator_jar
        
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
        cmd = self.java_path + ' -cp ' +  self.validator_jar + ' br.bireme.XMLCheck.XMLCheck ' + xml_filename + ' ' +  validation_type +  '>' + temp
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
        
        shutil.copyfile(temp, result_filename)

        if 'ERROR' in content.upper():
            shutil.copyfile(temp, err_filename)
        else:
            valid = True
        os.unlink(temp)
        
        return valid
        
    def format_parameters(self, parameters):
        r = ''
        for k, v in parameters.items():
            if  ' ' in v:
                r += k + '=' + '"' + v + '" '
            else:
                r += k + '=' +  v + ' '
        return r

    def transform(self, xml_filename, xsl_filename, result_filename, err_filename, parameters = {}):
        r = False
        temp_result = result_filename + '.tmp'
        
        if os.path.exists(temp_result):
            os.remove(temp_result)
        if os.path.exists(result_filename):
            os.remove(result_filename)
        if os.path.exists(err_filename):
            os.remove(err_filename)
         
        if os.path.exists(self.saxon_jar ):
            jar_saxon = self.saxon_jar 
        cmd = self.java_path + ' -jar ' +  jar_saxon + ' -novw -w0 -o "' + temp_result + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + self.format_parameters(parameters)
        os.system(cmd)
        print cmd
        
        
        if os.path.exists(temp_result):
            r = True
        else:
            f =open(temp_result, 'w')
            f.write('ERROR: transformation error.\n')
            f.write(cmd)
            f.close()
            
        if r == True:
            os.rename(temp_result, result_filename)
            print(result_filename)
        else:
            os.rename(temp_result, err_filename)
            print(err_filename)
        return r