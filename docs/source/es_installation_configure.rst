.. how_to_install:

=============
Cómo instalar
=============

XML Package Maker
=================

1. Instalar y/o verificar los `requisitos <es_installation_requirements.html>`_
2. Fazer el `download <es_installation_download.html>`_ de los instaladores
3. Ejecutar el instalador
4. Indicar la ubicación de la aplicación


    .. image:: img/howtoinstall_xpm.png


5. Abrir un terminal (cmd) y ejecutar los siguientes comandos:

Ejecutar el comando abajo para entrar en la carpeta donde está el programa **install_requirements.bat**:

    .. code-block:: code

       cd <LOCAL DE INSTALACAO XPM>\xml

Ejemplo:

    .. image:: img/installation_configure_xpm_01.png

Resultado esperado:

    .. image:: img/installation_configure_xpm_02.png


Ejecutar el comando abajo para instalar los requisitos **install_requirements.bat**:

    .. code-block:: code

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
2. Fazer el `download <es_installation_download.html>`_ de los instaladores
3. Ejecutar el instalador
4. Configurar:

   - **Application's folder:** complete con el nombre de la aplicación que presentará en el Menú de Programas
   - **URL:** endereço del sitio público de la colección
   - **Programs's destination folder:** ubicación de la carpeta de los programas (**bin**)
   - **Data destination folder:** ubicación de la carpeta de los dados (**serial**). Repetir el mesmo valor del anterior.

    .. image:: img/installation_setup.jpg


5. Seleccionar:

   - **Markup**: program to identify the bibliographic elements in the articles/texts
   - **Markup - Automata files** (opcionalmente): examples of files for automatic markup


    .. image:: img/howtoinstall_programs.png


6. Abrir un terminal (cmd) y ejecutar los siguientes comandos:

    Ejecutar el comando abajo para entrar en la carpeta donde está el programa **install_requirements.bat**:

        .. code-block:: code

           cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    Ejemplo:

        .. image:: img/installation_requirements_mkp_01.png

    Resultado esperado:

        .. image:: img/installation_requirements_mkp_02.png


    Ejecutar el comando abajo para instalar los requisitos **install_requirements.bat**:

        .. code-block:: code

          install_requirements.bat

    Ejemplo:

        .. image:: img/installation_requirements_mkp_03.png

    
    Este comando ejecutará varias líneas, pero el resultado principal esperado es:

        .. image:: img/installation_requirements_mkp_04.png


SciELO PC Programs Completo: Title Manager, Converter, Markup, XPM etc
======================================================================

1. Instalar y/o verificar los `requisitos <es_installation_requirements.html>`_
2. Fazer el `download <es_installation_download.html>`_ de los instaladores
3. Ejecutar el instalador

4. Configurar:

   - **Application's folder:** complete con el nombre de la aplicación que presentará en el Menú de Programas
   - **URL:** endereço del sitio público de la colección
   - **Programs's destination folder:** ubicación de la carpeta de los programas (**bin**)
   - **Data destination folder:** ubicación de la carpeta de los dados (**serial**). 


    .. image:: img/installation_setup.jpg


5. Seleccionar los programas:

  - Title Manager: program to manage journals and issues databases
  - Converter: program to load the marked documents into the database
  - XML SciELO: (opcional) program to create XML format for PubMed


    .. image:: img/howtoinstall_programs.png

6. Abrir un terminal (cmd) y ejecutar los siguientes comandos:

    Ejecutar el comando abajo para entrar en la carpeta donde está el programa **install_requirements.bat**:

        .. code-block:: code

          cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    Ejemplo:

        .. image:: img/installation_requirements_mkp_01.png

    Resultado esperado:

        .. image:: img/installation_requirements_mkp_02.png


    Ejecutar el comando abajo para instalar los requisitos **install_requirements.bat**:

        .. code-block:: code

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

Editar el archivo **c:\\scielo\\bin\\scielo_env.ini**, somente se la situación es diferente de la padrão:

  - sín proxy
  - con Internet
  - packtools


  .. code::

    PROXY_ADDRESS=123.456.789:1234
    ENABLED_WEB_ACCESS=off
    XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER=packtools|java


Complete **PROXY_ADDRESS**, se há un proxy para acceder la Internet

Indique off para ENABLED_WEB_ACCESS, se no há accede la Internet

Indique la ordem de preferência de los validadores de XML


Title Manager y Converter
=========================

Configurar la variável de ambiente:

  Set OS23470a to the environment variable BAP, by acccedeng the Windows menu: Control Panel -> Performance and Maintenance -> System -> Advanced Settings -> Environment variables.

  Check if the variable already exists. 
  If it does not, click New and enter the value.

    .. image:: img/installation_setup_bap.jpg


XML Converter
=============

PDF, XML y imagens para el sitio local
--------------------------------------

Para que XML Converter copie los archivos pdf, img, xml para el sitio local, edite el archivo correspondiente a **c:\\scielo\\bin\\scielo_paths.ini**, en la linha:

.. code::

  SCI_LISTA_SITE=c:\home\scielo\www\proc\scilista.lst

Reemplazar **c:\\home\\scielo\\www** por la ubicación del sitio local. Por ejemplo:

.. code::

  SCI_LISTA_SITE=c:\var\www\scielo\proc\scilista.lst


Validación de tabelas y fórmulas
-------------------------------

O padrão de exigência para tabelas y fórmulas es que elas seja codificadas.

Para alterar este nível, edite el archivo que correspond la **c:\\scielo\\bin\\scielo_collection.ini**:

.. code::

  CODED_FORMULA_REQUIRED=off
  CODED_TABLE_REQUIRED=off


**off** es para que el XML Converter no exija los elementos codificados


Menu de aplicación
=================

Sometimes the menu of the application will be created only for the Administrator user. 

.. code::

  C:\\Documents and Settings\\Administrador\\Menu Iniciar\\Programas

In this case, copy the SciELO folder to All Users folder, to all users have the menu.

.. code::

  C:\\Documents and Settings\\All Users\\Menu Iniciar\\Programas

