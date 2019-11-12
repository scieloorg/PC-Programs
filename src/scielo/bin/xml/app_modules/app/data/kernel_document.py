from ...generics import fs_utils
from . import scielo_id_gen
import xml.etree.ElementTree as ET


def add_article_id_to_received_documents(
    issn_id, year_and_order, received_docs, registered_docs, file_paths
):
    """Atualiza article-id (scielo-v2 e scielo-v3) dos documentos recebidos."""
    for name, received in received_docs.items():
        pid_v2 = received.get_scielo_pid("v2")
        pid_v3 = received.get_scielo_pid("v3")
        if pid_v2 and pid_v3:
            continue

        file_path = file_paths.get(name)
        xml = ET.parse(file_path)
        article_meta = xml.find(".//article-meta")
        registered = registered_docs.get(name)

        if not pid_v3:
            received.registered_scielo_id = get_scielo_pid_v3(registered)
            add_article_id(
                article_meta, received.registered_scielo_id, "scielo-v3")

        if not pid_v2:
            pid = get_scielo_pid_v2(issn_id, year_and_order, received.order)
            add_article_id(article_meta, pid, "scielo-v2")

        save(file_path, xml)


def get_scielo_pid_v2(issn_id, year_and_order, order_in_issue):
    year = year_and_order[:4]
    order_in_year = year_and_order[4:].zfill(4)
    return "".join(("S", issn_id, year, order_in_year, order_in_issue))


def get_scielo_pid_v3(registered):
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
