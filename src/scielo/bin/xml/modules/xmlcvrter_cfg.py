# coding=utf-8
import os


CURRENT_PATH = os.path.dirname(__file__).replace('\\', '/')


class XMLConverterConfiguration(object):

    def __init__(self, filename):
        self._data = {}
        for item in open(filename, 'r').readlines():
            s = item.strip()
            if '=' in s:
                if ',' in s:
                    s = s[0:s.rfind(',')]
                key, value = s.split('=')
                value = value.replace('\\', '/').strip()
                if value == '':
                    self._data[key] = None
                else:
                    self._data[key] = value
                if 'PATH' in key:
                    if not os.path.isdir(value):
                        os.makedirs(value)

    def data(self, key):
        return self._data.get(key)

    @property
    def cisis1030(self):
        return self._data.get('PATH_CISIS', CURRENT_PATH + '/../../cfg/')

    @property
    def cisis1660(self):
        return self._data.get('PATH_CISIS', CURRENT_PATH + '/../../cfg/cisis1660/')

    @property
    def website_folders_path(self):
        path = self._data.get('WEBSITE_FOLDERS_PATH', self._data.get('SCI_LISTA_SITE'))
        if path is not None:
            path = path.replace('\\', '/')
            if '/proc/' in path:
                path = path[0:path.find('/proc/')]
        return path

    @property
    def serial_path(self):
        return self._data.get('PROC_SERIAL_PATH', self._data.get('Serial Directory'))

    @property
    def issue_db(self):
        return self._data.get('SOURCE_ISSUE_DB', self._data.get('Issue Database'))

    @property
    def issue_db_copy(self):
        copy = self._data.get('Issue Database')
        if copy is not None:
            copy = copy.replace('/issue/', '/issue.tmp/')
        return self._data.get('ISSUE_DB_COPY', copy)

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
        if not os.path.isdir(self.website_folders_path):
            print('WARNING: Unable to find ' + self.website_folders_path)
        if not os.path.isdir(self.serial_path):
            r = False
            print('ERROR: Unable to find ' + self.serial_path)
        return r
