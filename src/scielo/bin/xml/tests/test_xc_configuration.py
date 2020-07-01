import unittest

from prodtools.config.config import Configuration


class TestConfigurationOfXC(unittest.TestCase):
    def setUp(self):
        self.configuration = Configuration()
        self.configuration._data = {
            "EMAIL_SUBJECT_CONVERSION_FAILURE": "Conversion Failure"
        }

    def test_email_subject_conversion_failure_should_exists_if_config_has_the_related_key(
        self,
    ):
        self.assertIsNotNone(self.configuration.email_subject_conversion_failure)
        self.assertEqual(
            self.configuration.email_subject_conversion_failure, "Conversion Failure"
        )

    def test_email_subject_conversion_failure_returns_none_if_config_is_empty(self):
        self.configuration._data = {}
        self.assertIsNone(self.configuration.email_subject_conversion_failure)
