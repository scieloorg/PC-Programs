
import os
import platform

from ...generics import system
from ...generics import fs_utils


so, node, release, version, machine, processor = platform.uname()
python_version = platform.python_version()
so = so.lower()


class VirtualEnv(object):

    def __init__(self, logger, venv_path, requirements):
        self.logger = logger
        self.path = venv_path
        self.requirements = requirements
        self.setUp()

    def setUp(self):
        if 'windows' in so:
            self.activate = '{}/Scripts/activate.bat'.format(self.path)
            self.deactivate = '{}/Scripts/deactivate.bat'.format(self.path)
            self.sep = ' & '
        else:
            self.activate = 'source {}/bin/activate'.format(self.path)
            self.deactivate = 'deactivate'
            self.sep = ';'
        if self.path is None or not os.path.isdir(self.path):
            self.activate = ''
            self.deactivate = ''

    def install(self, force=False):
        if self.path is not None:
            if force:
                if os.path.isdir(self.path):
                    fs_utils.delete_file_or_folder(self.path)
            if not os.path.isdir(self.path):
                system.run_command('python -m pip install --upgrade pip', True)
                system.run_command('pip install virtualenv', True)
                system.run_command(u'virtualenv {}'.format(self.path), True)

    def reqs_check(self):
        system.run_command(self.activate)
        reqs = self.requirements.checker()
        if len(reqs) > 0:
            self.execute(self.requirements.install_commands(uninstall=True))
        reqs = self.requirements.checker()
        if len(reqs) > 0:
            self.requirements.display_errors(reqs)
        return len(reqs) == 0

    def execute(self, commands):
        self.install()
        if self.reqs_check():
            _commands = [self.activate]
            _commands.extend(commands)
            _commands.append(self.deactivate)
            self._execute_inline(_commands)
        else:
            print('Unable to run {}'.format('\n'.join(commands)))

    def _execute_inline(self, commands):
        _commands = [item for item in commands if len(item) > 0]
        cmd = self.sep.join(_commands)
        if 'windows' in so:
            cmd = cmd.replace('/', '\\')
        self.logger.info(cmd)
        system.run_command(cmd)


class Requirements(object):

    def __init__(self, requirements_file, requirements_checker):
        self.requirements_file = requirements_file
        self.checker = requirements_checker

    def install_commands(self, uninstall=True):
        commands = []
        if uninstall is True:
            commands = self.uninstall_commands()
        commands.append('pip freeze > req_i_1.txt')
        commands.append('pip install -r {}'.format(self.requirements_file))
        commands.append('pip freeze > req_i_2.txt')
        return commands

    def uninstall_commands(self):
        commands = []
        commands.append('pip freeze > req_u_1.txt')
        commands.append('pip uninstall -r {} -y'.format(self.requirements_file))
        commands.append('pip freeze > req_u_2.txt')
        return commands

    def display_errors(self, reqs):
        print('!'*30)
        if len(reqs) == 0:
            print('Success')
            print('Requirements OK')
        else:
            print('Failure')
        for req in reqs:
            print('{} is not installed'.format(req))
        print('!'*30)


class AppCaller(object):

    def __init__(self, logger, venv_path, req_file, req_checker):
        self.venv = VirtualEnv(logger, venv_path, Requirements(req_file, req_checker))

    def install_virtualenv(self):
        self.venv.install(force=True)

    def install_requirements(self):
        self.venv.requirements.install()

    def execute(self, commands):
        self.venv.execute(commands)
