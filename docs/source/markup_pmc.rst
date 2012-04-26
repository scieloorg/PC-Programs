.. pcprograms documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Markup PMC
==========

Use the same Markup Program. So, read its documentation.

And use a copy of the markup file to generate the XML file to PMC.

The PMC Markup will be done on a copy of a markup file.

PMC Files Specifications: http://www.ncbi.nlm.nih.gov/pmc/pub/filespec/

The bars
--------

General bar
...........

    .. image:: img/en/markup_main_bar.png

Generate XML file button
........................

To generate the XML files to PMC, the user must guarantee that xmlbody and other tags must exist, including the regular markup.

    .. image:: img/en/markup_main_bar_genxml.png

Validate XML file button
........................

Click on it, to validate the XML file.

    .. image:: img/en/markup_main_bar_parser_xml.png


If the XML file is invalid:

    .. image:: img/en/pmc_stylechecker_errors.png


If the XML file is valid:

    .. image:: img/en/pmc_stylechecker_noerror.png


Preview the text generated using the XML file button
....................................................

To preview the text, generated from XML file, in order to check if how the fulltext will be presented in the website, click on the Preview text button.


    .. image:: img/en/pmc_scielochecker_errors.png


Markup button
-------------

To go back to markup file.

    .. image:: img/en/markup_main_bar_markup.png


Floating tag bar
----------------

    .. image:: img/en/markup_bar_floating.png

The floating elements are the ones which can appear in any part of the text.

aff  
    identifies an author affiliation
ign 
    identifies a text which can be ignored
tabwrap 
    identifies a table (includes label, caption and image)
    (only valid for XML PMC)
figgrps 
    identifies a compound figure (Fig 1A, 1B, etc), and each one must be figgrp
    (only valid for XML PMC)
figgrp 
    identifies a figure (includes label, caption and image)
    (only valid for XML PMC)
equation 
    identifies an equation (represented by image or LaTex or mml:math)
    (only valid for XML PMC)
list
    identifies a list
    (only valid for XML PMC)
xref 
    identifies cross reference
    (only valid for XML PMC)
uri 
    identifies external links
    (only valid for XML PMC)
sciname
    identifies scientific names
    (only valid for XML PMC)
