----
abnt6023
--------
Element
Group the elements of references which are according to NBR 6023/89 of ABNT
Contained in: `back`_
Contains: `acitat`_
Attributes: `standard`_, `count`_

----
abstract
--------
Element
Identify the abstract of the article
Contained in: `bbibcom`_, `bibcom`_
Attributes: `language`_

----
accepted
--------
Element
Identify the date in which the article was accepted to publish
Contained in: `hist`_
Attributes: `dateiso`_

----
acitat
------
Element
Identify a bibliography reference
Contained in: `abnt6023`_
Contains: `no`_, `acontrib`_, `amonog`_, `aiserial`_, `confgrp`_
Attributes: none

----
ack
---
Element
Group the elements of acknowledgment
Contained in: `back`_
Contains: `title`_, `p`_
Attributes: none

----
acontrib
--------
Element
Group the elements of a contribution
Contained in: `acitat`_
Contains: `author`_, `corpauth`_, `et-al`_, `title`_, `subtitle`_, `volid`_, `pages`_, `patgrp`_
Attributes: none

----
aff
---
Element
Identify the organization to which the author is affiliated
Contained in: `ifloat`_
Contains: `label`_, `city`_, `state`_, `country`_, `zipcode`_, `email`_
Attributes: `id`_, `orgname`_, `orgdiv1`_, `orgdiv2`_, `orgdiv3`_

----
aiserial
--------
Element
Group the elements of a serial publication
Contained in: `acitat`_
Contains: `sertitle`_, `stitle`_, `isstitle`_, `date`_, `volid`_, `issueno`_, `suppl`_, `pages`_, `extent`_, `url`_, `cited`_, `doi`_, `pubid`_, `issn`_, `city`_, `state`_, `country`_, `pubname`_, `notes`_
Attributes: none

----
amonog
------
Element
Group the elements of a monograph
Contained in: `acitat`_
Contains: `author`_, `corpauth`_, `et-al`_, `title`_, `subtitle`_, `date`_, `edition`_, `volid`_, `part`_, `tome`_, `coltitle`_, `colvolid`_, `pages`_, `extent`_, `city`_, `state`_, `country`_, `pubname`_, `patgrp`_, `confgrp`_, `thesis`_, `report`_, `isbn`_, `url`_, `cited`_, `doi`_, `pubid`_, `subresp`_, `notes`_
Attributes: none

----
anonym
------
Element
Identify anonymous authorship
Contained in: `oauthor`_
Attributes: none

----
apa
---
Element
Group the elements of references which are according to APA
Contained in: `back`_
Contains: `pcitat`_
Attributes: `standard`_, `count`_

----
app
---
Element
Identify the appendix
Contained in: `back`_
Contains: `title`_, `sec`_, `p`_
Attributes: `id`_

----
article
-------
Element
Identify the article
Contained in: `start`_
Contains: `deposit`_, `front`_, `xmlbody`_, `body`_, `back`_, `response`_, `subart`_
Attributes: none

----
authgrp
-------
Element
Group the authors of the document
Contained in: `front`_, `text`_
Contains: `author+`_, `author`_, `onbehalf`_, `corpauth`_
Attributes: none

----
author
------
Element
Group the elements of the author, such as name, last name and role
Contained in: `acontrib`_, `amonog`_, `authgrp`_, `icontrib`_, `iiserial`_, `imonog`_, `pcontrib`_, `pmonog`_, `product`_, `vcontrib`_, `vmonog`_
Contains: `fname`_, `surname`_, `previous`_
Attributes: `role`_, `rid`_, `corresp`_, `deceased`_, `eqcontr`_

----
back
----
Element
Identify the back part of the document
Contained in: `article`_, `response`_, `subart`_, `text`_
Contains: `ack`_, `vancouv`_, `iso690`_, `abnt6023`_, `apa`_, `other`_, `fngrp`_, `licenses`_, `bbibcom`_, `glossary`_, `app`_
Attributes: none

----
bbibcom
-------
Element
Group other elements that are in the back
Contained in: `back`_
Contains: `abstract`_, `keygrp`_, `confgrp`_, `report`_, `thesgrp`_, `hist`_, `title`_, `subtitle`_
Attributes: none

----
bibcom
------
Element
Group other elements that are in front
Contained in: `front`_
Contains: `abstract`_, `xmlabstr`_, `keygrp`_, `confgrp`_, `report`_, `thesgrp`_, `hist`_
Attributes: none

