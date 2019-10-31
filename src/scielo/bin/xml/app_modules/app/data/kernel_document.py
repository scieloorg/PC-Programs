from ...generics import fs_utils
from . import scielo_id_gen
import xml.etree.ElementTree as ET


def add_article_id_to_received_documents(
    received_documents, registered_documents, file_paths
):
    """Atualiza scielo_id dos documentos recebidos."""
    for name, received in received_documents.items():
        if not received.scielo_id:
            file_path = file_paths.get(name)
            registered = registered_documents.get(name)
            received.registered_scielo_id = get_scielo_id(registered)

            xml = ET.parse(file_path)
            article_meta = xml.find(".//article-meta")
            add_article_id(article_meta, received.registered_scielo_id, "scielo")

            save(file_path, xml)


def get_scielo_id(registered):
    if registered and registered.scielo_id:
        return registered.scielo_id
    return scielo_id_gen.generate_scielo_pid()


def add_article_id(article_meta, id_value, specific_use):
    article_id = ET.Element("article-id")
    article_id.text = id_value
    article_id.set("specific-use", specific_use)
    article_id.set("pub-id-type", "publisher-id")
    article_meta.insert(0, article_id)


def save(file_path, xml):
    new_content = ET.tostring(xml.find(".")).decode("utf-8")
    fs_utils.write_file(file_path, new_content)
