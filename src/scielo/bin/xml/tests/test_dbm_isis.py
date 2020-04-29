# coding=utf-8

from unittest import TestCase, skipIf
from unittest.mock import patch
import sys

from app_modules.generics.dbm.dbm_isis import IDFile
from app_modules.generics import fs_utils


python_version = sys.version_info.major


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

    def test__format_record(self):
        record = {
            "4": [{"x": "&#91;", "3": "subcampo 4b1"},
                  {"x": "subcxmpo 4x2", "3": "&ccedil;"},
                  {"x": "x ^ y"},
                  ],
            "5": "x ^ y",
            "6": "&ccedil;",
            "77": "&#91;",
            "1": "Dado do campo É 1",
            "2": ["x ^ y", "&#91;", "&ccedil;"],
            "3": {"_": "sem subcampo", "b": "subcampo 3b", "a": "subcampo 3a"},
            "9999": "",
        }
        expected = (
            "!v001!Dado do campo É 1\n"
            "!v002!x [PRESERVECIRC] y\n"
            "!v002!&#91;\n"
            "!v002!&ccedil;\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x&#91;\n"
            "!v004!^3&ccedil;^xsubcxmpo 4x2\n"
            "!v004!^xx [PRESERVECIRC] y\n"
            "!v005!x [PRESERVECIRC] y\n"
            "!v006!&ccedil;\n"
            "!v077!&#91;\n"
        )
        result = self.idfile._format_record(record)
        self.assertEqual(result, expected)

    def test_tag_data_returns_list(self):
        data = [{"x": "&#91;", "3": "subcampo 4b1"},
                {"x": "subcxmpo 4x2", "3": "&ccedil;"},
                "x ^ y",
                ""
                ]
        expected = [
            "!v004!^3subcampo 4b1^x&#91;\n",
            "!v004!^3&ccedil;^xsubcxmpo 4x2\n",
            "!v004!x [PRESERVECIRC] y\n",
            ""
        ]

        result = self.idfile._tag_data("4", data)
        self.assertEqual(result, expected)

    def test_tag_occ_returns_subfields(self):
        data = {"x": "&#91;", "3": "subcampo 4b1"}
        expected = "!v004!^3subcampo 4b1^x&#91;\n"
        result = self.idfile._tag_occ("4", data)
        self.assertEqual(result, expected)

    def test_tag_occ_returns_field(self):
        data = "texto"
        expected = "!v004!texto\n"
        result = self.idfile._tag_occ("4", data)
        self.assertEqual(result, expected)

    def test_tag_occ_raises_error(self):
        data = [1111]
        self.assertRaises(
            TypeError,
            self.idfile._tag_occ,
            "4", data
        )

    @skipIf(python_version < 3, "only apply for python >= 3")
    @patch("app_modules.generics.dbm.dbm_isis.fs_utils.write_file")
    def test_write_calls_write_file_with_expected_parameters(self, mock_write):
        file_path = "/tmp/isso_eh_teste.id"
        record = {
            "4": [{"x": "&#91;", "3": "subcampo 4b1"},
                  {"x": "subcxmpo 4x2", "3": "&ccedil;"},
                  {"x": "x ^ y"},
                  ],
            "5": "x ^ y",
            "6": "&ccedil;",
            "77": "&#91;",
            "1": "磨",
            "2": ["x ^ y", "&#91;", "&ccedil;"],
            "3": {"_": "sem subcampo", "b": "subcampo 3b", "a": "subcampo 3a"},
            "9999": "",
        }
        data = (
            "!ID 000001\n"
            "!v001!&#30952;\n"
            "!v002!x &#94; y\n"
            "!v002![\n"
            "!v002!ç\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x[\n"
            "!v004!^3ç^xsubcxmpo 4x2\n"
            "!v004!^xx &#94; y\n"
            "!v005!x &#94; y\n"
            "!v006!ç\n"
            "!v077![\n"
        )
        records = [record]
        self.idfile.write(file_path, records)
        mock_write.assert_called_once_with(file_path, data, "iso-8859-1")

    @skipIf(python_version < 3, "only apply for python >= 3")
    def test_write(self):
        file_path = "/tmp/isso_eh_teste.id"
        record = {
            "4": [{"x": "&#91;", "3": "subcampo 4b1"},
                  {"x": "subcxmpo 4x2", "3": "&ccedil;"},
                  {"x": "x ^ y"},
                  ],
            "5": "x ^ y",
            "6": "&ccedil;",
            "77": "&#91;",
            "1": "磨",
            "2": ["x ^ y", "&#91;", "&ccedil;"],
            "3": {"_": "sem subcampo", "b": "subcampo 3b", "a": "subcampo 3a"},
            "9999": "",
        }
        data = (
            "!ID 000001\n"
            "!v001!&#30952;\n"
            "!v002!x &#94; y\n"
            "!v002![\n"
            "!v002!ç\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x[\n"
            "!v004!^3ç^xsubcxmpo 4x2\n"
            "!v004!^xx &#94; y\n"
            "!v005!x &#94; y\n"
            "!v006!ç\n"
            "!v077![\n"
        )
        records = [record]
        self.idfile.write(file_path, records)
        x = fs_utils.read_file(file_path, "iso-8859-1")
        self.assertEqual(x, data)

    @skipIf(not python_version < 3, "only apply for python < 3")
    def test_write_python2(self):
        file_path = "/tmp/isso_eh_teste.id"
        record = {
            "4": [{"x": "&#91;", "3": "subcampo 4b1"},
                  {"x": "subcxmpo 4x2", "3": "&ccedil;"},
                  {"x": "x ^ y"},
                  ],
            "5": "x ^ y",
            "6": "&ccedil;",
            "77": "&#91;",
            "1": u"磨",
            "2": ["x ^ y", "&#91;", "&ccedil;"],
            "3": {"_": "sem subcampo", "b": "subcampo 3b", "a": "subcampo 3a"},
            "9999": "",
        }
        data = (
            "!ID 000001\n"
            "!v001!&#30952;\n"
            "!v002!x &#94; y\n"
            "!v002![\n"
            "!v002!ç\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x[\n"
            "!v004!^3ç^xsubcxmpo 4x2\n"
            "!v004!^xx &#94; y\n"
            "!v005!x &#94; y\n"
            "!v006!ç\n"
            "!v077![\n"
        )
        records = [record]
        self.idfile.write(file_path, records)
        x = fs_utils.read_file(file_path, "iso-8859-1")
        self.assertEqual(x, data)
