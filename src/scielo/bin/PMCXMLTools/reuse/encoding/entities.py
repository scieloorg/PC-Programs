

class Entities:
    def __init__(self):
        pass
        
        

    def replace_to_numeric_entities(self, content):
        if type(content) == type(''):
            content = content.encode('ascii', 'xmlcharrefreplace')
        else:
            content = content.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
        return content        

    


