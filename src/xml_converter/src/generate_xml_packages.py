import os, sys, shutil
import xml_toolbox as xml_toolbox

from reuse.input_output.parameters import Parameters 

from reuse.xml.xml_tree.xml_tree import XMLTree
from reuse.encoding.table_entities import TableEntities

from reuse.input_output.parameters import get_script_path as get_script_path
from reuse.input_output.report import Report 

def prepare_work_area(self, src_paths, work_path):
    if not os.path.isdir(work_path):
        os.makedirs(work_path)
    for path in src_paths:
        for f in os.listdir(path):
            shutil.copyfile(path + '/' + f, work_path + '/' + f)



# para markup somente o nome completo do .sgm.xml

# para cmd line e xml_convert
# src_xml_path or xml_filename
# pmc_package_path
# scielo_package_path
# validation_path


# src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, pmc_packge_path, validation_path, pdf_path
# validation_path, scielo_html_validation_report_ext, scielo_html_preview_ext, pmc_html_validation_report_ext, pmc_html_preview_ext



doit = False
sys.argv = [ arg.replace('\\', '/') for arg in sys.argv ]
if len(sys.argv) == 2:
    if sys.argv[1].endswith('.sgm.xml'):
        doit = True
        # from markup
        #acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path
        # pmc
        # pmc/pmc_work
        # pmc/pmc_work/file

        xml_filename = sys.argv[1]

        err_filename = xml_filename.replace('.sgm.xml', '.err.txt')
        
        print(err_filename)
        file_path = os.path.dirname(xml_filename)
        print(file_path)
        pmc_work_path = os.path.dirname(file_path)
        print(pmc_work_path)
        pmc_path = os.path.dirname(pmc_work_path)
        print(pmc_path)
        issue_path = os.path.dirname(pmc_path)
        print(issue_path)
        acron_path = os.path.dirname(issue_path)
        print(acron_path)
        acron = os.path.basename(acron_path)
        print(acron)
        alternative_id = ''
        validation_path = file_path

        scielo_package_path = pmc_path + '/xml_package'
        pmc_package_path = pmc_path + '/pmc_package' 


        src_path = pmc_path + '/src'
        if not os.path.isdir(src_path):
            src_path = pmc_path + '/pmc_src'
        
        if not os.path.isdir(src_path):
            os.makedirs(src_path)

        shutil.copy(xml_filename, src_path )
        name = os.path.basename(xml_filename).replace('.sgm.xml', '')
        
        xml_filename = src_path + '/' + os.path.basename(xml_filename)
        ctrl = ''
        
elif len(sys.argv) == 6:
    
    x = sys.argv[1]
    
    
    if os.path.isdir(x):
        doit = True
        xml_path = x
        xml_filename = ''
        ign, ign2, scielo_package_path, pmc_package_path, validation_path, acron = sys.argv
    elif os.path.isfile(x) and x.endswith('.xml'):
        doit = True
        xml_filename = x
        err_filename = xml_filename.replace('.xml', '.err.txt')
        ctrl = xml_filename.replace('.xml', '.ctrl')
        alternative_id = os.path.basename(xml_filename).replace('.xml', '')
        ign, ign2, scielo_package_path, pmc_package_path, validation_path, acron = sys.argv
    else:
        print('INvalid ' + x)
else:
    print('Usage:')
    print('python generate_xml_packages.py xml_file_or_src_xml_path scielo_path pmc_path report_path acronym')
    print('or')
    print('python generate_xml_packages.py sgm_xml_filename')

if doit:
    script = sys.argv[0]            

    current_path = get_script_path(script) 

    pmc_path = current_path + '/../pmc'
    if not os.path.exists(pmc_path):
        pmc_path = current_path + '/../../pmc'

    jar_path = current_path + '/../jar'
    if not os.path.exists(jar_path):
        jar_path = current_path+ '/../../jar'

    report = Report(validation_path + '/report.log', validation_path + '/report.err.txt', validation_path + '/report.txt')
    xml_toolbox.xml_tree = XMLTree(TableEntities(current_path + '/reuse/encoding/entities'))
    xml_packer = xml_toolbox.XMLPacker(pmc_path, jar_path)

    
    if len(xml_filename) > 0:
        print( 'xml_filename: ' + xml_filename)
        #xml_packer.generate_one_file(src_xml_path, src_paths_and_exts, src_img_path, scielo_package_path, report, acron, xml_filename, pmc_package_path, validation_path)
        
        #alternative_id = os.path.basename(xml_filename).replace('.xml', '')
        xml_packer.generate(xml_filename, err_filename, acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path)
        if os.path.exists(err_filename):
            print('ERRO:' + err_filename)
        if len(ctrl)>0:
            if os.path.isfile(ctrl):
                os.unlink(ctrl)

    else: 
        for f in os.listdir(xml_path):
            if f.endswith('.xml') and not f.endswith('.sgm.xml'):
                alternative_id = f.replace('.xml', '')
                err_filename = validation_path + '/' + alternative_id + '.err.txt'
                xml_packer.generate(xml_path + '/' + f, err_filename, acron, alternative_id, report, validation_path, scielo_package_path, pmc_package_path)
                
                ctrl = err_filename.replace('.err.txt', '.ctrl')
                if os.path.isfile(ctrl):
                    os.unlink(ctrl)
    


