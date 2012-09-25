<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">

	<xsl:include href="local_dtd.xsl"/>
	
	<xsl:variable name="display_funding"><xsl:if test="not(//ack)">yes</xsl:if></xsl:variable>
	<xsl:template match="*">
		<xsl:element name="{name()}">
		<xsl:apply-templates select="@* | * | text()"/></xsl:element>
	</xsl:template>
	<xsl:template match="@*"><xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute></xsl:template>
	<xsl:template match="text()"><xsl:value-of select="."/></xsl:template>
	<xsl:template match="mixed-citation"/>
	<xsl:template match="aff/institution"/>
	<xsl:template match="funding-group"><xsl:if test="$display_funding='yes'"><xsl:element name="{name()}">
		<xsl:apply-templates select="@* | * | text()"/></xsl:element></xsl:if></xsl:template>

</xsl:stylesheet>
