from ...generics import fs_utils
from . import scielo_id_gen

import xml.etree.ElementTree as ET


def add_article_id_to_received_documents(
    pid_manager,
    issn_id, year_and_order, received_docs, registered_docs, file_paths):
    """
    Atualiza article-id (scielo-v2 e scielo-v3) dos documentos recebidos.
    pid_manager: instância de PIDVersionsManager para gerir pid da versão 3
    issn_id: ISSN ID, chave para gerar o pid da versão 2
    year_and_order: também faz parte do pid da versão 2
    received_docs: pacote de documentos recebidos para processar
    registered_docs: documentos já registrados na base isis (acron/volnum)
    file_paths: arquivos do received_docs
    """
    for name, received in received_docs.items():
        pid_v2 = received.get_scielo_pid("v2")
        pid_v3 = received.get_scielo_pid("v3")
        if pid_v2 and pid_v3:
            """
            TODO: validar o pid_v3 que está presente no pacote recebido
            e / ou registrá-lo caso não esteja registrado
            """
            continue

        pid_and_specific_use_items = []

        if not pid_v2:
            pid_v2 = get_scielo_pid_v2(issn_id, year_and_order, received.order)
            pid_and_specific_use_items.append((pid_v2, "scielo-v2"))

        if not pid_v3:
            pid_v3_from_manager = None
            registered = registered_docs.get(name)
            if registered and registered.scielo_id:
                pid_v3 = registered.scielo_id

            if not pid_v3 and pid_manager:
                pid_v3 = pid_manager.get_pid_v3(pid_v2)
                pid_v3_from_manager = pid_v3

            if not pid_v3:
                pid_v3 = scielo_id_gen.generate_scielo_pid()

            received.registered_scielo_id = pid_v3
            if pid_v3_from_manager is None:
                pid_manager.insert(pid_v2, pid_v3)

            pid_and_specific_use_items.append((pid_v3, "scielo-v3"))

        if pid_and_specific_use_items:
            add_article_id_to_xml(
                file_paths.get(name),
                pid_and_specific_use_items)


def get_scielo_pid_v2(issn_id, year_and_order, order_in_issue):
    year = year_and_order[:4]
    order_in_year = year_and_order[4:].zfill(4)
    return "".join(("S", issn_id, year, order_in_year, order_in_issue))


def add_article_id_to_xml(file_path, pid_and_specific_use_items):
    if pid_and_specific_use_items:
        xml = ET.parse(file_path)
        article_meta = xml.find(".//article-meta")
        for id_value, specific_use in pid_and_specific_use_items:
            article_id = ET.Element("article-id")
            article_id.text = id_value
            article_id.set("specific-use", specific_use)
            article_id.set("pub-id-type", "publisher-id")
            article_meta.append(article_id)
        new_content = ET.tostring(xml.find(".")).decode("utf-8")
        fs_utils.write_file(file_path, new_content)
