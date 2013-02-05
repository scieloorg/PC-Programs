
import shutil
import os
import sys
import tempfile
import reuse.xml.xml_java as xml_java

xml_tree = None
report = None



def img_to_jpeg(self, img_path, jpg_path):
    import Image
    files = os.listdir(img_path)
    if not os.path.exists(jpg_path):
        os.makedirs(jpg_path)

    for f in files:
        new_file = jpg_path + '/'+ f[0:f.rfind('.')] + '.jpg'
        hd_image_filename = img_path + '/'+ f
        
        if os.path.exists(jpg_filename):
            os.unlink(jpg_filename)
        
        if f.endswith('.jpg'):
            shutil.copyfile(hd_image_filename, new_file)
        else:
            try:
                im = Image.open(hd_image_filename)
                im.thumbnail(im.size)
                im.save(jpg_filename, "JPEG")
            
            except Exception, e:
                print e
                print jpg_filename



def prepare_path(path, startswith = '', endswith = ''):
    if not os.path.exists(path):
        os.makedirs(path)
    for file in os.listdir(path):
        filename = path + '/' + file
        if len(startswith)>0:
            if file.startswith(startswith):
                os.unlink(filename)
        if len(endswith)>0:
            if file.endswith(endswith) and os.path.exists(file):
                os.unlink(filename)
        if len(endswith) == 0 and len(startswith) == 0:
            os.unlink(filename)

def fix_xml(xml):
    f = open(xml, 'r')
    c = f.read()
    f.close()
    new_c = c[0:c.rfind('>')+1]
    if new_c != c:            
        f = open(xml, 'w')
        f.write(new_c)
        f.close()


class XMLData:
    def __init__(self, xml_filename, report):
        xml_tree.load(xml_filename, report)
        

    def xml_data_new_name_from_sgmxml(self, acron = ''):
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

    def xml_data_new_name_from_xml(self, alternative_page, acron = ''):
        nodes = xml_tree.return_nodes()
        
        article_meta_node = xml_tree.return_nodes('front/article-meta', nodes[0])
        
        node_issn = xml_tree.return_nodes('front/journal-meta/issn', nodes[0])
        

        node_volume = xml_tree.return_nodes('volume', article_meta_node[0])
        node_number = xml_tree.return_nodes('issue', article_meta_node[0])
        node_fpage = xml_tree.return_nodes('fpage', article_meta_node[0])
        
        volume = node_volume[0].text
        number  = node_number[0].text
        fpage = node_fpage[0].text


        
        issn = node_issn[0].text

        number = number.lower().replace(' ', '_')

        if len(nodes)>0:
            page_or_alternative_page = fpage
            if fpage.replace('0','') == '':
                page_or_alternative_page = alternative_page
            r = ''
            for l in page_or_alternative_page:
                if l.isdigit():
                    r += l
            page_or_alternative_page = r

            issueno = '0' + number
            issueno = issueno[-2:]            
            if len(acron)>0:
                acron += '-'
            r = issn + '-' + acron  + volume + '-' + issueno + '-' +  page_or_alternative_page
        return r



    def xml_data_image_names(self, tags='fig | table-wrap | inline-graphic | figgrp | tabwrap | equation'):
        a = []        
        names = tags.split(' | ')

        names = [ './/' + n for n in names ]

        test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href'] 
        root = xml_tree.return_nodes()
        #print(root)
        for tag in names:
            
            xml_tree.debug = 3
            nodes = xml_tree.return_nodes(tag, root[0])
            #print(nodes)
            if tag == 'inline-graphic':
                new_name_suffix = 'i'
                inlines = []
                for gnode in nodes:
                    for test in test_href:
                        if test in gnode.attrib.keys():
                            current_href = gnode.attrib[test]
                            break
                    if len(current_href)>0:
                        current_href = current_href.replace('.jpg', '')
                        current_href = current_href.replace('.tiff', '')
                        current_href = current_href.replace('.tif', '')
                        inlines.append(current_href)
                c = ''
                for i in inlines:
                    c += '0'
                j = 0 
                for i in inlines:
                    j += 1
                    k = c + str(j)
                    k = k[-len(c):]
                    a.append((i, 'i' + k))
            else:
                for node in nodes:
                                   
                    current_href = ''
                    new_name_suffix = None

                    if 'id' in node.attrib.keys():
                        new_name_suffix = node.attrib['id']
                    
                    if new_name_suffix[0:1] == 'e':
                        new_name_suffix = 'e' + new_name_suffix
                    else:
                        new_name_suffix = 'g' + new_name_suffix
                    #print(new_name_suffix)
                    if 'filename' in node.attrib.keys():
                        current_href = node.attrib['filename']


                        if len(current_href)>0:
                            current_href = current_href.replace('.jpg', '')
                            current_href = current_href.replace('.tiff', '')
                            current_href = current_href.replace('.tif', '')

                            a.append( (current_href , new_name_suffix) )
                    else:

                        graphic_nodes = xml_tree.return_nodes('graphic', node)
                        #print(graphic_nodes)
                        for gnode in graphic_nodes:
                            for test in test_href:
                                if test in gnode.attrib.keys():
                                    current_href = gnode.attrib[test]
                                    break
                            if len(current_href)>0:
                                current_href = current_href.replace('.jpg', '')
                                current_href = current_href.replace('.tiff', '')
                                current_href = current_href.replace('.tif', '')
                                a.append( (current_href , new_name_suffix) )
        return a

    def data_to_rename(self, acron, alternative_id = ''):
        
        if len(alternative_id) == 0:
            #print(1)
            new_name = self.xml_data_new_name_from_sgmxml(acron)
            
        else:
            new_name =  self.xml_data_new_name_from_xml(alternative_id, acron)
        xml_images_list =  self.xml_data_image_names() 
        return (new_name, xml_images_list)


