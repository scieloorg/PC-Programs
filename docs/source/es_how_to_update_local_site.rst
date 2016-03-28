
Cómo actualizar el sitio local 
------------------------------

El flujo de publicación usa archivos SGML y/o archivos XML generados en el `Flujo de publicación SGML <workflow_sgml.html>`_ y/o `Flujo de publicación en XML <workflow_xml.html>`_ como entrada para la `Página Web de SciELO <http://docs.scielo.org/projects/scielo-site-windows/en/latest/>`_.

Datos de los archivos SGML y XML pueden ser publicados en la misma página web SciELO.


Bases de datos title y issue
...........................

Las bases de datos issue y title deben ser actualizadas en la `carpeta serial <concepts.html#data-folder>`_.

Para hacer la actualización, puedes usar la `Title Manager <titlemanager.html>`_.

Si tienes que sustituir la Title Manager por otra aplicación, tendrás que ejecutar progrmas específicos para actualizar estas bases de datos.

Otra opción es hacer copias de estas bases de datos.


Archivos SGML y/o XML
.....................

En la  `carpeta serial <concepts.html#data-folder>`_, debes tener las carpetas/archivos resultantes del proceso de `marcación en SGML <workflow_markup_sgml.html>`_ y/o del proceso de `marcación en XML <workflow_markup_xml.html>`_.

Para el SGML, los archivos de entrada son:

* serial/<acron>/<volnum>/markup 
* serial/<acron>/<volnum>/body

Para el XML, los archivos de entrada son:

* ??/<acron>/<volnum>/markup_xml/scielo_package 


XML Converter/ Converter
........................

Use `Converter <converter.html>`_ para generar la *carpeta base* de los archivos SGML.

Use `XML Converter <xml_converter.html>`_ para generar la *carpeta base* de los archivos XML.


GeraPadrao
..........

Ejecuta el scritpt `GeraPadrao.bat <http://docs.scielo.org/projects/scielo-site-windows/en/latest/howtogerapadrao.html#gerapadrao-bat>`_ para generar la página `Web SciELO <http://docs.scielo.org/projects/scielo-site-windows/en/latest/>`_. 


------------

Última actualización de esta página: Agosto de 2015
