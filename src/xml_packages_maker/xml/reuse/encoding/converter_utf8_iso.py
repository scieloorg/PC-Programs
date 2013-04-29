from unicodedata import normalize


class ConverterUTF8_ISO:
    def __init__(self):
        pass 

    def utf8_2_iso(self, utf8):
        u = utf8.decode('utf-8')
        try:
            iso = u.encode('iso-8859-1')
        except:
            iso = self.utf8_2_iso_by_words(utf8)
        return iso

    def utf8_2_iso_by_words(self, utf8):
        words = utf8.split(' ')
        new = []
        for w in words:
            new.append(self.utf8_2_iso_by_word(w))
        return ' '.join(new)


    def utf8_2_iso_by_word(self, utf8):
        u = utf8.decode('utf-8')
        try:
            iso = u.encode('iso-8859-1')
        except:
            iso = self.utf8_2_iso_by_characters(utf8)
        return iso



    def utf8_2_iso_by_characters(self, utf8):
        new = []
        for c in utf8:
            new.append(self.utf8_2_iso_by_character(c))
        return ''.join(new)

    def utf8_2_iso_by_character(self, utf8):
        
        try:
            u = utf8.decode('utf-8')
            iso = u.encode('iso-8859-1')
        except:
            iso = utf8
        return iso

    
        
