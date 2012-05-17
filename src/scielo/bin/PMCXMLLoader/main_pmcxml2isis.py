from pmcxml_loader import PMCXML_loader

#xml_filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/0004-282X-anp-69-859.xml'
path = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/'

pmcxml_loader = PMCXML_loader()
pmcxml_loader.load_xml_files(path, 'teste.id')

