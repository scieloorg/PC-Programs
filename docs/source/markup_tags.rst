.. toctree::
   :maxdepth: 1

SciELO Markup Elements and Attributes
=====================================

Automations
...........

*author
-------

Automatic identification of `author`_

Identify automatically one author

*authors
--------

Automatic identification of `authors`_

Identify automatically a group of authors in the references

*boxedtxt
---------

Automatic identification of `boxedtxt`_

Identify automatically boxed text

*deflist
--------

Automatic identification of `deflist`_

Identify automatically a list of definitions

*fn
---

Automatic identification of `fn`_

Identify all the footnotes and its links

*kwdgrp
-------

Automatic identification of `kwdgrp`_

Identify automatically more than one key word

*list
-----

Automatic identification of `list`_

Identify automatically a list

*oauthor
--------

Automatic identification of `oauthor`_

Identify automatically one oauthor

*pauthor
--------

Automatic identification of `pauthor`_

Identify automatically a (person) author: surname and fname

*publoc-pubname
---------------

Automatic identification of `publoc-pubname`_

Identify automatically publisher location and name

*pubname-publoc
---------------

Automatic identification of `pubname-publoc`_

Identify automatically publisher name and location

*sertitle
---------

Automatic identification of `sertitle`_

Identify all the journal titles which match with the selected text.

*source
-------

Automatic identification of `source`_

Identify automatically the document source (book title, journal title, etc)

*stitle
-------

Automatic identification of `stitle`_

Identify all the journal titles which match with the selected text.

Elements
........

abnt6023
--------

Element

Group the elements of references which are according to NBR 6023/89 of ABNT

Contained in: `back`_

Contains: `acitat`_

Attributes: `standard <markup_tags.html#attribute-standard>`_, `count <markup_tags.html#attribute-count>`_

abstract
--------

Element

Identify the abstract of the article

Contained in: `bbibcom`_, `bibcom`_, `subdoc`_

Attributes: `language <markup_tags.html#attribute-language>`_

accepted
--------

Element

Identify the date in which the article was accepted to publish

Contained in: `hist`_

Attributes: `dateiso <markup_tags.html#attribute-dateiso>`_

acitat
------

Element

Identify a bibliography reference

Contained in: `abnt6023`_

Contains: `acontrib`_, `aiserial`_, `amonog`_, `confgrp`_, `no`_

Attributes: none

ack
---

Element

Group the elements of acknowledgment

Contained in: `back`_, `doc`_, `docresp`_, `subdoc`_

Contains: `p`_, `sectitle`_

Attributes: none

acontrib
--------

Element

Group the elements of a contribution

Contained in: `acitat`_

Contains: `*author`_, `author`_, `corpauth`_, `et-al`_, `pages`_, `patgrp`_, `subtitle`_, `title`_, `volid`_

Attributes: none

aff
---

Element

Identify the organization to which the author is affiliated

Contained in: `front`_, `text`_

Contains: `city`_, `country`_, `email`_, `label`_, `role`_, `state`_, `zipcode`_

Attributes: `id <markup_tags.html#attribute-id>`_, `orgname <markup_tags.html#attribute-orgname>`_, `orgdiv1 <markup_tags.html#attribute-orgdiv1>`_, `orgdiv2 <markup_tags.html#attribute-orgdiv2>`_, `orgdiv3 <markup_tags.html#attribute-orgdiv3>`_

afftrans
--------

Element

Identify in subdoc the organization to which the author is affiliated

Contained in: `subdoc`_

Contains: `label`_

Attributes: `id <markup_tags.html#attribute-id>`_

aiserial
--------

Element

Group the elements of a serial publication

Contained in: `acitat`_

Contains: `*sertitle`_, `*stitle`_, `cited`_, `city`_, `country`_, `date`_, `doi`_, `extent`_, `issn`_, `isstitle`_, `issueno`_, `notes`_, `pages`_, `pubid`_, `pubname`_, `sertitle`_, `state`_, `stitle`_, `suppl`_, `url`_, `volid`_

Attributes: none

alttext
-------

Element

Identify an alternative text for a graphic or figure

Contained in: `figgrp`_, `graphic`_

Attributes: none

alttitle
--------

Element

Identify an alternative title for the document title

Contained in: `doctitle`_

Attributes: none

amonog
------

Element

Group the elements of a monograph

Contained in: `acitat`_

Contains: `*author`_, `author`_, `cited`_, `city`_, `coltitle`_, `colvolid`_, `confgrp`_, `corpauth`_, `country`_, `date`_, `doi`_, `edition`_, `et-al`_, `extent`_, `isbn`_, `notes`_, `pages`_, `part`_, `patgrp`_, `pubid`_, `pubname`_, `report`_, `state`_, `subresp`_, `subtitle`_, `thesis`_, `title`_, `tome`_, `url`_, `volid`_

Attributes: none

anonym
------

Element

Identify anonymous authorship

Contained in: `oauthor`_

Attributes: none

apa
---

Element

Group the elements of references which are according to APA

Contained in: `back`_

Contains: `pcitat`_

Attributes: `standard <markup_tags.html#attribute-standard>`_, `count <markup_tags.html#attribute-count>`_

app
---

Element

Identify the appendix

Contained in: `appgrp`_, `docresp`_, `subdoc`_

Contains: `p`_, `sec`_, `sectitle`_

Attributes: `id <markup_tags.html#attribute-id>`_

appgrp
------

Element

Identify a group of appendixes

Contained in: `back`_, `doc`_

Contains: `app`_

Attributes: none

article
-------

Element

Identify the article

Contained in: `start`_

Contains: `back`_, `body`_, `deposit`_, `front`_, `response`_, `subart`_, `xmlbody`_

Attributes: none

arttitle
--------

Element

Identify the article title in a reference

Contained in: `ref`_

Attributes: none

attrib
------

Element

Identify information concerning the origin of an extract, display quote, poetry, or similar element.

Contained in: `figgrp`_, `versegrp`_

Attributes: none

authgrp
-------

Element

Group the authors of the document

Contained in: `front`_, `text`_

Contains: `author`_, `corpauth`_, `onbehalf`_

Attributes: none

authid
------

Element



Attributes: `authidtp <markup_tags.html#attribute-authidtp>`_
author
------

Element

Group the elements of the author, such as name, last name and role

Contained in: `acontrib`_, `amonog`_, `authgrp`_, `doc`_, `docresp`_, `icontrib`_, `iiserial`_, `imonog`_, `pcontrib`_, `pmonog`_, `subdoc`_, `vcontrib`_, `vmonog`_

Contains: `fname`_, `previous`_, `role`_, `surname`_, `surname-fname`_

Attributes: `role <markup_tags.html#attribute-role>`_, `rid <markup_tags.html#attribute-rid>`_, `corresp <markup_tags.html#attribute-corresp>`_, `deceased <markup_tags.html#attribute-deceased>`_, `eqcontr <markup_tags.html#attribute-eqcontr>`_

authors
-------

Element

Group of authors in the references

Contained in: `product`_, `ref`_

Contains: `*pauthor`_, `cauthor`_, `et-al`_, `pauthor`_

Attributes: `role <markup_tags.html#attribute-role>`_

award
-----

Element

Group the contract and funding sources

Contained in: `funding`_

Contains: `contract`_, `fundsrc`_

Attributes: none

awarded
-------

Element



Contains: `fname`_, `orgdiv`_, `orgname`_, `surname`_, `surname-fname`_

Attributes: none

back
----

Element

Identify the back part of the document

Contained in: `article`_, `response`_, `subart`_, `text`_

Contains: `abnt6023`_, `ack`_, `apa`_, `appgrp`_, `bbibcom`_, `fngrp`_, `glossary`_, `iso690`_, `licenses`_, `other`_, `vancouv`_

Attributes: none

bbibcom
-------

Element

Group other elements that are in the back

Contained in: `back`_

Contains: `abstract`_, `confgrp`_, `hist`_, `keygrp`_, `report`_, `thesgrp`_

Attributes: none

bibcom
------

Element

Group other elements that are in front

Contained in: `front`_

Contains: `abstract`_, `confgrp`_, `hist`_, `keygrp`_, `report`_, `thesgrp`_, `xmlabstr`_

Attributes: none

body
----

Element

Identify the body of the document, without details

Contained in: `article`_

Attributes: none

boxedtxt
--------

Element

Identify a boxed text

Contained in: `ifloat`_

Contains: `p`_, `sec`_

Attributes: `id <markup_tags.html#attribute-id>`_

caption
-------

Element

Identify the caption

Contained in: `figgrp`_, `figgrps`_, `supplmat`_, `tabwrap`_

Attributes: none

cauthor
-------

Element

Identify corporative author

Contained in: `authors`_

Attributes: none

chptitle
--------

Element

Identify the chapter title in a reference

Contained in: `product`_, `ref`_

Attributes: none

cited
-----

Element

Identify the date in which the article was accessed

Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `ref`_, `viserial`_, `vmonog`_

Attributes: `dateiso <markup_tags.html#attribute-dateiso>`_

city
----

Element

Identify the city

Contained in: `aff`_, `aiserial`_, `amonog`_, `confgrp`_, `iiserial`_, `imonog`_, `normaff`_, `oiserial`_, `omonog`_, `pmonog`_, `thesgrp`_, `thesis`_, `vmonog`_

Attributes: none

cltrial
-------

Element

Group the elements of a clinical trial

Contained in: `ifloat`_

Contains: `ctreg`_

Attributes: none

coltitle
--------

Element

Identify the title of a collection

Contained in: `amonog`_, `imonog`_, `omonog`_, `pmonog`_, `vmonog`_

Attributes: none

colvolid
--------

Element

Identify the volume of a collection

Contained in: `amonog`_, `pmonog`_

Attributes: none

confgrp
-------

Element

Group the elements of a conference

Contained in: `acitat`_, `amonog`_, `bbibcom`_, `bibcom`_, `ocitat`_, `omonog`_, `pmonog`_, `ref`_, `vmonog`_

Contains: `city`_, `confname`_, `country`_, `date`_, `no`_, `sponsor`_, `state`_

Attributes: none

confname
--------

Element

Identify the conference name

Contained in: `confgrp`_

Attributes: none

contract
--------

Element

Identify the contract/project number given by the sponsor

Contained in: `award`_, `ref`_, `report`_, `rsponsor`_

Attributes: none

corpauth
--------

Element

Identify the corporative author

