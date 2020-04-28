from unittest import TestCase

from app_modules.generics.dbm.dbm_isis import IDFile


class TestIDFile(TestCase):

    def setUp(self):
        self.idfile = IDFile()

    def test__format_id(self):
        result = self.idfile._format_id(390)
        self.assertEqual(result, "!ID 000390\n")

    def test__format_id_raise_index_error(self):
        self.assertRaises(
            IndexError,
            self.idfile._format_id,
            9999999
        )
