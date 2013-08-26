import hashlib


def id_generate(s=None):
    if s is None:
        from datetime import datetime
        s = datetime.now().isoformat()
    return hashlib.md5(s).hexdigest()


class Items(object):
    def __init__(self):
        super(Items, self).__init__()
        self.elements = {}

    def find(self, item):
        return self.elements.get(self.key(item), None)

    def insert(self, item, replace):
        r = self.find(item)
        if r is None or replace:
            if self.key(item):
                self.elements[self.key(item)] = item

    def key(self, item):
        return ''

    @property
    def count(self):
        return len(self.elements)

    def __iter__(self):
        for k, item in self.elements.items():
            yield item