class Validator:
    def __init__(self, dtd, xsl_prep_report, xsl_report, xsl_preview, xsl_output, css):
        self.xsl_report = xsl_report
        self.xsl_prep_report = xsl_prep_report
        self.xsl_preview = xsl_preview
        self.xsl_output = xsl_output
        self.dtd = dtd 
        self.css = css
        

    
    def set_output_filenames(self, xml_filename, work_path, validation_report_filename, preview_filename, xml_output_filename):
        self.xml_filename = xml_filename
        
        self.work_path = work_path

        self.xml_output_path = os.path.dirname(xml_output_filename)
        
        self.xml_path = os.path.dirname(self.xml_filename)
        self.basename = os.path.basename(self.xml_filename)
        self.name = self.basename.replace('.xml', '')
        
        paths = [self.work_path, os.path.dirname(validation_report_filename), os.path.dirname(preview_filename), os.path.dirname(xml_output_filename)] 
        for p in paths:
            
            if os.path.exists(p):
                for f in os.listdir(p):
                    
                    if f.startswith(self.name) and not self.basename == f:
                        
                        os.unlink(p + '/' + f)
            else:
                os.makedirs(p)

        self.xml_ouput_filename = xml_output_filename
        self.html_report = validation_report_filename
        self.html_preview = preview_filename
        
        self.xml_report = self.work_path + '/' + self.name + '.rep.xml'
        self.result_filename = self.work_path + '/' + self.name  + '.res.tmp'
        self.err_filename = self.work_path + '/' + self.name  + '.err.tmp'        

 
                

            
    

    def validate(self, report, img_path, new_name = ''):  
        
        report.write('\nValidating:' + self.xml_filename)

        xml_java.replace_dtd_path(self.xml_filename, self.dtd)
        
        if xml_java.validate(self.xml_filename, self.dtd, self.result_filename, self.err_filename):              
            report.write('transform ' + self.xml_filename + ' '+  self.xsl_prep_report + ' '+  self.xml_report)
            if xml_java.transform(self.xml_filename, self.xsl_prep_report, self.xml_report, self.err_filename):
                # Generate self.report.html
                report.write('transform ' + self.xml_report + ' '+  self.xsl_report + ' '+  self.html_report)
                if xml_java.transform(self.xml_report, self.xsl_report, self.html_report, self.err_filename):
                    os.unlink(self.xml_report)
                    report.write('Validation report:' + self.html_report, True, False, True)
                else:
                    report.write('Unable to create validation report: ' + self.html_report, True, True, True)
            else:
                report.write('Unable to generate xml for report: ' + self.xml_report, True, True, True)

            if type(self.xsl_preview) == type([]):
                xml_java.tranform_in_steps(self.xml_filename, self.dtd, self.xsl_preview, self.html_preview, {'path_img': img_path +'/', 'css': self.css, 'new_name': new_name})
            else:
                report.write('transform ' + self.xml_filename + ' '+  self.xsl_preview + ' '+  self.html_preview )
                xml_java.transform(self.xml_filename, self.xsl_preview, self.html_preview, self.err_filename, {'path_img': img_path +'/', 'css': self.css, 'new_name': new_name})
            if os.path.exists(self.html_preview):
                report.write('Preview ' +  self.html_preview, True, False, True)
            else:
                report.write('Unable to create preview: ' + self.html_preview, True, True, True)
            
            report.write('transform ' + self.xml_filename + ' '+  self.xsl_output + ' '+  self.xml_ouput_filename)

            if xml_java.transform(self.xml_filename, self.xsl_output, self.xml_ouput_filename, self.err_filename):
                report.write('Result ' +  self.xml_ouput_filename)
            else:
                report.write('Unable to create result: ' + self.xml_ouput_filename, True, True, True)
                
        if os.path.exists(self.xml_ouput_filename):
            report.write('END - OK')
            r = True
        else:
            report.write('END - ERROR')
            if not os.path.exists(self.err_filename):
                f = open(self.err_filename, 'w')
                f.write('error')
                f.close()
            report.write('Errors: read ' + self.err_filename, False, True, True)
            r = False
        return r

