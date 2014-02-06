SGML Markup Tags
================

article
-------
Identify the article
children: `deposit`_, `front`_, `xmlbody`_, `body`_, `back`_, `response`_, `subart`_

text
----
Identify a text
children: `doi`_, `titlegrp`_, `authgrp`_, `xmlbody`_, `back`_

abnt6023
--------
Group the elements of references which are according to NBR 6023/89 of ABNT
children: `acitat`_

abstract
--------
Identify the abstract of the article

accepted
--------
Identify the date in which the article was accepted to publish

acitat
------
Identify a bibliography reference
children: `no`_, `acontrib`_, `amonog`_, `aiserial`_, `confgrp`_

acontrib
--------
Group the elements of a contribution
children: `author`_, `corpauth`_, `et-al`_, `title`_, `subtitle`_, `volid`_, `pages`_, `patgrp`_

aff
---
Identify the organization to which the author is affiliated
children: `label`_, `city`_, `state`_, `country`_, `zipcode`_, `email`_

aiserial
--------
Group the elements of a serial publication
children: `sertitle`_, `stitle`_, `isstitle`_, `date`_, `volid`_, `issueno`_, `suppl`_, `pages`_, `extent`_, `url`_, `cited`_, `doi`_, `pubid`_, `issn`_, `city`_, `state`_, `country`_, `pubname`_, `notes`_

amonog
------
Group the elements of a monograph
children: `author`_, `corpauth`_, `et-al`_, `title`_, `subtitle`_, `date`_, `edition`_, `volid`_, `part`_, `tome`_, `coltitle`_, `colvolid`_, `pages`_, `extent`_, `city`_, `state`_, `country`_, `pubname`_, `patgrp`_, `confgrp`_, `thesis`_, `report`_, `isbn`_, `url`_, `cited`_, `doi`_, `pubid`_, `subresp`_, `notes`_

anonym
------
Identify anonymous authorship

apa
---
Group the elements of references which are according to APA
children: `pcitat`_

app
---
Identify the appendix
children: `title`_, `sec`_, `p`_

authgrp
-------
Group the authors of the document
children: `author+`_, `author`_, `onbehalf`_, `corpauth`_

author
------
Group the elements of the author, such as name, last name and role
children: `fname`_, `surname`_, `previous`_

back
----
Identify the back part of the document
children: `ack`_, `vancouv`_, `iso690`_, `abnt6023`_, `apa`_, `other`_, `fngrp`_, `licenses`_, `bbibcom`_, `glossary`_, `app`_

bbibcom
-------
Group other elements that are in the back
children: `abstract`_, `keygrp`_, `confgrp`_, `report`_, `thesgrp`_, `hist`_, `title`_, `subtitle`_

bibcom
------
Group other elements that are in front
children: `abstract`_, `xmlabstr`_, `keygrp`_, `confgrp`_, `report`_, `thesgrp`_, `hist`_

body
----
Identify the body of the document, without details

caption
-------
Identify the caption

cited
-----
Identify the date in which the article was accessed

city
----
Identify the city

cltrial
-------
Group the elements of a clinical trial
children: `ctreg`_

coltitle
--------
Identify the title of a collection

colvolid
--------
Identify the volume of a collection

confgrp
-------
Group the elements of a conference
children: `confname`_, `no`_, `date`_, `city`_, `state`_, `country`_, `sponsor`_

confname
--------
Identify the conference name

contract
--------
Identify the contract/project number given by the sponsor

corpauth
--------
Identify the corporative author
children: `orgname`_, `orgdiv`_, `previous`_

country
-------
Identify the country

ctreg
-----
Identify the clinical trial number

date
----
Identify the date of registration of the patent

def
---
Identify the definition of a term

defitem
-------
Identify an item of a list of definitions
children: `term`_, `def`_

deflist
-------
Identify a list of definitions
children: `title`_, `defitem`_

degree
------
 Identify the degree of the thesis, such as Master, Doctor etc

deposit
-------
Identify the date of deposit in the repository

doi
---
Identify the DOI

dperiod
-------
Identify the período of time tratado at the content of the document

edition
-------
Identify the edition number

email
-----
Electronic address of the author

equation
--------
Identify the elements of a equation
children: `graphic`_, `texmath`_, `mmlmath`_

et-al
-----
Indicate non cited authors

extent
------
Identify the extension of the document (number of pages)

figgrp
------
Group the elements of a figure
children: `label`_, `caption`_, `graphic`_

figgrps
-------
Group a group of figures (Fig 1A, 1B,...)
children: `label`_, `caption`_, `figgrp`_

fname
-----
Identify the first names of an individual author