----
body
----
Element
Identify the body of the document, without details
Contained in: `article`_, `response`_, `subart`_, `text`_
Attributes: none

----
caption
-------
Element
Identify the caption
Contained in: `figgrp`_, `figgrps`_, `tabwrap`_
Attributes: none

----
cited
-----
Element
Identify the date in which the article was accessed
Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `viserial`_, `vmonog`_
Attributes: `dateiso`_

----
city
----
Element
Identify the city
Contained in: `aff`_, `aiserial`_, `amonog`_, `confgrp`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `pmonog`_, `product`_, `thesgrp`_, `thesis`_, `vmonog`_
Attributes: none

----
cltrial
-------
Element
Group the elements of a clinical trial
Contained in: `ifloat`_
Contains: `ctreg`_
Attributes: none

----
coltitle
--------
Element
Identify the title of a collection
Contained in: `amonog`_, `imonog`_, `omonog`_, `pmonog`_, `vmonog`_
Attributes: none

----
colvolid
--------
Element
Identify the volume of a collection
Contained in: `amonog`_, `pmonog`_
Attributes: none

----
confgrp
-------
Element
Group the elements of a conference
Contained in: `acitat`_, `amonog`_, `bbibcom`_, `bibcom`_, `ocitat`_, `omonog`_, `pmonog`_, `vmonog`_
Contains: `confname`_, `no`_, `date`_, `city`_, `state`_, `country`_, `sponsor`_
Attributes: none

----
confname
--------
Element
Identify the conference name
Contained in: `confgrp`_
Attributes: none

----
contract
--------
Element
Identify the contract/project number given by the sponsor
Contained in: `report`_
Attributes: none

----
corpauth
--------
Element
Identify the corporative author
Contained in: `acontrib`_, `amonog`_, `authgrp`_, `icontrib`_, `iiserial`_, `imonog`_, `pcontrib`_, `pmonog`_, `product`_, `vcontrib`_, `vmonog`_
Contains: `orgname`_, `orgdiv`_, `previous`_
Attributes: none

----
country
-------
Element
Identify the country
Contained in: `aff`_, `aiserial`_, `amonog`_, `confgrp`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `pmonog`_, `product`_, `thesgrp`_, `thesis`_, `vmonog`_
Attributes: none

----
ctreg
-----
Element
Identify the clinical trial number
Contained in: `cltrial`_
Attributes: `cturl`_, `ctdbid`_

----
date
----
Element
Identify the date of registration of the patent
Contained in: `aiserial`_, `amonog`_, `confgrp`_, `icontrib`_, `iiserial`_, `imonog`_, `ocontrib`_, `oiserial`_, `omonog`_, `patgrp`_, `pcontrib`_, `pmonog`_, `product`_, `thesgrp`_, `thesis`_, `viserial`_, `vmonog`_
Attributes: `dateiso`_, `specyear`_

----
def
---
Element
Identify the definition of a term
Contained in: `defitem`_
Attributes: none

----
defitem
-------
Element
Identify an item of a list of definitions
Contained in: `deflist`_
Contains: `term`_, `def`_
Attributes: none

----
deflist
-------
Element
Identify a list of definitions
Contained in: `glossary`_, `xmlbody`_
Contains: `title`_, `defitem`_
Attributes: `id`_

----
degree
------
Element
 Identify the degree of the thesis, such as Master, Doctor etc
Contained in: `thesgrp`_, `thesis`_
Attributes: none

----
deposit
-------
Element
Identify the date of deposit in the repository
Contained in: `article`_
Attributes: `deposid`_, `entrdate`_, `embdate`_

----
doi
---
Element
Identify the DOI
Contained in: `aiserial`_, `amonog`_, `front`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `text`_, `viserial`_, `vmonog`_
Attributes: none

----
dperiod
-------
Element
Identify the período of time tratado at the content of the document
Contained in: `keygrp`_
Attributes: `from`_, `to`_

----
edition
-------
Element
Identify the edition number
Contained in: `amonog`_, `iiserial`_, `imonog`_, `omonog`_, `pmonog`_, `vmonog`_
Attributes: none

----
email
-----
Element
Electronic address of the author
Contained in: `aff`_, `corresp`_
Attributes: none

----
equation
--------
Element
Identify the elements of a equation
Contained in: `ifloat`_
Contains: `graphic`_, `texmath`_, `mmlmath`_
Attributes: `id`_, `filename`_

