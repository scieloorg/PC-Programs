import sys

import app_run


app_run.appvenv.run_in_venv(
    ['python app_run.py xc ' + ' '.join(sys.argv[2:])])
