
import shutil
import os
import sys
import tempfile
import reuse.xml.xml_java as xml_java
import random


xml_tree = None
report = None


class EntitiesTable:
    def __init__(self, filename = 'entities'):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        self.table_number2char = {}
        self.table_named2char = {}

        for line in lines:
            values = line.replace("\n", "").split('|')
            if len(values) != 5:
                print(line)
            else:
                char, number_ent, named_ent, ign2, no_accent = values
                
                if self.is_valid_char(char) and self.is_valid_named(named_ent):
                    #entity_char = named_ent.replace('&','').replace(';','')
                    if not number_ent in self.table_number2char.keys():
                        self.table_number2char[number_ent] = char
                    if not named_ent in self.table_named2char.keys():
                        self.table_number2char[named_ent] = char

        
                    
    def is_valid_char(self, char):
        r = False
        if char != '':
            if not char in [ '>', '<', '&']:
                r = True
        return  r

    def is_valid_named(self, named):
        r = False
        if named != '':
            if not named in [ '&gt;', '&lt;', '&amp;']:
                r = True
        return  r

    
    def ent2chr(self, ent):
        r = ent
        if ent in self.table_number2char.keys():
            r = self.table_number2char[ent]
        elif ent in self.table_named2char.keys():
            r = self.table_named2char[ent]
        return r
    #def find_number_entities(self, content):
    #    l = []
    #    if '&#' in content and ';' in content:
    #        p = content.find('&#')
    #        ent = content[p:]
    #        ent = ent[0:ent.find(';')+1]
    #        if ent in self.table_number2char.keys():
    #            l.append(ent)
    #    return l
        
    #def chr2ent(self, content):

    #    for k,v in self.table_char2number.items():
    #        content = content.replace(k, v)
    #    return content

    #def ent2chr(self, content):
    #    entities = self.find_number_entities(content)
    #    for ent in entities:
    #        content = content.replace(ent, self.table_number2char[ent])
    #    return content
    





entities_table = EntitiesTable(os.path.dirname(os.path.realpath(__file__)) + '/reuse/encoding/entities')


def handle_entities(content):
    import HTMLParser
    h = HTMLParser.HTMLParser()
    try:
        content = h.unescape(content)
    except:
        print('Unable to use h.unescape')
        pass 


    if '&' in content:
        PREFIX_ENT = '#PREFIX_ENT#'
        while '&' in content:

            ent = content[content.find('&'):]
            ent = ent[0:ent.find(';')+1]

            char = entities_table.ent2chr(ent)
            if char == ent:
                content = content.replace(ent, ent.replace('&',  PREFIX_ENT))
                f = open('unknown_ent.txt', 'a+')
                f.write( char + '|' + ent + '|'  + ent + '||' + '\n')
                f.close()
            else:
                content = content.replace(ent, char)
            
        content = content.replace(PREFIX_ENT, '&')        

        

    return content



def filename_matches(f, name):
    return f.startswith(name + '.') or f.startswith(name + '-')

