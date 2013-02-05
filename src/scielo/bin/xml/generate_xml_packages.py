import os, sys
import xml_toolbox as xml_toolbox

from reuse.input_output.parameters import Parameters 

from reuse.xml.xml_tree.xml_tree import XMLTree
from reuse.encoding.table_entities import TableEntities

from reuse.input_output.parameters import get_script_path as get_script_path
from reuse.input_output.report import Report 



# para markup somente o nome completo do .sgm.xml

# para cmd line e xml_convert
# src_xml_path or xml_filename
# pmc_package_path
# scielo_package_path
# reports_path


# src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, pmc_packge_path, reports_path, pdf_path
# reports_path, scielo_html_validation_report_ext, scielo_html_preview_ext, pmc_html_validation_report_ext, pmc_html_preview_ext

param_list = [ arg.replace('\\', '/') for arg in sys.argv  ]

src_xml_path = ''
xml_filename = ''
acron = '??????'
scielo_package_path = ''
pmc_package_path = ''
reports_path = ''
src_paths_and_exts = []

required = [ '', 'src_xml_path or xml_filename', 'scielo_package_path', 'pmc_package_path', 'reports_path', 'acronym' ] 

is_valid_first_param = False
is_valid_paths = False
err_msg = []

if not len(param_list) in [2, 6]:
    print('Usage:')
    print('python generate_xml_packages.py xml_file_or_src_xml_path scielo_path pmc_path report_path acronym')

else:
    if os.path.isfile(param_list[1]):
        if param_list[1].endswith('.xml'):
            # xml file
            xml_filename = param_list[1]
            src_xml_path = os.path.dirname(xml_filename)
            is_valid_first_param = True


            if xml_filename.endswith('.sgm.xml'):
                required = [ '', '.sgm.xml file', ]
                src_img_path = src_xml_path + '/../../pmc_img'
                scielo_package_path = src_xml_path + '/../../xml_package'
                pmc_package_path = src_xml_path + '/../../pmc_package'
                
                pdf_path = src_xml_path + '/../../pmc_pdf'
                src_paths_and_exts = [(pdf_path, '.pdf')]
                
                a = xml_filename.split('/')
                acron = a[len(a)-6]
                
                reports_path = src_xml_path
                is_valid_paths = True 
        else:
            is_valid_first_param = False
            err_msg.append( xml_filename + ' is not a XML file.' )

    elif os.path.isdir(param_list[1]):
        # xml path
        xml_files = [ f for f in os.listdir(param_list[1]) if f.endswith('.xml') ]
        if len(xml_files) > 0:
            src_xml_path = param_list[1]
            is_valid_first_param = True
        else:
            err_msg.append(param_list[1] + ' has no XML files. ')
    else:
        err_msg.append(param_list[1] + ' is not file and is not folder')
        
if is_valid_first_param:
    parameters = Parameters(required)
    if parameters.check_parameters(param_list):
        if len(pmc_package_path) == 0 and len(scielo_package_path) == 0 and len(reports_path) == 0:
            script, ign, scielo_package_path, pmc_package_path, reports_path, acron = param_list
            paths = [ scielo_package_path, pmc_package_path, src_xml_path, reports_path] 

            src_img_path = src_xml_path
            src_paths_and_exts = [(src_xml_path, '.pdf')]
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
    

if is_valid_paths:
    script = param_list[0]            



    current_path = get_script_path(script) 

    pmc_path = current_path + '/../pmc'
    if not os.path.exists(pmc_path):
        pmc_path = current_path + '/../../pmc'

    jar_path = current_path + '/../jar'
    if not os.path.exists(jar_path):
        jar_path = current_path+ '/../../jar'

    report = Report(reports_path + '/report.log', reports_path + '/report.err', reports_path + '/report.txt')
    xml_toolbox.xml_tree = XMLTree(TableEntities(current_path + '/reuse/encoding/entities'))
    xml_packer = xml_toolbox.XMLPacker(pmc_path, jar_path)

    #xml_packer.generate_one_file(src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, report, acron, xml_filename, pmc_package_path, reports_path)
    #xml_packer.generate_one_folder(src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, report, acron, pmc_package_path, reports_path)

    if len(xml_filename) > 0:
        xml_packer.generate_one_file(src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, report, acron, xml_filename, pmc_package_path, reports_path)
    else: 
        xml_packer.generate_one_folder(src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, report, acron, pmc_package_path, reports_path)



    print('Summarized report: '+ reports_path + '/report.txt')
    print('Detailed report: '+ reports_path + '/report.log')
    print('Errors report: '+ reports_path + '/report.err')

else:
    print('\n'.join(err_msg))