Contained in: `acontrib`_, `amonog`_, `authgrp`_, `doc`_, `docresp`_, `icontrib`_, `iiserial`_, `imonog`_, `pcontrib`_, `pmonog`_, `subdoc`_, `vcontrib`_, `vmonog`_

Contains: `orgdiv`_, `orgname`_, `previous`_

Attributes: none

corresp
-------

Element



Contained in: `ifloat`_

Contains: `email`_

Attributes: `id <markup_tags.html#attribute-id>`_

country
-------

Element

Identify the country

Contained in: `aff`_, `aiserial`_, `amonog`_, `confgrp`_, `iiserial`_, `imonog`_, `normaff`_, `oiserial`_, `omonog`_, `pmonog`_, `thesgrp`_, `thesis`_, `vmonog`_

Attributes: none


ctreg
-----

Element

Identify the clinical trial number

Contained in: `cltrial`_

Attributes: `cturl <markup_tags.html#attribute-cturl>`_, `ctdbid <markup_tags.html#attribute-ctdbid>`_

date
----

Element

Identify the date related to the context (publication, conference, patent registration, etc)

Contained in: `aiserial`_, `amonog`_, `confgrp`_, `icontrib`_, `iiserial`_, `imonog`_, `ocontrib`_, `oiserial`_, `omonog`_, `patgrp`_, `pcontrib`_, `pmonog`_, `product`_, `ref`_, `thesgrp`_, `thesis`_, `viserial`_, `vmonog`_

Attributes: `dateiso <markup_tags.html#attribute-dateiso>`_, `specyear <markup_tags.html#attribute-specyear>`_

def
---

Element

Identify the definition of a term

Contained in: `defitem`_

Attributes: none

defitem
-------

Element

Identify an item of a list of definitions

Contained in: `deflist`_

Contains: `def`_, `term`_

Attributes: none

deflist
-------

Element

Identify a list of definitions

Contained in: `deflist`_, `glossary`_, `ifloat`_, `xmlbody`_

Contains: `*deflist`_, `defitem`_, `deflist`_, `sectitle`_

Attributes: `id <markup_tags.html#attribute-id>`_

degree
------

Element

 Identify the degree of the thesis, such as Master, Doctor etc

Contained in: `thesgrp`_, `thesis`_

Attributes: none

deposit
-------

Element

Identify the date of deposit in the repository

Contained in: `article`_

Attributes: `deposid <markup_tags.html#attribute-deposid>`_, `entrdate <markup_tags.html#attribute-entrdate>`_, `embdate <markup_tags.html#attribute-embdate>`_

doc
---

Element

Group the data of a document (for XML generation)

Contained in: `start`_

Contains: `*kwdgrp`_, `ack`_, `appgrp`_, `author`_, `corpauth`_, `docresp`_, `doctitle`_, `doi`_, `fngrp`_, `glossary`_, `hist`_, `kwdgrp`_, `normaff`_, `onbehalf`_, `refs`_, `related`_, `subdoc`_, `toctitle`_, `xmlabstr`_, `xmlbody`_

Attributes: none

docresp
-------

Element

Group the response data

Contained in: `doc`_, `subdoc`_

Contains: `*kwdgrp`_, `ack`_, `app`_, `author`_, `corpauth`_, `doctitle`_, `doi`_, `fngrp`_, `glossary`_, `hist`_, `kwdgrp`_, `onbehalf`_, `refs`_, `related`_, `toctitle`_, `xmlabstr`_, `xmlbody`_

Attributes: `id <markup_tags.html#attribute-id>`_, `resptp <markup_tags.html#attribute-resptp>`_, `language <markup_tags.html#attribute-language>`_

doctit
------

Element

Identify the document title in a reference

Attributes: none

doctitle
--------

Element

Identify the title of the document

Contained in: `doc`_, `docresp`_, `subdoc`_

Contains: `alttitle`_, `subtitle`_

Attributes: `language <markup_tags.html#attribute-language>`_

doi
---

Element

Identify the DOI

Contained in: `aiserial`_, `amonog`_, `doc`_, `docresp`_, `front`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `subdoc`_, `text`_, `viserial`_, `vmonog`_

Attributes: none

dperiod
-------

Element

Identify the período of time tratado at the content of the document

Attributes: `from <markup_tags.html#attribute-from>`_, `to <markup_tags.html#attribute-to>`_

edition
-------

Element

Identify the edition number

Contained in: `amonog`_, `iiserial`_, `imonog`_, `omonog`_, `pmonog`_, `ref`_, `vmonog`_

Attributes: none

elemattr
--------

Element

Identify any attribute of XML

Contained in: `element`_

Attributes: `name <markup_tags.html#attribute-name>`_, `value <markup_tags.html#attribute-value>`_

element
-------

Element

Identify any element of XML

Contained in: `ifloat`_

Contains: `elemattr`_

Attributes: `name <markup_tags.html#attribute-name>`_

email
-----

Element

Electronic address of the author

Contained in: `aff`_, `corresp`_, `normaff`_

Attributes: none

equation
--------

Element

Identify the elements of a equation

Contained in: `ifloat`_

Contains: `graphic`_, `label`_, `mmlmath`_, `texmath`_

Attributes: `id <markup_tags.html#attribute-id>`_

et-al
-----

Element

Indicate non cited authors

Contained in: `acontrib`_, `amonog`_, `authors`_, `icontrib`_, `iiserial`_, `imonog`_, `ocontrib`_, `omonog`_, `vcontrib`_, `vmonog`_

Attributes: none

extent
------

Element

Identify the extension of the document (number of pages)

Contained in: `aiserial`_, `amonog`_, `imonog`_, `oiserial`_, `omonog`_, `product`_, `ref`_, `viserial`_, `vmonog`_

Attributes: none

figgrp
------

Element

Group the elements of a figure

Contained in: `figgrps`_, `ifloat`_

Contains: `alttext`_, `attrib`_, `caption`_, `graphic`_, `label`_

Attributes: `id <markup_tags.html#attribute-id>`_

figgrps
-------

Element

Group a group of figures (Fig 1A, 1B,...)

Contained in: `ifloat`_

Contains: `caption`_, `figgrp`_, `label`_

Attributes: `id <markup_tags.html#attribute-id>`_

fname
-----

Element

Identify the first names of an individual author

Contained in: `author`_, `awarded`_, `oauthor`_, `pauthor`_, `sig`_, `subresp`_

Attributes: none

fngrp
-----

Element

Group the elements of a footnote

Contained in: `back`_, `doc`_, `docresp`_, `ifloat`_, `subdoc`_

Contains: `funding`_, `label`_

Attributes: `id <markup_tags.html#attribute-id>`_, `fntype <markup_tags.html#attribute-fntype>`_, `label <markup_tags.html#attribute-label>`_

fntable
-------

Element



Contained in: `tabwrap`_

Contains: `label`_

Attributes: `id <markup_tags.html#attribute-id>`_

found-at
--------

Element

Identify the location of the letter

Attributes: none

front
-----

Element

Identify the front of a document

Contained in: `article`_, `response`_, `subart`_

Contains: `aff`_, `authgrp`_, `bibcom`_, `doi`_, `related`_, `titlegrp`_, `toctitle`_

Attributes: none

funding
-------

Element

Group the data related to funding

Contained in: `fngrp`_, `p`_

Contains: `award`_

Attributes: none

fundsrc
-------

Element

Identify the funding source

Contained in: `award`_

Attributes: none

glossary
--------

Element

Identify a glossary

Contained in: `back`_, `doc`_, `docresp`_, `glossary`_, `subdoc`_

Contains: `*deflist`_, `deflist`_, `glossary`_, `label`_, `sectitle`_

Attributes: none

graphic
-------

Element

Identify an image

Contained in: `equation`_, `figgrp`_, `ifloat`_, `tabwrap`_

Contains: `alttext`_

Attributes: `href <markup_tags.html#attribute-href>`_

hist
----

Element

Identify the history of an article (received and accepted dates)

Contained in: `bbibcom`_, `bibcom`_, `doc`_, `docresp`_, `subdoc`_

Contains: `accepted`_, `received`_, `revised`_

Attributes: none

icitat
------

Element

Identify a reference in ISO 690/87

Contained in: `iso690`_

Contains: `icontrib`_, `iiserial`_, `imonog`_, `no`_

Attributes: none

icontrib
--------

Element

Group the elements of contribution

Contained in: `icitat`_

Contains: `*author`_, `author`_, `corpauth`_, `date`_, `et-al`_, `subresp`_, `subtitle`_, `title`_

Attributes: none

ifloat
------

Element



Contains: `*boxedtxt`_, `*deflist`_, `*fn`_, `*list`_, `boxedtxt`_, `cltrial`_, `corresp`_, `deflist`_, `element`_, `equation`_, `figgrp`_, `figgrps`_, `fngrp`_, `graphic`_, `ign`_, `list`_, `media`_, `product`_, `quote`_, `related`_, `supplmat`_, `tabwrap`_, `uri`_, `versegrp`_, `xref`_

Attributes: none

ign
---

Element

Ignored text

Contained in: `ifloat`_

Attributes: none

iiserial
--------

Element

Group the elements of serial

Contained in: `icitat`_

Contains: `*author`_, `*sertitle`_, `*stitle`_, `author`_, `cited`_, `city`_, `corpauth`_, `country`_, `date`_, `doi`_, `edition`_, `et-al`_, `isdesig`_, `issn`_, `isstitle`_, `issueno`_, `medium`_, `notes`_, `pages`_, `pubid`_, `pubname`_, `sertitle`_, `state`_, `stitle`_, `update`_, `url`_, `volid`_

Attributes: none

imonog
------

Element

Group the elements of monograph

Contained in: `icitat`_

Contains: `*author`_, `author`_, `cited`_, `city`_, `coltitle`_, `corpauth`_, `country`_, `date`_, `doi`_, `edition`_, `et-al`_, `extent`_, `isbn`_, `medium`_, `notes`_, `pages`_, `part`_, `patgrp`_, `pubid`_, `pubname`_, `report`_, `state`_, `subresp`_, `subtitle`_, `title`_, `update`_, `url`_, `volid`_

Attributes: none

inpress
-------

Element

Identify the document is in press status

Contained in: `viserial`_, `vmonog`_

Attributes: none

isbn
----

Element

Identify the Internacional Standard Book Number (ISBN)

Contained in: `amonog`_, `imonog`_, `omonog`_, `product`_, `ref`_

Attributes: none

isdesig
-------

Element

Identify the main dates of a collection, for instance, the initial date of the collection

Contained in: `iiserial`_

Attributes: none

iso690
------

Element

