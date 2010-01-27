<!--
$Id: svg.xsl,v 1.1 2002/06/29 22:22:37 davidc Exp $

Copyright David Carlisle 2001, 2002.

Use and distribution of this code are permitted under the terms of the <a
href="http://www.w3.org/Consortium/Legal/copyright-software-19980720"
>W3C Software Notice and License</a>.
-->
<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  xmlns:svg="http://www.w3.org/2000/svg"
  xmlns:h="http://www.w3.org/1999/xhtml"
  xmlns="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="h"
>


<h:p>The main bulk of this stylesheet is an identity transformation so...</h:p>
<xsl:template match="*">
<xsl:copy>
<xsl:copy-of select="@*"/>
<xsl:apply-templates/>
</xsl:copy>
</xsl:template>



<h:p>XHTML elements are copied sans prefix (XHTML is default namespace
here, so these elements will still be in XHTML namespace</h:p>
<xsl:template match="h:*">
<xsl:element name="{local-name(.)}">
 <xsl:copy-of select="@*"/>
<xsl:apply-templates/>
</xsl:element>
</xsl:template>

<h:p>This just ensures the mathml prefix declaration isn't copied from
the source at this stage, so that the system will use the mml prefix
coming from this stylesheet</h:p>
<xsl:template match="h:html|html">
<html>
<xsl:copy-of select="@*[not(namespace-uri(.)='http://www.w3.org/2002/Math/preference')]"/>
<xsl:apply-templates/>
</html>
</xsl:template>


<xsl:template match="h:head|head">
<head>
<object id="mmlFactory" 
        classid="clsid:32F66A20-7614-11D4-BD11-00104BD3F987">
<xsl:text> </xsl:text>
</object>
<xsl:processing-instruction name="import">
 namespace="mml" implementation="#mmlFactory"
</xsl:processing-instruction>
<object id="AdobeSVG" 
        classid="clsid:78156a80-c6a1-4bbf-8e6a-3cd390eeb4e2">
<xsl:text> </xsl:text>
</object>
<xsl:processing-instruction name="import">
 namespace="svg" implementation="#AdobeSVG"
</xsl:processing-instruction>
<xsl:apply-templates/>
</head>
</xsl:template>



<h:p>Somewhat bizarrely in an otherwise namespace aware system,
Microsoft behaviours are defined to trigger off the
<h:em>prefix</h:em> not the <h:em>Namespace</h:em>. In the code above
we associated a MathML rendering behaviour (if one was found) with the
prefix <h:code>mml:</h:code> so here we ensure that this is the prefix
that actually gets used in the output.</h:p>
<xsl:template match="mml:*">
<xsl:element name="mml:{local-name(.)}">
 <xsl:copy-of select="@*"/>
<xsl:apply-templates/>
</xsl:element>
</xsl:template>


<xsl:template match="svg:*">
<xsl:element name="svg:{local-name(.)}">
 <xsl:copy-of select="@*"/>
<xsl:apply-templates/>
</xsl:element>
</xsl:template>


</xsl:stylesheet>
