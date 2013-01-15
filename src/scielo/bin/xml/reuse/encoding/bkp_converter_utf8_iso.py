from unicodedata import normalize

# python2.x
#
# utf8_pa='pá'
# iso_pa = utf8_pa.decode('utf-8').encode('iso-8859-1')
#
# python3.x
# iso_pa = utf8_pa.encode('iso-8859-1')
#
class ConverterUTF8_ISO:
    def __init__(self):
        pass 

    def utf8_2_iso(self, utf8):
        utf8 = utf8.replace('\ufeff','')
        try:
            #print('try sentence')
            if utf8.encode('iso-8859-1') == utf8.encode('utf-8'):
                iso = utf8
            else:
                iso = self.utf8_2_iso_by_words(utf8)
        except: 
            #print('except sentence')
            iso = self.utf8_2_iso_by_words(utf8)
        return iso

    def utf8_2_iso_by_words(self, sentence):
        words = sentence.split(' ')
        new = []
        for w in words:
            new.append(self.utf8_2_iso_by_word(w))
        return ' '.join(new)


    def utf8_2_iso_by_word(self, word):
        try:
            #print('try by word')
            if word.encode('iso-8859-1') == word.encode('utf-8'):
                iso = word
            else:
                iso = self.utf8_2_iso_by_characters(word)
        except:
            #print('except by word')
            iso = self.utf8_2_iso_by_characters(word)
        return iso
    def utf8_2_iso_by_characters(self, word):
        new = []
        for c in word:
            new.append(self.utf8_2_iso_by_character(c))
        return ''.join(new)

    def utf8_2_iso_by_character(self, c):
        try:
            #print('try by char')
            if c.encode('iso-8859-1') == c.encode('utf-8'):
                iso = c
            else:
                iso = self.utf8_2_ent(c)
        except:
            #print('except by char')
            iso = self.utf8_2_ent(c)
        return iso

    def utf8_2_ent(self, c):
        try:
            #print('try ord')
            n = ord(c)
            i = '&#' + str(n) + ';'
        except:
            #print('except ord')
            try:
                #print('try num ent')
                n = 256*ord(c[0]) + ord(c[1])

                i = '&#' + str(hex(n)) + ';'
            except:
                #print('except num ent')
                i = '?'
        return i
        

    