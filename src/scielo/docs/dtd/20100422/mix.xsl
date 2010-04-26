<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" >
	<xsl:template match="/">
		<xsl:apply-templates/>
	</xsl:template>
	
	<xsl:template match="*">
	<xsl:copy>
		<xsl:apply-templates select="@*|*|text()"/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="xs:element[@name]">
		<xsl:variable name="name" select="@name"/>
		<xsl:copy>
			<xsl:apply-templates select="@name"/>
			<xs:annotation><xs:documentation>
			<xsl:value-of select="document('annotationFromMarkup.xml')//element[@name=$name]/annotation"/></xs:documentation></xs:annotation>
			<xsl:apply-templates select="*|text()"/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
</xsl:stylesheet>
