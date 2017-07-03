# coding=utf-8
import os
import sys
import shutil

from modules.config import config
from modules.ws import institutions_service
from modules.ws import institutions_manager


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
configuration_filename = CURRENT_PATH + '/../scielo_paths.ini'

text = None
filename = None
ctrl_filename = None

if len(sys.argv) == 4:
    ign, filename, ctrl_filename, text = sys.argv
    if os.path.isfile(filename):
        os.unlink(filename)
    if os.path.isfile(ctrl_filename):
        os.unlink(ctrl_filename)

    if not isinstance(text, unicode):
        text = text.decode('cp1252')

    configuration = config.Configuration(configuration_filename)
    app_institutions_manager = institutions_manager.InstitutionsManager(configuration.app_ws_requester)
    normaff_result = institutions_service.normaff_search(app_institutions_manager, text)
    open(filename, 'w').write(institutions_service.unicode2cp1252(normaff_result) + '\n')
    if os.path.isfile(filename):
        shutil.copyfile(filename, ctrl_filename)
    else:
        open(ctrl_filename, 'w').write('fim1')
else:
    open(ctrl_filename, 'w').write('fim')
    print('invalid parameters')
