import os
import sys
import shutil

from modules import affiliations_services


if affiliations_services.organizations_manager is None:
    affiliations_services.organizations_manager = affiliations_services.OrgManager()
    affiliations_services.organizations_manager.load()

text = None
filename = None
ctrl_filename = None

if len(sys.argv) == 4:
    ign, filename, ctrl_filename, text = sys.argv
    if os.path.isfile(filename):
        os.unlink(filename)
    if os.path.isfile(ctrl_filename):
        os.unlink(ctrl_filename)
    normaff_result = affiliations_services.normaff_search(text)
    open(filename, 'w').write(affiliations_services.unicode2cp1252(normaff_result) + '\n')
    if os.path.isfile(filename):
        shutil.copyfile(filename, ctrl_filename)
    else:
        open(ctrl_filename, 'w').write('fim1')
else:
    open(ctrl_filename, 'w').write('fim')
    print('invalid parameters')
