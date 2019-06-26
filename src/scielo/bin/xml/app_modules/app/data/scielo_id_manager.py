from ...generics import fs_utils
from . import scielo_id_gen
import xml.etree.ElementTree as ET


def add_scielo_id(received_documents, registered_documents,
                  xml_and_file_items):
    """Atualiza documento_recebido.registered_scielo_id com o valor do
    documento_registrado.scielo_id ou obtendo um novo scielo_id."""
    for name, received in received_documents.items():
        if not received.scielo_id:
            registered = registered_documents.get(name)
            if registered and registered.scielo_id:
                received.registered_scielo_id = registered.scielo_id
            else:
                node = xml_and_file_items[name]['xml'].find(".//article-meta")
                if node is not None:
                    article_id = ET.Element('article-id')
                    article_id.set("specific-use", "scielo-id")
                    article_id.set("pub-type-id", "publisher-id")
                    article_id.text = scielo_id_gen.generate_scielo_pid()
                    received.registered_scielo_id = article_id.text
                    node.insert(0, article_id)
                    filepath = xml_and_file_items[name]['file']
                    new_xml = xml_and_file_items[name]['xml']
                    content = fs_utils.read_file(filepath)
                    header = content[:content.find("<article")]
                    new_content = ET.tostring(new_xml.find(".")).decode("utf-8")
                    fs_utils.write_file(filepath, header+new_content)

