import os, sys
import xml_toolbox as xml_toolbox


from reuse.input_output.report import Report 

class XMLPacker:
    def __init__(self, path_pmc, path_jar, xml_tree):


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

        xml_toolbox.xml_tree = xml_tree

        xml_toolbox.xml_java.jar_transform = path_jar + '/jar/saxonb9-1-0-8j/saxon9.jar' 
        xml_toolbox.xml_java.jar_validate = path_jar + '/jar/XMLCheck.jar'

        validator_scielo = xml_toolbox.Validator(dtd, xsl_prep_report, xsl_report, xsl_preview, xsl_output)
        validator_pmc = xml_toolbox.Validator(dtd, pmc_xsl_prep_report, pmc_xsl_report, pmc_xsl_preview, pmc_xsl_output)

        xml_toolbox.report = Report(reports_path + '/report.log', reports_path + '/report.err', reports_path + '/report.txt')

        self.scielo_package = xml_toolbox.SciELOPackage(xml_toolbox.SGML2XML(xsl_sgml2xml))
        self.pmc_package = xml_toolbox.PMCPackage(validator_pmc, validator_scielo)

    def generate_one_file(self, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, acron, xml_filename, pmc_package_path, reports_path):    
        self.scielo_package.set_parameters(xml_toolbox.report, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path)

        self.scielo_package.do_for_one(acron, xml_filename)
        self.pmc_package.do_for_one(self.scielo_package.package_path + '/' + self.scielo_package.new_name + '.xml', pmc_package_path, reports_path)

    def generate_one_folder(self, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, acron, pmc_package_path, reports_path):
        self.scielo_package.set_parameters(xml_toolbox.report, src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path)
        self.scielo_package.do_for_all(acron)
        self.pmc_package.do_for_all(self.scielo_package_path, pmc_package_path, reports_path)

