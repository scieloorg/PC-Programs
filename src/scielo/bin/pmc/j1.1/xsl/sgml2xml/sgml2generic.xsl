<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"
	xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:import href="../../../j1.0/xsl/sgml2xml/sgml2generic.xsl"/>
    <xsl:template match="article|text|doc" mode="dtd-version">
        <xsl:attribute name="dtd-version">1.1</xsl:attribute>
    </xsl:template>
    
    <xsl:template match="aff/@city | aff/city | normaff/city ">
        <city>
            <xsl:value-of select="normalize-space(.)"/>
        </city>
    </xsl:template>

    <xsl:template match="aff/@state | aff/state | normaff/state ">
        <state>
            <xsl:value-of select="normalize-space(.)"/>
        </state>
    </xsl:template>

    <xsl:template match="aff/@zipcode | aff/zipcode | normaff/zipcode ">
        <postal-code>
            <xsl:value-of select="normalize-space(.)"/>
        </postal-code>
    </xsl:template>

    <xsl:template match="version">
        <version>
            <xsl:value-of select="normalize-space(.)"/>
        </version>
    </xsl:template>
    
    <xsl:template match="code/@itstype">
        <xsl:attribute name="code-type">
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="onbehalf[institid]">
        <institution-wrap>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </institution-wrap>
    </xsl:template>
    
    <xsl:template match="institid/@itstype">
        <xsl:attribute name="institution-id-type">
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="institid">
        <xsl:element name="institution-id">
            <xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
