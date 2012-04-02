.. pcprograms documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Markup
======


- single-user program, built in Visual Basic for Application Word, to descentralized use in any workstation. 
   Its installation can be done in distinct computer, others than [wiki:en_SciELO_Metodologia_Conceitos#servidorLocal local server].
- tool to identify bibliographic elements in the articles and texts, according to [wiki:SciELO_DTD DTD SciELO], based on standard ISO 8879-1986 (SGML - Standard Generalized Markup Language) and ISO 12083-1994 (Electronic Manuscript Preparation and Markup).

With this program, the user can:

- open the articles or text files
- identify the bibliographic elements in the file, by select them with the mouse or keyboard and then tagging them, according DTD
- markup bibliographics references semiautomatically
- validate the markup according to [wiki:SciELO_DTD DTD SciELO]
- generate XML PMC [http://dtd.nlm.nih.gov/publishing/3.0/]. Read the instructions given by [wiki:en_MarkupPubMedCentral PubMed Central].
- preview the text generated from XML PMC

Before using the Markup
-----------------------

- you must have one article or text by file
- check if the file contents is same of printed version or PDF file
- check if the file format is HTML, .doc, .rtf
- check if the number which the articles belong is recorded in title and issue databases
- If the markup will be done in a different machine than [wiki:en_SciELO_Metodologia_Conceitos#servidorLocal local server], copy  the files bellow from (local server)\bin\markup :
    - ??_issue.mds - it is updated when a new issue data is input on or modified in the database 
    - issue.mds - it is updated when a new issue data is input on or modified in the database 
    - ??_attb.mds - it is updated when a new code table data is input on or modified in the database
    - automata.mds - it is updated when a new title data is input on or modified in the database 
    - journal-standard.txt - it is updated when a new issue data is input on or modified in the database 

Open the program
----------------

Go to the menu, select "SciELO" and "Markup"

    .. image:: img/en/markup_abrir_programa.jpg

The program will try to open the Microsoft Word Program which is set in the file bin\markup\start.mds.

If the path is not valid, the program will ask for the right path of Microsoft Word Program.

Other option is to change this path by editing the bin\markup\start.mds file.

    .. image:: img/en/markup_word_path.jpg


Just in case it doesn't appear the message about macro execution, you need to drop the macro's security level down. 

In Word 2003, it appears as following:

    .. image:: img/en/markup_2007_habilitar_macros.jpg


If Word program opens correctly, the Markup bar will appear at the inferior part of the screen.

    .. image:: img/en/markup_botao_markup.jpg


In Word 2007, it is different. The Markup bar will appear inside the Supplement group.

    .. image:: img/en/markup_2007_botao_suplementos.jpg


Open an article or a text file.

As clicking on Markup button, two options will be shown: configuration and Markup DTD-SciELO.

In Word 2007:

    .. image:: img/en/markup_2007_botao_abrir_markup.jpg

If the macro was not loaded normally, the message bellow will appear:

    .. image:: img/en/markup_loadproblem.JPG

To solve it, select the  Tools->Supplements and Models option of the menu.

    .. image:: img/en/markup_habilitarmacro.JPG


So, remove the incorrect item, and put on the right path file corresponding of c:\scielo\bin\markup\markup.prg.

    .. image:: img/en/markup_habilitarmacro2.JPG


Using the program
-----------------

Open a .html or .doc file.

Click on Markup DTD-SciELO to start the markup.


The Word bars will disappear, remaining only the Markup bars:

- white: files operations, edit or eraser a tag, automatic markup
- orange: floating tags, can be used in any document part
- green: tags that have a specific hierarchy of DTD

    .. image:: img/en/markup_barras.jpg

In Word 2007, all these tags bars are agrouped in Supplements.

    .. image:: img/en/markup_2007_posicao_das_barras.jpg


The markup starts when you click on document type button:
    Article
        specifies scientific articles. They must have key-words, abstracts and bibliographic references. It is accounted in bibliometric module as scientific production.
    Text
        specifies texts that are part of a journal, but don't have scientific worth. Ex.: Editorial, interview, review, etc.

The bars
--------
General bar
...........
Exit button
...........
To exit the program, click on Exit button.

    .. image:: img/en/markup_botao_sair.jpg

Choose one of the options bellow.

    .. image:: img/en/markup_botao_sair_pergunta.jpg

Element's attribute edition button
..................................

To edit attributes of an element, select the name element, then click on the edit (pencil) button. The program will ask for changing the values of the attributes.

   .. image:: img/en/markup_botao_editar.jpg


Delete element button
.....................

To delete one element and its attributes, select the element name, then click on the delete button. The program will ask to confirm this action.

    .. image:: img/en/markup_botao_apagar.jpg


Save file button
................
To save a file, click on the save button.

    .. image:: img/en/markup_botao_salvar.jpg


Automata 1 button
.................
To mark bibliographic references automatically:
- the journal have to have an [wiki:SciELO_PCPrograms_Automata Automata] file, which configures the rules to identify the references elements.
- select one bibliographic reference until its final dot, including, and then click on the Automata 1 button.

    .. image:: img/en/markup_botao_auto1.jpg

This action will activate a tool which will try to identify the bibliographic reference elements automatically. The tool will present the several possibilities of identification. So the user have to select the correct one. 


    .. image:: img/en/automata1b.jpg



Automata 2 Button
.................

To mark a set of bibliographical references automatically (available only for Vancouver standard).
Select one or more bibliographic references and then click on the Automata 2 button. 

    .. image:: img/en/markup_automata2_select.jpg

    .. image:: img/en/markup_botao_auto2.jpg


The program will mark all references it can identify and will also keep the original reference, marked as [text-ref]. Thus the user can compare them in order to check if the reference was correctly identified and proceed the correction, if it is necessary.

    .. image:: img/en/markup_automata2_marcado.jpg



Validate markup button
......................

To validate the markup, click on the ''Validate markup'' button. 
It will run the [wiki:en_SciELO_PCPrograms_SGMLParser SGML Parser].

    .. image:: img/en/markup_botao_parser.jpg

XML generate button
...................
To generate XML PMC, the user must garantee that xmlbody element and all figures and tables had been marked, and click on the button.
The program will generate two XML files:
- XML PMC 
- XML PMC adapted to SciELO (<file_name>.scielo.xml) 
and it will validate them.


| Note: If you have any questions about XML PMC, read `PMC Files Specifications` <http://www.ncbi.nlm.nih.gov/pmc/about/PMC_Filespec.html>  
| This include nomenclature files rules


    .. image:: img/en/markup_botao_gerarxml.jpg

Preview text button (fulltext, no tags, generated from XML file)
................................................................

To preview the text, generated from XML file, in order to check if how the fulltext will be presented in the website, click on the ''Preview text'' button. 

    .. image:: img/en/markup_botao_view.jpg


Markup button
-------------

After previewing the text, click on the Markup button to see the marked text.

    .. image:: img/en/markup_botao_view_markup.jpg


Help
....

Floating tag bar
----------------

    .. image:: img/en/markup_barra_flutuante.jpg

The floating elements are the ones which can appear in any part of the text.

aff  
    identifies an author affiliation
ign 
    identifies a text which can be ignored
tabwrap 
    identifies a table (includes label, caption and image)
figgrp 
    identifies a figure (includes label, caption and image)
equation 
    identifies an equation (represented by image or LaTex or mml:math)
cltrial 
    identifies clinical trials data
xref 
    identifies a cross reference
uri 
    identifies a link

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
Bar of "front" element

    .. image:: img/en/markup_barra_front.jpg

Bar of "front" element's children

    .. image:: img/en/markup_barra_titlegrp.jpg

Bar of "titlegrp" element's chidren

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

