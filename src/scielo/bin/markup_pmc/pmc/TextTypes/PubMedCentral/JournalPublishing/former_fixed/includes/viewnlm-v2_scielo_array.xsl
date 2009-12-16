<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
		<!-- ============================================================= -->
	<!--  30. ARRAY                                                    -->
	<!-- ============================================================= -->
	<xsl:template match="array">
		<hr width="40%" align="left" noshade="1"/>
		<xsl:call-template name="nl-1"/>
		<table>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
			<xsl:call-template name="nl-1"/>
		</table>
		<xsl:call-template name="nl-1"/>
		<hr width="40%" align="left" noshade="1"/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	
</xsl:transform>
