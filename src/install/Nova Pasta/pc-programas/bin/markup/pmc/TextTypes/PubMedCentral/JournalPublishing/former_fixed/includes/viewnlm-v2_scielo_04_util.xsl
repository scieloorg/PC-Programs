<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<!-- ============================================================= -->
	<!-- 4. UTILITIES                                                  -->
	<!-- ============================================================= -->
	<!-- ============================================================= -->
	<!--  "capitalize" Capitalize a string                             -->
	<!-- ============================================================= -->
	<xsl:template name="capitalize">
		<xsl:param name="str"/>
		<xsl:value-of select="translate($str,
                          'abcdefghjiklmnopqrstuvwxyz',
                          'ABCDEFGHJIKLMNOPQRSTUVWXYZ')"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  "language"                                                   -->
	<!-- ============================================================= -->
	<xsl:template name="language">
		<xsl:param name="lang"/>
		<xsl:choose>
			<xsl:when test="$lang='fr' or $lang='FR'"> (Fre).</xsl:when>
			<xsl:when test="$lang='jp' or $lang='JP'"> (Jpn).</xsl:when>
			<xsl:when test="$lang='ru' or $lang='RU'"> (Rus).</xsl:when>
			<xsl:when test="$lang='de' or $lang='DE'"> (Ger).</xsl:when>
			<xsl:when test="$lang='se' or $lang='SE'"> (Swe).</xsl:when>
			<xsl:when test="$lang='it' or $lang='IT'"> (Ita).</xsl:when>
			<xsl:when test="$lang='he' or $lang='HE'"> (Heb).</xsl:when>
			<xsl:when test="$lang='sp' or $lang='SP'"> (Spa).</xsl:when>
		</xsl:choose>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  "cleantitle"                                                 -->
	<!-- ============================================================= -->
	<xsl:template name="cleantitle">
		<xsl:param name="str"/>
		<xsl:value-of select="translate($str,'. ,-_','')"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  "newlines"                                                   -->
	<!-- ============================================================= -->
	<!-- produces newlines in output, to increase legibility of XML    -->
	<xsl:template name="nl-1">
		<xsl:text>&#xA;</xsl:text>
	</xsl:template>
	<xsl:template name="nl-2">
		<xsl:text>&#xA;</xsl:text>
		<xsl:text>&#xA;</xsl:text>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  make-id, make-src, make-href, make-email                     -->
	<!-- ============================================================= -->
	<xsl:template name="make-id">
		<xsl:if test="@id">
			<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template name="make-src">
		<xsl:if test="@xlink:href">
			<xsl:attribute name="src"><!--xsl:value-of select="@xlink:href"/--><xsl:apply-templates select="@xlink:href"/></xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template name="make-href">
		<xsl:if test="@xlink:href">
			<!-- FIXED trocou src por href -->
			<xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template name="make-email">
		<xsl:if test="@xlink:href">
			<xsl:attribute name="href"><xsl:value-of select="concat('mailto:', @xlink:href)"/></xsl:attribute>
		</xsl:if>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  display-id                                                   -->
	<!-- ============================================================= -->
	<xsl:template name="display-id">
		<xsl:variable name="display-phrase">
			<xsl:choose>
				<xsl:when test="self::disp-formula">
					<xsl:text>Formula ID</xsl:text>
				</xsl:when>
				<xsl:when test="self::chem-struct-wrapper">
					<xsl:text>Chemical Structure Wrapper ID</xsl:text>
				</xsl:when>
				<xsl:when test="self::chem-struct">
					<xsl:text>Chemical Structure ID</xsl:text>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>ID</xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="@id">
			<span class="gen">
				<xsl:text>[</xsl:text>
				<xsl:value-of select="$display-phrase"/>
				<xsl:text>: </xsl:text>
			</span>
			<xsl:value-of select="@id"/>
			<span class="gen">
				<xsl:text>]</xsl:text>
			</span>
		</xsl:if>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  "table-setup": left column wide or narrow                    -->
	<!-- ============================================================= -->
	<xsl:template name="table-setup-l-wide">
		<xsl:call-template name="nl-1"/>
		<tr>
			<td width="30%"/>
			<td/>
		</tr>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template name="table-setup-l-narrow">
		<xsl:call-template name="nl-1"/>
		<tr>
			<td width="10%"/>
			<td/>
		</tr>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template name="table-setup-even">
		<xsl:call-template name="nl-1"/>
		<tr>
			<td width="50%"/>
			<td/>
		</tr>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!-- "make-figs-and-tables"                                        -->
	<!-- ============================================================= -->
	<!-- initial context node is article -->
	<xsl:template name="make-figs-and-tables">
		<xsl:if test="body//fig[not(parent::fig-group)] | back//fig[not(parent::fig-group)]">
			<hr class="section-rule"/>
			<xsl:call-template name="nl-1"/>
			<span class="tl-main-part">Figures</span>
			<xsl:call-template name="nl-1"/>
			<table width="100%" class="bm">
				<xsl:call-template name="table-setup-l-wide"/>
				<!-- each figure is a row -->
				<xsl:apply-templates select="body//fig | back//fig" mode="put-at-end"/>
			</table>
		</xsl:if>
		<xsl:if test="body//table-wrap | back//table-wrap">
			<hr class="section-rule"/>
			<xsl:call-template name="nl-1"/>
			<span class="tl-main-part">Tables</span>
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates select="body//table-wrap | back//table-wrap" mode="put-at-end"/>
			<xsl:call-template name="nl-1"/>
		</xsl:if>
	</xsl:template>

</xsl:transform>
