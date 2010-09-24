<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"  xmlns:mml="http://www.w3.org/1998/Math/MathML">
	<xsl:variable name="vol" select="//article/volume"/>
	<xsl:variable name="page" select="//article/fpage"/>
	<xsl:template match="/">ACRON-<xsl:value-of select="$vol"	/>-<xsl:value-of select="$page"/>;
	<xsl:apply-templates select="//equation"/>
	<xsl:apply-templates select="//fig"/>
	<xsl:apply-templates select="//tab-wrap"/>	
	</xsl:template>
	<xsl:template match="*[graphic]"><xsl:value-of select="graphic/@xlink:href"/>|ACRON-<xsl:value-of select="$vol"	/>-<xsl:value-of select="$page"/>-g<xsl:value-of select="@id"/>;
	</xsl:template>
	<xsl:template match="equation[graphic]"><xsl:value-of select="graphic/@xlink:href"/>|ACRON-<xsl:value-of select="$vol"	/>-<xsl:value-of select="$page"/>-e<xsl:value-of select="@id"/>;
	</xsl:template>
</xsl:stylesheet>
