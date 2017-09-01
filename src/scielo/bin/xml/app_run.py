import sys

import os
from modules.app.config import app_venv


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

venv_path = '{}/venv/scielo-programs'.format(THIS_LOCATION)
requirements_path = '{}/modules/venv/'.format(THIS_LOCATION)

appvenv = app_venv.AppEnv(venv_path)


if __name__ == '__main__':
    print(sys.argv)
    argv = sys.argv[1:]
    print(argv)
    if sys.argv[1] == 'install':
        appvenv.install(requirements_path)
    elif sys.argv[1] == 'xc':
        from modules.app import xc
        xc.call_make_packages(argv, '1.1')
    elif sys.argv[1] == 'xpm':
        from modules.app import xpm
        xpm.call_make_packages(argv, '1.1')
    else:
        print('unknown action')
        print(sys.argv)
        print('do nothing')
