<?xml version="1.0" encoding="utf-8"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" xmlns:ie5="http://www.w3.org/TR/WD-xsl" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:fns="http://www.w3.org/2002/Math/preference" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:pref="http://www.w3.org/2002/Math/preference" pref:renderer="mathplayer" exclude-result-prefixes="util xsl">
	<xsl:variable name="mainLanguage" select="//article/@xml:lang"/>
	<xsl:variable name="all_id" select="//*[@id]"/>
	
	<xsl:variable name="var_SUPPLMAT_PATH">
		<xsl:choose>
			<xsl:when test="//SIGLUM and //ISSUE">/pdf/<xsl:value-of select="//SIGLUM"/>/<xsl:if test="//ISSUE/@VOL">v<xsl:value-of select="//ISSUE/@VOL"/>
				</xsl:if>
				<xsl:if test="//ISSUE/@NUM='AHEAD' or //ISSUE/@NUM='ahead'">
					<xsl:value-of select="substring(//ISSUE/@PUBDATE,1,4)"/>
				</xsl:if>
				<xsl:if test="//ISSUE/@NUM">n<xsl:choose>
						<xsl:when test="//ISSUE/@NUM='AHEAD'">ahead</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="//ISSUE/@NUM"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:if>
				<xsl:if test="//ISSUE/@SUPPL">s<xsl:value-of select="//ISSUE/@SUPPL"/>
				</xsl:if>/</xsl:when>
			<xsl:otherwise>/</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<!--
		node, attr, text
	-->
	<xsl:template match="*">
		<xsl:comment> *, <xsl:value-of select="name()"/>
		</xsl:comment>
		<xsl:apply-templates select="@* | * | text()"/>
	</xsl:template>
	<xsl:template match="a | p |  sup | sub">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@* | * | text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="@*">
		<!--xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute-->
	</xsl:template>
	<xsl:template match="@id">
		<a name="{.}"/>
	</xsl:template>
	<!--
		xref
	-->
	<xsl:template match="xref/@rid">
		<a href="#{.}">
			<xsl:value-of select="."/>
		</a>
	</xsl:template>
	<xsl:template match="xref">
		<sup>
			<xsl:apply-templates select="@*|*|text()"/>
		</sup>
	</xsl:template>
	<xsl:template match="xref[text()!='']">
		<sup>
			<a href="#{@rid}">
				<xsl:value-of select="."/>
			</a>
		</sup>
	</xsl:template>
	<xsl:template match="xref[@ref-type='fig' or @ref-type='table' or @ref-type='equation']">
		<a href="#{@rid}">
			<xsl:value-of select="."/>
		</a>
	</xsl:template>
	<!--
		bold, italic
	-->
	<xsl:template match="bold">
		<b>
			<xsl:apply-templates/>
		</b>
	</xsl:template>
	<xsl:template match="italic">
		<i>
			<xsl:apply-templates/>
		</i>
	</xsl:template>
	
	<xsl:template match="*[@rid]" mode="check">
		<xsl:variable name="rid" select="@rid"/>
		<xsl:comment>
			<xsl:value-of select="$rid"/>=<xsl:value-of select="$all_id[@id=$rid]/@id"/>?
		</xsl:comment>
		<xsl:if test="not($all_id[@id=$rid])">
			<p>Missing id=<xsl:value-of select="$rid"/></p>
		</xsl:if>
	
	</xsl:template>
	<xsl:template match="xref[not(@rid)]" mode="check">
		<p>Missing or invalid rid. In markup file, find "<xsl:value-of select="."/>[/xref]" and check the rid. There must be something like  [xref rid="???"]<xsl:value-of select="."/>[/xref], where ??? is a valid id, e.g.: f01</p>

	
	</xsl:template>

	
	<!--
		inicio
	-->
	<xsl:template match="*" mode="make-a-piece">
		<!-- variable to be used in div id's to keep them unique -->
		
		<xsl:if test="not(//ARTICLE)">
		<div class="warning">		
			<xsl:apply-templates select=".//xref[not(@rid)]" mode="check"/>
			<xsl:apply-templates select=".//*[@rid]" mode="check"/>
		</div>
		
		</xsl:if>
		
		
		<div id="front" class="fm">
			<!-- class is repeated on contained table elements -->

			<xsl:apply-templates select="." mode="make-front"/>
		</div>
		<div id="body" class="body">
			<xsl:apply-templates select="." mode="make-body"/>
		</div>
		<div id="back" class="bm">
			<!-- class is repeated on contained table elements -->
			<xsl:apply-templates select="." mode="make-back"/>
		</div>
		<!-- retrieval metadata, at end -->
	</xsl:template>
	<xsl:template match="*" mode="make-end-metadata">
		<xsl:apply-templates select=".//article-meta"/>
	</xsl:template>
	<xsl:template match="article-meta">
		<xsl:apply-templates select="article-categories"/>
		<xsl:apply-templates select="related-article"/>
		<xsl:apply-templates select="conference"/>
	</xsl:template>
	<xsl:template match="mml:math">
		<xsl:comment>pmc</xsl:comment>
		<xsl:copy-of select="."/>
	</xsl:template>
	<xsl:template match="tex-math">
		<xsl:variable name="f">
			<xsl:choose>
				<xsl:when test="contains(.,'\begin{document}')">
					<xsl:value-of select="substring-before(substring-after(.,'\begin{document} $$'),'$$ \end{document}')"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<img src="{concat(//MIMETEX,'?',$f)}" alt="" border="0" align="middle"/>
	</xsl:template>
	<xsl:template match="email">
		<a href="mailto:{.}">
			<xsl:apply-templates/>
		</a>
	</xsl:template>
	<xsl:template match="ext-link[not(contains(@xlink:href,':')) and contains(@xlink:href,'.pdf')]">
		<a href="{concat($var_SUPPLMAT_PATH,@xlink:href)}" target="_blank">
			<xsl:apply-templates select="*|text()"/>
		</a>
	</xsl:template>
	<xsl:template match="title[normalize-space(.//text())='']">
		<xsl:comment>empty title</xsl:comment>
	</xsl:template>
	<xsl:template match="trans-title" mode="format">
		<xsl:variable name="lang" select="@xml:lang"/>
		<p class="scielo-article-other-titles{$languages//language[@id=$lang]/@view}">
			<xsl:value-of select="."/>
		</p>
	</xsl:template>
</xsl:transform>
