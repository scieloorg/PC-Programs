import sqlite3
import os


class DBManager:

    def __init__(self, dbname=None):
        if dbname is None:
            dbname = 'doi.db'
        self.dbname = dbname
        if not os.path.isfile(self.dbname):
            self.create_table()

    def execute_commit_close(self, command):
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        try:
        	c.execute(command)
        except:
        	print(command)
        conn.commit()
        conn.close()

    def create_table(self):
        #pid, doi, authors, issns, year
        self.execute_commit_close('''CREATE TABLE article (id integer primary key, pid text, doi text, authors text, issns text, year text, validated text, deposited_date text)''')

    def query(self, id=None, pid=None, doi=None, year=None, deposited_date=None, validated=None):
        fields = {'id':id, 'pid': pid, 'doi': doi, 'year':year, 'deposited_date':deposited_date, 'validated':validated}
        expr = [name + '="' + value + '"' for name, value in fields.items() if value is not None]
        expr = ' AND '.join(expr)
        if len(expr) > 0:
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()
            c.execute('SELECT * FROM article WHERE ' + expr)
            return c.fetchall()

    def update(self, id, pid=None, doi=None, authors=None, issns=None, year=None, deposited_date=None, validated=None):
        dados = {'pid': pid, 'doi': doi, 'authors':authors, 'issns':issns, 'year':year, 'deposited_date':deposited_date, 'validated':validated}
        op = []
        for k, v in dados.items():
            if v is None:
                v = ''
            op.append(k+'="'+v+'"')
        if len(op) > 0:
            op = ', '.join(op)
            execution = '''UPDATE article SET {fields} WHERE id={id}'''.format(fields=op, id=id)
            self.execute_commit_close(execution)

    def insert(self, pid=None, doi=None, authors=None, issns=None, year=None, deposited_date=None, validated=None):
        names = ['pid', 'doi', 'authors', 'issns', 'year', 'validated', 'deposited_date']
        dados = {'pid': pid, 'doi': doi, 'authors':authors, 'issns':issns, 'year':year, 'deposited_date':deposited_date, 'validated':validated}
        values = []
        for k in names:
            v = dados.get(k, '')
            if v is None:
                v = ''
            values.append(v)

        if len(values) > 0:
            values = tuple(values)
            execution = '''INSERT INTO article (pid, doi, authors, issns, year, validated, deposited_date) VALUES {values}'''.format(values=values)
            self.execute_commit_close(execution)
