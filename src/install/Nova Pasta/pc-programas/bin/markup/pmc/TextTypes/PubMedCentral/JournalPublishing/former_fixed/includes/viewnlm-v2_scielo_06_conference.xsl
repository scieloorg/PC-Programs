<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  Conference                                                   -->
	<!-- ============================================================= -->
	<xsl:template match="conference">
		<span class="gen">
			<xsl:text>Conference: </xsl:text>
		</span>
		<xsl:call-template name="make-conference"/>
		<br/>
	</xsl:template>
	<!-- doesn't use conf-num, conf-sponsor, conf-theme -->
	<xsl:template name="make-conference">
		<xsl:apply-templates select="conf-acronym" mode="add-period"/>
		<xsl:apply-templates select="conf-name" mode="add-period"/>
		<xsl:apply-templates select="conf-loc" mode="add-period"/>
		<xsl:apply-templates select="conf-date" mode="add-period"/>
	</xsl:template>
	<xsl:template match="*" mode="add-period">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
</xsl:transform>