----
et-al
-----
Element
Indicate non cited authors
Contained in: `acontrib`_, `amonog`_, `icontrib`_, `iiserial`_, `imonog`_, `ocontrib`_, `omonog`_, `vcontrib`_, `vmonog`_
Attributes: none

----
extent
------
Element
Identify the extension of the document (number of pages)
Contained in: `aiserial`_, `amonog`_, `imonog`_, `oiserial`_, `omonog`_, `viserial`_, `vmonog`_
Attributes: none

----
figgrp
------
Element
Group the elements of a figure
Contained in: `ifloat`_, `figgrps`_
Contains: `label`_, `caption`_, `graphic`_
Attributes: `id`_, `ftype`_, `filename`_

----
figgrps
-------
Element
Group a group of figures (Fig 1A, 1B,...)
Contained in: `ifloat`_
Contains: `label`_, `caption`_, `figgrp`_
Attributes: `id`_

----
fname
-----
Element
Identify the first names of an individual author
Contained in: `author`_, `awarded`_, `oauthor`_, `subresp`_
Attributes: none

----
fngrp
-----
Element
Group the elements of a footnote
Contained in: `back`_
Attributes: `id`_, `fntype`_

----
front
-----
Element
Identify the front of a document
Contained in: `article`_, `response`_, `subart`_
Contains: `related`_, `toctitle`_, `doi`_, `titlegrp`_, `authgrp`_, `bibcom`_
Attributes: none

----
glossary
--------
Element
Identify a glossary
Contained in: `back`_, `glossary`_
Contains: `label`_, `title`_, `glossary`_, `deflist`_
Attributes: `id`_

----
graphic
-------
Element
Identify an image
Contained in: `ifloat`_, `equation`_, `figgrp`_, `tabwrap`_
Attributes: `href`_

----
hist
----
Element
Identify the history of an article (received and accepted dates)
Contained in: `bbibcom`_, `bibcom`_
Contains: `received`_, `revised`_, `accepted`_
Attributes: none

----
icitat
------
Element
Identify a reference in ISO 690/87
Contained in: `iso690`_
Contains: `no`_, `icontrib`_, `imonog`_, `iiserial`_
Attributes: none

----
icontrib
--------
Element
Group the elements of contribution
Contained in: `icitat`_
Contains: `author`_, `corpauth`_, `et-al`_, `subresp`_, `date`_, `title`_, `subtitle`_
Attributes: none

----
ign
---
Element
Ignored text
Contained in: `ifloat`_
Attributes: none

----
iiserial
--------
Element
Group the elements of serial
Contained in: `icitat`_
Contains: `isstitle`_, `author`_, `corpauth`_, `et-al`_, `medium`_, `sertitle`_, `stitle`_, `city`_, `state`_, `country`_, `edition`_, `pubname`_, `date`_, `update`_, `volid`_, `issueno`_, `pages`_, `isdesig`_, `notes`_, `issn`_, `url`_, `cited`_, `doi`_, `pubid`_
Attributes: none

----
imonog
------
Element
Group the elements of monograph
Contained in: `icitat`_
Contains: `author`_, `corpauth`_, `et-al`_, `subresp`_, `title`_, `subtitle`_, `medium`_, `edition`_, `city`_, `state`_, `country`_, `pubname`_, `date`_, `update`_, `volid`_, `part`_, `pages`_, `extent`_, `coltitle`_, `report`_, `notes`_, `url`_, `cited`_, `doi`_, `pubid`_, `isbn`_, `patgrp`_
Attributes: none

----
inpress
-------
Element
Identify the document is in press status
Contained in: `viserial`_, `vmonog`_
Attributes: none

----
isbn
----
Element
Identify the Internacional Standard Book Number (ISBN)
Contained in: `amonog`_, `imonog`_, `omonog`_, `product`_
Attributes: none

----
isdesig
-------
Element
Identify the main dates of a collection, for instance, the initial date of the collection
Contained in: `iiserial`_
Attributes: none

----
iso690
------
Element
Group the elements of bibliography references which are according to ISO 690/87
Contained in: `back`_
Contains: `icitat`_
Attributes: `standard`_, `count`_

----
issn
----
Element
Identify the Internacional Standard Serial  Number (ISSN)
Contained in: `aiserial`_, `iiserial`_, `oiserial`_
Attributes: none

----
isstitle
--------
Element
Identify the title of an issue number
Contained in: `aiserial`_, `iiserial`_, `oiserial`_
Attributes: none

