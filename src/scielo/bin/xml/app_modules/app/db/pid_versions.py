import sqlite3


class PIDVersionsManager:

    def __init__(self, db):
        self.db = db

    def insert(self, v2, v3):
        self.db.insert(v2, v3)

    def get_pid_v3(self, v2):
        return self.db.get_pid_v3(v2)


class PIDVersionsBD:

    def __init__(self, db_name):
        self.db_name = db_name
        self._connection = None
        self._cursor = None
        self._is_table_created = None

    @property
    def conn(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_name)
        return self._connection

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    @property
    def is_table_created(self):
        if self._is_table_created is None:
            self._is_table_created = self.create_table()
        return self._is_table_created

    def _execute(self, command, parameters=None):
        if self._is_table_created:
            if parameters:
                self.cursor.execute(command, parameters)
            else:
                self.cursor.execute(command)
            if command.startswith("SELECT"):
                return self.cursor.fetchone()
            else:
                self.conn.commit()
                self.conn.close()
                return True

    def create_table(self):
        return self._execute(
            """CREATE TABLE IF NOT EXISTS pid_versions (v2 varchar(23) unique, v3 varchar(255) unique)"""
        )

    def insert(self, v2, v3):
        return self._execute(
            """INSERT INTO pid_versions VALUES ('?','?')""", (v2, v3)
        )

    def get_pid_v3(self, v2):
        expr = (v2, )
        found = self._execute(
            """SELECT v3 FROM pid_versions WHERE v2 = ?""", expr)
        if found:
            return found[0]
