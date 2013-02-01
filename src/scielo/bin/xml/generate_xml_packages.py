import os, sys
import xml_toolbox as xml_toolbox

from reuse.input_output.parameters import Parameters 

from reuse.xml.xml_tree.xml_tree import XMLTree
from reuse.encoding.table_entities import TableEntities

from reuse.input_output.parameters import get_script_path as get_script_path
from reuse.input_output.report import Report 



# para markup somente o nome completo do .sgm.xml

# para cmd line e xml_convert
# xml_path or xml_filename
# pmc_package_path
# scielo_package_path
# reports_path


# xml_path, src_paths_and_exts, src_img_path, scielo_package_path, pmc_packge_path, reports_path, pdf_path
# reports_path, scielo_html_validation_report_ext, scielo_html_preview_ext, pmc_html_validation_report_ext, pmc_html_preview_ext

param_list = [ arg.replace('\\', '/') for arg in sys.argv  ]

xml_path = ''
xml_filename = ''
acron = ''
scielo_package_path = ''
pmc_package_path = ''
reports_path = ''

required = ['', 'xml_path or xml_filename', 'scielo_package_path', 'pmc_package_path', 'reports_path' ] 

is_valid_first_param = False
is_valid_paths = False
err_msg = []

if len(param_list) > 0:
    
    if os.path.isfile(param_list[1]):
        if param_list[1].endswith('.xml'):
            # xml file
            xml_filename = param_list[1]
            xml_path = os.path.dirname(xml_filename)
            is_valid_first_param = True


            if xml_filename.endswith('.sgm.xml'):
                required = [ '', '.sgm.xml file', ]
                src_img_path = xml_path + '/../../pmc_img'
                scielo_package_path = xml_path + '/../../xml_package'
                pmc_package_path = xml_path + '/../../pmc_package'
                
                pdf_path = xml_path + '/../../pmc_pdf'
                src_paths_and_exts = [(pdf_path, '.pdf')]
                reports_path = xml_path
                is_valid_paths = True 
        else:
            is_valid_first_param = False
            err_msg.append( xml_filename + ' is not a XML file.' )

    elif os.path.isdir(param_list[1]):
        # xml path
        xml_files = [ f for f in os.listdir(param_list[1]) if f.endswith('.xml') ]
        if len(xml_files) > 0:
            xml_path = param_list[1]
            is_valid_first_param = True

        else:
            err_msg.append(param_list[1] + ' has no XML files. ')
    else:
        err_msg.append(param_list[1] + ' is not file and is not folder')
if is_valid_first_param:
    parameters = Parameters(required)
    if parameters.check_parameters(param_list):
        if len(pmc_package_path) == 0 and len(scielo_package_path) == 0 and len(reports_path) == 0:
            script, ign, scielo_package_path, pmc_package_path, reports_path = param_list
            paths = [ scielo_package_path, pmc_package_path, xml_path, reports_path] 

            src_img_path = xml_path
            src_paths_and_exts = [(xml_path, '.pdf')]
            repete = []
            for item in paths:
                if item in repete:
                    break
                else:
                    repete.append(item)
            if len(repete) != len(paths):
                err_msg.append( ', '.join(paths) + ' can not be the same. Choose different folder to them.')
            else: 
                is_valid_paths = True 
    else:
        print('?')

if is_valid_paths:
    script = param_list[0]            

    current_path = get_script_path(script) 
    path_xsl = current_path + '/../pmc/v3.0/xsl'

    dtd = current_path + '/../pmc/v3.0/dtd/journalpublishing3.dtd' 
    css = current_path + '/../pmc/v3.0/xsl/web/xml.css'
    

    xsl_sgml2xml = path_xsl + '/sgml2xml/sgml2xml.xsl'
    
    xsl_prep_report = path_xsl + '/scielo-style/stylechecker.xsl'
    xsl_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
    xsl_preview = path_xsl + '/previewer/preview.xsl'
    xsl_output = path_xsl + '/sgml2xml/xml2pmc.xsl'
   
    #pmc_xsl_prep_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
    #pmc_xsl_report = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
    pmc_xsl_prep_report = path_xsl + '/nlm-style-4.6.6/nlm-stylechecker.xsl'
    pmc_xsl_report = path_xsl + '/nlm-style-4.6.6/style-reporter.xsl'
    pmc_xsl_preview = [ path_xsl + '/jpub/citations-prep/jpub3-PMCcit.xsl', path_xsl + '/previewer/jpub-main-jpub3-html.xsl', ]
    pmc_xsl_output = path_xsl + '/sgml2xml/pmc.xsl'
    pmc_css = current_path + '/../pmc/v3.0/xsl/jpub/jpub-preview.css'
    
    xml_toolbox.xml_tree = XMLTree(TableEntities(current_path + '/reuse/encoding/entities'))

    xml_toolbox.xml_java.jar_transform = current_path  + '/../jar/saxonb9-1-0-8j/saxon9.jar' 
    xml_toolbox.xml_java.jar_validate = current_path + '/../jar/XMLCheck.jar'
    
    xml_toolbox.report = Report(reports_path + '/report.log', reports_path + '/report.err', reports_path + '/report.txt')

    validator_scielo = xml_toolbox.Validator(dtd, xsl_prep_report, xsl_report, xsl_preview, xsl_output, xml_toolbox.report, src_img_path, css)
    validator_pmc = xml_toolbox.Validator(dtd, pmc_xsl_prep_report, pmc_xsl_report, pmc_xsl_preview, pmc_xsl_output, xml_toolbox.report, src_img_path, pmc_css)

    scielo_package = xml_toolbox.SciELOPackage(xml_toolbox.SGML2XML(xsl_sgml2xml), xml_toolbox.report, xml_path, src_paths_and_exts, src_img_path, scielo_package_path)
    pmc_package = xml_toolbox.PMCPackage(validator_pmc, validator_scielo)


    if len(xml_filename) > 0:
        xml_toolbox.report.write('Generating PMC files to ' + xml_filename, True, False, True)
        scielo_package.do_for_one(acron, xml_filename)

        pmc_package.do_for_one(scielo_package.package_path + '/' + scielo_package.new_name + '.xml', pmc_package_path, reports_path)

    else:
        scielo_package.do_for_all(acron)
        pmc_package.do_for_all(scielo_package_path, pmc_package_path, reports_path)

    print('Summarized report: '+ reports_path + '/report.txt')
    print('Detailed report: '+ reports_path + '/report.log')
    print('Errors report: '+ reports_path + '/report.err')

else:
    print('\n'.join(err_msg))
