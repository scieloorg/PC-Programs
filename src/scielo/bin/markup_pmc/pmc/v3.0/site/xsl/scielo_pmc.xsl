<?xml version="1.0" encoding="utf-8"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" xmlns:ie5="http://www.w3.org/TR/WD-xsl" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:fns="http://www.w3.org/2002/Math/preference" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:pref="http://www.w3.org/2002/Math/preference" pref:renderer="mathplayer" exclude-result-prefixes="util xsl">
	<xsl:variable name="mainLanguage" select="//article/@xml:lang"/>
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
	<xsl:template match="xref">
		<sup>
			<a href="#{@rid}">
				<xsl:value-of select="@rid"/>
			</a>
		</sup>
	</xsl:template>
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
	<!--
	-->
	<xsl:template match="*" mode="make-a-piece">
		<!-- variable to be used in div id's to keep them unique -->
		<xsl:variable name="which-piece">
			<xsl:value-of select="concat(local-name(), '-level-', count(ancestor::*))"/>
		</xsl:variable>
		<!-- front matter, in table -->
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-front" class="fm">
			<!-- class is repeated on contained table elements -->
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates select="." mode="make-front"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-body" class="body">
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates select="." mode="make-body"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-back" class="bm">
			<!-- class is repeated on contained table elements -->
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates select="." mode="make-back"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<!-- retrieval metadata, at end -->
		<xsl:call-template name="nl-2"/>
	</xsl:template>
	<!--
		body
	-->
	<xsl:template match="*" mode="make-body">
		<xsl:apply-templates select=".//body/*"/>
	</xsl:template>
	<xsl:template match="sec[@sec-type]">
		<div class="section">
			<a name="{@sec-type}"/>
			<xsl:apply-templates select="label" mode="body"/>
			<xsl:apply-templates select="*[name()!='label']"/>
		</div>
	</xsl:template>
	<xsl:template match="sec/label" mode="body">
		<h3>
			<xsl:apply-templates/>
			<a href="#topo">-</a>
		</h3>
	</xsl:template>
	<xsl:template match="sec/sec">
		<div class="subsection">
			<xsl:apply-templates select="*"/>
		</div>
	</xsl:template>
	<xsl:template match="p">
		<xsl:comment>p66666666</xsl:comment>
		<p>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates select="*|@*|text()"/>
		</p>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- 
	back
	-->
	<xsl:template match="*" mode="make-back">
		<xsl:comment>*, make-back</xsl:comment>
		<xsl:variable name="layout" select="'float'"/>
		<xsl:choose>
			<xsl:when test=".//back//table-wrap or .//body//sec//fig">
				<xsl:apply-templates select=".//back/*[.//table-wrap] | .//back/*[.//fig] "/>
			</xsl:when>
			<xsl:when test=".//body//sec//table-wrap or .//body//sec//fig">
				<xsl:comment>nada</xsl:comment>
			</xsl:when>
			<xsl:otherwise>
				<xsl:comment>layout float</xsl:comment>
				<xsl:apply-templates select="." mode="figures-and-tables"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates select="//ack"/>
		<xsl:apply-templates select=".//back/ref-list"/>
		<xsl:apply-templates select="//author-notes" mode="back"/>
		<xsl:apply-templates select="//permissions" mode="back"/>
		<xsl:apply-templates select=".//back/*[name()!='ref-list'  and name()!='ack' and not(.//table-wrap)]"/>
	</xsl:template>
	<xsl:template match="ref-list/label">
		<h3><xsl:apply-templates /></h3>
	</xsl:template>
	<xsl:template match="author-notes" mode="back">
		<div id="{name()}" class="back">
			<xsl:apply-templates select="@*|*|text()"/>
		</div>
	</xsl:template>
	<xsl:template match="author-notes" mode="back">
		<div id="corresp" class="back">
			<p>
				<br/>
			</p>
			<p>
				<br/>
			</p>
			<a>
				<xsl:attribute name="href">#top</xsl:attribute>^
		</a>
			<xsl:text> </xsl:text>
			<a name="CORRESP">&#160;
		</a>
			<xsl:apply-templates select="*|text()"/>
		</div>
	</xsl:template>
	<!--
	 footnotes
	-->
	<xsl:template match="fn">
		<p>
			<xsl:apply-templates select="@*|*|text()"/>
		</p>
	</xsl:template>
	<xsl:template match="fn/p">
		<xsl:apply-templates select="text()"/>
	</xsl:template>
	<xsl:template match="fn/@*">
	</xsl:template>
	<xsl:template match="fn/@id">
		<sup>
			<a name="{.}"/>
			<a href="#back_fn{.}">
				<xsl:value-of select="."/>
			</a>
		</sup>
	</xsl:template>
	<xsl:template match="xref[@ref-type='fn']">
		<a name="back_fn{@rid}">
			</a>
		<sup>
			<xsl:text> </xsl:text>
			<a href="#{@rid}">
				<xsl:value-of select="@rid"/>
			</a>
		</sup>
		<xsl:text> </xsl:text>
	</xsl:template>
	<!--
	 
	-->
	<!-- ScELO -->
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
	<xsl:template match="trans-title" mode="format">
		<xsl:variable name="lang" select="@xml:lang"/>
		<p class="scielo-article-other-titles{$languages//language[@id=$lang]/@view}">
			<xsl:value-of select="."/>
		</p>
	</xsl:template>
	<xsl:template match="email">
		<a href="mailto:{.}">
			<xsl:apply-templates/>
		</a>
	</xsl:template>
	<xsl:template match="title[normalize-space(.//text())='']">
		<xsl:comment>empty title</xsl:comment>
	</xsl:template>
	<xsl:template match="back/*[.//table-wrap]">
		<div id="tables">
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<xsl:template match="back/*[.//fig]">
		<div id="figs">
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<xsl:template match="permissions" mode="back">
		<p>
			<xsl:value-of select="copyright-year"/>
			<xsl:value-of select="copyright-statement"/>
			<xsl:apply-templates select="license"/>
		</p>
	</xsl:template>
	<xsl:template match="ext-link[not(contains(@xlink:href,':')) and contains(@xlink:href,'.pdf')]">
		<a href="{concat($var_SUPPLMAT_PATH,@xlink:href)}" target="_blank">
			<xsl:apply-templates select="*|text()"/>
		</a>
	</xsl:template>
	<xsl:template match="a">
		<xsl:copy-of select="."/>
	</xsl:template>
</xsl:transform>
