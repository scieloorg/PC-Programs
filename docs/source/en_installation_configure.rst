.. how_to_install:

===============
How to install
===============

XML Package Maker
=================

1. Install and/or check the `requirements <en_installation_requirements.html>`_
2. Download the `installer <en_installation_download.html>`_
3. Run the installer
4. Inform the application location


    .. image:: img/howtoinstall_xpm.png


5. Open a terminal (cmd) and execute the following commands:

Execute the command below to go to the folder where the script **install_requirements.bat** is:

    .. code-block:: text

       cd <LOCAL DE INSTALACAO XPM>\xml

For instance:

    .. image:: img/installation_configure_xpm_01.png

Expected:

    .. image:: img/installation_configure_xpm_02.png


Execute the command below to install the requirements **install_requirements.bat**:

    .. code-block:: text

      install_requirements.bat

For instance:

    .. image:: img/installation_configure_xpm_03.png

Expected:

    .. image:: img/installation_configure_xpm_04.png
    .. image:: img/installation_configure_xpm_05.png
    .. image:: img/installation_configure_xpm_06.png


Markup
======

1. Install and/or check the `requirements <en_installation_requirements.html>`_
2. Download the `installer <en_installation_download.html>`_
3. Run the installer
4. Configure:

   - **Application's folder:** complete with the application name for the Programs Menu
   - **URL:** SciELO Collection URL
   - **Programs's destination folder:** location of the programs folder (**bin**)
   - **Data destination folder:** location of the data folder (**serial**). Repeat the same value of the previous field.

    .. image:: img/installation_setup.jpg


5. Select:

   - **Markup**: program to identify the bibliographic elements in the articles/texts
   - **Markup - Automata files** (opcionalmente): examples of files for automatic markup


    .. image:: img/howtoinstall_programs.png


6. Open a terminal (cmd) and execute the following commands:

    Execute the command below to go to the location of **install_requirements.bat**:

        .. code-block:: text

           cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    For instance:

        .. image:: img/installation_requirements_mkp_01.png

    Expected:

        .. image:: img/installation_requirements_mkp_02.png


    Execute the command below to install the requirements **install_requirements.bat**:

        .. code-block:: text

          install_requirements.bat

    For instance:

        .. image:: img/installation_requirements_mkp_03.png

    
    This command will display several lines, the main result expected is:

        .. image:: img/installation_requirements_mkp_04.png


SciELO PC Programs Completo: Title Manager, Converter, Markup, XPM etc
======================================================================

1. Install and/or check the `requirements <en_installation_requirements.html>`_
2. Download the `installer <en_installation_download.html>`_
3. Run the installer

4. Configure:

   - **Application's folder:** complete with the application name for the Programs Menu
   - **URL:** SciELO Collection URL
   - **Programs's destination folder:** location of the programs folder (**bin**)
   - **Data destination folder:** location of the data folder (**serial**). 


    .. image:: img/installation_setup.jpg


5. Select the programas:

  - Title Manager: program to manage journals and issues databases
  - Converter: program to load the marked documents into the database
  - XML SciELO: (opcional) program to create XML format for PubMed


    .. image:: img/howtoinstall_programs.png

6. Open a terminal (cmd) and execute the following commands:

    Execute the command below to go to the location of  **install_requirements.bat**:

        .. code-block:: text

          cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    For instance:


        .. image:: img/installation_requirements_mkp_01.png


    Expected:


        .. image:: img/installation_requirements_mkp_02.png


    Execute the command below to install the requirements **install_requirements.bat**:

        .. code-block:: text

          install_requirements.bat

    For instance:

        .. image:: img/installation_requirements_mkp_03.png

    
    This command will display several lines, the main result expected is:

        .. image:: img/installation_requirements_mkp_04.png


================
How to configure
================

XML Package Maker and XML Markup
================================

Edit the file **c:\\scielo\\bin\\scielo_env.ini**, only if the situation is different from the standard:

  - no proxy
  - Internet access
  - packtools as XML Validator


  .. code::

    PROXY_ADDRESS=123.456.789:1234
    ENABLED_WEB_ACCESS=off
    XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER=packtools|java


Complete **PROXY_ADDRESS**, if there is a proxy to access the Internet

Inform off to ENABLED_WEB_ACCESS, if there is no access to the Internet

Inform preference order to use XML Validators


Title Manager and Converter
===========================

Configure the environment variable BAP:

  Set OS23470a to the environment variable BAP, by acccedeng the Windows menu: Control Panel -> Performance and Maintenance -> System -> Advanced Settings -> Environment variables.

  Check if the variable already exists. 
  If it does not, click New and enter the value.


    .. image:: img/installation_setup_bap.jpg


XML Converter
=============

PDF, XML and imagens to the sitio local
---------------------------------------

Inform to XML Converter the location of local web site in order the PDF, XML and images files be copied to the local web site. 
Edit the file **c:\\scielo\\bin\\scielo_paths.ini**, the line:

.. code::

  SCI_LISTA_SITE=c:\home\scielo\www\proc\scilista.lst

Replace **c:\\home\\scielo\\www** by the local web site location. For instance:

.. code::

  SCI_LISTA_SITE=c:\var\www\scielo\proc\scilista.lst


Validation of tables and formulas
---------------------------------

Tables and formulas are required to be codified by default.

To change this level of demanding, edit the corresponding file: **c:\\scielo\\bin\\scielo_collection.ini**:

.. code::

  CODED_FORMULA_REQUIRED=off
  CODED_TABLE_REQUIRED=off


Set to **off** not to require codified table and formula.


Application Program Menu
========================

Sometimes the menu of the application will be created only for the Administrator user. 

.. code::

  C:\\Documents and Settings\\Administrador\\Menu Iniciar\\Programas

In this case, copy the SciELO folder to All Users folder, to all users have the menu.

.. code::

  C:\\Documents and Settings\\All Users\\Menu Iniciar\\Programas

