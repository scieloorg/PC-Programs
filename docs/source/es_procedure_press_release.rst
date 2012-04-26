Procedimento para publicación de comunicación de prenta (press release)
=======================================================================

Press releases son textos que divulgan contenido de artículos y/o fascículo.

Una comunicación de prenta no es parte de ningun facículo.

Pero para que la metodología pudiera publicar comunicación de prenta, se crea un fascículo para agrupar este tipo de documento.


Crear un facículo
-----------------

Use Title Manager para crear un **facículo press release**.

Cree un **facículo press release** para cada facículo **regular**.

Mira la documentación de `Title Manager <titlemanager_issue.html>`_ para saber como se hace.

Es decir, se llena el campo compl (complemento) con **pr**.

Un **facículo press release** puede contener 1 o más documentos, marcados como text.

Estos facículos deben ser publicados antes o simultaneamente a los artículos/facículos que ellos divulgan. 

El sistema asocia la identificación de **facículo press release** con la de los facículo/artículos divulgados.

Es decir:

- facículo *regular*         v3n1
- facículo *press release*   v3n1pr

Crear la carpeta en serial
--------------------------

El nombre de la carpeta es la identificación del facículo divulgado más pr.

Ej.: v2n1pr

Markup
------

- Press release
    Se los marcan como text. Van a tener un atributo llamado **isidpart**, cuyo valor es **pr**.


Converter
---------

Complete el campo compl con **pr**.

GeraPadrao
----------

    .. warning::
        Los **facículos** press releases deben ser puestos antes del fascículo regular divulgado

Website
-------

Los enlaces para los textos de press release serán presentados:

- en la página inicial de la revista al lado derecho.
- en la tabla de contenido, junto al artículo divulgado o al inicio de la tabla si el texto divulga el facículo
- en la página del artículo, en la caja de herramientas





