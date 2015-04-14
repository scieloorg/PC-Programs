# coding=utf-8
import sys

from modules import institutions_service


text = None
filename = None
ctrl_filename = None

if len(sys.argv) == 7:
    ign, orgname, norgname, country_name, country_code, state, city = sys.argv
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

    normaff_result = institutions_service.validate_organization(org_manager, orgname, norgname, country_name, country_code, state, city)
    print(normaff_result)
else:
    print('python normaff_checker.py orgname norgname country_name country_code state city')
