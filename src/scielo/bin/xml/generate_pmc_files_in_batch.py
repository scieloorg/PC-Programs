
import sys
import os

#from scielo2pmc import PMCXMLGenerator
import scielo2pmc

from reuse.input_output.parameters import Parameters 


from reuse.input_output.report import Report 


required_parameters = ['', 'xml scielo path', 'output path', 'jpg images path'  ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    #ign, java_path, jar_validator, xsl_path, xml_path, output_path, err_filename = sys.argv
    script, xml_path, output_path, img_path = sys.argv

    
    # configuration
    

    if '/' in script:
        current_path = os.path.dirname(script).replace('\\', '/')
    else:
        current_path = os.getcwd()

    path_xsl = current_path + '/../pmc/v3.0/xsl/'
    entities_filename = current_path + '/reuse/encoding/entities'


    scielo2pmc.css_pmc = path_xsl + '/jpub/jpub-preview.css'
    scielo2pmc.css = current_path + '/../pmc/v3.0/xsl/previewer/preview.css'
    scielo2pmc.xml_java.jar_transform = current_path + '/../jar/saxonb9-1-0-8j/saxon9.jar' 
    scielo2pmc.xml_java.jar_validate = current_path + '/../jar/XMLCheck.jar'
    

    
    
    scielo2pmc.xsl_sgml2xml = path_xsl + '/sgml2xml/sgml2xml.xsl'
    scielo2pmc.xsl_xml2pmc = path_xsl + '/sgml2xml/xml2pmc.xsl'
    scielo2pmc.xsl_pmc = path_xsl + '/sgml2xml/pmc.xsl'
    
    scielo2pmc.xsl_err = path_xsl + '/scielo-style/stylechecker.xsl'
    scielo2pmc.xsl_report = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
    scielo2pmc.xsl_preview = path_xsl + '/previewer/preview.xsl'
    
    scielo2pmc.xsl_pmc_err = path_xsl + '/nlm-style-4.6.6/nlm-style-reporter.xsl'
    scielo2pmc.xsl_pmc_report = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
    scielo2pmc.xsl_pmc_preview = path_xsl + '/previewer/jpub-main-jpub3-html.xsl'
    
    scielo2pmc.xsl_prepare_citations =  path_xsl + '/jpub/citations-prep/jpub3-PMCcit.xsl'

    
    
    report = Report(xml_path + '/report.log', xml_path + '/report.err', xml_path + '/report.txt')
    
    generator = scielo2pmc.PMCXMLGenerator(current_path + '/../pmc/v3.0/dtd/journalpublishing3.dtd', report)
    
    generator.generate_xml_files(xml_path, img_path, output_path)       
