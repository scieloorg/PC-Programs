# coding=utf-8

import os

from . import encoding


def format_command(command, params=None):
    parameters = ''
    if params is not None:
        parameters = ' '.join(['"' + item + '"' for item in params])
    return command + ' ' + parameters


def run_command(command):
    try:
        os.system(encoding.encode(command, encoding.SYS_DEFAULT_ENCODING))
    except Exception as e:
        encoding.report_exception('system.run_command()', e, command)
