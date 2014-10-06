# coding=utf-8
import os

import isis


class Configuration(object):

    def __init__(self, filename):
        self.data = {}
        for item in open(filename, 'r').readlines():
            s = item.replace('\n', '').replace('\r', '')
            if not item.startswith(';'):
                if '=' in s:
                    temp = s.split('=')
                    self.data[temp[0]] = temp[1].replace('\\', '/')[0:temp[1].find(',')]

    @property
    def web_path(self):
        path = self.data.get('SCI_LISTA_SITE')
        if path is not None:
            path = path.replace('\\', '/')
            path = path[0:path.find('/proc/')]
        return path

    @property
    def serial_path(self):
        return self.data.get('Serial Directory')

    @property
    def issue_db(self):
        return self.data.get('Issue Database')

    @property
    def isis_dao(self):
        r = None
        curr_path = os.getcwd().replace('\\', '/')
        if os.path.isdir(curr_path + '/./../cfg/') and os.path.isdir(curr_path + '/./../cfg/cisis1660/'):
            r = isis.IsisDAO(isis.UCISIS(isis.CISIS(curr_path + '/./../cfg/'), isis.CISIS(curr_path + '/./../cfg/cisis1660/')))
        return r

    def valid(self):
        r = True
        if not isinstance(self.isis_dao, isis.IsisDAO):
            r = False
            print('ERROR: Unable to instanciate IsisDAO')
        if not os.path.isfile(self.issue_db + '.mst'):
            r = False
            print('ERROR: Unable to find ' + self.issue_db + '.mst')
        if not os.path.isdir(self.web_path):
            print('WARNING: Unable to find ' + self.web_path)
        if not os.path.isdir(self.serial_path):
            r = False
            print('ERROR: Unable to find ' + self.serial_path)
        return r

