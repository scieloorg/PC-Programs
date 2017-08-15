# coding=utf-8

from ...generics import remote_server


class FilesTransfer(object):

    def __init__(self, config, log_filename=None):
        self.config = config
        self.servers = [remote_server.RemoteServer(server, self.config.user, log_filename) for server in self.config.transference_servers]

    def transfer_files(self, acron, issue_id, folders):
        if self.config.is_enabled_transference:
            issue_id_path = acron + '/' + issue_id
            for folder in folders:
                dest_path = self.config.remote_web_app_path + folder + issue_id_path
                source_path = self.config.local_web_app_path + folder + issue_id_path
                for server in self.servers:
                    server.run_remote_mkdirs(dest_path)
                    server.run_rsync(source_path, dest_path)

    def transfer_website_files(self, acron, issue_id):
        folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']
        self.transfer_files(acron, issue_id, folders)

    def transfer_report_files(self, acron, issue_id):
        folders = ['/htdocs/reports/']
        self.transfer_files(acron, issue_id, folders)
