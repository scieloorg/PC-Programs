
Issue database
--------------

ISIS Base. One record per issue. Each record contains the following tags:

===  =  ========================================================================================
---  -  ----------------------------------------------------------------------------------------
030      Short Title. Corresponds to 150 of TITLE
031      Volume
032      Number
033      Title of the issue
034      Party
035      ISSN. Corresponds to the field of 400 TITLE
036      Seq Num
041      Complement. Identify a press release number||
042      Status
043      Legend
043  v   volume
043  w   Supplement volume
043  n   number
043  s   Supplement number
043  y   Year
043  c   City
043  m   Month
048  l   Language header summary
048  h   Header Summary (Table of contents, summary, etc.)
049  c   Code sections
049  l   Language Sections
049  t   Title of the sections
062      Editor of the issue
064      Date of publication.   for the year (four digits),   m month (two digits)
065      Date ISO
085      Controlled Vocabulary
091      Date ISO to register the update date||
097      Cover
117      Standard (vancouver, ISO, ABNT, etc.)
122      Number of documents
130      Title of the journal. Corresponds to the field of 100 of TITLE database||
131      SuplVol
132      SuplNum
140      Sponsor
200      Markup done
230      corresponds to the same field of TITLE database
540      Text provided by the Creative Commons site in accordance with the choice of license
700      position of the record on the basis of an issue. Value equal to 0, first record
701      Counter record type. Value of 1
706      type / name of the record. Value of i (of issue)
930      Journal's acronym  in uppercase
935      ISSN of the journal at the time the issue had been published. Corresponds to the field of 935 TITLE
===  =  ========================================================================================



Section database
----------------

ISIS Base. A record by title. Each record contains the following tags:

================  =====================================================================================================
tag
----------------  -----------------------------------------------------------------------------------------------------
035               ISSN. Corresponds to the field of 400 of TITLE
048  subfield l   Language of table of contents' header 
048  subfield h   title for table of contents' header  (Table of contents (en), Sumario (pt), Tabla de Contenido (es))
049  subfield c   code of the section
049  subfield l   language of the section
049  subfield t   title of the section
091               Date ISO to register the update date
100               Journal's title. Corresponds to the same field of TITLE.
930               Journal's acronym in uppercase
================  =====================================================================================================
