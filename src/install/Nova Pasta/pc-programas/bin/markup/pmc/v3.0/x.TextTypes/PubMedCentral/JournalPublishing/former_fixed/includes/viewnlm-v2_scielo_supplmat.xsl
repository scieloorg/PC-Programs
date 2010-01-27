<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  22. SUPPLEMENTARY MATERIAL                                   -->
	<!-- ============================================================= -->
	<xsl:template match="supplementary-material">
		<xsl:variable name="the-label">
			<xsl:choose>
				<xsl:when test="label">
					<xsl:value-of select="label"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>Supplementary Material</xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<span class="tl-default">
			<xsl:choose>
				<xsl:when test="@xlink:href">
					<a>
						<xsl:call-template name="make-href"/>
						<xsl:call-template name="make-id"/>
						<xsl:value-of select="$the-label"/>
					</a>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="make-id"/>
					<xsl:value-of select="$the-label"/>
				</xsl:otherwise>
			</xsl:choose>
		</span>
		<xsl:apply-templates select="*[not(self::label)]"/>
	</xsl:template>

	

	
</xsl:transform>
