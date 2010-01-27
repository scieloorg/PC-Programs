<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mml="http://www.w3.org/1998/Math/MathML">
	<!--xsl:output method="xhtml" omit-xml-declaration="yes" indent="yes" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/-->
	
	<!-- 
		Variables
	-->
	<xsl:variable name="translations" select="//locale"/>

	<xsl:variable name="orientalLanguages" select="'ar'"/>
	<xsl:variable name="var_IMAGE_PATH">
		<xsl:choose>
			<xsl:when test="//PATH_SERIMG and //SIGLUM and //ISSUE">
				<xsl:value-of select="//PATH_SERIMG"/>
				<xsl:value-of select="//SIGLUM"/>/<xsl:if test="//ISSUE/@VOL">v<xsl:value-of select="//ISSUE/@VOL"/>
				</xsl:if>
				<xsl:if test="//ISSUE/@NUM">n<xsl:value-of select="//ISSUE/@NUM"/>
				</xsl:if>
				<xsl:if test="//ISSUE/@SUPPL">s<xsl:value-of select="//ISSUE/@SUPPL"/>
				</xsl:if>/</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="//image-path"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:variable name="var_IMAGES_INFO" select="//images-info"/>
	<xsl:variable name="css_path" select="//css-path"/>
	<xsl:variable name="languages" select="document('../../../../../xml/language.xml')"/>

	<!--
	
	-->
	<xsl:template match="*" mode="css">
		<link rel="stylesheet" type="text/css" href="{$css_path}/pmc/css/common.css"/>
		<link rel="stylesheet" type="text/css" href="{$css_path}/pmc/css/TextTypes/PubMedCentral/JournalPublishing/ViewNLM.css"/>
		<link rel="stylesheet" type="text/css" href="{$css_path}/pmc/css/TextTypes/PubMedCentral/JournalPublishing/ViewScielo.css"/>
	</xsl:template>
	
</xsl:stylesheet>
