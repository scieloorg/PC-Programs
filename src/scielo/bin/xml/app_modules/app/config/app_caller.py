
import os
import platform

from ...generics import system
from ...generics import encoding


so, node, release, version, machine, processor = platform.uname()
python_version = platform.python_version()
so = so.lower()


def ask_to_execute(commands):
    print('\nExecute the commands: ')
    print('\n'+'='*20)
    print('\n'.join(commands))
    print('\n'+'='*20)


def inform(msg):
    print('')
    encoding.display_message(u' >>> '+msg)
    print('')


class VirtualEnv(object):

    def __init__(self, logger, venv_path, requirements):
        self.logger = logger
        self.path = venv_path
        self.requirements = requirements
        self.setUp()
        self.proxy_data = None

    def setUp(self):
        if 'windows' in so:
            self.activate_filename = u'{}/Scripts/activate.bat'.format(self.path)
            self.activate_command = u'call "{}/Scripts/activate.bat"'.format(self.path)
            self.deactivate_command = u'call "{}/Scripts/deactivate.bat"'.format(self.path)
            self.sep = ' & '
        else:
            self.activate_filename = u'{}/bin/activate'.format(self.path)
            self.activate_command = u'source "{}/bin/activate"'.format(self.path)
            self.deactivate_command = 'deactivate'
            self.sep = ';'
        if self.path is None or not os.path.isdir(self.path):
            self.activate_command = ''
            self.deactivate_command = ''

    def omit_password(self, cmd):
        if self.proxy_data is not None:
            username, password, proxy_info = self.proxy_data
            return cmd.replace(
                ':{}@'.format(password), ':{}@'.format('*'*len(password)))

    @property
    def proxy_parameter(self):
        if self.proxy_data is not None:
            return proxy_parameter(self.proxy_data)

    @property
    def installed(self):
        status = os.path.isfile(self.activate_filename)
        if status is False:
            inform(u'Missing virtualenv: "{}"'.format(self.activate_filename))
        return status

    def install_venv(self):
        if self.path is not None:
            if not self.installed:
                commands = []
                commands.append('python -m pip install {} --upgrade pip'.format(self.proxy_parameter))
                commands.append('pip install {} virtualenv'.format(self.proxy_parameter))
                commands.append(u'virtualenv "{}"'.format(self.path))
                for cmd in commands:
                    system.run_command(cmd)
                if self.installed:
                    inform(u'CREATED virtualenv: {}'.format(self.path))
                else:
                    inform(u'Unable to find: "{}"'.format(self.activate_filename))
                    inform(u'Unable to create the virtualenv: "{}"'.format(self.path))
                    inform('Install the programs in a path which does not have diacritics')

    def install_requirements(self):
        commands = self.requirements.install_commands(
                uninstall=True, proxy_data=self.proxy_data)
        self.execute(commands)

    def execute(self, commands):
        self.install_venv()
        if self.installed:
            _commands = [self.activate_command]
            _commands.extend(commands)
            self._execute_inline(_commands)

    def _execute_inline(self, commands):
        _commands = [item for item in commands if len(item) > 0]
        cmd = self.sep.join(_commands)

        display_cmd = cmd
        if self.proxy_data is not None:
            display_cmd = self.omit_password(cmd)
            encoding.display_message(display_cmd)
        self.logger.info(display_cmd)
        system.run_command(cmd, self.proxy_data is None)

    def activate(self):
        if self.installed:
            system.run_command(self.activate_command, True)

    def deactivate(self):
        if self.installed:
            system.run_command(self.deactivate_command, True)


class Requirements(object):

    def __init__(self, requirements_file):
        self.requirements_file = requirements_file

    def register_proxy(self, proxy_data):
        commands = []
        if proxy_data is not None:
            username, password, proxy = proxy_data
            proxy_info = '{}:{}@{}'.format(username, password, proxy)
            command = 'set'
            if 'windows' not in so:
                command = 'export'
            commands.append('{} http=http://{}'.format(command, proxy_info))
            commands.append('{} https=https://{}'.format(command, proxy_info))
        return commands

    def install_commands(self, uninstall=True, proxy_data=None):
        commands = []
        if uninstall is True:
            commands = self.uninstall_commands()
        commands.extend(self.register_proxy(proxy_data))
        commands.append('pip freeze > req_i1.txt')
        commands.append(u'pip install {} -r "{}"'.format(
            proxy_parameter(proxy_data), self.requirements_file))
        commands.append('pip freeze > req_i2.txt')
        return commands

    def uninstall_commands(self):
        commands = []
        commands.append('pip freeze > req_u1.txt')
        commands.append(u'pip uninstall -r "{}" -y'.format(self.requirements_file))
        commands.append('pip freeze > req_u2.txt')
        return commands


class AppCaller(object):

    def __init__(self, logger, venv_path, req_file):
        self.venv = VirtualEnv(logger, venv_path, Requirements(req_file))

    @property
    def proxy_data(self):
        return self.venv.proxy_data

    @proxy_data.setter
    def proxy_data(self, value):
        self.venv.proxy_data = value

    def install_virtualenv(self, recreate=False):
        inform('Install virtualenv')
        self.venv.install_venv()
        if self.venv.installed:
            inform('Install virtualenv: done!')

    def install_requirements(self):
        if self.venv.installed:
            inform('Install Requirements')
            self.venv.install_requirements()
        #inform('Install Requirements: done!')

    def execute(self, commands):
        self.venv.execute(commands)


def proxy_parameter(proxy_data):
    if proxy_data is not None:
        username, password, proxy_info = proxy_data
        return '--proxy="{}:{}@http://{}"'.format(
                username, password, proxy_info
            )
    return ''
