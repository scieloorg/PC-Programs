<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  57. "CITATION-TAG-ENDS"                                      -->
	<!-- ============================================================= -->
	<xsl:template name="citation-tag-ends">
		<xsl:apply-templates select="series" mode="citation"/>
		<!-- If language is not English -->
		<!-- XX review logic -->
		<xsl:if test="article-title[@xml:lang!='en']
               or article-title[@xml:lang!='EN']">
			<xsl:call-template name="language">
				<xsl:with-param name="lang" select="article-title/@xml:lang"/>
			</xsl:call-template>
		</xsl:if>
		<xsl:if test="source[@xml:lang!='en']
              or source[@xml:lang!='EN']">
			<xsl:call-template name="language">
				<xsl:with-param name="lang" select="source/@xml:lang"/>
			</xsl:call-template>
		</xsl:if>
		<xsl:apply-templates select="comment" mode="citation"/>
		<xsl:apply-templates select="annotation" mode="citation"/>
	</xsl:template>
	</xsl:transform>
