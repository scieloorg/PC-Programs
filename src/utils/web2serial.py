acron_issue_id=bn/v15n3
rsync -r homolog.scielo.br:/var/www/xml_scielo_br/bases/xml/$acron_issue_id/*.xml /bases/xml.000/serial/$acron_issue_id/base_xml/base_source
rsync -r homolog.scielo.br:/var/www/xml_scielo_br/bases/pdf/$acron_issue_id/*.pdf /bases/xml.000/serial/$acron_issue_id/base_xml/base_source
rsync -r homolog.scielo.br:/var/www/xml_scielo_br/htdocs/img/revistas/$acron_issue_id/* /bases/xml.000/serial/$acron_issue_id/base_xml/base_source
