import unittest
import os
import xml.etree.ElementTree as ET
from copy import deepcopy
from app_modules.app.data.scielo_id_manager import (
    add_scielo_id,
    add_scielo_id_to_received_documents,
)


class Article:
    def __init__(self, scielo_id):
        self.scielo_id = scielo_id
        self.registered_scielo_id = None


class TestAddSciELOIdManager(unittest.TestCase):
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

    def test_add_scielo_id(self):
        text = """<article><article-meta></article-meta></article>"""
        registered = {}
        for i in range(1, 3):
            registered.update({"file" + str(i): Article(None)})
        received = deepcopy(registered)
        file_paths = {}
        for fname in self.files:
            name, ext = os.path.splitext(fname)
            received.update({name: Article(None)})
            file_paths.update({name: fname})

        add_scielo_id_to_received_documents(received, registered, file_paths)
        for name, item in received.items():
            with self.subTest(name):
                self.assertIsNotNone(item.registered_scielo_id)
                with open(file_paths[name], "r") as fp:
                    content = fp.read()
                    self.assertIn("article-id", content)
