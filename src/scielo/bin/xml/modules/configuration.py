# coding=utf-8


class Configuration(object):

    def __init__(self, data={}):
        self.data = data

    def read(self, filename):
        f = open(filename, 'r')
        for item in f.readlines():
            s = item.replace('\n', '').replace('\r', '')
            if not item.startswith(';'):
                if '=' in s:
                    temp = s.split('=')
                    self.data[temp[0]] = temp[1].replace('\\', '/')[0:temp[1].find(',')]
        f.close()
