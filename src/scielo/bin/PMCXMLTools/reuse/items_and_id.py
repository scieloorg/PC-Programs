import hashlib
def id_generate(s):
    return hashlib.md5(s).hexdigest()

class Items:
    def __init__(self):
        self.elements = {}
        
    def __iter__(self):
        for elem in self.elements.values():
            yield elem
        
    def count(self):
        return len(self.elements)

    def insert(self, item, replace):
        try:
            id = item.id
        except:
            id = id_generate( datetime.now().isoformat())
            item.id = id
        if id in self.elements.keys():
            if replace == True:
                self.elements[id] = item
        else:
            self.elements[id] = item
        return self.elements[id]
        

    def get(self, id):
        r = None
        if id in self.elements.keys():
            r = self.elements[id]
        return r