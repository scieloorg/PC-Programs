<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  25. SEMANTIC ELEMENTS                                        -->
	<!-- ============================================================= -->
	<xsl:template match="abbrev">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="capture-id">
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</span>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="inline-graphic">
		<xsl:call-template name="nl-1"/>
		<img>
			<xsl:call-template name="make-src"/>
			<xsl:call-template name="make-id"/>
		</img>
	</xsl:template>
	<xsl:template match="inline-formula">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</span>
	</xsl:template>
	<!-- is meant be a link: we assume the xlink:href
     attribute is used, although it is not
     required by the DTD. -->
	<xsl:template match="inline-supplementary-material">
		<xsl:call-template name="nl-1"/>
		<a>
			<xsl:call-template name="make-href"/>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</a>
	</xsl:template>
	<xsl:template match="glyph-data">
		<xsl:call-template name="nl-1"/>
		<span class="take-note">
			<xsl:call-template name="make-id"/>
			<xsl:text>[glyph data here: ID=</xsl:text>
			<xsl:value-of select="@id"/>
			<xsl:text>]</xsl:text>
		</span>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  Named Content                                                -->
	<!-- ============================================================= -->
	<xsl:template match="named-content">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="capture-id">
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</span>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:transform>
