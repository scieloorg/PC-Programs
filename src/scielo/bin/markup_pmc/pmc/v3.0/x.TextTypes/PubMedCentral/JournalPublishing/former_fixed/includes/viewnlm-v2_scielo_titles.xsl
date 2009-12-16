<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">

	<!-- ============================================================= -->
	<!--  46. TITLES: MAIN ARTICLE DIVISIONS                           -->
	<!-- ========================================================== -->
	
	<!-- main or top-level divisions -->
	<xsl:template match="abstract/title | body/sec/title
                   | back/title | app-group/title | app/title
                   | glossary/title | def-list/title | ack/title
                   | ref-list/title | back/notes/title">
		<xsl:call-template name="nl-1"/>
		<span class="tl-main-part">
			<xsl:apply-templates/>
		</span>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  47. TITLES: FIRST-LEVEL DIVISIONS AND DEFAULT                -->
	<!-- ============================================================= -->
	<!-- first-level divisions and default -->
	<xsl:template match="body/sec/sec/title | ack/sec/title | app/sec/title
                   | boxed-text/title | gloss-group/title | notes/sec/title">
		<xsl:call-template name="nl-1"/>
		<span class="tl-lowest-section">
			<xsl:apply-templates/>
		</span>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- default: any other titles found -->
	<xsl:template match="title">
		<xsl:call-template name="nl-1"/>
		<span class="tl-default">
			<xsl:apply-templates/>
		</span>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	</xsl:transform>
