
Como atualizar o site local
===========================

O fluxo de publicação usa arquivos SGML e/ou arquivos XML gerados no `Fluxo de publicação em SGML <workflow_sgml.html>`_ e/ou `Fluxo de publicação em XML <workflow_xml.html>`_ como entrada para o`site SciELO <http://docs.scielo.org/projects/scielo-site-windows/en/latest/>`_.

Os dados dos arquivos SGML e XML podem ser publicados na mesma página web do SciELO.


Bases de dados title e issue
----------------------------

As bases de dados issue e title devem ser atualizadas na `pasta serial <concepts.html#data-folder>`_.

Para atualizá-los, você pode usar a `Title Manager <titlemanager.html>`_.

Se precisar substituir a Title Manager por outra aplicação, terá que executar programas específicos para atualizar as bases de dados.

Outra opção é fazer uma cópia das bases de dados.



Arquivos SGML e/ou XML
----------------------

Na  `pasta serial <concepts.html#data-folder>`_, deve incluir as pastas/arquivos resultantes do fluxo de `marcação em SGML <workflow_markup_sgml.html>`_ e/ou do fluxo de `marcação em XML <workflow_markup_xml.html>`_.

Para SGML, os arquivos são:

* serial/<acron>/<volnum>/markup 
* serial/<acron>/<volnum>/body

Para XML, os arquivos são:

* ??/<acron>/<volnum>/markup_xml/scielo_package
 


XML Converter/ Converter
------------------------

Use `Converter <converter.html>`_ para gerar a *pasta base* dos arquivos SGML.

Use `XML Converter <xml_converter.html>`_ para gerar a *pasta base* dos arquivos XML.


GeraPadrao
----------

Execuar o scritpt `GeraPadrao.bat <http://docs.scielo.org/projects/scielo-site-windows/en/latest/howtogerapadrao.html#gerapadrao-bat>`_ para gerar a página `Web SciELO <http://docs.scielo.org/projects/scielo-site-windows/en/latest/>`_.


------------

Última atualização da página: agosto de 2015
