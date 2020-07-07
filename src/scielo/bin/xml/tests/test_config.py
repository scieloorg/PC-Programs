from unittest import TestCase
from unittest.mock import patch
from prodtools.config.config import Configuration


class TestConfiguration(TestCase):

    def setUp(self):
        pass

    @patch("prodtools.config.config.Configuration.load")
    @patch("prodtools.config.config.os.path.isfile")
    @patch("prodtools.config.config.fs_utils.read_file")
    @patch("prodtools.config.config.os.path.join")
    def test_read_files_returns_valid_value_for_last_variable_of_a_config_file(
            self, mock_join, mock_read_file, mock_is_file, mock_load):
        mock_is_file.return_value = True
        mock_join.side_effect = ['path1', 'path2']
        mock_read_file.side_effect = [
            'var1=valor1',
            'var2=valor2',
            'var3=valor3'
        ]
        config = Configuration('scielo_paths.ini')
        result = config.read_files()
        expected = "var1=valor1\nvar2=valor2\nvar3=valor3"
        self.assertEqual(expected, result)


