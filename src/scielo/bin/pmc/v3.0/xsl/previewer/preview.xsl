<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
	<xsl:import href="../jpub/main/jpub3-html.xsl"/>
    <xsl:import href="../web/scielo-fulltext.xsl"/>
    
    <xsl:param name="css" select="'../web/xml.css'"/>
	<xsl:param name="path_img" select="'/'"/>
	<xsl:param name="img_format" select="'.jpg'"/>

    <xsl:variable name="xml_article_lang"><xsl:choose><xsl:when test="./article/@xml:lang"></xsl:when><xsl:otherwise>en</xsl:otherwise></xsl:choose></xsl:variable>
    <xsl:variable name="xml_display_objects"/>
    <xsl:variable name="PID"/>

    <xsl:output method="html" omit-xml-declaration="no"
    encoding="utf-8" indent="no"/>
  
    
	<xsl:template match="/">
		<html>
			<xsl:call-template name="make-html-header"/>
			<body>
				<xsl:apply-templates select="article"  mode="text-content"/>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