fngrp
-----
Group the elements of a footnote

front
-----
Identify the front of a document
children: `related`_, `toctitle`_, `doi`_, `titlegrp`_, `authgrp`_, `bibcom`_

glossary
--------
Identify a glossary
children: `label`_, `title`_, `glossary`_, `deflist`_

graphic
-------
Identify an image

hist
----
Identify the history of an article (received and accepted dates)
children: `received`_, `revised`_, `accepted`_

icitat
------
Identify a reference in ISO 690/87
children: `no`_, `icontrib`_, `imonog`_, `iiserial`_

icontrib
--------
Group the elements of contribution
children: `author`_, `corpauth`_, `et-al`_, `subresp`_, `date`_, `title`_, `subtitle`_

ign
---
Ignored text

iiserial
--------
Group the elements of serial
children: `isstitle`_, `author`_, `corpauth`_, `et-al`_, `medium`_, `sertitle`_, `stitle`_, `city`_, `state`_, `country`_, `edition`_, `pubname`_, `date`_, `update`_, `volid`_, `issueno`_, `pages`_, `isdesig`_, `notes`_, `issn`_, `url`_, `cited`_, `doi`_, `pubid`_

imonog
------
Group the elements of monograph
children: `author`_, `corpauth`_, `et-al`_, `subresp`_, `title`_, `subtitle`_, `medium`_, `edition`_, `city`_, `state`_, `country`_, `pubname`_, `date`_, `update`_, `volid`_, `part`_, `pages`_, `extent`_, `coltitle`_, `report`_, `notes`_, `url`_, `cited`_, `doi`_, `pubid`_, `isbn`_, `patgrp`_

inpress
-------
Identify the document is in press status

isbn
----
Identify the Internacional Standard Book Number (ISBN)

isdesig
-------
Identify the main dates of a collection, for instance, the initial date of the collection

iso690
------
Group the elements of bibliography references which are according to ISO 690/87
children: `icitat`_

issn
----
Identify the Internacional Standard Serial  Number (ISSN)

isstitle
--------
Identify the title of an issue number

issueno
-------
Identify the issue number

keygrp
------
Group the key words of a document
children: `keyword`_, `subkey`_, `dperiod`_

keyword
-------
Identify a key word of the document

label
-----
Identify a label

li
--
Identify an item of a list
children: `lilabel`_, `litext`_

license
-------
Identify the text of a license
children: `licensep`_

licensep
--------
Identify the paragraph of a license

licenses
--------
Group the elements of a license
children: `license`_

lilabel
-------
Identify the label of a item of a list

list
----
Identify the list
children: `li`_

litext
------
Identify the text of a item of a list

location
--------
Identify the electronic address of the document

medium
------
Identify the format of the media in which the document is published

mmlmath
-------
Math (MathML 2.0 Tag Set)

no
--
Identify the number

notes
-----
Identify notes

oauthor
-------
Group the elements of an individual author
children: `fname`_, `surname`_, `anonym`_, `previous`_

ocitat
------
Identify a reference
children: `no`_, `ocontrib`_, `omonog`_, `oiserial`_, `confgrp`_

ocontrib
--------
Group the elements of a contribution
children: `oauthor`_, `ocorpaut`_, `et-al`_, `title`_, `subtitle`_, `date`_, `pages`_, `patgrp`_

ocorpaut
--------
Identify a corporative author
children: `orgname`_, `orgdiv`_, `previous`_

oiserial
--------
Group the elements of serial
children: `sertitle`_, `stitle`_, `isstitle`_, `date`_, `volid`_, `issueno`_, `suppl`_, `pages`_, `extent`_, `issn`_, `url`_, `cited`_, `doi`_, `pubid`_, `othinfo`_, `city`_, `country`_, `pubname`_

omonog
------
Group the elements of monograph
children: `oauthor`_, `ocorpaut`_, `et-al`_, `title`_, `subtitle`_, `date`_, `pages`_, `extent`_, `edition`_, `thesis`_, `confgrp`_, `report`_, `patgrp`_, `city`_, `state`_, `country`_, `pubname`_, `coltitle`_, `volid`_, `part`_, `url`_, `cited`_, `doi`_, `pubid`_, `isbn`_, `othinfo`_

orgdiv
------
Identify the division of an institution

orgname
-------
Identify the name of an institution

other
-----
Group the elements of bibliography references which are not according to any adopted standard
children: `ocitat`_

othinfo
-------
Group any other information

p
-
Identify a paragraph
children: `report`_

pages
-----
Identify the pagination

part
----
Identify the part of the volume/issue number

patent
------
Identify the number of the patent

patgrp
------
Group the elements of patent
children: `orgname`_, `patent`_, `date`_

