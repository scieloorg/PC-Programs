<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="aff" mode="format">
		<xsl:apply-templates select="." mode="aff-outside-contrib"/>
		<xsl:apply-templates select="." mode="check"/>
	</xsl:template>
	<xsl:template match="aff" mode="check">
		<xsl:if test="not(addr-line) or not(institution) or not(country)">
			<p class="warning">
				<xsl:value-of select="$translations//message[@key='TextViewer.text.page.warning.missing']"/>
				<xsl:if test="not(addr-line)">&#160;addr-line</xsl:if>
				<xsl:if test="not(institution)">&#160;institution</xsl:if>
				<xsl:if test="not(country)">&#160;country</xsl:if>
			</p>
		</xsl:if>
		<xsl:apply-templates select="." mode="check-unmarked-text"/>
	</xsl:template>
	<xsl:template match="text()" mode="show-xml">
		<xsl:choose>
			<xsl:when test="../aff">
				<span class="destaque">
					<xsl:value-of select="."/>
				</span>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:transform>
