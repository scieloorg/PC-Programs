# coding=utf-8

import os
from datetime import datetime

import email_service
import xc_config
import fs_utils


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


def get_mailer(config):
    if config.is_enabled_email_service:
        return email_service.EmailService(config.email_sender_name, config.email_sender_email)


def get_configuration(collection_acron):
    config = None
    f = xc_config_filename(collection_acron)
    errors = is_config_file(f)
    if len(errors) > 0:
        print('\n'.join(errors))
    else:
        config = xc_read_configuration(f)

    return config


def xc_read_configuration(filename):
    r = None
    if os.path.isfile(filename):
        r = xc_config.XMLConverterConfiguration(filename)
        if not r.valid:
            r = None
    return r


def xc_config_filename(collection_acron):
    if collection_acron is None:
        f = CURRENT_PATH + '/../../scielo_paths.ini'
        if os.path.isfile(f):
            filename = f
        else:
            filename = CURRENT_PATH + '/../config/default.xc.ini'
    else:
        filename = CURRENT_PATH + '/../config/' + collection_acron + '.xc.ini'

    return filename


def is_config_file(configuration_filename):
    messages = []
    if configuration_filename is None:
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: No configuration file was informed')
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: unable to read the configuration file: ' + configuration_filename)
    return messages


def run_cmd(cmd, log_filename=None):
    print(cmd)
    if log_filename is not None:
        fs_utils.append_file(log_filename, datetime.now().isoformat() + ' ' + cmd)
    try:
        os.system(cmd)
        if log_filename is not None:
            fs_utils.append_file(log_filename, 'done')
    except:
        if log_filename is not None:
            fs_utils.append_file(log_filename, 'failure')


def run_remote_mkdirs(user, server, path, log_filename=None):
    cmd = 'ssh ' + user + '@' + server + ' "mkdir -p ' + path + '"'
    run_cmd(cmd, log_filename)


def run_rsync(source, user, server, dest, log_filename=None):
    cmd = 'nohup rsync -CrvK ' + source + '/* ' + user + '@' + server + ':' + dest + '&\n'
    run_cmd(cmd, log_filename)


def run_scp(source, user, server, dest, log_filename=None):
    cmd = 'nohup scp -r ' + source + ' ' + user + '@' + server + ':' + dest + '&\n'
    run_cmd(cmd, log_filename)
