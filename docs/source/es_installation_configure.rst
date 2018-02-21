.. how_to_install:

=============
Cómo instalar
=============

XML Package Maker
=================

1. Instalar y/o verificar los `requisitos <es_installation_requirements.html>`_
2. Descargar el `instalador <es_installation_download.html>`_
3. Ejecutar el instalador
4. Indicar la ubicación de la aplicación


    .. image:: img/howtoinstall_xpm.png


5. Abrir un terminal (cmd) y ejecutar los siguientes comandos:

Ejecutar el comando abajo para entrar en la carpeta donde está el programa **install_requirements.bat**:

    .. code-block:: text

       cd <LOCAL DE INSTALACAO XPM>\xml

Ejemplo:

    .. image:: img/installation_configure_xpm_01.png

Resultado esperado:

    .. image:: img/installation_configure_xpm_02.png


Ejecutar el comando abajo para instalar los requisitos **install_requirements.bat**:

    .. code-block:: text

      install_requirements.bat

Ejemplo:

    .. image:: img/installation_configure_xpm_03.png

Resultado esperado:

    .. image:: img/installation_configure_xpm_04.png
    .. image:: img/installation_configure_xpm_05.png
    .. image:: img/installation_configure_xpm_06.png


Markup
======

1. Instalar y/o verificar los `requisitos <es_installation_requirements.html>`_
2. Descargar el `instalador <es_installation_download.html>`_
3. Ejecutar el instalador
4. Configurar:

   - **Application's folder:** complete con el nombre de la aplicación que presentará en el Menú de Programas
   - **URL:** dirección del sitio público de la colección
   - **Programs's destination folder:** ubicación de la carpeta de los programas (**bin**)
   - **Data destination folder:** ubicación de la carpeta de los datos (**serial**). Repetir el mesmo valor de lo anterior.

    .. image:: img/installation_setup.jpg


5. Seleccionar:

   - **Markup**: programa para identificar elementos de un artículo/texto
   - **Markup - Archivos Automata** (opcional): ejemplos de archivos para marcaje automática de referencias bibliográficas


    .. image:: img/howtoinstall_programs.png


6. Abrir un terminal (cmd) y ejecutar los siguientes comandos:

    Ejecutar el comando abajo para entrar en la carpeta donde está el programa **install_requirements.bat**:

        .. code-block:: text

           cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    Ejemplo:

        .. image:: img/installation_requirements_mkp_01.png

    Resultado esperado:

        .. image:: img/installation_requirements_mkp_02.png


    Ejecutar el comando abajo para instalar los requisitos **install_requirements.bat**:

        .. code-block:: text

          install_requirements.bat

    Ejemplo:

        .. image:: img/installation_requirements_mkp_03.png

    
    Este comando ejecutará varias líneas, pero el resultado principal esperado es:

        .. image:: img/installation_requirements_mkp_04.png


SciELO PC Programs Completo: Title Manager, Converter, Markup, XPM etc
======================================================================

1. Instalar y/o verificar los `requisitos <es_installation_requirements.html>`_
2. Descargar el `instalador <es_installation_download.html>`_
3. Ejecutar el instalador

4. Configurar:

   - **Application's folder:** complete con el nombre de la aplicación que presentará en el Menú de Programas
   - **URL:** dirección del sitio público de la colección
   - **Programs's destination folder:** ubicación de la carpeta de los programas (**bin**)
   - **Data destination folder:** ubicación de la carpeta de los datos (**serial**). 


    .. image:: img/installation_setup.jpg


5. Seleccionar los programas:

  - Title Manager: programa para manejar las bases de revistas y números
  - Converter: programa para convertir los documentos marcados para la base de datos
  - XML SciELO: (opcional) programa para generar XML en el formato de Pubmed


    .. image:: img/howtoinstall_programs.png

6. Abrir un terminal (cmd) y ejecutar los siguientes comandos:

    Ejecutar el comando abajo para entrar en la carpeta donde está el programa **install_requirements.bat**:

        .. code-block:: text

          cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    Ejemplo:


        .. image:: img/installation_requirements_mkp_01.png


    Resultado esperado:


        .. image:: img/installation_requirements_mkp_02.png


    Ejecutar el comando abajo para instalar los requisitos **install_requirements.bat**:

        .. code-block:: text

          install_requirements.bat

    Ejemplo:

        .. image:: img/installation_requirements_mkp_03.png

    
    Este comando ejecutará varias líneas, pero el resultado principal esperado es:

        .. image:: img/installation_requirements_mkp_04.png


===============
Cómo configurar
===============

XML Package Maker and XML Markup
================================

Por stándar el programa funciona considerando acceso a Internet disponible, ausencia de proxy para acceso a Internet y uso de packtools como validador de estrutura de XML (en lugar de style-checker).

Para los casos en que el acceso a Internet es hecho via proxy o no hay acceso a Internet es necesario editar el archivo scielo_env.ini disponible en ?/bin/ con los siguientes parámetros:

  .. code:: text

    PROXY_ADDRESS=(IP:PUERTA de proxy)
    ENABLED_WEB_ACCESS=off (si no hay Internet)
    XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER=packtools|java (en este caso la validación es hecha preferencialmente usando la herramienta packtools, en lugar de la validación con style checker(Java).


Ejemplo de los parámetros preenchidos:

  .. code::

    PROXY_ADDRESS=123.456.789:1234
    ENABLED_WEB_ACCESS=off
    XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER=java|packtools


Title Manager y Converter
=========================

Configurar la variable de ambiente BAP:

  Configure OS23470a en la variable de entorno BAP, accediendo al menú de Windows: Panel de control -> Rendimiento y mantenimiento -> Sistema -> Configuración avanzada -> Variables de entorno.

  Verifica si la variable ya existe. 
  Si no existe, haga clic en Nuevo e ingrese el valor.


    .. image:: img/installation_setup_bap.jpg


XML Converter
=============

PDF, XML y imagens para el sitio local
--------------------------------------

Para que XML Converter copie los archivos pdf, img, xml para el sitio local, editar el archivo correspondiente a **c:\\scielo\\bin\\scielo_paths.ini**, en la línea:

.. code::

  SCI_LISTA_SITE=c:\home\scielo\www\proc\scilista.lst

Reemplazar **c:\\home\\scielo\\www** por la ubicación del sitio local. Por ejemplo:

.. code::

  SCI_LISTA_SITE=c:\var\www\scielo\proc\scilista.lst


Validación de tablas y fórmulas
-------------------------------

El stándar de exigencia para tablas y fórmulas es que ellas estén codificadas.

Para cambiar el nível de exigencia, editar el archivo que corresponde a **c:\\scielo\\bin\\scielo_collection.ini**:

.. code::

  CODED_FORMULA_REQUIRED=off
  CODED_TABLE_REQUIRED=off


**off** es para que XML Converter no exija los elementos codificados.


Menú de aplicación
==================

A veces, el menú de la aplicación se creará solo por el usuario administrador.

.. code::

  C:\\Documents and Settings\\Administrador\\Menu Iniciar\\Programas

En este caso, copie la carpeta SciELO para la carpeta Todos los usuarios, para que todos los usuarios tengan el menú.

.. code::

  C:\\Documents and Settings\\All Users\\Menu Iniciar\\Programas