class SGML2XML:
    def __init__(self, xsl_sgml2xml):
        self.xsl_sgml2xml = xsl_sgml2xml
        
    def generate_xml_from_sgmxml(self, sgml_xml, xml_filename):
        result_filename = sgml_xml + '.res'
        err_filename = sgml_xml + '.err'
        #xml_filename = sgml_xml.replace('.sgm.xml', '.xml')
        fix_xml(sgml_xml)
        r = xml_java.transform(sgml_xml, self.xsl_sgml2xml, xml_filename, err_filename)
        if os.path.exists(err_filename):
            if not report == None:
                report.write('Unable to create ' + xml_filename + ' from ' + sgml_xml, True, False, True)
                report.write(err_filename, True, False, True)
        
class SciELOPackage:
    def __init__(self, sgmlxml):  
        self.sgmlxml = sgmlxml
        

    def set_parameters(self, report, src_xml_path, src_paths_and_exts, src_img_path, package_path):   
        self.src_xml_path = src_xml_path
        self.src_paths_and_exts = src_paths_and_exts
        self.src_img_path = src_img_path
        self.package_path = package_path
        self.new_name = ''
        self.xml_images_list = []
        self.name = ''
        self.report = report

        if not os.path.exists(self.package_path):
            os.makedirs(self.package_path)

    def prepare_file(self, xml_filename, alternative_id, acron):
        self.xml_filename = xml_filename
        data_filename = xml_filename
        if '.sgm.xml' in self.xml_filename:
            if os.path.exists(xml_filename):
                sgml2xml_filename = self.xml_filename
                self.xml_filename = self.xml_filename.replace('.sgm.xml', '.xml')
                # generate XML SciELO and rename href img according to pmc naming rules
                self.report.write('Converting ' + sgml2xml_filename + '->' + self.xml_filename, True, False, True)
                self.sgmlxml.generate_xml_from_sgmxml(sgml2xml_filename, self.xml_filename)
                    
                alternative_id = ''
        r = False
        if os.path.exists(self.xml_filename):
            self.name = os.path.basename(self.xml_filename).replace('.xml', '')
          
            is_pmc_valid_name = False
            if '-' in self.name:
                if len(self.name.split('-')) > 5:
                    is_pmc_valid_name = True

            if is_pmc_valid_name:
                for f in os.listdir(os.path.dirname(self.xml_filename)):
                    if f.startswith(self.name):
                        shutil.copyfile(os.path.dirname(self.xml_filename) + '/' + f, self.package_path +'/' +f)
            else:
                # filename must contain old img href
                self.report.write('Rename files and copy them to ' + self.package_path, True, False, True)
                xml_data = XMLData(data_filename, self.report)
                self.new_name, self.xml_images_list = xml_data.data_to_rename(acron, alternative_id)
                self.add_xml_to_package()
                self.add_file_to_package()
                self.add_img_to_package(['.jpg', '.tiff', '.tif', '.eps'])
            r = True
        else:
            self.report.write('Missing ' + self.xml_filename, True, True, True)
            self.report.write('ERROR', True, True, True)
        return r

    def add_img_to_package(self, ext_list):
        if self.name != self.new_name and self.new_name != '':
            # renaming as copying to package folder
            for ext in ext_list:
                self.copy_renamed_img_files(ext)
        else:
            # do not rename, only copy the files
            for ext in ext_list:
                self.copy_files_which_match_pattern(self.src_img_path, ext)

    def copy_files_which_match_pattern(self, src_path, ext):
        for f in os.listdir(src_path):
            if f.startswith(self.name) and f.endswith(ext):
                shutil.copyfile(f, self.package_path + '/' + os.path.basename(f))

    def copy_renamed_img_files(self, ext = '.jpg'):
        missing_files = []
        for old_and_new in self.xml_images_list:
            old_name = old_and_new[0]
            new_name = old_and_new[1]
            #print(old_name)
            #print(new_name)
            
            if not ext in old_name:
                old_name += ext        
            if not ext in new_name:
                new_name += ext

            
            if os.path.isfile(self.src_img_path  + '/' + old_name ):
                #print('Copying ' + self.src_img_path  + '/' + old_name + ' -> ' + self.package_path + '/' + self.new_name + '-' + new_name)
                shutil.copyfile(self.src_img_path  + '/' + old_name, self.package_path + '/' + self.new_name + '-' + new_name)
            else:
                missing_files.append(self.src_img_path  + '/' + old_name)
            if len(missing_files) > 0:
                self.report.write('Unable to find the files:' + '\n'.join(missing_files), True, True, True)
        return missing_files    

    def add_file_to_package(self):
        if self.name != self.new_name and self.new_name != '':
            for src_path, ext in self.src_paths_and_exts:
                #print(src_path + '/' + self.name + ext)
                if os.path.exists(src_path + '/' + self.name + ext):
                    #print('Copying from ' + src_path + '/' + self.name + ext + ' to ' + self.package_path + '/' + self.new_name + ext)
                    shutil.copyfile(src_path + '/' + self.name + ext, self.package_path + '/' + self.new_name + ext)
        else:
            #print(src_path + '/' + self.name + ext)
            if os.path.exists(src_path + '/' + self.name + ext):
                #print('Copying from ' + src_path + '/' + self.name + ext + ' to ' + self.package_path + '/' + self.name + ext)
                    
                shutil.copyfile(src_path + '/' + self.name + ext, self.package_path + '/' + self.name + ext)

    def add_xml_to_package(self):
        if self.name != self.new_name and self.new_name != '':
            shutil.copyfile(self.xml_filename, self.package_path + '/' + self.new_name + '.xml')
        else:
            shutil.copyfile(self.xml_filename, self.package_path + '/' + self.name + '.xml')

    def do_for_all(self, acron):
        for xml_file in os.listdir(self.src_xml_path):
            if xml_file.endswith('.xml'):
                alternative_id = xml_file.replace('.xml', '')
                self.prepare_file(self.src_xml_path + '/' + xml_file, alternative_id, acron)

    def do_for_one(self, acron, xml_filename):
        if self.src_xml_path == os.path.dirname(xml_filename) and xml_filename.endswith('.xml'):
            if os.path.isfile(xml_filename):
                xml_file = os.path.basename(xml_filename)
                alternative_id = xml_file.replace('.xml', '')
                self.prepare_file(xml_filename, alternative_id, acron)
        

