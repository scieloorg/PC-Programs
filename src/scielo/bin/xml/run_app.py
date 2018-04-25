import sys

from app_modules.generics import (
    encoding,
    system,
    logger,
)
from app_modules.app.config import (
    app_caller,
    config,
)
from app_modules.__init__ import (
    BIN_XML_PATH,
    LOG_PATH,
    VENV_PATH,
    REQUIREMENTS_FILE,
)


configuration = config.Configuration()

appcaller = app_caller.AppCaller(
    logger.get_logger(LOG_PATH+'/app_caller.log', 'Environment'),
    VENV_PATH if configuration.USE_VIRTUAL_ENV is True else None,
    REQUIREMENTS_FILE,
    configuration.proxy_info
)


def execute(parameters):
    appcaller.execute(
        [system.format_command(
            u'python "{}/run_app.py"'.format(BIN_XML_PATH), parameters)])


def requirements_checker():
    required = []
    try:
        import PIL
    except:
        required.append('PIL')
    try:
        import packtools
    except:
        required.append('packtools')
    return required


def check_requirements():
    reqs = requirements_checker()
    if len(reqs) > 0:
        encoding.display_message(
            '#########\nChecking requirements:\n{}\n########'.format(
                '\n'.join(reqs)
            )
        )
        encoding.debugging('run_app.py: check_requirements()')
        appcaller.install_requirements(False, requirements_checker)


def main(parameters):
    parameters = encoding.fix_args(parameters)
    argv = parameters[1:]

    if parameters[1].endswith('xml_package_maker.py'):
        encoding.debugging('run_app.py: xpm')
        check_requirements()
        from app_modules.app import xpm
        xpm.call_make_packages(argv, '1.1')
    elif parameters[1].endswith('xml_converter.py'):
        check_requirements()
        from app_modules.app import xc
        xc.call_converter(argv, '1.1')
    elif parameters[1] == 'install':
        # configuration = config.Configuration()
        # proxy_info = configuration.proxy_info
        # appcaller.proxy_data = system.proxy_data(configuration.proxy_info)
        encoding.debugging('run_app.py: main_install()')
        appcaller.install_requirements(True, requirements_checker)
    else:
        encoding.debugging('run_app.py: unknown command')
        encoding.debugging(parameters)
        encoding.debugging('run_app.py: do nothing')


if __name__ == '__main__':
    main(sys.argv)
