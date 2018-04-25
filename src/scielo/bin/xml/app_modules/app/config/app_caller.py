
import os
import platform

from ...generics import system
from ...generics import encoding


# proxy_data = system.proxy_data(configuration.proxy_info)


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


def gen_proxy_info(proxy_server_port):
    return ProxyInfo(system.proxy_data(proxy_server_port))


class VirtualEnv(object):

    def __init__(self, logger, venv_path):
        encoding.debugging('VirtualEnv.VirtualEnv()')
        self.logger = logger
        self.path = venv_path
        self.setUp()

    def setUp(self):
        encoding.debugging('VirtualEnv.setUp')
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

    def inform_status(self):
        encoding.debugging('VirtualEnv.inform_status')
        if self.installed is False:
            inform(u'Not found: "{}"'.format(self.activate_filename))

    @property
    def installed(self):
        encoding.debugging('VirtualEnv.installed')
        return os.path.isfile(self.activate_filename)

    def install_venv(self, recreate, proxy_info):
        encoding.debugging('VirtualEnv.install_venv')
        if self.path is not None:
            if not self.installed or recreate:
                commands = []
                commands.extend(proxy_info.register_commands)
                commands.append(
                    'python -m pip install {} -U pip'.format(
                        proxy_info.parameter)
                    )
                commands.append(
                    'python -m pip install {} --upgrade pip'.format(
                        proxy_info.parameter)
                    )
                commands.append(
                    'pip install {} virtualenv'.format(proxy_info.parameter)
                    )
                commands.append(u'virtualenv "{}"'.format(self.path))
                for cmd in commands:
                    if 'teste' in proxy_info.parameter:
                        encoding.display_message('Executaria\n  {}'.format(cmd))
                    else:
                        system.run_command(cmd)
                if self.installed:
                    inform(u'CREATED virtualenv: {}'.format(self.path))
                else:
                    inform(u'Unable to find: "{}"'.format(self.activate_filename))
                    inform(u'Unable to create the virtualenv: "{}"'.format(self.path))
                    inform('Install the programs in a path which does not have diacritics')


class Requirements(object):

    def __init__(self, requirements_file):
        self.requirements_file = requirements_file

    def install_commands(self, proxy_info, uninstall):
        commands = []
        if uninstall is True:
            commands = self.uninstall_commands()
        commands.append(
                    'python -m pip install {} -U pip'.format(
                        proxy_info.parameter)
                    )
        commands.append(
                    'python -m pip install {} --upgrade pip'.format(
                        proxy_info.parameter)
                    )
        commands.append(u'pip install {} -r "{}"'.format(
            proxy_info.parameter, self.requirements_file))
        commands.append('pip freeze > python_libraries_installed.txt')
        return commands

    def uninstall_commands(self):
        commands = []
        commands.append(
            u'pip uninstall -r "{}" -y'.format(self.requirements_file))
        return commands


class AppCaller(object):

    def __init__(self, logger, venv_path, req_file, proxy_server_port):
        encoding.debugging('AppCaller.AppCaller()')
        self.logger = logger
        self.venv = VirtualEnv(logger, venv_path)
        self.requirements = Requirements(req_file)
        self.proxy_server_port = proxy_server_port
        self.proxy_info = ProxyInfo(None)

    def install_requirements(self, restart, requirements_checker):
        encoding.debugging(
            'AppCaller.install_requirements',
            (restart, requirements_checker))
        reqs = 0
        if requirements_checker is not None:
            reqs = requirements_checker()
        encoding.debugging(
            'AppCaller.install_requirements',
            (reqs, restart))
        if restart or reqs > 0:
            self.proxy_info = gen_proxy_info(self.proxy_server_port)
            if restart or not self.venv.installed:
                encoding.debugging(
                    'AppCaller.install_requirements: self.venv.install_venv')
                self.venv.install_venv(restart, self.proxy_info)
            encoding.debugging(
                'AppCaller.install_requirements: self.requirements.install_commands')
            commands = self.requirements.install_commands(
                self.proxy_info,
                uninstall=restart)

            self.execute(commands)

    def format_commands(self, commands):
        encoding.debugging('AppCaller.format_commands', commands)
        _commands = []
        for cmd in commands:
            _cmd = []
            if self.venv.installed:
                _cmd = [self.venv.activate_command]
            if self.proxy_info.parameter in cmd:
                _cmd.extend(self.proxy_info.register_commands)
            _cmd.append(cmd)
            if self.venv.installed:
                # _cmd.append(self.venv.deactivate_command)
                _cmd = [self.commands_inline(_cmd)]
            _commands.extend(_cmd)
        encoding.debugging('AppCaller.format_commands: formatted', _commands)
        return _commands

    def commands_inline(self, commands):
        encoding.debugging('AppCaller.commands_inline', commands)
        _commands = [item for item in commands if len(item) > 0]
        _cmd = self.venv.sep.join(_commands)
        return _cmd

    def execute(self, commands):
        encoding.debugging(
            'AppCaller.execute',
            commands)
        for cmd in self.format_commands(commands):
            encoding.debugging(
                'AppCaller.execute',
                cmd)
            display_cmd = self.proxy_info.hide_password(cmd)
            self.logger.info(display_cmd)
            encoding.display_message(display_cmd)
            os.system(cmd)
