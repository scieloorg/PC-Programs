from PMCXML import PMCXML

xml_filename = '/Users/robertatakenaka/Documents/vm_dados/dados_pmc/anp/v69n6/pmc/pmc_package/0004-282X-anp-69-859.xml'

pmcxml = PMCXML(xml_filename, 0)

print pmcxml.return_lang()
print pmcxml.return_authors()