----
issueno
-------
Element
Identify the issue number
Contained in: `aiserial`_, `iiserial`_, `oiserial`_, `piserial`_, `viserial`_
Attributes: none

----
keygrp
------
Element
Group the key words of a document
Contained in: `bbibcom`_, `bibcom`_
Contains: `keyword`_, `subkey`_, `dperiod`_
Attributes: `scheme`_

----
keyword
-------
Element
Identify a key word of the document
Contained in: `keygrp`_
Attributes: `keyword priority level`_, `language`_, `id`_

----
label
-----
Element
Identify a label
Contained in: `aff`_, `figgrp`_, `figgrps`_, `fntable`_, `glossary`_, `tabwrap`_
Attributes: none

----
li
--
Element
Identify an item of a list
Contained in: `list`_
Contains: `lilabel`_, `litext`_
Attributes: none

----
license
-------
Element
Identify the text of a license
Contained in: `licenses`_
Contains: `licensep`_
Attributes: `language`_, `lictype`_, `href`_

----
licensep
--------
Element
Identify the paragraph of a license
Contained in: `license`_
Attributes: none

----
licenses
--------
Element
Group the elements of a license
Contained in: `back`_
Contains: `license`_
Attributes: none

----
lilabel
-------
Element
Identify the label of a item of a list
Contained in: `li`_
Attributes: none

----
list
----
Element
Identify the list
Contained in: `ifloat`_
Contains: `li`_
Attributes: `listtype`_

----
litext
------
Element
Identify the text of a item of a list
Contained in: `li`_
Attributes: none

----
medium
------
Element
Identify the format of the media in which the document is published
Contained in: `iiserial`_, `imonog`_
Attributes: none

----
mmlmath
-------
Element
Math (MathML 2.0 Tag Set)
Contained in: `equation`_
Attributes: none

----
no
--
Element
Identify the number
Contained in: `acitat`_, `confgrp`_, `icitat`_, `ocitat`_, `pcitat`_, `report`_, `vcitat`_
Attributes: none

----
notes
-----
Element
Identify notes
Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `pmonog`_
Attributes: none

----
oauthor
-------
Element
Group the elements of an individual author
Contained in: `ocontrib`_, `omonog`_
Contains: `fname`_, `surname`_, `anonym`_, `previous`_
Attributes: `role`_, `rid`_

----
ocitat
------
Element
Identify a reference
Contained in: `other`_
Contains: `no`_, `ocontrib`_, `omonog`_, `oiserial`_, `confgrp`_
Attributes: none

----
ocontrib
--------
Element
Group the elements of a contribution
Contained in: `ocitat`_
Contains: `oauthor`_, `ocorpaut`_, `et-al`_, `title`_, `subtitle`_, `date`_, `pages`_, `patgrp`_
Attributes: none

----
ocorpaut
--------
Element
Identify a corporative author
Contained in: `ocontrib`_, `omonog`_
Contains: `orgname`_, `orgdiv`_, `previous`_
Attributes: none

----
oiserial
--------
Element
Group the elements of serial
Contained in: `ocitat`_
Contains: `sertitle`_, `stitle`_, `isstitle`_, `date`_, `volid`_, `issueno`_, `suppl`_, `pages`_, `extent`_, `issn`_, `url`_, `cited`_, `doi`_, `pubid`_, `othinfo`_, `city`_, `country`_, `pubname`_
Attributes: none

----
omonog
------
Element
Group the elements of monograph
Contained in: `ocitat`_
Contains: `oauthor`_, `ocorpaut`_, `et-al`_, `title`_, `subtitle`_, `date`_, `pages`_, `extent`_, `edition`_, `thesis`_, `confgrp`_, `report`_, `patgrp`_, `city`_, `state`_, `country`_, `pubname`_, `coltitle`_, `volid`_, `part`_, `url`_, `cited`_, `doi`_, `pubid`_, `isbn`_, `othinfo`_
Attributes: none

----
onbehalf
--------
Element
Identify the institution which the contributor represents. Example: John Smith on behalf of Instituition ABCD
Contained in: `authgrp`_
Attributes: none

----
orgdiv
------
Element
Identify the division of an institution
Contained in: `awarded`_, `corpauth`_, `ocorpaut`_, `rsponsor`_, `sponsor`_, `thesgrp`_, `thesis`_
Attributes: none

----
orgname
-------
Element
Identify the name of an institution
Contained in: `awarded`_, `corpauth`_, `ocorpaut`_, `patgrp`_, `rsponsor`_, `sponsor`_, `thesgrp`_, `thesis`_
Attributes: none

