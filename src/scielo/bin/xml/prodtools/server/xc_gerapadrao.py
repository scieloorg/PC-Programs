# coding=utf-8
import logging
import logging.config
import os

from datetime import datetime

from prodtools.utils import fs_utils
from prodtools.server import filestransfer
from prodtools import LOG_PATH


logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


class GeraPadraoStatusManager:

    def __init__(self, permission_file, proc_path):
        self.permission_file = permission_file
        self.proc_path = proc_path
        self._status = None

    @property
    def status(self):
        _status = None
        try:
            with open(self.permission_file, 'r') as fp:
                _status = fp.read()
        except (IOError, OSError, ValueError, TypeError):
            _status = 'FINISHED'
        return _status

    @status.setter
    def status(self, value):
        with open(self.permission_file, 'w') as fp:
            fp.write(value)

    def block(self):
        self.status = "running"

    def free(self):
        self.status = "FINISHED"

    @property
    def is_free(self):
        return self.status == 'FINISHED' or self.status != 'running'


class Scilista:

    def __init__(self, scilista_file):
        self.scilista_file = scilista_file

    def consume_collection_scilista(self):
        try:
            content = fs_utils.read_file(self.scilista_file)
        except (IOError, OSError, ValueError, TypeError):
            content = ''
        else:
            fs_utils.delete_file_or_folder(self.scilista_file)
        return content


def sort_scilista(scilista_content):
    scilista_items = list(set([item.strip()
                               for item in scilista_content.split('\n')
                               if len(item) if ' ' in item]))
    scilista_items = ([item
                       for item in scilista_items
                       if item.endswith('pr')] +
                      [item
                       for item in scilista_items
                       if not item.endswith('pr')])
    return '\n'.join(scilista_items) + '\n'


class GeraPadrao:

    def __init__(self, collection_acron, config, mailer):
        self.collection_acron = collection_acron
        self.config = config
        self.mailer = mailer
        self.status_manager = GeraPadraoStatusManager(
            self.config.gerapadrao_permission_file)
        self.col_scilista = Scilista(self.config.collection_scilista)
        log_filename = (LOG_PATH + '/gerapadrao_' +
                        collection_acron+'-'+self.now+'.log')
        logging.basicConfig(filename=log_filename, filemode='w')

    @property
    def now(self):
        return datetime.now().isoformat()[11:11+5].replace(':', '')

    @property
    def command(self):
        return 'cd {};./GeraPadrao.bat;echo FINISHED>{}'.format(
                self.config.gerapadrao_proc_path,
                self.config.gerapadrao_permission_file)

    def run(self):
        if self.status_manager.is_free:
            self.status_manager.block()
            scilista_content = self.col_scilista.consume_collection_scilista()
            if scilista_content:
                self.config.update_title_and_issue()
                scilista_content = sort_scilista(scilista_content)
                fs_utils.write_file(
                    self.config.gerapadrao_scilista, scilista_content)
                self._gerapadrao(scilista_content)
                self._update_web_site(scilista_content)
            else:
                self.status_manager.free()
        else:
            self.mail_gerapadrao_is_busy()

    def _gerapadrao(self, scilista_content):
        if self.mailer is not None:
            self.mailer.send_message(
                self.config.email_to,
                self.config.email_subject_gerapadrao.replace(
                    'Gerapadrao',
                    'Gerapadrao {}'.format(self.now)),
                self.config.email_text_gerapadrao + scilista_content)

        command = self.command
        logger.info(self.now + ' - inicio gerapadrao')
        logger.info(command)
        logger.info(scilista_content)
        os.system(command)
        logger.info(self.now + ' - fim gerapadrao')

    def _update_web_site(self, scilista_content):
        if self.config.is_enabled_transference:
            logger.info(self.now + ' - inicio transf bases')
            transfer = filestransfer.SciELOWebFilesTransfer(self.config)
            transfer.transfer_website_bases()
            logger.info(self.now + ' - fim transf bases')

        if self.mailer is not None:
            self.mailer.send_message(
                self.config.email_to,
                self.config.email_subject_website_update.replace(
                    'Gerapadrao',
                    'Gerapadrao ' + self.now + ' '),
                self.config.email_text_website_update + scilista_content)

    def mail_gerapadrao_is_busy(self):
        print('gerapadrao is running. Wait ...')
        if self.mailer:
            msg = []
            if os.path.isfile(self.config.gerapadrao_scilista):
                msg.append(
                    'Running:\n' + fs_utils.read_file(
                        self.config.gerapadrao_scilista)+'\n\n')
            if os.path.isfile(self.config.collection_scilista):
                msg.append(
                    'Waiting:\n' + sort_scilista(
                        fs_utils.read_file(self.config.collection_scilista)))

            if len(msg) > 0:
                self.mailer.send_message(
                    self.config.email_to_adm,
                    'gerapadrao is busy',
                    ''.join(msg))
