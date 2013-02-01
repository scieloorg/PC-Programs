
import shutil
import os
import sys
import tempfile
import reuse.xml.xml_java as xml_java

xml_tree = None

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
        article_meta_node = xml_tree.return_nodes('article-meta', nodes[0])
        volume = xml_tree.return_nodes('volume', article_meta_node[0])
        number = xml_tree.return_nodes('issue', article_meta_node[0])
        fpage = xml_tree.return_nodes('first-page', article_meta_node[0])
        issn = xml_tree.return_nodes('issn', article_meta_node[0])
        
        number = number.lower().replace(' ', '_')

        if len(nodes)>0:
            page_or_alternative_page = fpage[0]
            if fpage.replace('0','') == '':
                page_or_alternative_page = alternative_page
            r = ''
            for l in page_or_alternative_page:
                if l.isdigit():
                    r += l
            page_or_alternative_page = r

            issueno = '0' + number[0]
            issueno = issueno[-2:]            
            if len(acron)>0:
                acron += '-'
            r = issn[0] + '-' + acron  + volume[0] + '-' + issueno + '-' +  page_or_alternative_page
        return r



    def xml_data_image_names(self, tags='fig | table-wrap | inline-graphic | figgrp | tabwrap | equation'):
        a = []        
        names = tags.split(' | ')
        test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href'] 

        for tag in names:
            #print tag
            xml_tree.debug = 3
            nodes = xml_tree.return_nodes(tag)
            
            if tag == 'inline-graphic':
                new_name_suffix = 'i'
                inlines = []
                for gnode in nodes:
                    for test in test_href:
                        if test in gnode.attrib.keys():
                            current_href = gnode.attrib[test]
                            break
                    if len(current_href)>0:
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

                    if 'filename' in node.attrib.keys():
                        current_href = node.attrib['filename']
                    else:

                        graphic_nodes = xml_tree.return_nodes('graphic', node)
                        
                        for gnode in graphic_nodes:
                            for test in test_href:
                                if test in gnode.attrib.keys():
                                    current_href = gnode.attrib[test]
                                    break
                        if len(current_href)>0:
                            a.append( (current_href , new_name_suffix) )
        return a

    def data_to_rename(self, acron, alternative_id = ''):
        
        if len(alternative_id) == 0:
            new_name = self.xml_data_new_name_from_sgmxml(acron)
            
        else:
            new_name =  self.xml_data_new_name_from_xml(alternative_id, acron)
        xml_images_list =  self.xml_data_image_names() 
        return (new_name, xml_images_list)


class Validator:
    def __init__(self, dtd, xsl_validation, xsl_prep_report, xsl_report, xsl_preview, xsl_output, report, img_path, css):
        self.xsl_validation = xsl_validation
        self.xsl_report = xsl_report
        self.xsl_prep_report = xsl_prep_report
        self.xsl_preview = xsl_preview
        self.xsl_output = xsl_output
        self.report = report
        self.dtd = dtd 
        self.img_path = img_path
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
                    if f.startswith(self.name):
                        os.unlink(p + '/' + f)
            else:
                os.makedirs(p)

        self.xml_ouput_filename = xml_output_filename
        self.html_report = validation_report_filename
        self.html_preview = preview_filename
        
        self.xml_report = self.work_path + '/' + self.name + '.rep.xml'
        self.result_filename = self.work_path + '/' + self.name  + '.res.tmp'
        self.err_filename = self.work_path + '/' + self.name  + '.err.tmp'        

 
                
    def tranform_in_steps(self, xml, xsl_list, result, parameters={}):
        inputfile = xml

        from tempfile import mkstemp
        
        _, res = mkstemp()
        _, err = mkstemp()
        for xsl in xsl_list:
            _, outputfile = mkstemp()
            xml_java.transform(inputfile, xsl, outputfile, res, err, parameters)
            inputfile = outputfile
            if inputfile != xml:
                os.unlink(inputfile)
        if os.path.exists(outputfile):
            shutil.move(outputfile, result)
               
    def validate(self):  
        report = self.report
        report.write('XML filename:' + self.xml_filename, True, False, True)

        xml_java.replace_dtd_path(self.xml_filename, self.dtd)
        
        if xml_java.validate(self.xml_filename, self.dtd, self.result_filename, self.err_filename):              
            report.write('transform ' + self.xml_filename + ' '+  self.xsl_prep_report + ' '+  self.xml_report)
            if xml_java.transform(self.xml_filename, self.xsl_prep_report, self.xml_report, self.result_filename, self.err_filename)
                # Generate self.report.html
                report.write('transform ' + self.xml_report + ' '+  self.xsl_report + ' '+  self.html_report)
                if xml_java.transform(self.xml_report, self.xsl_report, self.html_report, self.result_filename, self.err_filename):
                    report.write('Validation report:' + self.html_report, True, False, True)
                    
            if type(self.xsl_preview) == type([]):
                self.tranform_in_steps(self.xml_filename, self.xsl_preview, self.html_preview, {'path_img': self.img_path +'/', 'css':css})
            else:
                report.write('transform ' + self.xml_filename + ' '+  self.xsl_preview + ' '+  self.html_preview )
                xml_java.transform(self.xml_filename, self.xsl_preview, self.html_preview, self.result_filename, self.err_filename, {'path_img': self.img_path +'/', 'css':css})
            if os.path.exists(self.html_preview):
                report.write('Preview ' +  self.html_preview, True, False, True)
            
            report.write('transform ' + self.xml_filename + ' '+  self.xsl_output + ' '+  self.xml_ouput_filename)

            if xml_java.transform(self.xml_filename, self.xsl_output, self.xml_ouput_filename, self.result_filename, self.err_filename):
                report.write('Result ' +  self.result_filename, True, False, True)
                
        if os.path.exists(self.xml_ouput_filename):
            report.write('END - OK')
            r = True
        else:
            report.write('END - ERROR')
            if not os.path.exists(self.err_filename):
                f = open(self.err_filename, 'w')
                f.write('error')
                f.close()
            r = False
            
