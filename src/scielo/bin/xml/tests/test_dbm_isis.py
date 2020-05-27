# coding=utf-8

from unittest import TestCase, skipIf
from unittest.mock import patch, mock_open
import sys

from prodtools.utils.dbm.dbm_isis import IDFile, CISIS
from prodtools.utils import fs_utils
from prodtools.utils.dbm import dbm_isis

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
    @patch("prodtools.utils.dbm.dbm_isis.fs_utils.write_file")
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
            "!v002!x \\^ y\n"
            "!v002![\n"
            "!v002!ç\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x[\n"
            "!v004!^3ç^xsubcxmpo 4x2\n"
            "!v004!^xx \\^ y\n"
            "!v005!x \\^ y\n"
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
            "!v002!x \\^ y\n"
            "!v002![\n"
            "!v002!ç\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x[\n"
            "!v004!^3ç^xsubcxmpo 4x2\n"
            "!v004!^xx \\^ y\n"
            "!v005!x \\^ y\n"
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
            "!v002!x \\^ y\n"
            "!v002![\n"
            "!v002!ç\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x[\n"
            "!v004!^3ç^xsubcxmpo 4x2\n"
            "!v004!^xx \\^ y\n"
            "!v005!x \\^ y\n"
            "!v006!ç\n"
            "!v077![\n"
        )
        records = [record]
        self.idfile.write(file_path, records)
        x = fs_utils.read_file(file_path, "iso-8859-1")
        self.assertEqual(x, data)

    @skipIf(python_version < 3, "only apply for python >= 3")
    @patch("prodtools.utils.dbm.dbm_isis.fs_utils.read_file")
    def test_read(self, mock_read_file):
        file_path = "db.id"
        mock_read_file.return_value = (
            "!ID 000001\n"
            "!v001!&#30952;\n"
            "!v002!x \\^ y\n"
            "!v002![\n"
            "!v002!ç\n"
            "!v003!sem subcampo^asubcampo 3a^bsubcampo 3b\n"
            "!v004!^3subcampo 4b1^x[\n"
            "!v004!^3ç^xsubcxmpo 4x2\n"
            "!v004!^xx \\^ y\n"
            "!v004!x \\^ y\n"
            "!v005!x \\^ y\n"
            "!v006!ç\n"
            "!v077![\n"
        )
        expected = [
            {
                "1": "磨",
                "2": ["x ^ y", "[", "ç"],
                "3": {"_": "sem subcampo",
                      "a": "subcampo 3a", "b": "subcampo 3b"},
                "4": [
                    {"3": "subcampo 4b1", "x": "["},
                    {"3": "ç", "x": "subcxmpo 4x2"},
                    {"x": "x ^ y"},
                    "x ^ y",
                ],
                "5": "x ^ y",
                "6": "ç",
                "77": "[",
            }
        ]
        records = self.idfile.read(file_path)
        print(records)
        self.assertEqual(records, expected)


class TestCISIS(TestCase):
    @patch("prodtools.utils.dbm.dbm_isis.os.path.exists", return_value=True)
    def setUp(self, mock_exists):
        self.cisis = CISIS("cisis")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_run_cmd(self, mock_getoutput):
        mock_getoutput.return_value = "any"
        self.cisis.run_cmd(
            "meucomando", "parametro1", "parametro2=valor", 'x y')
        mock_getoutput.assert_called_once_with(
            "cisis/meucomando parametro1 parametro2=valor x y")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_is_available(self, mock_getoutput):
        self.cisis.is_available
        mock_getoutput.assert_called_once_with("cisis/mx what")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_crunchmf(self, mock_getoutput):
        self.cisis.crunchmf("baselinux", "basewindows")
        mock_getoutput.assert_called_once_with(
            "cisis/crunchmf baselinux basewindows")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_id2i(self, mock_getoutput):
        self.cisis.id2i("base.id", "base")
        mock_getoutput.assert_called_once_with(
            "cisis/id2i base.id create=base")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_append(self, mock_getoutput):
        self.cisis.append("base", "base_resultante")
        mock_getoutput.assert_called_once_with(
            "cisis/mx base append=base_resultante now -all")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_create(self, mock_getoutput):
        self.cisis.create("base", "base_resultante")
        mock_getoutput.assert_called_once_with(
            "cisis/mx base create=base_resultante now -all")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_i2id(self, mock_getoutput):
        self.cisis.i2id("base", "basex.id")
        mock_getoutput.assert_called_once_with(
            "cisis/i2id base > basex.id")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_mst2iso(self, mock_getoutput):
        self.cisis.mst2iso("base", "basex.iso")
        mock_getoutput.assert_called_once_with(
            "cisis/mx base iso=basex.iso now -all")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_iso2mst(self, mock_getoutput):
        self.cisis.iso2mst("base.iso", "basex")
        mock_getoutput.assert_called_once_with(
            "cisis/mx iso=base.iso create=basex now -all")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_search(self, mock_getoutput):
        self.cisis.search("base", "procura", "base_resultado")
        mock_getoutput.assert_called_once_with(
            "cisis/mx btell=0 base \"bool=procura\" lw=999 "
            "append=base_resultado now -all")

    @patch("prodtools.utils.system.subprocess.getoutput")
    def test_generate_indexes(self, mock_getoutput):
        self.cisis.generate_indexes("base", "base.fst", "base_invertida")
        mock_getoutput.assert_called_once_with(
            "cisis/mx base fst=@base.fst fullinv=base_invertida")

    @patch("prodtools.utils.dbm.dbm_isis.system.run_command")
    @patch("prodtools.utils.dbm.dbm_isis.os.path.isfile", return_value=True)
    def test_is_readable(self, mock_isfile, mock_run_command):
        mock_run_command.return_value = "nxtmfn"
        self.cisis.is_readable("base")
        mock_run_command.assert_called_once_with("cisis/mx base +control now")