Group the elements of bibliography references which are according to ISO 690/87

Contained in: `back`_

Contains: `icitat`_

Attributes: `standard <markup_tags.html#attribute-standard>`_, `count <markup_tags.html#attribute-count>`_

issn
----

Element

Identify the Internacional Standard Serial  Number (ISSN)

Contained in: `aiserial`_, `iiserial`_, `oiserial`_, `ref`_

Attributes: none

isstitle
--------

Element

Identify the title of an issue number

Contained in: `aiserial`_, `iiserial`_, `oiserial`_

Attributes: none

issueno
-------

Element

Identify the issue number

Contained in: `aiserial`_, `iiserial`_, `oiserial`_, `piserial`_, `ref`_, `viserial`_

Attributes: none

keygrp
------

Element

Group the key words of a document

Contained in: `bbibcom`_, `bibcom`_

Contains: `keyword`_

Attributes: `scheme <markup_tags.html#attribute-scheme>`_

keyword
-------

Element

Identify a key word of the document

Contained in: `keygrp`_

Attributes: `keyword priority level <markup_tags.html#attribute-keyword-priority-level>`_, `language <markup_tags.html#attribute-language>`_

kwd
---

Element

Identify a keyword

Contained in: `kwdgrp`_

Attributes: none

kwdgrp
------

Element

Group the key words related to one language

Contained in: `doc`_, `docresp`_, `subdoc`_

Contains: `kwd`_, `sectitle`_

Attributes: `language <markup_tags.html#attribute-language>`_

label
-----

Element

Identify a label

Contained in: `aff`_, `afftrans`_, `equation`_, `figgrp`_, `figgrps`_, `fngrp`_, `fntable`_, `glossary`_, `li`_, `normaff`_, `ref`_, `supplmat`_, `tabwrap`_, `versegrp`_

Attributes: none

letterto
--------

Element

Identify the recipient of the letter

Attributes: none

li
--

Element

Identify an item of a list

Contained in: `list`_

Contains: `label`_

Attributes: none

license
-------

Element

Identify the text of a license

Contained in: `licenses`_

Contains: `licensep`_

Attributes: `language <markup_tags.html#attribute-language>`_, `lictype <markup_tags.html#attribute-lictype>`_, `href <markup_tags.html#attribute-href>`_

licensep
--------

Element

Identify the paragraph of a license

Contained in: `license`_

Attributes: none

licenses
--------

Element

Group the elements of a license

Contained in: `back`_

Contains: `license`_

Attributes: none

list
----

Element

Identify a list

Contained in: `ifloat`_

Contains: `li`_

Attributes: `listtype <markup_tags.html#attribute-listtype>`_

media
-----

Element



Contained in: `ifloat`_

Attributes: `id <markup_tags.html#attribute-id>`_, `href <markup_tags.html#attribute-href>`_

medium
------

Element

Identify the format of the media in which the document is published

Contained in: `iiserial`_, `imonog`_

Attributes: none

mmlmath
-------

Element

Math (MathML 2.0 Tag Set)

Contained in: `equation`_

Attributes: none

moreinfo
--------

Element

Identify any other information to which there is no tag to identify it. Use the descript attribute to describe the data

Contained in: `product`_, `ref`_

Attributes: none

no
--

Element

Identify the number

Contained in: `acitat`_, `confgrp`_, `icitat`_, `ocitat`_, `pcitat`_, `report`_, `vcitat`_

Attributes: none

normaff
-------

Element

Identify normalized affiliation

Contained in: `doc`_

Contains: `city`_, `country`_, `email`_, `label`_, `orgdiv1`_, `orgdiv2`_, `orgname`_, `role`_, `state`_

Attributes: `id <markup_tags.html#attribute-id>`_, `ncountry <markup_tags.html#attribute-ncountry>`_, `norgname <markup_tags.html#attribute-norgname>`_, `icountry <markup_tags.html#attribute-icountry>`_

notes
-----

Element

Identify notes

Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `pmonog`_

Attributes: none

oauthor
-------

Element

Group the elements of an individual author

Contained in: `ocontrib`_, `omonog`_

Contains: `anonym`_, `fname`_, `previous`_, `surname`_, `surname-fname`_

Attributes: `role <markup_tags.html#attribute-role>`_

ocitat
------

Element

Identify a reference

Contained in: `other`_

Contains: `confgrp`_, `no`_, `ocontrib`_, `oiserial`_, `omonog`_

Attributes: none

ocontrib
--------

Element

Group the elements of a contribution

Contained in: `ocitat`_

Contains: `*oauthor`_, `date`_, `et-al`_, `oauthor`_, `ocorpaut`_, `pages`_, `patgrp`_, `subtitle`_, `title`_

Attributes: none

ocorpaut
--------

Element

Identify a corporative author

Contained in: `ocontrib`_, `omonog`_

Contains: `orgdiv`_, `orgname`_, `previous`_

Attributes: none

oiserial
--------

Element

Group the elements of serial

Contained in: `ocitat`_

Contains: `*sertitle`_, `*stitle`_, `cited`_, `city`_, `country`_, `date`_, `doi`_, `extent`_, `issn`_, `isstitle`_, `issueno`_, `othinfo`_, `pages`_, `pubid`_, `pubname`_, `sertitle`_, `stitle`_, `suppl`_, `url`_, `volid`_

Attributes: none

omonog
------

Element

Group the elements of monograph

Contained in: `ocitat`_

Contains: `*oauthor`_, `cited`_, `city`_, `coltitle`_, `confgrp`_, `country`_, `date`_, `doi`_, `edition`_, `et-al`_, `extent`_, `isbn`_, `oauthor`_, `ocorpaut`_, `othinfo`_, `pages`_, `part`_, `patgrp`_, `pubid`_, `pubname`_, `report`_, `state`_, `subtitle`_, `thesis`_, `title`_, `url`_, `volid`_

Attributes: none

onbehalf
--------

Element

Identify the institution which the contributor represents. Example: John Smith on behalf of Instituition ABCD

Contained in: `authgrp`_, `doc`_, `docresp`_, `subdoc`_

Attributes: none

orgdiv
------

Element

Identify the division of an institution

Contained in: `awarded`_, `corpauth`_, `ocorpaut`_, `rsponsor`_, `sponsor`_, `thesgrp`_, `thesis`_

Attributes: none

orgdiv1
-------

Element

Identify organization division 1

Contained in: `normaff`_

Attributes: none

orgdiv2
-------

Element

Identify organization division 2

Contained in: `normaff`_

Attributes: none

orgname
-------

Element

Identify the name of an institution

Contained in: `awarded`_, `corpauth`_, `normaff`_, `ocorpaut`_, `patgrp`_, `rsponsor`_, `sponsor`_, `thesgrp`_, `thesis`_

Attributes: none

other
-----

Element

Group the elements of bibliography references which are not according to any adopted standard

Contained in: `back`_

Contains: `ocitat`_

Attributes: `standard <markup_tags.html#attribute-standard>`_, `count <markup_tags.html#attribute-count>`_

othinfo
-------

Element

Group any other information

Contained in: `oiserial`_, `omonog`_

Attributes: none

p
-

Element

Identify a paragraph

Contained in: `ack`_, `app`_, `boxedtxt`_, `sec`_, `subsec`_, `xmlabstr`_, `xmlbody`_

Contains: `funding`_

Attributes: none

pages
-----

Element

Identify the pagination

Contained in: `acontrib`_, `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `ocontrib`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `ref`_, `viserial`_, `vmonog`_

Attributes: none

part
----

Element

Identify the part of the volume/issue number

Contained in: `amonog`_, `imonog`_, `omonog`_, `pmonog`_, `ref`_, `viserial`_, `vmonog`_

Attributes: none

patent
------

Element

Identify the number of the patent

Contained in: `patgrp`_

Attributes: none

patentno
--------

Element

Identify the number of the patent

Contained in: `ref`_

Attributes: `country <markup_tags.html#attribute-country>`_

patgrp
------

Element

Group the elements of patent

Contained in: `acontrib`_, `amonog`_, `imonog`_, `ocontrib`_, `omonog`_, `vcontrib`_, `vmonog`_

Contains: `date`_, `orgname`_, `patent`_

Attributes: `country <markup_tags.html#attribute-country>`_

pauthor
-------

Element

Identify a (person) author

Contained in: `authors`_

Contains: `fname`_, `surname`_, `surname-fname`_

Attributes: none

pcitat
------

Element

Identify a bibliography reference

Contained in: `apa`_

Contains: `no`_, `pcontrib`_, `piserial`_, `pmonog`_

Attributes: none

pcontrib
--------

Element

Group the elements of contribution

Contained in: `pcitat`_

Contains: `*author`_, `author`_, `corpauth`_, `date`_, `subtitle`_, `title`_

Attributes: none

piserial
--------

Element

Group the elements of serial

Contained in: `pcitat`_

Contains: `*sertitle`_, `cited`_, `doi`_, `issueno`_, `pages`_, `pubid`_, `sertitle`_, `suppl`_, `url`_, `volid`_

Attributes: none

pmonog
------

Element

Group the elements of monograph

Contained in: `pcitat`_

Contains: `*author`_, `author`_, `cited`_, `city`_, `coltitle`_, `colvolid`_, `confgrp`_, `corpauth`_, `country`_, `date`_, `doi`_, `edition`_, `notes`_, `pages`_, `part`_, `pubid`_, `pubname`_, `report`_, `state`_, `subtitle`_, `thesis`_, `title`_, `url`_, `volid`_

Attributes: none

previous
--------

Element

Identify the author is the same author of the previous reference

Contained in: `author`_, `corpauth`_, `oauthor`_, `ocorpaut`_

Attributes: none

product
-------

Element



Contained in: `ifloat`_

Contains: `authors`_, `chptitle`_, `date`_, `extent`_, `isbn`_, `moreinfo`_, `publoc`_, `pubname`_, `series`_, `source`_

Attributes: `prodtype <markup_tags.html#attribute-prodtype>`_

projname
--------

Element

Identify the name of the project

Contained in: `report`_

Attributes: none

pubid
-----

Element

Identify an id of any external database, such as DOI, pmid (PubMed), pmcid (PMC), etc

Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `ref`_, `viserial`_, `vmonog`_

Attributes: `idtype <markup_tags.html#attribute-idtype>`_

publoc
------

Element

Identify the publisher location

Contained in: `product`_, `ref`_

Attributes: none

pubname
-------

Element

Identify the publisher

Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `pmonog`_, `product`_, `ref`_, `vmonog`_

Attributes: none

quote
-----

