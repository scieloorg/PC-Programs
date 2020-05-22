# coding=utf-8
import os
import sys
import shutil

from ..app.config import config
from ..app.ws import institutions_service
from ..app.ws import institutions_manager
from ..generics import fs_utils
from ..generics import encoding

from ..__init__ import BIN_PATH


configuration_filename = BIN_PATH + '/scielo_paths.ini'

text = None
filename = None
ctrl_filename = None
if len(sys.argv) == 4:
    ign, filename, ctrl_filename, text = encoding.fix_args(sys.argv)
    if os.path.isfile(filename):
        os.unlink(filename)
    if os.path.isfile(ctrl_filename):
        os.unlink(ctrl_filename)

    if not isinstance(text, unicode):
        text = text.decode('cp1252')

    configuration = config.Configuration(configuration_filename)
    app_institutions_manager = institutions_manager.InstitutionsManager(configuration.app_ws_requester)
    normaff_result = institutions_service.normaff_search(app_institutions_manager, text)
    fs_utils.write_file(filename, '\n'.join(normaff_result) + '\n', 'cp1252')
    if os.path.isfile(filename):
        shutil.copyfile(filename, ctrl_filename)
    else:
        open(ctrl_filename, 'w').write('fim1')
else:
    open(ctrl_filename, 'w').write('fim')
    print('invalid parameters')
