# coding=utf-8

import logging

from ..useful import system


class FilesTransfer(object):

    def __init__(self, config, log_filename=None):
        self.config = config
        self.log_filename = log_filename
        if log_filename is not None:
            logging.basicConfig(log_filename, format='%(asctime)s %(message)s')

    def transfer_website_files(self, acron, issue_id):
        if self.config.is_enabled_transference:
            issue_id_path = acron + '/' + issue_id
            folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']
            for folder in folders:
                dest_path = self.config.remote_web_app_path + folder + issue_id_path
                source_path = self.config.local_web_app_path + folder + issue_id_path
                for server in self.config.transference_servers:
                    self.run_remote_mkdirs(server, dest_path)
                    self.run_rsync(source_path, server, dest_path)

    def transfer_report_files(self, acron, issue_id):
        # 'rsync -CrvK img/* self.config.user@server:/var/www/...../revistas'
        if self.config.is_enabled_transference:
            issue_id_path = acron + '/' + issue_id
            folders = ['/htdocs/reports/']
            for folder in folders:
                dest_path = self.config.remote_web_app_path + folder + issue_id_path
                source_path = self.config.local_web_app_path + folder + issue_id_path
                log_filename = './transfer_report_' + issue_id_path.replace('/', '-') + '.log'
                for server in self.config.transference_servers:
                    self.run_remote_mkdirs(server, dest_path, log_filename)
                    self.run_rsync(source_path, server, dest_path, log_filename)

    def run_cmd(self, cmd):
        if self.log_filename is not None:
            logging.info(cmd)
        try:
            system.run_command(cmd)
            if self.log_filename is not None:
                logging.info('done')
        except:
            if self.log_filename is not None:
                logging.error('failure')

    def run_remote_mkdirs(self, server, path):
        cmd = 'ssh ' + self.config.user + '@' + server + ' "mkdir -p ' + path + '"'
        self.run_cmd(cmd)

    def run_rsync(self, source, server, dest):
        cmd = 'nohup rsync -CrvK ' + source + '/* ' + self.config.user + '@' + server + ':' + dest + '&\n'
        self.run_cmd(cmd)

    def run_scp(self, source, server, dest):
        cmd = 'nohup scp -r ' + source + ' ' + self.config.user + '@' + server + ':' + dest + '&\n'
        self.run_cmd(cmd)
