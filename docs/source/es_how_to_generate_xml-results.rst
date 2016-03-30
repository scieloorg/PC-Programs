.. es_how_to_generate_xml-results:

Generando el Archivo .xml
=========================

Después de identificar todos los datos del documento .doc, el siguiente paso es generar el archivo .xml.

Antes de todo, salve el archivo marcado haciendo un click en el botón "Markup: Salvar":

.. image:: img/doc-mkp-salvar.jpg
   :align: center


Después haga un click  en el botón "Markup: Gerar o XML":

.. image:: img/doc-mkp-gerarxml.jpg
   :align: center


.. informes

Informes
========

Al generar el archivo .xml el programa Markup presenta tres informes: :ref:`informe-archivos`, :ref:`informe-estilos` e :ref:`informe-contenido`.
Abajo la función de cada informe presentado.


.. _informe-archivos:

Informes de Errores de los Archivos
-----------------------------------

Al hacer un click en "Markup: Gerar o XML" el programa presenta un informe con las informaciones de las alteraciones hechas en el documento.


.. image:: img/doc-mkp-report-name.jpg
   :height: 450px


Lo resultado de eso, es un informe el cual presenta las acciones del programa al generar el XML desde el archivo .doc.

El programa modifica el nombre del archivo que, en .doc, estaba presentado como "12-Artigo.doc" para "ISSN-acronimo-volume-numero-paginação.xml" y las imagenes son extraídas del documento yá con el nombre convertido para la recomiendación SciELO.


.. _informe-estilos:

Informe de Estilos SciELO
-------------------------

Después haga un click en el botón situado junto "Relatório de Estilos SciELO" y verifique si hay algun error en el documento.


.. image:: img/doc-mkp-gerar-report-scielo.jpg
   :align: center

El programa mostrará un informe que se parece con lo que sigue abajo:

.. image:: img/doc-mkp-report-style.jpg
   :align: center
   :height: 450px

Ver que en el informe de errores no es presentado ningun error. Eso ocurre porque el xml generado está de acuerdo con la estructura de estilos solicitada.


.. _informe-contenido:

Informe de Errores de los Contenidos
------------------------------------

Hecha la verificación en el informe de estilos SciELO, el siguiente paso es generar el informe de errores de los datos/contenido.


Ese informe es exatamente lo mismo que el programa Package Maker genera. Por lo tanto, para verificar el manual de uso para validación y verificación de errores presentados, entre en proyecto `Package Maker <es_how_to_validate_xml_package.html>`_ y confira las características de esa herramienta.


.. _informe-carpetas:

Carpetas Generadas
==================

Al generar el archivo .xml el programa Markup crea 6 carpetas en el mismo nivel que la carpeta "src" y "scielo_markup", como sigue abajo:

.. image:: img/doc-mkp-pastas-geradas.jpg
   :align: center
   :height: 300px


**carpeta de errores:**

	En esa carpeta hay el informe de errores de cada uno de los archivos .xml. El archivo final '.rep' presenta los posibles errores de estilo y el archivo con el final '.contents' presenta los contenidos. Son los mismos informes presentados en el programa de marcación.


**pmc_package:**

	Para los periódicos que presentam el títutlo corto NLM, el programa retira los elementos de especificación SciELO y mantiene solo los elementos necesarios para el envio al PMC.
	Los elementos que son retirados de lo documento XML para envio al PMC son: detallamento en afiliación, información de financiación en ``<funding-group>`` y ``<mixed-citation>``.


**pmc_package_zips:**

	Al validar el paquete pmc_package el programa, automaticamente, comprime la carpeta que está pronta para envio.


**scielo_package:**

	En el momento de la validación del paquete XML, el programa verifica las entidades (numericas o alfa-numericas) que existen en el documento y, automaticamente, convierte para el caractere correspondiente, evitando futuros problemas en entidades. Lo ideal es usar los archivos .xml validados en esa carpeta en vez de usar los xmls del paquete.


**scielo_package_zips:**

	Al validar el paquete scielo_package el programa, automaticamente, comprime la carpeta yá con el nombre predeterminado SciELO que está pronta para envio.


**work:**

	Es una carpeta de archivos temporales usadas para la generación de los resultados. Esta carpeta se puede borrar si lo prefiere, pero también puede ser usada con finalidad de soporte.

	Esa estructura de carpetas es la misma presentada si el usuario usar el programa `Package Maker <es_how_to_validate_xml_package.html>`_. Para verificar los informes presentados, entra en la carpeta "errors" y abre el documento con extensão: ".contents.html"


