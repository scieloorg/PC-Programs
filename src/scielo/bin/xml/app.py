
import sys

from app_modules.__init__ import appcaller
from app_modules.generics import system


def execute(parameters):
    appcaller.execute(
        [system.format_command('python app.py', parameters)])


if __name__ == '__main__':
    argv = sys.argv[1:]
    if sys.argv[1] == 'install':
        from app_modules.__init__ import REQUIREMENTS_FILE
        from app_modules.__init__ import REQUIREMENTS_CHECKER
        appcaller.install(REQUIREMENTS_FILE, REQUIREMENTS_CHECKER)
    elif sys.argv[1] == 'xml_converter.py':
        from app_modules.app import xc
        xc.call_make_packages(argv, '1.1')
    elif sys.argv[1] == 'xml_package_maker.py':
        from app_modules.app import xpm
        xpm.call_make_packages(argv, '1.1')
    else:
        print('unknown action')
        print(sys.argv)
        print('do nothing')
