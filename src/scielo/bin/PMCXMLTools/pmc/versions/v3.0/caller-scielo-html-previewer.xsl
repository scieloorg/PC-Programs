<?xml version="1.0"?>
<!DOCTYPE xsl:stylesheet  [
  <!ENTITY nbsp   "&#160;">
  <!ENTITY copy   "&#169;">
  <!ENTITY reg    "&#174;">
  <!ENTITY trade  "&#8482;">
  <!ENTITY mdash  "&#8212;">
  <!ENTITY ldquo  "&#8220;">
  <!ENTITY rdquo  "&#8221;"> 
  <!ENTITY pound  "&#163;">
  <!ENTITY yen    "&#165;">
  <!ENTITY euro   "&#8364;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:saxon="http://saxon.sf.net/"
  version="2.0"
  extension-element-prefixes="saxon">

  <xsl:output method="html" omit-xml-declaration="yes"
    encoding="utf-8" indent="no"/>

  <!-- <xsl:output method="xml" omit-xml-declaration="no"
    encoding="utf-8" indent="no"/> -->
  
  <xsl:variable name="processes">
    <!-- format citations in NLM/PMC format -->
    <step>jpub/citations-prep/jpub3-PMCcit.xsl</step>
    <!-- convert into HTML for display -->
    <step>scielo-html-previewer.xsl</step>
  </xsl:variable>

  <xsl:include href="shell-utility.xsl"/>
  

</xsl:stylesheet>