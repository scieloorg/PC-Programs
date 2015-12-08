# coding=utf-8
import sys

from modules import institutions_service


text = None
filename = None
ctrl_filename = None

if len(sys.argv) == 7:
    ign, orgname, norgname, country_name, country_code, state, city = [item.decode(encoding=sys.getfilesystemencoding()) for item in sys.argv]
    print([orgname, norgname, country_name, country_code, state, city])
    org_manager = institutions_service.OrgManager()

    if orgname == '':
        orgname = None
    if norgname == '':
        norgname = None
    if country_name == '':
        country_name = None
    if country_code == '':
        country_code = None
    if state == '':
        state = None
    if city == '':
        city = None

    normaff_result = institutions_service.validate_organization(orgname, norgname, country_name, country_code, state, city)
    print(normaff_result)
    normaff_result = institutions_service.normaff_search('|'.join([item if item is not None else '' for item in [orgname, country_name]]))
    print(normaff_result)
else:
    print('python normaff_checker.py orgname norgname country_name country_code state city')
