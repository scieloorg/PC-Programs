from ...generics import fs_utils
from . import scielo_id_gen
import xml.etree.ElementTree as ET


def add_scielo_id_to_documents(received_documents, registered_documents):
    """Atualiza scielo_id."""
    for name, received in received_documents.items():
        registered_id = None
        registered = registered_documents.get(name)
        if registered:
            registered_id = registered.registered_scielo_id
        received.registered_scielo_id = registered_id or scielo_id_gen.generate_scielo_pid()


def add_scielo_id_to_xml_files(received_documents, file_paths):
    """Atualiza scielo_id."""
    for name, received in received_documents.items():
        file_path = file_paths.get(name)
        xml = ET.parse(file_path)
        article_meta = xml.find(".//article-meta")
        if article_meta is None:
            continue
        article_id_node = xml.find(
            ".//article-meta/article-id[@specific-use='scielo']")
        if article_id_node is None:
            article_id_node = ET.Element("article-id")
            article_id_node.set("specific-use", "scielo")
            article_id_node.set("pub-type-id", "publisher-id")

        if (article_id_node is not None and
                article_id_node.text != received.registered_scielo_id):
            article_id_node.text = received.registered_scielo_id

            article_meta.insert(0, article_id_node)
            new_content = ET.tostring(xml.find(".")).decode("utf-8")
            fs_utils.write_file(file_path, new_content)