class SGML2XML:
    def __init__(self, xsl_sgml2xml):
        self.xsl_sgml2xml = xsl_sgml2xml
        
    def generate_xml_from_sgmxml(self, sgml_xml, xml_filename):
        result_filename = sgml_xml + '.res'
        err_filename = sgml_xml + '.err'
        #xml_filename = sgml_xml.replace('.sgm.xml', '.xml')
        fix_xml(sgml_xml)
        xml_java.transform(sgml_xml, self.xsl_sgml2xml, xml_filename, result_filename, err_filename)
        

class ArticlePackageFiles:
    def __init__(self, name, package_path, new_name, xml_images_list):        
        self.name = name
        self.new_name = new_name
        self.xml_images_list = xml_images_list
        self.package_path = package_path

    def add_img_to_package(self, img_path, ext_list):
        if self.name != self.new_name and new_name != '':
            # renaming as copying to package folder
            for ext in ext_list:
                self.copy_renamed_img_files(img_path, ext)
        else:
            # do not rename, only copy the files
            for ext in ext_list:
                self.copy_files_which_match_pattern(img_path, ext)

    def copy_files_which_match_pattern(self, src_path, ext):
        for f in os.listdir(src_path):
            if f.startswith(self.name) and f.endswith(ext):
                shutil.copyfile(f, self.package_path + '/' + os.path.basename(f))

    def copy_renamed_img_files(self, src_path, ext = '.jpg'):
        missing_files = []
        for old_and_new in self.xml_images_list:
            old_name = old_and_new[0]
            new_name = old_and_new[1]
            if not ext in old_name:
                old_name += ext        
            if not ext in new_name:
                new_name += ext
            if os.path.isfile(src_path + '/' + old_name ):
                shutil.copyfile(src_path + '/' + old_name, self.package_path + '/' + self.new_name + '-' + new_name + ext)
            else:
                missing_files.append(src_path + '/' + old_name)
        
        return missing_files    

    def add_file_to_package(self, src_paths_and_exts):
        if self.name != self.new_name and new_name != '':
            for src_path, ext in src_paths_and_exts:
                shutil.copyfile(src_path + '/' + self.name + ext, self.package_path + '/' + self.new_name + ext)
        else:
            shutil.copyfile(src_path + '/' + self.name + ext, self.package_path + '/' + self.name + ext)

    def add_xml_to_package(self, filename):
        if self.name != self.new_name and new_name != '':
            shutil.copyfile(filename, self.package_path + '/' + self.new_name + '.xml')
        else:
            shutil.copyfile(filename, self.package_path + '/' + self.name + '.xml')
    



class Package:
    def __init__(self, validator_pmc, validator_scielo, sgmlxml):
        
        self.validator_scielo = validator_scielo
        self.validator_pmc = validator_pmc
        self.sgmlxml = sgmlxml

    def prepare_scielo_package(self, xml_filename, src_paths_and_exts, src_img_path, package_path, alternative_id, acron):
        filename = xml_filename
        if '.sgm.xml' in xml_filename:
            if os.path.exists(xml_filename):
                sgml2xml_filename = xml_filename
                xml_filename = sgml2xml_filename.replace('.sgm.xml', '.xml')
                # generate XML SciELO and rename href img according to pmc naming rules
                self.sgmlxml.generate_xml_from_sgmxml(sgml2xml_filename, xml_filename)
                alternative_id = ''
        
        name = os.basename(xml_filename).replace('.xml', '')
        is_pmc_valid_name = False
        if '-' in name:
            if len(name.split('-')) >=4:
                is_pmc_valid_name = True

        if not is_pmc_valid_name:
            # filename must contain old img href
            xml_data = XMLData(filename)
            new_name, img_names = xml_data.data_to_rename(acron, alternative_id)
                
            a = ArticlePackageFiles(name, package_path, new_name, img_names)
            a.add_xml_to_package(filename)
            a.add_file_to_package(src_paths_and_exts)
            a.add_img_to_package(src_img_path, ['.jpg', '.tiff', '.tif', '.eps'])

    def convert_scielo2pmc(self, xml_filename, scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview, pmc_path):
        r = False

        pmc_xml_local = xml_filename.replace('.xml', '.local.xml')

        name = os.path.basename(xml_filename)
        work_path = os.path.dirname(xml_filename)

        self.validator_scielo.set_output_filenames(xml_filename, work_path, scielo_html_validation_report, scielo_html_preview, pmc_xml_local)
        if self.validator_scielo.validate():
            # generate pmc package
            self.validator_pmc.set_output_filenames(pmc_xml_local, work_path, pmc_html_validation_report, pmc_html_preview, pmc_path + '/' + name )         
            r = self.validator_pmc.validate()
        return r                

    def pack_all_files(self, xml_path, src_paths_and_exts, src_img_path, package_path, alternative_id, acron, scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview, pmc_path):        
        for xml_file in os.listdir(xml_path):
            if xml_file.endswith('.xml'):
                self.prepare_scielo_package(xml_path + '/' + xml_file, src_paths_and_exts, src_img_path, package_path, alternative_id, acron)

        for xml_file in os.listdir(package_path):
            if xml_file.endswith('.xml'):
                self.convert_scielo2pmc(package_path + '/' + xml_file, scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview, pmc_path)
            elif xml_file.endswith('.jpg'):
                pass
            else:
                shutil.copyfile(package_path + '/' + xml_file, pmc_path)

        


