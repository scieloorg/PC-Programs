<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">

    <xsl:import href="../jpub/main/jpub3-html.xsl"/>
    <xsl:param name="path_img" select="'/'"/>
    <xsl:param name="css" select="''"/>
    
    <xsl:template match="graphic | inline-graphic">
        <xsl:apply-templates/>
        <img alt="{$path_img}/{@xlink:href}.jpg">
            <xsl:for-each select="alt-text">
                <xsl:attribute name="alt">
                  <xsl:value-of select="normalize-space(.)"/>
                </xsl:attribute>
            </xsl:for-each>
            <xsl:call-template name="assign-src"/>
        </img>
  </xsl:template>
  	
</xsl:stylesheet>
	

