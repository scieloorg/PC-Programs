<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:output method="text" encoding="iso-8859-1" />
	<xsl:variable name="journal_acron" select="//extra-scielo/journal-acron"/>
	<xsl:variable name="journal_issn" select="node()/@issn"/>
	<xsl:variable name="journal_vol" select="node()/@volid"/>
	<xsl:variable name="article_page">
		<xsl:choose>
			<xsl:when test="./@fpage='0'">
				<xsl:value-of select="node()/@order"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="node()/@fpage"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:variable name="PREFIXO" select="concat($journal_issn,'-',$journal_acron,'-',$journal_vol,'-',$article_page)"/>
	<xsl:variable name="prefix" select="concat($PREFIXO,'-')"/>
	
	<xsl:template match="/"><xsl:value-of select="$PREFIXO"/>|<xsl:text>
</xsl:text><xsl:apply-templates select=".//figgrp | .//tabwrap | .//equation"/>
	</xsl:template>
	
	<xsl:template match="figgrp | tabwrap | equation">
		<xsl:variable name="filename1">
			<xsl:choose>
				<xsl:when test="@filename">
					<xsl:value-of select="@filename"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select=".//graphic/@href"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="filename" select="substring-before($filename1,'.jpg')"/>
		<xsl:variable name="file">
			<xsl:choose>
				<xsl:when test="contains($filename,'\')">
					<xsl:value-of select="substring-before(substring-after($filename,'img\'),'.')"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$filename"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="standardname"><xsl:value-of select="$prefix"/>
		<xsl:choose>
			<xsl:when test="name()='equation'">e</xsl:when>
			<xsl:otherwise>g</xsl:otherwise>
		</xsl:choose><xsl:value-of select="@id"/></xsl:variable>
<xsl:value-of select="$file"/>|<xsl:value-of select="$standardname"/><xsl:text>
</xsl:text>		
	</xsl:template>
	
</xsl:stylesheet>
