
import shutil
import os
import sys

class XMLData:
    def __init__(self, xml_manager):
        
        self.xml = xml_manager
        
    def load(self,  xml_filename, report):
        self.xml.load(xml_filename, report)

    def new_name(self, acron):
        nodes = self.xml.return_nodes()
        r = ''
        if len(nodes)>0:
            order = '00' + nodes[0].attrib['order']
            order = order[-3:]        
            fpage = '000' + nodes[0].attrib['fpage']
            fpage = fpage[-4:]
            if fpage == '0000':
                page_or_order ='e' + order
            else:
                page_or_order = fpage        
            issueno = '0' + nodes[0].attrib['issueno']
            issueno = issueno[-2:]            
            if len(acron)>0:
                acron += '-'
            r = nodes[0].attrib['issn'] + '-' + acron  + nodes[0].attrib['volid']+ '-' + issueno + '-' +  page_or_order
        return r
    
    def images(self, tags='figgrp | tabwrap | equation'):
        a = []        
        names = tags.split(' | ')
        print('return_images ')
        print(names)
        for tag in names:
            #print tag
            self.xml.debug = 3
            nodes = self.xml.return_nodes(tag)
            print(nodes)
            for node in nodes:
                print(node)                
                attr_filename = ''
                filetype = node.attrib['id']
                print('type=' + filetype)
                if filetype[0:1] == 'e':
                    filetype = 'e' + filetype
                else:
                    filetype = 'g' + filetype
                try:
                    attr_filename = node.attrib['filename']
                except:
                    graphic_nodes = self.xml.return_nodes('graphic', node)
                    print(graphic_nodes)
                    
                    for gnode in graphic_nodes:
                        print(gnode.attrib)
                        try:
                            attr_filename = gnode.attrib['href']
                        except:
                            attr_filename = ''
                        if attr_filename == '':
                            attr_filename = gnode.attrib['{http://www.w3.org/XML/1998/namespace}href']
                if attr_filename!='':
                    a.append( (attr_filename , filetype) )
        return a

