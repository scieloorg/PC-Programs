import os
from datetime import date, datetime

class Tracker:
    def __init__(self, path, filename):
        self.path = path
        self.name = filename
        self.filename = path + '/' + self.name
        if not os.path.exists(path):
            os.makedirs(path)

    @property
    def daily(self):
        return date.today().isoformat()[0:10]

    def register(self, name, status, frequency = 'daily'):
        suffix = ''
        if frequency == 'daily':
            suffix = '-' + self.daily
        f = open(self.filename  + suffix + '.log', 'a+')
        f.write(datetime.now().isoformat() + '|' + name +  '|' + status)
        f.close()
