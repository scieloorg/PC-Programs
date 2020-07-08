from unittest import TestCase
from prodtools.config.config import get_data


scielo_collection = """
CODED_FORMULA_REQUIRED=on
CODED_TABLE_REQUIRED=on
BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA=off
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
