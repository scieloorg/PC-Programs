Working with XML files
======================

Requirements
------------

Install the softwares below:

  - JAVA (add the java path to PATH, in order to run java from any directory in the computer)
  - Saxon

Download the files below:

  - XSD or DTD  (add XSD path to PATH, in order to run java from any directory in the computer)
  - XSL files (add XSL files' path to PATH, in order to run java from any directory in the computer)



How to validate an XML file
---------------------------


How to convert XML PMC to XML SciELO
------------------------------------

  - Download the XSL to convert XML SciELO to XML PMC v3.0 `xml2pmc.xsl <xml2pmc.xsl>`_
  - Execute in the command line:

  .. code-block::

    java <SAXON> -o <RESULT_FILENAME> <XML_FILENAME> <XSL_FILENAME>



  E.g.:

  .. code-block::
   
    java -jar c:\bin\saxon_9.2\saxon9.jar -o c:\my_results\result.html c:\my_xml_files\article.xml xml2pmc.xsl




How to preview the article
--------------------------

  - Download the XSL to preview the article in HTML format `xml2pmc.xsl <preview.xsl>`_
  - Execute in the command line:

  .. code-block::

    java <SAXON> -o <RESULT_FILENAME> <XML_FILENAME> <XSL_FILENAME>



  E.g.:

  .. code-block::
   
    java -jar c:\bin\saxon_9.2\saxon9.jar -o c:\my_results\result.html c:\my_xml_files\article.xml preview.xsl




