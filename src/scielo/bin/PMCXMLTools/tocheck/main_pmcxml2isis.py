from pmcxml_loader import PMCXML_loader
from extra_data import ExtraData
import os

#xml_filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/0004-282X-anp-69-859.xml'
path = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/'

pmcxml_loader = PMCXML_loader()

files = os.listdir(path)
i=0
for f in files:
    if '.xml' in f:
        i = i+1

folders = path.split('/')
acron = folders[-5:][0]

control_info = ExtraData()
control_info.set_acron(acron)
control_info.set_standard('?')
control_info.set_descriptor('?')
control_info.set_dateiso('?')
control_info.set_document_count(str(i))
control_info.set_issue_status('1')
control_info.set_is_markup_done('1')

control_info.set_issue_folder_name(folders[-4:][0])

pmcxml_loader.load_xml_files(path, 'teste.id', control_info)

