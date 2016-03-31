
How to update the local web site
================================

The publishing workflow uses SGML Files and/or XML Files as input and generates the local website according to `SciELOWeb site <http://docs.scielo.org/projects/scielo-site-windows/en/latest/>`_.

Data from SGML and XML files can be published on the same SciELO Web site.


title and issue databases
.........................

issue and title databases must be updated in `serial folder <concepts.html#data-folder>`_.

This databases are managed by `Title Manager <titlemanager.html>`_.

If you have replaced Title Manager by SciELO Manager, you have to run specifics programs to update (Delorean) these databases.

Other option is having updated copies of these databases.


SGML files and/or XML files
...........................

In `serial folder <concepts.html#data-folder>`_, you must have the folders/files resulting of `SGML Markup workflow <workflow_markup_sgml.html>`_ and/or `XML Markup workflow <workflow_markup_xml.html>`_.

For SGML, the input files must be in:

* serial/<acron>/<volnum>/markup 
* serial/<acron>/<volnum>/body

For XML, the input files must be in:

* ??/<acron>/<volnum>/markup_xml/scielo_package 


XML Converter/ Converter
........................

Use `Converter <converter.html>`_ to generate the *base folder* from the SGML files.

Use `XML Converter <xml_converter.html>`_ to generate the *base folder* from the XML files.


GeraPadrao
..........

Run `GeraPadrao.bat <http://docs.scielo.org/projects/scielo-site-windows/en/latest/howtogerapadrao.html#gerapadrao-bat>`_ script to generate de local website. 



