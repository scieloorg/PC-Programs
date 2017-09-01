import platform
from ...generics import system


so = platform.platform().lower()


def info(venv_path):
    if 'windows' in so:
        return '{}/Scripts/activate'.format(venv_path), '{}/Scripts/deactivate'.format(venv_path), ' & '
    return 'source {}/bin/activate'.format(venv_path), 'deactivate', ';'


def execute_commands_in_venv(venv_path, commands):
    activate_command, deactivate_command, sep = info(venv_path)
    _commands = [activate_command]
    _commands.append('python -V')
    _commands.extend(commands)
    _commands.append(deactivate_command)
    system.run_command(sep.join(_commands))
