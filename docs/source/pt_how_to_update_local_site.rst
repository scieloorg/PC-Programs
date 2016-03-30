
Como atualizar o site local
===========================

O fluxo de publicação usa arquivos SGML e/ou arquivos XML como entrada para o site local segundo `site SciELO <http://docs.scielo.org/projects/scielo-site-windows/en/latest/>`_.

Os dados dos arquivos SGML e XML podem ser publicados no mesmo website do SciELO.


Bases de dados title e issue
----------------------------

As bases de dados issue e title devem estar atualizadas na `pasta serial <concepts.html#data-folder>`_.

Estas bases de dados são geridas pelo programa `Title Manager <titlemanager.html>`_ ou atualizadas pela aplicação Delorean quando a coleção é gerida pelo SciELO Manager.


Arquivos SGML e/ou XML
----------------------

Na `pasta serial <concepts.html#data-folder>`_, deve incluir as pastas/arquivos resultantes do fluxo de marcação em SGML e/ou do fluxo de marcação em XML.

Para SGML, os arquivos que contém os artigos ficam em:

* serial/<acron>/<volnum>/markup 
* serial/<acron>/<volnum>/body

Para XML, os arquivos que contém os artigos ficam em:

* ??/<acron>/<volnum>/markup_xml/scielo_package
 


XML Converter/ Converter
------------------------

Use `Converter <converter.html>`_ para gerar a *pasta base* dos arquivos SGML.

Use `XML Converter <xml_converter.html>`_ para gerar a *pasta base* dos arquivos XML.


GeraPadrao
----------

Executar o scritpt `GeraPadrao.bat <http://docs.scielo.org/projects/scielo-site-windows/en/latest/howtogerapadrao.html#gerapadrao-bat>`_ para gerar o site local.

