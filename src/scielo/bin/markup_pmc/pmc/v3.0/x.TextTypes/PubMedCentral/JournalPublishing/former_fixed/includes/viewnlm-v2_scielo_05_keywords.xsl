<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	
	<!-- ============================================================= -->
	<!--  Keywords                                                     -->
	<!-- ============================================================= -->
	<!-- kwd-group and its kwd occur only in article-meta -->
	<xsl:template match="kwd-group">
		<span class="gen">
			<xsl:call-template name="make-id"/>
			<xsl:text>Keywords: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
	</xsl:template>
	<xsl:template match="kwd">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</span>
		<xsl:call-template name="make-keyword-punct"/>
	</xsl:template>
	<xsl:template name="make-keyword-punct">
		<xsl:choose>
			<xsl:when test="following-sibling::kwd">
				<xsl:text>, </xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>.</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template></xsl:transform>
