Procedimiento para publicación de comunicación de prensa (press release)
========================================================================

Press releases son textos que divulgan contenido de artículos y/o fascículo.

Una comunicación de prensa no es parte de ningun facículo.

Pero para que la metodología pudiera publicar comunicación de prensa, se crea un fascículo para agrupar este tipo de documento.
Pero para el sitio, el **facículo press release** no es considerado un facículo.


Crear un facículo
-----------------

Use Title Manager para crear un **facículo press release**.

Cree un **facículo press release** para cada facículo **regular**.

Mira la documentación de `Title Manager <titlemanager_issue.html#indentifying-press-release-issues>`_ para saber como se hace.

    .. image:: img/en/01_iss_pr.jpg

Es decir, se completa el campo compl (complemento) con **pr**.

Un **facículo press release** puede contener 1 o más documentos, marcados como text.

Estos facículos deben ser publicados antes o simultaneamente a los artículos/facículos que ellos divulgan. 

El sistema asocia la identificación de **facículo press release** con la de los facículo/artículos divulgados.

Es decir:

    - facículo *regular*         
        v3n1
    - facículo *press release*
        v3n1pr

Crear la carpeta en serial
--------------------------

El nombre de la carpeta es la identificación del facículo divulgado más pr.

Ej.: v2n1pr


    .. image:: img/en/pr_folder_structure.png



Markup
------

- Press release
    Se los marcan como text. Van a tener un atributo llamado **isidpart**, cuyo valor es **pr**.

    .. image:: img/en/pr_markup.png


- Artículo divulgado
    Debe ser identificado que está relacionado a um **texto press release** 

   .. image:: img/en/markup_atributo_related_marcado.jpg


Converter
---------

Complete el campo compl con **pr**.

   .. image:: imag/en/pressrelease_converter.jpg


GeraPadrao
----------

    .. warning::
        Los **facículos** press releases deben ser puestos antes del fascículo regular divulgado

    .. code-block:: text

        jb v45n1pr
        jb v45n1


Website
-------

Los enlaces para los textos de press release serán presentados:

- en la página inicial de la revista al lado derecho.
- en la tabla de contenido, junto al artículo divulgado o al inicio de la tabla si el texto divulga el facículo
- en la página del artículo, en la caja de herramientas


En la página inicial de la revista, queda el listado de los **textos press release**.

    .. image:: img/en/pressrelease_site02.jpg

Al acceder un **texto de press release**
 
    .. image:: img/en/pressrelease_texto.jpg

Si el **texto press release** es de un artículo, entonces habrá un enlace para el artículo.

    .. image:: img/en/pressrelease_artigo.jpg

En el sumario, será presentado un enlace para el **texto press release**.

    .. image:: img/en/pressrelease_site01.jpg



