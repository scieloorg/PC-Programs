
import shutil
import os
import sys
import tempfile
import reuse.xml.xml_java as xml_java


xml_tree = None
xsl_sgml2xml = ''
xsl_xml2pmc = ''
xsl_pmc = ''
xsl_err = ''
xsl_report = ''
xsl_preview = ''
css = ''

valid_extensions = [ '.tiff', '.eps', '.tif' ]
outputs_extensions = [ '.local.xml', '.rep.xml', '.rep.html', '.xml.html', '.xml', '.scielo.xml', '.sgm.xml.res.tmp', '.sgm.xml.err.tmp']


def prepare_path(path, startswith = '', endswith = ''):
    if not os.path.exists(path):
        os.makedirs(path)
    for file in os.listdir(path):
        if len(startswith)>0:
            if file.startswith(startswith):
                os.unlink(file)
        if len(endswith)>0:
            if file.endswith(endswith) and os.path.exists(file):
                os.unlink(file)
        if len(endswith) == 0 and len(startswith) == 0:
            os.unlink(file)

def fix_xml(xml):
    f = open(xml, 'r')
    c = f.read()
    f.close()
    new_c = c[0:c.rfind('>')+1]
    if new_c != c:            
        f = open(xml, 'w')
        f.write(new_c)
        f.close()

def xml_data_new_name(acron):
    nodes = xml_tree.return_nodes()
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