def delete(filename):
    try:
        os.unlink(filename)
    except WindowsError,e:
        pass

   
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
            if filename_matches(file, startswith):
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
        

    def data_from_sgml(self):
        nodes = xml_tree.return_nodes()
        r = None
        if len(nodes) > 0:
            order = nodes[0].attrib['order']
            fpage = nodes[0].attrib['fpage']
            suppl = ''
            issueno = ''
            volid = ''
            issn = ''
            if 'issn' in nodes[0].attrib.keys():
                issn = nodes[0].attrib['issn']
            if 'volid' in nodes[0].attrib.keys():
                volid = nodes[0].attrib['volid']
            if 'issueno' in nodes[0].attrib.keys():
                issueno = nodes[0].attrib['issueno']
            if 'supplvol' in nodes[0].attrib.keys():
                suppl = nodes[0].attrib['supplvol']
            if 'supplno' in nodes[0].attrib.keys():
                suppl = nodes[0].attrib['supplno']
            if suppl == '0':
                suppl = 'suppl'
            r = (issn, volid, issueno, suppl, fpage, order)
        return r

    def data_from_xml(self):
        nodes = xml_tree.return_nodes()
        r = None

        if len(nodes) > 0:
            article_meta_node = xml_tree.return_nodes('.//article-meta', nodes[0])

            issn = ''
            vol = ''
            number = ''
            suppl = ''
            fpage = ''

            node = xml_tree.return_nodes('.//front/journal-meta/issn', nodes[0])
            if len(node) > 0:
                issn = node[0].text
            if len(article_meta_node) > 0:
                print(article_meta_node)
                node = xml_tree.return_nodes('volume', article_meta_node[0])
                if len(node) > 0:
                    vol = node[0].text
            
                node = xml_tree.return_nodes('issue', article_meta_node[0])
                if len(node) > 0:
                    issue = node[0].text.lower()
            

                node = xml_tree.return_nodes('supplement', article_meta_node[0])
                if len(node) > 0:
                    suppl = node[0].text
            

                node = xml_tree.return_nodes('fpage', article_meta_node[0])
                if len(node) > 0:
                    fpage = node[0].text

                
                if 'suppl' in issue:
                    if issue == 'suppl':
                        suppl = 'suppl'
                    else:
                        number, suppl = issue.split('suppl')
                        number = number.replace(' ', '')
                        suppl = suppl.replace(' ', '')

                        if suppl == '':
                            suppl = 'suppl'
                else:
                    number = issue
            
                    
            r = (issn, vol, number, suppl, fpage, '')        
        
        return r

    def format_data(self, data, param_acron = '', param_order = ''):
        r = ''
        if data != None:
            issn, vol, issueno, suppl, fpage, order = data

            if order == '':
                order = param_order

            order = '00000' + order
            order = order[-5:]   

            fpage = '00000' + fpage
            fpage = fpage[-5:]

            if fpage == '00000':
                page_or_order ='e' + order
            else:
                page_or_order = fpage     

            if issueno == 'ahead':
               issueno = '00'

            issueno = '00' + issueno
            issueno = issueno[-2:] 

            if suppl == 'suppl':
                issueno += '-' + suppl
            elif suppl != '':
                issueno += '-' + 's' + suppl
            
            if len(param_acron) > 0:
                param_acron = '-' + param_acron
            if len(vol) > 0:
                vol = '-' + vol 
            if len(issueno) > 0:
                issueno = '-' + issueno 
            
            
            r = issn +  param_acron  + vol + issueno + '-' + page_or_order
        return r



    def xml_data_image_names(self):
        test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href'] 
        root = xml_tree.return_nodes()
        r = []
        if type(root) == type([]):
            nodes = []
            if len(root) > 0:                    
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
            data = self.data_from_sgml()
            new_name = self.format_data(data, acron)

        else:
            data = self.data_from_xml()
            new_name = self.format_data(data, acron, alternative_id)
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
                    
                    if filename_matches(f, self.name) and not self.basename == f:
                        
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

            if ':' in img_path:
                img_path = 'file:///' + img_path 
            if type(self.xsl_preview) == type([]):
                xml_java.tranform_in_steps(self.xml_filename, self.dtd, self.xsl_preview, self.html_preview, {'path_img': img_path +'/', 'css':  self.css, 'new_name': new_name})
            else:
                report.write('transform ' + self.xml_filename + ' '+  self.xsl_preview + ' '+  self.html_preview )
                xml_java.transform(self.xml_filename, self.xsl_preview, self.html_preview, self.err_filename, {'path_img': img_path +'/', 'css':  self.css, 'new_name': new_name})
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

    def validate_xml_and_style(self, report):          
        is_valid_xml = False
        
        import time

        xml_java.replace_dtd_path(self.xml_filename, self.dtd)        
        if xml_java.validate(self.xml_filename, self.dtd, self.result_filename, self.err_filename):  
            is_valid_xml = True    

            report.write('Transform ' + self.xml_filename + ' + ' + self.xsl_prep_report +  ' => ' + self.xml_report + ' ' + self.err_filename)        
            t = time.time()
            report.write(str(os.path.exists(self.xml_filename)))        
            report.write(str(os.path.exists(self.xsl_prep_report))   )     
            
            if xml_java.transform(self.xml_filename, self.xsl_prep_report, self.xml_report, self.err_filename):
                t1 = time.time()
                report.write(str(t1 - t))
                report.write('Transform ' + self.xml_report + ' + ' + self.xsl_report +  ' => ' + self.html_report + ' ' + self.err_filename)        
                
                report.write(str(os.path.exists(self.xml_report)))        
                report.write(str(os.path.exists(self.xsl_report)))        
                if xml_java.transform(self.xml_report, self.xsl_report, self.html_report, self.err_filename):
                    t2 = time.time()
                    report.write(str(t2 - t1))
                else:
                    t2 = time.time()
                    report.write('Unable to generate ' + self.html_report )
                    report.write(str(t2 - t1))
            else:
                t1 = time.time()
                report.write('Unable to generate ' + self.xml_report)
                report.write(str(t1 - t))
        
        if os.path.isfile(self.result_filename):
            os.unlink(self.result_filename)

        c = ''
        if os.path.exists(self.html_report):
            f = open(self.html_report, 'r')
            c = f.read()
            f.close()
            

        return (is_valid_xml, ('Total of errors = 0' in c))

