import sys

import app_run

print(sys.argv[1:])
app_run.appvenv.run_in_venv(
    ['python app_run.py xpm ' + ' '.join(sys.argv[1:])])
