Sections
========

It manages all the sections of the table of contents of the all the journal issues. 

Opening the journal sections form
---------------------------------

#. Select File-> Open-> Sections

    .. image:: img/en/01_menu_section.jpg

#. Select a title and click on Open button


Sections form
-------------
As opening the form, it will be presented a screen with four columns:

    * Seccode (code sections)
    * titles of the section in Spanish
    * titles of the section in Portuguese
    * titles of the section in English

The code of sections are formed by the `Journal acronym`, followed by 010, or 020, or 030, and, so on.

The title of the sections may or not be in all the languages of the interface.

    .. image:: img/en/01_sec_lista.jpg

    Fig 1a - List of sections of the journal

The list can be rearranged, by clicking on any column. For example, clicking on code column, the list will be sorted by code. 

    .. image:: img/en/01_sec_ordem.jpg

    Fig 1b - List of sections, ordered by the English column

Creating a section
------------------

#. Register the section code according to the format [wiki:en_SciELO_PCPrograms_Title_Manager_TITLE#Preenchimento_de_dados_para_o_site acronym], followed by 010, or 020, or 030, and successively.

    .. image:: img/en/01_sec_code.jpg

    Figure 2 - Field to enter the section code

#. Register the fields for section title

    .. image:: img/en/01_sec_titles.jpg

    Figure 3 - Fields to enter the section titles

#. Click on Insert button
#. Click on Save button

| NOTES:
| Only after clicking on the Save button, the record will be up to date with all the changes.

Editing the section
-------------------

#. Click on the line of the section to edit. Code and section titles go to the fields.

    .. image:: img/en/01_sec_edition.jpg

    Figure 4 - selected section to edit or delete

#. Edit the section titles
#. Click on Insert button

    .. image:: img/en/01_sec_insert.jpg

    Figure 5 - Insert button

#. Click on Save button

| NOTES:
| Only after clicking on the Save button, the record will be up to date with all the changes.
| It is allowed to change only the sections which are not in use.


Deleting a section
------------------
#. Click on the line of the section to be deleted. Section code and titles will go to their fields.

    .. image:: img/en/01_sec_edition.jpg


    Figure 6 - selected section to edit or delete

#. Click on Remove button

    Figure 7 - Remove button

#. Click on Save button

 | NOTES:
 | Only after clicking on the Save button, the record will be up to date with all the changes.
 | It is allowed to change only the sections which are not in use.

    Figure 8 - Buttons: Save, Close, Help


Section database
----------------

ISIS Base. A record by title. Each record contains the following tags:

===  =======================================================================================================================
tag
---  -----------------------------------------------------------------------------------------------------------------------
035  ISSN. Corresponds to the field of 400 TITLE
048  subfield l Language of table of contents' header 
048  subfield h title for table of contents' header  (Table of contents (en), Sumario (pt), Tabla de Contenido (es))
049  subfield c code of the section
049  subfield l language of the section
049  subfield t title of the section
091  Date ISO to register the update date
100  Journal's title. Corresponds to the same field of TITLE.
930  Journal's acronym in uppercase
===  =======================================================================================================================

