from PMCFilesManager import PMCFilesManager
from JavaXMLManager import JavaXMLManager

import shutil
import os
import sys

class PMCXMLGeneratorAndValidator:

    def __init__(self, path_xsl, java_path, jar_path):
        self.path_xsl = path_xsl
        self.xml_manager = JavaXMLManager(java_path, jar_path)
        
        self.xsl_sgml2xml = path_xsl + '/../sgml2xml/sgml2xml.xsl'
        
        self.xsl_xml2pmc = path_xsl + '/../sgml2xml/xml2pmc.xsl'
        self.xsl_pmc = path_xsl + '/../sgml2xml/pmc.xsl'
        self.xsl_err = path_xsl + '/pmcstylechecker.xsl'
        self.xsl_report = path_xsl + '/pmcstylereporter.xsl'
        self.xsl_preview = path_xsl + '/viewText.xsl'
        
        
        
    def execute(self, sgm_xml_filename, param_result_filename, param_err_filename):
        #sgm_xml_filename = original_sgm_xml_filename.replace('.sgm.xml', '.fixed.sgm.xml')

        #shutil.copyfile(original_sgm_xml_filename, sgm_xml_filename)

        f = open(sgm_xml_filename, 'r')
        c = f.read()
        f.close()

        new_c = c[0:c.rfind('>')+1]
        if new_c != c:
            
            f = open(sgm_xml_filename, 'w')
            f.write(new_c)
            f.close()


        filename = sgm_xml_filename.replace('.sgm.xml', '')
        xml_pmc_local = filename + '.local.xml'
        xml_report = filename + '.rep.xml'
        html_report = filename + '.rep.html'
        preview_filename = filename + '.xml.html'
        xml_pmc = filename + '.xml'
        xml_scielo = filename + '.scielo.xml'
                    
        result_filename = sgm_xml_filename + '.res.tmp'
        err_filename = sgm_xml_filename + '.err.tmp'
        
        if os.path.isfile(param_result_filename):
            os.remove(param_result_filename)
        if os.path.isfile(param_err_filename):
            os.remove(param_err_filename)
        if os.path.isfile(result_filename):
            os.remove(result_filename)
        if os.path.isfile(err_filename):
            os.remove(err_filename)
            


        pmc_files_manager = PMCFilesManager(sgm_xml_filename)
        pmc_files_manager.clean_directory()
        
        done = False
           
        # Validate sgm.xml

        if self.xml_manager.validate(sgm_xml_filename, False, result_filename, err_filename):
            print('Valid sgm.xml')
            # Generate scielo.xml, setting a local DTD
            if self.xml_manager.transform(sgm_xml_filename, self.xsl_sgml2xml, xml_scielo, err_filename):
                print('Generated scielo.xml')
                # Validate scielo.xml, using a local DTD
                if self.xml_manager.validate(xml_scielo, True, result_filename, err_filename):

                    
                    # fix scielo.xml local.xml
                    print('Valid scielo.xml')
                    if self.xml_manager.transform(xml_scielo, self.xsl_xml2pmc, xml_pmc_local, err_filename):

                        # Generate report.xml 
                        print('Generated pmc local')
                        if self.xml_manager.transform(xml_pmc_local, self.xsl_err, xml_report, err_filename):
                        
                            # Generate report.html
                            print('Generated xml report')
                            if self.xml_manager.transform(xml_report, self.xsl_report, html_report, err_filename):
                                #os.remove(xml_report)
                                # Preview text
                                pmc_files_manager.copy_files_from_img_to_work_folder()
                                print('Copy img to work')
                                if self.xml_manager.transform(xml_pmc_local, self.xsl_preview, preview_filename, err_filename):

                                    # Generate xml (final version)
                                    print('Generated preview')
                                    if self.xml_manager.transform(xml_pmc_local, self.xsl_pmc, xml_pmc, err_filename):
                                        #shutil.copyfile(xml_pmc_local, xml_pmc)
                                        print('Generated xml pmc final')
                                        pmc_files_manager.create_xml_package(xml_scielo)
                                    
                                        print('Generated xml scielo')
                                        pmc_files_manager.copy_files_from_work_to_package_folder(xml_pmc)
                                        print('Copied to package')
                                        done = True
                                       
        if done:
            if preview_filename != param_result_filename:
                os.rename(preview_filename, param_result_filename)
        else:
            if not os.path.exists(err_filename):
            
                f = open(err_filename, 'w')
                f.write('error')
                f.close()
            if err_filename != param_err_filename:
                os.rename(err_filename, param_err_filename)
            
        pmc_files_manager.remove_tmp_files()
        
        return done



                            
                            
if __name__ == '__main__':
    print sys.argv
    print sys.argv[1]
    
    if len(sys.argv) == 7:
        ign, java_path, jar_path, xsl_path, sgm_xml_filename, output_filename, err_filename = sys.argv
        
    if sys.argv[1] == 'test':
        
       java_path = 'java'
       jar_path = os.getcwd() + "/core"
       xsl_path = os.getcwd() + "/../markup_pmc/pmc/v3.0/check"
       sgm_xml_filename = os.getcwd() + "/samples/pmc/pmc_work/a05v41n3/a05v41n3.sgm.xml"
       output_filename = os.getcwd() + "/abc.html"
       err_filename = os.getcwd() + "/abc.err"
    
    java_path = java_path.replace('\\','/')
    jar_path = jar_path.replace('\\','/')
    xsl_path = xsl_path.replace('\\','/')
    sgm_xml_filename = sgm_xml_filename.replace('\\','/')
    output_filename = output_filename.replace('\\','/')
    err_filename = err_filename.replace('\\','/')
    
    pmc = PMCXMLGeneratorAndValidator(xsl_path, java_path, jar_path)
    pmc.execute(sgm_xml_filename, output_filename, err_filename)       
    
    print "fim"
    
    if os.path.exists(output_filename):
         print output_filename                    
    if os.path.exists(err_filename):
         print err_filename                    
                            
                            
                            
                            
                            
                            
                            
                            
                            
        