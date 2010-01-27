<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">

	<!-- ============================================================= -->
	<!--  49. UNMODED DATA ELEMENTS: MISCELLANEOUS                     -->
	<!-- ============================================================= -->
	<!-- epage -->
	<xsl:template match="epage">
		<span class="gen">
			<xsl:text>Electronic Page: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
	</xsl:template>
	<!-- series -->
	<xsl:template match="series">
		<xsl:text> (</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>).</xsl:text>
	</xsl:template>
	<!-- comment -->
	<xsl:template match="comment">
		<xsl:if test="not(self::node()='.')">
			&#160;<xsl:text/>
			<xsl:apply-templates/>
			<xsl:text>. </xsl:text>
		</xsl:if>
	</xsl:template>
	<!-- annotation -->
	<xsl:template match="annotation">
		<br/>
		<xsl:text> [</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>]</xsl:text>
		<br/>
	</xsl:template>
	<!-- permissions -->
	<xsl:template match="permissions">
		<xsl:choose>
			<xsl:when test="copyright-statement">
				<xsl:apply-templates select="copyright-statement"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="copyright-year">
					<p>
						<span class="gen">
							<xsl:text>Copyright: </xsl:text>
						</span>
						<xsl:apply-templates select="copyright-year"/>
						<xsl:apply-templates select="copyright-holder"/>
					</p>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- copyright-statement whether or not part of permissions -->
	<xsl:template match="copyright-statement">
		<p>
			<xsl:apply-templates/>
		</p>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  50. UNMODED DATA ELEMENTS: PARTS OF A DATE                   -->
	<!-- ============================================================= -->
	<xsl:template match="day">
		<span class="gen">
			<xsl:text>Day: </xsl:text>
		</span>
		<xsl:apply-templates/>
		&#160;<xsl:text/>
	</xsl:template>
	<xsl:template match="month">
		<span class="gen">
			<xsl:text>Month: </xsl:text>
		</span>
		<xsl:apply-templates/>
		&#160;<xsl:text/>
	</xsl:template>
	<xsl:template match="season">
		<span class="gen">
			<xsl:text>Season: </xsl:text>
		</span>
		<xsl:apply-templates/>
		&#160;<xsl:text/>
	</xsl:template>
	<xsl:template match="year">
		<span class="gen">
			<xsl:text>Year: </xsl:text>
		</span>
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="stringdate">
		<span class="gen">
			<xsl:text>Stringdate: </xsl:text>
		</span>
		<xsl:apply-templates/>
	</xsl:template>
	</xsl:transform>
