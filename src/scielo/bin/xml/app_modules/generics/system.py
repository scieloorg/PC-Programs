# coding=utf-8

import os

from . import encoding


def format_command(command, params=None):
    parameters = ''
    if params is not None:
        parameters = ' '.join(['"' + item + '"' for item in params])
    return command + ' ' + parameters


def run_command(command, display=False):
    if display is True:
        try:
            encoding.display_message(u'Running:\n {}'.format(command))
        except Exception as e:
            pass

    try:
        os.system(encoding.encode(command, encoding.SYS_DEFAULT_ENCODING))
        if display is True:
            encoding.display_message('...done')
    except Exception as e:
        encoding.report_exception('system.run_command()', e, command)
