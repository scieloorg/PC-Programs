
import shutil
import os
import sys
import tempfile
import reuse.xml.xml_java as xml_java

xml_tree = None
report = None



def img_to_jpeg(img_path, jpg_path):
    
    try:
        import Image

        files = [ f for f in os.listdir(img_path) if not f.endswith('.jpg') ]
        
        for f in files:
            jpg_filename = jpg_path + '/'+ f[0:f.rfind('.')] + '.jpg'
            image_filename = img_path + '/'+ f
            
            if jpg_filename != image_filename:
                try:
                    im = Image.open(image_filename)
                    im.thumbnail(im.size)
                    im.save(jpg_filename, "JPEG")
                
                except Exception, e:
                    print e
                    print jpg_filename
    except:
        print('Desirable have installed PIL in order to convert images to jpg')



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
        article_meta_node = xml_tree.return_nodes('.//article-meta', nodes[0])
        node_issn = xml_tree.return_nodes('.//front/journal-meta/issn', nodes[0])
        

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



    def xml_data_image_names(self):
        test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href'] 
        root = xml_tree.return_nodes()
        r = []
        nodes = xml_tree.return_nodes('.//*[graphic]', root[0])
        for n in nodes:
            id = xml_tree.return_node_attr_value(n, 'id')
            if '-' in id:
                id = id[id.rfind('-')+1:]
            if n.tag == 'equation':
                id = 'e' + id
            elif n.tag == 'inline-display':
                id = 'i' + id 
            else:
                id = 'g' + id
            graphic_nodes = xml_tree.return_nodes('graphic', n)
            if len(graphic_nodes) > 0:
                for test in test_href:
                    href = xml_tree.return_node_attr_value(graphic_nodes[0], test)
                    if len(href) > 0:
                        r.append((href, id))
                        break
        return r

    

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
                xml_java.tranform_in_steps(self.xml_filename, self.dtd, self.xsl_preview, self.html_preview, {'path_img': img_path +'/', 'css': 'file:///' + self.css, 'new_name': new_name})
            else:
                report.write('transform ' + self.xml_filename + ' '+  self.xsl_preview + ' '+  self.html_preview )
                xml_java.transform(self.xml_filename, self.xsl_preview, self.html_preview, self.err_filename, {'path_img': img_path +'/', 'css': 'file:///' + self.css, 'new_name': new_name})
            if os.path.exists(self.html_preview):
                report.write('Preview ' +  self.html_preview, True, False, True)
            else:
                report.write('Unable to create preview: ' + self.html_preview, True, True, True)
            
            report.write('transform ' + self.xml_filename + ' '+  self.xsl_output + ' '+  self.xml_ouput_filename)

            if xml_java.transform(self.xml_filename, self.xsl_output, self.xml_ouput_filename, self.err_filename):
                report.write('Result ' +  self.xml_ouput_filename)
            else:
                report.write('Unable to create result: ' + self.xml_ouput_filename, True, True, True)
        if os.path.isfile(self.result_filename):
            os.unlink(self.result_filename)
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
        
    def fix_xml_tags(self, xml):
        f = open(xml_filename, 'r')
        content = f.read()
        f.close()
        c = self.fix_tags(content)
        f = open(xml_filename, 'w')
        f.write(c)
        f.close()
        

    def fix_tags(self, content):
        tags = [ 'italic', 'bold', 'sub', 'sup']
        close_tags = [ '/italic', '/bold', '/sub', '/sup']
        stack = [] 
        ignore = []
      
        s = content.split( '<')
        n = 0
        r = ''

        for item in s:
            
            #print('\n' + item)
            #print('content:' + content)
            #print('result: ' + r)
            if n == 1:
                added = ''
                tag = item[0:item.find( '>')]
                if tag in tags:
                    # tag inicial
                    #print('empilha ' + tag)
                    stack.append(tag)
                    r +=  '<' + item
                    #print(stack)
                elif tag in close_tags:
                    # tag fecha
                    if tag in ignore:
                        k = 0 
                        for ign in ignore:
                            if ign == tag:
                                item = item[len(tag)+1:]
                                del ignore[k]
                                break
                            k += 1
                        r += item
                    else:

                        while tag[1:] != stack[len(stack)-1]:
                            added = '</' + stack[len(stack)-1] + '>'
                            #print('force close tag of the top of the stack ' + added)
                            #print('antes:')
                            #print(stack)
                            ignore.append('/' + stack[len(stack)-1])
                            del stack[len(stack)-1]
                        
                            #print('depois:')
                            #print(stack)

                            #print('ignore:')
                            #print(ignore)
                            r += added 
                        if tag[1:] == stack[len(stack)-1]:
                            #print('desempilha ' + stack[len(stack)-1])
                            del stack[len(stack)-1]
                            r +=  '<' + item
                            #print(stack)
                            
                else:
                    r += '<' + item
                
            else:
                r += item
            n = 1
        return r


    def sgmxml2xml(self, sgmxml_filename, xml_filename, err_filename, report):        
        fix_xml(sgmxml_filename)

        r = False
        if not xml_java.validate(sgmxml_filename, '', xml_filename.replace('.sgm.xml', '.res'), err_filename):
            self.fix_xml_tags(sgmxml_filename)
        if xml_java.validate(sgmxml_filename, '', xml_filename.replace('.sgm.xml', '.res'), err_filename):
            r = xml_java.transform(sgmxml_filename, self.xsl_sgml2xml, xml_filename, err_filename)
        if not r:
            report.write('Unable to create ' + xml_filename + ' from ' + sgmxml_filename, True, True, True)
            report.write(err_filename, True, True, True)
        return r
        

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

        
        self.checker = XMLPackagesChecker(SGML2XML(xsl_sgml2xml), validator_scielo, validator_pmc)
    


    def generate(self, filename, err_filename, acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path):    
        if os.path.isfile(err_filename):
            os.unlink(err_filename)
        self.checker.process(filename, err_filename, acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path)

    


    def generate_validation_reports(self, report, xml_path, pmc_package_path, reports_path, jpg_path):
        for f in os.listdir(xml_path):
            if f.endswith('.xml'):
                err_filename = path + '/' + f.replace('.xml', '.err.txt')
                xml_filename = path + '/' + f
                self.checker.validate_packages(report, err_filename, xml_filename, reports_path, pmc_package_path, jpg_path, '')