pcitat
------
Identify a bibliography reference
children: `no`_, `pcontrib`_, `pmonog`_, `piserial`_

pcontrib
--------
Group the elements of contribution
children: `author`_, `corpauth`_, `date`_, `title`_, `subtitle`_

piserial
--------
Group the elements of serial
children: `sertitle`_, `volid`_, `issueno`_, `suppl`_, `pages`_, `url`_, `cited`_, `doi`_, `pubid`_

pmonog
------
Group the elements of monograph
children: `author`_, `corpauth`_, `date`_, `title`_, `volid`_, `part`_, `subtitle`_, `confgrp`_, `thesis`_, `coltitle`_, `colvolid`_, `pages`_, `edition`_, `city`_, `state`_, `country`_, `pubname`_, `report`_, `url`_, `cited`_, `doi`_, `pubid`_, `notes`_

previous
--------
Identify the author is the same author of the previous reference

projname
--------
Identify the name of the project

pubname
-------
Identify the publisher

received
--------
Identify the date in which the article was received by peer review system

related
-------
Identify related documents

report
------
Group the elements of funding
children: `no`_, `rsponsor`_, `awarded`_, `projname`_, `contract`_

response
--------
Group the elements of a response to an article
children: `front`_, `body`_, `back`_

revised
-------
Identify the date in which the article was revised by peer review system

rsponsor
--------
Identify the sponsor or funding institution
children: `orgname`_, `orgdiv`_

sciname
-------
Identify scientific names

sec
---
Identify a section
children: `sectitle`_, `subsec`_, `p`_

sectitle
--------
Identify a section title

sertitle
--------
Identify the journal title

sponsor
-------
Identify the sponsor or funding institution
children: `orgname`_, `orgdiv`_

state
-----
Identify the state/region

stitle
------
Identify the short title of a journal

subart
------
Identify the text which is related to the article
children: `front`_, `xmlbody`_, `body`_, `back`_, `response`_

subkey
------
Identify the subkey of a key word

subresp
-------
Identify the secondary responsabilities
children: `fname`_, `surname`_

subsec
------
Identify a sub-section
children: `sectitle`_, `p`_

subtitle
--------
Identify the subtitle

suppl
-----
Identify the supplement

surname
-------
Identify the last name

tabwrap
-------
Group the elements of a table
children: `label`_, `caption`_, `graphic`_, `table`_, `fntable`_

term
----
Identify a term

texmath
-------
Identify a formula using Tex Math Equation

thesgrp
-------
Group the elements of a thesis
children: `city`_, `state`_, `country`_, `date`_, `degree`_, `orgname`_, `orgdiv`_

thesis
------
Group the elements of a thesis
children: `city`_, `state`_, `country`_, `date`_, `degree`_, `orgname`_, `orgdiv`_

title
-----
Identify the title of the document

titlegrp
--------
Group the titles of the document
children: `title`_, `subtitle`_

tome
----
Identify the tome of a publication

tp
--
Identify the type of publication

update
------
Identify the information of update

uri
---
Identify an uri

url
---
Identify the electronic address of the document

vancouv
-------
Group the elements of bibliography references which are according to Vancouver
children: `vcitat`_

vcitat
------
Identify a bibliography reference
children: `no`_, `vcontrib`_, `viserial`_, `vmonog`_

vcontrib
--------
Group the elements of contribution
children: `author`_, `corpauth`_, `et-al`_, `vtitle`_, `patgrp`_

version
-------
Identify the version

viserial
--------
Group the elements of serial
children: `vstitle`_, `date`_, `inpress`_, `volid`_, `issueno`_, `suppl`_, `part`_, `extent`_, `pages`_, `url`_, `cited`_, `doi`_, `pubid`_

vmonog
------
Group the elements of monograph
children: `author`_, `corpauth`_, `et-al`_, `vtitle`_, `edition`_, `volid`_, `part`_, `version`_, `confgrp`_, `city`_, `state`_, `country`_, `pubname`_, `inpress`_, `date`_, `pages`_, `extent`_, `report`_, `thesis`_, `url`_, `cited`_, `doi`_, `pubid`_, `patgrp`_, `coltitle`_

volid
-----
Identify the volume

vstitle
-------
Short title in Vancouver
children: `stitle`_, `tp`_

vtitle
------
Group the elements of title in Vancouver
children: `title`_, `subtitle`_, `tp`_

xmlbody
-------
Identify the body of the document, in details
children: `sec`_, `p`_, `deflist`_, `sigblock`_

xref
----
Identify a cross-reference

zipcode
-------
Identify a ZIP Code



.. include:: draft_version.rst
