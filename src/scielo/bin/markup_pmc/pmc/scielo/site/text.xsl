<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML">
	<!--xsl:output method="xhtml" omit-xml-declaration="yes" indent="yes" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/-->
	<xsl:output method="xml"/>

	<xsl:variable name="LANGUAGE" select="'en'"/>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="*">
		<xsl:copy-of select="."/>
	</xsl:template>

	<xsl:include href="./../../common/page.xsl"/>
	<!--xsl:include href="configuration/text_config.xsl"/-->

	<xsl:include href="scielo_pmc_main.xsl"/>

	<xsl:template match="*" mode="content">
		<xsl:apply-templates select="//article"/>
	</xsl:template>
</xsl:stylesheet>
