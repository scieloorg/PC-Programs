<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  23. DISPLAY FORMULA, CHEM-STRUCT-WRAPPER                     -->
	<!-- ============================================================= -->
	<!-- both are grouping elements to keep parts together -->
	<xsl:template match="disp-formula | chem-struct-wrapper">
		<div class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:call-template name="display-id"/>
			<br/>
			<xsl:apply-templates/>
		</div>
	</xsl:template>

	

	
</xsl:transform>
