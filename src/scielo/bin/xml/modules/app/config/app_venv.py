
import platform
from ...generics import system


so = platform.platform().lower()


def info(venv_path):
    if 'windows' in so:
        activate = '{}/Scripts/activate'.format(venv_path)
        deactivate = '{}/Scripts/deactivate'.format(venv_path)
        sep = ' & '
    else:
        activate = 'source {}/bin/activate'.format(venv_path)
        deactivate = 'deactivate'
        sep = ';'
    if venv_path is None:
        activate = ''
        deactivate = ''
    return activate, deactivate, sep


class AppEnv(object):

    def __init__(self, venv_path=None):
        self.venv_path = venv_path
        self.activate_command, self.deactivate_command, self.sep = info(venv_path)

    def install(self, requirements_path):
        if self.venv_path is not None:
            system.run_command('pip install virtualenv')
            system.run_command(u'virtualenv {}'.format(self.venv_path))
        self.install_requirements(
            requirements_path+'/requirements.txt',
            requirements_path+'/requirements_checker.py')

    def run_in_venv(self, commands):
        _commands = [self.activate_command]
        _commands.append(u'echo {}'.format(self.venv_path))
        _commands.append('python -V')
        _commands.extend(commands)
        _commands.append(self.deactivate_command)
        system.run_command(self.sep.join(_commands))

    def install_requirements(self, requirements_file, requirements_checker):
        commands = []
        commands.append('pip install -r {}'.format(requirements_file))
        commands.append('python {}'.format(requirements_checker))
        self.run_in_venv(commands)
