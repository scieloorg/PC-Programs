
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
::::::::::::::::::::::

Presents the total of fatal errors, errors, and warnings, found in the whole package.

FATAL ERRORS
   represents errors related to Bibliometrics Indicators.

ERRORS
   represents other types of errors

WARNINGS
   represents something that needs more attencion


.. image:: img/xpm_report.png


Detail report
..............

Presents the documents in a table.

The columns order, aop pid, toc section, @article-type are hightlighted because contains important data.

The column "reports" contains "buttons" to open/close the detail reports of each document.


.. image:: img/xpm_report_detail.png

Detail report - Validations
:::::::::::::::::::::::::::

Click on "Data Quality Control" to view the problems.
The detail report is displayed below the row


.. image:: img/xpm_report_detail_validations.png


Folders/Files
.............

Displays the files/folders which are inputs and outputs.

.. image:: img/xpm_report_folder.png


Overview report
...............

Overview report - languages
:::::::::::::::::::::::::::

Displays the elements which contains @xml:lang. 

.. image:: img/xpm_report_overview_lang.png

Overview report - dates
:::::::::::::::::::::::

Displays the dates found in the document: publication and history.
Displays the spent time between received and accepted, accepted and published, accepted and the present date.

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






----------------

Last update of this page: August, 2015
