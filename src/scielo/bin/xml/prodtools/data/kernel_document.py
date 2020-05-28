# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from prodtools.utils import fs_utils
from . import scielo_id_gen


def add_article_id_to_received_documents(
    pid_manager, issn_id, year_and_order, received_docs, documents_in_isis, file_paths
):
    """Atualiza article-id (scielo-v2 e scielo-v3) dos documentos recebidos.

    Params:
        pid_manager (PIDVersionsManager): instância de PIDVersionsManager para gerir pid da versão 3
        issn_id (str): ISSN do periódico
        year_and_order (str): Ano e ordem da issue processada
        received_docs (dict): Pacote de documentos recebidos para processar
        documents_in_isis (dict): Documentos já registrados na base isis (acron/volnum)
        file_paths (dict): arquivos do received_docs

    Returns:
        None
    """

    for xml_name, article in received_docs.items():
        pid_v2 = article.get_scielo_pid("v2")
        pid_v3 = article.get_scielo_pid("v3")
        pids_to_append_in_xml = []

        if pid_v2 and pid_v3:
            exists_in_database = pid_manager.pids_already_registered(pid_v2, pid_v3)

            if not exists_in_database:
                pid_manager.register(pid_v2, pid_v3)

            continue

        if pid_v2 is None:
            pid_v2 = get_scielo_pid_v2(issn_id, year_and_order, article.order)
            pids_to_append_in_xml.append((pid_v2, "scielo-v2"))

        if pid_v3 is None:
            pid_v3 = (
                documents_in_isis.get(xml_name, article).scielo_id
                or pid_manager.get_pid_v3(pid_v2)
                or scielo_id_gen.generate_scielo_pid()
            )
            pid_manager.register(pid_v2, pid_v3)
            article.registered_scielo_id = pid_v3
            pids_to_append_in_xml.append((pid_v3, "scielo-v3"))

        add_article_id_to_xml(file_paths.get(xml_name), pids_to_append_in_xml)


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
            article_meta.insert(0, article_id)
        new_content = ET.tostring(xml.find(".")).decode("utf-8")
        fs_utils.write_file(file_path, new_content)
