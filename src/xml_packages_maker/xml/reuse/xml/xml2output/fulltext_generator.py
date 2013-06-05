class FullTextGenerator:
    def __init__(self, transformer, xsl_and_output_list):
        self.transformer = transformer

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
            #print(c[0:200])
            if '<!DOCTYPE' in c:
            	part1 = c[0:c.find('<!DOCTYPE')]
            	part2 = c[c.find('<!DOCTYPE'):]
            	part2 = part2[part2.find('>')+1:]
                
                f = open(xml_file.replace('.xml', '.original.xml'), 'w')
                f.write(c)
                f.close()

                filename = xml_file
            	f = open(filename,  'w')
            	f.write(part1+part2)
            	f.close()

            self.transformer.transform(filename, xsl_and_output['xsl'], xml, xml + '.err', parameters)


     