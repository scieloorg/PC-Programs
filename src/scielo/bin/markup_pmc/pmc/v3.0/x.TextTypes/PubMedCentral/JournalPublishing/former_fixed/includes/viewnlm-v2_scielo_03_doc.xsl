<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  3. DOCUMENT ELEMENT                                          -->
	<!-- ============================================================= -->
	<!-- Can add sub-article and response to this match:
      - "make-a-piece" as required;
      - adapt the selection of elements that get managed as a set:
        footnotes, cross-references, tables, and figures. -->
	<xsl:template match="article">	
		<xsl:call-template name="make-a-piece"/>
	</xsl:template>
</xsl:transform>
