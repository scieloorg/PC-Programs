.. pcprograms documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Table of Contents Validations
=============================

Identify the warnings/errors/fatal errors related to the issue.

- Some data must have equal value in all the XML files:

 * journal-title
 * journal id NLM
 * journal ISSN
 * publisher name
 * issue label
 * issue pub date

- Some data must have unique value in all the XML files:

 * doi
 * elocation-id, if it is applicable
 * fpage and fpage/@seq
 * order (used to generated article PID)



TOC Report
----------

Creation date and statistics


 .. image:: img/xml_reports__toc_header.jpg

 
Example of fatal error because of different values for publisher-name. 

 .. image:: img/xml_reports__toc_fatal_error_required_equal_publisher.jpg


Example of fatal error because of different values for pub-date. 

 .. image:: img/xml_reports_toc_fatal_error_required_equal_date.png



Example of fatal error because unique value is required

 .. image:: img/xml_reports_toc_fatal_error_unique.png.jpg
       


----------------

Last update of this page: Oct, 2014