----
other
-----
Element
Group the elements of bibliography references which are not according to any adopted standard
Contained in: `back`_
Contains: `ocitat`_
Attributes: `standard`_, `count`_

----
othinfo
-------
Element
Group any other information
Contained in: `oiserial`_, `omonog`_, `product`_
Attributes: none

----
p
-
Element
Identify a paragraph
Contained in: `ack`_, `app`_, `sec`_, `subsec`_, `xmlabstr`_, `xmlbody`_
Contains: `report`_
Attributes: none

----
pages
-----
Element
Identify the pagination
Contained in: `acontrib`_, `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `ocontrib`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `viserial`_, `vmonog`_
Attributes: none

----
part
----
Element
Identify the part of the volume/issue number
Contained in: `amonog`_, `imonog`_, `omonog`_, `pmonog`_, `viserial`_, `vmonog`_
Attributes: none

----
patent
------
Element
Identify the number of the patent
Contained in: `patgrp`_
Attributes: none

----
patgrp
------
Element
Group the elements of patent
Contained in: `acontrib`_, `amonog`_, `imonog`_, `ocontrib`_, `omonog`_, `vcontrib`_, `vmonog`_
Contains: `orgname`_, `patent`_, `date`_
Attributes: `country`_

----
pcitat
------
Element
Identify a bibliography reference
Contained in: `apa`_
Contains: `no`_, `pcontrib`_, `pmonog`_, `piserial`_
Attributes: none

----
pcontrib
--------
Element
Group the elements of contribution
Contained in: `pcitat`_
Contains: `author`_, `corpauth`_, `date`_, `title`_, `subtitle`_
Attributes: none

----
piserial
--------
Element
Group the elements of serial
Contained in: `pcitat`_
Contains: `sertitle`_, `volid`_, `issueno`_, `suppl`_, `pages`_, `url`_, `cited`_, `doi`_, `pubid`_
Attributes: none

----
pmonog
------
Element
Group the elements of monograph
Contained in: `pcitat`_
Contains: `author`_, `corpauth`_, `date`_, `title`_, `volid`_, `part`_, `subtitle`_, `confgrp`_, `thesis`_, `coltitle`_, `colvolid`_, `pages`_, `edition`_, `city`_, `state`_, `country`_, `pubname`_, `report`_, `url`_, `cited`_, `doi`_, `pubid`_, `notes`_
Attributes: none

----
previous
--------
Element
Identify the author is the same author of the previous reference
Contained in: `author`_, `corpauth`_, `oauthor`_, `ocorpaut`_
Attributes: none

----
projname
--------
Element
Identify the name of the project
Contained in: `report`_
Attributes: none

----
pubid
-----
Element
Identify an id of any external database, such as DOI, pmid (PubMed), pmcid (PMC), etc
Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `viserial`_, `vmonog`_
Attributes: `idtype`_

----
pubname
-------
Element
Identify the publisher
Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `pmonog`_, `product`_, `vmonog`_
Attributes: none

----
received
--------
Element
Identify the date in which the article was received by peer review system
Contained in: `hist`_
Attributes: `dateiso`_

----
related
-------
Element
Identify related documents
Contained in: `ifloat`_, `front`_
Attributes: `doctype`_, `link`_, `linktype`_

----
report
------
Element
Group the elements of funding
Contained in: `amonog`_, `bbibcom`_, `bibcom`_, `imonog`_, `omonog`_, `p`_, `pmonog`_, `vmonog`_
Contains: `no`_, `rsponsor`_, `awarded`_, `projname`_, `contract`_
Attributes: none

----
response
--------
Element
Group the elements of a response to an article
Contained in: `article`_, `subart`_
Contains: `front`_, `body`_, `back`_
Attributes: `id`_, `resptp`_, `language`_

----
revised
-------
Element
Identify the date in which the article was revised by peer review system
Contained in: `hist`_
Attributes: `dateiso`_

----
rsponsor
--------
Element
Identify the sponsor or funding institution
Contained in: `report`_
Contains: `orgname`_, `orgdiv`_
Attributes: none

----
sciname
-------
Element
Identify scientific names
Contained in: `ifloat`_
Attributes: none

----
sec
---
Element
Identify a section
Contained in: `app`_, `xmlabstr`_, `xmlbody`_
Contains: `sectitle`_, `subsec`_, `p`_
Attributes: `sec-type`_

----
sectitle
--------
Element
Identify a section title
Contained in: `sec`_, `subsec`_
Attributes: none

----
sertitle
--------
Element
Identify the journal title
Contained in: `aiserial`_, `iiserial`_, `oiserial`_, `piserial`_, `product`_
Attributes: none

----
sponsor
-------
Element
Identify the sponsor or funding institution
Contained in: `confgrp`_
Contains: `orgname`_, `orgdiv`_
Attributes: none

----
state
-----
Element
Identify the state/region
Contained in: `aff`_, `aiserial`_, `amonog`_, `confgrp`_, `iiserial`_, `imonog`_, `omonog`_, `pmonog`_, `product`_, `thesgrp`_, `thesis`_, `vmonog`_
Attributes: none

----
stitle
------
Element
Identify the short title of a journal
Contained in: `aiserial`_, `iiserial`_, `oiserial`_, `vstitle`_
Attributes: none

----
subart
------
Element
Identify the text which is related to the article
Contained in: `article`_
Contains: `front`_, `xmlbody`_, `body`_, `back`_, `response`_
Attributes: `id`_, `doctype`_, `language`_

----
subkey
------
Element
Identify the subkey of a key word
Contained in: `keygrp`_
Attributes: `rid`_

----
subresp
-------
Element
Identify the secondary responsabilities
Contained in: `amonog`_, `icontrib`_, `imonog`_
Contains: `fname`_, `surname`_
Attributes: `role`_

----
subsec
------
Element
Identify a sub-section
Contained in: `sec`_
Contains: `sectitle`_, `p`_
Attributes: none

----
subtitle
--------
Element
Identify the subtitle
Contained in: `acontrib`_, `amonog`_, `bbibcom`_, `icontrib`_, `imonog`_, `ocontrib`_, `omonog`_, `pcontrib`_, `pmonog`_, `titlegrp`_, `vtitle`_
Attributes: none

----
suppl
-----
Element
Identify the supplement
Contained in: `aiserial`_, `oiserial`_, `piserial`_, `viserial`_
Attributes: none

----
surname
-------
Element
Identify the last name
Contained in: `author`_, `awarded`_, `oauthor`_, `subresp`_
Attributes: none

----
tabwrap
-------
Element
Group the elements of a table
Contained in: `ifloat`_
Contains: `label`_, `caption`_, `graphic`_, `table`_, `fntable`_
Attributes: `id`_, `filename`_

----
term
----
Element
Identify a term
Contained in: `defitem`_
Attributes: none

----
texmath
-------
Element
Identify a formula using Tex Math Equation
Contained in: `equation`_
Attributes: none

----
text
----
Element
Identify a text
Contained in: `start`_
Contains: `doi`_, `titlegrp`_, `authgrp`_, `body`_, `back`_
Attributes: none

----
thesgrp
-------
Element
Group the elements of a thesis
Contained in: `bbibcom`_, `bibcom`_
Contains: `city`_, `state`_, `country`_, `date`_, `degree`_, `orgname`_, `orgdiv`_
Attributes: none

----
thesis
------
Element
Group the elements of a thesis
Contained in: `amonog`_, `omonog`_, `pmonog`_, `vmonog`_
Contains: `city`_, `state`_, `country`_, `date`_, `degree`_, `orgname`_, `orgdiv`_
Attributes: none

----
title
-----
Element
Identify the title of the document
Contained in: `ack`_, `acontrib`_, `amonog`_, `app`_, `bbibcom`_, `glossary`_, `deflist`_, `icontrib`_, `imonog`_, `ocontrib`_, `omonog`_, `pcontrib`_, `pmonog`_, `product`_, `titlegrp`_, `vtitle`_
Attributes: `language`_

----
titlegrp
--------
Element
Group the titles of the document
Contained in: `front`_, `text`_
Contains: `title`_, `subtitle`_
Attributes: none

----
toctitle
--------
Element
Identify the TOC section title. It is mandatory to the generation of XML files.
Contained in: `front`_
Attributes: none

----
tome
----
Element
Identify the tome of a publication
Contained in: `amonog`_
Attributes: none

----
tp
--
Element
Identify the type of publication
Contained in: `vstitle`_, `vtitle`_
Attributes: none

----
update
------
Element
Identify the information of update
Contained in: `iiserial`_, `imonog`_
Attributes: none

----
uri
---
Element
Identify an uri
Contained in: `ifloat`_
Attributes: none

----
url
---
Element
Identify the electronic address of the document
Contained in: `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `viserial`_, `vmonog`_
Attributes: none