Element



Contained in: `ifloat`_

Attributes: none

received
--------

Element

Identify the date in which the article was received by peer review system

Contained in: `hist`_

Attributes: `dateiso <markup_tags.html#attribute-dateiso>`_

ref
---

Element

Group the reference elements

Contained in: `refs`_

Contains: `*authors`_, `*publoc-pubname`_, `*pubname-publoc`_, `*source`_, `arttitle`_, `authors`_, `chptitle`_, `cited`_, `confgrp`_, `contract`_, `date`_, `edition`_, `extent`_, `isbn`_, `issn`_, `issueno`_, `label`_, `moreinfo`_, `pages`_, `part`_, `patentno`_, `pubid`_, `publoc`_, `pubname`_, `reportid`_, `series`_, `source`_, `suppl`_, `text-ref`_, `thesgrp`_, `url`_, `volid`_

Attributes: `id <markup_tags.html#attribute-id>`_, `reftype <markup_tags.html#attribute-reftype>`_

refs
----

Element

Group the references

Contained in: `doc`_, `docresp`_, `subdoc`_

Contains: `ref`_, `sectitle`_

Attributes: none

related
-------

Element

Identify related documents

Contained in: `doc`_, `docresp`_, `front`_, `ifloat`_, `subdoc`_

Attributes: `reltp <markup_tags.html#attribute-reltp>`_, `pid-doi <markup_tags.html#attribute-pid-doi>`_

report
------

Element

Group the elements of funding

Contained in: `amonog`_, `bbibcom`_, `bibcom`_, `imonog`_, `omonog`_, `pmonog`_, `vmonog`_

Contains: `contract`_, `no`_, `projname`_, `rsponsor`_

Attributes: none

reportid
--------

Element

Identify the number or name of the report

Contained in: `ref`_

Attributes: none

response
--------

Element

Group the elements of a response to an article

Contained in: `article`_, `subart`_

Contains: `back`_, `front`_, `xmlbody`_

Attributes: `id <markup_tags.html#attribute-id>`_, `resptp <markup_tags.html#attribute-resptp>`_, `language <markup_tags.html#attribute-language>`_

revised
-------

Element

Identify the date in which the article was revised by peer review system

Contained in: `hist`_

Attributes: `dateiso <markup_tags.html#attribute-dateiso>`_

role
----

Element

Identify the role of the author

Contained in: `aff`_, `author`_, `normaff`_, `sigblock`_

Attributes: none

rsponsor
--------

Element

Identify the sponsor or funding institution

Contained in: `report`_

Contains: `contract`_, `orgdiv`_, `orgname`_

Attributes: none

sciname
-------

Element

Identify scientific names

Attributes: none

sec
---

Element

Identify a section

Contained in: `app`_, `boxedtxt`_, `xmlabstr`_, `xmlbody`_

Contains: `p`_, `sectitle`_, `subsec`_

Attributes: `sec-type <markup_tags.html#attribute-sec-type>`_

sectitle
--------

Element

Identify a section title

Contained in: `ack`_, `app`_, `deflist`_, `glossary`_, `kwdgrp`_, `refs`_, `sec`_, `subsec`_, `xmlabstr`_

Attributes: none

series
------

Element

Identify series

Contained in: `product`_, `ref`_

Attributes: none

sertitle
--------

Element

Identify the journal title

Contained in: `aiserial`_, `iiserial`_, `oiserial`_, `piserial`_

Attributes: none

sig
---

Element



Contained in: `sigblock`_

Contains: `fname`_, `surname`_, `surname-fname`_

Attributes: `rid <markup_tags.html#attribute-rid>`_, `role <markup_tags.html#attribute-role>`_

sigblock
--------

Element



Contained in: `xmlbody`_

Contains: `role`_, `sig`_

Attributes: none

source
------

Element

Identify the document source (book title, journal title, etc)

Contained in: `product`_, `ref`_

Attributes: none

sponsor
-------

Element

Identify the sponsor or funding institution

Contained in: `confgrp`_

Contains: `orgdiv`_, `orgname`_

Attributes: none

start
-----

Element



Contains: `article`_, `doc`_, `text`_

Attributes: none

state
-----

Element

Identify the state/region

Contained in: `aff`_, `aiserial`_, `amonog`_, `confgrp`_, `iiserial`_, `imonog`_, `normaff`_, `omonog`_, `pmonog`_, `thesgrp`_, `thesis`_, `vmonog`_

Attributes: none

stitle
------

Element

Identify the short title of a journal

Contained in: `aiserial`_, `iiserial`_, `oiserial`_, `vstitle`_

Attributes: none

subart
------

Element

Identify the text which is related to the article

Contained in: `article`_, `subart`_

Contains: `back`_, `front`_, `response`_, `subart`_, `xmlbody`_

Attributes: `id <markup_tags.html#attribute-id>`_, `subarttp <markup_tags.html#attribute-subarttp>`_, `language <markup_tags.html#attribute-language>`_

subdoc
------

Element

Group the sub-document data

Contained in: `doc`_, `subdoc`_

Contains: `*kwdgrp`_, `abstract`_, `ack`_, `afftrans`_, `app`_, `author`_, `corpauth`_, `docresp`_, `doctitle`_, `doi`_, `fngrp`_, `glossary`_, `hist`_, `kwdgrp`_, `onbehalf`_, `refs`_, `related`_, `subdoc`_, `toctitle`_, `xmlabstr`_, `xmlbody`_

Attributes: `id <markup_tags.html#attribute-id>`_, `subarttp <markup_tags.html#attribute-subarttp>`_, `language <markup_tags.html#attribute-language>`_

subkey
------

Element

Identify the subkey of a key word

Attributes: none

subresp
-------

Element

Identify the secondary responsabilities

Contained in: `amonog`_, `icontrib`_, `imonog`_

Contains: `fname`_, `surname`_, `surname-fname`_

Attributes: `role <markup_tags.html#attribute-role>`_

subsec
------

Element

Identify a sub-section

Contained in: `sec`_

Contains: `p`_, `sectitle`_

Attributes: none

subtitle
--------

Element

Identify the subtitle

Contained in: `acontrib`_, `amonog`_, `doctitle`_, `icontrib`_, `imonog`_, `ocontrib`_, `omonog`_, `pcontrib`_, `pmonog`_, `titlegrp`_, `vtitle`_

Attributes: none

suppl
-----

Element

Identify the supplement

Contained in: `aiserial`_, `oiserial`_, `piserial`_, `ref`_, `viserial`_

Attributes: none

supplmat
--------

Element



Contained in: `ifloat`_

Contains: `caption`_, `label`_

Attributes: `id <markup_tags.html#attribute-id>`_, `href <markup_tags.html#attribute-href>`_

surname
-------

Element

Identify the last name

Contained in: `author`_, `awarded`_, `oauthor`_, `pauthor`_, `sig`_, `subresp`_

Attributes: none

surname-fname
-------------

Element

Identify surname and fname of one author (surname separator fname or fname separator surname)

Contained in: `author`_, `awarded`_, `oauthor`_, `pauthor`_, `sig`_, `subresp`_

Attributes: none

table
-----

Element



Contained in: `tabwrap`_

Contains: `tr`_

Attributes: none

tabwrap
-------

Element

Group the elements of a table

Contained in: `ifloat`_

Contains: `caption`_, `fntable`_, `graphic`_, `label`_, `table`_

Attributes: `id <markup_tags.html#attribute-id>`_

td
--

Element



Contained in: `tr`_

Attributes: `align <markup_tags.html#attribute-align>`_, `colspan <markup_tags.html#attribute-colspan>`_, `rowspan <markup_tags.html#attribute-rowspan>`_

term
----

Element

Identify a term

Contained in: `defitem`_

Attributes: none

texmath
-------

Element

Identify a formula using Tex Math Equation

Contained in: `equation`_

Attributes: none

text
----

Element

Identify a text

Contained in: `start`_

Contains: `aff`_, `authgrp`_, `back`_, `doi`_, `titlegrp`_

Attributes: none

text-ref
--------

Element

Identify the original form of the reference

Contained in: `ref`_

Attributes: none

th
--

Element



Contained in: `tr`_

Attributes: `align <markup_tags.html#attribute-align>`_, `colspan <markup_tags.html#attribute-colspan>`_, `rowspan <markup_tags.html#attribute-rowspan>`_

thesgrp
-------

Element

Group the elements of a thesis

Contained in: `bbibcom`_, `bibcom`_, `ref`_

Contains: `city`_, `country`_, `date`_, `degree`_, `orgdiv`_, `orgname`_, `state`_

Attributes: none

thesis
------

Element

Group the elements of a thesis

Contained in: `amonog`_, `omonog`_, `pmonog`_, `vmonog`_

Contains: `city`_, `country`_, `date`_, `degree`_, `orgdiv`_, `orgname`_, `state`_

Attributes: none

title
-----

Element

Identify the title of the document

Contained in: `acontrib`_, `amonog`_, `icontrib`_, `imonog`_, `ocontrib`_, `omonog`_, `pcontrib`_, `pmonog`_, `titlegrp`_, `vtitle`_

Attributes: `language <markup_tags.html#attribute-language>`_

titlegrp
--------

Element

Group the titles of the document

Contained in: `front`_, `text`_

Contains: `subtitle`_, `title`_

Attributes: none

toctitle
--------

Element

Identify the TOC section title. It is mandatory to the generation of XML files.

Contained in: `doc`_, `docresp`_, `front`_, `subdoc`_

Attributes: none

tome
----

Element

Identify the tome of a publication

Contained in: `amonog`_

Attributes: none

tp
--

Element

Identify the type of publication

Contained in: `vstitle`_, `vtitle`_

Attributes: none

tr
--

Element



Contained in: `table`_

Contains: `td`_, `th`_

Attributes: none

update
------

Element

Identify the information of update

Contained in: `iiserial`_, `imonog`_

Attributes: none

uri
---

Element

Identify an uri

Contained in: `ifloat`_

Attributes: `href <markup_tags.html#attribute-href>`_

url
---

Element

Identify the electronic address of the document

Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `ref`_, `viserial`_, `vmonog`_

Attributes: none

vancouv
-------

Element

Group the elements of bibliography references which are according to Vancouver

Contained in: `back`_

Contains: `vcitat`_

Attributes: `standard <markup_tags.html#attribute-standard>`_, `count <markup_tags.html#attribute-count>`_

vcitat
------

Element

Identify a bibliography reference

Contained in: `vancouv`_

Contains: `no`_, `vcontrib`_, `viserial`_, `vmonog`_

