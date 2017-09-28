# coding=utf-8

import os

from datetime import datetime

from ...generics import fs_utils
from ...generics import logger
from ...generics import system
from . import filestransfer
from ...__init__ import LOG_PATH


def is_finished(permission_file):
    ret = False
    if permission_file is not None:
        if os.path.isfile(permission_file):
            status = open(permission_file, 'r').read()
        else:
            status = 'FINISHED'
        if status != 'running':
            ret = True
    return ret


def block_gerapadrao(permission_file):
    open(permission_file, 'w').write('running')


def consume_collection_scilista(scilista_file):
    content = None
    if scilista_file is not None:
        if os.path.isfile(scilista_file):
            content = fs_utils.read_file(scilista_file)
            fs_utils.delete_file_or_folder(scilista_file)
    return content


def sort_scilista(scilista_content):
    scilista_items = list(set([item.strip() for item in scilista_content.split('\n') if len(item) if ' ' in item]))
    scilista_items = [item for item in scilista_items if item.endswith('pr')] + [item for item in scilista_items if not item.endswith('pr')]
    return '\n'.join(scilista_items) + '\n'


def gerapadrao(collection_acron, config, mailer):
    if is_finished(config.gerapadrao_permission_file):
        start_time = datetime.now().isoformat()[11:11+5].replace(':', '')
        log_filename = LOG_PATH + '/gerapadrao_'+collection_acron+'-'+start_time+'.log'
        gerapadrao_logger = logger.get_logger(log_filename, 'gerapadrao')

        config.update_title_and_issue()
        scilista_content = consume_collection_scilista(
            config.collection_scilista)

        if scilista_content is None:
            print(config.collection_scilista + ' is empty')
        else:
            block_gerapadrao(config.gerapadrao_permission_file)

            scilista_content = sort_scilista(scilista_content)
            fs_utils.write_file(config.gerapadrao_scilista, scilista_content)

            scilista_items = scilista_content.split('\n')

            gerapadrao_cmd = gerapadrao_command(
                config.gerapadrao_proc_path,
                config.gerapadrao_permission_file)

            if mailer is not None:
                mailer.send_message(
                    config.email_to,
                    config.email_subject_gerapadrao.replace(
                        'Gerapadrao',
                        'Gerapadrao ' + start_time + ' '),
                    config.email_text_gerapadrao + scilista_content)

            gerapadrao_logger.info(start_time + ' - inicio gerapadrao')
            gerapadrao_logger.info(gerapadrao_cmd)
            gerapadrao_logger.info(scilista_content)
            system.run_command(gerapadrao_cmd)
            gerapadrao_logger.info(start_time + ' - fim gerapadrao')

            if config.is_enabled_transference:
                transfer = filestransfer.FilesTransfer(config)

                gerapadrao_logger.info(start_time + ' - inicio transf bases')
                transfer.transfer_website_bases()
                gerapadrao_logger.info(start_time + ' - fim transf bases')

                gerapadrao_logger.info(start_time + ' - inicio transf files')
                for scilista_item in scilista_items:
                    gerapadrao_logger.info(start_time + ' ' + scilista_item)
                    items = scilista_item.split()
                    if len(items) == 2:
                        acron, issue_id = items
                        transfer.transfer_website_files(acron, issue_id)
                gerapadrao_logger.info(start_time + ' - fim transf files')

            if mailer is not None:
                mailer.send_message(
                    config.email_to,
                    config.email_subject_website_update.replace(
                        'Gerapadrao',
                        'Gerapadrao ' + start_time + ' '),
                    config.email_text_website_update + scilista_content)
    else:
        print('gerapadrao is running. Wait ...')
        if mailer is not None:
            msg = []
            if os.path.isfile(config.gerapadrao_scilista):
                msg.append(
                    'Running:\n' + fs_utils.read_file(
                        config.gerapadrao_scilista)+'\n\n')
            if os.path.isfile(config.collection_scilista):
                msg.append(
                    'Waiting:\n' + sort_scilista(
                        fs_utils.read_file(config.collection_scilista)))

            if len(msg) > 0:
                mailer.send_message(
                    config.email_to_adm,
                    'gerapadrao is busy',
                    ''.join(msg))


def gerapadrao_command(proc_path, gerapadrao_status_filename):
    return 'cd ' + proc_path + ';./GeraPadrao.bat;echo FINISHED>' + gerapadrao_status_filename
