
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


class ProxyInfo(object):

    def __init__(self, proxy_data):
        self.username = None
        self.password = None
        self.server_port = None
        if proxy_data is not None:
            self.username, self.password, self.server_port = proxy_data

    @property
    def parameter(self):
        if all([self.username, self.password, self.server_port]) is True:
            return '--proxy="{}:{}@{}"'.format(
                    self.username, self.password, self.server_port
                )
        return ''

    def hide_password(self, cmd):
        if self.password is not None:
            return cmd.replace(
                ':{}@'.format(self.password),
                ':{}@'.format('*'*len(self.password)))
        return cmd

    @property
    def register_commands(self):
        commands = []
        if all([self.username, self.password, self.server_port]) is True:
            proxy_info = '{}:{}@{}'.format(
                self.username, self.password, self.server_port)
            command = 'set'
            if 'windows' not in so:
                command = 'export'
            commands.append(
                '{} http_proxy=http://{}'.format(command, proxy_info))
            commands.append(
                '{} https_proxy=https://{}'.format(command, proxy_info))
        return commands


class VirtualEnv(object):

    def __init__(self, logger, venv_path, requirements_filename):
        self.logger = logger
        self.path = venv_path
        self.requirements = Requirements(requirements_filename)
        self.proxy_info = ProxyInfo(None)
        self.setUp()

    def setUp(self):
        if 'windows' in so:
            self.activate_filename = u'{}/Scripts/activate.bat'.format(self.path)
            self.activate_command = u'call "{}"'.format(self.activate_filename)
            self.deactivate_command = u'call "{}/Scripts/deactivate.bat"'.format(self.path)
            self.sep = ' & '
        else:
            self.activate_filename = u'{}/bin/activate'.format(self.path)
            self.activate_command = u'source "{}"'.format(self.activate_filename)
            self.deactivate_command = 'deactivate'
            self.sep = ';'
        if self.path is None or not os.path.isdir(self.path):
            self.activate_command = ''
            self.deactivate_command = ''

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
                commands.extend(self.proxy_info.register_commands)
                commands.append(
                    'python -m pip install {} -U pip'.format(
                        self.proxy_info.parameter)
                    )
                commands.append(
                    'python -m pip install {} --upgrade pip'.format(
                        self.proxy_info.parameter)
                    )
                commands.append(
                    'pip install {} virtualenv'.format(self.proxy_info.parameter)
                    )
                commands.append(u'virtualenv "{}"'.format(self.path))
                for cmd in commands:
                    if 'teste' in self.proxy_info.parameter:
                        encoding.display_message('Executaria\n  {}'.format(cmd))
                    else:
                        system.run_command(cmd)
                if self.installed:
                    inform(u'CREATED virtualenv: {}'.format(self.path))
                else:
                    inform(u'Unable to find: "{}"'.format(self.activate_filename))
                    inform(u'Unable to create the virtualenv: "{}"'.format(self.path))
                    inform('Install the programs in a path which does not have diacritics')

    def install_requirements(self):
        commands = self.requirements.install_commands(
                self.proxy_info,
                uninstall=True)
        self.execute_in_virtualenv(commands)

    def execute_in_virtualenv(self, commands):
        self.install_venv()
        if self.installed:
            _commands = [self.activate_command]
            _commands.extend(commands)
            self._execute_inline(_commands)

    def _execute_inline(self, commands):
        _commands = [item for item in commands if len(item) > 0]
        cmd = self.sep.join(_commands)
        display_cmd = self.proxy_info.hide_password(cmd)
        self.logger.info(display_cmd)
        if 'teste' in cmd:
            encoding.display_message('Executaria\n  {}'.format(cmd))
        else:
            encoding.display_message(display_cmd)
            system.run_command(cmd, False)

    def activate(self):
        if self.installed:
            system.run_command(self.activate_command, True)

    def deactivate(self):
        if self.installed:
            system.run_command(self.deactivate_command, True)


class RealEnv(object):

    def __init__(self, logger, requirements_filename):
        self.logger = logger
        self.requirements = Requirements(requirements_filename)
        self.proxy_info = ProxyInfo(None)

    def install_requirements(self):
        commands = self.requirements.install_commands(
                self.proxy_info,
                uninstall=True)
        self.execute_commands(commands)

    def execute_commands(self, commands):
        for cmd in commands:
            display_cmd = self.proxy_info.hide_password(cmd)
            self.logger.info(display_cmd)
            encoding.display_message(display_cmd)
            os.system(cmd)


class Requirements(object):

    def __init__(self, requirements_file):
        self.requirements_file = requirements_file

    def install_commands(self, proxy, uninstall):
        commands = []
        if uninstall is True:
            commands = self.uninstall_commands()
        commands.extend(proxy.register_commands)
        commands.append(
                    'python -m pip install {} -U pip'.format(
                        proxy.parameter)
                    )
        commands.append(
                    'python -m pip install {} --upgrade pip'.format(
                        proxy.parameter)
                    )
        commands.append(u'pip install {} -r "{}"'.format(
            proxy.parameter, self.requirements_file))
        commands.append('pip freeze > python_libraries_installed.txt')
        return commands

    def uninstall_commands(self):
        commands = []
        commands.append(
            u'pip uninstall -r "{}" -y'.format(self.requirements_file))
        return commands


class VEnvAppCaller(object):

    def __init__(self, logger, venv_path, req_file):
        self.environment = VirtualEnv(logger, venv_path, req_file)

    @property
    def proxy_info(self):
        return self.environment.proxy_info

    @proxy_info.setter
    def proxy_info(self, _proxy_info):
        self.environment.proxy_info = _proxy_info

    def install_virtualenv(self, recreate=False):
        inform('Install virtualenv')
        self.environment.install_venv()
        if self.environment.installed:
            inform('Install virtualenv: done!')

    def install_requirements(self):
        if self.environment.installed:
            inform('Install Requirements')
            self.environment.install_requirements()
        #inform('Install Requirements: done!')

    def execute(self, commands):
        self.environment.execute_in_virtualenv(commands)


class RealAppCaller(object):

    def __init__(self, logger, venv_path, req_file):
        self.environment = RealEnv(logger, req_file)

    @property
    def proxy_info(self):
        return self.environment.proxy_info

    @proxy_info.setter
    def proxy_info(self, _proxy_info):
        self.environment.proxy_info = _proxy_info

    def install_virtualenv(self, recreate=False):
        pass

    def install_requirements(self):
        self.environment.install_requirements()

    def execute(self, commands):
        self.environment.execute_commands(commands)


class AppCaller(object):

    def __init__(self, logger, venv_path, req_file):
        self.caller = None
        if venv_path is not None:
            virtual = VEnvAppCaller(logger, venv_path, req_file)
            virtual.install_virtualenv(True)
            if virtual.environment.installed:
                self.caller = virtual
        if self.caller is None:
            self.caller = RealAppCaller(logger, venv_path, req_file)

    @property
    def proxy_data(self):
        return self.caller.proxy_info

    @proxy_data.setter
    def proxy_data(self, _proxy_data):
        self.caller.proxy_info = ProxyInfo(_proxy_data)

    def install_virtualenv(self, recreate=False):
        self.caller.install_virtualenv(recreate)

    def install_requirements(self):
        self.caller.install_requirements()

    def execute(self, commands):
        self.caller.execute(commands)
