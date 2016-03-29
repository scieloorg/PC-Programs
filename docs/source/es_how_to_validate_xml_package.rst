.. _es_como_validar_paquete_xml

Como validar el paquete XML
===========================

Usa el Paquete XPM para generar el paquete XML para SciELO y PMC.


Package Maker - ¿Cómo usar?
---------------------------

Para usar el programa Package Maker haga un click en el menú inicio de Windows, busca la carpeta del programa Markup que fue instalado en su ordenador y con el ratón verifica los itens disponibles en la carpeta.

Haga un click en el botón *XML Package Maker*



.. image:: img/scielo_menu_xpm.png

.. image:: img/xpm_gui.png


Ahora haga un click en el botón "Choose Folder" y escoja la carpeta de archivos que será validada 



.. image:: img/xpm_gui_selected_folder.png


Haga un click en **XML Package Maker**.


Resultados
----------


* Para arquivos XML SciELO (verifica la carpeta scielo_package e/ou scielo_package_zips)
* Para arquivos XML PMC (verifica la carpeta pmc_package)
* Para Relatório de arquivos (verifica la carpeta errors)

La carpeta que es generado por el XPM "ISSN-acronimo-volume-numero_xml_package_maker_result" estará disponible en lo mismo nivel de la carpeta que fue usada para generar el paquete:


.. image:: img/xpm_result_folders.png



Informes
--------

Despues de validar y generar los paquetes, los informes serán disponiblizados automaticamente en web browser.


Informes Resumidos
.................

Estatísticas de Validaciones
::::::::::::::::::::::::::::

Se presenta el total de errores fatales (Fatal Errors), errores (Errors), y advertencias (Warnings), que se encuentran en todo el paquete.

FATAL ERRORS
   Representa los errores relacionados con los indicadores bibliometricos.

ERRORS
   Representa otros tipos de errores.

WARNINGS
   Representa alguna cosa que necesita de más atención.


.. image:: img/xpm_report.png


Informe Detallado
.................

Informe Detallado - Validaciones del Paquete
::::::::::::::::::::::::::::::::::::::::::::


Primeiro de todo, el programa XPM valida algunos datos del paquete:

- Elementos que tienen el mismo valor en todos los archivos XML, tales como:


 * journal-title
 * journal id NLM
 * journal ISSN
 * publisher name
 * issue label
 * issue pub date

-  Elementos que tienen un valor único para cada archivo XML, como por ejemplo:

 * doi
 * elocation-id, if applicable
 * fpage and fpage/@seq
 * order (used to generated article PID)


Ejemplo de errores fatales (Fatal Error) que tienen un valor diferente para el elemento ``<publisher-name>``

 .. image:: img/xml_reports__toc_fatal_error_required_equal_publisher.jpg


Ejemplo de Errores Fatales (Fatal Error) que tienen valores diferentes en ``<pub-date>``

 .. image:: img/xml_reports_toc_fatal_error_required_equal_date.png


Ejemplo de Errores Fatales (Fatal Error) ya que requiere un valor único

 .. image:: img/xml_reports_toc_fatal_error_unique.png.jpg


Informe Detallado - Validaciones del Documento
::::::::::::::::::::::::::::::::::::::::::::::

El documento se presenta en una tabla.

Las columnas 'order', 'aop pid', 'toc section', '@article-type'  se destacan porque contiene datos importantes.

La columna **reports** tiene **botones** para abrir/cerrar el informe detallado de cada documento.


Cada linea tiene un dato en el documento:

.. image:: img/xpm_report_detail.png


Informe Detallado - Validaciones
::::::::::::::::::::::::::::::::

Haga un click en **Validación de Contenido** para verificar los problemas presentados.

El informe detallado es presentado debajo de la linea.

.. image:: img/xpm_report_detail_validations.png


Archivos/Carpetas
.................

Muestra los archivos y carpetas que fueron generado y validados.

.. image:: img/xpm_report_folder.png


Visión General de Paquete
.........................

Visión General de Paquete - idiomas
:::::::::::::::::::::::::::::::::::

Muestra los elementos que tienen el atributo de idioma ``@xml:lang``. 

.. image:: img/xpm_report_overview_lang.png


Visión General de Paquete - datos
:::::::::::::::::::::::::::::::::

Muestra los datos encontrados en el documento: publicación y historico.

Muestra el tiempo de espera entre: Fecha recibido y aceptado, aceptado y publicado, aceptado, y la fecha actual.

.. image:: img/xpm_report_overview_date.png


Visión General de Paquete - afiliaciones
::::::::::::::::::::::::::::::::::::::::


.. image:: img/xpm_report_overview_aff.png


Visión General de Paquete - Citas bibliograficas
::::::::::::::::::::::::::::::::::::::::::::::::


.. image:: img/xpm_report_overview_ref.png


Informes fonte
..............

.. image:: img/xpm_report_sources.png

.. image:: img/xpm_report_sources_journals.png

.. image:: img/xpm_report_sources_books.png

.. image:: img/xpm_report_sources_others.png
