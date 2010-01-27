<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<!-- ============================================================= -->
	<!--  2. ROOT TEMPLATE - HANDLES HTML FRAMEWORK                    -->
	<!-- ============================================================= -->
	<!-- NO_USE ISSO SOBRE-ESCRITO por sci_arttext -->
	<xsl:template match="/">
		<xsl:call-template name="nl-1"/>
		<html>
			<!-- HTML header -->
			<xsl:call-template name="nl-2"/>
			<xsl:call-template name="make-html-header"/>
			<xsl:call-template name="nl-2"/>
			<body bgcolor="#f8f8f8">
				<xsl:apply-templates/>
			</body>
		</html>
	</xsl:template>	
	<!-- ============================================================= -->
	<!--  26. BREAK AND HORIZONTAL RULE                                -->
	<!-- ============================================================= -->
	<xsl:template match="break" name="make-break">
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="hr" name="make-rule">
		<xsl:call-template name="nl-1"/>
		<hr/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	
</xsl:transform>
