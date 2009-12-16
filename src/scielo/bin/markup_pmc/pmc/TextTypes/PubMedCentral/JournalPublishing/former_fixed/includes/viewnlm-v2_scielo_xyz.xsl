<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  27. CHEM-STRUCT                                              -->
	<!-- ============================================================= -->
	<xsl:template match="chem-struct">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:call-template name="display-id"/>
			<xsl:choose>
				<xsl:when test="@xlink:href">
					<a>
						<xsl:call-template name="make-href"/>
						<xsl:apply-templates/>
					</a>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates/>
				</xsl:otherwise>
			</xsl:choose>
		</span>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  28. TEX-MATH and MML:MATH                                    -->
	<!-- ============================================================= -->
	<xsl:template match="tex-math">
		<span class="take-note">
			<xsl:text>[tex-math code here]</xsl:text>
		</span>
	</xsl:template>
	<!-- can presume this is meant to be inline -->
	<xsl:template match="inline-formula//mml:math">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="capture-id">
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</span>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- we don't -know- mml:math in general to be inline,
     so treat it as block.
     Put it in a table to get a pretty border. -->
	<xsl:template match="mml:math">
		<xsl:comment>viewnlm-v2.xsl</xsl:comment>
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<table border="1">
					<tr>
						<td valign="top">
							<a>
								<xsl:call-template name="make-href"/>
								<xsl:call-template name="make-id"/>
								<xsl:apply-templates/>
							</a>
						</td>
					</tr>
				</table>
			</xsl:when>
			<xsl:otherwise>
				<table border="1">
					<tr>
						<td valign="top">
							<span>
								<xsl:call-template name="make-id"/>
								<xsl:apply-templates/>
							</span>
						</td>
					</tr>
				</table>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  29. GRAPHIC and MEDIA                                        -->
	<!-- ============================================================= -->
	<xsl:template match="graphic">
		<img>
			<xsl:call-template name="make-src"/>
			<xsl:call-template name="make-id"/>
		</img>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="media">
		<a>
			<xsl:call-template name="make-href"/>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</a>
		<xsl:call-template name="nl-1"/>
	</xsl:template></xsl:transform>