Attributes: none

vcontrib
--------

Element

Group the elements of contribution

Contained in: `vcitat`_

Contains: `*author`_, `author`_, `corpauth`_, `et-al`_, `patgrp`_, `vtitle`_

Attributes: none

versegrp
--------

Element

Identify song, poem, or verse

Contained in: `ifloat`_, `versegrp`_

Contains: `attrib`_, `label`_, `versegrp`_, `versline`_

Attributes: none

version
-------

Element

Identify the version

Contained in: `vmonog`_

Attributes: none

versline
--------

Element

Identify a song, poem, or verse line

Contained in: `versegrp`_

Attributes: none

viserial
--------

Element

Group the elements of serial

Contained in: `vcitat`_

Contains: `cited`_, `date`_, `doi`_, `extent`_, `inpress`_, `issueno`_, `pages`_, `part`_, `pubid`_, `suppl`_, `url`_, `volid`_, `vstitle`_

Attributes: none

vmonog
------

Element

Group the elements of monograph

Contained in: `vcitat`_

Contains: `*author`_, `author`_, `cited`_, `city`_, `coltitle`_, `confgrp`_, `corpauth`_, `country`_, `date`_, `doi`_, `edition`_, `et-al`_, `extent`_, `inpress`_, `pages`_, `part`_, `patgrp`_, `pubid`_, `pubname`_, `report`_, `state`_, `thesis`_, `url`_, `version`_, `volid`_, `vtitle`_

Attributes: none

volid
-----

Element

Identify the volume

Contained in: `acontrib`_, `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `ref`_, `viserial`_, `vmonog`_

Attributes: none

vstitle
-------

Element

Short title in Vancouver

Contained in: `viserial`_

Contains: `stitle`_, `tp`_

Attributes: none

vtitle
------

Element

Group the elements of title in Vancouver

Contained in: `vcontrib`_, `vmonog`_

Contains: `subtitle`_, `title`_, `tp`_

Attributes: none

xmlabstr
--------

Element

Identify the abstract with sections

Contained in: `bibcom`_, `doc`_, `docresp`_, `subdoc`_

Contains: `p`_, `sec`_, `sectitle`_

Attributes: `language <markup_tags.html#attribute-language>`_

xmlbody
-------

Element

Identify the body of the document, in details

Contained in: `article`_, `doc`_, `docresp`_, `response`_, `subart`_, `subdoc`_

Contains: `*deflist`_, `deflist`_, `p`_, `sec`_, `sigblock`_

Attributes: none

xref
----

Element

Identify a cross-reference

Contained in: `ifloat`_

Attributes: `ref-type <markup_tags.html#attribute-ref-type>`_, `rid <markup_tags.html#attribute-rid>`_, `label <markup_tags.html#attribute-label>`_

zipcode
-------

Element

Identify a ZIP Code

Contained in: `aff`_

Attributes: none

Attributes
..........

Attribute authidtp
------------------

Attribute

Identify the type of author id

Is attribute of: 


+------+-----------+
|orcid |orcid      |
+------+-----------+
|lattes|lattes     |
+------+-----------+


Attribute blcktype
------------------

Attribute

Identify the text block type

Is attribute of: 


+---+-----------+
|nd |undefined  |
+---+-----------+
|ack|Acknowledge|
+---+-----------+




Attribute ccode
---------------

Attribute

Identify the Identify where the markup is done

Is attribute of: 


+-------+-----------------------------------------------------------+
|bjce   |brazilian journal of chemical engineering                  |
+-------+-----------------------------------------------------------+
|bjg    |brazilian journal of genetics                              |
+-------+-----------------------------------------------------------+
|bjmbr  |brazilian journal of medical and biological research       |
+-------+-----------------------------------------------------------+
|bjp    |brazilian journal of physics                               |
+-------+-----------------------------------------------------------+
|conicyt|Comisión Nacional de Investigación Científica y Tecnológica|
+-------+-----------------------------------------------------------+
|dados  |dados - revista de ciências sociais                        |
+-------+-----------------------------------------------------------+
|br1.1  |scielo/bireme                                              |
+-------+-----------------------------------------------------------+
|infomed|InfoMed                                                    |
+-------+-----------------------------------------------------------+
|jbchs  |journal of the brazilian chemical society                  |
+-------+-----------------------------------------------------------+
|jbcos  |journal of the brazilian computer society                  |
+-------+-----------------------------------------------------------+
|mioc   |memórias do instituto oswaldo cruz                         |
+-------+-----------------------------------------------------------+
|rbcs   |revista brasileira de ciência do solo                      |
+-------+-----------------------------------------------------------+
|rbgeo  |revista brasileira de geociências                          |
+-------+-----------------------------------------------------------+
|rimtsp |revista do instituto de medicina tropical de são paulo     |
+-------+-----------------------------------------------------------+
|rsp    |revista de saúde pública                                   |
+-------+-----------------------------------------------------------+




Attribute corresp
-----------------

Attribute

Identify the correspondence information

Is attribute of: `author`_


+-+---+
|y|yes|
+-+---+
|n|no |
+-+---+




Attribute count
---------------

Attribute

Identify the quantity

Is attribute of: `abnt6023`_, `apa`_, `iso690`_, `other`_, `vancouv`_


+-+-+
|0|0|
+-+-+




Attribute country
-----------------

Attribute

Identify the country

Is attribute of: `patentno`_, `patgrp`_


