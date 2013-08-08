# -*- coding: UTF-8 -*-

from unicodedata import normalize

class TableEntities:
    def __init__(self, filename='entities'):
        f = open(filename, 'rb')
        lines = f.readlines()
        f.close()

        self.table_number2char = {}
        self.table_char2number = {}
        self.table_noaccent = {}
        self.table_named2number = {}
        self.table_named2char = {}

        for line in lines:
            values = line.replace("\n", "").split('|')
            if len(values) != 5:
                print(line)
            else:
                char, number_ent, named_ent, ign2, no_accent = values

                if self.is_valid_char(char) and self.is_valid_named(named_ent):
                    entity_char = named_ent.replace('&', '').replace(';', '')
                    if self.table_char2number.get(char, None) is None:
                        self.table_char2number[char] = number_ent
                        self.table_noaccent[char] = no_accent

                    if not named_ent in self.table_named2number.keys():
                        self.table_named2number[named_ent] = number_ent

                        if char != entity_char:
                            self.table_named2char[named_ent] = char

                    if number_ent != '' and not number_ent in self.table_noaccent.keys():
                        if char != entity_char:
                            self.table_number2char[number_ent] = char
                        self.table_noaccent[number_ent] = no_accent

    def is_valid_char(self, char):
        r = False
        if char != '':
            if not char in ['>', '<', '&']:
                r = True
        return r

    def is_valid_named(self, named):
        r = False
        if named != '':
            if not named in ['&gt;', '&lt;', '&amp;']:
                r = True
        return r

    def number2char(self, content):
        for k, v in self.table_number2char.items():
            k2 = k.replace('&', '&amp;')
            content = content.replace(k2, v)
            content = content.replace(k, v)
        return content

    def name2number(self, content):
        for k, v in self.table_named2number.items():
            k2 = k.replace('&', '&amp;')
            content = content.replace(k2, v)
            content = content.replace(k, v)
        return content

    def name2char(self, content):
        for k, v in self.table_named2char.items():
            k2 = k.replace('&', '&amp;')
            content = content.replace(k2, v)
            content = content.replace(k, v)
        return content

