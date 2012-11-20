import os
from datetime import date, datetime

class Tracker:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

    @property
    def daily(self):
        return date.today().isoformat()[0:7]

    def register(self, name, status, frequency = 'daily'):
        suffix = ''
        if frequency == 'daily':
            suffix = '-' + self.daily
        f = open(self.filename  + suffix + '.log', 'a+')
        f.write(datetime.now().isoformat() + '|' + name +  '|' + status)
        f.close()
