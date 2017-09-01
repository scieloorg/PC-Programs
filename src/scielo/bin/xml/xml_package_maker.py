import os
import sys

from modules.app.config import app_venv


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

venv_path = '{}/venv/scielo-programs'.format(THIS_LOCATION)

commands = ['python -V',
            'python xpm_caller.py '.format(THIS_LOCATION) + ' '.join(sys.argv[1:])]

print(commands)
app_venv.execute_commands_in_venv(venv_path, commands)
