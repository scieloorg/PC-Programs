import os
from modules.generics import system
from modules.app.config import app_venv


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

venv_path = '{}/venv/scielo-programs'.format(THIS_LOCATION)
system.run_command('pip install virtualenv')
system.run_command('virtualenv {}/venv/scielo-programs'.format(THIS_LOCATION))

pip_install_command = 'pip install -r {}/venv/requirements.txt'.format(THIS_LOCATION)
test_req = 'python {}/venv/requirements_checker.py'.format(THIS_LOCATION)

commands = [pip_install_command]
commands.append(test_req)
app_venv.execute_commands_in_venv(venv_path, commands)
