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


def add_scielo_id(received, registered, file_path):
    """Atualiza received.registered_scielo_id com o valor do
    registered.scielo_id ou gerando um novo scielo_id."""
    if registered and registered.scielo_id:
        received.registered_scielo_id = registered.scielo_id
    else:
        received.registered_scielo_id = scielo_id_gen.generate_scielo_pid()
    xml = ET.parse(file_path)
    node = xml.find(".//article-meta")
    if node is not None:
        article_id = ET.Element("article-id")
        article_id.set("specific-use", "scielo")
        article_id.set("pub-id-type", "publisher-id")
        article_id.text = received.registered_scielo_id
        node.insert(0, article_id)
        new_content = ET.tostring(xml.find(".")).decode("utf-8")
        fs_utils.write_file(file_path, new_content)
