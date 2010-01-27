<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  24. FORMATTING ELEMENTS                                      -->
	<!-- ============================================================= -->
	<xsl:template match="bold">
		<b>
			<xsl:apply-templates/>
		</b>
	</xsl:template>
	<xsl:template match="italic">
		<i>
			<xsl:apply-templates/>
		</i>
	</xsl:template>
	<xsl:template match="monospace">
		<span class="monospace">
			<xsl:apply-templates/>
		</span>
	</xsl:template>
	<xsl:template match="overline">
		<span class="overline">
			<xsl:apply-templates/>
		</span>
	</xsl:template>
	<xsl:template match="sc">
		<!-- handle any tags as usual, until
       we're down to the text strings -->
		<small>
			<xsl:apply-templates/>
		</small>
	</xsl:template>
	<xsl:template match="sc//text()">
		<xsl:param name="str" select="."/>
		<xsl:call-template name="capitalize">
			<xsl:with-param name="str" select="$str"/>
		</xsl:call-template>
	</xsl:template>
	<xsl:template match="strike">
		<s>
			<xsl:apply-templates/>
		</s>
	</xsl:template>
	<xsl:template match="sub">
		<sub>
			<xsl:apply-templates/>
		</sub>
	</xsl:template>
	<xsl:template match="sup">
		<sup>
			<xsl:apply-templates/>
		</sup>
	</xsl:template>
	<xsl:template match="underline">
		<u>
			<xsl:apply-templates/>
		</u>
	</xsl:template>
	

	
</xsl:transform>
