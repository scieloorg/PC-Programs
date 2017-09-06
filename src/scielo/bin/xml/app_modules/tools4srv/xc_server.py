# coding=utf-8
import os
import sys

from ...generics import ftp_service
from ...app.config import config
from ...app.server import mailer
from . import xc_gerapadrao


def download_packages(configuration):
    ftp = ftp_service.FTPService(
        configuration.ftp_server,
        configuration.ftp_user,
        configuration.ftp_pswd)
    if not os.path.isdir(configuration.download_path):
        os.makedirs(configuration.download_path)
    files = ftp.download_files(
        configuration.download_path, configuration.ftp_dir)
    return (files, ftp.registered_actions)


if len(sys.argv) == 3:
    action, collection_acron = sys.argv[1:]
    filename = config.get_configuration_filename(collection_acron)
    if filename is None:
        print('Unable to find configuration file for ' + collection_acron)
    else:
        cfg = config.Configuration(filename)
        msg_sender = mailer.Mailer(cfg)
        if action == 'begin':
            files, msg = download_packages(cfg)
            if len(files) > 0 and msg_sender is not None:
                msg_sender.send_message(
                    cfg.email_to,
                    cfg.email_subject_packages_receipt,
                    cfg.email_text_packages_receipt + '\n' + msg)
        elif action == 'end':
            xc_gerapadrao.gerapadrao(collection_acron, cfg, mailer)
        else:
            print('Unable to execute')
            print(sys.argv)
