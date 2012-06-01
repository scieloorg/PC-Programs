from MKPXML import MKPXML
import shutil
import os
import sys

class PMCFilesManager:
    valid_extensions = [ '.tiff', '.eps', '.tif' ]
    
    def __init__(self, mkp_xml_fullname):
        self.fullname = '' 
        
        # <???>/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml
        
        if not '/pmc/pmc_work/' in mkp_xml_fullname:
            print 'Invalid path. Expected: <???>/<acron>/<issue_id>/pmc/pmc_work/<article_filename>/<article_filename>.sgm.xml'   
            print '   Ex.: <???>/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml'   
        else:
            # <???>/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml
            self.fullname = mkp_xml_fullname
             
            # 02-05.sgm.xml
            self.filename = mkp_xml_fullname[mkp_xml_fullname.rfind('/')+1:] 
            
            # <???>/ag/v49n1/pmc/pmc_work/02-05
            self.work_path = mkp_xml_fullname[0:mkp_xml_fullname.rfind('/')]
            
            # <???>/ag/v49n1/pmc/
            pmc_path = self.work_path[0:self.work_path.rfind('/pmc_work')+1] 
            
            # <???>/ag/v49n1/pmc/pmc_package
            self.package_path = pmc_path + 'pmc_package' 
            
            # <???>/ag/v49n1/pmc/pmc_img
            self.img_path = pmc_path + 'pmc_img' 
            self.jpg_path = mkp_xml_fullname[0:mkp_xml_fullname.rfind('/pmc/pmc_work')+1] + 'img'
            
            # <???>/ag/v49n1/pmc/pmc_pdf
            self.pdf_path = pmc_path + 'pmc_pdf' 
            self.pdf_filename = self.pdf_path + '/' + self.filename.replace('sgm.xml', 'pdf')
            
            
            if not os.path.exists(self.package_path):
                try:
                    os.makedirs(self.package_path)
                except:
                    print 'Unable to create ' +self.package_path
    
    def clean_directory(self):
        
        filename = self.filename.replace('.sgm.xml','')
        extensions = [ '.local.xml', '.rep.xml', '.rep.html', '.xml.html', '.xml']
        files = [ filename + ext for ext in extensions ]
        list = os.listdir(self.work_path)
        for f in list:
            if f in files:
                os.remove(self.work_path + '/' + f)    
                      
    def remove_tmp_files(self):
        list = os.listdir(self.work_path)
        for f in list:
            if '.tmp' in f:
                os.remove(self.work_path + '/' + f)
                                            
    def copy_files_from_work_to_package_folder(self, pmc_xml_fullname):
        if not os.path.isfile(pmc_xml_fullname):
             print 'Expected: ' + pmc_xml_fullname
        else:
            mkp_xml = MKPXML(self.fullname)
            newfilename = mkp_xml.return_filename()
            images = mkp_xml.return_images()
            new_fullname = self.package_path + '/' + newfilename 
            
            shutil.copy(pmc_xml_fullname, new_fullname + '.xml')
            shutil.copy(self.pdf_filename, new_fullname + '.pdf')
             
            img_extension = ''
            for src_dest_img in images:
                src = src_dest_img[0]
                if '.jpg' in src:
                    src = src.replace('.jpg','')
             
                test_ext = False
                i = 0
                msg =  'ERROR: one of the files below is expected:' + "\n"
                while (not test_ext) and (i < len(self.valid_extensions)):
                    img_extension = self.valid_extensions[i]
                    if os.path.isfile(self.img_path + '/' + src + img_extension):
                 	    test_ext = True
                 	    shutil.copy(self.img_path + '/' + src + img_extension, new_fullname + '-' + src_dest_img[1] +  img_extension)
                    else:
                        msg = msg + '   - '  +  self.img_path + '/' + src + img_extension + ' does not exist' + "\n"
                    i+=1
                if not test_ext:
                    print msg
                     
    def copy_files_from_img_to_work_folder(self):
        msg = ''
        mkp_xml = MKPXML(self.fullname)
        images = mkp_xml.return_images()
        for src_dest_img in images:
            
            src = src_dest_img[0]
            if not '.jpg' in src:
                src = src + '.jpg'
 
            
            if os.path.isfile(self.jpg_path + '/' + src ):
     	        shutil.copy(self.jpg_path + '/' + src , self.work_path + '/' + src)
            else:
                msg = msg + '   - Missing file: '  +  self.jpg_path + '/' + src   + "\n"
         
        if len(msg)>0:
            print msg          
                            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1]=='test':
            pmcfolders = PMCFilesManager('samples/pmc/pmc_work/a05v41n3/a05v41n3.sgm.xml')
            pmcfolders.copy_files_from_work_to_package_folder('samples/pmc/pmc_work/a05v41n3/a05v41n3.sgm.xml.local.xml')
            pmcfolders.copy_files_from_img_to_work_folder()
       
   
                     