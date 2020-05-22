import os
import tempfile
import unittest
import sqlite3

from prodtools.db.pid_versions import PIDVersionsManager, PIDVersionsDB


class TestPIDVersionsManager(unittest.TestCase):
    def setUp(self):
        self.temporary_db = tempfile.mkstemp()[-1]
        self.manager = PIDVersionsManager(db=PIDVersionsDB(self.temporary_db))
        self.manager.register("pid-2", "pid-3")

    def tearDown(self):
        os.remove(self.temporary_db)

    def test_should_raise_exception_when_could_not_open_database_file(self):
        with self.assertRaises(sqlite3.OperationalError):
            fake_db_file = os.path.join(tempfile.gettempdir(), "fake-folder", "fake-file.db")
            PIDVersionsDB(fake_db_file)
            os.remove(fake_db_file)

    def test_should_insert_a_pair_of_pids(self):
        self.assertTrue(self.manager.register("random-v2", "random-v3"))

    def test_should_not_insert_duplicated_pids(self):
        self.assertFalse(self.manager.register("pid-2", "pid-3"))

    def test_should_retrieve_scielo_pid_v3_using_pid_v2(self):
        self.assertEqual(self.manager.get_pid_v3("pid-2"), "pid-3")

    def test_should_return_none_if_pid_v2_is_not_registered_yet(self):
        self.assertEqual(self.manager.get_pid_v3("does-not-exists"), None)

    def test_check_if_pids_already_registered_in_database(self):
        self.assertTrue(self.manager.pids_already_registered("pid-2", "pid-3"))
