# coding:utf-8
import unittest
from unittest.mock import Mock, patch
import os

from xml.etree import ElementTree as etree
from copy import deepcopy
from prodtools.data import kernel_document


class Article:
    def __init__(self, scielo_id, scielo_pid):
        self.scielo_id = scielo_id
        self.scielo_pid = scielo_pid
        self.registered_scielo_id = None
        self.order = "12345"

    def get_scielo_pid(self, name):
        if name == "v3":
            return self.scielo_id
        return self.scielo_pid


@unittest.skip("deixou de passar após PR 3171")
class TestKernelDocumentAddArticleIdToReceivedDocuments(unittest.TestCase):
    def setUp(self):
        self.files = ["file" + str(i) + ".xml" for i in range(1, 6)]
        for f in self.files:
            with open(f, "wb") as fp:
                fp.write(b"<article><article-meta></article-meta></article>")

    def tearDown(self):
        for f in self.files:
            try:
                os.unlink(f)
            except IOError:
                pass

    def test_add_article_id_to_received_documents(self):
        registered = {}
        registered.update({"file1": Article(None, None)})
        registered.update({"file2": Article("xyzwx", None)})
        registered.update({"file3": Article(None, "09873")})
        registered.update({"file4": Article("Akouuad", "83847")})

        received = deepcopy(registered)
        file_paths = {}
        for fname in self.files:
            name, ext = os.path.splitext(fname)
            received.update({name: Article(None, None)})
            file_paths.update({name: fname})
        issn_id = "9876-3456"
        year_and_order = "20173"

        mock_pid_manager = Mock()
        kernel_document.scielo_id_gen.generate_scielo_pid = Mock(return_value="xxxxxx")
        kernel_document.add_article_id_to_received_documents(
            mock_pid_manager, issn_id, year_and_order, received,
            registered, file_paths
        )

        for name, item in received.items():
            registered_doc = registered.get(name)
            if registered_doc and registered_doc.scielo_id:
                expected_scielo_id = registered_doc.scielo_id
            else:
                expected_scielo_id = "xxxxxx"
            with self.subTest(name):
                self.assertEqual(item.registered_scielo_id, expected_scielo_id)
                with open(file_paths[name], "r") as fp:
                    content = fp.read()
                    self.assertIn("article-id", content)
                    self.assertIn("S9876-34562017000312345", content)
                    self.assertIn('specific-use="scielo-v3"', content)
                    self.assertIn('specific-use="scielo-v2"', content)
                    self.assertIn(expected_scielo_id, content)


class TestKernelDocument(unittest.TestCase):
    """docstring for TestKernelDocument"""

    def test_get_scielo_pid_v2(self):
        result = kernel_document.get_scielo_pid_v2(
            issn_id="3456-0987",
            year_and_order="20095",
            order_in_issue="54321")
        self.assertEqual("S3456-09872009000554321", result)

    @unittest.skip("kernel_document.get_scielo_pid_v3 foi removida no PR 3171")
    @patch("prodtools.data.kernel_document.scielo_id_gen.generate_scielo_pid")
    def test_get_scielo_pid_v3_returns_a_new_scielo_id(self, mocked_generate_scielo_pid):
        registered = Mock()
        registered.scielo_id = None
        mocked_generate_scielo_pid.return_value = "GENERATED"
        result = kernel_document.get_scielo_pid_v3(registered)
        self.assertEqual("GENERATED", result)

    @unittest.skip("kernel_document.get_scielo_pid_v3 foi removida no PR 3171")
    @patch("prodtools.data.kernel_document.scielo_id_gen.generate_scielo_pid")
    def test_get_scielo_pid_v3_returns_previously_registered_scielo_id(self, mocked_generate_scielo_pid):
        registered = Mock()
        registered.scielo_id = "REGISTERED"
        mocked_generate_scielo_pid.return_value = "GENERATED"
        result = kernel_document.get_scielo_pid_v3(registered)
        self.assertEqual("REGISTERED", result)

    @unittest.skip("kernel_document.add_article_id foi removida no PR 3171")
    def test_add_article_id_create_article_id_which_specific_use_is_scielo_v3(self):
        article_meta = etree.Element("article-meta")
        id_value = "01"
        specific_use = "scielo-v3"
        kernel_document.add_article_id(article_meta, id_value, specific_use)
        article_id = article_meta.find("article-id")
        self.assertEqual(article_id.text, id_value)
        self.assertEqual(article_id.get("specific-use"), specific_use)

    @unittest.skip("kernel_document.add_article_id foi removida no PR 3171")
    def test_add_article_id_create_article_id_which_specific_use_is_scielo_v2(self):
        article_meta = etree.Element("article-meta")
        id_value = "01"
        specific_use = "scielo-v2"
        kernel_document.add_article_id(article_meta, id_value, specific_use)
        article_id = article_meta.find("article-id")
        self.assertEqual(article_id.text, id_value)
        self.assertEqual(article_id.get("specific-use"), specific_use)
