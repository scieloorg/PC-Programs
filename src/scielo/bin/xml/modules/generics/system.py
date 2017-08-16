# coding=utf-8

import os

from . import encoding
from . import utils


def format_command(command, params=None):
    parameters = ''
    if params is not None:
        parameters = ' '.join(['"' + item + '"' for item in params])
    return command + ' ' + parameters


def run_command(command):
    try:
        cmd = encoding.encode(command, encoding.SYS_DEFAULT_ENCODING)
        os.system(cmd)
    except Exception as e:
        utils.debugging('system.run_command()', cmd)
        utils.debugging('system.run_command()', e)
