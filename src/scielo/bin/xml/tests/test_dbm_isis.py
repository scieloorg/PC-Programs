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

        result = self.idfile.tag_data("4", data)
        self.assertEqual(result, expected)
