
class Author:
    def __init__(self):
        self.fields = {}

    def add(self, name, v):
        if name in self.fields.keys():
            pass
        else:
            self.fields[name] = []
        if v: self.fields[name] = v

    def set_author_id(self,  value):
        self.add('author_id',value)

    def get_author_id(self):
        return self.fields['author_id']

    def set_author_date(self,  value):
        self.add('author_date',value)

    def get_author_date(self):
        return self.fields['author_date']

    def set_author_loc(self,  value):
        self.add('author_loc',value)

    def get_author_loc(self):
        return self.fields['author_loc']

    def set_author_name(self,  value):
        self.add('author_name',value)

    def get_author_name(self):
        return self.fields['author_name']

    def set_author_num(self,  value):
        self.add('author_num',value)

    def get_author_num(self):
        return self.fields['author_num']

    def set_author_role(self,  value):
        self.add('author_role',value)

    def get_author_role(self):
        return self.fields['author_role']

    def set_author_title(self,  value):
        self.add('author_title',value)

    def get_author_title(self):
        return self.fields['author_title']

    def set_author_unit(self,  value):
        self.add('author_unit',value)

    def get_author_unit(self):
        return self.fields['author_unit']

