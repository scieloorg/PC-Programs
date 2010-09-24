<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="corresp" select=".//unidentified[contains(.,'Corresp')]"/>
	<xsl:variable name="corresp2" select=".//unidentified[contains(.,'@')]"/>
	<xsl:variable name="ack" select=".//unidentified[contains(.,'Ack') or contains(.,'Agradec')]"/>
	<xsl:variable name="cit" select=".//unidentified[not(sec) and contains(.,'Refer') ]"/>
	<xsl:variable name="xref_id" select=".//*[@id]"/>
	<xsl:variable name="journal_acron" select="//extra-scielo/journal-acron"/>
	<xsl:variable name="journal_issn" select="node()/@issn"/>
	<xsl:variable name="journal_vol" select="node()/@volid"/>
	<xsl:variable name="article_page">
		<xsl:choose>
			<xsl:when test="./@fpage='0'">
				<xsl:value-of select="node()/@order"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="node()/@fpage"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:variable name="prefixFigOrTabId">
		<xsl:value-of select="//extra-scielo/changeFigOrTabId"/>
	</xsl:variable>
	<xsl:variable name="data4previous" select="//back//*[contains(name(),'citat')]"/>
	<!--
	
	-->
	<xsl:template match="text()">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>
	<xsl:template match="*">
		<xsl:param name="id"/>
		<xsl:element name="{name()}">
			<xsl:apply-templates select="*|@*|text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template>
	<xsl:template match="graphic">
		<graphic xlink:href="{@href}"/>
	</xsl:template>
	<xsl:template match="@filename">
	</xsl:template>
	<xsl:template match="@doctopic" mode="type">
		<xsl:attribute name="article-type"><xsl:choose><xsl:when test=".='oa'">research-article</xsl:when><xsl:when test=".='ab'">abstract</xsl:when><xsl:when test=".='an'">announcement</xsl:when><xsl:when test=".='co'">article-commentary</xsl:when><xsl:when test=".='cr'">case-report</xsl:when><xsl:when test=".='ed'">editorial</xsl:when><xsl:when test=".='le'">letter</xsl:when><xsl:when test=".='ra'">review-article</xsl:when><xsl:when test=".='sc'">rapid-communication</xsl:when><xsl:when test=".='??'">addendum</xsl:when><xsl:when test=".='??'">book-review</xsl:when><xsl:when test=".='??'">books-received</xsl:when><xsl:when test=".='??'">brief-report</xsl:when><xsl:when test=".='??'">calendar</xsl:when><xsl:when test=".='??'">collection</xsl:when><xsl:when test=".='??'">correction</xsl:when><xsl:when test=".='??'">discussion</xsl:when><xsl:when test=".='??'">dissertation</xsl:when><xsl:when test=".='??'">in-brief</xsl:when><xsl:when test=".='??'">introduction</xsl:when><xsl:when test=".='??'">meeting-report</xsl:when><xsl:when test=".='??'">news</xsl:when><xsl:when test=".='??'">obituary</xsl:when><xsl:when test=".='??'">oration</xsl:when><xsl:when test=".='??'">partial-retraction</xsl:when><xsl:when test=".='??'">product-review</xsl:when><xsl:when test=".='??'">reply</xsl:when><xsl:when test=".='??'">reprint</xsl:when><xsl:when test=".='??'">retraction</xsl:when><xsl:when test=".='??'">translation</xsl:when><xsl:otherwise>other</xsl:otherwise></xsl:choose></xsl:attribute>
	</xsl:template>
	<xsl:template match="@language">
		<xsl:attribute name="xml:lang"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template>
	<xsl:template match="fname">
		<given-names>
			<xsl:apply-templates/>
		</given-names>
	</xsl:template>
	<xsl:template match="article|text">
		<article dtd-version="3.0">
			<xsl:apply-templates select="@doctopic" mode="type"/>
			<xsl:apply-templates select="@language"/>
			<xsl:apply-templates select="." mode="front"/>
			<xsl:apply-templates select="." mode="body"/>
			<xsl:apply-templates select="." mode="back"/>
		</article>
	</xsl:template>
	<xsl:template match="*" mode="front">
		<front>
			<xsl:apply-templates select="." mode="journal-meta"/>
			<xsl:apply-templates select="." mode="article-meta"/>
		</front>
	</xsl:template>
	<xsl:template match="article|text" mode="journal-meta">
		<journal-meta>
			<xsl:copy-of select=".//journal-id"/>
			<journal-id journal-id-type="publisher">
				<xsl:value-of select="@issn"/>
			</journal-id>
			<journal-title-group>
				<abbrev-journal-title abbrev-type="publisher">
					<xsl:value-of select="@stitle"/>
				</abbrev-journal-title>
				<xsl:copy-of select=".//journal-title"/>
			</journal-title-group>
			<issn>
				<xsl:value-of select="@issn"/>
			</issn>
			<xsl:copy-of select="..//extra-scielo/publisher"/>
		</journal-meta>
	</xsl:template>
	<xsl:template match="article|text" mode="article-meta">
		<xsl:variable name="l" select="@language"/>
		<article-meta>
			<xsl:if test="..//extra-scielo/issue-order">
				<article-id pub-id-type="publisher-id">S<xsl:value-of select="@issn"/>
					<xsl:value-of select="substring(@dateiso,1,4)"/>
					<xsl:value-of select="substring(10000 + substring(..//extra-scielo/issue-order,5),2)"/>
					<xsl:value-of select="substring-after(100000 + @order,'1')"/>
				</article-id>
			</xsl:if>
			<xsl:apply-templates select="." mode="article-title"/>
			<xsl:apply-templates select=".//authgrp" mode="front"/>
			<xsl:apply-templates select="." mode="author-notes"/>
			<pub-date pub-type="pub">
				<month>
					<xsl:value-of select="substring(@dateiso,5,2)"/>
				</month>
				<year>
					<xsl:value-of select="substring(@dateiso,1,4)"/>
				</year>
			</pub-date>
			<xsl:apply-templates select="@volid | @issueno | @supplvol | @supplno | @fpage | @lpage"/>
			<xsl:apply-templates select=".//hist"/>
			<xsl:apply-templates select=".//back/licenses"/>
			<xsl:apply-templates select=".//abstract[@language=$l]"/>
			<xsl:apply-templates select=".//abstract[@language!=$l]" mode="trans"/>
			<xsl:apply-templates select=".//keygrp"/>
			<xsl:apply-templates select=".//front/report | .//front/confgrp | ..//front/thesgrp | .//bibcom/report | .//bibcom/confgrp | ..//bibcom/thesgrp  | .//bbibcom/report | .//bbibcom/confgrp | ..//bbibcom/thesgrp "/>
		</article-meta>
	</xsl:template>
	<xsl:template match="*" mode="article-title">
		<xsl:variable name="l" select="//*[name()='article' or name()='text']/@language"/>
		<title-group>
			<xsl:apply-templates select=".//titlegrp/title[@language=$l] "/>
			<xsl:apply-templates select=".//titlegrp/title[@language!=$l]" mode="trans-title-group">
				<xsl:with-param name="subtitles" select=".//titlegrp/subtitle[position()!=1]"/>
			</xsl:apply-templates>
		</title-group>
	</xsl:template>
	<xsl:template match="titlegrp/title">
		<article-title>
			<xsl:apply-templates select="@language|*|text()"/>
		</article-title>
		<xsl:apply-templates select="../subtitle[1]"/>
	</xsl:template>
	<xsl:template match="title" mode="trans-title-group">
		<xsl:param name="subtitles"/>
		<xsl:variable name="p" select="position()"/>
		<trans-title-group>
			<xsl:apply-templates select="@language"/>
			<xsl:apply-templates select="." mode="trans-title"/>
			<xsl:apply-templates select="$subtitles[$p]" mode="trans-title"/>
		</trans-title-group>
	</xsl:template>
	<xsl:template match="title|subtitle" mode="trans-title">
		<xsl:element name="trans-{name()}">
			<xsl:apply-templates select="*|text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="authgrp" mode="front">
		<contrib-group>
			<xsl:apply-templates select="author|corpauth" mode="front"/>
		</contrib-group>
		<xsl:apply-templates select="..//aff"/>
	</xsl:template>
	<xsl:template match="@role">
		<xsl:attribute name="contrib-type"><xsl:choose><xsl:when test=".='nd'">author</xsl:when><xsl:when test=".='ed'">editor</xsl:when><xsl:when test=".='tr'">translator</xsl:when><xsl:when test=".='rev'">rev</xsl:when></xsl:choose></xsl:attribute>
	</xsl:template>
	<xsl:template match="author|corpauth" mode="front">
		<contrib>
			<xsl:apply-templates select="@role"/>
			<xsl:apply-templates select="."/>
			<xsl:apply-templates select="@rid"/>
		</contrib>
	</xsl:template>
	<xsl:template match="author/@rid">
		<xref ref-type="aff" rid="aff{substring(normalize-space(.),3,1)}"/>
		<xsl:if test="string-length(normalize-space(.))&gt;3">
			<xref ref-type="aff" rid="aff{substring(substring-after(normalize-space(.),' '),3,1)}"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="aff">
		<aff id="aff{substring(@id,3)}">
			<xsl:apply-templates select="@*[name()!='id']"/>
			<xsl:apply-templates select="city | state | country | zipcode | e-mail"/>
		</aff>
	</xsl:template>
	<xsl:template match="aff/@*">
		<xsl:element name="{name()}">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="aff/@orgname">
		<institution>
			<xsl:value-of select="."/>
		</institution>
	</xsl:template>
	<xsl:template match="aff/*">
		<xsl:copy>
			<xsl:value-of select="."/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="e-mail">
		<email>
			<xsl:apply-templates/>
		</email>
	</xsl:template>
	<xsl:template match="*" mode="author-notes">
		<xsl:choose>
			<xsl:when test="$corresp//p">
				<author-notes>
					<xsl:apply-templates select="$corresp//p" mode="corresp"/>
				</author-notes>
			</xsl:when>
			<xsl:otherwise>
				<author-notes>
					<xsl:apply-templates select="$corresp2//p" mode="corresp"/>
				</author-notes>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="p" mode="corresp">
		<corresp>
			<xsl:choose>
				<xsl:when test="contains(.,'@') and not(contains(normalize-space(.),' '))">
					<email>
						<xsl:apply-templates select="bold|italic|sup|sub|uri|text()"/>
					</email>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="bold|italic|sup|sub|uri|text()"/>
				</xsl:otherwise>
			</xsl:choose>
		</corresp>
	</xsl:template>
	<xsl:template match="@volid | volid">
		<volume>
			<xsl:value-of select="."/>
		</volume>
	</xsl:template>
	<xsl:template match="@issueno | issueno">
		<issue>
			<xsl:value-of select="."/>
		</issue>
	</xsl:template>
	<xsl:template match="@supplvol | @supplno | suppl">
		<supplement>
			<xsl:value-of select="."/>
		</supplement>
	</xsl:template>
	<xsl:template match="@fpage | fpage">
		<fpage>
			<xsl:value-of select="."/>
		</fpage>
	</xsl:template>
	<xsl:template match="@lpage | lpage">
		<lpage>
			<xsl:value-of select="."/>
		</lpage>
	</xsl:template>
	<xsl:template match="pages">
		<page-range>
			<xsl:value-of select="."/>
		</page-range>
	</xsl:template>
	<xsl:template match="hist">
		<history>
			<xsl:apply-templates select="received | revised | accepted "/>
		</history>
	</xsl:template>
	<xsl:template match="received | revised | accepted">
		<date date-type="{name()}">
			<day>
				<xsl:value-of select="substring(@dateiso,7,2)"/>
			</day>
			<month>
				<xsl:value-of select="substring(@dateiso,5,2)"/>
			</month>
			<year>
				<xsl:value-of select="substring(@dateiso,1,4)"/>
			</year>
		</date>
	</xsl:template>
	<xsl:template match="abstract" mode="trans">
		<trans-abstract xml:lang="{@language}">
			<p>
				<xsl:apply-templates/>
			</p>
		</trans-abstract>
	</xsl:template>
	<xsl:template match="abstract">
		<abstract xml:lang="{@language}">
			<p>
				<xsl:apply-templates/>
			</p>
		</abstract>
	</xsl:template>
	<xsl:template match="keygrp">
		<kwd-group xml:lang="{keyword[1]/@language}">
			<xsl:apply-templates select="keyword"/>
		</kwd-group>
	</xsl:template>
	<xsl:template match="keyword">
		<kwd>
			<xsl:apply-templates/>
		</kwd>
	</xsl:template>
	<xsl:template match="confgrp">
		<conference>
			<conf-date>
				<xsl:value-of select="date"/>
			</conf-date>
			<conf-name>
				<xsl:value-of select="confname"/>
			</conf-name>
			<conf-num>
				<xsl:value-of select="no"/>
			</conf-num>
			<xsl:if test="city or state or country">
				<conf-loc>
					<xsl:value-of select="city"/>
					<xsl:if test="city and state">, </xsl:if>
					<xsl:value-of select="state"/>
					<xsl:if test="(city or state) and country">,</xsl:if>
					<xsl:value-of select="country"/>
				</conf-loc>
			</xsl:if>
			<xsl:if test="sponsor">
				<conf-sponsor>
					<xsl:value-of select="sponsor"/>
				</conf-sponsor>
			</xsl:if>
		</conference>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//confgrp">
		<conf-date>
			<xsl:value-of select="date"/>
		</conf-date>
		<conf-name>
			<xsl:value-of select="confname"/>
		</conf-name>
		<conf-num>
			<xsl:value-of select="no"/>
		</conf-num>
		<xsl:if test="city or state or country">
			<conf-loc>
				<xsl:value-of select="city"/>
				<xsl:if test="city and state">, </xsl:if>
				<xsl:value-of select="state"/>
				<xsl:if test="(city or state) and country">,</xsl:if>
				<xsl:value-of select="country"/>
			</conf-loc>
		</xsl:if>
		<xsl:if test="sponsor">
			<conf-sponsor>
				<xsl:value-of select="sponsor"/>
			</conf-sponsor>
		</xsl:if>
	</xsl:template>
	<xsl:template match="*" mode="counts">
		<counts>
			<fig-count count="{count(.//figgrp)}"/>
			<table-count count="{count(.//tabwrap)}"/>
			<equation-count count="{count(.//equation)}"/>
			<ref-count count="{count(.//ref/element-citation)}"/>
			<!--page-count count="6"/-->
			<!--word-count count="2847"/-->
		</counts>
	</xsl:template>
	<xsl:template match="*" mode="body">
		<body>
			<xsl:apply-templates select="xmlbody|unidentified"/>
		</body>
	</xsl:template>
	<xsl:template match="body"/>
	<xsl:template match="xmlbody">
		<xsl:apply-templates select=" * |text()"/>
	</xsl:template>
	<xsl:template match="unidentified">
		<xsl:apply-templates select="*"/>
	</xsl:template>
	<xsl:template match="text/unidentified | article/unidentified">
		<xsl:choose>
			<xsl:when test="not(contains(.,'Corresp')) and not(contains(.,'Ack') or contains(.,'Agradec')) and not(contains(.,'Refer'))">
				<xsl:apply-templates select="*"/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="subsec">
		<sec>
			<xsl:apply-templates select="@*|*|text()"/>
		</sec>
	</xsl:template>
	<xsl:template match="sectitle">
		<title>
			<xsl:apply-templates/>
			<xsl:apply-templates select="following-sibling::node()[1 and name()='xref']" mode="xref-in-sectitle"/>
		</title>
	</xsl:template>
	<xsl:template match="@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="*" mode="back">
		<back>
			<xsl:apply-templates select="$ack" mode="ack"/>
			<xsl:apply-templates select="back/vancouv | back/abnt6023 | back/iso690 | back/other| back/apa "/>
			<xsl:apply-templates select="..//hist" mode="back"/>
			<xsl:apply-templates select="back//fngrp"/>
			<!--xsl:apply-templates select="$otherUnidentified"/-->
			<!--xsl:apply-templates select=".//bbibcom" mode="back-info"/-->
		</back>
	</xsl:template>
	<!--xsl:template match="bbibcom " mode="back-info">
		<xsl:apply-templates select="*|text()" mode="back-info"/>
	</xsl:template>
	<xsl:template match="bbibcom//* | bbibcom//text() " mode="back-info">
		<xsl:value-of select="."/>&#160;
	</xsl:template>
	<xsl:template match="bbibcom/text() " mode="back-info">
		<notes>
			<p>
				<xsl:value-of select="."/>
			</p>
		</notes>
	</xsl:template>
	<xsl:template match="bbibcom/* " mode="back-info">
		<notes>
			<p>
				<xsl:apply-templates select="*|text()" mode="back-info"/>
			</p>
		</notes>
	</xsl:template-->
	<xsl:template match="hist" mode="back">
		<notes>
			<p>
				<xsl:apply-templates select=".//text()"/>
			</p>
		</notes>
	</xsl:template>
	<xsl:template match="unidentified" mode="ack">
		<ack>
			<xsl:apply-templates select="*"/>
		</ack>
	</xsl:template>
	<xsl:template match="*[@standard]">
		<ref-list>
			<xsl:if test="bold">
				<label>
					<xsl:value-of select="bold"/>
				</label>
			</xsl:if>
			<xsl:if test="$cit">
				<xsl:apply-templates select="$cit/*"/>
			</xsl:if>
			<!--xsl:apply-templates select="*[contains(name(),'citat')]"/-->
		</ref-list>
	</xsl:template>
	<xsl:template match="*[@standard]/*">
		<ref id="R{position()}">
			<xsl:apply-templates select="no"/>
			<!-- book, communication, letter, review, conf-proc, journal, list, patent, thesis, discussion, report, standard, and working-paper.  -->
			<xsl:variable name="type">
				<xsl:choose>
					<xsl:when test="viserial or aiserial or oiserial or iiserial or piserial">journal</xsl:when>
					<xsl:when test=".//confgrp">conf-proc</xsl:when>
					<xsl:when test=".//degree">thesis</xsl:when>
					<xsl:when test=".//patgrp">patent</xsl:when>
					<xsl:when test="vmonog or amonog or omonog or imonog or pmonog">book</xsl:when>
					<xsl:otherwise>other</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<element-citation publication-type="{$type}">
				<xsl:apply-templates select="*[name()!='no' and name()!='text-ref']">
					<xsl:with-param name="position" select="position()"/>
				</xsl:apply-templates>
			</element-citation>
			<xsl:apply-templates select="." mode="text-ref"/>
		</ref>
	</xsl:template>
	<xsl:template match="back//no">
		<label>
			<xsl:value-of select="."/>
		</label>
	</xsl:template>
	<xsl:template match="*[contains(name(),'monog')]">
		<xsl:variable name="type">
			<xsl:choose>
				<xsl:when test=".//node()[@role='org']">compiler</xsl:when>
				<xsl:when test=".//node()[@role='ed']">editor</xsl:when>
				<xsl:when test=".//node()[@role='nd']">author</xsl:when>
				<xsl:when test=".//node()[@role='tr']">translator</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test=".//*[contains(name(),'auth')]">
			<person-group person-group-type="{$type}">
				<xsl:apply-templates select=".//*[contains(name(),'auth')]"/>
			</person-group>
		</xsl:if>
		<xsl:apply-templates select="*[not(contains(name(),'auth'))]"/>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'corpaut')]">
		<collab>
			<xsl:value-of select="orgdiv"/>
			<xsl:if test="orgdiv">, </xsl:if>
			<xsl:value-of select="orgname"/>
		</collab>
	</xsl:template>
	<xsl:template match="*[contains(name(),'author')]">
		<name>
			<xsl:apply-templates select="surname"/>
			<xsl:apply-templates select="fname"/>
		</name>
	</xsl:template>
	<xsl:template match="back//*[previous]">
		<xsl:param name="position"/>
		<xsl:apply-templates select="$data4previous[$position - 1]//*[contains(name(),'author')]">
			<xsl:with-param name="position" select="$position - 1"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="back//stitle | back//vstitle | vmonog/vtitle/title | coltitle">
		<source>
			<xsl:value-of select="."/>
		</source>
	</xsl:template>
	<xsl:template match="back//date">
		<day>
			<xsl:value-of select="substring(@dateiso,7,2)"/>
		</day>
		<month>
			<xsl:value-of select="substring(@dateiso,5,2)"/>
		</month>
		<year>
			<xsl:value-of select="substring(@dateiso,1,4)"/>
		</year>
	</xsl:template>
	<xsl:template match="back//cited">
		<date-in-citation content-type="access-date">
			<xsl:value-of select="."/>
		</date-in-citation>
	</xsl:template>
	<xsl:template match="back//pubname">
		<publisher-name>
			<xsl:value-of select="."/>
		</publisher-name>
	</xsl:template>
	<xsl:template match="back//orgdiv">
	</xsl:template>
	<xsl:template match="back//orgname">
		<publisher-name>
			<xsl:if test="../orgdiv">
				<xsl:value-of select="../orgdiv"/>, </xsl:if>
			<xsl:value-of select="."/>
		</publisher-name>
	</xsl:template>
	<xsl:template match="back//city">
		<publisher-loc>
			<xsl:value-of select="."/>
		</publisher-loc>
	</xsl:template>
	<xsl:template match="*[contains(name(),'contrib')]">
		<xsl:param name="position"/>
		<person-group person-group-type="author">
			<xsl:apply-templates select="*[contains(name(),'aut')] | *[contains(name(),'corpaut')]">
				<xsl:with-param name="position" select="$position"/>
			</xsl:apply-templates>
		</person-group>
		<xsl:apply-templates select=".//title"/>
	</xsl:template>
	<xsl:template match="vtitle">
	</xsl:template>
	<xsl:template match="*[contains(name(),'serial')]">
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="*[contains(name(),'serial')]/sertitle">
		<source>
			<xsl:apply-templates/>
		</source>
	</xsl:template>
	<xsl:template match="url">
		<ext-link>
			<xsl:apply-templates/>
		</ext-link>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]" mode="text-ref">
		<mixed-citation>
			<xsl:choose>
				<xsl:when test="text-ref">
					<xsl:value-of select="text-ref" disable-output-escaping="yes"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="." mode="create-text-ref"/>
				</xsl:otherwise>
			</xsl:choose>
		</mixed-citation>
	</xsl:template>
	<xsl:template match="*" mode="create-text-ref">
		<xsl:apply-templates select="@* | * | text() " mode="create-text-ref"/>
	</xsl:template>
	<xsl:template match="@*" mode="create-text-ref"/>
	<xsl:template match="text()" mode="create-text-ref">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]/text() | *[contains(name(),'citat')]//*[*]/text()"/>
	<xsl:template match="uri[contains(@href,'mailto:')]">
		<email>
			<xsl:apply-templates select=".//text()"/>
		</email>
	</xsl:template>
	<xsl:template match="figgrp">
		<p>
			<fig id="{@id}" fig-type="{@ftype}">
				<xsl:apply-templates select=".//label"/>
				<xsl:apply-templates select=".//caption"/>
				<xsl:apply-templates select="." mode="graphic">
					<xsl:with-param name="id" select="@id"/>
				</xsl:apply-templates>
			</fig>
		</p>
	</xsl:template>
	<xsl:template match="graphic/*|graphic/text()">
	</xsl:template>
	<xsl:template match="*[name()!='tabwrap']/table">
		<p>
			<xsl:apply-templates select="*|@*|text()" mode="tableless"/>
		</p>
	</xsl:template>
	<xsl:template match="*" mode="tableless">
		<xsl:apply-templates select="*|@*|text()" mode="tableless"/>
	</xsl:template>
	<xsl:template match="@*" mode="tableless">
		<xsl:apply-templates select="text()"/>
	</xsl:template>
	<xsl:template match="tabwrap">
		<p>
			<table-wrap id="{@id}">
				<xsl:apply-templates select=".//label"/>
				<xsl:apply-templates select=".//caption"/>
				<xsl:choose>
					<xsl:when test=".//graphic | @filename">
						<xsl:apply-templates select="." mode="graphic">
							<xsl:with-param name="id" select="@id"/>
						</xsl:apply-templates>
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates select=".//table"/>
					</xsl:otherwise>
				</xsl:choose>
			</table-wrap>
		</p>
	</xsl:template>
	<xsl:template match="caption">
		<caption>
			<p>
				<xsl:apply-templates/>
			</p>
		</caption>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle"/>
	<xsl:template match="back//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle" mode="title">: <xsl:apply-templates select="@* | * | text()"/>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'monog')]//title">
		<xsl:choose>
			<xsl:when test="../../node()[contains(name(),'contrib')]">
				<source>
					<xsl:apply-templates select="@language|*|text()"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
				</source>
			</xsl:when>
			<xsl:otherwise>
				<article-title>
					<xsl:apply-templates select="@language|*|text()"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
				</article-title>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'contrib')]//title">
		<article-title>
			<xsl:apply-templates select="@language|*|text()"/>
			<xsl:apply-templates select="../subtitle" mode="title"/>
		</article-title>
	</xsl:template>
	<xsl:template match="othinfo">
		<comment>
			<xsl:apply-templates/>
		</comment>
	</xsl:template>
	<xsl:template match="xref/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="xref[@rid!='']">
		<xsl:variable name="rid" select="@rid"/>
		<xsl:if test="$xref_id[@id=$rid]">
			<xref>
				<xsl:apply-templates select="@*|*[name()!='graphic']|text()"/>
			</xref>
		</xsl:if>
	</xsl:template>
	<xsl:template match="xref[graphic and @rid!='']">
		<xsl:variable name="rid" select="@rid"/>
		<xsl:if test="$xref_id[@id=$rid]">
			<xref>
				<xsl:apply-templates select="@*|*[name()!='graphic']|text()"/>
			</xref>
			<graphic>
				<xsl:apply-templates select="graphic/@*|graphic/*|graphic/text()"/>
				<uri>#<xsl:value-of select="@rid"/>
				</uri>
			</graphic>
		</xsl:if>
	</xsl:template>
	<xsl:template match="xref" mode="xref-in-sectitle">
		<xsl:copy-of select="."/>
	</xsl:template>
	<xsl:template match="text()" mode="nostyle">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="*" mode="nostyle">
		<xsl:apply-templates select="*|text()" mode="nostyle"/>
	</xsl:template>
	<xsl:template match="fname">
		<given-names>
			<xsl:apply-templates select="*|text()" mode="nostyle"/>
		</given-names>
	</xsl:template>
	<xsl:template match="surname">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="*|text()" mode="nostyle"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//p | *[contains(name(),'citat')]//unidentified | *[contains(name(),'citat')]/text()">

	</xsl:template>
	<xsl:template match="*" mode="debug">
		<xsl:comment>debugging - start </xsl:comment>
		<xsl:if test="contains(text(),'Ref')">sim</xsl:if>
		<xsl:copy-of select="."/>
		<xsl:comment>debugging - end</xsl:comment>
	</xsl:template>
	<xsl:template match="xmlbody[sec]/p | unidentified[../xmlbody[sec]]"/>
	<xsl:template match="figgrp//graphic | tabwrap//graphic | equation//graphic">
		<graphic>
			<xsl:apply-templates select="@href"/>
		</graphic>
	</xsl:template>
	<!--xsl:template match="figgrp//graphic/@href | tabwrap//graphic/@href | equation//graphic/@href">
		<xsl:param name="id"/>
		<xsl:variable name="SLASH">
			<xsl:choose>
				<xsl:when test="contains(.,'/')">/</xsl:when>
				<xsl:when test="contains(.,'\')">\</xsl:when>
				<xsl:otherwise/>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="noSlash">
			<xsl:choose>
				<xsl:when test="$SLASH!=''">
					<xsl:apply-templates select="." mode="onlyFileName">
						<xsl:with-param name="text" select="."/>
						<xsl:with-param name="slash" select="$SLASH"/>
					</xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>.
		</xsl:variable>
		<xsl:variable name="noExt">
			<xsl:value-of select="substring-before($noSlash,'.')"/>
		</xsl:variable>
		<xsl:attribute name="xlink:href"><xsl:choose><xsl:when test="$prefixFigOrTabId='yes'"><xsl:value-of select="concat($fileName,'-',$id)"/></xsl:when><xsl:otherwise><xsl:value-of select="$noExt"/></xsl:otherwise></xsl:choose></xsl:attribute>
	</xsl:template>
	<xsl:template match="@href" mode="onlyFileName">
		<xsl:param name="text"/>
		<xsl:param name="slash"/>
		<xsl:choose>
			<xsl:when test="contains($text,$slash)">
				<xsl:apply-templates select="." mode="onlyFileName">
					<xsl:with-param name="text" select="substring-after($text,$slash)"/>
					<xsl:with-param name="slash" select="$slash"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template-->
	<xsl:template match="text()[normalize-space(.)='']"/>
	<xsl:template match="equation">
		<p>
			<disp-formula>
				<xsl:apply-templates select=".//graphic | @filename">
					<xsl:with-param name="id" select="@id"/>
				</xsl:apply-templates>
			</disp-formula>
		</p>
	</xsl:template>
	<xsl:template match="equation[.//table]">
		<p>
			<disp-formula>
				<xsl:apply-templates select=".//graphic">
					<xsl:with-param name="id" select="@id"/>
				</xsl:apply-templates>
			</disp-formula>
			<xsl:apply-templates select=".//p" mode="p-in-equation"/>
		</p>
	</xsl:template>
	<xsl:template match="graphic" mode="p-in-equation">
	</xsl:template>
	<xsl:template match="p" mode="p-in-equation">
		<xsl:apply-templates select="*|text()" mode="p-in-equation"/>
	</xsl:template>
	<xsl:template match="licenses">
		<permissions>
			<xsl:apply-templates/>
		</permissions>
	</xsl:template>
	<xsl:template match="license">
		<!--copyright-statement>Copyright: &copy; 2004 Eichenberger