class SGML2XML:
    def __init__(self, xsl_sgml2xml):
        self.xsl_sgml2xml = xsl_sgml2xml
        
    def fix_xml_tags(self, xml_filename):
        shutil.copyfile(xml_filename, xml_filename + '.bkp')
        f = open(xml_filename, 'r')
        content = f.read()
        f.close()
        
        f = open(xml_filename, 'w')
        f.write(self.fix_tags(self.fix_open_close(content)))
        f.close()
        

    def fix_open_close(self, content):
        changes = []
        parts = content.split('>')
        for s in parts:
            if '<' in s:
                if not '</' in s and not '<!--' in s and not '<?' in s:

                    s = s[s.find('<')+1:]
                    if ' ' in s and not '=' in s:
                        test = s[s.find('<')+1:]
                        changes.append(test)
        for change in changes:
            print(change)
            content = content.replace('<' + test + '>', '[' + test + ']')
        return content


    def fix_tags(self, content):
        rcontent = content

        tags = [ 'italic', 'bold', 'sub', 'sup']
        
        tag_list = []

        for tag in tags:
            tag_list.append('<' + tag + '>')
            tag_list.append('</' + tag + '>')
        
            rcontent = rcontent.replace('<' + tag + '>',  'BREAKBEGINCONSERTA<' + tag + '>BREAKBEGINCONSERTA').replace('</' + tag + '>', 'BREAKBEGINCONSERTA</' + tag + '>BREAKBEGINCONSERTA')

        if content != rcontent:
            parts = rcontent.split('BREAKBEGINCONSERTA')
            content = self.fix_problem( tag_list, parts)
            
        return content


    def fix_problem(self, tag_list, parts):

        expected_close_tags = [] 
        ign_list = [] 
        
        k = 0
        for part in parts:
            if part in tag_list:
                tag = part 
                print('\ncurrent:' + tag)
                if tag.startswith('</'):
                    print('expected')
                    print(expected_close_tags)
                    print('ign_list')
                    print(ign_list)
                
                    if tag in ign_list:
                        print('remove from ignore')
                        ign_list.remove(tag)
                        parts[k] = ''
                    else:

                        matched = False
                        if len(expected_close_tags) > 0:
                            matched = (expected_close_tags[-1] == tag)

                            if not matched:
                                print('not matched')

                                while not matched and len(expected_close_tags) > 0:

                                    ign_list.append(expected_close_tags[-1])
                                    parts[k-1] += expected_close_tags[-1]
                                    del expected_close_tags[-1]

                                    matched = (expected_close_tags[-1] == tag)

                                print('...expected')
                                print(expected_close_tags)
                                print('...ign_list')
                                print(ign_list)

                            if matched:                            
                                del expected_close_tags[-1]
                                

                else:
                    expected_close_tags.append(tag.replace('<', '</'))
            k += 1
        
        return ''.join(parts)

    def sgmxml2xml(self, sgmxml_filename, xml_filename, err_filename, report):        
        fix_xml(sgmxml_filename)

        r = False
        temp_err_filename = sgmxml_filename.replace('.sgm.xml', '.res1')
        res_filename = sgmxml_filename.replace('.sgm.xml', '.res')

        if not xml_java.validate(sgmxml_filename, '', res_filename, temp_err_filename):
            shutil.copyfile(sgmxml_filename, sgmxml_filename.replace('.sgm.xml', '.sgm.txt'))

            self.fix_xml_tags(sgmxml_filename)
        

        if xml_java.validate(sgmxml_filename, '', res_filename, err_filename):
            r = xml_java.transform(sgmxml_filename, self.xsl_sgml2xml, xml_filename, err_filename)
        if not r:
            report.write('Unable to create ' + xml_filename + ' from ' + sgmxml_filename, True, True, True)
            report.write(err_filename, True, True, True)
        
        if os.path.isfile(temp_err_filename):
            delete(temp_err_filename)
        if os.path.isfile(res_filename):
            delete(res_filename)
        return r
        

