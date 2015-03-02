
XML Converter
=============

Script to generate the base folder for a given a XML package.


Executing
---------

Usage:

1. Opena a DOS session


2. Go to the script location

.. code::

    cd \scielo\bin\xml


3. Use the command 

.. code::

    python xml_converter.py <parameter_1>


where

    <parameter_1>: path of the folder where there are the XML files and related files, such as PDF, ePub, etc.
    

 .. image:: img/xml_reports_converter_call.png


Report location
---------------

If it converts fine, the reports, base, and other files/folders are generated in the *issue folder* in *serial* folder.

 .. image:: img/xml_reports_converter_prompt_end_ok.png



If it does not convert, the reports are generated in the given XML folder.

 .. image:: img/xml_reports_converter_prompt_end.png



After the processing, with failure or success, XML Converter Report displays the report in your Web browser.

 .. image:: img/xml_reports_converter_result_html.png


 .. image:: img/xml_reports_converter_result_browser_fail.png



Report content: Header
--------------

 .. image:: img/xml_reports_converter_list.jpg


Report content: Statistics of XML and Data Validations
--------------


 Displays the statistics of the total of warnings/errors/fatal errors in the package.

 
 .. image:: img/xml_reports_converter_statistics.jpg


Report content: TOC Report
--------------

If there are FATAL ERRORS in Table of Contents Validations, the conversion is interrupted.

It is mandatory to fix the problems before continue.

Click on the "toc.html" link in order to display the `TOC Report <xml_reports_toc.html>`_ the problems.


 .. image:: img/xml_reports_converter_toc_fail.jpg



If there is no FATAL ERROR in Table of Contents Validations, the conversion continues.


 .. image:: img/xml_reports_converter_toc_not_fail.jpg



If there is no ERROR related to Table of Contents, the "toc.html" link is not displayed.


 .. image:: img/xml_reports_converter_author_source.png


Report content: Articles validations
--------------

And in the sequence, for each XML file the result of the validations (DTD, style, data) and other validations is displayed:

 * previous version of the article (ahead of print)
 * section
 * display @article-type and section



 .. image:: img/xml_reports_converter_article.png


 .. image:: img/xml_reports_converter_article2.png



Section
'''''''

If the article was previously published as ahead of print, the converter remove the previous version.

 .. image:: img/xml_reports_converter_exahead.png


ex-ahead
'''''''

If an article has a section which is not registered in issue database, the converter do not allow its conversion.

 .. image:: img/xml_reports_converter_section_error.png


Report content: Result
----------------

At the end, a summary of the processing is displayed

 .. image:: img/xml_reports_converter_end.png



Folders/Files resulting of the processing
-----------------------------------------

Converted
.........

 .. image:: img/xml_reports_converter_resulting_files_and_folders.png


 * base
 * base_reports: result of this processing
 * base_source: xml package
 * id: for usage of converter. Do not delete.


.. image:: img/xml_reports_converter_resulting_files_and_folders.png


Not converted
.............

If it does not convert, the reports are generated in the given XML folder.


 .. image:: img/xml_reports_converter_reports_folder_begin.png

 .. image:: img/xml_reports_converter_reports_folder_end.png



 

----------------

Last update of this page: Octubre, 2014
