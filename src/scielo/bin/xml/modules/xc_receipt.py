# coding=utf-8

import os

import ftp_service
import xc


CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')
CONFIG_PATH = CURRENT_PATH + '/../config/'

def download_packages(config):
    ftp = ftp_service.FTPService(config.ftp_server, config.ftp_user, config.ftp_user_pswd)
    if not os.path.isdir(config.download_path):
        os.makedirs(config.download_path)
    files = ftp.download_files(config.download_path, config.ftp_dir)
    log = ftp.registered_actions
    return (files, log)


def xml_receipt_get_inputs(args):
    # python xml_receipt.py <collection_acron>
    script = None
    collection_acron = None
    if len(args) == 2:
        script, collection_acron = args
    return (script, collection_acron)


def xml_receipt_validate_inputs(collection_acron):
    errors = []
    if collection_acron is None:
        errors.append('Missing collection acronym')
    return errors


def receive_xml_files(args):
    collection_acron = xml_receipt_get_inputs(args)
    errors = xml_receipt_validate_inputs(collection_acron)
    if len(errors) > 0:
        print(errors)
    else:
        config = xc.get_configuration(collection_acron)
        if config is not None:
            files, log = download_packages(config)
            if len(files) > 0:
                mailer = xc.get_mailer(config)
                if mailer is not None:
                    mailer.send_message(config.email_to, config.email_subject_packages_receipt, config.email_text_packages_receipt + '\n' + log)
