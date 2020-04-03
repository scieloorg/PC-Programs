# coding=utf-8

import os
import sys
import getpass


from . import encoding


def format_param(param):
    if ' ' in param:
        return u'"{}"'.format(param)
    return param


def format_command(command, params=None):
    parameters = ''
    if params is not None:
        parameters = u' '.join([format_param(item) for item in params])
    return command + ' ' + parameters


def run_command(command, display=False):
    if display:
        encoding.display_message(u'Running:\n {}'.format(command))
    os.system(command)
    if display:
        encoding.display_message('...done')


def input_password():
    pswd = getpass.getpass('Password: ')
    return encoding.decode(pswd, sys.stdin.encoding)


def proxy_parameter(proxy_info):
    proxy = ''
    if proxy_info is not None:
        resp = read_input('Do you use proxy for Internet access ({})? Y/N '.format(proxy_info))
        if resp in 'Yy':
            username = read_input('Inform proxy Username: ')
            password = input_password()
            proxy = '--proxy="{}:{}@http://{}"'.format(
                username,
                password,
                proxy_info
                )
    return proxy


def proxy_data(proxy_info):
    proxy = None
    if proxy_info is not None:
        resp = read_input('Do you use proxy for Internet access ({})? Y/N '.format(proxy_info))
        if resp in 'Yy':
            username = read_input('Inform proxy Username: ')
            password = input_password()
            proxy = [
                username,
                password,
                proxy_info
            ]
    return proxy


def read_input(question):
    if sys.version_info[0] == 2:
        return raw_input(question)
    return input(question)


def command_proxy_parameter(command):
    if '--proxy="' in command:
        p = command[command.find('--proxy="'):]
        p = p[:p.find('" ')+1]
        return p
    return ''


def proxy_password(param):
    if ':' in param and '@' in param:
        p = param[param.find(':'):]
        p = p[:p.find('@')+1]
        return p
