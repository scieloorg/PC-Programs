
import os
import platform

from ...generics import system
from ...generics import fs_utils
from ...generics import encoding
from ...generics.ws import ws_requester


so, node, release, version, machine, processor = platform.uname()
python_version = platform.python_version()
so = so.lower()


def info(venv_path):
    if 'windows' in so:
        activate = '{}/Scripts/activate.bat'.format(venv_path)
        deactivate = '{}/Scripts/deactivate.bat'.format(venv_path)
        sep = ' & '
    else:
        activate = 'source {}/bin/activate'.format(venv_path)
        deactivate = 'deactivate'
        sep = ';'
    if venv_path is None or not os.path.isdir(venv_path):
        activate = ''
        deactivate = ''
    return activate, deactivate, sep


class AppCaller(object):

    def __init__(self, logger, venv_path=None):
        self.venv_path = venv_path
        self.activate_command, self.deactivate_command, self.sep = info(venv_path)
        self.logger = logger

    def install_virtualenv(self):
        if self.venv_path is not None:
            if not os.path.isdir(self.venv_path):
                system.run_command('python -m pip install --upgrade pip', True)
                system.run_command('pip install virtualenv', True)
                system.run_command(u'virtualenv {}'.format(self.venv_path), True)

    def execute(self, commands):
        _commands = [self.activate_command]
        _commands.extend(commands)
        _commands.append(self.deactivate_command)
        self.execute_inline(_commands)

    def execute_inline(self, commands):
        _commands = [item for item in commands if len(item) > 0]
        cmd = self.sep.join(_commands)
        if 'windows' in so:
            cmd = cmd.replace('/', '\\')
        self.logger.info(cmd)
        system.run_command(cmd)

    def install_requirements(self, requirements_file, requirements_checker, uninstall=True):
        if uninstall is True:
            self.uninstall_requirements(requirements_file)
        commands = []
        commands.append('pip freeze')
        commands.append('pip install -r {}'.format(requirements_file))
        commands.append('python {}'.format(requirements_checker))
        commands.append('pip freeze')
        self.execute(commands)

    def uninstall_requirements(self, requirements_file):
        commands = []
        commands.append('pip freeze')
        commands.append('pip uninstall -r {} -y'.format(requirements_file))
        commands.append('pip freeze')
        self.execute(commands)

    def install_special_requirements(self, special_requirements, tmp_dir):
        if os.path.isfile(special_requirements):
            for url in fs_utils.read_file_lines(special_requirements):
                filename = url[url.rfind('/')+1:]
                filename = filename[:filename.find('#')]
                filename = tmp_dir+'/'+filename
                ws_requester.urllib_request.urlretrieve(
                    url, filename=filename)
                self.execute(['pip install {}'.format(filename)])
        else:
            encoding.display_message(
                _('Not found {}. '.format(special_requirements)))