class PMCPackage:
    def __init__(self, validator_pmc, validator_scielo):
        
        self.validator_scielo = validator_scielo
        self.validator_pmc = validator_pmc
        

    def convert_file(self, report, xml_filename, work_path, scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview, pmc_path):
        r = False
        if not os.path.exists(work_path):
            os.makedirs(work_path)
        
        name = os.path.basename(xml_filename)
        pmc_xml_local = work_path + '/' + name.replace('.xml', '.local.xml')
        report.write('\nProcess ' + xml_filename, True, False, True)
        self.validator_scielo.set_output_filenames(xml_filename, work_path, scielo_html_validation_report, scielo_html_preview, pmc_xml_local)
        if self.validator_scielo.validate(report, os.path.dirname(xml_filename), name.replace('.xml', '.local.xml')):
            # generate pmc package
            if not os.path.exists(pmc_path):
                os.makedirs(pmc_path)
            self.validator_pmc.set_output_filenames(pmc_xml_local, work_path, pmc_html_validation_report, pmc_html_preview, pmc_path + '/' + name )         
            if self.validator_pmc.validate(report, os.path.dirname(xml_filename)):
                if os.path.exists(pmc_xml_local):
                    os.unlink(pmc_xml_local)
                if os.path.exists(pmc_path + '/' + name):
                    report.write('Created ' + pmc_path + '/' + name + '\n', True, False, True)

        
        return r                

    def do_for_all(self, report, scielo_package_path, pmc_path, validation_path, scielo_html_validation_report_ext = '.rep.html', scielo_html_preview_ext = '.xml.html', pmc_html_validation_report_ext = '.pmc.rep.html', pmc_html_preview_ext = '.pmc.xml.html'):        
        if not os.path.exists(pmc_path):
            os.makedirs(pmc_path)
        for filename in os.listdir(scielo_package_path):
            if filename.endswith('.xml'):
                name = filename.replace('.xml', '')

                scielo_html_validation_report = validation_path + '/' + name + scielo_html_validation_report_ext
                scielo_html_preview = validation_path + '/' + name + scielo_html_preview_ext
                pmc_html_validation_report = validation_path + '/' + name + pmc_html_validation_report_ext
                pmc_html_preview = validation_path + '/' + name + pmc_html_preview_ext

                self.convert_file(report, scielo_package_path + '/' + filename, validation_path, scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview, pmc_path)
            elif not filename.endswith('.jpg'):
                shutil.copyfile(scielo_package_path + '/' + filename, pmc_path+ '/' + filename)

    def do_for_one(self, report, xml_filename, pmc_package_path, validation_path, scielo_html_validation_report_ext = '.rep.html', scielo_html_preview_ext = '.xml.html', pmc_html_validation_report_ext = '.pmc.rep.html', pmc_html_preview_ext = '.pmc.xml.html'):       
        if not os.path.exists(pmc_package_path):
            os.makedirs(pmc_package_path)
        report.write('Generate PMC from ' + xml_filename, True, False, True) 
        if os.path.isfile(xml_filename) and xml_filename.endswith('.xml'):
            report.write('Generate PMC from ' + xml_filename, True, False, True)
            scielo_package_path = os.path.dirname(xml_filename)
            name = os.path.basename(xml_filename).replace('.xml', '')

            files = [ f for f in os.listdir(scielo_package_path) if f.startswith(name) ]

            for filename in files:
                if filename.endswith('.xml'):
                    report.write('Converting ' + xml_filename)
                    scielo_html_validation_report = validation_path + '/' + name + scielo_html_validation_report_ext
                    scielo_html_preview = validation_path + '/' + name + scielo_html_preview_ext
                    pmc_html_validation_report = validation_path + '/' + name + pmc_html_validation_report_ext
                    pmc_html_preview = validation_path + '/' + name + pmc_html_preview_ext
                    
                    self.convert_file(report, scielo_package_path + '/' + filename, validation_path, scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview, pmc_package_path)
                    
                    items = [scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview, pmc_package_path + '/' + filename, ]
                    for i in items:
                        if os.path.exists(i ):
                            report.write('Generated: ' + i, True, False, True)
                        else:
                            report.write('Unable to generate: ' + i, True, True, True)
                        

                elif not filename.endswith('.jpg'):
                    shutil.copyfile(scielo_package_path + '/' + filename, pmc_package_path + '/' + filename)
        else:
            report.write('Missing ' + xml_filename, True, True, True)