def xml_data_images(tags='figgrp | tabwrap | equation'):
    a = []        
    names = tags.split(' | ')
    
    for tag in names:
        #print tag
        xml_tree.debug = 3
        nodes = xml_tree.return_nodes(tag)
        
        for node in nodes:
                           
            attr_filename = ''
            filetype = node.attrib['id']
            
            if filetype[0:1] == 'e':
                filetype = 'e' + filetype
            else:
                filetype = 'g' + filetype
            try:
                attr_filename = node.attrib['filename']
            except:
                graphic_nodes = xml_tree.return_nodes('graphic', node)
                
                for gnode in graphic_nodes:
                    #print(gnode.attrib)
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
    def __init__(self, sgml_xml_filename, dtd, report):
        self.sgml_xml_filename = sgml_xml_filename
        self.report = report
        self.dtd = dtd 

    def output_files(self):
        self.work_path = os.path.dirname(self.sgml_xml_filename)
        self.basename = os.path.basename(self.sgml_xml_filename)
        self.name = self.basename.replace('.sgm.xml', '')
        
        # XML        
        self.xml_pmc_local = self.work_path + '/' + self.name + '.local.xml'
        self.xml_report = self.work_path + '/' + self.name + '.rep.xml'
        self.html_report = self.work_path + '/' + self.name + '.rep.html'
        self.html_preview = self.work_path + '/' + self.name + '.xml.html'
        self.xml_pmc = self.work_path + '/' + self.name + '.xml'
        self.xml_scielo = self.work_path + '/' + self.name + '.scielo.xml'       
        
        # error and result files
        self.result_filename = self.sgml_xml_filename + '.res.tmp'
        self.err_filename = self.sgml_xml_filename + '.err.tmp'        
        
        if '/pmc/pmc_work/' in self.sgml_xml_filename:
            # /pmc
            pmc_path = os.path.dirname(os.path.dirname(self.work_path)) + '/'
            
            folders = os.path.dirname(os.path.dirname(pmc_path))
            self.acron = folders[folders.rfind('/')+1:]
            
        else:
            self.acron = ''
            pmc_path = self.work_path + '/'


        self.pmc_package_path = pmc_path + 'pmc_package' 
        self.xml_package_path = pmc_path + 'xml_package' 
        self.img_path = pmc_path + 'pmc_img' 
        self.jpg_path = pmc_path + 'pmc_img'
        self.pdf_path = pmc_path + 'pmc_pdf' 

        files = [self.pmc_package_path, self.xml_package_path, self.img_path, self.jpg_path, self.pdf_path]
        for f in files:
            if not os.path.exists(f):
                os.makedirs(f)
        self.pdf_filename = self.pdf_path + '/' + self.name + '.pdf'
        
        xml_tree.load(self.sgml_xml_filename, self.report)
        self.new_name = xml_data_new_name(self.acron)
        self.xml_images_list = xml_data_images()


    
    def validate(self, xml, use_dtd):
        return xml_java.validate(xml, use_dtd, self.result_filename, self.err_filename)
        
    def transform(self, xml, xsl, result, parameters = {}):
        return xml_java.transform(xml, xsl, result, self.err_filename, parameters)
        
    def validate_and_transform(self, xml, xsl, result, validate_dtd):
        r = False
        if self.validate(xml, validate_dtd):
            r = self.transform(xml, xsl, result)
        return r

    def generate_xml(self, param_result_filename, param_err_filename):  
        self.report.write('fix xml')
        fix_xml(self.sgml_xml_filename)

        self.report.write('output_files')
        self.output_files()
        
        self.report.write('clean directory')
        self.clean_work_path()
        
        
        if os.path.exists(param_err_filename):
            self.report.write('delete ' + param_err_filename)
            os.unlink(param_err_filename)
        if os.path.exists(param_result_filename):
            self.report.write('delete ' + param_result_filename)
            os.unlink(param_result_filename)

        self.report.write('validate_and_transform ' + self.sgml_xml_filename + ' ' + xsl_sgml2xml + ' ' + self.xml_scielo)
        if self.validate_and_transform(self.sgml_xml_filename, xsl_sgml2xml, self.xml_scielo, ''):
            
            xml_java.replace_dtd_path(self.xml_scielo, self.dtd)
            
            self.report.write('validate_and_transform ' + self.xml_scielo + ' ' + xsl_xml2pmc + ' ' + self.xml_pmc_local)
            if self.validate_and_transform(self.xml_scielo, xsl_xml2pmc, self.xml_pmc_local, self.dtd):
                xml_java.replace_dtd_path(self.xml_pmc_local, self.dtd)

                print('\nXML for SciELO: ' + self.xml_scielo)
                self.report.write('transform ' + self.xml_pmc_local + ' '+  xsl_err + ' '+  self.xml_report)
                if self.transform(self.xml_pmc_local, xsl_err, self.xml_report):
                    # Generate self.report.html
                    self.report.write('transform ' + self.xml_report + ' '+  xsl_report + ' '+  self.html_report)
                    if self.transform(self.xml_report, xsl_report, self.html_report):
                        self.report.write('done')
                        print('\nValidation report: ' + self.html_report)
                    
                self.report.write('transform ' + self.xml_pmc_local + ' '+  xsl_preview + ' '+  self.html_preview )
                if self.transform(self.xml_pmc_local, xsl_preview, self.html_preview, {'path_img': self.work_path +'/', 'css':css}):
                    # Generate xml (final version)
                    self.report.write('done')
                    self.copy_img_files_to_preview()
                    self.report.write('copy_img_files_to_preview')
                    print('\nPreview: ' + self.html_preview)
                
                self.report.write('transform ' + self.xml_pmc_local + ' '+  xsl_pmc + ' '+  self.xml_pmc)
                if self.transform(self.xml_pmc_local, xsl_pmc, self.xml_pmc):
                    #shutil.copyfile(self.xml_pmc_local, xml_pmc)
                    self.report.write('Generated xml pmc final')

                    self.copy_from_work_to_xml_package()
                    self.report.write('copy_from_work_to_xml_package')
                    
                    self.copy_from_work_to_pmc_package()
                    self.report.write('copy_from_work_to_pmc_package')
                    print('\nXML for PMC: ' + self.xml_pmc)
                            
                                                                
        if os.path.exists(self.html_preview):
            self.report.write('END - OK')
            if self.html_preview != param_result_filename:
                self.report.write('copy ' + self.html_preview + ' ' +  param_result_filename)
                shutil.copyfile(self.html_preview, param_result_filename)
                #print(self.html_preview)
        else:
            self.report.write('END - ERROR')
            if not os.path.exists(self.err_filename):
                f = open(self.err_filename, 'w')
                f.write('error')
                f.close()
            
            if self.err_filename != param_err_filename:
                self.report.write('copy ' + self.err_filename + ' ' +  param_err_filename)
                shutil.copyfile(self.err_filename, param_err_filename)
            #print(self.err_filename)
    

    def clean_work_path(self):
        files = [ self.name + ext for ext in outputs_extensions ]
        for f in files:
            if os.path.exists(self.work_path + '/' + f):
                os.unlink(self.work_path + '/' + f)    

    def copy_from_work_to_xml_package(self):
        if os.path.exists(self.xml_scielo):
            shutil.copyfile(self.xml_scielo, self.xml_package_path + '/' + self.new_name + '.xml')
                

    def copy_from_work_to_pmc_package(self):
        self.report.write('copy_from_work_to_pmc_package')

        if os.path.isfile(self.xml_pmc):
            new_fullname = self.pmc_package_path + '/' + self.new_name 
            self.report.write('copy ' + self.xml_pmc + ' ' + new_fullname)
            shutil.copy(self.xml_pmc, new_fullname + '.xml')

            if os.path.exists(self.pdf_filename):
                self.report.write('copy ' + self.pdf_filename + ' ' + new_fullname)
                shutil.copy(self.pdf_filename, new_fullname + '.pdf')
             
            img_extension = ''
            for old_and_new_img_name in self.xml_images_list:
                old_img_name = old_and_new_img_name[0]
                self.report.write(old_img_name)
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
                    self.report.write('ERROR: one of the files below is expected:' + "\n" + '\n'.join(expected_files))
                 

    def copy_img_files_to_preview(self):
        msg = ''
        self.report.write('copy_img_files_to_preview')
        self.report.write('\n'.join(self.xml_images_list))
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
            self.report.write( msg )

