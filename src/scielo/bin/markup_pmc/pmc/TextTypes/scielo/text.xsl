<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mml="http://www.w3.org/1998/Math/MathML">
	<!--xsl:output method="xhtml" omit-xml-declaration="yes" indent="yes" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/-->
	
	
	<xsl:include href="../former_fixed/viewnlm-v2_scielo.xsl"/>
	
	<xsl:include href="config/scielo_pmc_config.xsl"/>
	
	<xsl:include href="custom/text_front.xsl"/>
	
	<xsl:include href="generic/scielo_pmc_table.xsl"/>
	<xsl:include href="generic/scielo_pmc_fig.xsl"/>
	<xsl:include href="generic/scielo_pmc_references.xsl"/>
	<xsl:include href="generic/scielo_pmc.xsl"/>
	
	<xsl:include href="check/show-xml.xsl"/>
	<xsl:include href="check/check_xmllang.xsl"/>
	<xsl:include href="check/check_aff.xsl"/>
	<xsl:include href="check/check_references.xsl"/>
	
	<xsl:template match="article">
		<xsl:apply-templates select="." mode="make-a-piece"/>
	</xsl:template>
	
</xsl:stylesheet>
