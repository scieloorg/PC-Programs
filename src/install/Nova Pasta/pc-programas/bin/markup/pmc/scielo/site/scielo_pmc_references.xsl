<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="pid" select="//ARTICLE/@PID"/>
	
	<xsl:template match="ref-list">
			<span class="tl-main-part">
				<xsl:choose>
					<xsl:when test="title">
						<xsl:value-of select="title"/>
					</xsl:when>
					<xsl:otherwise>
			References			
			</xsl:otherwise>
				</xsl:choose>
			</span>
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates select="ref"/>
			<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="ref">
		<p id="{@id}">
			<span id="x{@id}">
			<xsl:apply-templates select="label"/>
			<xsl:apply-templates select="citation|nlm-citation"/>
			</span>
			<!--xsl:apply-templates select="citation/pub-id|nlm-citation/pub-id" mode="link"/-->
			<xsl:apply-templates select="citation|nlm-citation" mode="link">
				<xsl:with-param name="pos" select="position()"/>
				<xsl:with-param name="pub-id" select=".//pub-id"/>
			</xsl:apply-templates>
			<xsl:call-template name="nl-1"/>
		</p>
	</xsl:template>
	<xsl:template match="ref//label">
		<b>
			<i>
				<xsl:apply-templates/>
				<xsl:text>. </xsl:text>
			</i>
		</b>
	</xsl:template>
	<xsl:template match="ref//label | ref//ext-link" mode="nscitation">
		<xsl:apply-templates select="."/>
	</xsl:template>
	<xsl:template match="ref//label | ref//ext-link" mode="none">
		<xsl:apply-templates select="."/>
	</xsl:template>
	<xsl:template match="citation|nlm-citation" mode="link">
		<xsl:param name="pos"/>
		<xsl:param name="pub-id"/>
		<xsl:variable name="position" select="concat(substring('00000',1,5 - string-length($pos)),$pos)"/>
		&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;[&#32;<a>
			<xsl:attribute name="href">javascript:void(0);</xsl:attribute>
			<xsl:attribute name="onclick">javascript: window.open('/scieloOrg/php/reflinks.php?refpid=<xsl:value-of select="$pid"/><xsl:value-of select="$position"/>&amp;pid=<xsl:value-of select="$pid"/>&amp;lng=<xsl:value-of select="$LANGUAGE"/>&amp;script=sci_reflinks&amp;refid=<xsl:value-of select="../@id"/><xsl:apply-templates select="$pub-id" mode="param"/>','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');</xsl:attribute>

			
			<!--xsl:attribute name="onclick">javascript: window.open('/scielo.php?pid=<xsl:value-of select="$pid"/><xsl:value-of select="$position"/>&amp;lng=<xsl:value-of select="$LANGUAGE"/>&amp;script=sci_reflinks<xsl:apply-templates select="$pub-id" mode="param"/>','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');</xsl:attribute-->
		Links</a>&#160;]
	</xsl:template>
	<xsl:template match="pub-id" mode="param">&amp;<xsl:value-of select="@pub-id-type"/>=<xsl:value-of select="."/>
		<xsl:if test="@pub-id-type='pmid'">&amp;medline_db=MEDLINE_<xsl:choose>
				<xsl:when test="..//year &lt; 1997">1966-1996</xsl:when>
				<xsl:when test="..//year &gt;= 1997">1997-2007</xsl:when>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	<xsl:template match="pub-id" mode="none"/>
	<xsl:template match="pub-id" mode="nscitation"/>
	<xsl:template match="pub-id" mode="link">
		<xsl:if test="position()=1">
			<br/>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</xsl:if>
		[&#160;<xsl:apply-templates select="." mode="link-value"/>&#160;]&#160;
	</xsl:template>
	<xsl:template match="pub-id[@pub-id-type='pmid']" mode="link-value">
		<a target="_blank">
			<xsl:attribute name="href"><xsl:apply-templates select="../../node()" mode="medline-link-src"/></xsl:attribute>Medline</a>
	</xsl:template>
	<xsl:template match="pub-id[@pub-id-type='doi']" mode="link-value">
		<a href="http://dx.doi.org/{.}" target="_blank">CrossRef</a>
	</xsl:template>
	<xsl:template match="lpage" mode="none"/>
	<xsl:template match="*[.//pub-id]" mode="medline-link-src">
		<xsl:variable name="year-range">
			<xsl:choose>
				<xsl:when test=".//year &lt; 1997">1966-1996</xsl:when>
				<xsl:when test=".//year &gt;= 1997">1997-2007</xsl:when>
			</xsl:choose>
		</xsl:variable>http://bases.bireme.br/cgi-bin/wxislind.exe/iah/online/?IsisScript=iah/iah.xis&amp;nextAction=lnk&amp;base=MEDLINE_<xsl:value-of select="$year-range"/>&amp;exprSearch=<xsl:value-of select=".//pub-id[@pub-id-type='pmid']"/>&amp;indexSearch=UI&amp;lang=i</xsl:template>
	<xsl:include href="scielo_pmc_references_gmb.xsl"/>
	<xsl:template match="lpage[not(../fpage) and (../../*[@citation-type='book' or @citaton-type='thesis'])] | *[@citation-type]/page-count" mode="none">
		<xsl:apply-templates select="@*|*|text()"/> pp.
	</xsl:template>
	<xsl:template match="source" mode="none"><xsl:apply-templates/><xsl:if test="../..//@citation-type!='journal'"><xsl:apply-templates select="." mode="dot"/></xsl:if>&#160;</xsl:template>
	
	<xsl:template match="*" mode="dot"><xsl:variable name="x" select="normalize-space(.)"/><xsl:if test="not(contains('?.!',substring($x,string-length($x),1)))">.</xsl:if></xsl:template>
</xsl:transform>
