from ...generics import fs_utils
from . import scielo_id_gen
import xml.etree.ElementTree as ET


def add_article_id_to_received_documents(
        received_documents, registered_documents, file_paths):
    """Atualiza scielo_id dos documentos recebidos."""
    for name, received in received_documents.items():
        if not received.scielo_id:
            add_scielo_id(
                received,
                registered_documents.get(name),
                file_paths.get(name),
            )


def get_scielo_id(registered):
    if registered and registered.scielo_id:
        return registered.scielo_id
    return scielo_id_gen.generate_scielo_pid()


def add_scielo_id(received, registered, file_path):
    """Atualiza received.registered_scielo_id com o valor do
    registered.scielo_id ou gerando um novo scielo_id."""
    received.registered_scielo_id = get_scielo_id(registered)
    xml = ET.parse(file_path)
    article_meta = xml.find(".//article-meta")
    if article_meta is not None:
        attributes = {
            "specific-use": "scielo",
            "pub-id-type": "publisher-id",
        }
        add_article_id(article_meta, received.registered_scielo_id, attributes)

        save(file_path, xml)


def add_article_id(article_meta, value, attributes):
    article_id = ET.Element("article-id")
    article_id.text = value
    for name, value in attributes.items():
        article_id.set(name, value)
    article_meta.insert(0, article_id)


def save(file_path, xml):
    new_content = ET.tostring(xml.find(".")).decode("utf-8")
    fs_utils.write_file(file_path, new_content)
