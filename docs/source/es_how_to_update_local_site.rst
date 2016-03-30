
.. _como-actualizar-sitio-local:

Cómo actualizar el sitio local
==============================

El flujo de publicación usa archivos SGML y/o archivos XML generados como entrada para el sitio lcoal segun `Web de SciELO <http://docs.scielo.org/projects/scielo-site-windows/en/latest/>`_.

Datos de los archivos SGML y XML pueden ser publicados en el mismo sitio Web SciELO.


.. _bases-datos:

Bases de datos title e issue
----------------------------

Las bases de datos issue y title deben ser actualizadas en la `carpeta serial <concepts.html#data-folder>`_.

Para hacer la actualización, puedes usar el programa `Title Manager <titlemanager.html>`_.

Si Title Manager fue reemplazado por SciELO Manager, tiene que ejecutar programas específicos (Delorean) para actualizar estas bases de datos.


.. _archivos-sgml-xml:

Archivos SGML y/o XML
---------------------

En la `carpeta serial <concepts.html#data-folder>`_, debes tener las carpetas/archivos resultantes del proceso de `marcación en SGML <workflow_markup_sgml.html>`_ y/o del proceso de `marcación en XML <workflow_markup_xml.html>`_.

Para el SGML, los archivos de entrada deben estar en:

* serial/<acron>/<volnum>/markup 
* serial/<acron>/<volnum>/body

Para el XML, los archivos de entrada deben estar en:

* ??/<acron>/<volnum>/markup_xml/scielo_package 


.. _xml-converter:

XML Converter/ Converter
........................

Use `Converter <converter.html>`_ para generar la *carpeta base* de los archivos SGML.

Use `XML Converter <xml_converter.html>`_ para generar la *carpeta base* de los archivos XML.


.. _gera-padrao:

GeraPadrao
----------

Ejecute el scritpt `GeraPadrao.bat <http://docs.scielo.org/projects/scielo-site-windows/en/latest/howtogerapadrao.html#gerapadrao-bat>`_ para generar el sitio local.



------------
Última actualización de esta página: Agosto de 2015
