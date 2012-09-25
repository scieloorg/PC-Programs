<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">

	<xsl:output encoding="utf-8" method="xml" indent="yes" doctype-public="-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" doctype-system="journalpublishing3.dtd"/>

	
	<xsl:template match="article"><xsl:copy-of select="."/></xsl:template>

</xsl:stylesheet>
