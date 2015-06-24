# coding=utf-8

import os

import email_service
import xc_config


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


def get_mailer(config):
    if config.is_enabled_email_service:
        return email_service.EmailService(config.email_sender_name, config.email_sender_email)


def get_configuration(collection_acron):
    config = None
    f = xc_config_filename(collection_acron)
    errors = is_valid_configuration_file(f)
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


def is_valid_configuration_file(configuration_filename):
    messages = []
    if configuration_filename is None:
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: No configuration file was informed')
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: unable to read the configuration file: ' + configuration_filename)
    return messages


def run_remote_mkdirs(user, server, path):
    try:
        os.system('ssh ' + user + '@' + server + ' "mkdir -p ' + path + '"')
    except:
        pass


def run_rsync(source, user, server, dest):
    try:
        os.system('nohup rsync -CrvK ' + source + '/* ' + user + '@' + server + ':' + dest + '&\n')
    except:
        pass
