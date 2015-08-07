

.. toctree::
   :maxdepth: 2

=======================
XML Package Maker (XPM)
=======================

It is a tool to generate XML packages for SciELO and PMC.


How to use
----------

Use the Windows menu to open the program.

.. image:: img/scielo_menu_xpm.png



.. image:: img/xpm_gui.png


Select the folder which contains XML package files

.. image:: img/xpm_gui_selected_folder.png


Inform the journal acronym which will be used to form the files and package names

.. image:: img/xpm_acron.png


Press XML Package Maker

It will generate

* XML files for SciELO (scielo_package and/or scielo_package_zips folders)
* XML files for PMC (pmc_package folder)
* report files (errors folder)

in the folder which contains XML package files plus the current time.


.. image:: img/xpm_result_folders.png


Results
-------

After finishing the processing the reports are displayed in a Web browser.

Navigate among the tabs.


Summary report
..............

Validations Statistics
;;;;;;;;;;;;;;;;;;;;;;

Presents the total of fatal errors, errors, and warnings, found in the whole package.

FATAL ERRORS
   represents errors related to Bibliometrics Indicators.

ERRORS
   represents other types of errors

WARNINGS
   represents something that needs more attencion

Conversion Results
;;;;;;;;;;;;;;;;;;

Presents the files according to the conversion results:

converted
   database was successfully generated

deleted incorrect order
   indicates if there are files which "order" was corrected



.. image:: img/xpm_report.png



Detail report
..............

.. image:: img/xpm_report_detail.png


Detail report - Validations
:::::::::::::::::::::::::::

.. image:: img/xpm_report_detail_validations.png


Folders/Files
.............

.. image:: img/xpm_report_folder.png

Overview report
...............

Overview report - languages
:::::::::::::::::::::::::::

.. image:: img/xpm_report_overview_lang.png

Overview report - dates
:::::::::::::::::::::::

.. image:: img/xpm_report_overview_date.png


Overview report - affiliations
::::::::::::::::::::::::::::::


.. image:: img/xpm_report_overview_aff.png

Overview report - references
::::::::::::::::::::::::::::

.. image:: img/xpm_report_overview_ref.png


Sources report
..............

.. image:: img/xpm_report_sources.png

.. image:: img/xpm_report_sources_journals.png

.. image:: img/xpm_report_sources_books.png

.. image:: img/xpm_report_sources_others.png





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
