<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"
	xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="pub_type"><xsl:choose>
		<xsl:when test="node()/@ahpdate!='' and node()/@issueno='ahead'"></xsl:when>
		<xsl:when test=".//extra-scielo/print-issn!='' and .//extra-scielo/e-issn!=''">epub-ppub</xsl:when>
		<xsl:when test=".//extra-scielo/print-issn!=''">ppub</xsl:when>
		<xsl:when test=".//extra-scielo/e-issn!=''">epub</xsl:when>
	</xsl:choose></xsl:variable>
	<xsl:variable name="unident" select="//unidentified"/>
	<xsl:variable name="corresp" select="//corresp"/>
	<xsl:variable name="deceased" select="//fngrp[@fntype='deceased']"/>
	<xsl:variable name="eqcontrib" select="//fngrp[@fntype='equal']"/>
	<xsl:variable name="unident_back" select="//back//unidentified"/>
	<xsl:variable name="fn_author" select=".//fngrp[@fntype='author']"/>
	<xsl:variable name="fn" select=".//fngrp"/>
	<xsl:variable name="affs" select=".//aff"/>
	<xsl:variable name="normalized_affs" select=".//normaff"/>
	
	<xsl:variable name="affs_xrefs" select=".//front//author"/>
	<xsl:variable name="xref_id" select="//*[@id]"/>
	<xsl:variable name="qtd_ref" select="count(//*[@standard]/*)"/>
	<xsl:variable name="reflen"><xsl:choose>
		<xsl:when test="string-length($qtd_ref)&gt;2"><xsl:value-of select="string-length($qtd_ref)"/></xsl:when>
		<xsl:otherwise>2</xsl:otherwise>
	</xsl:choose></xsl:variable>
	
	<xsl:variable name="ref_no" select="//*[contains(name(),'citat')]/no"/>
	<xsl:variable name="this_doi"><xsl:choose>
		<xsl:when test="./front/doi"><xsl:value-of select="./front/doi"/></xsl:when>
		<xsl:otherwise><xsl:value-of select="doi"/></xsl:otherwise>
	</xsl:choose></xsl:variable>
	<xsl:variable name="journal_acron">
		<xsl:choose>
			<xsl:when test="//extra-scielo/journal-acron"><xsl:value-of select="//extra-scielo/journal-acron"/></xsl:when>
			<xsl:when test="node()/@acron"><xsl:value-of select="node()/@acron"/></xsl:when>
		</xsl:choose>
	</xsl:variable>
	<xsl:variable name="JOURNAL_PID" select="node()/@issn"/>
	<xsl:variable name="journal_vol" select="node()/@volid"/>
	<xsl:variable name="journal_issue">
		<xsl:if test="string-length(node()/@issueno)=1">0</xsl:if>
		<xsl:choose>
			<xsl:when test="node()/@issueno='ahead'">00</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="node()/@issueno"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:variable name="zeros_page">00000<xsl:value-of select="node()/@fpage"/></xsl:variable>
	<xsl:variable name="zeros_order">00000<xsl:value-of select="node()/@order"/></xsl:variable>
	<xsl:variable name="normalized_page">
		<xsl:value-of select="substring($zeros_page,string-length($zeros_page)-4)"/>
	</xsl:variable>
	<xsl:variable name="normalized_order">
		<xsl:value-of select="substring($zeros_order,string-length($zeros_order)-4)"/>
	</xsl:variable>
	<xsl:variable name="article_page">
		<xsl:choose>
			<xsl:when test="$normalized_page='00000'">
				<xsl:value-of select="$normalized_order"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$normalized_page"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:variable name="prefix"><xsl:value-of select="$JOURNAL_PID"/>-<xsl:value-of
			select="$journal_acron"/><xsl:if test="$journal_vol!=''">-</xsl:if><xsl:value-of
			select="$journal_vol"/><xsl:if test="$journal_issue!=''">-</xsl:if><xsl:value-of
			select="$journal_issue"/>-<xsl:value-of select="$article_page"/>-</xsl:variable>
	<!--xsl:variable name="g" select="//*[name()!='equation' and .//graphic]"/>
	<xsl:variable name="e" select="//equation[.//graphic]"/-->
	<xsl:variable name="data4previous" select="//back//*[contains(name(),'citat')]"/>
	
	<!-- text -->
	<xsl:template match="*/text()">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>
	<!-- nodes -->
	<xsl:template match="*">
		<xsl:apply-templates select="@*| * | text()"/>
	</xsl:template>
	
	<!-- attributes -->
	<xsl:template match="@*">
		<xsl:attribute name="{name()}">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template><!-- attributes -->
	
	<!--
    	mode=text
	-->
	<xsl:template match="*" mode="text-only">
		<xsl:apply-templates select="*|text()" mode="text-only"/>
	</xsl:template>
	<xsl:template match="text()" mode="text-only">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<!-- 
		mode=ignore-style
	-->
	<xsl:template match="text()" mode="ignore-style">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="*" mode="ignore-style">
		<xsl:apply-templates select="*|text()" mode="ignore-style"/>
	</xsl:template>
	<xsl:template match="bold | italic" mode="ignore-style">
		<xsl:apply-templates select="*|text()" mode="ignore-style"/>
	</xsl:template>
	
	<xsl:template match="@href">
		<xsl:attribute name="xlink:href">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template>


	<xsl:template match="isstitle">
		<issue-title>
			<xsl:value-of select="normalize-space(.)"/>
		</issue-title>
	</xsl:template>

	<xsl:template match="caption">
		<caption>
			<title>
				<xsl:apply-templates select="*|text()"/>
			</title>
		</caption>
	</xsl:template>


	<xsl:template match="et-al">
		<etal/>
	</xsl:template>
	<xsl:template match="ign"/>
	<xsl:template match="list">
		<p>
			<list>
				<xsl:apply-templates select="@*|*"/>
			</list>
		</p>
	</xsl:template>
	<xsl:template match="@listtype">
		<xsl:attribute name="list-type">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="li">
		<list-item>
			<xsl:apply-templates select="lilabel|label"/>
			<xsl:choose>
				<xsl:when test="litext">
					<xsl:apply-templates select="litext"></xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<p>
						<xsl:apply-templates select="*[name()!='label'] |text()"/>
					</p>
				</xsl:otherwise>
			</xsl:choose>
		</list-item>
	</xsl:template>
	<xsl:template match="lilabel">
		<label>
			<xsl:value-of select="normalize-space(.)"/>
		</label>
	</xsl:template>
	
	<xsl:template match="litext">
		<p>
			<xsl:apply-templates select="* | text()"/>
		</p>
	</xsl:template>

	<xsl:template match="extent">
		<size units="pages">
			<xsl:value-of select="normalize-space(.)"/>
		</size>
	</xsl:template>
	<xsl:template match="*[contains(name(),'serial')]//extent">
		<fpage>
			<xsl:value-of select="normalize-space(.)"/>
		</fpage>
	</xsl:template>
	<xsl:template match="body"/>
	<xsl:template match="bold | italic | sup" mode="formatted-text"/>
	<xsl:template match="*[bold or italic or sup]" mode="formatted-text"><xsl:apply-templates select="text()" mode="formatted-text"></xsl:apply-templates></xsl:template>
	<xsl:template match="*[bold or italic or sup]/text()" mode="formatted-text"><xsl:value-of select="."/></xsl:template>
	<xsl:template match="bold | italic | sup">
		<xsl:param name="id"/>
		<xsl:variable name="all_levels_texts"><xsl:apply-templates select="parent::node()" mode="text-only"></xsl:apply-templates></xsl:variable>
		<xsl:variable name="first_level_texts"><xsl:apply-templates select="parent::node()" mode="formatted-text"></xsl:apply-templates></xsl:variable>
		<xsl:choose>
			<xsl:when test="normalize-space($first_level_texts)=''"><xsl:apply-templates select="*|text()">
					<xsl:with-param name="id" select="$id"/>
				</xsl:apply-templates></xsl:when>
			<xsl:when test="normalize-space($all_levels_texts)=normalize-space(.)"><xsl:apply-templates select="*|text()">
					<xsl:with-param name="id" select="$id"/>
				</xsl:apply-templates></xsl:when>
			<xsl:otherwise>
				<xsl:element name="{name()}"><xsl:apply-templates select="@* | * | text()">
						<xsl:with-param name="id" select="$id"/>
					</xsl:apply-templates></xsl:element></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="source">
		<xsl:param name="id"/>
		
		<xsl:element name="{name()}">
			<xsl:apply-templates select=".//text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="anonym | isbn | glossary | term | def | response | sig |  p | sec | sub | label | subtitle | edition |  issn | corresp | ack | sig-block">
		<xsl:param name="id"/>
		
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@* | * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="app">
		<xsl:param name="id"/>
		<app-group>
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@* | * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element></app-group>
	</xsl:template>
	
	<xsl:template match="graphic">
		<xsl:choose>
			<xsl:when test="substring(@href,1,1)='?'">
				<graphic xlink:href="{substring(@href,2)}"></graphic>
			</xsl:when>
			<xsl:otherwise>
				<graphic xlink:href="{@href}"></graphic>	
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="sec/graphic"><p>
		<xsl:choose>
			<xsl:when test="substring(@href,1,1)='?'">
				<graphic xlink:href="{substring(@href,2)}"></graphic>
			</xsl:when>
			<xsl:otherwise>
				<graphic xlink:href="{@href}"></graphic>	
			</xsl:otherwise>
		</xsl:choose></p>
	</xsl:template>
	<xsl:template match="@resptp">
		<xsl:attribute name="response-type"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template>
	
	<xsl:template match="subart">
		<xsl:param name="parentid"/>
		<sub-article>
			<xsl:apply-templates select="@*">
				<xsl:with-param name="parentid" select="$parentid"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="front">
				<xsl:with-param name="language" select="@language"/>
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="body">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="back">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="docresp | response | subart">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
		</sub-article>
	</xsl:template>
	
	<xsl:template match="docresp|response">
		<xsl:param name="parentid"/>
		<response>
			<xsl:apply-templates select="@*">
				<xsl:with-param name="parentid" select="$parentid"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="front">
				<xsl:with-param name="language" select="@language"/>
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="body">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="back">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
		</response>
	</xsl:template>
	
	<xsl:template match="subdoc">
		<xsl:param name="parentid"/>
		<sub-article>
			<xsl:apply-templates select="@*">
				<xsl:with-param name="parentid" select="$parentid"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="front">
				<xsl:with-param name="language" select="@language"/>
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="body">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="back">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="docresp | subdoc">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
		</sub-article>
	</xsl:template>
	
	<xsl:template match="subart/@id | subdoc/@id">
		<xsl:attribute name="id"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template>
	
	<xsl:template match="@subarttp">
		<xsl:attribute name="article-type"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template>
	
	<xsl:template match="deflist">
		<def-list>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="sectitle|defitem|deflist"/>
		</def-list>
	</xsl:template>
	
	<xsl:template match="defitem">
		<def-item>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="term | def"/>
		</def-item>
	</xsl:template>
	<xsl:template match="def">
		<def>
			<p>
				<xsl:apply-templates select="*|text()"/>
			</p>
			
		</def>
	</xsl:template>
	
	<xsl:template match="@corresp | @deceased">
		<xsl:if test=".='yes'">
			<xsl:if test="not($fn[@fntype=name()])">
				<xsl:attribute name="{name()}">yes</xsl:attribute>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	<xsl:template match="@eqcontr">
		<xsl:if test=".='yes'">
			<xsl:if test="not($fn[@fntype='eq-contrib'])">
				<xsl:attribute name="eq-contrib">yes</xsl:attribute>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	<xsl:template match="sigblock">
		<xsl:param name="id"/>
		<sig-block>
			<xsl:apply-templates select="@*| * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</sig-block>
	</xsl:template>
	<xsl:template match="version">
		<edition>
			<xsl:value-of select="normalize-space(.)"/>
		</edition>
	</xsl:template>
	<xsl:template match="issn[contains(.,'PMID:')]">
		<pub-id pub-id-type="pmid">
			<xsl:value-of select="substring-after(., 'PMID:')"/>
		</pub-id>
	</xsl:template>
	<xsl:template match="@doctopic" mode="type">
		<xsl:attribute name="article-type">
			<xsl:choose>
				<xsl:when test=".='oa'">research-article</xsl:when>
				<xsl:when test=".='ab'">abstract</xsl:when>
				<xsl:when test=".='an'">announcement</xsl:when>
				<xsl:when test=".='co'">article-commentary</xsl:when>
				<xsl:when test=".='cr'">case-report</xsl:when>
				<xsl:when test=".='ed'">editorial</xsl:when>
				<xsl:when test=".='le'">letter</xsl:when>
				<xsl:when test=".='ra'">review-article</xsl:when>
				<xsl:when test=".='sc'">rapid-communication</xsl:when>
				<xsl:when test=".='ax'">addendum</xsl:when>
				<xsl:when test=".='rc'">book-review</xsl:when>
				<xsl:when test=".='??'">books-received</xsl:when>
				<xsl:when test=".='rn'">brief-report</xsl:when>
				<xsl:when test=".='??'">calendar</xsl:when>
				<xsl:when test=".='??'">collection</xsl:when>
				<xsl:when test=".='er'">correction</xsl:when>
				<xsl:when test=".='??'">discussion</xsl:when>
				<xsl:when test=".='??'">dissertation</xsl:when>
				<xsl:when test=".='pr'">in-brief</xsl:when>
				<xsl:when test=".='??'">introduction</xsl:when>
				<xsl:when test=".='??'">meeting-report</xsl:when>
				<xsl:when test=".='??'">news</xsl:when>
				<xsl:when test=".='??'">obituary</xsl:when>
				<xsl:when test=".='??'">oration</xsl:when>
				<xsl:when test=".='??'">partial-retraction</xsl:when>
				<xsl:when test=".='??'">product-review</xsl:when>
				<xsl:when test=".='??'">reply</xsl:when>
				<xsl:when test=".='??'">reprint</xsl:when>
				<xsl:when test=".='??'">retraction</xsl:when>
				<xsl:when test=".='??'">translation</xsl:when>
				<xsl:otherwise>research-article</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="@language">
		<xsl:if test="not(.='unknown')">
			<xsl:attribute name="xml:lang"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template match="article|text|doc" mode="dtd-version">
		<xsl:attribute name="dtd-version">3.0</xsl:attribute>
	</xsl:template>
	<xsl:template match="article|text|doc">
		<article>
					<xsl:apply-templates select="." mode="dtd-version"/>
					<xsl:apply-templates select="@doctopic" mode="type"/>
					<xsl:apply-templates select="@language"/>
					<xsl:apply-templates select="." mode="front">
						<xsl:with-param name="language" select="@language"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="body"/>
					<xsl:apply-templates select="." mode="back"/>
					<xsl:apply-templates select="response | subart"/>
					<xsl:apply-templates select="docresp | subdoc"/>
		</article>
	</xsl:template>
	<xsl:template match="article|text|response|subart|doc|subdoc|docresp" mode="front">
		<xsl:param name="language"/>
		<xsl:choose>
			<xsl:when test="name()='doc' or name()='article'">
				<front>
					<xsl:apply-templates select="." mode="journal-meta"/>
					<xsl:apply-templates select="." mode="article-meta">
						<xsl:with-param name="language" select="$language"/>
					</xsl:apply-templates>					
				</front>
			</xsl:when>
			<xsl:when test="name()='subdoc' or name()='docresp'">
				<front-stub>
					<xsl:apply-templates select="." mode="article-meta">
						<xsl:with-param name="language" select="$language"/>
					</xsl:apply-templates>										
				</front-stub>
			</xsl:when>
			<xsl:otherwise>
				<front-stub>
					<xsl:apply-templates select="front" mode="article-meta">
						<xsl:with-param name="language" select="$language"/>
					</xsl:apply-templates>										
				</front-stub>
			</xsl:otherwise>
		</xsl:choose>		
	</xsl:template>
	<xsl:template match="article|text|doc" mode="journal-meta">
		<journal-meta>
			<xsl:if test=".//nlm-title and .//nlm-title!=''">
				<journal-id journal-id-type="nlm-ta">
					<xsl:value-of select=".//nlm-title"/>
				</journal-id>
			</xsl:if>
			<xsl:if test="not(.//nlm-title) or .//nlm-title=''">
				<journal-id journal-id-type="publisher-id">
					<xsl:value-of select="$journal_acron"/>
				</journal-id>
			</xsl:if>
			<journal-title-group>
				<xsl:if test=".//journal-title!=''">
					<xsl:copy-of select=".//journal-title"/>
					<abbrev-journal-title abbrev-type="publisher">
						<xsl:value-of select="@stitle"/>
					</abbrev-journal-title>
				</xsl:if>
			</journal-title-group>
			
			<xsl:if test="..//extra-scielo/print-issn!=''">
				<issn pub-type="ppub">
					<xsl:apply-templates select="..//extra-scielo/print-issn"/>
				</issn>
			</xsl:if>
			<xsl:if test="..//extra-scielo/e-issn!=''">
				<issn pub-type="epub">
					<xsl:apply-templates select="..//extra-scielo/e-issn"/>
				</issn>
			</xsl:if>
			<xsl:if test="..//extra-scielo/publisher/publisher-name!=''">
				<publisher>
					<publisher-name>
						<xsl:apply-templates select="..//extra-scielo/publisher/publisher-name"/>
					</publisher-name>
				</publisher>
			</xsl:if>
		</journal-meta>
	</xsl:template>
	<xsl:template match="extra-scielo/publisher/publisher-name">
		<xsl:value-of select="normalize-space(.)"/>
		<xsl:if test="position()!=last()">, </xsl:if>
	</xsl:template>
	<xsl:template match="front/doi | text/doi | doc/doi">
		<article-id pub-id-type="doi">
			<xsl:value-of select="normalize-space(.)"/>
		</article-id>
	</xsl:template>

	<xsl:template match="*" mode="format-subject">
		<xsl:param name="t"/>
		<xsl:choose>
			<xsl:when test="contains($t,' ')">
				<xsl:variable name="t1" select="substring-before($t,' ')"/>
				<xsl:variable name="t2" select="substring-after($t,' ')"/>

				<xsl:value-of
					select="translate(substring($t,1,1),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
				<xsl:value-of
					select="translate(concat(substring($t1,2),' '),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
				<xsl:apply-templates select="." mode="format-subject">
					<xsl:with-param name="t" select="$t2"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of
					select="translate(substring($t,1,1),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
				<xsl:value-of
					select="translate(substring($t,2),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
				/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="toctitle">
		<article-categories>
			<subj-group subj-group-type="heading">
				<xsl:variable name="t" select="normalize-space(.)"/>
				<subject>
					<xsl:apply-templates select="." mode="format-subject">
						<xsl:with-param name="t" select="$t"/>
					</xsl:apply-templates>
				</subject>
			</subj-group>
		</article-categories>
	</xsl:template>
	<xsl:template match="*" mode="toctitle">
		<article-categories>
			<subj-group subj-group-type="heading">
				<subject>Articles</subject>
			</subj-group>
		</article-categories>
	</xsl:template>
	<xsl:template match="subart/front | subdoc | docresp" mode="article-meta">
		<xsl:param name="language"/>
		<xsl:if test="not(.//toctitle)">
			<xsl:apply-templates select="." mode="toctitle"></xsl:apply-templates>
		</xsl:if>
		<xsl:apply-templates select=".//toctitle"></xsl:apply-templates>
		<title-group>
			<xsl:apply-templates select=".//titlegrp/title|doctitle">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>
		</title-group>
		<xsl:apply-templates select="." mode="front-author"/>
		
		<xsl:apply-templates select="../xmlbody/sigblock" mode="author"></xsl:apply-templates>
		<xsl:apply-templates select=".//cltrial"></xsl:apply-templates>
		<xsl:apply-templates select=".//abstract|.//xmlabstr">
			<xsl:with-param name="language" select="$language"/>
		</xsl:apply-templates>
		<xsl:apply-templates select=".//keygrp|.//kwdgrp">
			<xsl:with-param name="language" select="$language"/>
		</xsl:apply-templates>
		
	</xsl:template>
	<xsl:template match="*" mode="front-author">
		<xsl:apply-templates select=".//authgrp" mode="front"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="cltrial">
		<uri>
			<xsl:attribute name="xlink:href"><xsl:value-of select="ctreg/@cturl"/></xsl:attribute>
			<xsl:apply-templates select=".//text()"></xsl:apply-templates>
		</uri>
	</xsl:template>
	<xsl:template match="*" mode="given-names">
		<xsl:param name="sig"></xsl:param>
		<xsl:param name="prefix"></xsl:param>
		<xsl:choose>
			<xsl:when test="contains($sig, ' ')">
				<xsl:value-of select="concat($prefix,substring-before($sig,' '))"/>
				<xsl:apply-templates select="." mode="given-names">
					<xsl:with-param name="sig"><xsl:value-of select="substring-after($sig,' ')"/></xsl:with-param>
					<xsl:with-param name="prefix"><xsl:value-of select="concat(' ','')"/></xsl:with-param>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="sigblock" mode="author">
		<contrib-group>
			<xsl:apply-templates select="sig" mode="author"></xsl:apply-templates>
		</contrib-group>
	</xsl:template>
	<xsl:template match="sig" mode="author">
		<xsl:variable name="given-names"><xsl:apply-templates select="." mode="given-names">
			<xsl:with-param name="sig" select="."/>
		</xsl:apply-templates></xsl:variable>
		<xsl:variable name="contrib_type">
			<xsl:choose><xsl:when test="contains(../text(),'ditor')">editor</xsl:when><xsl:when test="contains(../role,'ditor')">editor</xsl:when><xsl:otherwise>author</xsl:otherwise></xsl:choose>
		</xsl:variable>
		<xsl:variable name="position"><xsl:value-of select="position()"/></xsl:variable>
		<contrib contrib-type="{$contrib_type}">
			<name>
				<surname><xsl:value-of select="substring-after(.,concat($given-names, ' '))"/></surname>
				<given-names><xsl:value-of select="$given-names"/></given-names>
			</name>
		</contrib>
		<xsl:copy-of select="..//role[$position]"/>
	</xsl:template>
	
	<xsl:template match="article|text|doc" mode="article-meta">
		<xsl:param name="language"/>
		<article-meta>
			<xsl:apply-templates select="front/doi|doi"/>
			
			<xsl:variable name="fpage"><xsl:choose>
				<xsl:when test="contains(@fpage,'-')">
					<xsl:value-of select="substring-before(@fpage,'-')"/>
				</xsl:when>
				<xsl:when test="contains(@fpage,string(number(@fpage)))"><xsl:value-of select="@fpage"/></xsl:when>
				<xsl:otherwise>0</xsl:otherwise>
			</xsl:choose></xsl:variable>
			<xsl:if test="number($fpage)&lt;number(@order) or contains(@fpage,'-')">
					<!-- criar article-id (other), regra quando  -->
				<article-id pub-id-type="other"><xsl:value-of select="substring-after(string(100000 + number(@order)),'1')"/></article-id>
			</xsl:if>
			<xsl:if test="@ahppid!=''"><article-id specific-use="previous-pid"><xsl:value-of select="@ahppid"/></article-id></xsl:if>

			<xsl:apply-templates select=".//toctitle"></xsl:apply-templates>
			<xsl:if test="not(.//toctitle)">
				<xsl:apply-templates select="." mode="toctitle"></xsl:apply-templates>
			</xsl:if>
			
			<xsl:apply-templates select="." mode="article-title">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>
			<xsl:apply-templates select="xmlbody/sigblock" mode="author"></xsl:apply-templates>
			<xsl:apply-templates select="." mode="front-author"/>
			<xsl:apply-templates select="." mode="author-notes"/>

			<xsl:apply-templates select="." mode="pub-date"/>

			<xsl:apply-templates select="@volid | @issueno  | @fpage | @lpage | @elocatid"/>
			<xsl:apply-templates select=".//product" mode="article-meta"></xsl:apply-templates>
			<xsl:apply-templates select=".//cltrial"></xsl:apply-templates>
			<xsl:apply-templates select=".//hist" mode="front"/>
			<xsl:apply-templates select=".//back/licenses| cc | .//extra-scielo/license"/>
			<xsl:apply-templates select="front/related|related"/>
			<xsl:apply-templates select=".//abstract[@language=$language or not(@language)]|.//xmlabstr[@language=$language or not(@language)]"/>
			<xsl:apply-templates select=".//abstract[@language!=$language]|.//xmlabstr[@language!=$language]"
				mode="trans"/>
			<xsl:apply-templates select=".//keygrp|.//kwdgrp">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>
			<xsl:apply-templates
				select=".//front/report  | .//bibcom/report |  .//bbibcom/report | .//back/ack//report | .//ack//funding" mode="front"/>
			<xsl:apply-templates
				select=".//fngrp//report|.//fngrp//funding" mode="front">
				<xsl:with-param name="statement" select="'true'"/>
			</xsl:apply-templates>
			<xsl:apply-templates
				select=".//front/confgrp | ..//front/thesgrp | .//bibcom/confgrp | ..//bibcom/thesgrp  
				| .//bbibcom/confgrp | ..//bbibcom/thesgrp "/>
			<xsl:apply-templates
				select="confgrp | thesgrp"/>
			<xsl:apply-templates select="." mode="counts"/>
		</article-meta>
	</xsl:template>
	<xsl:template match="*" mode="article-title">
		<xsl:param name="language"/>
		<xsl:choose>
			<xsl:when test="doctitle">
				<title-group>
					<xsl:apply-templates select="doctitle[@language=$language or not(@language)] "/>
					<xsl:apply-templates select="doctitle[@language!=$language]" mode="trans-title-group"/>
				</title-group>
			</xsl:when>
			<xsl:otherwise>
				<title-group>
					<xsl:apply-templates select=".//titlegrp/title[@language=$language or not(@language)] "/>
					<xsl:apply-templates select=".//titlegrp/title[@language!=$language]" mode="trans-title-group">
						<xsl:with-param name="subtitles" select=".//titlegrp/subtitle[position()!=1]"/>
					</xsl:apply-templates>
				</title-group>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="titlegrp/title">
		<article-title>
			<xsl:apply-templates select="@language|*|text()"/>
		</article-title>
		<xsl:apply-templates select="../subtitle[1]"/>
	</xsl:template>
	<xsl:template match="doctitle">
		<article-title>
			<xsl:apply-templates select="*[name()!='subtitle'] |text()"/>
		</article-title>
		<xsl:apply-templates select="subtitle"/>
	</xsl:template>
	<xsl:template match="doctitle" mode="trans-title-group">
		<trans-title-group>
			<xsl:apply-templates select="@language"/>
			<trans-title>
			<xsl:apply-templates select="*[name()!='subtitle'] |text()"></xsl:apply-templates>
			</trans-title>
			<xsl:apply-templates select="subtitle" mode="trans-title"/>
		</trans-title-group>
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
			<xsl:if test="onbehalf">
				<on-behalf-of>
					<xsl:value-of select="onbehalf"/>
				</on-behalf-of>
			</xsl:if>
			<xsl:if test="count(..//aff)=1">
				<xsl:apply-templates select="..//aff"/>
			</xsl:if>
		</contrib-group>
		<xsl:if test="count(..//aff)&gt;1">
			<xsl:apply-templates select="..//aff"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="doc | subdoc | docresp" mode="front-author">
		<xsl:choose>
			<xsl:when test=".//aff">
				<aff content-type="USE normaff instead of aff"></aff>
			</xsl:when>
			<xsl:otherwise>
				<contrib-group>
					<xsl:apply-templates select="author|corpauth" mode="front"/>
					<xsl:if test="onbehalf">
						<on-behalf-of>
							<xsl:value-of select="onbehalf"/>
						</on-behalf-of>
					</xsl:if>
					<xsl:if test="count(normaff)=1">
						<xsl:apply-templates select="normaff"/>
					</xsl:if>
				</contrib-group>
				<xsl:if test="count(normaff)&gt;1">
					<xsl:apply-templates select="normaff"/>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="@role">
		<xsl:attribute name="contrib-type">
			<xsl:choose>
				<xsl:when test=".='nd'">author</xsl:when>
				<xsl:when test=".='ed'">editor</xsl:when>
				<xsl:when test=".='tr'">translator</xsl:when>
				<xsl:when test=".='rev'">rev</xsl:when>
				<xsl:when test=".='coord'">coordinator</xsl:when>
				<xsl:when test=".='org'">organizer</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="author/@*[.='y']">
		<xsl:if test="not($corresp)">
			<xsl:attribute name="{name()}">yes</xsl:attribute>
		</xsl:if>
	</xsl:template>

	<xsl:template match="author/@deceased[.='y']">
		<xsl:if test="not($deceased)">
			<xsl:attribute name="{name()}">yes</xsl:attribute>
		</xsl:if>
	</xsl:template>

	<xsl:template match="author/@eqcontr[.='y']">
		<xsl:if test="not($eqcontrib)">
			<xsl:attribute name="equal-contrib">yes</xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template match="author" mode="front">
		<!-- author front -->
		<xsl:variable name="author_rid" select="@rid"/>
		<contrib>
			<!-- xsl:if test="contains($corresp,.//fname) and contains($corresp,//surname)"><xsl:attribute name="corresp">yes</xsl:attribute></xsl:if> -->
			<xsl:apply-templates select="@*[name()!='rid']"/>
			<xsl:apply-templates select="."/>
			<xsl:apply-templates select=".//xref|text()"/>
		</contrib>
		<xsl:copy-of select="../..//aff[@id=$author_rid]/role"/>
	</xsl:template>

	<xsl:template match="corpauth" mode="front">
		<xsl:variable name="teste">
			<xsl:apply-templates select="./../../authgrp//text()"/>
			<xsl:apply-templates select="../text()"/>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($teste,'behalf')">
				<on-behalf-of>
					<xsl:apply-templates select="orgname | orgdiv | text()"/>
				</on-behalf-of>
			</xsl:when>
			<xsl:otherwise>
				<contrib contrib-type="author">
					<collab>
						<xsl:apply-templates select="orgname | orgdiv | text()" mode="ignore-style"/>
					</collab>
				</contrib>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="author/@rid">
		<!-- quando nao existe author/xref -->
		<!-- xref deve ser marcado -->
		<!--xsl:variable name="rid" select="normalize-space(.)"/>

		<xsl:apply-templates select="." mode="mult-rid">
			<xsl:with-param name="rid_list" select="concat($rid, ' ')"/>
		</xsl:apply-templates-->
	</xsl:template>

	<xsl:template match="author/@rid" mode="mult-rid">
		<!-- quando nao existe author/xref -->
		<!-- xref deve ser marcado -->
		<xsl:param name="rid_list"/>
		<xsl:variable name="next" select="substring-after($rid_list,' ')"/>
		<xsl:variable name="rid" select="substring-before($rid_list,' ')"/>
		<xref ref-type="aff" rid="{$rid}">

			<xsl:value-of select="$rid"/>

		</xref>
		<xsl:if test="$next!=''">
			<xsl:apply-templates select="." mode="mult-rid">
				<xsl:with-param name="rid_list" select="$next"/>
			</xsl:apply-templates>
		</xsl:if>
	</xsl:template>


	<xsl:template match="aff | normaff">
		<xsl:variable name="parentid"></xsl:variable>
		<xsl:variable name="label">
			<xsl:value-of select="normalize-space(label)"/>
			<xsl:if test="not(label)">
				<xsl:value-of select="normalize-space(sup)"/>
			</xsl:if>
		</xsl:variable>
		<aff>
			<xsl:apply-templates select="@id"/>
			<xsl:apply-templates select="label|sup"/>
			<institution content-type="original"><xsl:apply-templates select="*|text()" mode="original"></xsl:apply-templates></institution>
			<institution content-type="aff-pmc"><xsl:apply-templates select="*[name()!='label' and name()!='sup']|text()" mode="aff-pmc"/></institution>
			<xsl:choose>
				<xsl:when test="@orgname">
					<xsl:apply-templates select="@*[name()!='id']"/>
					<xsl:if test="city or state or zipcode">
						<addr-line>
							<xsl:apply-templates select="city|state|zipcode"/>
						</addr-line>
					</xsl:if>
				</xsl:when>
				<xsl:when test="@norgname">
					<xsl:apply-templates select="*[contains(name(),'org')]"/>
					<xsl:if test="city or state or zipcode">
						<addr-line>
							<xsl:apply-templates select="city|state|zipcode"/>
						</addr-line>
					</xsl:if>
				</xsl:when>
			</xsl:choose>
			<xsl:choose>
				<xsl:when test="@ncountry">
					<xsl:apply-templates select="@ncountry"></xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise><xsl:apply-templates select="country"></xsl:apply-templates></xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="email"></xsl:apply-templates>
		</aff>
	</xsl:template>
	<xsl:template match="@ncountry">
		<country><xsl:value-of select="."/></country>
	</xsl:template>
	<xsl:template match="aff/country| aff/email | normaff/country| normaff/email">
		<xsl:element name="{name()}">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="aff/label | aff/sup | normaff/label | normaff/sup">
		<xsl:choose>
			<xsl:when test="not(../label) and name()='sup'">
				<label>
					<xsl:value-of select="normalize-space(.)"/>
				</label>
			</xsl:when>
			<xsl:otherwise>
				<label>
					<xsl:value-of select="normalize-space(.)"/>
				</label>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="aff/* | normaff/*" mode="aff-pmc">
		<xsl:value-of select="text()"/>
	</xsl:template>
	
	<xsl:template match="aff/label | normaff/label" mode="aff-pmc">
	</xsl:template>
	
	<xsl:template match="aff/email | aff/country | normaff/email | normaff/country" mode="aff-pmc">
		<named-content content-type="{name()}"><xsl:value-of select="normalize-space(.)"/></named-content>
	</xsl:template>
		
	<xsl:template match="aff/text() | normaff/text()" mode="aff-pmc">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="aff/* | normaff/*" mode="original">
		<xsl:value-of select="text()"/>
	</xsl:template>
	<xsl:template match="aff/label" mode="aff-pmc">
	</xsl:template>
	
	<xsl:template match="aff/email | normaff/email" mode="original"><named-content content-type="email"><xsl:value-of select="text()"/></named-content>
	</xsl:template>
	<xsl:template match="aff//text() | normaff//text()" mode="original">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="xref[@ref-type='aff']/@rid">
		<xsl:variable name="var_id">
			<xsl:choose>
				<xsl:when test="contains(.,' ')">aff<xsl:value-of select="substring-before(.,' ')"
					/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($var_id,'a0')">aff<xsl:value-of
					select="substring-after($var_id,'a0')"/></xsl:when>
			<xsl:otherwise>aff<xsl:value-of select="substring-after($var_id,'a')"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="aff/@id | normaff/@id">
		<!-- FIXMEID -->
		<!-- quando nao ha aff/label = author/xref enquanto author/@rid = aff/@id -->
		<xsl:variable name="var_id">
			<xsl:choose>
				<xsl:when test="contains(.,' ')">aff<xsl:value-of select="substring-before(.,' ')"
					/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:attribute name="id"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if>
			<xsl:choose>
				<xsl:when test="contains($var_id,'a0')">aff<xsl:value-of
						select="substring-after($var_id,'a0')"/></xsl:when>
				<xsl:otherwise>aff<xsl:value-of select="substring-after($var_id,'a')"
					/></xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="normaff/orgname">
		<xsl:if test="../@norgname!='Not normalized'">
			<institution content-type="normalized"><xsl:value-of select="../@norgname"/></institution>
		</xsl:if>
		<institution content-type="orgname"><xsl:value-of select="."/></institution>
	</xsl:template>
	<xsl:template match="normaff/*[contains(name(),'orgdiv')]">
		<institution content-type="{name()}"><xsl:value-of select="."/></institution>
	</xsl:template>
	<xsl:template match="aff/@*[contains(name(),'org')] | aff/*[contains(name(),'org')]">
		<institution>
			<xsl:attribute name="content-type">
				<xsl:value-of select="name()"/>
			</xsl:attribute>
			<xsl:value-of select="normalize-space(.)"/>
		</institution>
	</xsl:template>

	<xsl:template match="aff/@city | aff/@state | aff/@country | aff/city | aff/state | aff/zipcode | normaff/city | normaff/state | normaff/zipcode">
		<named-content content-type="{name()}">
			<xsl:value-of select="normalize-space(.)"/>
		</named-content>
	</xsl:template>


	<xsl:template match="e-mail|email">
		<email>
			<xsl:value-of select="normalize-space(.)"/>
		</email>
	</xsl:template>

	<xsl:template match="*" mode="author-notes">
		<xsl:variable name="fnauthors">
			<xsl:apply-templates select="$fn" mode="fnauthors"/>
		</xsl:variable>
		<xsl:if test="$corresp or $fnauthors!='' ">
			<author-notes>
				<xsl:apply-templates select="$corresp"/>
				<xsl:apply-templates select="$fn" mode="fnauthors"/>
			</author-notes>
		</xsl:if>
	</xsl:template>

	<xsl:template match="fngrp" mode="fnauthors">
		<xsl:choose>
			<xsl:when
				test="contains('abbr|financial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype)"/>
			<xsl:otherwise>
				<xsl:apply-templates select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="fngrp" mode="notfnauthors">
		<xsl:choose>
			<xsl:when
				test="contains('abbr|financial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype)">
				<xsl:apply-templates select="."/>
			</xsl:when>
			<xsl:otherwise> </xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="@volid">
		<volume>
			<xsl:value-of select="normalize-space(.)"/>
		</volume>
		<xsl:if test="not(../@issueno) and ../@supplvol"><issue>Suppl<xsl:if test="../@supplvol!='0'"> <xsl:value-of select="concat(' ',../@supplvol)"/></xsl:if>
		</issue></xsl:if>
	</xsl:template>
	<xsl:template match="volid">
		<volume>
			<xsl:value-of select="normalize-space(.)"/>
		</volume>
	</xsl:template>
	<xsl:template match="part">
		<issue-part>
			<xsl:value-of select="normalize-space(.)"/>
		</issue-part>
	</xsl:template>
	<xsl:template match="@issueno ">
		<xsl:choose>
			<xsl:when test="contains(.,' Pt ')">
				<issue>
					<xsl:value-of select="substring-before(.,' Pt ')"/>
				</issue>
				<issue-part>Pt <xsl:value-of select="substring-after(.,' Pt ')"/></issue-part>
			</xsl:when>
			<xsl:when test=".='ahead'">
				<volume>00</volume>
				<issue>00</issue>
			</xsl:when>
			<xsl:otherwise>
				<issue>
					<xsl:value-of select="normalize-space(.)"/>
					<xsl:if test="../@supplno"> Suppl<xsl:if test="../@supplno!='0'"> <xsl:value-of select="concat(' ',../@supplno)"/></xsl:if></xsl:if>
					<xsl:if test="../@supplvol"> Suppl<xsl:if test="../@supplvol!='0'"> <xsl:value-of select="concat(' ',../@supplvol)"/></xsl:if></xsl:if>
				</issue>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
	<xsl:template match=" issueno">
		<xsl:choose>
			<xsl:when test="contains(.,' Pt ')">
				<issue>
					<xsl:value-of select="substring-before(.,' Pt ')"/>
				</issue>
				<issue-part>Pt <xsl:value-of select="substring-after(.,' Pt ')"/></issue-part>
			</xsl:when>
			<xsl:otherwise>
				<issue>
					<xsl:value-of select="normalize-space(.)"/>
				</issue>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
	<xsl:template match="@supplvol | @supplno"> </xsl:template>
	<xsl:template match="suppl">
		<supplement>
			<xsl:value-of select="normalize-space(.)"/>
		</supplement>
	</xsl:template>
	<xsl:template match="@fpage">
		<fpage>
			<xsl:choose>
				<xsl:when test="contains(.,'-')">
					<xsl:attribute name="seq"><xsl:value-of select="substring-after(.,'-')"/></xsl:attribute>
					<xsl:value-of select="substring-before(.,'-')"/>
				</xsl:when>
				<xsl:when test="../@fpageseq"><xsl:attribute name="seq"><xsl:value-of select="../@fpageseq"/></xsl:attribute>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
			</xsl:choose>
		</fpage>
	</xsl:template>
	<xsl:template match="@lpage">
		<lpage>
			<xsl:choose>
				<xsl:when test="contains(.,'-')">
					<xsl:attribute name="seq"><xsl:value-of select="substring-after(.,'-')"/></xsl:attribute>
					<xsl:value-of select="substring-before(.,'-')"/>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
			</xsl:choose>
		</lpage>
	</xsl:template>
	<xsl:template match="@elocatid"><elocation-id><xsl:value-of select="."/></elocation-id></xsl:template>
	<xsl:template match="fpage">
		<fpage>
			<xsl:value-of select="normalize-space(.)"/>
		</fpage>
	</xsl:template>
	<xsl:template match="lpage">
		<lpage>
			<xsl:value-of select="normalize-space(.)"/>
		</lpage>
	</xsl:template>
	<xsl:template match="pages" mode="get-fpage">
		<xsl:param name="pages"/>
		<xsl:variable name="temp">
			<xsl:choose>
				<xsl:when test="contains($pages, ';')">
					<xsl:apply-templates select="." mode="get-fpage">
						<xsl:with-param name="pages" select="substring-after($pages,';')"/>
					</xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="substring-before($pages,'-')"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:choose>
			<xsl:when test="normalize-space(translate($temp,'0123456789','          '))=''">
				<xsl:value-of select="$temp"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of
					select="normalize-space(translate($temp,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','                                              '))"
				/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="pages" mode="get-lpage">
		<xsl:param name="pages"/>
		<xsl:choose>
			<xsl:when test="contains($pages, ';')">
				<xsl:apply-templates select="." mode="get-lpage">
					<xsl:with-param name="pages" select="substring-after($pages,';')"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="substring-after($pages,'-')"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="pages">
		<!-- page-range>
			<xsl:value-of select="normalize-space(.)"/>
		</page-range> -->

		<xsl:choose>
			<xsl:when test="substring(.,1,2)='ID'">
				<elocation-id>
					<xsl:value-of select="normalize-space(.)"/>
				</elocation-id>
			</xsl:when>
			<xsl:when test="contains(.,';') or contains(.,',')">
				<xsl:variable name="pagination" select="translate(.,',',';')"/>
				<xsl:variable name="page1">
					<xsl:value-of select="substring-before(.,'-')"/>
				</xsl:variable>
				<xsl:variable name="fpage">
					<xsl:apply-templates select="." mode="get-fpage">
						<xsl:with-param name="pages" select="substring-after($pagination,';')"/>
					</xsl:apply-templates>
				</xsl:variable>
				<xsl:variable name="lpage">
					<xsl:apply-templates select="." mode="get-lpage">
						<xsl:with-param name="pages" select="substring-after($pagination,';')"/>
					</xsl:apply-templates>
				</xsl:variable>

				<fpage>
					<xsl:value-of select="$page1"/>
				</fpage>
				<lpage>
					<xsl:if test="string-length($lpage)&lt;string-length($fpage)">
						<xsl:value-of
							select="substring($fpage,1,string-length($fpage) - string-length($lpage))"
						/>
					</xsl:if>
					<xsl:value-of select="$lpage"/>
				</lpage>
				<page-range>
					<xsl:value-of select="normalize-space(.)"/>
				</page-range>
			</xsl:when>
			<xsl:when test="contains(.,'-')">
				<xsl:variable name="fpage" select="substring-before(normalize-space(.),'-')"/>
				<xsl:variable name="lpage" select="substring-after(normalize-space(.),'-')"/>

				<fpage>
					<xsl:value-of select="$fpage"/>
				</fpage>
				<lpage>
					<xsl:if test="string-length($lpage)&lt;string-length($fpage)">
						<xsl:value-of
							select="substring($fpage,1,string-length($fpage) - string-length($lpage))"
						/>
					</xsl:if>
					<xsl:value-of select="$lpage"/>
				</lpage>

			</xsl:when>
			<xsl:when test="substring(.,1,1)='e'">
				<xsl:variable name="e" select="substring-after(.,'e')"/>
				<xsl:if test="normalize-space(translate($e,'0123456789','          '))=''">
					<elocation-id>
						<xsl:value-of select="normalize-space(.)"/>
					</elocation-id>
				</xsl:if>
			</xsl:when>
			<xsl:when test="substring(.,1,1)='E'">
				<xsl:variable name="e" select="substring-after(.,'E')"/>
				<xsl:if test="normalize-space(translate($e,'0123456789','          '))=''">
					<elocation-id>
						<xsl:value-of select="normalize-space(.)"/>
					</elocation-id>
				</xsl:if>
			</xsl:when>

			<xsl:otherwise>
				<fpage>
					<xsl:value-of select="normalize-space(.)"/>
				</fpage>
				<lpage>
					<xsl:value-of select="normalize-space(.)"/>
				</lpage>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
	<xsl:template match="hist" mode="front">
		<history>
			<xsl:apply-templates select="received | revised | accepted " mode="front"/>
		</history>
	</xsl:template>
	<xsl:template match="received | revised | accepted" mode="front">
		<xsl:variable name="dtype">
			<xsl:choose>
				<xsl:when test="name()='revised'">rev-recd</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="name()"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<date date-type="{$dtype}">
			<xsl:call-template name="display_date">
				<xsl:with-param name="dateiso">
					<xsl:value-of select="@dateiso"/>
				</xsl:with-param>
			</xsl:call-template>
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
		<xsl:param name="language"/>
		<abstract xml:lang="{$language}">
			<p>
				<xsl:apply-templates/>
			</p>
		</abstract>
	</xsl:template>
	<xsl:template match="xmlabstr" mode="trans">
		<trans-abstract xml:lang="{@language}">
			<xsl:apply-templates select="*"/>
		</trans-abstract>
	</xsl:template>
	<xsl:template match="xmlabstr">
		<xsl:param name="language"/>
		<abstract xml:lang="{$language}">
			<xsl:apply-templates select="*"/>
		</abstract>
	</xsl:template>
	<xsl:template match="keygrp">
		<kwd-group xml:lang="{keyword[1]/@language}">
			<xsl:apply-templates select="keyword"/>
		</kwd-group>
	</xsl:template>
	<xsl:template match="keyword|kwd">
		<kwd>
			<xsl:apply-templates/>
		</kwd>
	</xsl:template>
	<xsl:template match="kwdgrp">
		<xsl:param name="language"/>
		<kwd-group>
			<xsl:choose>
				<xsl:when test="@language"><xsl:attribute name="xml:lang"><xsl:value-of select="@language"/></xsl:attribute></xsl:when>
				<xsl:when test="$language!=''"><xsl:attribute name="xml:lang"><xsl:value-of select="$language"/></xsl:attribute></xsl:when>
			</xsl:choose>
			<xsl:apply-templates select="kwd"/>
		</kwd-group>
	</xsl:template>
	
	<xsl:template match="*" mode="counts">
		<counts>
			<xsl:choose>
				<xsl:when test="not(@figcount)">
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'fig-count'"/>
						<xsl:with-param name="count" select="count(.//figgrp)"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'table-count'"/>
						<xsl:with-param name="count" select="count(.//tabwrap)"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'equation-count'"/>
						<xsl:with-param name="count" select="count(.//equation)"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'ref-count'"/>
						<xsl:with-param name="count"><xsl:choose>
							<xsl:when test=".//back">
								<xsl:value-of select="count(.//back//*[contains(name(),'citat')])"/>
							</xsl:when><xsl:otherwise><xsl:value-of select="count(.//ref)"/></xsl:otherwise>
						</xsl:choose></xsl:with-param>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'page-count'"/>
						<xsl:with-param name="count"><xsl:choose>
							<xsl:when test="@pagcount"><xsl:value-of select="@pagcount"/></xsl:when>
							<xsl:when test="string(number(@fpage))=@fpage and string(number(@lpage))=@lpage"><xsl:value-of select="@lpage - @fpage + 1"/></xsl:when>
							<xsl:otherwise></xsl:otherwise>
						</xsl:choose></xsl:with-param>
					</xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'fig-count'"/>
						<xsl:with-param name="count" select="@figcount"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'table-count'"/>
						<xsl:with-param name="count" select="@tabcount"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'equation-count'"/>
						<xsl:with-param name="count" select="@eqcount"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'ref-count'"/>
						<xsl:with-param name="count" select="@refcount"/>
					</xsl:apply-templates>
					<xsl:apply-templates select="." mode="element-counts">
						<xsl:with-param name="element_name" select="'page-count'"/>
						<xsl:with-param name="count" select="@pagcount"/>
					</xsl:apply-templates>
				</xsl:otherwise>
			</xsl:choose>
			
		</counts>
	</xsl:template>
	<xsl:template match="*" mode="element-counts">
		<xsl:param name="element_name"/>
		<xsl:param name="count"/>
			<xsl:element name="{$element_name}">
				<xsl:attribute name="count"><xsl:choose>
					<xsl:when test="$count=''">0</xsl:when>
					<xsl:otherwise><xsl:value-of select="$count"/></xsl:otherwise>
				</xsl:choose></xsl:attribute>
			</xsl:element>
	</xsl:template>
	<xsl:template match="@sec-type[.='nd']"> </xsl:template>
	<xsl:template match="*" mode="body">
		<body>
			<xsl:apply-templates select="xmlbody"/>
		</body>
	</xsl:template>
	<xsl:template match="subsec">
		<sec>
			<xsl:apply-templates select="@*|*|text()"/>
		</sec>
	</xsl:template>
	<xsl:template match="sectitle">
		<title>
			<xsl:apply-templates select="*|text()"/>
				<xsl:apply-templates select="following-sibling::node()[1 and name()='xref']"
				mode="xref-in-sectitle"/>
		</title>
	</xsl:template>
	<!--xsl:template match="@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template-->
	<!-- BACK -->
	<xsl:template match="article|text|subart|response" mode="back">
		<xsl:variable name="test">
			<xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"/>
		</xsl:variable>

		<xsl:if test="$test!='' or back/ack or back/fxmlbody or back/*[@standard]">
			<back>
				<xsl:apply-templates select="back"/>
			</back>
		</xsl:if>
	</xsl:template>

	<xsl:template match="doc|subdoc|docresp" mode="back">
		<xsl:if test="ack or fngrp  or refs or other or vancouv or iso690 or abnt6023 or apa or glossary or app">
			<back>
				<xsl:apply-templates select="ack"/>
				<xsl:apply-templates select="other | vancouv | iso690 | abnt6023 | apa | refs"/>
				<xsl:variable name="test">
					<xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"/>
				</xsl:variable>
				<xsl:if test="$test!=''">
					<fn-group>
						<xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"/>
					</fn-group>
				</xsl:if>
				<xsl:apply-templates select="glossary | app"></xsl:apply-templates>				
			</back>
		</xsl:if>
	</xsl:template>

	<xsl:template match="back">
		<xsl:apply-templates select="fxmlbody[@type='ack']|ack"/>
		<xsl:apply-templates select="*[@standard]"/>
		<xsl:variable name="test">
			<xsl:apply-templates select="fngrp[@fntype]" mode="notfnauthors"/>
		</xsl:variable>
		<xsl:if test="$test!=''">
			<fn-group>
				<xsl:apply-templates select="fngrp[@fntype]" mode="notfnauthors"/>
			</fn-group>
		</xsl:if>
		<xsl:apply-templates select="glossary | app"></xsl:apply-templates>				
		
	</xsl:template>

	<xsl:template match="*/fngrp[@fntype]">
		<fn>
			<xsl:apply-templates select="@*|label"/>
			<p>
				<xsl:apply-templates select="*[name()!='label']|text()"/>
			</p>
		</fn>
	</xsl:template>
	
	<xsl:template match="fngrp/@fntype">
		<xsl:attribute name="fn-type">
			<xsl:choose>
				<xsl:when test=".='author'">other</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>

	<xsl:template match="unidentified"> </xsl:template>

	<xsl:template match="fxmlbody[@type='ack']">
		<ack>
			<xsl:copy-of select="*"/>
		</ack>
	</xsl:template>

	<xsl:template match="*[contains(name(),'citat')]//bold | *[contains(name(),'citat')]//italic | ref//italic | ref//bold">
		<xsl:if test="not(contains(',. :;',text()))"><xsl:apply-templates select="text()"></xsl:apply-templates>
		</xsl:if>
	</xsl:template>
	<xsl:template
		match="*[contains(name(),'citat')]/text() | ref/text()"/>
	<xsl:template
		match="*[contains(name(),'citat')]//*[*]/text()"/>
	
	<xsl:template match="*[@standard] | refs">
		<ref-list>
			<xsl:choose>
				<xsl:when test="contains(text(),'Ref')">
					<title>
						<xsl:value-of select="text()"/>
					</title>
				</xsl:when>
				<xsl:when test="bold">
					<title>
						<xsl:value-of select="bold"/>
					</title>
				</xsl:when>
			</xsl:choose>
			<xsl:apply-templates select="*[contains(name(),'citat')]|ref"/>
		</ref-list>
	</xsl:template>

	<xsl:template match="xref[@ref-type='bibr']/@rid">
		<xsl:variable name="rid">
		<xsl:choose>
			<xsl:when test="contains(., 'mkp_ref_')"><xsl:value-of
						select="substring-before(substring-after(.,'mkp_ref_'),'_')"
					/></xsl:when>
			<xsl:otherwise><xsl:value-of select="substring(.,2)"/></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<xsl:variable name="zeros"><xsl:value-of select="substring('0000000000',1, $reflen - string-length($rid))"/></xsl:variable>
		<xsl:variable name="id">B<xsl:value-of select="$zeros"/><xsl:value-of select="$rid"/></xsl:variable>
		<xsl:attribute name="rid"><xsl:value-of select="$id"/></xsl:attribute>
	</xsl:template>

	<xsl:template match="*[@standard]/*[contains(name(),'citat')]">
		<xsl:variable name="zeros"><xsl:value-of select="substring('0000000000',1, $reflen - string-length(position()))"/></xsl:variable>
		<xsl:variable name="id"><xsl:value-of select="$zeros"/><xsl:value-of select="position()"/></xsl:variable>
		<ref id="B{$id}">
			<xsl:apply-templates select="no"/>
			<!-- book, communication, letter, review, conf-proc, journal, list, patent, thesis, discussion, report, standard, and working-paper.  -->
			<xsl:variable name="type">
				<xsl:choose>
					<xsl:when test="viserial or aiserial or oiserial or iiserial or piserial"
						>journal</xsl:when>
					<xsl:when test=".//confgrp">conf-proc</xsl:when>
					<xsl:when
						test=".//degree or contains(.//text(),'Master') or contains(.//text(),'Dissert')"
						>thesis</xsl:when>
					<xsl:when test=".//patgrp or contains(.//text(), 'atent')">patent</xsl:when>
					<xsl:when
						test=".//report or contains(.//text(), 'Report') or contains(.//text(), 'Informe ') or (contains(.//text(), 'Relat') and contains(.//text(), 'rio '))"
						>report</xsl:when>
					<xsl:when test=".//version">software</xsl:when>
					<xsl:when test=".//url and .//cited and not (.//pages or .//extent)"
						>web</xsl:when>
					<xsl:when test="vmonog or amonog or omonog or imonog or pmonog">book</xsl:when>
					<xsl:otherwise>other</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<xsl:apply-templates select="." mode="text-ref"/>
			<element-citation publication-type="{$type}">
				<xsl:apply-templates select="*[name()!='no' and name()!='text-ref']">
					<xsl:with-param name="position" select="position()"/>
				</xsl:apply-templates>
			</element-citation>
		</ref>
	</xsl:template>
	<xsl:template match="ref">
		<xsl:variable name="zeros"><xsl:value-of select="substring('0000000000',1, $reflen - string-length(position()))"/></xsl:variable>
		<xsl:variable name="id"><xsl:value-of select="$zeros"/><xsl:value-of select="position()"/></xsl:variable>
		<ref id="B{$id}">
			<xsl:apply-templates select="label"/>
			
			<xsl:apply-templates select="." mode="text-ref"/>
			<element-citation publication-type="{@reftype}">
				<xsl:apply-templates select="*[name()!='no' and name()!='text-ref']">
					<xsl:with-param name="position" select="position()"/>
				</xsl:apply-templates>
			</element-citation>
		</ref>
	</xsl:template>
	<xsl:template match="authors">
		<xsl:variable name="type">
			<xsl:choose>
				<xsl:when test="@role='org'">compiler</xsl:when>
				<xsl:when test="@role='ed'">editor</xsl:when>
				<xsl:when test="@role='nd'">author</xsl:when>
				<xsl:when test="@role='tr'">translator</xsl:when>
				<xsl:otherwise>author</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<person-group person-group-type="{$type}">
			<xsl:apply-templates select=".//pauthor|.//cauthor|et-al"></xsl:apply-templates>
		</person-group>
	</xsl:template>
	<xsl:template match="cauthor">
		<collab>
			<xsl:value-of select="."/>
		</collab>
	</xsl:template>
	<xsl:template match="doctit">
		<xsl:choose>
			<xsl:when test="not(../source)">
				<source><xsl:apply-templates select=".//text()"/></source>
			</xsl:when>
			<xsl:when test="../@reftype='book'">
				<chapter-title><xsl:apply-templates select=".//text()"/></chapter-title>
			</xsl:when>
			<xsl:otherwise><article-title><xsl:apply-templates select=".//text()"/></article-title></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="arttitle">
		<article-title><xsl:apply-templates select=".//text()"/></article-title>
	</xsl:template>
	<xsl:template match="chptitle">
		<chapter-title><xsl:apply-templates select=".//text()"/></chapter-title>
	</xsl:template>
	<xsl:template match="reportid">
		<!-- <pub-id pub-id-type="other">Report No.: HETA2000-0139-2824</pub-id> -->
		<pub-id pub-id-type="other"><xsl:value-of select="."/></pub-id>
	</xsl:template>
	<xsl:template match="patentno">
		<patent country="{@country}"><xsl:value-of select="."/></patent>
	</xsl:template>
	<xsl:template match="letterto">
		<source><xsl:value-of select="."/></source>
	</xsl:template>
	<xsl:template match="found-at|moreinfo">
		<comment><xsl:value-of select="."/></comment>
	</xsl:template>
	<xsl:template match="ref/contract">
		<comment content-type="award-id"><xsl:value-of select="."/></comment>
	</xsl:template>
	<xsl:template match="ref/date"></xsl:template>
	<xsl:template match="back//no">
		<label>
			<xsl:value-of select="normalize-space(.)"/>
		</label>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//country | ref/country">
		<xsl:choose>
			<xsl:when test="../city"> </xsl:when>
			<xsl:when test="../state"> </xsl:when>
			<xsl:otherwise>
				<publisher-loc>
					<xsl:value-of select="normalize-space(.)"/>
				</publisher-loc>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//city | ref/city">
		<publisher-loc>
			<xsl:value-of select="normalize-space(.)"/>
			<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
			<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</publisher-loc>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//state | ref/state">
		<xsl:choose>
			<xsl:when test="../city"> </xsl:when>
			<xsl:otherwise>
				<publisher-loc>
					<xsl:value-of select="normalize-space(.)"/>
					<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
				</publisher-loc>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="*[contains(name(),'monog')]">
		<xsl:variable name="type">
			<xsl:choose>
				<xsl:when test=".//node()[@role='org']">compiler</xsl:when>
				<xsl:when test=".//node()[@role='ed']">editor</xsl:when>
				<xsl:when test=".//node()[@role='nd']">author</xsl:when>
				<xsl:when test=".//node()[@role='tr']">translator</xsl:when>
				<xsl:otherwise>author</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test=".//*[fname] or .//*[contains(name(),'corpaut') or .//anonym]">
			<person-group person-group-type="{$type}">
				<xsl:apply-templates
					select=".//*[fname] | .//*[contains(name(),'corpaut')] | .//et-al | .//anonym"
				> </xsl:apply-templates>
			</person-group>
		</xsl:if>
		<xsl:apply-templates select="*[not(fname) and not(contains(name(),'corpaut'))]"/>
	</xsl:template>
	<xsl:template match="*[contains(name(),'corpaut')]">
		<collab>
			<xsl:apply-templates select="orgname|orgdiv|text()"/>
		</collab>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//pubname | ref/pubname">
		<publisher-name>
			<xsl:value-of select="normalize-space(.)"/>
		</publisher-name>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//orgdiv"> </xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//orgname">
		<publisher-name>
			<xsl:if test="../orgdiv">
				<xsl:value-of select="../orgdiv"/>, </xsl:if>
			<xsl:value-of select="normalize-space(.)"/>
		</publisher-name>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//*[contains(name(),'corpaut')]/text()">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	<xsl:template
		match="*[contains(name(),'citat')]//*[contains(name(),'corpaut')]/orgdiv|back//*[contains(name(),'corpaut')]/orgname">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	<xsl:template match="*[fname or surname]">
		<name>
			<xsl:choose>
				<xsl:when test="contains(surname,' ')">
					<xsl:choose>
						<xsl:when
							test="contains(surname,' Jr') or contains(surname,' Sr') or contains(surname,'nior')">
							<surname>
								<xsl:value-of select="substring-before(surname,' ')"/>
							</surname>

						</xsl:when>
						<xsl:when test="contains(surname,' Neto')">
							<surname>
								<xsl:value-of select="substring-before(surname,' Neto')"/>
							</surname>

						</xsl:when>
						<xsl:when test="contains(surname,' Filho')">
							<surname>
								<xsl:value-of select="substring-before(surname,' Filho')"/>
							</surname>

						</xsl:when>
						<xsl:when test="contains(surname,' Sobrinho')">
							<surname>
								<xsl:value-of select="substring-before(surname,' Sobrinho')"/>
							</surname>

						</xsl:when>
						<xsl:otherwise>
							<xsl:apply-templates select="surname"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="surname"/>
				</xsl:otherwise>
			</xsl:choose>

			<xsl:apply-templates select="fname"/>

			<xsl:if test="contains(surname,' ')">
				<xsl:choose>
					<xsl:when
						test="contains(surname,' Jr') or contains(surname,' Sr') or contains(surname,'nior')">

						<suffix>
							<xsl:value-of select="substring-after(surname,' ')"/>
						</suffix>
					</xsl:when>
					<xsl:when test="contains(surname,' Neto')">

						<suffix>Neto</suffix>
					</xsl:when>
					<xsl:when test="contains(surname,' Filho')">

						<suffix>Filho</suffix>
					</xsl:when>
					<xsl:when test="contains(surname,' Sobrinho')">

						<suffix>Sobrinho</suffix>
					</xsl:when>
					<xsl:otherwise> </xsl:otherwise>
				</xsl:choose>

			</xsl:if>

		</name>

	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//*[previous]">
		<xsl:param name="position"/>
		<xsl:apply-templates select="." mode="try-previous">
			<xsl:with-param name="position" select="$position - 1"/>
		</xsl:apply-templates>
	</xsl:template>

	<xsl:template match="*" mode="try-previous">
		<xsl:param name="position"/>
		<xsl:if test="$position&gt;0">
			<xsl:apply-templates
				select="$data4previous[$position]//*[surname or (contains(name(),'corpaut') and orgname)]">
				<xsl:with-param name="position" select="$position"/>
			</xsl:apply-templates>
			<xsl:if test="$position&gt;1">
				<xsl:if
					test="not($data4previous[$position]//*[surname or (contains(name(),'corpaut') and orgname)])">
					<xsl:apply-templates select="$data4previous" mode="try-previous">
						<xsl:with-param name="position" select="$position - 1"/>
					</xsl:apply-templates>
				</xsl:if>
			</xsl:if>
		</xsl:if>
	</xsl:template>

	<xsl:template match="back//date | doc//date">
		<xsl:call-template name="display_date">
			<xsl:with-param name="dateiso">
				<xsl:value-of select="@dateiso"/>
			</xsl:with-param>
			<xsl:with-param name="date">
				<xsl:value-of select="normalize-space(.)"/>
			</xsl:with-param>
			<xsl:with-param name="specyear"><xsl:value-of select="@specyear"/></xsl:with-param>
			<xsl:with-param name="format">textual</xsl:with-param>
		</xsl:call-template>
	</xsl:template>

	<xsl:template match="*[contains(name(),'citat')]//cited | ref/cited">
		<date-in-citation content-type="access-date">
			<xsl:value-of select="normalize-space(.)"/>
		</date-in-citation>
	</xsl:template>

	<xsl:template match="*[contains(name(),'contrib')]">
		<xsl:param name="position"/>
		<xsl:if test=".//fname or .//surname or .//orgname or .//anonym">
			<person-group person-group-type="author">
				<xsl:apply-templates select="*[contains(name(),'aut')]|et-al | .//anonym">
					<xsl:with-param name="position" select="$position"/>
				</xsl:apply-templates>
			</person-group>
		</xsl:if>
		<xsl:apply-templates select=".//title | .//date| .//pages "/>
	</xsl:template>

	<xsl:template match="*[contains(name(),'serial')]">
		<xsl:apply-templates/>
	</xsl:template>
    <xsl:template match="url">
    	
		<xsl:choose>
			<xsl:when test="../cited">
				<xsl:variable name="text">
					<xsl:apply-templates select="..//text()" mode="text-only"/>
				</xsl:variable>
				<xsl:variable name="term"><xsl:choose>
					<xsl:when test="contains($text,'Dispon')">Dispon</xsl:when><xsl:otherwise>Available</xsl:otherwise>
				</xsl:choose></xsl:variable>
				<xsl:variable name="comment">
					<xsl:value-of select="substring-before(substring-after($text, substring-before($text, $term)),.)"/>
				</xsl:variable>
				
				<comment content-type="cited">
					<xsl:choose>
						<xsl:when test="contains($comment, '&lt;')"><xsl:value-of select="substring-before($comment,'&lt;')"/></xsl:when>
					<xsl:otherwise><xsl:value-of select="$comment"/></xsl:otherwise>
			
					</xsl:choose>
					<ext-link ext-link-type="uri">
						<xsl:attribute name="xlink:href"><xsl:choose>
							<xsl:when test="@href"><xsl:value-of select="@href"/></xsl:when>
							<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
						</xsl:choose>
						</xsl:attribute>
						<xsl:apply-templates/>
					</ext-link>
				</comment>
			</xsl:when>
			<xsl:otherwise>
				<ext-link ext-link-type="uri">
					<xsl:attribute name="xlink:href"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
					<xsl:apply-templates/>
				</ext-link>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="uri">
		<ext-link ext-link-type="uri">
			<xsl:attribute name="xlink:href"><xsl:value-of select="@href"/></xsl:attribute>
			<xsl:apply-templates/>
		</ext-link>
	</xsl:template>

	<xsl:template match="*[contains(name(),'citat')]| ref" mode="text-ref">
		<mixed-citation>
			<xsl:choose>
				<xsl:when test="text-ref">
					<xsl:apply-templates select="text-ref"></xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="." mode="create-text-ref"/>
				</xsl:otherwise>
			</xsl:choose>
		</mixed-citation>
	</xsl:template>

	<xsl:template match="*" mode="create-text-ref">
		<xsl:apply-templates select=" * | text() " mode="create-text-ref"/>
	</xsl:template>

	<xsl:template match="@*" mode="create-text-ref"/>

	<xsl:template match="text()" mode="create-text-ref">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>

	<xsl:template match="uri[contains(@href,'mailto:')]">
		<email>
			<xsl:apply-templates select=".//text()"/>
		</email>
	</xsl:template>


	<xsl:template match="figgrps[not(label)]">
		<!-- FIXMEID -->
		<xsl:variable name="parentid"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if></xsl:variable>
		<fig-group id="{concat($parentid,@id)}">
			<xsl:apply-templates select="caption"/>
			<xsl:apply-templates select=".//figgrp"/>
		</fig-group>
	</xsl:template>

	<xsl:template match="figgrps[label]">
		<!-- FIXMEID -->
		<xsl:variable name="parentid"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if></xsl:variable>
	
	<fig id="{concat($parentid,@id)}">
			<xsl:apply-templates select="label"/>
			<xsl:apply-templates select="caption"/>
			<xsl:apply-templates select=".//figgrp"/>
		</fig>
	</xsl:template>

	<xsl:template match="figgrp">
		<p>
			<!-- FIXMEID -->
			<xsl:variable name="parentid"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if></xsl:variable>
			
			<fig id="{concat($parentid,@id)}">
				<xsl:if test="@ftype!='other'">
					<xsl:attribute name="fig-type">
						<xsl:value-of select="@ftype"/>
					</xsl:attribute>
				</xsl:if>
				<xsl:apply-templates select=".//label"/>
				<xsl:apply-templates select=".//caption"/>
				<xsl:apply-templates select="." mode="graphic"/>
			</fig>
		</p>
	</xsl:template>

	<xsl:template match="*[name()!='tabwrap']/table">
		<p>
			<xsl:apply-templates select="@*| * | text()" mode="tableless"/>
		</p>
	</xsl:template>

	<xsl:template match="p/figgrp|figgrps/figgrp">
		<!-- FIXMEID -->
		<xsl:variable name="parentid"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if></xsl:variable>
		
		<fig id="{concat($parentid,@id)}">
			<xsl:if test="@ftype!='other'">
				<xsl:attribute name="fig-type">
					<xsl:value-of select="@ftype"/>
				</xsl:attribute>
			</xsl:if>
			<xsl:apply-templates select=".//label"/>
			<xsl:apply-templates select=".//caption"/>
			<xsl:apply-templates select="." mode="graphic"/>
		</fig>
	</xsl:template>

	<xsl:template match="tabwrap">
		<p><!-- FIXMEID -->
			<xsl:variable name="parentid"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if></xsl:variable>
			
			<table-wrap id="{concat($parentid,@id)}">
				<xsl:apply-templates select="label"/>
				<xsl:apply-templates select=".//caption"/>
				<xsl:apply-templates select="." mode="graphic"/>
				<xsl:apply-templates select="." mode="notes"/>

				<!-- xsl:if test=".//notes">
				<table-wrap-foot>
					<fn><p><xsl:value-of select=".//notes"/></p></fn>
					
				</table-wrap-foot>
				</xsl:if> -->
			</table-wrap>
		</p>
	</xsl:template>

	<xsl:template match="tabwrap//fntable" mode="table">
		<xsl:param name="table_id"/>
		<!-- FIXMEID -->
		<xsl:variable name="parentid"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if></xsl:variable>
		
		<fn id="{$parentid}{translate(@id,'tfn','TFN')}">
			<xsl:apply-templates select="label"/>
			<p>
				<xsl:apply-templates select="text()|*[name()!='label']"/>
			</p>
		</fn>
	</xsl:template>

	<xsl:template match="tabwrap" mode="notes">
		<xsl:if test=".//fntable">
			<table-wrap-foot>
				<xsl:apply-templates select=".//fntable" mode="table">
					<xsl:with-param name="table_id" select="@id"/>
				</xsl:apply-templates>
			</table-wrap-foot>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="p/tabwrap">
		<!-- FIXMEID -->
		<xsl:variable name="parentid"><xsl:if test="ancestor::node()[name()='subart']"><xsl:value-of select="ancestor::node()[name()='subart']/@id"/></xsl:if></xsl:variable>
		
		<table-wrap id="{$parentid}{@id}">
			<xsl:apply-templates select=".//label"/>
			<xsl:apply-templates select=".//caption"/>
			<xsl:apply-templates select="." mode="graphic"/>
			<xsl:apply-templates select="." mode="notes"/>
		</table-wrap>
	</xsl:template>

    <xsl:template match="*[contains(name(),'citat')]//*[contains(name(),'contrib')]//title">
		<xsl:variable name="title">
			<xsl:apply-templates select="*|text()"/>
			<xsl:apply-templates select="../subtitle" mode="title"/>
		</xsl:variable>
		<xsl:variable name="t" select="normalize-space($title)"/>
		<xsl:choose>
			<xsl:when test="../../node()[contains(name(),'monog')] or ../../vmonog">
				<chapter-title>
					<xsl:apply-templates select="@language"></xsl:apply-templates>
					<xsl:apply-templates select="*|text()"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
				</chapter-title>
			</xsl:when>
			<xsl:when
				test="substring($t,1,1)='[' and (substring(.,string-length($t),1)=']' or substring(.,string-length($t)-1,2)='].')">
				<trans-title>
					<xsl:apply-templates select="@language"/>
					<xsl:value-of select="translate(translate($t,'[',''),']','')"/>

				</trans-title>
			</xsl:when>
			<xsl:otherwise>
				<article-title>
					<xsl:apply-templates select="@language"/>
					<xsl:apply-templates select="*|text()"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
				</article-title>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!--  xsl:template match="*[contains(name(),'citat')]//title/*">
	<xsl:comment>*[contains(name(),'citat')]//title/*,<xsl:value-of select="name()"/></xsl:comment>
			
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>-->
	<xsl:template match="*[contains(name(),'citat')]//title/text()">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	
	<xsl:template match="*[contains(name(),'monog')]//title">
		<xsl:variable name="lang">
			<xsl:choose>
				<xsl:when test="../vtitle">
					<xsl:value-of select="../../..//title[@language]/@language"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="../..//title[@language]/@language"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<source xml:lang="{$lang}"><xsl:apply-templates select="*|text()"/></source>
	</xsl:template>
	
	<xsl:template match="sertitle | stitle | vstitle/stitle">
		<xsl:variable name="first_level_texts"><xsl:apply-templates select="." mode="formatted-text"></xsl:apply-templates></xsl:variable>
		
		<source><xsl:choose>
			<xsl:when test="normalize-space($first_level_texts)=''"><xsl:apply-templates select="*"></xsl:apply-templates></xsl:when>
			<xsl:when test="not(*)"><xsl:value-of select="normalize-space(.)"/></xsl:when>
			<xsl:otherwise><xsl:apply-templates select="*|text()"></xsl:apply-templates></xsl:otherwise>
		</xsl:choose></source>
	</xsl:template>
	
	<xsl:template match="sertitle/text() | stitle/text()"><xsl:value-of select="."/></xsl:template>
	
	<xsl:template match="*[contains(name(),'citat')]//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle"/>
	<xsl:template match="*[contains(name(),'citat')]//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle"
		mode="title">
		<xsl:variable name="texts">
			<xsl:choose>
				<xsl:when test="../../vtitle">
					<xsl:value-of select="../../../text-ref/text()"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="..//text()"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:value-of select="substring(substring-after($texts,../title),1,2)"/>
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>

	<xsl:template match="*" mode="identify-ids">
		<xsl:param name="first_str"/>
		<xsl:param name="second_str"/>
		<xsl:param name="third_str"/>
		<xsl:param name="first_name"/>
		<xsl:param name="second_name"/>
		<xsl:param name="third_name"/>
		<xsl:param name="extra_str"/>
		<xsl:param name="extra_name"/>

		<xsl:variable name="first"
			select="normalize-space(substring-before($first_str,$second_name))"/>
		<xsl:variable name="sep" select="substring($first,string-length($first),1)"/>
		<xsl:variable name="fixed_first">
			<xsl:choose>
				<xsl:when test="contains('.,;',$sep)">
					<xsl:value-of select="substring($first,1,string-length($first)-1)"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$first"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:variable name="second">
			<xsl:choose>
				<xsl:when test="$third_name!=''">
					<xsl:value-of
						select="normalize-space(substring-before($second_str,$third_name))"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$second_str"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="sep2" select="substring($second,string-length($second),1)"/>
		<xsl:variable name="fixed_second">
			<xsl:choose>
				<xsl:when test="contains('.,;',$sep2)">
					<xsl:value-of select="substring($second,1,string-length($second)-1)"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$second"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:if test="$extra_name!=''">
			<xsl:variable name="extra"
				select="normalize-space(substring-before($extra_str,concat($first_name,':')))"/>
			<xsl:variable name="sep4" select="substring($extra,string-length($extra),1)"/>
			<xsl:variable name="fixed_extra">
				<xsl:choose>
					<xsl:when test="contains('.,;',$sep4)">
						<xsl:value-of select="substring($extra,1,string-length($extra)-1)"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$extra"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<pub-id pub-id-type="{$extra_name}">
				<xsl:value-of select="$fixed_extra"/>
			</pub-id>
		</xsl:if>

		<pub-id pub-id-type="{$first_name}">
			<xsl:value-of select="$fixed_first"/>
		</pub-id>
		<pub-id pub-id-type="{$second_name}">
			<xsl:value-of select="$fixed_second"/>
		</pub-id>

		<xsl:if test="$third_name!=''">
			<xsl:variable name="third" select="normalize-space($third_str)"/>
			<xsl:variable name="sep3" select="substring($third,string-length($third),1)"/>
			<xsl:variable name="fixed_third">
				<xsl:choose>
					<xsl:when test="contains('.,;',$sep3)">
						<xsl:value-of select="substring($third,1,string-length($third)-1)"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$third"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<pub-id pub-id-type="{$third_name}">
				<xsl:value-of select="$fixed_third"/>
			</pub-id>
		</xsl:if>
	</xsl:template>

	<xsl:template match="*" mode="identify-two-ids">
		<xsl:param name="e1"/>
		<xsl:param name="e2"/>
		<xsl:param name="e1_name"/>
		<xsl:param name="e2_name"/>
		<xsl:param name="first"/>
		<xsl:param name="first_name"/>

		<xsl:variable name="maior">
			<xsl:choose>
				<xsl:when test="string-length($e1) &gt; string-length($e2)">
					<xsl:value-of select="$e1_name"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$e2_name"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="$maior=$e1_name">
				<xsl:apply-templates select="." mode="identify-ids">
					<xsl:with-param name="first_str" select="$e1"/>
					<xsl:with-param name="second_str" select="$e2"/>
					<xsl:with-param name="first_name" select="$e1_name"/>
					<xsl:with-param name="second_name" select="$e2_name"/>
					<xsl:with-param name="extra_str" select="$first"/>
					<xsl:with-param name="extra_name" select="$first_name"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:when test="$maior=$e2_name">
				<xsl:apply-templates select="." mode="identify-ids">
					<xsl:with-param name="first_str" select="$e2"/>
					<xsl:with-param name="second_str" select="$e1"/>
					<xsl:with-param name="first_name" select="$e2_name"/>
					<xsl:with-param name="second_name" select="$e1_name"/>
					<xsl:with-param name="extra_str" select="$first"/>
					<xsl:with-param name="extra_name" select="$first_name"/>
				</xsl:apply-templates>
			</xsl:when>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="othinfo | vmonog/text() | notes ">
		<xsl:variable name="lowercase"
			select="translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
		<!-- doi,pmid,pmcid -->
		<xsl:variable name="has">
			<xsl:choose>
				<xsl:when test="contains($lowercase,'doi:')">1</xsl:when>
				<xsl:otherwise>0</xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
				<xsl:when test="contains($lowercase,'pmid:')">1</xsl:when>
				<xsl:otherwise>0</xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
				<xsl:when test="contains($lowercase,'pmcid:')">1</xsl:when>
				<xsl:otherwise>0</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:variable name="b_pmcid" select="normalize-space(substring-before($lowercase,'pmcid'))"/>
		<xsl:variable name="b_pmid" select="normalize-space(substring-before($lowercase,'pmid'))"/>
		<xsl:variable name="a_pmcid" select="normalize-space(substring-after($lowercase,'pmcid:'))"/>
		<xsl:variable name="a_pmid" select="normalize-space(substring-after($lowercase,'pmid:'))"/>
		<xsl:variable name="b_doi" select="normalize-space(substring-before($lowercase,'doi'))"/>
		<xsl:variable name="a_doi" select="normalize-space(substring-after($lowercase,'doi:'))"/>

		<xsl:choose>
			<xsl:when test="$has='000'">
				<comment>
					<xsl:value-of select="normalize-space(.)"/>
				</comment>
			</xsl:when>
			<xsl:when test="$has='001'">
				<pub-id pub-id-type="pmcid">
					<xsl:value-of
						select="normalize-space(translate(substring-after($lowercase, 'pmcid:'),'.',''))"
					/>
				</pub-id>
			</xsl:when>
			<xsl:when test="$has='010'">
				<pub-id pub-id-type="pmid">
					<xsl:value-of
						select="normalize-space(translate(substring-after($lowercase, 'pmid:'),'.',''))"
					/>
				</pub-id>
			</xsl:when>
			<xsl:when test="$has='100'">
				<xsl:variable name="doi">
					<xsl:value-of select="normalize-space(substring-after($lowercase, 'doi:'))"/>
				</xsl:variable>
				<xsl:variable name="fixed_doi">
					<xsl:choose>
						<xsl:when
							test="substring($doi,string-length($doi),1)='.' or substring($doi,string-length($doi),1)=',' or substring($doi,string-length($doi),1)=';' ">
							<xsl:value-of select="substring($doi,1,string-length($doi)-1)"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="$doi"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:variable>
				<pub-id pub-id-type="doi">
					<xsl:value-of select="$fixed_doi"/>
				</pub-id>
			</xsl:when>
			<xsl:when test="$has='011'">
				<!-- pmcid / pmid -->
				<xsl:apply-templates select="." mode="identify-two-ids">
					<xsl:with-param name="e1" select="$a_pmcid"/>
					<xsl:with-param name="e2" select="$a_pmid"/>
					<xsl:with-param name="e1_name" select="'pmcid'"/>
					<xsl:with-param name="e2_name" select="'pmid'"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:when test="$has='101'">
				<!-- pmcid / doi -->
				<xsl:apply-templates select="." mode="identify-two-ids">
					<xsl:with-param name="e1" select="$a_pmcid"/>
					<xsl:with-param name="e2" select="$a_doi"/>
					<xsl:with-param name="e1_name" select="'pmcid'"/>
					<xsl:with-param name="e2_name" select="'doi'"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:when test="$has='110'">
				<!-- pmcid / doi -->
				<xsl:apply-templates select="." mode="identify-two-ids">
					<xsl:with-param name="e1" select="$a_pmid"/>
					<xsl:with-param name="e2" select="$a_doi"/>
					<xsl:with-param name="e1_name" select="'pmid'"/>
					<xsl:with-param name="e2_name" select="'doi'"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:when test="$has='111'">
				<xsl:variable name="first">
					<xsl:choose>
						<xsl:when test="$b_doi=''">
							<xsl:value-of select="$a_doi"/>
						</xsl:when>
						<xsl:when test="$b_pmid=''">
							<xsl:value-of select="$a_pmid"/>
						</xsl:when>
						<xsl:when test="$b_pmcid=''">
							<xsl:value-of select="$a_pmcid"/>
						</xsl:when>
					</xsl:choose>
				</xsl:variable>

				<xsl:variable name="first_name">
					<xsl:choose>
						<xsl:when test="$b_doi=''">doi</xsl:when>
						<xsl:when test="$b_pmid=''">pmid</xsl:when>
						<xsl:when test="$b_pmcid=''">pmcid</xsl:when>
					</xsl:choose>
				</xsl:variable>

				<xsl:choose>
					<xsl:when test="$first_name='doi'">
						<!-- doi,?,? -->

						<xsl:apply-templates select="." mode="identify-two-ids">
							<xsl:with-param name="e1" select="$a_pmid"/>
							<xsl:with-param name="e2" select="$a_pmcid"/>
							<xsl:with-param name="e1_name" select="'pmid'"/>
							<xsl:with-param name="e2_name" select="'pmcid'"/>
							<xsl:with-param name="first" select="$first"/>
							<xsl:with-param name="first_name" select="$first_name"/>
						</xsl:apply-templates>
					</xsl:when>
					<xsl:when test="$first_name='pmid'">
						<!-- pmid,?,? -->
						<xsl:apply-templates select="." mode="identify-two-ids">
							<xsl:with-param name="e1" select="$a_doi"/>
							<xsl:with-param name="e2" select="$a_pmcid"/>
							<xsl:with-param name="e1_name" select="'doi'"/>
							<xsl:with-param name="e2_name" select="'pmcid'"/>
							<xsl:with-param name="first" select="$first"/>
							<xsl:with-param name="first_name" select="$first_name"/>
						</xsl:apply-templates>
					</xsl:when>
					<xsl:when test="$first_name='pmcid'">
						<!-- pmcid,?,? -->
						<xsl:apply-templates select="." mode="identify-two-ids">
							<xsl:with-param name="e1" select="$a_doi"/>
							<xsl:with-param name="e2" select="$a_pmid"/>
							<xsl:with-param name="e1_name" select="'doi'"/>
							<xsl:with-param name="e2_name" select="'pmid'"/>
							<xsl:with-param name="first" select="$first"/>
							<xsl:with-param name="first_name" select="$first_name"/>
						</xsl:apply-templates>
					</xsl:when>
				</xsl:choose>
			</xsl:when>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="xref[@rid!=''] | author//sup">
		<xsl:variable name="rid" select="@rid"/>

		<xsl:choose>
			<xsl:when test="@ref-type='bibr'">
				<xref>
					<xsl:apply-templates select="@*"/>
					<xsl:apply-templates select="*|text()"/>
				</xref>

			</xsl:when>
			<xsl:when test="name()='sup'">
				<xsl:variable name="label" select="normalize-space(.)"/>
				<xsl:choose>
					<xsl:when
						test="$affs[normalize-space(label)=$label or normalize-space(.//sup//text())=$label]">
						<!-- sup = aff -->
						<xref ref-type="aff">
							<xsl:attribute name="rid">AFF<xsl:value-of select="$label"
								/></xsl:attribute>
							<sup>
								<xsl:value-of select="$label"/>
							</sup>
						</xref>
					</xsl:when>
					<xsl:otherwise>
						<xref>
							<sup>
								<xsl:value-of select="$label"/>
							</sup>
						</xref>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="@ref-type='aff'">
				<xsl:variable name="label" select="normalize-space(.)"/>
				<xref ref-type="aff">
					<!--xsl:choose>
						<xsl:when
							test="$affs[normalize-space(label)=$label or normalize-space(.//sup//text())=$label]">
							<xsl:attribute name="rid">AFF<xsl:value-of select="$label"
								/></xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="rid">
								<xsl:value-of select="translate(@rid, 'a', 'A')"/>
							</xsl:attribute>
						</xsl:otherwise>
					</xsl:choose-->
					<xsl:attribute name="rid">
						<xsl:apply-templates select="@rid"/>
					</xsl:attribute>
					<sup>
						<xsl:value-of select="$label"/>
					</sup>
				</xref>
			</xsl:when>
			<xsl:when test="$xref_id[@id=$rid]">
				<xref>
					<xsl:apply-templates select="@*"/>
					<xsl:apply-templates select="*[name()!='graphic']|text()" mode="ignore-style"/>
				</xref>
				<xsl:if test="graphic">
					<graphic>
						<xsl:apply-templates select="graphic/@*|graphic/*|graphic/text()"/>
						<uri>#<xsl:value-of select="@rid"/>
						</uri>
					</graphic>
				</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="*[@id]" mode="display-id">
		<xsl:value-of select="@id"/>,</xsl:template>
	<!--xsl:template match="xref[@rid!='']">
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
	</xsl:template-->
	<xsl:template match="xref" mode="xref-in-sectitle">
		<xsl:copy-of select="."/>
	</xsl:template>
	<xsl:template match="fname">
		<given-names>
			<xsl:apply-templates select="*|text()" mode="ignore-style"/>
		</given-names>
	</xsl:template>
	<xsl:template match="surname">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="*|text()" mode="ignore-style"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="isstitle">
		<issue-title>
			<xsl:value-of select="normalize-space(.)"/>
		</issue-title>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//p | *[contains(name(),'citat')]/text()"> </xsl:template>
	<xsl:template match="*" mode="debug"> </xsl:template>
	<xsl:template match="figgrp | tabwrap | equation" mode="graphic">
		<xsl:variable name="standardname">
			<xsl:value-of select="$prefix"/>
			<xsl:choose>
				<xsl:when test="name()='equation'">e</xsl:when>
				<xsl:otherwise>g</xsl:otherwise>
			</xsl:choose>
			<xsl:value-of select="@id"/>
		</xsl:variable>
		<xsl:if test=".//graphic">
			<xsl:choose>
				<xsl:when test="substring(.//graphic/@href,1,1)='?'">
					<graphic xlink:href="{substring(.//graphic/@href,2)}{@id}"></graphic>
				</xsl:when>
				<xsl:when test="@filename">
					<graphic xlink:href="{@filename}"></graphic>
				</xsl:when>
				<xsl:otherwise>
					<graphic xlink:href="{.//graphic/@href}"></graphic>	
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		<xsl:if test=".//table">
			<xsl:apply-templates select=".//table" mode="pmc-table"></xsl:apply-templates>
		</xsl:if>
		<xsl:apply-templates select="mmlmath|texmath"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="tr/td | tr/th" mode="pmc-table-cols">
		<col>
			<xsl:if test="@colspan"><xsl:attribute name="span"><xsl:value-of select="@colspan"/></xsl:attribute></xsl:if>
		</col>
	</xsl:template>
	<xsl:template match="table" mode="pmc-table">
		<table>
				<colgroup>
					<xsl:choose>
						<xsl:when test="thead">
							<xsl:apply-templates select="thead/tr[1]/th" mode="pmc-table-cols"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:apply-templates select="tbody/tr[1]/td" mode="pmc-table-cols"/>
						</xsl:otherwise>
					</xsl:choose>
				</colgroup>
			<xsl:apply-templates select="thead"></xsl:apply-templates>
			<xsl:copy-of select="tbody"/>
		</table>
	</xsl:template>
	<xsl:template match="th/bold">
		<xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="th/@*">
		<xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="thead | thead/tr | thead//th">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@filename">
	</xsl:template>
	<xsl:template match="equation">
		<p>
			<disp-formula>
				<xsl:apply-templates select="@*"/>
				<xsl:apply-templates select="." mode="graphic"/>
			</disp-formula>
		</p>
	</xsl:template>
	<xsl:template match="p/equation">
		<inline-formula>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="." mode="graphic"/>
		</inline-formula>
	</xsl:template>
	<xsl:template match="p/graphic">
		<inline-graphic>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="." mode="graphic"/>
		</inline-graphic>
	</xsl:template>
	<xsl:template match="graphic" mode="p-in-equation"> </xsl:template>
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
		<xsl:if test="normalize-space(.)!=''">
			<license-p>
				<xsl:value-of select="normalize-space(.)"/>
			</license-p>
		</xsl:if>
	</xsl:template>
	<xsl:template match="licensep">
		<xsl:if test="normalize-space(.)!=''">
			<license-p>
				<xsl:apply-templates/>
			</license-p>
		</xsl:if>
	</xsl:template>
	<xsl:template match="mmlmath">
		<xsl:choose>
			<xsl:when test="*">
				<xsl:copy-of select="*"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="." disable-output-escaping="yes"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="texmath">
		<tex-math>
			<xsl:apply-templates/>
		</tex-math>
	</xsl:template>
	<xsl:template match="*" mode="doi">
		<xsl:param name="doi"/>
		<ext-link ext-link-type="doi" xlink:href="{$doi}">
			<xsl:value-of select="$doi"/>
		</ext-link>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//doi | ref/doi">
		<!-- ext-link ext-link-type="doi" xlink:href="{.}"><xsl:value-of select="normalize-space(.)"/></ext-link> -->
		<pub-id pub-id-type="doi">
			<xsl:value-of select="normalize-space(.)"/>
		</pub-id>
	</xsl:template>
	<xsl:template match="sec/text() | subsec/text()"/>
	<xsl:template match="thesis | thesgrp">
		<xsl:apply-templates select="@* | * | text()"> </xsl:apply-templates>
	</xsl:template>
	<xsl:template match="degree "> </xsl:template>



	<!--xsl:template match=" *[contains(name(),'contrib')]//bold |  *[contains(name(),'monog')]//bold"/-->
	<xsl:template match="subsec/xref | sec/xref"> </xsl:template>
	<xsl:template match="*[*]" mode="next">
		<xsl:if test="position()=1">
			<xsl:value-of select="name()"/>
		</xsl:if>
	</xsl:template>

	<xsl:template match="figgrps/figgrp/caption">
		<caption>
			<p>
				<xsl:apply-templates select="@*| * | text()"/>
			</p>
		</caption>
	</xsl:template>

	<xsl:template name="display_date">
		<xsl:param name="dateiso"/>
		<xsl:param name="date" select="''"/>
		<xsl:param name="format">number</xsl:param>
		<xsl:param name="specyear"></xsl:param>
		<xsl:variable name="y">
			<xsl:value-of select="substring($dateiso,1,4)"/>
		</xsl:variable>

		<xsl:choose>
			<xsl:when test="$date=''">
				<xsl:if test="substring($dateiso,7,2)!='00'">
					<day>
						<xsl:value-of select="substring($dateiso,7,2)"/>
					</day>
				</xsl:if>
				<xsl:if test="substring($dateiso,5,2)!='00'">
					<month>
						<xsl:value-of select="substring($dateiso,5,2)"/>
					</month>
				</xsl:if>
			</xsl:when>

			<xsl:when
				test="contains($date,'-') or contains($date,'/') or contains($date,'Summer') or contains($date,'Winter') or contains($date,'Autumn') or contains($date,'Fall') or contains($date,'Spring')">
				<xsl:choose>
					<xsl:when test="contains($date,$y)">
						<xsl:variable name="d">
							<xsl:value-of select="substring-before($date,$y)"/>
							<xsl:value-of select="substring-after($date,$y)"/>
						</xsl:variable>
						<xsl:variable name="season">
							<xsl:value-of
								select="translate(translate(translate($d,' ',''),'.',''),'/','-')"/>
						</xsl:variable>

						<xsl:if test="$season!=''">
							<season>
								<xsl:apply-templates select="." mode="fix_season">
									<xsl:with-param name="season" select="$season"/>
								</xsl:apply-templates>
							</season>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<season>
							<xsl:apply-templates select="." mode="fix_season">
								<xsl:with-param name="season"
									select="translate(translate(translate($date,' ',''),'.',''),'/','-')"
								/>
							</xsl:apply-templates>
						</season>
					</xsl:otherwise>
				</xsl:choose>

			</xsl:when>
			<xsl:when test="$format='number'">
				<xsl:if test="substring($dateiso,7,2)!='00'">
					<day>
						<xsl:value-of select="substring($dateiso,7,2)"/>
					</day>
				</xsl:if>
				<xsl:if test="substring($dateiso,5,2)!='00'">
					<month>
						<xsl:value-of select="substring($dateiso,5,2)"/>
					</month>
				</xsl:if>
			</xsl:when>
			<xsl:when test="$format='textual'">
				<xsl:variable name="d" select="substring($dateiso,7,2)"/>
				<xsl:variable name="m" select="substring($dateiso,5,2)"/>
				<xsl:if test="$d!='00'">
					<day>
						<xsl:value-of select="$d"/>
					</day>
				</xsl:if>
				<xsl:if test="$m!='00'">
					<xsl:variable name="month">
						<xsl:choose>
							<xsl:when test="$m='01'">
								<xsl:choose>
									<xsl:when test="contains($date,'Jan')">Jan</xsl:when>
									<xsl:when test="contains($date,'jan')">jan</xsl:when>
									<xsl:when test="contains($date,'ene')">ene</xsl:when>
									<xsl:when test="contains($date,'Ene')">Ene</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='02'">
								<xsl:choose>
									<xsl:when test="contains($date,'Feb')">Feb</xsl:when>
									<xsl:when test="contains($date,'Fev')">Fev</xsl:when>
									<xsl:when test="contains($date,'fev')">fev</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='03'">
								<xsl:choose>
									<xsl:when test="contains($date,'Mar')">Mar</xsl:when>
									<xsl:when test="contains($date,'mar')">mar</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='04'">
								<xsl:choose>
									<xsl:when test="contains($date,'Apr')">Apr</xsl:when>
									<xsl:when test="contains($date,'apr')">apr</xsl:when>
									<xsl:when test="contains($date,'abr')">abr</xsl:when>
									<xsl:when test="contains($date,'Abr')">Abr</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='05'">
								<xsl:choose>
									<xsl:when test="contains($date,'May')">May</xsl:when>
									<xsl:when test="contains($date,'may')">may</xsl:when>
									<xsl:when test="contains($date,'mai')">mai</xsl:when>
									<xsl:when test="contains($date,'Mai')">Mai</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='06'">
								<xsl:choose>
									<xsl:when test="contains($date,'Jun')">Jun</xsl:when>
									<xsl:when test="contains($date,'jun')">jun</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='07'">
								<xsl:choose>
									<xsl:when test="contains($date,'Jul')">Jul</xsl:when>
									<xsl:when test="contains($date,'jul')">jul</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='08'">
								<xsl:choose>
									<xsl:when test="contains($date,'Aug')">Aug</xsl:when>
									<xsl:when test="contains($date,'ago')">ago</xsl:when>
									<xsl:when test="contains($date,'Ago')">Ago</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='09'">
								<xsl:choose>
									<xsl:when test="contains($date,'Sep')">Sep</xsl:when>
									<xsl:when test="contains($date,'sep')">sep</xsl:when>
									<xsl:when test="contains($date,'Set')">Set</xsl:when>
									<xsl:when test="contains($date,'set')">set</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='10'">
								<xsl:choose>
									<xsl:when test="contains($date,'Oct')">Oct</xsl:when>
									<xsl:when test="contains($date,'oct')">oct</xsl:when>
									<xsl:when test="contains($date,'out')">out</xsl:when>
									<xsl:when test="contains($date,'Out')">Out</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='11'">
								<xsl:choose>
									<xsl:when test="contains($date,'Nov')">Nov</xsl:when>
									<xsl:when test="contains($date,'nov')">nov</xsl:when>
								</xsl:choose>
							</xsl:when>
							<xsl:when test="$m='12'">
								<xsl:choose>
									<xsl:when test="contains($date,'Dec')">Dec</xsl:when>
									<xsl:when test="contains($date,'dez')">dez</xsl:when>
									<xsl:when test="contains($date,'Dez')">Dez</xsl:when>
									<xsl:when test="contains($date,'dic')">dic</xsl:when>
									<xsl:when test="contains($date,'Dic')">Dic</xsl:when>

								</xsl:choose>
							</xsl:when>
						</xsl:choose>
					</xsl:variable>
					<xsl:if test="contains($date,$month)">
						<xsl:variable name="test" select="substring-after($date,$month)"/>
						<month>
							<xsl:value-of select="$month"/>
							<xsl:choose>
								<xsl:when test="contains($test,$y)">
									<xsl:value-of
										select="substring-before(substring-after($date,$month),$y)"
									/>
								</xsl:when>
								<xsl:when test="contains($test,' ')">
									<xsl:value-of
										select="substring-before(substring-after($date,$month),' ')"
									/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="substring-after($date,$month)"/>
								</xsl:otherwise>
							</xsl:choose>

						</month>
					</xsl:if>
				</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="substring($dateiso,7,2)!='00'">
					<day>
						<xsl:value-of select="substring($dateiso,7,2)"/>
					</day>
				</xsl:if>
				<xsl:if test="substring($dateiso,5,2)!='00'">
					<month>
						<xsl:value-of select="substring($dateiso,5,2)"/>
					</month>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
		<year><xsl:choose>
				<xsl:when test="$specyear!=''"><xsl:value-of select="$specyear"/></xsl:when>
				<xsl:otherwise><xsl:value-of select="substring($dateiso,1,4)"/></xsl:otherwise>
			</xsl:choose></year>
	</xsl:template>
	<xsl:template match="season">
		<xsl:apply-templates select="." mode="fix_season">
			<xsl:with-param name="season" select="."/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="*" mode="fix_season">
		<xsl:param name="season"/>
		<xsl:choose>
			<xsl:when
				test="contains($season,'Summer') or contains($season,'Spring') or contains($season,'Autumn') or contains($season,'Fall') or contains($season,'Winter')"> </xsl:when>
			<xsl:otherwise>
				<xsl:variable name="s1" select="substring-before($season,'-')"/>
				<xsl:variable name="s2" select="substring-after($season,'-')"/>
				<xsl:value-of select="substring($s1,1,3)"/>-<xsl:value-of
					select="substring($s2,1,3)"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="inpress">
		<comment content-type="inpress">
			<xsl:value-of select="normalize-space(.)"/>
		</comment>
	</xsl:template>

	<xsl:template match="sciname | title//sciname">
		<named-content content-type="scientific-name">
			<xsl:apply-templates/>
		</named-content>
	</xsl:template>
	<xsl:template match="quote">
		<disp-quote>
			<p>
				<xsl:value-of select="normalize-space(.)"/>
			</p>
		</disp-quote>
	</xsl:template>


	<xsl:template match="confgrp">
		<conference>
			<xsl:apply-templates select="*|text()"/>
		</conference>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//confgrp | ref/confgrp">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="confgrp/date">
		<conf-date>
			<xsl:value-of select="normalize-space(.)"/>
		</conf-date>
	</xsl:template>
	<xsl:template match="confgrp/sponsor">
		<conf-sponsor>
			<xsl:value-of select="normalize-space(.)"/>
		</conf-sponsor>
	</xsl:template>
	<xsl:template match="confgrp/city">
		<conf-loc>
			<xsl:value-of select="normalize-space(.)"/>
			<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
			<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</conf-loc>
	</xsl:template>
	<xsl:template match="confgrp/state">
		<xsl:if test="not(../city)">

			<conf-loc>
				<xsl:value-of select="normalize-space(.)"/>
				<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
			</conf-loc>
		</xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/country">
		<xsl:if test="not(../city) and not(../state)">

			<conf-loc>
				<xsl:value-of select="normalize-space(.)"/>
			</conf-loc>
		</xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/no"/>
	<xsl:template match="confgrp/confname">
		<conf-name>
			<xsl:apply-templates select="../confgrp" mode="fulltitle"/>
		</conf-name>
	</xsl:template>

	<xsl:template match="confgrp" mode="fulltitle">
		<xsl:apply-templates select="no|confname" mode="fulltitle"/>
	</xsl:template>

	<xsl:template match="confgrp/confname | confgrp/no" mode="fulltitle"><xsl:value-of select="normalize-space(.)"/>&#160;</xsl:template>

	<xsl:template match="colvolid"><volume><xsl:value-of select="."/></volume></xsl:template>
	<xsl:template match="coltitle">
			<series>
			<xsl:value-of select="normalize-space(.)"/>
		</series>
	</xsl:template>

	<xsl:template match="xref[@rid='']"/>
	<xsl:template match="thesgrp"/>
	
	<xsl:template match="sec//title | caption//title">
		<title>
			<xsl:apply-templates select="*|text()"/>
		</title>
	</xsl:template>
	<xsl:template match="patgrp">
		<patent>
			<xsl:apply-templates select="@*|orgname|patent"/>
		</patent>
		<xsl:if test="date">
			<year>
				<xsl:value-of select="date"/>
			</year>
		</xsl:if>
	</xsl:template>
	<xsl:template match="patgrp/orgname">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	<xsl:template match="article|text|doc" mode="pub-date">
		<xsl:variable name="preprint_date">
			<xsl:choose>
				<xsl:when test="@rvpdate">
					<xsl:value-of select="@rvpdate"/>
				</xsl:when>
				<xsl:when test="@artdate">
					<xsl:value-of select="@artdate"/>
				</xsl:when>
				<xsl:when test="@ahpdate">
					<xsl:value-of select="@ahpdate"/>
				</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="string-length(normalize-space($preprint_date))&gt;0">
			<pub-date pub-type="epub">
				<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso">
						<xsl:value-of select="$preprint_date"/>
					</xsl:with-param>
				</xsl:call-template>
			</pub-date>
		</xsl:if>
		<xsl:variable name="date_type">
			<xsl:choose>
				<xsl:when test="normalize-space($preprint_date)!=''">ppub</xsl:when>
				<xsl:otherwise><xsl:value-of select="$pub_type"/></xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="$date_type!=''">
			<pub-date pub-type="{$date_type}">
				<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso">
						<xsl:value-of select="@dateiso"/>
					</xsl:with-param>
					<xsl:with-param name="date">
						<xsl:value-of select="//extra-scielo//season"/>
					</xsl:with-param>
				</xsl:call-template>
			</pub-date>
		</xsl:if>
	</xsl:template>
	<xsl:template match="element">
		<xsl:element name="{@name}">
			<xsl:apply-templates select="attrib|element|text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="attrib">
		<xsl:attribute name="{@name}">
			<xsl:apply-templates select="@value"/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="supplmat">
		<supplementary-material id="{@id}" xlink:href="{@href}" mimetype="{@mimetype}" mime-subtype="{@mimesubt}">
			<xsl:apply-templates></xsl:apply-templates>
		</supplementary-material>
	</xsl:template>
	<xsl:template match="p/supplmat">
		<inline-supplementary-material xlink:href="{@href}" mimetype="{@mimetype}" mime-subtype="{@mimesubt}">
			<xsl:apply-templates></xsl:apply-templates>
		</inline-supplementary-material>
	</xsl:template>
	<xsl:template match="pubid"><xsl:element name="pub-id"><xsl:attribute name="pub-id-type"><xsl:value-of select="@idtype"/></xsl:attribute><xsl:value-of select="normalize-space(.)"/></xsl:element></xsl:template>

	<xsl:template match="related">
		<xsl:variable name="teste"><xsl:value-of select="concat('|',@reltype,'|')"/></xsl:variable>
		<xsl:variable name="type"><xsl:choose>
			<xsl:when test="contains('|article|pr|', $teste)">document</xsl:when>
			<xsl:when test="contains('|other-related-article|unknown-related-article|addended-article|addendum|commentary-article|object-of-concern|companion|corrected-article|letter|retracted-article|peer-reviewed-article|peer-review|', $teste)">related-article</xsl:when>
			<xsl:when test="contains('|other-object|unknown-object|vi|au|table|figure|', $teste)">object</xsl:when>
			<xsl:when test="contains('|other-source|unknown-source|book|database|', $teste)">source</xsl:when>
			<xsl:when test="contains('|other-document|unknown-source|book chapter|', $teste)">document</xsl:when>			
			<xsl:otherwise>source</xsl:otherwise>
		</xsl:choose></xsl:variable>
		
		<xsl:variable name="elem_name"><xsl:choose>
			<xsl:when test="$type='related-article'">related-article</xsl:when>
			<xsl:otherwise>related-object</xsl:otherwise></xsl:choose></xsl:variable>
		
		<xsl:variable name="attrib_prefix"><xsl:value-of select="$type"/></xsl:variable>
		<xsl:element name="{$elem_name}">
			<xsl:choose>
				<xsl:when test="$type='related-article'">
					<xsl:attribute name="id"><xsl:value-of select="$this_doi"/></xsl:attribute>
					<xsl:attribute name="{$attrib_prefix}-type"><xsl:value-of select="@reltype"/></xsl:attribute>
					<xsl:attribute name="href"><xsl:value-of select="@relid"/></xsl:attribute>
					<xsl:attribute name="ext-link-type"><xsl:value-of select="@relidtp"/></xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="{$attrib_prefix}-type"><xsl:value-of select="@reltype"/></xsl:attribute>
					<xsl:attribute name="{$attrib_prefix}-id"><xsl:value-of select="@relid"/></xsl:attribute>
					
					<xsl:choose>
						<xsl:when test="@reltype='pr'">
							<xsl:attribute name="{$attrib_prefix}-id-type">press-release</xsl:attribute>
							<xsl:attribute name="specific-use">processing-only</xsl:attribute>
						</xsl:when>
						<xsl:when test="@reltype='article'">
							<xsl:attribute name="{$attrib_prefix}-id-type"><xsl:value-of select="@relidtp"/></xsl:attribute>
							<xsl:attribute name="link-type">article-has-press-release</xsl:attribute>
							<xsl:attribute name="specific-use">processing-only</xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="{$attrib_prefix}-id-type"><xsl:value-of select="@relidtp"/></xsl:attribute>
						</xsl:otherwise>
					</xsl:choose>
					
				</xsl:otherwise>
			</xsl:choose>
			
		</xsl:element>
	</xsl:template>
	<xsl:template match="author">
		<contrib><xsl:apply-templates select="*"></xsl:apply-templates></contrib>
	</xsl:template>
	<xsl:template match="corpauth">
		<collab><xsl:apply-templates select="orgname|orgiv|text()"></xsl:apply-templates></collab>
	</xsl:template>
	<xsl:template match="product" mode="article-meta">
		<product product-type="{@prodtype}">
			<xsl:apply-templates select="*" mode="article-meta"></xsl:apply-templates>
		</product>
	</xsl:template>
	
	<xsl:template match="product/*"  mode="article-meta"><xsl:element name="{name()}"><xsl:value-of select="normalize-space(.)"/></xsl:element>
	</xsl:template>
	<xsl:template match="product/author|product/corpauth"  mode="article-meta"><xsl:apply-templates select="."></xsl:apply-templates></xsl:template>
	<xsl:template match="product/othinfo"  mode="article-meta"><comment><xsl:value-of select="normalize-space(.)"/></comment></xsl:template>
	<xsl:template match="product/pubname"  mode="article-meta"><publisher-name><xsl:value-of select="normalize-space(.)"/></publisher-name>
		</xsl:template>
	<xsl:template match="product/city | product/state | product/country"  mode="article-meta">
		<xsl:choose>
			<xsl:when test="../city">
				<xsl:if test="../city=.">
				<publisher-loc><xsl:value-of select="normalize-space(.)"/>
					<xsl:if test="../state">, <xsl:value-of select="../state"/>
					</xsl:if>
					<xsl:if test="../country">, <xsl:value-of select="../country"/>
					</xsl:if></publisher-loc>
				</xsl:if>
			</xsl:when>
			<xsl:when test="../state">
				<xsl:if test="../state=.">
					<publisher-loc><xsl:value-of select="normalize-space(.)"/>
						<xsl:if test="../country">, <xsl:value-of select="../country"/>
						</xsl:if></publisher-loc>
				</xsl:if>
			</xsl:when>
			<xsl:when test="../country">
				<publisher-loc><xsl:value-of select="normalize-space(.)"/></publisher-loc>
			</xsl:when>
		</xsl:choose>
		
	</xsl:template>
	<xsl:template match="product/date"  mode="article-meta">
		<year><xsl:value-of select="substring(@dateiso,1,4)"/></year>
	</xsl:template>
	<xsl:template match="product/title"  mode="article-meta">
		<xsl:choose>
			<xsl:when test="../sertitle| ../stitle">
				<article-title><xsl:value-of select="normalize-space(.)"/></article-title>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="count(..//title)&gt;1">
						<xsl:choose>
							<xsl:when test=".=..//title[1]">
								<chapter-title><xsl:value-of select="normalize-space(.)"/></chapter-title>
							</xsl:when>
							<xsl:otherwise>
								<source><xsl:value-of select="normalize-space(.)"/></source>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:when>
					<xsl:otherwise>
						<source><xsl:value-of select="normalize-space(.)"/></source>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="p//product">
		<xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="p//product//text()">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	
	<xsl:template match="p//product//*"><xsl:apply-templates select="*|text()"></xsl:apply-templates></xsl:template>
	
	<xsl:template match="cc">
		<xsl:variable name="href">http://creativecommons.org/licenses/</xsl:variable>
		<xsl:variable name="ccid"><xsl:if test="@ccid"><xsl:value-of select="translate(@ccid,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>/</xsl:if></xsl:variable>
		<xsl:variable name="cversion"><xsl:if test="@cversion"><xsl:value-of select="@cversion"/>/</xsl:if></xsl:variable>
		<xsl:variable name="cccompl"><xsl:if test="@cccompl!='nd'"><xsl:value-of select="translate(@cccompl,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>/</xsl:if></xsl:variable>
		<xsl:variable name="licid"><xsl:value-of select="concat($ccid,$cversion,$cccompl)"/></xsl:variable>
		<permissions>
			<license license-type="{@ccid}" xlink:href="{$href}{$licid}">
				<license-p>
					<graphic>
						<xsl:attribute name="xlink:href">http://i.creativecommons.org/l/<xsl:value-of select="$licid"/>88x31.png</xsl:attribute>
					</graphic>
					CC <xsl:value-of select="concat(@ccid,' ',@cversion,' ',@cccompl)"/>
				</license-p>
			</license>
		</permissions>
	</xsl:template>
	
	<xsl:template match="extra-scielo/license">
		<xsl:variable name="href"><xsl:value-of select="."/></xsl:variable>
		<xsl:variable name="ccid"><xsl:value-of select="../license-type"/></xsl:variable>
		<xsl:variable name="cversion"><xsl:value-of select="../license-version"/></xsl:variable>
		<xsl:variable name="cccompl"><xsl:value-of select="../license-complement"/></xsl:variable>
		<xsl:variable name="licid"><xsl:value-of select="concat($ccid,'/',$cversion,'/',$cccompl)"/></xsl:variable>
		<permissions>
			<license license-type="{substring-before(../license-label,' ')}" xlink:href="{$href}">
				<license-p>
					<graphic>
						<xsl:attribute name="xlink:href">http://i.creativecommons.org/l/<xsl:value-of select="$licid"/>88x31.png</xsl:attribute>
					</graphic>
					CC <xsl:value-of select="../license-label"/>
				</license-p>
			</license>
		</permissions>
	</xsl:template>
	
	<xsl:template match="ack">
		<ack>
			<xsl:apply-templates select="*"/>
		</ack>
	</xsl:template>
	<xsl:template match="funding | funding//*">
		<xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//report//*[name()!='no']">
		<!--xsl:comment>*[contains(name(),'citat')]//report//*[name()!='no']</xsl:comment-->
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//report">
		<!--xsl:comment>report of citation</xsl:comment-->
		<xsl:if test="no">
			<pub-id pub-id-type="other">
				<xsl:value-of select="no"/>
			</pub-id>
		</xsl:if>
		<xsl:if test="*[name()!='no']">
			<comment content-type="award-id">
				<xsl:apply-templates select="*[name()!='no']|text()"/>
			</comment>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="contract" mode="front">
		<award-id>
			<xsl:apply-templates/>
		</award-id>
	</xsl:template>
	
	<xsl:template match="rsponsor | fundsrc" mode="front">
		<funding-source>
			<xsl:choose>
				<xsl:when test="orgname">
					<xsl:value-of select="normalize-space(orgname)"/><xsl:if test="orgdiv">, <xsl:value-of select="orgdiv"/></xsl:if>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select=".//text()"></xsl:apply-templates>
				</xsl:otherwise>
			</xsl:choose>
		</funding-source>
	</xsl:template>
	
	<xsl:template match="report" mode="front">
		<xsl:param name="statement"/>
		<xsl:if test=".//contract">
			<funding-group>
				<xsl:choose>
					<xsl:when test="rsponsor and contract">
						<xsl:apply-templates select=".//rsponsor" mode="award-group">
							<xsl:with-param name="contract" select=".//contract"/>
						</xsl:apply-templates>
					</xsl:when>
					<xsl:when test="rsponsor">
						<xsl:apply-templates select=".//rsponsor" mode="award-group"/>
					</xsl:when>
					<xsl:when test="contract">
						<xsl:apply-templates select=".//contract" mode="award-group"/>
					</xsl:when>
				</xsl:choose>
				<xsl:if test="$statement='true'">
					<funding-statement><xsl:apply-templates select=".//text()"/></funding-statement>
				</xsl:if>
			</funding-group>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="ack//funding | fn//funding" mode="front">
		<xsl:param name="statement"/>
		<xsl:if test=".//contract">
			<funding-group>
				<xsl:apply-templates select="award[contract]" mode="front"></xsl:apply-templates>
				<xsl:if test="$statement='true'">
					<funding-statement><xsl:apply-templates select=".//text()"/></funding-statement>
				</xsl:if>
			</funding-group>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="award" mode="front">
		<xsl:apply-templates select=".//fundsrc" mode="award-group">
			<xsl:with-param name="contract" select=".//contract"/>
		</xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="report//rsponsor | funding//fundsrc" mode="award-group">
		<xsl:param name="contract"/>
		<xsl:if test="$contract">
				<xsl:apply-templates select="$contract" mode="award-group">
					<xsl:with-param name="fundsrc" select="."/>
				</xsl:apply-templates>
		</xsl:if>	
		<xsl:apply-templates select=".//contract" mode="award-group">
			<xsl:with-param name="fundsrc" select="."/>
		</xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="contract" mode="award-group">
		<xsl:param name="fundsrc"/>
		<award-group>
			<xsl:attribute name="award-type">contract</xsl:attribute>
			<xsl:apply-templates select="." mode="front"/>
			<xsl:apply-templates select="$fundsrc" mode="front"/>
		</award-group>
	</xsl:template>
</xsl:stylesheet>
