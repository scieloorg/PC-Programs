
import shutil
import os
import sys
import tempfile
import reuse.xml.xml_java as xml_java

css = ''
css_pmc = ''


xsl_sgml2xml = ''

xsl_xml2pmc = ''

xsl_pmc = ''

xsl_err = ''
xsl_report = ''
xsl_preview = ''

xsl_pmc_err = ''
xsl_pmc_report = ''
xsl_pmc_preview = ''


xsl_prepare_citations = ''

valid_extensions = [ '.tiff', '.eps', '.tif' ]
outputs_extensions = [ '.local.xml', '.rep.xml', '.rep.html', '.xml.html', '.xml', '.scielo.xml', '.sgm.xml.res.tmp', '.sgm.xml.err.tmp']


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


class XMLSciELO:
    def __init__(self, xml_filename, output_path, dtd, report, img_path):
        self.scielo_xml_filename = xml_filename
        self.report = report
        self.dtd = dtd 
        self.img_path = img_path
        self.output_path = output_path


    def output_files(self):
        self.xml_path = os.path.dirname(self.scielo_xml_filename)
        self.basename = os.path.basename(self.scielo_xml_filename)
        self.name = self.basename.replace('.xml', '')
        
        #self.parent_path = os.path.dirname(self.xml_path) 
        self.parent_path = self.xml_path
        self.pmc_package_path = self.output_path
        self.work_path = self.xml_path + '/work'

        
        prepare_path(self.work_path, self.name)
        prepare_path(self.pmc_package_path, self.name)

        print(self.work_path)
        print(self.pmc_package_path)
        # XML        
        self.xml_pmc_local = self.work_path + '/' + self.name + '.pmc.tmp.xml'
        
        self.xml_report = self.work_path + '/' + self.name + '.rep.xml'
        self.html_preview = self.work_path + '/' + self.name + '.scielo.preview.html'
        self.html_report = self.work_path + '/' + self.name + '.scielo.validation.report.html'
        

        
        self.pmc_xml_report = self.work_path + '/' + self.name + '.pmc.rep.xml'
        
        self.pmc_html_preview = self.work_path + '/' + self.name + '.pmc.preview.html'
        self.pmc_html_report = self.work_path + '/' + self.name + '.pmc.validation.report.html'
        
        self.xml_pmc = self.pmc_package_path + '/' + self.name + '.xml'
        
        self.xml_pmc_citations = self.work_path + '/' + self.name + '.cit.xml'

        # error and result files
        self.result_filename = self.scielo_xml_filename + '.res.tmp'
        self.err_filename = self.scielo_xml_filename + '.err.tmp'        
        
        
    
    def validate(self, xml, use_dtd):
        return xml_java.validate(xml, use_dtd, self.result_filename, self.err_filename)
        
    def transform(self, xml, xsl, result, parameters = {}):
        return xml_java.transform(xml, xsl, result, self.err_filename, parameters)
        
    def validate_and_transform(self, xml, xsl, result, validate_dtd):
        r = False
        if self.validate(xml, validate_dtd):
            r = self.transform(xml, xsl, result)
        return r

    def generate_xml(self):  
        
        self.report.write('output_files')
        self.output_files()
        
        print('\nXML for SciELO: ' + self.scielo_xml_filename)

        xml_java.replace_dtd_path(self.scielo_xml_filename, self.dtd)
        
        if self.validate(self.scielo_xml_filename, self.dtd):                
            self.report.write('transform ' + self.scielo_xml_filename + ' '+  xsl_err + ' '+  self.xml_report)
            if self.transform(self.scielo_xml_filename, xsl_err, self.xml_report):
                # Generate self.report.html
                self.report.write('transform ' + self.xml_report + ' '+  xsl_report + ' '+  self.html_report)
                if self.transform(self.xml_report, xsl_report, self.html_report):
                    self.report.write('done')
                    print('  XML for SciELO: Validation report: ' + self.html_report)
                
            self.report.write('transform ' + self.scielo_xml_filename + ' '+  xsl_preview + ' '+  self.html_preview )
            if self.transform(self.scielo_xml_filename, xsl_preview, self.html_preview, {'path_img': self.img_path +'/', 'css':css}):
                # Generate xml (final version)
                self.report.write('done')
                print('  XML for SciELO: Preview: ' + self.html_preview)
            
            self.report.write('transform ' + self.scielo_xml_filename + ' '+  xsl_xml2pmc + ' '+  self.xml_pmc_local)
            if self.transform(self.scielo_xml_filename, xsl_xml2pmc, self.xml_pmc_local):
                xml_java.replace_dtd_path(self.xml_pmc_local, self.dtd)
                if self.transform(self.xml_pmc_local, xsl_pmc, self.xml_pmc):
                    if self.validate(self.xml_pmc, self.dtd): 
                        print('  XML for PMC: ' + self.xml_pmc)

                        self.report.write('Generated xml pmc final')
                
                        if self.transform(self.xml_pmc_local, xsl_pmc_err, self.pmc_xml_report):
                            # Generate self.report.html
                            self.report.write('transform ' + self.pmc_xml_report + ' '+  xsl_pmc_report + ' '+  self.pmc_html_report)
                            if self.transform(self.xml_report, xsl_pmc_report, self.pmc_html_report):
                                self.report.write('done')
                                print('  XML for PMC: Validation report: ' + self.pmc_html_report)
                        
                        self.report.write('transform ' + self.xml_pmc_local + ' '+  xsl_prepare_citations + ' '+  self.xml_pmc_citations )
                        if self.transform(self.xml_pmc_local, xsl_prepare_citations, self.xml_pmc_citations):
                            xml_java.replace_dtd_path(self.xml_pmc_citations, self.dtd)
                            self.report.write('transform ' + self.xml_pmc_citations + ' '+  xsl_pmc_preview + ' '+  self.pmc_html_preview )
                            if self.transform(self.xml_pmc_citations, xsl_pmc_preview, self.pmc_html_preview, {'path_img': self.img_path +'/', 'css':css_pmc}):
                                print('  XML for PMC: Preview: ' + self.pmc_html_preview)
                
        if os.path.exists(self.xml_pmc):
            self.report.write('END - OK')
            
        else:
            self.report.write('END - ERROR')
            if not os.path.exists(self.err_filename):
                f = open(self.err_filename, 'w')
                f.write('error')
                f.close()
            



class PMCXMLGenerator:
    def __init__(self, dtd, report):
        self.dtd = dtd
        self.report = report

    def generate_xml_files(self, xml_path, img_path, output_path):
        for xml_file in os.listdir(xml_path):
            if xml_file.endswith('.xml'):
                xml_scielo = XMLSciELO(xml_path +'/' + xml_file, output_path, self.dtd, self.report, img_path)
                xml_scielo.generate_xml()

        


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