+--+----------------------------+
|AF|Afghanistan                 |
+--+----------------------------+
|AL|Albania                     |
+--+----------------------------+
|DZ|Algeria                     |
+--+----------------------------+
|AS|American Samoa              |
+--+----------------------------+
|AD|Andorra                     |
+--+----------------------------+
|AO|Angola                      |
+--+----------------------------+
|AQ|Antarctica                  |
+--+----------------------------+
|AG|Antigua                     |
+--+----------------------------+
|AR|Argentina                   |
+--+----------------------------+
|AU|Australia                   |
+--+----------------------------+
|AT|Austria                     |
+--+----------------------------+
|BS|Bahamas                     |
+--+----------------------------+
|BH|Bahrain                     |
+--+----------------------------+
|BD|Bangladesh                  |
+--+----------------------------+
|BB|Barbados                    |
+--+----------------------------+
|BE|Belgium                     |
+--+----------------------------+
|BZ|Belize                      |
+--+----------------------------+
|BM|Bermuda                     |
+--+----------------------------+
|BT|Bhutan                      |
+--+----------------------------+
|BO|Bolivia                     |
+--+----------------------------+
|BW|Botswana                    |
+--+----------------------------+
|BV|Bouvet Island               |
+--+----------------------------+
|BR|Brazil                      |
+--+----------------------------+
|VG|British Virgin Islands      |
+--+----------------------------+
|BN|Brunei                      |
+--+----------------------------+
|BG|Bulgaria                    |
+--+----------------------------+
|BU|Burma                       |
+--+----------------------------+
|BI|Burundi                     |
+--+----------------------------+
|BY|Byelorussian RSS            |
+--+----------------------------+
|CM|Cameroon                    |
+--+----------------------------+
|CA|Canada                      |
+--+----------------------------+
|CV|Cape Verde                  |
+--+----------------------------+
|CF|Central African Rep.        |
+--+----------------------------+
|TD|Chad                        |
+--+----------------------------+
|CL|Chile                       |
+--+----------------------------+
|CN|China                       |
+--+----------------------------+
|CO|Colombia                    |
+--+----------------------------+
|CG|Congo                       |
+--+----------------------------+
|CR|Costa Rica                  |
+--+----------------------------+
|CU|Cuba                        |
+--+----------------------------+
|CY|Cyprus                      |
+--+----------------------------+
|CS|Czechoslovakia              |
+--+----------------------------+
|DK|Denmark                     |
+--+----------------------------+
|DM|Dominica                    |
+--+----------------------------+
|DO|Dominican Republic          |
+--+----------------------------+
|NQ|Dronning Maud Land          |
+--+----------------------------+
|EC|Ecuador                     |
+--+----------------------------+
|EG|Egypt                       |
+--+----------------------------+
|SV|El Salvador                 |
+--+----------------------------+
|ET|Ethiopia                    |
+--+----------------------------+
|FK|Falkland Islands(Malvinas)  |
+--+----------------------------+
|FJ|Fiji                        |
+--+----------------------------+
|FI|Filand                      |
+--+----------------------------+
|FR|France                      |
+--+----------------------------+
|GF|French Guiana               |
+--+----------------------------+
|PF|French Polynesia            |
+--+----------------------------+
|GA|Gabon                       |
+--+----------------------------+
|DD|German Democratic Republic  |
+--+----------------------------+
|DE|Germany, Federal Republic   |
+--+----------------------------+
|GH|Ghana                       |
+--+----------------------------+
|GI|Gibraltar                   |
+--+----------------------------+
|GR|Greece                      |
+--+----------------------------+
|GL|Greenland                   |
+--+----------------------------+
|GD|Grenada                     |
+--+----------------------------+
|GP|Guadeloupe                  |
+--+----------------------------+
|GU|Guam                        |
+--+----------------------------+
|GT|Guatemala                   |
+--+----------------------------+
|GC|Guinea Ecuatorial           |
+--+----------------------------+
|GN|Guinea                      |
+--+----------------------------+
|GW|Guinea-Bissau               |
+--+----------------------------+
|GY|Guyana                      |
+--+----------------------------+
|HT|Haiti                       |
+--+----------------------------+
|HN|Honduras                    |
+--+----------------------------+
|HK|Hong Kong                   |
+--+----------------------------+
|HU|Hungary                     |
+--+----------------------------+
|IS|Iceland                     |
+--+----------------------------+
|IN|India                       |
+--+----------------------------+
|ID|Indonesia                   |
+--+----------------------------+
|IR|Iran                        |
+--+----------------------------+
|IQ|Iraq                        |
+--+----------------------------+
|IE|Ireland                     |
+--+----------------------------+
|CX|Isla de Navidad             |
+--+----------------------------+
|JT|Isla Johnston               |
+--+----------------------------+
|NU|Isla Niue                   |
+--+----------------------------+
|WK|Isla Wake                   |
+--+----------------------------+
|PU|Islands Miscellaneous       |
+--+----------------------------+
|CT|Islas Canton y Enderbury    |
+--+----------------------------+
|CC|Islas Cocos (Keeling)       |
+--+----------------------------+
|CK|Islas Cook                  |
+--+----------------------------+
|FO|Islas Feroe                 |
+--+----------------------------+
|HM|Islas Heard y Mc Donald     |
+--+----------------------------+
|MI|Islas Midway                |
+--+----------------------------+
|PN|Islas Pitcairn              |
+--+----------------------------+
|SB|Islas Salomón Británico     |
+--+----------------------------+
|SJ|Islas Svalbard y Jan Mayen  |
+--+----------------------------+
|TK|Islas Tokelau               |
+--+----------------------------+
|WF|Islas Wallis y Futuna       |
+--+----------------------------+
|IL|Israel                      |
+--+----------------------------+
|IT|Italy                       |
+--+----------------------------+
|YU|Iugoslavia                  |
+--+----------------------------+
|CI|Ivory Coast                 |
+--+----------------------------+
|JM|Jamaica                     |
+--+----------------------------+
|JP|Japan                       |
+--+----------------------------+
|JO|Jordan                      |
+--+----------------------------+
|KM|Kamoras Islands             |
+--+----------------------------+
|KH|Kampuchea Democrática       |
+--+----------------------------+
|KY|Kayman Islands              |
+--+----------------------------+
|KE|Kenya                       |
+--+----------------------------+
|KD|Korea, Democratic People's  |
+--+----------------------------+
|KP|Korea, Democratic People's  |
+--+----------------------------+
|KR|Korea, Republic of          |
+--+----------------------------+
|KW|Kuwait                      |
+--+----------------------------+
|LD|Lao People's Democratic     |
+--+----------------------------+
|LB|Lebanon                     |
+--+----------------------------+
|LS|Lesotho                     |
+--+----------------------------+
|LR|Liberia                     |
+--+----------------------------+
|LY|Libyan                      |
+--+----------------------------+
|LI|Liechtenstein               |
+--+----------------------------+
|LU|Luxembourg                  |
+--+----------------------------+
|MO|Macau                       |
+--+----------------------------+
|MG|Madagascar                  |
+--+----------------------------+
|MW|Malawi                      |
+--+----------------------------+
|MY|Malaysia                    |
+--+----------------------------+
|MV|Maldivas                    |
+--+----------------------------+
|ML|Mali                        |
+--+----------------------------+
|MT|Malta                       |
+--+----------------------------+
|MQ|Martinique                  |
+--+----------------------------+
|MR|Mauritania                  |
+--+----------------------------+
|MU|Mauritius                   |
+--+----------------------------+
|MX|Mexico                      |
+--+----------------------------+
|MC|Monaco                      |
+--+----------------------------+
|MN|Mongolia                    |
+--+----------------------------+
|MS|Montserrat                  |
+--+----------------------------+
|MA|Morocco                     |
+--+----------------------------+
|MZ|Mozambique                  |
+--+----------------------------+
|NA|Namibia                     |
+--+----------------------------+
|NR|Nauru                       |
+--+----------------------------+
|NP|Nepal                       |
+--+----------------------------+
|NL|Netherlands                 |
+--+----------------------------+
|AN|Netherlands Antilles        |
+--+----------------------------+
|NC|New Caledonia               |
+--+----------------------------+
|NZ|New Zealand                 |
+--+----------------------------+
|NI|Nicaragua                   |
+--+----------------------------+
|NE|Niger                       |
+--+----------------------------+
|NG|Nigeria                     |
+--+----------------------------+
|NF|Norfolk Island              |
+--+----------------------------+
|NO|Norway                      |
+--+----------------------------+
|NH|Nuevas Hébridas             |
+--+----------------------------+
|OM|Oman                        |
+--+----------------------------+
|PC|Pacific Islands             |
+--+----------------------------+
|PK|Pakistan                    |
+--+----------------------------+
|PA|Panama                      |
+--+----------------------------+
|PG|Papua New Guinea            |
+--+----------------------------+
|PY|Paraguay                    |
+--+----------------------------+
|PE|Peru                        |
+--+----------------------------+
|PH|Philippines                 |
+--+----------------------------+
|PL|Poland                      |
+--+----------------------------+
|PT|Portugal                    |
+--+----------------------------+
|PR|Puerto Rico                 |
+--+----------------------------+
|QA|Qatar                       |
+--+----------------------------+
|LA|Republic                    |
+--+----------------------------+
|RE|Réunion                     |
+--+----------------------------+
|RO|Romania                     |
+--+----------------------------+
|RW|Rwanda                      |
+--+----------------------------+
|PM|S. Pedro y Miguelón         |
+--+----------------------------+
|LC|Saint Lucia                 |
+--+----------------------------+
|VC|Saint Vincent               |
+--+----------------------------+
|WS|Samoa                       |
+--+----------------------------+
|KN|San Cristóbal-Nieves-Anguila|
+--+----------------------------+
|SM|San Marino                  |
+--+----------------------------+
|ST|Sao Tome and Principe       |
+--+----------------------------+
|SA|Saudi Arabia                |
+--+----------------------------+
|SC|Seichelles                  |
+--+----------------------------+
|SN|Senegal                     |
+--+----------------------------+
|SL|Sierra Leone                |
+--+----------------------------+
|SK|Sikkim                      |
+--+----------------------------+
|SG|Singapur                    |
+--+----------------------------+
|SO|Somalia                     |
+--+----------------------------+
|ZA|South Africa                |
+--+----------------------------+
|ES|Spain                       |
+--+----------------------------+
|LK|Sri Lanka                   |
+--+----------------------------+
|SH|St. Helena                  |
+--+----------------------------+
|SD|Sudan                       |
+--+----------------------------+
|SR|Suriname                    |
+--+----------------------------+
|SZ|Swaziland                   |
+--+----------------------------+
|SE|Sweden                      |
+--+----------------------------+
|CH|Switzerland                 |
+--+----------------------------+
|SY|Syrian Arab Republic        |
+--+----------------------------+
|TW|Taiwan                      |
+--+----------------------------+
|TZ|Tanzania                    |
+--+----------------------------+
|TH|Thailand                    |
+--+----------------------------+
|TG|Togo                        |
+--+----------------------------+
|TO|Tonga                       |
+--+----------------------------+
|TT|Trinidad and Tobago         |
+--+----------------------------+
|TN|Tunisia                     |
+--+----------------------------+
|TR|Turkey                      |
+--+----------------------------+
|TC|Turks and Caicos Islands    |
+--+----------------------------+
|UG|Uganda                      |
+--+----------------------------+
|UA|Ukrainian RSS               |
+--+----------------------------+
|AE|United Arab Emirates        |
+--+----------------------------+
|GB|United Kingdom              |
+--+----------------------------+
|US|United States               |
+--+----------------------------+
|UP|United States Pacific       |
+--+----------------------------+
|HV|Upper Volta                 |
+--+----------------------------+
|SU|URSS                        |
+--+----------------------------+
|UY|Uruguay                     |
+--+----------------------------+
|VU|Vanuatu                     |
+--+----------------------------+
|VA|Vatican City State          |
+--+----------------------------+
|VE|Venezuela                   |
+--+----------------------------+
|VN|Viet Nam                    |
+--+----------------------------+
|EH|Western Sahara              |
+--+----------------------------+
|YE|Yemen                       |
+--+----------------------------+
|YD|Yemen, Democratic           |
+--+----------------------------+
|ZR|Zaire                       |
+--+----------------------------+
|ZM|Zambia                      |
+--+----------------------------+
|nd|Not defined                 |
+--+----------------------------+




Attribute ctdbid
----------------

Attribute

Identify the clinical trial database ID

Is attribute of: `ctreg`_


+------+---------------------------------------------------------------------------+
|CT    |CT - Clinicaltrials.gov                                                    |
+------+---------------------------------------------------------------------------+
|ACTR  |ACTR - Australian Clinical Trials Registry                                 |
+------+---------------------------------------------------------------------------+
|ISRCTN|ISRCTN - International Standard Randomised Controlled Trial Number Register|
+------+---------------------------------------------------------------------------+
|NTR   |NTR - Nederlands Trial Register                                            |
+------+---------------------------------------------------------------------------+
|UMIN  |UMIN - University Hospital Medical Information Network                     |
+------+---------------------------------------------------------------------------+
|ChiCTR|ChiCTR - Chinese Clinical Trial Register                                   |
+------+---------------------------------------------------------------------------+




Attribute cturl
---------------

Attribute

Identify the clinical trial database's URL

Is attribute of: `ctreg`_




Attribute dateiso
-----------------

Attribute

Identify the date in format YYYYMMDD (YYYY = 4 digits for year, 2 digits for month, 2 digits for day)

Is attribute of: `accepted`_, `cited`_, `date`_, `received`_, `revised`_


+--------+--------+
|00000000|00000000|
+--------+--------+




Attribute deceased
------------------

Attribute

Identify the deceased author

Is attribute of: `author`_


+-+---+
|y|yes|
+-+---+
|n|no |
+-+---+




Attribute deposid
-----------------

Attribute

Identify the repository ID

Is attribute of: `deposit`_


+-+-------+
|1|Unicamp|
+-+-------+
|2|Unifesp|
+-+-------+
|3|Unesp  |
+-+-------+
|4|USP    |
+-+-------+
|5|ITA    |
+-+-------+
|6|UFSCar |
+-+-------+




Attribute doctopic
------------------

Attribute

Identify the type of the document

Is attribute of: 


+--+-------------------+
|ab|abstracts          |
+--+-------------------+
|ax|annex              |
+--+-------------------+
|an|announcements      |
+--+-------------------+
|sc|brief communication|
+--+-------------------+
|cr|case report        |
+--+-------------------+
|ct|clinical trial     |
+--+-------------------+
|co|comments           |
+--+-------------------+
|er|correction         |
+--+-------------------+
|ed|editorial          |
+--+-------------------+
|in|interview          |
+--+-------------------+
|le|letter             |
+--+-------------------+
|mt|methodology        |
+--+-------------------+
|oa|original article   |
+--+-------------------+
|pv|point-of-view      |
+--+-------------------+
|pr|press release      |
+--+-------------------+
|rc|recount            |
+--+-------------------+
|rn|research note      |
+--+-------------------+
|ra|review article     |
+--+-------------------+
|tr|technical report   |
+--+-------------------+
|up|update             |
+--+-------------------+




Attribute embdate
-----------------

Attribute

Identify the embargo date

Is attribute of: `deposit`_




Attribute entrdate
------------------

Attribute

Identify the entrance date

Is attribute of: `deposit`_




Attribute eqcontr
-----------------

Attribute

Identify the equality information

Is attribute of: `author`_


+-+---+
|y|yes|
+-+---+
|n|no |
+-+---+




