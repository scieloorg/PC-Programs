.. pcprograms documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Markup
======

Markup program is a desktop Application (macro in Microsoft Office Word), to identify bibliographic elements in the articles and texts, according to SciELO DTD for `article <dtd.html#article>`_ and for `text <dtd.html#text>`_, based on standard ISO 8879-1986 (SGML - Standard Generalized Markup Language) and ISO 12083-1994 (Electronic Manuscript Preparation and Markup).


Functionalities
---------------

- identify the bibliographic elements in a .doc or .html file
- identify the elements of references semiautomatically
- validate the identification according to `article <dtd.html#article>`_ and for `text <dtd.html#text>`_
- generate XML files according to `http://dtd.nlm.nih.gov/publishing/3.0/`.
- validate XML files according to `http://dtd.nlm.nih.gov/publishing/3.0/`.


Before starting
---------------

File specification
..................

- one article/text by file
- .doc or .html
- same name of the corresponding PDF file
- location of .doc or .html file: /scielo/serial/<acron>/<issue_identification>/pmc/pmc_markup
- location of the other files: /scielo/serial/<acron>/<issue_identification>/pmc/src (images, PDF, etc)

.. image:: img/markup_file_system.png


Input files
...........

Title Manager  and Code Manager programs generate, in the `local server <concepts.html#local-server>`_, at /scielo/bin/markup/, the following files:

- ??_attb.mds - updated when code database is updated
- ??_issue.mds - updated when any issue number's data is updated/created
- issue.mds - updated when any issue number's data is updated/created
- journal-standard.txt - updated when any journal's data is updated/created

Opening the program
-------------------

By the menu, selecting **SciELO** > **Markup**:

.. image:: img/markup_open.jpg

By the path of the program, clicking on markup.exe: 

  c:\\scielo\\bin\\markup\\markup.exe


Setting the Word path
.....................

Markup will try to open the Microsoft Office Word Program. If it is not in the correct path, Markup program will ask for the right path of Microsoft Office Word Program.

.. image:: img/markup_word_path.jpg

Or edit, c:\\scielo\\bin\\markup\\start.mds, inserting the Microsoft Office Word path:

  "c:\\arquivos de programas\\microsoft office\\office11\\winword.exe"


Enabling macro execution
........................

Possibly an warning about enable macro will be displayed.

.. image:: img/markup_2007_habilitar_macros.jpg


Markup button
.............

If Word program opens properly, Markup bar will appear at the bottom of the screen.

.. image:: img/markup_botao_markup.jpg


In Word 2007, it is different. The Markup bar will appear inside the Supplement group.

.. image:: img/markup_2007_botao_suplementos.jpg


Loading macro manually
......................

If there is no Markup button. You can try to load the macro manually.

Select the  Tools->Supplements and Models option of the menu.

.. image:: img/markup_habilitarmacro.jpg


Remove the incorrect item and inform the right path corresponding to c:\\scielo\\bin\\markup\\markup.prg.

.. image:: img/markup_habilitarmacro2.jpg


Using the program
-----------------

Markup button
.............

If Word program opens properly, the Markup bar will appear at the bottom of the screen.

.. image:: img/markup_botao_markup.jpg


In Word 2007, it is different. The Markup bar will appear inside the Supplement group.

.. image:: img/markup_2007_botao_suplementos.jpg


Opening a file
..............

#. Open an article or a text file (.doc or .html).

#. Click on Markup button

#. Click on Markup DTD-SciELO.



The Word bars will disappear, remaining only the Markup bars:

- white: files operations, edit or eraser a tag, automatic markup
- orange: floating tags, can be used in any part of the document
- green: tags in a hierarchical structure

.. image:: img/markup_barras.jpg


In Word 2007, all these tags bars are agrouped in Supplements.

.. image:: img/markup_2007_posicao_das_barras.jpg


The bars
--------
General bar
...........

    .. image:: img/markup_main_bar.png

Exit button
...........
To exit the program, click on Exit button.

    .. image:: img/en/markup_main_bar_exit.jpg

Choose one of the options bellow.

    .. image:: img/en/markup_exit_message.png

Element's attribute edition button
..................................

To edit attributes of an element, select the name element, then click on the edit (pencil) button. The program will ask for changing the values of the attributes.

   .. image:: img/en/markup_main_bar_edit_attr.jpg


