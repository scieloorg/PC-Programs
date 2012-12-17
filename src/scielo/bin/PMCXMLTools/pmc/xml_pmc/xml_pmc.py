
import shutil
import os
import sys


class XML_PMC:
    valid_extensions = [ '.tiff', '.eps', '.tif' ]
    
    def __init__(self, xml_processor, path_xsl):
        # <???>/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml
        self.xml_processor = xml_processor
        
        self.path_xsl = path_xsl
         
        # XSL
        self.xsl_web = path_xsl + '/scielo/jpub3-PMCcit-xhtml-scielo-previewer.xsl'
        
    def load(self, xml_file, report):
        self.xml_file = xml_file
        
        self.result_filename = xml_file + '.preview.res'

        self.preview_filename = xml_file + '.preview.html'
        self.err_filename = xml_file + '.preview.err'


    def fix_xml(self, xml):
        f = open(xml, 'r')
        c = f.read()
        f.close()

        new_c = c[0:c.rfind('>')+1]

        p = new_c.find('<!DOCTYPE')
        if p > 0:
            part1 = new_c[0:p]
            part2 = new_c[p+1:]
            p = part2.find('>')
            if p > 0:
                part2 = part2[p+1:]
            new_c = part1 + part2

        
        if new_c != c:            
            f = open(xml, 'w')
            f.write(new_c)
            f.close()
    
    def validate(self, xml, use_dtd):
        return self.xml_processor.validate(xml, use_dtd, self.result_filename, self.err_filename)
        
    def transform(self, xml, xsl, result):
        return self.xml_processor.transform(xml, xsl, result, self.err_filename)
        
    def generate_preview(self, xml_file, param_result_filename, param_err_filename, report):  
        self.fix_xml(xml_file)
        self.load(xml_file, report)
        
        if os.path.exists(param_err_filename):
            os.unlink(param_err_filename)
        if os.path.exists(param_result_filename):
            os.unlink(param_result_filename)

        if self.validate(self.xml_file, False):
            print('Valid pmc.xml')
            # Generate html for web
            if self.transform(self.xml_file, self.xsl_web, self.preview_filename):
                print('Generated web ')
        else:
            if self.transform(self.xml_file, self.xsl_web, self.preview_filename):
                print('Generated web ')
                            
                                                                
        if os.path.exists(self.preview_filename):
            if self.preview_filename != param_result_filename:
                os.rename(self.preview_filename, param_result_filename)
        
        else:
            if not os.path.exists(self.err_filename):
                f = open(self.err_filename, 'w')
                f.write('error')
                f.close()
            
            if self.err_filename != param_err_filename:
                os.rename(self.err_filename, param_err_filename)
       