Attribute filename
------------------

Attribute

Identify the filename of a figure or table or equation

Is attribute of: 




Attribute fntype
----------------

Attribute

Identify the footnote type

Is attribute of: `fngrp`_


+-------------------------+--------------------------------------------------------------------------------------------------------+
|abbr                     |Abbreviations                                                                                           |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|com                      |Communicated-by information                                                                             |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|con                      |Contributed-by information                                                                              |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|conflict                 |Conflict of interest statements                                                                         |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|corresp                  |Corresponding author information not identified separately, but merely footnoted                        |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|current-aff              |Contributor's current affiliation                                                                       |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|deceased                 |Person has died since article was written                                                               |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|edited-by                |Contributor has the role of an editor                                                                   |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|equal                    |Contributed equally to the creation of the document                                                     |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|financial-disclosure     |Statement of funding or denial of funds received in support of the research on which an article is based|
+-------------------------+--------------------------------------------------------------------------------------------------------+
|on-leave                 |Contributor is on sabbatical or other leave of absence                                                  |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|other                    |Some footnote type, other than those enumerated.                                                        |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|author                   |Some footnote type, other than those enumerated, but related to author.                                 |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|participating-researchers|Contributor was a researcher for an article                                                             |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|present-address          |Contributor's current address                                                                           |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|presented-at             |Conference, colloquium, or other occasion at which this paper was presented                             |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|presented-by             |Contributor who presented the material                                                                  |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|previously-at            |Contributor's previous location or affiliation                                                          |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|study-group-members      |Contributor was a member of the study group for the research                                            |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|supplementary-material   |Points to or describes supplementary material for the article                                           |
+-------------------------+--------------------------------------------------------------------------------------------------------+
|supported-by             |Research upon which an article is based was supported by some entity                                    |
+-------------------------+--------------------------------------------------------------------------------------------------------+




Attribute from
--------------

Attribute

Identify the start date

Is attribute of: `dperiod`_


+--------+--------+
|00000000|00000000|
+--------+--------+




Attribute ftype
---------------

Attribute

Identify the type of the figure

Is attribute of: 


+------------------+------------------+
|audiogram         |audiogram         |
+------------------+------------------+
|cardiogram        |cardiogram        |
+------------------+------------------+
|cartoon           |cartoon           |
+------------------+------------------+
|chart             |chart             |
+------------------+------------------+
|chemical structure|chemical structure|
+------------------+------------------+
|dendrogram        |dendrogram        |
+------------------+------------------+
|diagram           |diagram           |
+------------------+------------------+
|drawing           |drawing           |
+------------------+------------------+
|exihibit          |exihibit          |
+------------------+------------------+
|graphic           |graphic           |
+------------------+------------------+
|illustration      |illustration      |
+------------------+------------------+
|map               |map               |
+------------------+------------------+
|medical image     |medical image     |
+------------------+------------------+
|other             |other             |
+------------------+------------------+
|photo             |photo             |
+------------------+------------------+
|photomicrograph   |photomicrograph   |
+------------------+------------------+
|plate             |plate             |
+------------------+------------------+
|polysomnogram     |polysomnogram     |
+------------------+------------------+
|schema            |schema            |
+------------------+------------------+
|workflow          |workflow          |
+------------------+------------------+




Attribute hcomment
------------------

Attribute

Identify the permission to comment or not the document

Is attribute of: 


+-+----------------------+
|0|people can not comment|
+-+----------------------+
|1|people can comment    |
+-+----------------------+




Attribute href
--------------

Attribute

Identify the href of a file

Is attribute of: `graphic`_, `license`_, `media`_, `supplmat`_, `uri`_




Attribute id
------------

Attribute

Identify an ID

Is attribute of: `aff`_, `afftrans`_, `app`_, `boxedtxt`_, `corresp`_, `deflist`_, `docresp`_, `equation`_, `figgrp`_, `figgrps`_, `fngrp`_, `fntable`_, `media`_, `normaff`_, `ref`_, `response`_, `subart`_, `subdoc`_, `supplmat`_, `tabwrap`_


+--+-----------+
|nd|No definido|
+--+-----------+




Attribute idtype
----------------

Attribute

Identify the Identify type of the ID

Is attribute of: `pubid`_


+-------------+-------------+
|art-access-id|art-access-id|
+-------------+-------------+
|coden        |coden        |
+-------------+-------------+
|doaj         |doaj         |
+-------------+-------------+
|doi          |doi          |
+-------------+-------------+
|medline      |medline      |
+-------------+-------------+
|manuscript   |manuscript   |
+-------------+-------------+
|rrn          |rrn          |
+-------------+-------------+
|other        |other        |
+-------------+-------------+
|pii          |pii          |
+-------------+-------------+
|pmcid        |pmcid        |
+-------------+-------------+
|pmid         |pmid         |
+-------------+-------------+
|publisher-id |publisher-id |
+-------------+-------------+
|sici         |sici         |
+-------------+-------------+




Attribute illustrative material type
------------------------------------

Attribute

Identify the illustrative material type existing in the document

Is attribute of: 


+----+------------------------+
|nd  |no illustrative material|
+----+------------------------+
|ilus|figure                  |
+----+------------------------+
|gra |graphic                 |
+----+------------------------+
|map |map                     |
+----+------------------------+
|tab |table                   |
+----+------------------------+




Attribute keyword priority level
--------------------------------

Attribute

Identify the indicates the

Is attribute of: `keyword`_


+-+---------+
|m|main     |
+-+---------+
|s|secondary|
+-+---------+




Attribute language
------------------

Attribute

Identify the language

Is attribute of: `abstract`_, `docresp`_, `doctitle`_, `keyword`_, `kwdgrp`_, `license`_, `response`_, `subart`_, `subdoc`_, `title`_, `xmlabstr`_


+--+-----------+
|en|English    |
+--+-----------+
|pt|Portuguese |
+--+-----------+
|es|Spanish    |
+--+-----------+
|af|Afrikaans  |
+--+-----------+
|ar|Arabic     |
+--+-----------+
|bg|Bulgarian  |
+--+-----------+
|ch|Chinese    |
+--+-----------+
|cs|Czech      |
+--+-----------+
|da|Danish     |
+--+-----------+
|nl|Dutch      |
+--+-----------+
|eo|Esperanto  |
+--+-----------+
|fr|French     |
+--+-----------+
|de|German     |
+--+-----------+
|gr|Greek      |
+--+-----------+
|he|Hebrew     |
+--+-----------+
|hi|Hindi      |
+--+-----------+
|hu|Hungarian  |
+--+-----------+
|in|Indonesian |
+--+-----------+
|ia|Interlingua|
+--+-----------+
|ie|Interlingue|
+--+-----------+
|it|Italian    |
+--+-----------+
|ja|Japanese   |
+--+-----------+
|ko|Korean     |
+--+-----------+
|la|Latin      |
+--+-----------+
|no|Norwergian |
+--+-----------+
|pl|Polish     |
+--+-----------+
|ro|Romanian   |
+--+-----------+
|ru|Russian    |
+--+-----------+
|sa|Sanskrit   |
+--+-----------+
|sh|Serbo-Croat|
+--+-----------+
|sk|Slovak     |
+--+-----------+
|sn|Slovenian  |
+--+-----------+
|sv|Swedish    |
+--+-----------+
|tr|Turkish    |
+--+-----------+
|uk|Ukrainian  |
+--+-----------+
|ur|Urdu       |
+--+-----------+
|zz|Other      |
+--+-----------+
|gl|Galician   |
+--+-----------+
|eu|Basque     |
+--+-----------+
|ca|Catalan    |
+--+-----------+




Attribute lictype
-----------------

Attribute

Identify the license type

Is attribute of: `license`_


+-----------+-----------+
|open-access|open access|
+-----------+-----------+
|nd         |not defined|
+-----------+-----------+




Attribute listtype
------------------

Attribute

Identify the type of the list

Is attribute of: `list`_


+-----------+-------------------------------------------------------------------------------+
|order      |Ordered list. Prefix character is a number or a letter, depending on style     |
+-----------+-------------------------------------------------------------------------------+
|bullet     |Unordered or bulleted list. Prefix character is a bullet, dash, or other symbol|
+-----------+-------------------------------------------------------------------------------+
|alpha-lower|Ordered list. Prefix character is a lowercase alphabetical character           |
+-----------+-------------------------------------------------------------------------------+
|alpha-upper|Ordered list. Prefix character is an uppercase alphabetical character          |
+-----------+-------------------------------------------------------------------------------+
|roman-lower|Ordered list. Prefix character is a lowercase roman numeral                    |
+-----------+-------------------------------------------------------------------------------+
|roman-upper|Ordered list. Prefix character is an uppercase roman numeral                   |
+-----------+-------------------------------------------------------------------------------+
|simple     |Simple or plain list (No prefix character before each item)                    |
+-----------+-------------------------------------------------------------------------------+




Attribute name
--------------

Attribute

Identify the name of the element or attribute

Is attribute of: `elemattr`_, `element`_




Attribute no
------------

Attribute

Identify the number

Is attribute of: 


+-+-+
|0|0|
+-+-+




Attribute orgdiv1
-----------------

Attribute

Identify the organization division 1

Is attribute of: `aff`_


+--+--+
|nd|nd|
+--+--+




Attribute orgdiv2
-----------------

Attribute

Identify the organization division 2

Is attribute of: `aff`_


+--+--+
|nd|nd|
+--+--+




Attribute orgdiv3
-----------------

Attribute

Identify the organization division 3

Is attribute of: `aff`_


+--+--+
|nd|nd|
+--+--+




Attribute orgname
-----------------

Attribute

Identify the organization name

Is attribute of: `aff`_


+--+--+
|nd|nd|
+--+--+




Attribute pages
---------------

Attribute

Identify the pagination

Is attribute of: 


+---+---+
|0-0|0-0|
+---+---+




Attribute prodtype
------------------

Attribute

Identify the product type

Is attribute of: `product`_


+--------+--------+
|book    |book    |
+--------+--------+
|software|software|
+--------+--------+
|article |article |
+--------+--------+
|chapter |chapter |
+--------+--------+
|website |website |
+--------+--------+
|other   |other   |
+--------+--------+




Attribute pubtype
-----------------

Attribute

Identify the publication type

Is attribute of: 


+----+----------------------+
|epub|electronic publication|
+----+----------------------+
|ppub|print publication     |
+----+----------------------+




Attribute ref-type
------------------

Attribute

Identify the type of the reference

Is attribute of: `xref`_


