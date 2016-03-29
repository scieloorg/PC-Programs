.. _como-generar-archivos-sgml:

Cómo generar archivos SGML (Marcación en el HTML con DTD article y text)
========================================================================

.. toctree::
   :maxdepth: 3


.. _especificaciones-archivos:

Especificaciones de Archivos
----------------------------

- Un documento (article o text) por archivo
- .html
- Todos los archivos relacionados al documento debentener lo mismo nombre. Ejemplo, a01.pdf. 
- Todos los archivos 'translation' deben tener lo mismo nombre precedido por lo codigo de dos letras (norma ISO 639-1). Ejemplo, en_a01.pdf, en_a01.html.


.. _ubicacion-archivos:

Ubicación de los archivos
-------------------------

Organiza los archivos de acuerdo con la estructura de archivos/carpetas disponible abajo:

Archivos para Markup
    /scielo/serial/<acron>/<numero_identificador>/markup

body
    /scielo/serial/<acron>/<numero_identificador>/body

imágenes
    /scielo/serial/<acron>/<numero_identificador>/img

pdf
    /scielo/serial/<acron>/<numero_identificador>/pdf

Ejemplo:

.. image:: img/concepts_serial_abc.jpg


.. _archivos-markup:

Archivos para Markup
--------------------

No debe existir lo archivo /scielo/bin/markup/markup_journals_list.csv. Si existe, exclua esto archivo 'markup_journals_list.csv'.

En su lugar, debe tener la siguiente estructura:

- ??_issue.mds: actualizar/crear como cualquer dato de número de fascículo es actualizado/creado
- issue.mds: actualizar/crear como cualquer dato de número de fascículo es actualizado/creado
- journal-standard.txt: actualizar/crear como cualquer dato de revista es actualizado/creado


Estos archivos son generados a través de `Title Manager <titlemanager.html>`_ o SciELO Manager.


.. _markup:

Markup
------


Usa `Markup Program <markup.html>`_.

----------------

Última actualización de esta pagina: Agosto de 2015
