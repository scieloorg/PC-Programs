<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"  xmlns:mml="http://www.w3.org/1998/Math/MathML">
	<!--xsl:output method="xhtml" omit-xml-declaration="yes" indent="yes" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/-->
		<!-- <xsl:output method="xml" encoding="utf-8"/>

		Variables
	-->
	<xsl:variable name="orientalLanguages" select="'ar'"/>
	<!--xsl:variable name="layout" select="'ar'"/-->
	
	<xsl:variable name="var_IMAGE_PATH">
		<xsl:choose>
			<xsl:when test="//PATH_SERIMG and //SIGLUM and //ISSUE">
				<xsl:value-of select="//PATH_SERIMG"/>
				<xsl:value-of select="//SIGLUM"/>/<xsl:if test="//ISSUE/@VOL">v<xsl:value-of select="//ISSUE/@VOL"/>
				</xsl:if>
				<xsl:if test="//ISSUE/@NUM='AHEAD' or //ISSUE/@NUM='ahead'"><xsl:value-of select="substring(//ISSUE/@PUBDATE,1,4)"/></xsl:if>
				<xsl:if test="//ISSUE/@NUM">n<xsl:choose>
					<xsl:when test="//ISSUE/@NUM='AHEAD'">ahead</xsl:when>
					<xsl:otherwise><xsl:value-of select="//ISSUE/@NUM"/></xsl:otherwise>
				</xsl:choose>
				</xsl:if>
				<xsl:if test="//ISSUE/@SUPPL">s<xsl:value-of select="//ISSUE/@SUPPL"/>
				</xsl:if>/</xsl:when>
			<xsl:otherwise>./../img/</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:variable name="var_IMAGES_INFO" select="//images-info"/>
	<xsl:variable name="languages" select="document('../xml/en/language.xml')"/>
	<xsl:variable name="person-strings" select="document('viewnlm-v2_scielo.xsl')//util:map[@id='person-strings']/item"/>
      	<!--xsl:variable name="css_path" select="//css-path"/-->
      	<xsl:variable name="css_path"><xsl:choose>
								<xsl:when test="//css-path"><xsl:value-of select="//css-path"/></xsl:when>
								<xsl:when test="//ISSUE">/css/pmc</xsl:when>
								<xsl:otherwise><xsl:value-of select="document('../xml/css_path.xml')//css-path"/></xsl:otherwise>
							</xsl:choose></xsl:variable>
	
        <!--xsl:include href="viewnlm-v2_scielo.xsl"/-->
        
        <xsl:template name="nl-1"></xsl:template>
        <xsl:template name="nl-2"></xsl:template>

        <xsl:template name="make-id"></xsl:template>

	<xsl:include href="scielo_pmc.xsl"/>
	<xsl:include href="scielo_pmc_front.xsl"/>
	<xsl:include href="scielo_pmc_body.xsl"/>
	<xsl:include href="scielo_pmc_back.xsl"/>
	<xsl:include href="scielo_pmc_references.xsl"/>
	<xsl:include href="scielo_pmc_table.xsl"/>
	<xsl:include href="scielo_pmc_graphic.xsl"/>
	
	
	<!--xsl:include href="viewnlm-v2_scielo.xsl"/>
	<xsl:include href="scielo_pmc_common.xsl"/>
	<xsl:include href="scielo_pmc_front.xsl"/>	
	<xsl:include href="scielo_pmc_table.xsl"/>
	<xsl:include href="scielo_pmc_fig.xsl"/>
	<xsl:include href="scielo_pmc_body.xsl"/>	
	<xsl:include href="scielo_pmc_references.xsl"/>
	<xsl:include href="scielo_pmc_back.xsl"/-->
	<!--
	
	-->
	<xsl:template match="*" mode="css">
		<link rel="stylesheet" type="text/css" href="{$css_path}/ViewNLM.css"/>
		<link rel="stylesheet" type="text/css" href="{$css_path}/ViewScielo.css"/>
	</xsl:template>
	<!--
	
	-->
	<xsl:template match="article | ARTICLE[fulltext]">
	
		<xsl:apply-templates select="." mode="make-a-piece"/>
	</xsl:template>
</xsl:stylesheet>