class XMLPacker:
    def __init__(self, path_pmc, path_jar, java_path, dtd_version = 'j1.0'):

        if dtd_version == 'v3.0':
            stylechecker_version = '4.6.6'
            dtd = path_pmc + '/' + dtd_version + '/dtd/journalpublishing3.dtd' 
        else:
            stylechecker_version = '5.1'
            dtd = path_pmc + '/' + dtd_version + '/dtd/jats1.0/JATS-journalpublishing1.dtd' 

        path_xsl = path_pmc + '/' + dtd_version + '/xsl'

        
        self.css = path_pmc + '/' + dtd_version + '/xsl/previewers/scielo.css'


        xsl_sgml2xml = path_xsl + '/sgml2xml/sgml2xml.xsl'

        xsl_prep_report = path_xsl + '/scielo-style/stylechecker.xsl'
        xsl_report = path_xsl + '/nlm-style-' + stylechecker_version + '/style-reporter.xsl'
        xsl_preview = path_xsl + '/previewers/scielo-html.xsl'
        xsl_output = path_xsl + '/sgml2xml/xml2pmc.xsl'

        pmc_xsl_prep_report = path_xsl + '/nlm-style-' + stylechecker_version + '/nlm-stylechecker.xsl'
        pmc_xsl_report = path_xsl + '/nlm-style-' + stylechecker_version + '/style-reporter.xsl'
        pmc_xsl_preview = [ path_xsl + '/jpub/citations-prep/jpub3-PMCcit.xsl', path_xsl + '/previewers/jpub-main-jpub3-html.xsl', ]
        pmc_xsl_output = path_xsl + '/sgml2xml/pmc.xsl'
        self.pmc_css = path_pmc + '/' + dtd_version + '/xsl/jpub/jpub-preview.css'

        #xml_toolbox.xml_tree = XMLTree(TableEntities(current_path + '/reuse/encoding/entities'))
        xml_java.java_path = java_path
        xml_java.jar_transform = path_jar + '/saxonb9-1-0-8j/saxon9.jar' 
        xml_java.jar_validate = path_jar + '/XMLCheck.jar'

        validator_scielo = Validator(dtd, xsl_prep_report, xsl_report, xsl_preview, xsl_output, self.css)
        validator_pmc = Validator(dtd, pmc_xsl_prep_report, pmc_xsl_report, pmc_xsl_preview, pmc_xsl_output, self.pmc_css)

        
        self.checker = XMLPackagesChecker(SGML2XML(xsl_sgml2xml), validator_scielo, validator_pmc)
    


    def generate(self, filename, err_filename, acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path):    
        if os.path.isfile(err_filename):
            os.unlink(err_filename)
        self.checker.process(filename, err_filename, acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path)

    


    def generate_validation_reports(self, report, xml_path, pmc_package_path, reports_path, jpg_path):
        for f in os.listdir(xml_path):
            if f.endswith('.xml'):
                err_filename = xml_path + '/' + f.replace('.xml', '.err.txt')
                xml_filename = xml_path + '/' + f
                name = f.replace('.xml', '')
                new_name = name
                self.checker.validate_packages(report, err_filename, xml_filename, reports_path, pmc_package_path, jpg_path, name, new_name)

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

    def alternative_normalize_entities(self, c):

        def prefix_ent(N=7):
            return ''.join(random.choice('^({|~_`!QZ[') for x in range(N))

        

        from reuse.encoding.entities_table import EntitiesTable

        PREFIX_ENT = prefix_ent()
        while PREFIX_ENT in c:
            PREFIX_ENT = prefix_en()

        ents = {'&gt;': PREFIX_ENT + 'gt;', '&lt;': PREFIX_ENT + 'lt;', '&amp;': PREFIX_ENT + 'amp;', }

        content = c
        for ent, new_ent in ents.items():
            content = content.replace(ent, new_ent)

        while '&' in content:
            ent = content[content.find('&'):]
            ent = ent[0:ent.find(';')+1]

            replace_by = EntitiesTable().find_character(ent)
            if replace_by != None:
                content = content.replace(ent, replace_by)
            else:
                content = content.replace(ent, ent.replace('&',  PREFIX_ENT))
                f = open('unknown_ent.txt', 'a+')
                f.write(ent+ '\n')
                f.close()

        if c != content:
            content = content.replace( PREFIX_ENT, '&')


            f = open(filename, 'w')
            f.write(content)
            f.close()

    def normalize_entities(self, filename):
        def prefix_ent(N=7):
            return ''.join(random.choice('^({|~_`!QZ[') for x in range(N))

        f = open(filename, 'rb')
        c = f.read()
        f.close()

        PREFIX_ENT = prefix_ent()
        while PREFIX_ENT in c:
            PREFIX_ENT = prefix_en()

        ents = {}
        for e in [ '&gt;', '&lt;', '&amp;']:
            ents[e] = e.replace('&', PREFIX_ENT)

        ents = {'&gt;': PREFIX_ENT + 'gt;', '&lt;': PREFIX_ENT + 'lt;', '&amp;': PREFIX_ENT + 'amp;', }

        content = c
        for ent, new_ent in ents.items():
            content = content.replace(ent, new_ent)

        content = handle_entities(content)

        for ent, new_ent in ents.items():
            content = content.replace(new_ent, ent)

        if content != c:
            print(len(content))
            f = open(filename, 'wb')
            f.write(content)
            f.close()

    

    def prepare_file(self, filename, err_filename, acron, alternative_id, report):
        new_name = ''
        xml_images_list = []
        xml_filename = ''

        r = None
        
        self.normalize_entities(filename)
        # if .sgm.xml converts it into xml
        if filename.endswith('.sgm.xml'):
            filename2 = filename.replace('.sgm.xml', '.xml')
            if self.sgmlxml.sgmxml2xml(filename, filename2, err_filename, report):
                
                xml_filename = filename2
        elif filename.endswith('.xml'):
            xml_filename = filename
            
        if xml_tree.load(filename, report):
            if xml_tree.root != [] and xml_tree.root != None:
                new_name, xml_images_list = self.find_new_name(filename, acron, alternative_id, report)
                r = (xml_filename, new_name, xml_images_list)
        return r
             
    
    def build_scielo_package(self, filename, dest_path, img_list, new_name):
        extensions = ['.jpg', '.tiff', '.tif', '.eps']
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        for f in os.listdir(dest_path):
            if filename_matches(f, new_name):
                os.unlink(dest_path + '/' + f)

        src_path = os.path.dirname(filename)
        if os.path.isdir(dest_path):
            name = os.path.basename(filename).replace('.xml', '')
            if new_name == name:
                # nao precisa renomear
                shutil.copyfile(filename, dest_path + '/' + name + '.xml')
                for f in os.listdir(src_path):
                    if filename_matches(f, name) and not f.endswith('.sgm.xml') and not f.endswith('.res') and not f.endswith('.res1'):
                        shutil.copyfile(src_path + '/' + f, dest_path + '/' + f)
            else:
                # renomear
                self.rename(filename, dest_path + '/' + new_name + '.xml', img_list, new_name)

                for f in os.listdir(src_path):
                    if filename_matches(f, name) and not f.endswith('.xml'):
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
            print(filename)
            jpg  = [ f for f in os.listdir(path) if f.endswith('.jpg')]
            if len(jpg) == 0:
                hd  = [ f for f in os.listdir(path) if f.endswith('.tiff') or f.endswith('.tif') or f.endswith('.eps')]
                if len(hd) > 0:
                    img_to_jpeg(path, path) 
            # prepare file
            name = os.path.basename(filename).replace('.sgm', '').replace('.xml', '')
            prepared = self.prepare_file(filename, err_filename, acron, alternative_id, report)
            
            if prepared == None:
                report.write('Unable to load')
            else:
                xml_filename, new_name, img_list = prepared
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
                if filename_matches(f, new_name):
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
                        if filename_matches(f, new_name) and not f.endswith('.xml') and not f.endswith('.jpg'):
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