----
vancouv
-------
Element
Group the elements of bibliography references which are according to Vancouver
Contained in: `back`_
Contains: `vcitat`_
Attributes: `standard`_, `count`_

----
vcitat
------
Element
Identify a bibliography reference
Contained in: `vancouv`_
Contains: `no`_, `vcontrib`_, `viserial`_, `vmonog`_
Attributes: none

----
vcontrib
--------
Element
Group the elements of contribution
Contained in: `vcitat`_
Contains: `author`_, `corpauth`_, `et-al`_, `vtitle`_, `patgrp`_
Attributes: none

----
version
-------
Element
Identify the version
Contained in: `vmonog`_
Attributes: none

----
viserial
--------
Element
Group the elements of serial
Contained in: `vcitat`_
Contains: `vstitle`_, `date`_, `inpress`_, `volid`_, `issueno`_, `suppl`_, `part`_, `extent`_, `pages`_, `url`_, `cited`_, `doi`_, `pubid`_
Attributes: none

----
vmonog
------
Element
Group the elements of monograph
Contained in: `vcitat`_
Contains: `author`_, `corpauth`_, `et-al`_, `vtitle`_, `edition`_, `volid`_, `part`_, `version`_, `confgrp`_, `city`_, `state`_, `country`_, `pubname`_, `inpress`_, `date`_, `pages`_, `extent`_, `report`_, `thesis`_, `url`_, `cited`_, `doi`_, `pubid`_, `patgrp`_, `coltitle`_
Attributes: none

