# coding=utf-8

import os
import sys

from . import encoding


def format_command(command, params=None):
    parameters = ''
    if params is not None:
        parameters = ' '.join(['"' + item + '"' for item in params])
    return command + ' ' + parameters


def run_command(command):
    try:
        cmd = encoding.encode(command, sys.getfilesystemencoding())
        os.system(cmd)
    except Exception as e:
        print('run_command():')
        print(cmd)
        print(e)