et al.</copyright-statement>
			<copyright-year>2004</copyright-year-->
		<license license-type="open-access" xlink:href="{@href}">
			<xsl:apply-templates select="licensep|text()"/>
		</license>
	</xsl:template>
	<xsl:template match="license/text()">
		<license-p>
			<xsl:value-of select="."/>
		</license-p>
	</xsl:template>
	<xsl:template match="licensep">
		<license-p>
			<xsl:apply-templates/>
		</license-p>
	</xsl:template>
	<xsl:template match="mmlmath">
		<mml:math>
			<xsl:copy-of select="*"/>
		</mml:math>
	</xsl:template>
	<xsl:template match="texmath">
		<tex-math>
			<xsl:apply-templates/>
		</tex-math>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//doi">
		<elocation-id>
			<xsl:value-of select="."/>
		</elocation-id>
	</xsl:template>
	<xsl:template match="sec/text() | subsec/text()"/>
	<xsl:template match="*[@filename or graphic] " mode="graphic">
		<xsl:param name="id"/>
		<xsl:apply-templates select="@filename | graphic">
			<xsl:with-param name="id" select="$id"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="thesis">
		<xsl:apply-templates select="@* | * | text()">
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="degree ">
		<comment>
			<xsl:apply-templates select="@* | * | text()">
		</xsl:apply-templates>
		</comment>
	</xsl:template>
	<xsl:template match="fngrp">
		<fn-group>
			<xsl:apply-templates select="*"/>
		</fn-group>
	</xsl:template>
	<xsl:template match="fn">
		<fn>
			<xsl:apply-templates select="@*"/>
			<p>
				<xsl:value-of select="."/>
			</p>
		</fn>
	</xsl:template>
	<xsl:template match="*[contains(name(),'contrib')]/italic | *[contains(name(),'contrib')]/bold | *[contains(name(),'monog')]/italic | *[contains(name(),'monog')]/bold"/>
	<xsl:template match="subsec/xref | sec/xref">
		<xsl:comment>xref</xsl:comment>
	</xsl:template>
</xsl:stylesheet>