----
volid
-----
Element
Identify the volume
Contained in: `acontrib`_, `aiserial`_, `amonog`_, `iiserial`_, `imonog`_, `oiserial`_, `omonog`_, `piserial`_, `pmonog`_, `viserial`_, `vmonog`_
Attributes: none

----
vstitle
-------
Element
Short title in Vancouver
Contained in: `viserial`_
Contains: `stitle`_, `tp`_
Attributes: none

----
vtitle
------
Element
Group the elements of title in Vancouver
Contained in: `vcontrib`_, `vmonog`_
Contains: `title`_, `subtitle`_, `tp`_
Attributes: none

----
xmlabstr
--------
Element
Identify the abstract with sections
Contained in: `bibcom`_
Contains: `sec`_, `p`_
Attributes: `language`_

----
xmlbody
-------
Element
Identify the body of the document, in details
Contained in: `article`_, `subart`_
Contains: `sec`_, `p`_, `deflist`_, `sigblock`_
Attributes: none

----
xref
----
Element
Identify a cross-reference
Contained in: `ifloat`_
Attributes: `ref-type`_, `rid`_

----
zipcode
-------
Element
Identify a ZIP Code
Contained in: `aff`_
Attributes: none

----
Attribute blcktype
------------------
Attribute
Identify the text block type
Is attribute of: `txtblock`_
+---+-----------+
|nd |undefined  |
+---+-----------+
|ack|Acknowledge|
+---+-----------+


----
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


----
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


----
Attribute count
---------------
Attribute
Identify the quantity
Is attribute of: `vancouv`_, `iso690`_, `abnt6023`_, `apa`_, `other`_
+-+-+
|0|0|
+-+-+


----
Attribute country
-----------------
Attribute
Identify the country
Is attribute of: `patgrp`_
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


----
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


----
Attribute cturl
---------------
Attribute
Identify the clinical trial database's URL
Is attribute of: `ctreg`_
+++
|||
+++


----
Attribute dateiso
-----------------
Attribute
Identify the date in format YYYYMMDD (YYYY = 4 digits for year, 2 digits for month, 2 digits for day)
Is attribute of: `date`_, `received`_, `accepted`_, `revised`_, `cited`_
+--------+--------+
|00000000|00000000|
+--------+--------+


----
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


----
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


----
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


----
Attribute doctype
-----------------
Attribute
Identify the type of the document
Is attribute of: `related`_, `subart`_
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


----
Attribute embdate
-----------------
Attribute
Identify the embargo date
Is attribute of: `deposit`_
+++
|||
+++


----
Attribute entrdate
------------------
Attribute
Identify the entrance date
Is attribute of: `deposit`_
+++
|||
+++


----
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


----
Attribute filename
------------------
Attribute
Identify the filename of a figure or table or equation
Is attribute of: `tabwrap`_, `figgrp`_, `equation`_
+++
|||
+++


