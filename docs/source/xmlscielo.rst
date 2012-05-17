.. pcprograms documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

XML SciELO
==========
- DOS Batch program
- local server

This program generates XML and SGML files to PubMed and ISI.

For PubMed, there are two types of files:

- Journal data: 
    http://www.ncbi.nlm.nih.gov/books/bv.fcgi?rid=helplinkout.section.files.Resource_File#files.Resource_File_Format. 
    Sent once or every time the journal data was changed.

- Articles data: 
    http://www.ncbi.nlm.nih.gov/entrez/query/static/spec.html 
    Sent one XML file for each issue.


Installation
------------
This program is installed in PROGRAMS_PATH on the local Server using the SciELO PC-Programs package, where PROGRAMS_PATH is the path for all the SciELO PC programs.

The examples are considering PROGRAMS_PATH equal to c:\\scielo\\.

It is also necessary to install java, if there is no java installed.


Configuration
-------------
Configuring the files and paths
...............................

Some configurations are done automatically as installing the PC Programs. The configuration files for all the PC Programs is c:\\scielo\\bin\\scielo_paths.ini.

This program use the following parameters of this configuration file:

    .. code-block:: text

    ; Serial
    Serial Directory=f:\\serial\\,required
    …
    ; xml_scielo
    XML_SCIELO_PROGRAM_PATH=c:\\scielo\\xml_scielo
    PHP_EXE=c:\\server\\php\\php.exe
    JAVA_EXE=java
    PubMed_DIR_COPY=c:\\scielo\\serial\
    SCI_LISTA_SITE=c:\\scielo\\web\\proc\\scilista.lst
    PubMed_PROVIDER_ID=3081


Serial Directory
    it is the place for all the journal and issues data. So, it indicates to the program where to find the data: c:\\scielo\\serial\\title\\title, c:\\scielo\\serial\\<revistas>\\<issue>\\.

XML_SCIELO_PROGRAM_PATH
    it indicates the place where the programs is installed. E.g.: c:\\scielo\\xml_scielo.

PHP_EXE
    it indicates the full path to php.exe, used for XML transformation. E.g: c:\\server\\php\\php.exe.

JAVA_EXE
    it indicates the full path to java or just java, if it is already in the PATH, used for XML transformation. E.g: java.

PubMed_DIR_COPY
    it indicates the place where there Will be a copy of the generated files.

SCI_LISTA_SITE
    it indicates the list used to generate the website. This program uses this list to create another list, used by itself.

PubMed_PROVIDER_ID
    it is the ID of the provider. SciELO is one of the providers whose ID is 3081, for all the SciELO Collection.



Configuration of the data
-------------------------

If it is the first installation, you have some procedures to execute.

There is a file in c:\\scielo\\xml_scielo\\config.example. You have to copy and rename to **config**. 

Configure the files:

- PubMed\\doi_conf.txt
- PubMed\\config\\config.seq
- PubMed\\journals\\journals.seq  


File doi_conf.txt
.................

It contains the data of the Publisher and the prefix given by CrossRef, according to the agreement signed by CrossRef and the SciELO of each country. IF YOUR SCIELO DOES NOT HAVE IT. SO THIS FILE MUST BE EMPTY.


   INSTITUTION SPACE E-MAIL SPACE PREFIX


   .. image:: img/en/xml_scielo_doiconf.jpg
 
File config\\config.seq
.......................
The file config\config.seq is to informe to the program which articles or text should not be sent to PubMed, because some kind of documents are not accepted. So by their section in the table of contents it is possible to know if the document would be accept or not. So, this file contains the list of sections whose documents will not be accepted by PubMed.


   Acronym space sectionId

 
   .. image:: img/en/xml_scielo_scilista.jpg


File journals\\journals.seq
...........................
This file journals\\journals.seq contains data used to generate XML file of the journal: journals_acronimo.xml. This is the first XML file which must be sent to PubMed in order to register the journal. Read more: http://www.ncbi.nlm.nih.gov/books/bv.fcgi?rid=helplinkout.section.files.Resource_File#files.Resource_File_Format.

Its format is:


   ACRONYM SPACE FIRST_YEAR_IN_PubMed SPACE SCIELO_URL SPACE ISSN


One line for each journal.


    .. image:: img/en/xml_scielo_journal.jpg

 
Executing
---------

It has to be executed using the command line in DOS. 

    .. image:: img/en/xml_scielo_doscommand.jpg

 
Go to the folder where this program is installed. E.g.: c:\\scielo\\xml_scielo\\proc\\.

    .. image:: img/en/xml_scielo_doscommand2.jpg

 
In proc you will find three scripts:

- GenerateXML_all.bat: generates at the same time ISI and PubMed
- GenerateXML_ISI.bat: generates SGML to ISI
- GenerateXML_PubMed.bat: generates XML to PubMed


    .. image:: img/en/xml_scielo_doscommand3.jpg


Provide a list similar to scilist, to execute any of them.

The program will open the scilist file and you have to check it, and include or remove lines, according to what you want to generate.


    .. image:: img/en/xml_scielo_doscommand4.jpg


 


To generate also the XML file which contains journal data, journals_<acronimo>.xml, add one more parameter “YES”: 


.. code-block:: text

    hcsm v13n2 YES


To generate ONLY the XML file which contains journal data, journals_<acronimo>.xml, the second parameter must be “NONE” and third one must be YES.

.. code-block:: text

    hcsm NONE YES




