import unittest
import os
import xml.etree.ElementTree as ET
from copy import deepcopy
from app_modules.app.pkg_processors.pkg_processors import add_scielo_id


class Article:
    def __init__(self, scielo_id):
        self.scielo_id = scielo_id
        self.registered_scielo_id = None


class TestAddSciELOId(unittest.TestCase):

    def setUp(self):
        self.files = ["file"+str(i)+".xml"
                      for i in range(1, 6)]

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
            registered.update({'file'+str(i): Article(None)})
        received = deepcopy(registered)
        xml_items = {}
        for fname in self.files:
            name, ext = os.path.splitext(fname)
            received.update({name: Article(None)})
            xml_items.update(
                {name:
                    {'file': fname,
                     'xml': ET.fromstring(text)}})

        add_scielo_id(received, registered, xml_items)
        for name, item in received.items():
            with self.subTest(name):
                self.assertIsNotNone(item.registered_scielo_id)
                with open(xml_items[name]['file'], 'r') as fp:
                    content = fp.read()
                    self.assertIn('article-id', content)