+----------------------+--------------------------+
|aff                   |Affiliation               |
+----------------------+--------------------------+
|app                   |Appendix                  |
+----------------------+--------------------------+
|author-notes          |Author notes              |
+----------------------+--------------------------+
|bibr                  |Bibliographic reference   |
+----------------------+--------------------------+
|boxed-text            |Textbox or sidebar        |
+----------------------+--------------------------+
|chem                  |Chemical structure        |
+----------------------+--------------------------+
|contrib               |Contributor               |
+----------------------+--------------------------+
|corresp               |Corresponding author      |
+----------------------+--------------------------+
|disp-formula          |Display formula           |
+----------------------+--------------------------+
|fig                   |Figure or group of figures|
+----------------------+--------------------------+
|fn                    |Footnote                  |
+----------------------+--------------------------+
|kwd                   |Keyword                   |
+----------------------+--------------------------+
|list                  |List or list item         |
+----------------------+--------------------------+
|other                 |None of the items listed  |
+----------------------+--------------------------+
|plate                 |Plate                     |
+----------------------+--------------------------+
|scheme                |Scheme                    |
+----------------------+--------------------------+
|sec                   |Section                   |
+----------------------+--------------------------+
|statement             |Statement                 |
+----------------------+--------------------------+
|supplementary-material|Supplementary information |
+----------------------+--------------------------+
|table                 |Table or group of tables  |
+----------------------+--------------------------+




Attribute relid
---------------

Attribute

Identify the relation between the documents

Is attribute of: 




Attribute relidtp
-----------------

Attribute

Identify the type of relation between documents

Is attribute of: 


+-------------+-------------+
|art-access-id|art-access-id|
+-------------+-------------+
|coden        |coden        |
+-------------+-------------+
|doaj         |doaj         |
+-------------+-------------+
|doi          |doi          |
+-------------+-------------+
|medline      |medline      |
+-------------+-------------+
|manuscript   |manuscript   |
+-------------+-------------+
|rrn          |rrn          |
+-------------+-------------+
|other        |other        |
+-------------+-------------+
|pii          |pii          |
+-------------+-------------+
|pmcid        |pmcid        |
+-------------+-------------+
|pmid         |pmid         |
+-------------+-------------+
|publisher-id |publisher-id |
+-------------+-------------+
|sici         |sici         |
+-------------+-------------+




Attribute reltype
-----------------

Attribute

Identify the type of the related document

Is attribute of: 


+---------------------+-----------------------------------+
|unknown              |- choose one of the options below -|
+---------------------+-----------------------------------+
|unknown-object       |-- objects --                      |
+---------------------+-----------------------------------+
|vi                   |video                              |
+---------------------+-----------------------------------+
|au                   |audio                              |
+---------------------+-----------------------------------+
|table                |table                              |
+---------------------+-----------------------------------+
|figure               |figure                             |
+---------------------+-----------------------------------+
|other-object         |other object                       |
+---------------------+-----------------------------------+
|unknown-source       |-- sources --                      |
+---------------------+-----------------------------------+
|book                 |book                               |
+---------------------+-----------------------------------+
|book chapter         |book chapter                       |
+---------------------+-----------------------------------+
|database             |database                           |
+---------------------+-----------------------------------+
|article              |article                            |
+---------------------+-----------------------------------+
|pr                   |press release                      |
+---------------------+-----------------------------------+
|other-source         |other source                       |
+---------------------+-----------------------------------+
|unknown-related-type |-- related types --                |
+---------------------+-----------------------------------+
|addended-article     |addended-article                   |
+---------------------+-----------------------------------+
|addendum             |addendum                           |
+---------------------+-----------------------------------+
|commentary-article   |commentary-article                 |
+---------------------+-----------------------------------+
|object-of-concern    |object-of-concern                  |
+---------------------+-----------------------------------+
|companion            |companion                          |
+---------------------+-----------------------------------+
|corrected-article    |corrected-article                  |
+---------------------+-----------------------------------+
|letter               |letter                             |
+---------------------+-----------------------------------+
|retracted-article    |retracted-article                  |
+---------------------+-----------------------------------+
|peer-reviewed-article|peer-reviewed-article              |
+---------------------+-----------------------------------+
|peer-review          |peer-review                        |
+---------------------+-----------------------------------+
|other-related-type   |other related type                 |
+---------------------+-----------------------------------+




Attribute resptp
----------------

Attribute

Identify the response type

Is attribute of: `docresp`_, `response`_


+----------+----------+
|addendum  |addendum  |
+----------+----------+
|discussion|discussion|
+----------+----------+
|reply     |reply     |
+----------+----------+




Attribute rid
-------------

Attribute

Identify an reference to an ID

Is attribute of: `author`_, `sig`_, `xref`_


+--+-----------+
|nd|No definido|
+--+-----------+




Attribute role
--------------

Attribute

Identify the Role of the author

Is attribute of: `author`_, `authors`_, `oauthor`_, `sig`_, `subresp`_


+-----+-----------+
|nd   |Not defined|
+-----+-----------+
|coord|coordinator|
+-----+-----------+
|ed   |publisher  |
+-----+-----------+
|org  |organizer  |
+-----+-----------+
|tr   |translator |
+-----+-----------+




Attribute scheme
----------------

Attribute

Identify the controlled vocabulary

Is attribute of: `keygrp`_


+----+--------------------------+
|nd  |No Descriptor             |
+----+--------------------------+
|decs|Health Science Descriptors|
+----+--------------------------+




Attribute sec-type
------------------

Attribute

Identify the type of the section

Is attribute of: `sec`_


+------------------------------+----------------------------------+
|nd                            |undefined                         |
+------------------------------+----------------------------------+
|materials|methods             |* Materials and Methodology       |
+------------------------------+----------------------------------+
|results|discussion            |* Results and Discussion          |
+------------------------------+----------------------------------+
|results|conclusions           |* Results and Conclusions         |
+------------------------------+----------------------------------+
|results|discussion|conclusions|* Results, Discussion, Conclusions|
+------------------------------+----------------------------------+
|cases                         |Cases/Case Reports                |
+------------------------------+----------------------------------+
|conclusions                   |Conclusions/Comment               |
+------------------------------+----------------------------------+
|discussion                    |Discussion/Interpretation         |
+------------------------------+----------------------------------+
|intro                         |Introduction/Synopsis             |
+------------------------------+----------------------------------+
|materials                     |Materials                         |
+------------------------------+----------------------------------+
|methods                       |Methods/Methodology/Procedures    |
+------------------------------+----------------------------------+
|results                       |Results/Statement of Findings     |
+------------------------------+----------------------------------+
|subjects                      |Subjects/Participants/Patients    |
+------------------------------+----------------------------------+
|supplementary-material        |Supplementary materials           |
+------------------------------+----------------------------------+




Attribute specyear
------------------

Attribute

Identify the year as presented in the reference. E.g.: 2005, c1900 (about 1900), 1800a, etc.

Is attribute of: `date`_




Attribute sponsor
-----------------

Attribute

Identify the funding institution

Is attribute of: 


+--+------------+
|nd|Not definido|
+--+------------+




Attribute standard
------------------

Attribute

Identify the standard adopted by the journal

Is attribute of: `abnt6023`_, `apa`_, `iso690`_, `other`_, `vancouv`_


+-------+-------------------------------------------------------------------------------------------+
|iso690 |iso 690/87 - international standard organization                                           |
+-------+-------------------------------------------------------------------------------------------+
|nbr6023|nbr 6023/89 - associação nacional de normas técnicas                                       |
+-------+-------------------------------------------------------------------------------------------+
|other  |other standard                                                                             |
+-------+-------------------------------------------------------------------------------------------+
|vancouv|the vancouver group - uniform requirements for manuscripts submitted to biomedical journals|
+-------+-------------------------------------------------------------------------------------------+
|apa    |American Psychological Association                                                         |
+-------+-------------------------------------------------------------------------------------------+




Attribute subarttp
------------------

Attribute

Identify the type of the sub-article

Is attribute of: `subart`_, `subdoc`_


+-------------------+-------------------+
|translation        |translation        |
+-------------------+-------------------+
|abstract           |abstract           |
+-------------------+-------------------+
|addendum           |addendum           |
+-------------------+-------------------+
|announcement       |announcement       |
+-------------------+-------------------+
|article-commentary |article-commentary |
+-------------------+-------------------+
|book-review        |book-review        |
+-------------------+-------------------+
|books-received     |books-received     |
+-------------------+-------------------+
|brief-report       |brief-report       |
+-------------------+-------------------+
|calendar           |calendar           |
+-------------------+-------------------+
|case-report        |case-report        |
+-------------------+-------------------+
|collection         |collection         |
+-------------------+-------------------+
|correction         |correction         |
+-------------------+-------------------+
|discussion         |discussion         |
+-------------------+-------------------+
|dissertation       |dissertation       |
+-------------------+-------------------+
|editorial          |editorial          |
+-------------------+-------------------+
|in-brief           |in-brief           |
+-------------------+-------------------+
|introduction       |introduction       |
+-------------------+-------------------+
|letter             |letter             |
+-------------------+-------------------+
|meeting-report     |meeting-report     |
+-------------------+-------------------+
|news               |news               |
+-------------------+-------------------+
|obituary           |obituary           |
+-------------------+-------------------+
|oration            |oration            |
+-------------------+-------------------+
|partial-retraction |partial-retraction |
+-------------------+-------------------+
|procut-review      |procut-review      |
+-------------------+-------------------+
|rapid-communication|rapid-communication|
+-------------------+-------------------+
|reply              |reply              |
+-------------------+-------------------+
|reprint            |reprint            |
+-------------------+-------------------+
|research-article   |research-article   |
+-------------------+-------------------+
|retraction         |retraction         |
+-------------------+-------------------+
|review-article     |review-article     |
+-------------------+-------------------+




Attribute to
------------

Attribute

Identify the due date

Is attribute of: `dperiod`_


+--------+--------+
|00000000|00000000|
+--------+--------+




Attribute toccode
-----------------

Attribute

Identify the indicates whether the text title is present on the table of contents (title) or not (sectitle)

Is attribute of: 


+-+--------+
|1|title   |
+-+--------+
|2|sectitle|
+-+--------+




Attribute value
---------------

Attribute

Identify the value of the element or attribute

Is attribute of: `elemattr`_




Attribute version
-----------------

Attribute

Identify the version of the document

Is attribute of: 


+---+---+
|3.1|3.1|
+---+---+
|4.0|4.0|
+---+---+




[]
