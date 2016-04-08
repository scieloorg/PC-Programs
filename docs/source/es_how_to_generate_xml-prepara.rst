.. _es_how_to_generate_xml-prepara:

========================================================
Preparación de los archivos para uso del Programa Markup
========================================================

Introducción
============
 
Antes de iniciar el proceso de marcaje, es necesario seguir algunos pasos para preparación de los archivos que van a ser marcados.
Sigue los requisitos para el marcaje del documento.
 
 * Los archivos deben estar en formato Word (.doc) o (.docx).
 * La estructura de carpetas debe seguir el padrón SciELO
 * Os archivos deben ser formateados de acuerdo con el Formateo SciELO.
 

.. note:: Los nombres de los archivos que no deben contener espacios, diacríticos o caracteres especiales. Caso sea necesario separar un dato de otro use underline. 
         Sólo así, las imágenes marcadas en el cuerpo del texto serán renombradas y generadas correctamente. 
         Ejemplo: ACB_2345.doc


Archivos de entrada para el Markup
==================================

Revista de  www.scielo.org
............................

Sólo si es una revista de www.scielo.org, use el menú para actualizar la lista de revistas.

   .. image:: img/scielo_menu_download_journals.png


Seleccione la colección:

   .. image:: img/download_journals_data.png



Otras revistas
.................

No debe existir el archivo /scielo/bin/markup/markup_journals_list.csv. Si existir, borrarlo.

En su lugar, debe existir:

- ??_issue.mds: actualizado/creado así que cualquier dato de número es creado o actualizado
- journal-standard.txt: actualizado/creado cuándo los datos de una revista es creado o actualizado

Estos archivos son generados por el programa `Title Manager <titlemanager.html>`_ o `SciELO Manager <http://docs.scielo.org/projects/scielo-manager/en/latest/>`_.


.. note::
   Title Manager genera estos archivos en /scielo/bin/markup en el computador dónde la Title Manager es ejecutado.
   Si el Markup es usado en otro computador, precisarás copiar estos dos archivos para el computador donde el Markup será ejecutado.


.. raw:: html

   <iframe width="854" height="480" src="https://www.youtube.com/embed/SNAXZ1BaMM0?list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _estructura-de-carpetas:

Estructura de carpetas
======================

Antes de comenzar la marcación, es preciso garantizar que la estructura de carpetas esté como sigue:

.. image:: img/doc-mkp-estrutura.jpg
   :height: 200px
   :align: center



Dentro de la carpeta "markup_xml" fueron insertadas dúas carpetas, en el mismo nivel:

 * src: utilizada para insertar los archivos PDF, media y suplementos.
 * scielo_markup: utilizada para insertar los archivos .doc ou .docx.


..  note:: Si la recomendación de estructura presentada no fuera seguida, el proceso de marcaje no será iniciado.


.. raw:: html

   <iframe width="854" height="480" src="https://www.youtube.com/embed/RLizVtt5Ca8?list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>

.. _formato-scielo:

Formateo de lo Archivo
======================

Para optimizar el proceso de marcaje de los elementos básicos do archivo, es necesario seguir el padrón de formateo SciELO que sigue:

**Instrucción para formateo de datos básicos del artículo:**

 * Línea 1: inserir número de DOI (solamente si presente), caso no exista empezar por la sección;
 * Línea 2: inserir la sección de la tabla de contenido (si ausente, dejar línea en blanco);
 * Línea 3: Título del artículo;
 * Líneas siguientes: Títulos traducidos del archivo;
 * Para separar autores de título, saltar una línea;
 * Cada autor debe estar en una línea y usar sobrescrito para label;
 * Saltar una Línea para separar autores de afiliaciones;
 * Cada afiliación debe estar en una línea;
 * Saltar una línea para separar afiliación de los resúmenes;
 * Resúmenes estructurados: negrita en el nombre de la sección;
 * Palabras-clave: los separadores deben ser o punto-y-vírgula o vírgula;
 * Secciones: negrita, 16, centralizadas;
 * Subsecciones: negrita, 14, centralizadas;
 * Subsección de subsección: negrita, 13, centralizadas;
 * Texto: formateo libre;
 * Para tablas, label y caption (leyenda) en la línea antes de la imagen, en los demás casos, después de la imagen;
 * Separador de label y caption: dos-puntos e espacio o espacio + guion + espacio o ponto + espacio;
 * Para tablas codificadas, el encabezamiento debe estar en negrita;
 * La cita del tipo autor/fecha en el cuerpo del texto debe ser: sobrenombre del autor, año;
 * Para citas en el sistema numérico en el cuerpo del texto: "sobrescrito" e entre paréntesis;
 * Notas de pie de página en el cuerpo del texto pueden estar “sobrescrito", pero no estarán entre paréntesis;
 * Citaciones (quote), reculado en 4 cm de la margen izquierda;


Ejemplo:

.. image:: img/doc-mkp-2mostra.jpg
   :height: 400px
   :width: 200px
   :align: center


.. raw:: html

   <iframe width="854" height="480" src="https://www.youtube.com/embed/kaYRu-bkhBE?list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>

.. note:: Las imágenes de los artículos deben estar disponibles en el archivo .doc, preferencialmente en formato .jpeg y .png.
