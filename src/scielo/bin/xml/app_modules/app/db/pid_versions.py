import sqlite3
import logging

CREATE_PID_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS pid_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        v2 VARCHAR(23) UNIQUE,
        v3 VARCHAR(255) UNIQUE
    );
"""


class PIDVersionsManager:
    def __init__(self, db):
        self.db = db
        self.db.cursor.execute(CREATE_PID_TABLE_QUERY)

    def register(self, v2, v3):
        return self.db.insert("INSERT INTO pid_versions (v2, v3) VALUES (?,?)", (v2, v3,))

    def get_pid_v3(self, v2):
        return self.db.get_pid_v3(v2)

    def pids_already_registered(self, v2, v3):
        """Verifica se a chave composta (v2 e v3) existe no banco de dadoss"""
        result = self.db.fetch(
            "SELECT COUNT(*) FROM pid_versions WHERE v2 = ? and v3 = ?", (v2, v3,)
        )
        return result[0][0] == 1

    def close(self):
        self.db.close()


class PIDVersionsDB:
    def __init__(self, name):
        self.conn = None
        self.cursor = None
        self.open(name)

    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            logging.exception(e)
            raise sqlite3.OperationalError("unable to open database '%s'" % name)

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, excution_type, excution_value, traceback):

        if isinstance(excution_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()

        self.close()

    def fetch(self, sql, parameters=None):
        self.cursor.execute(sql, parameters)
        return self.cursor.fetchall()

    def insert(self, sql, parameters):
        try:
            self.cursor.execute(sql, parameters)
        except sqlite3.IntegrityError as e:
            logging.error("this item already exists in database")
            return False
        else:
            self.conn.commit()
            return True

    def get_pid_v3(self, v2):
        found = self.fetch("SELECT v3 FROM pid_versions WHERE v2 = ?", (v2,))

        if found is not None and len(found) > 0:
            return found[0][0]
