# coding=utf-8

from ...generics import remote_server


class FilesTransfer(object):

    def __init__(self, config, _logger=None):
        self.config = config
        if self.config.is_enabled_transference:
            self.servers = [remote_server.RemoteServer(server, self.config.transference_user, _logger) for server in self.config.transference_servers]

    def transfer_files(self, acron, issue_id, folders):
        if self.config.is_enabled_transference:
            issue_id_path = acron + '/' + issue_id
            for server in self.servers:
                for folder in folders:
                    dest_path = self.config.remote_web_app_path + folder + issue_id_path
                    source_path = self.config.local_web_app_path + folder + issue_id_path
                    server.run_remote_mkdirs(dest_path)
                    server.run_rsync(source_path, dest_path)

    def transfer_website_files(self, acron, issue_id):
        folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']
        self.transfer_files(acron, issue_id, folders)

    def transfer_report_files(self, acron, issue_id):
        folders = ['/htdocs/reports/']
        self.transfer_files(acron, issue_id, folders)

    def transfer_website_bases(self):
        if self.config.is_enabled_transference:
            dest_path = self.config.remote_web_app_path + '/bases/'
            folders = ['artigo', 'issue', 'newissue', 'title']
            for server in self.servers:
                server.run_remote_mkdirs(dest_path)
                for folder in folders:
                    source_path = self.config.local_web_app_path + '/bases/' + folder
                    server.run_scp(source_path, dest_path)
