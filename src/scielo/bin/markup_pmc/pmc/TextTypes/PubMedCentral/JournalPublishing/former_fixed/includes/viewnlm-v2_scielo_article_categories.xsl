<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  Article Categories                                           -->
	<!-- ============================================================= -->
	<xsl:template match="article-categories">
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="subj-group">
		<xsl:if test="not(parent::subj-group)">
			<span class="gen">
				<xsl:text>Article Categories:</xsl:text>
			</span>
		</xsl:if>
		<ul>
			<xsl:apply-templates/>
		</ul>
	</xsl:template>
	<xsl:template match="subject">
		<li>
			<xsl:apply-templates/>
		</li>
	</xsl:template>
	<!-- There may be many series-title elements; there
     may be one series-text (description) element. -->
	<xsl:template match="series-title">
		<xsl:if test="not(preceding-sibling::series-title)">
			<span class="gen">
				<xsl:text>Series: </xsl:text>
			</span>
		</xsl:if>
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
		<xsl:if test="not(following-sibling::*)">
			<br/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="series-text">
		<xsl:apply-templates/>
		<br/>
	</xsl:template>	</xsl:transform>