class XMLPacker:
    def __init__(self, path_pmc, path_jar):


        path_xsl = path_pmc + '/v3.0/xsl'

        dtd = path_pmc + '/v3.0/dtd/journalpublishing3.dtd' 
        css = path_pmc + '/v3.0/xsl/web/xml.css'


        xsl_sgml2xml = path_xsl + '/sgml2xml/sgml2xml.xsl'

        xsl_prep_report = path_xsl + '/scielo-style/stylechecker.xsl'
        xsl_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
        xsl_preview = path_xsl + '/previewer/preview.xsl'
        xsl_output = path_xsl + '/sgml2xml/xml2pmc.xsl'

        pmc_xsl_prep_report = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
        pmc_xsl_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
        pmc_xsl_preview = [ path_xsl + '/jpub/citations-prep/jpub3-PMCcit.xsl', path_xsl + '/previewer/jpub-main-jpub3-html.xsl', ]
        pmc_xsl_output = path_xsl + '/sgml2xml/pmc.xsl'
        pmc_css = path_pmc + '/v3.0/xsl/jpub/jpub-preview.css'

        #xml_toolbox.xml_tree = XMLTree(TableEntities(current_path + '/reuse/encoding/entities'))

        xml_java.jar_transform = path_jar + '/saxonb9-1-0-8j/saxon9.jar' 
        xml_java.jar_validate = path_jar + '/XMLCheck.jar'

        validator_scielo = Validator(dtd, xsl_prep_report, xsl_report, xsl_preview, xsl_output, css)
        validator_pmc = Validator(dtd, pmc_xsl_prep_report, pmc_xsl_report, pmc_xsl_preview, pmc_xsl_output, pmc_css)

        
        self.scielo_package = SciELOPackage(SGML2XML(xsl_sgml2xml))
        self.pmc_package = PMCPackage(validator_pmc, validator_scielo)

    def generate_one_file(self, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, report, acron, xml_filename, pmc_package_path, reports_path):    
        self.scielo_package.set_parameters(report, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path)

        self.scielo_package.do_for_one(acron, xml_filename)
        self.pmc_package.do_for_one(report, self.scielo_package.package_path + '/' + self.scielo_package.new_name + '.xml', pmc_package_path, reports_path)

    def generate_one_folder(self, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, report, acron, pmc_package_path, reports_path):
        self.scielo_package.set_parameters(report, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path)
        self.scielo_package.do_for_all(acron)
        self.pmc_package.do_for_all(report, scielo_package_path, pmc_package_path, reports_path)