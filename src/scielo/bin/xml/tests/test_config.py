from unittest import TestCase
from unittest.mock import patch
from prodtools.config.config import (
    get_data,
    Configuration
)


scielo_collection = """
CODED_FORMULA_REQUIRED=on
CODED_TABLE_REQUIRED=on
BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA=off
"""

scielo_env = """
PROXY_ADDRESS=123.456.789:1234
ENABLED_WEB_ACCESS=off
XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER=packtools|java
"""

scielo_paths = """
;
package_version=4.0
; Arquivo de configuração dos caminhos
; SGML Parser
SGML Parser Program Directory=c:\\programas\\scielo\\bin\\sgmlpars\\,required
SGML Parser Program=c:\\programas\\scielo\\bin\\sgmlpars\\parser.exe,required
"""


class TestConfig(TestCase):

    def test_get_data_returns_dict(self):
        result = get_data(scielo_collection)
        expected = {
            "CODED_FORMULA_REQUIRED": "on",
            "CODED_TABLE_REQUIRED": "on",
            "BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA": "off",
        }
        self.assertEqual(expected, result)

    def test_get_data_returns_empty_dict(self):
        result = get_data(None)
        expected = {}
        self.assertEqual(expected, result)

    def test_get_data_handles_odd_ini_content_and_returns_dict(self):
        result = get_data(scielo_paths)
        expected = {
            "package_version": "4.0",
            "SGML Parser Program Directory": "c:\\programas\\scielo\\bin\\sgmlpars\\",
            "SGML Parser Program": "c:\\programas\\scielo\\bin\\sgmlpars\\parser.exe",
        }
        self.assertEqual(expected, result)


class TestConfiguration(TestCase):

    @patch("prodtools.config.config.get_configuration_filename")
    @patch("prodtools.config.config.fs_utils.read_file")
    def test_init_updates_data_with_config_files_content(self, mock_read_file,
            mock_get_configuration_filename):
        # para garantir que executará read_file 3 vezes
        mock_get_configuration_filename.return_value = "scielo_paths.ini"
        mock_read_file.side_effect = [
            scielo_paths,
            scielo_collection,
            scielo_env,
        ]
        c = Configuration()
        result = c._data
        expected = {
            "package_version": "4.0",
            "SGML Parser Program Directory": "c:\\programas\\scielo\\bin\\sgmlpars\\",
            "SGML Parser Program": "c:\\programas\\scielo\\bin\\sgmlpars\\parser.exe",
            "CODED_FORMULA_REQUIRED": "on",
            "CODED_TABLE_REQUIRED": "on",
            "BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA": "off",
            "PROXY_ADDRESS": "123.456.789:1234",
            "ENABLED_WEB_ACCESS": "off",
            "XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER": "packtools|java",
        }
        self.assertEqual(expected, result)
