<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="table-wrap">
		<a name="{@id}"/>
		<div class="capture-id">
			<xsl:call-template name="make-id"/>
			<!--xsl:apply-templates select="@id"/-->
			<xsl:apply-templates/>
			<br/>
		</div>
	</xsl:template>
<xsl:template match="tfoot | table-wrap-foot">
		<div class="foot">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</div>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
</xsl:transform>