Delete element button
.....................

To delete one element and its attributes, select the element name, then click on the delete button. The program will ask to confirm this action.

    .. image:: img/en/markup_main_bar_del.JPG


Save file button
................
To save a file, click on the save button.

    .. image:: img/en/markup_main_bar_save.JPG


Automata 1 button
.................

To mark bibliographic references automatically:

- the journal have to have an Automata file (read `how to programming an automata <automata.html>`_), which configures the rules to identify the references elements.
- select one bibliographic reference until its final dot, including, and then click on the Automata 1 button.

    .. image:: img/en/markup_main_bar_auto1.JPG

This action will activate a tool which will try to identify the bibliographic reference elements automatically. The tool will present the several possibilities of identification. So the user have to select the correct one. 


    .. image:: img/en/automata1b.jpg



Automata 2 Button
.................

To mark a set of bibliographical references automatically (available only for Vancouver standard).
Select one or more bibliographic references and then click on the Automata 2 button. 

    .. image:: img/en/markup_automata2_select.jpg

    .. image:: img/en/markup_main_bar_auto2.JPG


The program will mark all references it can identify and will also keep the original reference, marked as [text-ref]. Thus the user can compare them in order to check if the reference was correctly identified and proceed the correction, if it is necessary.

    .. image:: img/en/markup_automata2_marcado.jpg



Validate markup button
......................

To validate the markup, click on the **Validate markup** button. 
It will run the `SGML Parser <parser.html>`_.


    .. image:: img/en/markup_main_bar_parser.JPG



Floating tag bar
----------------

    .. image:: img/en/markup_bar_floating.png

The floating elements are the ones which can appear in any part of the text.

aff  
    identifies an author affiliation
ign 
    identifies a text which can be ignored
tabwrap 
    (only valid for XML PMC)
figgrps 
    (only valid for XML PMC)
figgrp 
    (only valid for XML PMC)
equation 
    (only valid for XML PMC)
cltrial 
    identifies clinical trials data
list
    (only valid for XML PMC)
xref 
    (only valid for XML PMC)
uri 
    (only valid for XML PMC)
sciname
    (only valid for XML PMC)

Hierarchical tags bar
---------------------

This bar groups the elements according to the DTD. This bar will present the elements of one hierarchical level each time. As the user goes to a down or up level, the bar presents respectively, only the down or up level. The user goes to a down level, when clicks on an element or on a down arrow, and goes to an up level, clicking on the up arrow.

If there is no element marked in the text, then the initial elements buttons (article and text) are presented.

    .. image:: img/en/markup_inicial.jpg

If there are any element marked in the text, the level just below the article or text are presented.

    .. image:: img/en/markup_barra_hierarquica.jpg

Navegation
..........

The down and up arrows  are to navegate between hierachical elements levels. The user should find the elements to mark in the bars.

Clicking on the down arrow next to bibcom, its children (hierarchical related) will appear.

Clicking on the up arrow, at the right side of the bar, the elements of the superior level will appear.

   .. image:: img/en/markup_barra_hierarquica2.jpg

For example: 

Down
....
Bar of **front** element

    .. image:: img/en/markup_barra_front.jpg

Bar of **front** element's children

    .. image:: img/en/markup_barra_titlegrp.jpg

Bar of **titlegrp** element's chidren

    .. image:: img/en/markup_barra_title.jpg

Up
..
    .. image:: img/en/markup_barra_title_sobe.jpg

    .. image:: img/en/markup_barra_titlegrp_paracima.jpg

    .. image:: img/en/markup_barra_front_0.jpg

Error messages
--------------

To avoid errors and to guide the user during the markup, the program presents some messages in case the procedures described previously have not been correctly done. For example:

- If the user has clicked on an element button and no text was selected.
- If a mandatory atribute value wasn't filled in.
- If the user try to insert a tag in an incorrect place, disaccording to DTD.

    .. image:: img/en/markup_msg_01.jpg

    Bad value to a mandatory attribute


    .. image:: img/en/markup_msg_02.jpg

    The user tried to identify an element which is not according to the hierarchical structure / DTD


    .. image:: img/en/markup_msg_03.jpg

    the user has clicked on an element button and no text was selected