class XMLPackagesChecker:
    def __init__(self, sgmlxml, validator_scielo, validator_pmc):
        self.validator_scielo = validator_scielo
        self.validator_pmc = validator_pmc
        self.sgmlxml = sgmlxml
        self.scielo_html_validation_report_ext = '.rep.html'
        self.scielo_html_preview_ext = '.xml.html'
        self.pmc_html_validation_report_ext = '.pmc.rep.html'
        self.pmc_html_preview_ext = '.pmc.xml.html'
                

    
    def find_new_name(self, filename, acron, alternative_id, report):

        xml_data = XMLData(filename, report)
        new_name, img_list = xml_data.data_to_rename(acron, alternative_id)

        return (new_name, img_list)

    def prepare_file(self, filename, err_filename, acron, alternative_id, report):
        new_name = ''
        xml_images_list = []
        xml_filename = ''
        
        # if .sgm.xml converts it into xml
        if filename.endswith('.sgm.xml'):
            filename2 = filename.replace('.sgm.xml', '.xml')
            if self.sgmlxml.sgmxml2xml(filename, filename2, err_filename, report):
                new_name, xml_images_list = self.find_new_name(filename, acron, alternative_id, report)
            
                xml_filename = filename2
        elif filename.endswith('.xml'):
            xml_filename = filename
            new_name, xml_images_list = self.find_new_name(filename, acron, alternative_id, report)
            
        return (xml_filename, new_name, xml_images_list)
    
    def build_scielo_package(self, filename, dest_path, img_list, new_name):
        extensions = ['.jpg', '.tiff', '.tif', '.eps']
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        for f in os.listdir(dest_path):
            if f.startswith(new_name):
                os.unlink(dest_path + '/' + f)

        src_path = os.path.dirname(filename)
        if os.path.isdir(dest_path):
            name = os.path.basename(filename).replace('.xml', '')
            if new_name == name:
                # nao precisa renomear
                shutil.copyfile(filename, dest_path + '/' + name + '.xml')
                for f in os.listdir(src_path):
                    if f.startswith(name) and not f.endswith('.sgm.xml'):
                        shutil.copyfile(src_path + '/' + f, dest_path + '/' + f)
            else:
                # renomear
                self.rename(filename, dest_path + '/' + new_name + '.xml', img_list, new_name)

                for f in os.listdir(src_path):
                    if f.startswith(name) and not f.endswith('.xml'):
                        print('copying ' + dest_path + '/' + f.replace(name, new_name))
                        shutil.copyfile(src_path + '/' + f, dest_path + '/' + f.replace(name, new_name))                        
                
                for img_name, new_img_name in img_list:
                    if img_name[img_name.rfind('.'):] in extensions:
                        img_name = img_name[0:img_name.rfind('.')]
                    for ext in extensions:
                        src_img = src_path + '/' + img_name + ext
                        dest_img = dest_path + '/' + new_name + '-' + new_img_name + ext
                        if os.path.isfile(src_img):
                            print('copying '  + dest_img)
                            shutil.copyfile(src_img, dest_img )  


    def rename(self, filename, new_filename, xml_images_list, new_name):
        f = open(filename, 'r')
        c = f.read()
        f.close()

        f = open(new_filename, 'w')
        for img_ref, img_suffix in xml_images_list:
            
            c = c.replace(img_ref, new_name + '-' + img_suffix)
        f.write(c)
        f.close()
        

    def process(self, filename, err_filename, acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path):
        r = False
        if os.path.isfile(filename):
            path = os.path.dirname(filename)

            jpg  = [ f for f in os.listdir(path) if f.endswith('.jpg')]
            if len(jpg) == 0:
                hd  = [ f for f in os.listdir(path) if f.endswith('.tiff') or f.endswith('.tif') or f.endswith('.eps')]
                if len(hd) > 0:
                    img_to_jpeg(path, path) 
            # prepare file
            name = os.path.basename(filename).replace('.sgm', '').replace('.xml', '')
            xml_filename, new_name, img_list = self.prepare_file(filename, err_filename, acron, alternative_id, report)
            
            if os.path.isfile(err_filename):
                print(err_filename)
                shutil.copyfile(err_filename, err_filename.replace('.err.txt', '.ctrl'))
            else:
                # build scielo package
                
                new_xml_filename = scielo_package_path + '/' + new_name + '.xml'
                self.build_scielo_package(xml_filename, scielo_package_path, img_list, new_name)
                
                # build pmc package
                if os.path.isfile(new_xml_filename):
                    
                    jpg_path = scielo_package_path
                    r = self.validate_packages(report, err_filename, new_xml_filename, validation_path, pmc_package_path, jpg_path, name, new_name)

        return r

    def validate_packages(self, report, err_filename, xml_filename, validation_path, pmc_path, jpg_path, name, new_name):
        r = False
        
        scielo_html_validation_report = validation_path + '/' + name + self.scielo_html_validation_report_ext
        scielo_html_preview = validation_path + '/' + name + self.scielo_html_preview_ext
        pmc_html_validation_report = validation_path + '/' + name + self.pmc_html_validation_report_ext
        pmc_html_preview = validation_path + '/' + name + self.pmc_html_preview_ext
        
        pmc_xml_local = validation_path + '/' + name + '.local.xml'
        pmc_xml_filename = pmc_path + '/' + new_name + '.xml'

        scielo_package_path = os.path.dirname(xml_filename)

        ctrl_filename =  err_filename.replace('.err.txt', '.ctrl')

        if not os.path.exists(validation_path):
            os.makedirs(validation_path)
        for f in [scielo_html_validation_report, scielo_html_preview, pmc_html_validation_report, pmc_html_preview]:
            if os.path.isfile(f):
                os.unlink(f)
        
        if not os.path.isdir(pmc_path):
            os.makedirs(pmc_path)
        for f in os.listdir(pmc_path):
            if os.path.isfile(pmc_path + '/' + f):
                if f.startswith(new_name):
                    os.unlink(pmc_path + '/' + f)


        report.write('\nProcess ' + xml_filename, True, False, True)
        self.validator_scielo.set_output_filenames(xml_filename, validation_path, scielo_html_validation_report, scielo_html_preview, pmc_xml_local)
        if name != new_name:
            xsl_param_newname = new_name
        else:
            xsl_param_newname = ''

        
        if self.validator_scielo.validate(report, jpg_path, xsl_param_newname):
            # generate pmc package
            self.validator_pmc.set_output_filenames(pmc_xml_local, validation_path, pmc_html_validation_report, pmc_html_preview, pmc_xml_filename)         
            
            if self.validator_pmc.validate(report, jpg_path):
                if os.path.exists(pmc_xml_filename):
                    shutil.copyfile(pmc_xml_local, ctrl_filename)
            
                    report.write('Created ' + pmc_xml_filename + '\n', True, False, True)
                    for f in os.listdir(scielo_package_path):
                        if f.startswith(new_name) and not f.endswith('.xml') and not f.endswith('.jpg'):
                            shutil.copyfile(scielo_package_path + '/' + f, pmc_path + '/' + f)
                    r = True
                    if os.path.exists(pmc_xml_local):
                        os.unlink(pmc_xml_local)
                    
            else:
                shutil.move(self.validator_pmc.err_filename, err_filename)
                report.write('Unable to validate ' + pmc_xml_filename + '\n', True, False, True)
        else:
            shutil.move(self.validator_scielo.err_filename, err_filename)
            report.write('Unable to validate ' + xml_filename + '\n', True, False, True)

        if os.path.exists(err_filename):
            shutil.copyfile(err_filename, ctrl_filename)
        else:
            shutil.copyfile(pmc_xml_filename, ctrl_filename)
        return r   