<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  32. FIGURE, MODE PUT-AT-END                                  -->
	<!-- ============================================================= -->
	<!-- each figure is a row -->
	<xsl:template match="fig" mode="put-at-end">
		<!-- left column:  graphic
         right column: captioning elements - label, caption, etc. -->
		<tr>
			<xsl:call-template name="nl-1"/>
			<td valign="top">
				<xsl:apply-templates select="graphic"/>
				<br/>
				<span class="gen">
					<xsl:call-template name="make-id"/>
					<xsl:text>[Figure ID: </xsl:text>
				</span>
				<xsl:value-of select="@id"/>
				<span class="gen">
					<xsl:text>] </xsl:text>
				</span>
			</td>
			<xsl:call-template name="nl-1"/>
			<td valign="top">
				<xsl:apply-templates select="child::*[not(self::graphic)]"/>
			</td>
			<xsl:call-template name="nl-1"/>
		</tr>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	</xsl:transform>
