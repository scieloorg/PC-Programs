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
	<xsl:template match="*" mode="make-body">
		<xsl:apply-templates select=".//body/*"/>
	</xsl:template>
	<xsl:template match="sec[@sec-type]">
		<div class="section">
			<a name="{@sec-type}"/>
			<xsl:apply-templates select="*"/>
		</div>
	</xsl:template>
	<xsl:template match="sec/sec">
		<div class="subsection">
			<xsl:apply-templates select="*"/>
		</div>
	</xsl:template>
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
		<div>
			<xsl:apply-templates select="//ack"/>
		</div>
		<xsl:apply-templates select=".//back/ref-list"/>
		<div>
			<xsl:apply-templates select=".//back/*[name()!='ref-list'  and name()!='ack' and name()!='fn-group' and not(.//table-wrap)]"/>
			<xsl:apply-templates select="//author-notes" mode="text"/>
			<xsl:apply-templates select="//history" mode="text"/>
			<xsl:apply-templates select="//fn-group" mode="text"/>
			<xsl:apply-templates select="//permissions"/>
		</div>
	</xsl:template>
	<xsl:template match="author-notes" mode="text">
		<xsl:apply-templates select="*" mode="text"/>
	</xsl:template>
	<xsl:template match="author-notes/corresp" mode="text">
		<p>
			<br/>
		</p>
		<p>
			<br/>
		</p>
		<a>
			<xsl:attribute name="href">#top</xsl:attribute>
			<img src="/img/seta.gif" alt="" border="0" align="middle"/>
		</a>
		<xsl:text> </xsl:text>
		<a name="CORRESP">&#160;
		</a>
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<!--xsl:template match="author-notes/fn" mode="text">
		
	</xsl:template-->
	<xsl:template match="corresp" mode="copyValue">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<!-- ScELO -->
	<xsl:template match="history" mode="text">
		<div class="history">
			<xsl:apply-templates select="date" mode="text"/>
			<xsl:text>.</xsl:text>
		</div>
	</xsl:template>
	<xsl:template match="date" mode="text">
		<xsl:if test="position()!=1">; </xsl:if>
		<xsl:variable name="the-type">
			<xsl:choose>
				<xsl:when test="@date-type='accepted'">Accepted: </xsl:when>
				<xsl:when test="@date-type='received'">Received: </xsl:when>
				<xsl:when test="@date-type='rev-request'">Revision Requested: </xsl:when>
				<xsl:when test="@date-type='rev-recd'">Revision Received: </xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="@date-type">
			<!--span class="gen"-->
			<xsl:value-of select="$the-type"/>
			<xsl:text/>
			<!--/span-->
		</xsl:if>
		<xsl:variable name="the-month">
			<xsl:choose>
				<xsl:when test="month='01'">January</xsl:when>
				<xsl:when test="month='02'">February</xsl:when>
				<xsl:when test="month='03'">March</xsl:when>
				<xsl:when test="month='04'">April</xsl:when>
				<xsl:when test="month='05'">May</xsl:when>
				<xsl:when test="month='06'">June</xsl:when>
				<xsl:when test="month='07'">July</xsl:when>
				<xsl:when test="month='08'">August</xsl:when>
				<xsl:when test="month='09'">September</xsl:when>
				<xsl:when test="month='10'">October</xsl:when>
				<xsl:when test="month='11'">November</xsl:when>
				<xsl:when test="month='12'">December</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:value-of select="$the-month"/>
		<xsl:text> </xsl:text>
		<xsl:value-of select="day"/>
		<xsl:text>, </xsl:text>
		<xsl:value-of select="year"/>
	</xsl:template>
	<xsl:template match="fn-group" mode="text">
		<p>
			<br/>
		</p>
		<p>
			<br/>
		</p>
		<p>
			<br/>
		</p>
		<xsl:value-of select="fn"/>
	</xsl:template>
	<xsl:template match="fn" mode="text">
		<p>
			<xsl:apply-templates select="@*|*|text()"/>
		</p>
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
	<xsl:template match="author-notes" mode="translate">
		<xsl:param name="lang">
			<xsl:choose>
				<xsl:when test="../../../../..//ARTICLE/@TEXTLANG">
					<xsl:value-of select="../../../../..//ARTICLE/@TEXTLANG"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="../../../..//@xml:lang"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:param>
		<xsl:choose>
			<xsl:when test="$lang='pt' ">Correspondência</xsl:when>
			<xsl:when test="$lang='es' ">Correspondencia</xsl:when>
			<xsl:when test="$lang='en' ">Send correspondence to</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="*" mode="back">
		<!--a href="javascript: back()">_</a-->
	</xsl:template>
	<xsl:template match="title[normalize-space(.//text())='']">
		<xsl:comment>empty title</xsl:comment>
	</xsl:template>
	<xsl:template match="back/*">
		<div>
			<xsl:attribute name="id"><xsl:value-of select="name()"/></xsl:attribute>
			<xsl:apply-templates/>
		</div>
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
	<xsl:template match="permissions">
		<p>
			<xsl:value-of select="copyright-year"/>
			<xsl:value-of select="copyright-statement"/>
			<xsl:apply-templates select="license"/>
		</p>
	</xsl:template>
	<xsl:template match="fn/@id">
		<a name="{.}">&#160;</a>
	</xsl:template>
	<xsl:template match="ext-link[not(contains(@xlink:href,':')) and contains(@xlink:href,'.pdf')]">
		<a href="{concat($var_SUPPLMAT_PATH,@xlink:href)}" target="_blank">
			<xsl:apply-templates select="*|text()"/>
		</a>
	</xsl:template>
	<xsl:template match="p">
		<xsl:comment>p66666666</xsl:comment>
		<p>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates select="*|@*|text()"/>
		</p>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="a">
		<xsl:copy-of select="."/>
	</xsl:template>
</xsl:transform>
