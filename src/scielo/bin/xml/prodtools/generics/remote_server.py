# coding=utf-8

from prodtools.utils import system


class RemoteServer(object):

    def __init__(self, server, user, _logger=None):
        self.server = server
        self.user = user
        self.logger = _logger
        self.port = None
        if ':' in server:
            self.server, self.port = server.split(':')

    def run_cmd(self, cmd):
        if self.logger is not None:
            self.logger.info(cmd)
        try:
            system.run_command(cmd)
            if self.logger is not None:
                self.logger.info('done')
        except:
            if self.logger is not None:
                self.logger.error('failure')

    @property
    def rsync_port_param(self):
        return '' if self.port is None else ' -e "ssh -p {}" '.format(self.port)

    @property
    def scp_port_param(self):
        return '' if self.port is None else ' -P {} '.format(self.port)

    @property
    def ssh_port_param(self):
        return '' if self.port is None else ' -p {} '.format(self.port)

    def run_remote_mkdirs(self, path):
        cmd = 'ssh ' + self.user + '@' + self.server + self.ssh_port_param + ' "mkdir -p ' + path + '"'
        self.run_cmd(cmd)

    def run_rsync(self, source, dest):
        cmd = 'nohup rsync ' + self.rsync_port_param + '-CrvK ' + source + '/* ' + self.user + '@' + self.server + ':' + dest + '&\n'
        self.run_cmd(cmd)

    def run_scp(self, source, dest):
        cmd = 'nohup scp ' + self.scp_port_param + '-r ' + source + ' ' + self.user + '@' + self.server + ':' + dest + '&\n'
        self.run_cmd(cmd)
