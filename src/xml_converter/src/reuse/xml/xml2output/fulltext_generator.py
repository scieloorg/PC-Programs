import os, shutil
import reuse.xml.xml_java as xml_java

xml_java.jar_transform = 'jar/saxonb9-1-0-8j/saxon9.jar' 
xml_java.jar_validate = 'jar/XMLCheck.jar'

class FullTextGenerator:
    def __init__(self, xsl_and_output_list):
        
        self.xsl_and_output_list = xsl_and_output_list

    def generate(self, xml_file, parameters = {}):
        for name, xsl_and_output in self.xsl_and_output_list.items():
            xml = xml_file.replace('.xml', xsl_and_output['output'])
            print(xml_file)
            print(xsl_and_output['xsl'])
            print(xml)
            print(xml + '.err')
            
            f = open(xml_file, 'r')
            c = f.read()
            f.close()

            filename = xml_file
            temp = ''
            #print(c[0:200])
            if '<!DOCTYPE' in c:
            	part1 = c[0:c.find('<!DOCTYPE')]
            	part2 = c[c.find('<!DOCTYPE'):]
            	part2 = part2[part2.find('>')+1:]
                
                import tempfile
                import shutil
                ign, temp = tempfile.mkstemp()

                shutil.copyfile(filename, temp)
                
            	f = open(temp,  'w')
            	f.write(part1+part2)
            	f.close()
                filename = temp

            xml_java.transform(filename, xsl_and_output['xsl'], xml, xml + '.err', parameters)

            if len(temp)>0:
                os.unlink(temp)


     