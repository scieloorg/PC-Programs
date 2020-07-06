from unittest import TestCase
from unittest.mock import Mock, patch


from prodtools.db.xc_models import IssueAndTitleManager

ISSUE_RECORD = {
    '30': 'Food Sci. Technol',
    '31': '40',
    '35': '0101-2061',
    '36': '20205',
    '42': '1',
    '43': [
        {'a': '2020', 'c': 'Campinas', 'l': 'es', 'm': 'jun.', 's': 'supl.1',
         't': 'Food Sci. Technol', 'v': 'vol.40'},
        {'a': '2020', 'c': 'Campinas', 'l': 'pt', 'm': 'jun.', 's': 'supl.1',
         't': 'Food Sci. Technol', 'v': 'vol.40'},
        {'a': '2020', 'c': 'Campinas', 'l': 'en', 'm': 'June', 's': 'supl.1',
         't': 'Food Sci. Technol', 'v': 'vol.40'}],
    '48': [
        {'h': 'Sumario', 'l': 'es'},
        {'h': 'Sumário', 'l': 'pt'},
        {'h': 'Table of Contents', 'l': 'en'}],
    '49': [{'c': 'CTA090', 'l': 'pt', 't': 'Artigo Original'},
           {'c': 'CTA090', 'l': 'en', 't': 'Original Article'},
           {'c': 'CTA100', 'l': 'pt', 't': 'Artigo de Revisão'},
           {'c': 'CTA100', 'l': 'en', 't': 'Review Article'}],
    '65': '20200600',
    '85': 'nd',
    '91': '20200624',
    '117': 'other',
    '122': '50',
    '130': 'Food Science and Technology',
    '132': '1',
    '151': 'Food Sci. Technol',
    '200': '0',
    '230': 'Ciência e Tecnologia de Alimentos',
    '435': [{'_': '0101-2061', 't': 'PRINT'},
            {'_': '1678-457X', 't': 'ONLIN'}],
    '480': 'Sociedade Brasileira de Ciência e Tecnologia de Alimentos',
    '541': 'BY',
    '700': '0',
    '701': '1',
    '706': 'i',
    '930': 'CTA',
    '935': '1678-457X',
    '991': '1',
}


class TestIssueAndTitleManager(TestCase):

    def setUp(self):
        self.manager = IssueAndTitleManager(
            Mock(),
            ['base', 'base2', 'base.fst'],
            ['base', 'base2', 'base.fst'],
            Mock())

    def test_get_registered_issue_data_returns_unidentified_issue(self):
        issue_label = None
        p_issn = None
        e_issn = None
        acron_issue_label = 'unidentified issue'
        issue_models = None

        expected = acron_issue_label, issue_models, ''
        result = self.manager.get_registered_issue_data(
            issue_label, p_issn, e_issn)
        self.assertEqual(expected[:2], result[:2])
        self.assertIsNotNone(result[2])

    @patch("prodtools.db.xc_models.IssueAndTitleManager.find_i_record")
    def test_get_registered_issue_data_returns_not_registered_issue(
            self, mock_find_i_record):
        issue_label = "v1n1"
        p_issn = "1234-5678"
        e_issn = "5678-1234"
        mock_find_i_record.return_value = None

        result = self.manager.get_registered_issue_data(
            issue_label, p_issn, e_issn)
        res_acron_issue_label, res_issue_models, res_msg = result
        self.assertEqual('not_registered issue', res_acron_issue_label)
        self.assertEqual(None, res_issue_models)
        self.assertIn(p_issn, res_msg)
        self.assertIn(e_issn, res_msg)
        self.assertIn(issue_label, res_msg)

    @patch("prodtools.db.xc_models.IssueAndTitleManager.find_i_record")
    def test_get_registered_issue_data_returns_registered_issue(
            self, mock_find_i_record):
        issue_label = "v1n1"
        p_issn = "1234-5678"
        e_issn = "5678-1234"

        mock_find_i_record.return_value = ISSUE_RECORD
        result = self.manager.get_registered_issue_data(
            issue_label, p_issn, e_issn)
        res_acron_issue_label, res_issue_models, res_msg = result
        self.assertEqual('cta v40s1', res_acron_issue_label)
        self.assertIsNotNone(res_issue_models)
        self.assertIsNone(res_msg)

    @patch("prodtools.db.xc_models.IssueAndTitleManager.find_journal_record")
    def test_get_registered_journal_data_returns_not_registered_journal(
            self, mock_find_journal_record):
        journal_title = "Título"
        p_issn = "1234-5678"
        e_issn = "5678-1234"
        mock_find_journal_record.return_value = None

        result = self.manager.get_registered_journal_data(
            journal_title, p_issn, e_issn)
        registered_title, res_msg = result
        self.assertIsNone(registered_title)
        self.assertIn(journal_title, res_msg)

    @patch("prodtools.db.xc_models.IssueAndTitleManager.find_journal_record")
    def test_get_registered_journal_data_returns_registered_journal(
            self, mock_find_journal_record):
        journal_title = "Título"
        p_issn = "1234-5678"
        e_issn = "5678-1234"

        mock_find_journal_record.return_value = {}
        result = self.manager.get_registered_journal_data(
            journal_title, p_issn, e_issn)
        registered_title, res_msg = result
        self.assertIsNotNone(registered_title)
        self.assertIsNone(res_msg)
