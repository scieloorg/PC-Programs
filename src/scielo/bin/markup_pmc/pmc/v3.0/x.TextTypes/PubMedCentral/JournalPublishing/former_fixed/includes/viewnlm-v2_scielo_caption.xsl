<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">

	<!-- ============================================================= -->
	<!--  31. CAPTIONING                                               -->
	<!-- ============================================================= -->
	<!-- the chooses before and after the element content
     tweak the display as appropriate -->
	<xsl:template match="label | alt-text | attrib | copyright-statement">
		<!-- element-specific handling before content: -->
		<xsl:choose>
			<!-- alt-text gets a generated label-->
			<xsl:when test="self::alt-text">
				<xsl:if test="not(ancestor::fig)
                  and not(ancestor::table)">
					<br/>
				</xsl:if>
				<span class="gen">
					<xsl:call-template name="make-id"/>
					<xsl:text>Alternate Text: </xsl:text>
				</span>
			</xsl:when>
			<!-- attrib is preceded by spaces plus em-dash -->
			<xsl:when test="self::attrib">
				<xsl:text>&#8194;&#8194;&#8212;</xsl:text>
			</xsl:when>
		</xsl:choose>
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
		<!-- element-specific handling after content: -->
		<xsl:choose>
			<!-- alt-text and long-desc get a break after -->
			<xsl:when test="self::alt-text | self::long-desc">
				<br/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="caption">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</span>
		<br/>
	</xsl:template>
	<!-- mixed-content; used in figures, tables, etc. -->
	<xsl:template match="long-desc">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</span>
		<br/>
	</xsl:template>
	<xsl:template match="object-id">
		<xsl:choose>
			<xsl:when test="@pub-id-type">
				<xsl:value-of select="@pub-id-type"/>
			</xsl:when>
			<xsl:otherwise>
				<span class="gen">
					<xsl:text>Object ID</xsl:text>
				</span>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:text>: </xsl:text>
		
		<xsl:text>. </xsl:text>
		<br/>
	</xsl:template>
	
</xsl:transform>
