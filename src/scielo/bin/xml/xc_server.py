# coding=utf-8
import os
import sys

from prodtools.utils import encoding
from prodtools.utils import ftp_service
from prodtools.config import config
from prodtools.server import mailer
from prodtools.server import xc_gerapadrao


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


valid_parameters = False
argv = encoding.fix_args(sys.argv)
if len(argv) == 3:
    action, collection_acron = argv[1:]
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
            valid_parameters = True
        elif action == 'end':
            xc_gerapadrao.gerapadrao(collection_acron, cfg, msg_sender)
            valid_parameters = True
        elif action == 'xc':
            from app_modules.app import xc
            valid_parameters = True
            xc.call_converter([action, collection_acron], '1.1')


if valid_parameters is False:
    print('Unable to execute')
    print(argv)
    print('Usage: python2.7 {} [begin|end] <col>'.format(argv[0]))


