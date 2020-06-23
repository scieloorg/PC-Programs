from unittest import TestCase
from prodtools.processing import xml_versions


class TestSPSNumbers(TestCase):

    def test_sps_numbers_returns_a_tuple_1_8_1_for_sps_1_8_1(self):
        result = xml_versions.sps_numbers("sps-1.8.1")
        self.assertEqual((1, 8, 1), result)

    def test_sps_numbers_returns_a_tuple_1_10_for_sps_1_10(self):
        result = xml_versions.sps_numbers("sps-1.10")
        self.assertEqual((1, 10), result)

    def test_sps_numbers_returns_a_tuple_1_1_for_sps_1_1(self):
        result = xml_versions.sps_numbers("sps-1.1")
        self.assertEqual((1, 1), result)

    def test_sps_numbers_returns_a_tuple_1_10_for_1_10(self):
        result = xml_versions.sps_numbers("1.10")
        self.assertEqual((1, 10), result)

    def test_sps_numbers_returns_a_tuple_1_1_for_1_1(self):
        result = xml_versions.sps_numbers("1.1")
        self.assertEqual((1, 1), result)

    def test_sps_numbers_returns_a_tuple_0_0_for_none(self):
        result = xml_versions.sps_numbers(None)
        self.assertEqual((0, 0), result)