----
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


----
Attribute from
--------------
Attribute
Identify the start date
Is attribute of: `dperiod`_
+--------+--------+
|00000000|00000000|
+--------+--------+


----
Attribute ftype
---------------
Attribute
Identify the type of the figure
Is attribute of: `figgrp`_
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


----
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


----
Attribute href
--------------
Attribute
Identify the href of a file
Is attribute of: `license`_, `graphic`_, `supplmat`_
+++
|||
+++


----
Attribute id
------------
Attribute
Identify an ID
Is attribute of: `aff`_, `keyword`_, `tabwrap`_, `figgrp`_, `figgrps`_, `equation`_, `fngrp`_, `fntable`_, `corresp`_, `response`_, `subart`_, `glossary`_, `deflist`_, `app`_
+--+-----------+
|nd|No definido|
+--+-----------+


----
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


----
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


----
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


----
Attribute language
------------------
Attribute
Identify the language
Is attribute of: `title`_, `abstract`_, `xmlabstr`_, `keyword`_, `license`_, `response`_, `subart`_
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


----
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


----
Attribute link
--------------
Attribute
Identify the relation between the documents
Is attribute of: `related`_
+++
|||
+++


----
Attribute linktype
------------------
Attribute
Identify the type of relation between documents
Is attribute of: `related`_
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


----
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


----
Attribute name
--------------
Attribute
Identify the name of the element or attribute
Is attribute of: `element`_, `attrib`_
+++
|||
+++


----
Attribute no
------------
Attribute
Identify the number
Is attribute of: 
+-+-+
|0|0|
+-+-+


----
Attribute orgdiv1
-----------------
Attribute
Identify the organization division 1
Is attribute of: `aff`_
+--+--+
|nd|nd|
+--+--+


----
Attribute orgdiv2
-----------------
Attribute
Identify the organization division 2
Is attribute of: `aff`_
+--+--+
|nd|nd|
+--+--+


----
Attribute orgdiv3
-----------------
Attribute
Identify the organization division 3
Is attribute of: `aff`_
+--+--+
|nd|nd|
+--+--+


----
Attribute orgname
-----------------
Attribute
Identify the organization name
Is attribute of: `aff`_
+--+--+
|nd|nd|
+--+--+


----
Attribute pages
---------------
Attribute
Identify the pagination
Is attribute of: 
+---+---+
|0-0|0-0|
+---+---+


----
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


----
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


----
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


----
Attribute resptp
----------------
Attribute
Identify the response type
Is attribute of: `response`_
+----------+----------+
|addendum  |addendum  |
+----------+----------+
|discussion|discussion|
+----------+----------+
|reply     |reply     |
+----------+----------+


----
Attribute rid
-------------
Attribute
Identify an reference to an ID 
Is attribute of: `author`_, `oauthor`_, `subkey`_, `xref`_
+--+-----------+
|nd|No definido|
+--+-----------+


----
Attribute role
--------------
Attribute
Identify the Role of the author
Is attribute of: `author`_, `oauthor`_, `subresp`_
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


----
Attribute scheme
----------------
Attribute
Identify the indicates the controlled vocabulary
Is attribute of: `keygrp`_
+----+--------------------------+
|nd  |No Descriptor             |
+----+--------------------------+
|decs|Health Science Descriptors|
+----+--------------------------+


----
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


----
Attribute specyear
------------------
Attribute
Identify the year as presented in the reference. E.g.: 2005, c1900 (about 1900), 1800a, etc.
Is attribute of: `date`_
+++
|||
+++


----
Attribute sponsor
-----------------
Attribute
Identify the funding institution
Is attribute of: 
+--+------------+
|nd|Not definido|
+--+------------+


----
Attribute standard
------------------
Attribute
Identify the standard adopted by the journal
Is attribute of: `vancouv`_, `iso690`_, `abnt6023`_, `apa`_, `other`_
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


----
Attribute to
------------
Attribute
Identify the due date
Is attribute of: `dperiod`_
+--------+--------+
|00000000|00000000|
+--------+--------+


----
Attribute toccode
-----------------
Attribute
Identify the indicates whether the title is the text title or section title
Is attribute of: 
+-+--------+
|1|title   |
+-+--------+
|2|sectitle|
+-+--------+


----
Attribute value
---------------
Attribute
Identify the value of the element or attribute
Is attribute of: `attrib`_
+++
|||
+++


----
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
