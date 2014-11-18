# coding=utf-8
import os


CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')


class XMLConverterConfiguration(object):

    def __init__(self, filename):
        self.data = {}
        for item in open(filename, 'r').readlines():
            s = item.replace('\n', '').replace('\r', '')
            if not item.startswith(';'):
                if '=' in s:
                    if ',' in s:
                        s = s[0:s.rfind(',')]
                    temp = s.split('=')
                    self.data[temp[0]] = temp[1].replace('\\', '/')

    @property
    def cisis1030(self):
        return self.data.get('PATH_CISIS_1030', CURRENT_PATH + '/../../cfg/')

    @property
    def cisis1660(self):
        return self.data.get('PATH_CISIS_1660', CURRENT_PATH + '/../../cfg/cisis1660/')

    @property
    def web_path(self):
        path = self.data.get('WEB_PATH', self.data.get('SCI_LISTA_SITE'))
        if path is not None:
            path = path.replace('\\', '/')
            if '/proc/' in path:
                path = path[0:path.find('/proc/')]
        return path

    @property
    def serial_path(self):
        return self.data.get('SERIAL_PATH', self.data.get('Serial Directory'))

    @property
    def issue_db(self):
        return self.data.get('ISSUE_DB', self.data.get('Issue Database'))

    @property
    def issue_db_copy(self):
        copy = self.data.get('Issue Database').replace('/issue/', '/issue.tmp/')
        return self.data.get('ISSUE_DB_COPY', copy)

    def valid(self):
        r = True
        if not os.path.isdir(self.cisis1030):
            r = False
            print('ERROR: Unable to find ' + self.cisis1030)
        if not os.path.isdir(self.cisis1660):
            r = False
            print('ERROR: Unable to find ' + self.cisis1660)
        if not os.path.isfile(self.issue_db + '.mst'):
            r = False
            print('ERROR: Unable to find ' + self.issue_db + '.mst')
        if not os.path.isdir(self.web_path):
            print('WARNING: Unable to find ' + self.web_path)
        if not os.path.isdir(self.serial_path):
            r = False
            print('ERROR: Unable to find ' + self.serial_path)
        return r