class MarkupPMC:
    valid_extensions = [ '.tiff', '.eps', '.tif' ]
    
    def __init__(self, xml_processor, xml_manager, path_xsl):
        # <???>/ag/v49n1/pmc/pmc_work/02-05/02-05.sgm.xml
        self.xml_processor = xml_processor
        
        self.xml_data = XMLData(xml_manager)
        self.path_xsl = path_xsl
         
        # XSL
        self.xsl_sgml2xml = path_xsl + '/../sgml2xml/sgml2xml.xsl'
        self.xsl_xml2pmc = path_xsl + '/../sgml2xml/xml2pmc.xsl'
        self.xsl_pmc = path_xsl + '/../sgml2xml/pmc.xsl'
        self.xsl_err = path_xsl + '/pmcstylechecker.xsl'
        self.xsl_report = path_xsl + '/pmcstylereporter.xsl'
        self.xsl_preview = path_xsl + '/viewText.xsl'

    def load(self, sgml_xml_filename, report):
        self.sgml_xml_filename = sgml_xml_filename
        self.work_path = os.path.dirname(sgml_xml_filename)
        self.basename = os.path.basename(sgml_xml_filename)
        self.name = self.basename.replace('.sgm.xml', '')
        
        # XML
        self.generation_extensions = [ '.local.xml', '.rep.xml', '.rep.html', '.xml.html', '.xml', '.scielo.xml', '.sgm.xml.res.tmp', '.sgm.xml.err.tmp']
        
        self.xml_pmc_local = self.work_path + '/' + self.name + '.local.xml'
        self.xml_report = self.work_path + '/' + self.name + '.rep.xml'
        self.html_report = self.work_path + '/' + self.name + '.rep.html'
        self.preview_filename = self.work_path + '/' + self.name + '.xml.html'
        self.xml_pmc = self.work_path + '/' + self.name + '.xml'
        self.xml_scielo = self.work_path + '/' + self.name + '.scielo.xml'       
        
        # error and result files
        self.result_filename = sgml_xml_filename + '.res.tmp'
        self.err_filename = sgml_xml_filename + '.err.tmp'        
        
        if '/pmc/pmc_work/' in sgml_xml_filename:
            # /pmc
            pmc_path = os.path.dirname(os.path.dirname(self.work_path)) + '/'
            print('xxx')
            folders = os.path.dirname(os.path.dirname(pmc_path))
            self.acron = folders[folders.rfind('/')+1:]
            
        else:
            self.acron = ''
            pmc_path = self.work_path


        self.package_path = pmc_path + 'pmc_package' 
        self.xml_package_path = pmc_path + 'xml_package' 
        self.img_path = pmc_path + 'pmc_img' 
        self.jpg_path = pmc_path + 'pmc_img'
        self.pdf_path = pmc_path + 'pmc_pdf' 

        files = [self.package_path, self.xml_package_path, self.img_path, self.jpg_path, self.pdf_path]
        for f in files:
            if not os.path.exists(f):
                os.makedirs(f)
        self.pdf_filename = self.pdf_path + '/' + self.name + '.pdf'
        
        self.xml_data.load(self.sgml_xml_filename, report)
        self.new_name = self.xml_data.new_name(self.acron)
        self.xml_images_list = self.xml_data.images()

    def fix_xml(self, xml):
        f = open(xml, 'r')
        c = f.read()
        f.close()
        new_c = c[0:c.rfind('>')+1]
        if new_c != c:            
            f = open(xml, 'w')
            f.write(new_c)
            f.close()
    
    def validate(self, xml, use_dtd):
        return self.xml_processor.validate(xml, use_dtd, self.result_filename, self.err_filename)
        
    def transform(self, xml, xsl, result):
        return self.xml_processor.transform(xml, xsl, result, self.err_filename)
        
    def generate_xml(self, sgml_xml_filename, param_result_filename, param_err_filename, report):  
        self.fix_xml(sgml_xml_filename)
        self.load(sgml_xml_filename, report)
        self.clean_directory()
        
        if os.path.exists(param_err_filename):
            os.unlink(param_err_filename)
        if os.path.exists(param_result_filename):
            os.unlink(param_result_filename)

        if self.validate(self.sgml_xml_filename, False):
            print('Valid sgm.xml')
            # Generate scielo.xml, setting a local DTD
            if self.transform(self.sgml_xml_filename, self.xsl_sgml2xml, self.xml_scielo):
                print('Generated scielo.xml')
                # Validate scielo.xml, using a local DTD
                if self.validate(self.xml_scielo, True):                    
                    # fix scielo.xml local.xml
                    print('Valid scielo.xml')
                    if self.transform(self.xml_scielo, self.xsl_xml2pmc, self.xml_pmc_local):
                        
                        # Generate report.xml 
                        print('Generated pmc local')
                        if self.transform(self.xml_pmc_local, self.xsl_err, self.xml_report):
                            # Generate report.html
                            print('Generated xml report')
                            if self.transform(self.xml_report, self.xsl_report, self.html_report):
                                print('Generated html report')
                        
                        if self.transform(self.xml_pmc_local, self.xsl_preview, self.preview_filename):
                            # Generate xml (final version)
                            print('Generated preview')
                            self.copy_img_files_to_preview()
                            print('Copied img to work')
                        
                        if self.transform(self.xml_pmc_local, self.xsl_pmc, self.xml_pmc):
                            #shutil.copyfile(self.xml_pmc_local, xml_pmc)
                            print('Generated xml pmc final')

                            self.copy_files_from_work_to_xml_package_folder()
                            print('Copied to xml_package')
                            
                            self.copy_files_from_work_to_package_folder()
                            print('Copied to pmc_package')
                            
                                                                
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
       
    

    def clean_directory(self):
        files = [ self.name + ext for ext in self.generation_extensions ]
        for f in files:
            if os.path.exists(self.work_path + '/' + f):
                os.unlink(self.work_path + '/' + f)    

    def copy_files_from_work_to_xml_package_folder(self):
        if os.path.exists(self.xml_scielo):
            shutil.copyfile(self.xml_scielo, self.xml_package_path + '/' + self.new_name + '.xml')
                

    def copy_files_from_work_to_package_folder(self):
        print('copy_files_from_work_to_package_folder')

        if os.path.isfile(self.xml_pmc):
            new_fullname = self.package_path + '/' + self.new_name 
            print('copy ' + self.xml_pmc + ' ' + new_fullname)
            shutil.copy(self.xml_pmc, new_fullname + '.xml')

            if os.path.exists(self.pdf_filename):
                print('copy ' + self.pdf_filename + ' ' + new_fullname)
                shutil.copy(self.pdf_filename, new_fullname + '.pdf')
             
            img_extension = ''
            for old_and_new_img_name in self.xml_images_list:
                old_img_name = old_and_new_img_name[0]
                print(old_img_name)
                if '.jpg' in old_img_name:
                    old_img_name = old_img_name.replace('.jpg','')
             
                test_ext = False

                expected_files = [] 
                
                for img_extension in self.valid_extensions:

                    if os.path.isfile(self.img_path + '/' + old_img_name + img_extension):
                        test_ext = True
                        shutil.copy(self.img_path + '/' + old_img_name + img_extension, new_fullname + '-' + old_and_new_img_name[1] +  img_extension)
                        break
                    else:
                        expected_files.append(self.img_path + '/' + old_img_name + img_extension)
                if not test_ext and len(expected_files)>0:
                    print('ERROR: one of the files below is expected:' + "\n" + '\n'.join(expected_files))
                 

    def copy_img_files_to_preview(self):
        msg = ''
        print('copy_img_files_to_preview')
        print(self.xml_images_list)
        for old_and_new_img_name in self.xml_images_list:
            old_img_name = old_and_new_img_name[0]
            if not '.jpg' in old_img_name:
                old_img_name = old_img_name + '.jpg'
            new_img_name = old_and_new_img_name[1]
            if not '.jpg' in new_img_name:
                new_img_name += '.jpg'
            if os.path.isfile(self.jpg_path + '/' + old_img_name ):
     	        shutil.copy(self.jpg_path + '/' + old_img_name , self.work_path + '/' + self.new_name + '-' + new_img_name)
            else:
                msg = msg + '   - Missing file: '  +  self.jpg_path + '/' +  old_img_name   + "\n"
        if len(msg)>0:
            print msg          
                            
 
                     