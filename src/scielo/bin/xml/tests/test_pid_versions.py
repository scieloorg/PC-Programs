import unittest

from app_modules.app.data.kernel_document import (
    PIDVersionsManager,
    PIDVersionsDB,
)


class TestPIDVersionsManager(unittest.TestCase):

    def setUp(self):
        self.pid_manager = PIDVersionsManager(PIDVersionsDB("/tmp/db.db"))

    def test_get_pid_v3_returns_pid_v3(self):
        self.pid_manager.insert("pid2", "pid3")
        self.assertEqual("pid3", self.pid_manager.get_pid_v3("pid2"))

    def test_get_pid_v3_returns_none(self):
        self.assertEqual(None, self.pid_manager.get_pid_v3("PID2"))

    def tearDown(self):
        self.pid_manager.disconnect()
