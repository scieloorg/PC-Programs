
import sys

from app_modules.generics import system
from app_modules.__init__ import appcaller
from app_modules.__init__ import BIN_XML_PATH


def execute(parameters):
    appcaller.execute(
        [system.format_command(
            'python {}/run_app.py'.format(BIN_XML_PATH), parameters)])


if __name__ == '__main__':
    argv = sys.argv[1:]
    if sys.argv[1] == 'install':
        from app_modules.__init__ import REQUIREMENTS_FILE
        from app_modules.__init__ import REQUIREMENTS_CHECKER
        appcaller.install(REQUIREMENTS_FILE, REQUIREMENTS_CHECKER)
    elif sys.argv[1].endswith('xml_converter.py'):
        from app_modules.app import xc
        xc.call_make_packages(argv, '1.1')
    elif sys.argv[1].endswith('xml_package_maker.py'):
        from app_modules.app import xpm
        xpm.call_make_packages(argv, '1.1')
    else:
        print('unknown command')
        print(sys.argv)
        print('do nothing')
