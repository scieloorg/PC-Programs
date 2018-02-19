import sys

import run_app
from app_modules.generics import encoding


run_app.execute(encoding.fix_args(sys.argv))
