<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"
	xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="unident" select="//unidentified"/>
	<xsl:variable name="corresp" select="//corresp"/>
	<xsl:variable name="deceased" select="//fngrp[@fntype='deceased']"/>
	<xsl:variable name="eqcontrib" select="//fngrp[@fntype='equal']"/>
	<xsl:variable name="unident_back" select="//back//unidentified"/>
	<xsl:variable name="fn_author" select=".//fngrp[@fntype='author']"/>
	<xsl:variable name="fn" select=".//fngrp"/>
	<xsl:variable name="affs" select=".//aff"/>
	<xsl:variable name="affs_xrefs" select=".//front//author"/>
	<xsl:variable name="xref_id" select="//*[@id]"/>
	<xsl:variable name="qtd_ref" select="count(//*[contains(name(),'citat')])"/>
	<xsl:variable name="reflen">
		<xsl:value-of select="string-length($qtd_ref)"/>
	</xsl:variable>
	<xsl:variable name="ref_no" select="//*[contains(name(),'citat')]/no"/>

	<xsl:variable name="journal_acron" select="//extra-scielo/journal-acron"/>
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
	<!--
    	mode=text
	-->
	<xsl:template match="*" mode="text">
		<xsl:apply-templates select="*|text()" mode="text"/>
	</xsl:template>
	<xsl:template match="text()" mode="text">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	<xsl:template match="text()">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>


	<!-- nodes -->
	<xsl:template match="*">
		<xsl:variable name="test">
			<xsl:apply-templates select="*|text()" mode="ignore-style"/>
		</xsl:variable>
		<xsl:variable name="testbold">
			<xsl:apply-templates select="bold|text()" mode="ignore-style"/>
		</xsl:variable>
		<xsl:variable name="testitalic">
			<xsl:apply-templates select="italic|text()" mode="ignore-style"/>
		</xsl:variable>

		<xsl:choose>
			<xsl:when test="bold and italic">
				<xsl:apply-templates select="@*| * | text()"/>
			</xsl:when>
			<xsl:when test="$test=$testbold">
				<xsl:value-of select="$test"/>
			</xsl:when>
			<xsl:when test="$test=$testitalic">
				<xsl:value-of select="$test"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="@*| * | text()"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>

	<!-- attributes -->
	<xsl:template match="@*">
		<xsl:attribute name="{name()}">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template>

	<xsl:template match="@href">
		<xsl:attribute name="xlink:href">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template>


	<xsl:template match="isstitle">
		<issue-title>
			<xsl:value-of select="."/>
		</issue-title>
	</xsl:template>

	<xsl:template match="caption">
		<caption>
			<title>
				<xsl:choose>
					<xsl:when test="normalize-space(text())!=''">
						<xsl:apply-templates select="*|text()"/>
					</xsl:when>
					<xsl:when test="*[name()!='bold'] or *[name()!='italic']">
						<xsl:apply-templates select="*|text()"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates select="*|text()" mode="ignore-style"/>
					</xsl:otherwise>
				</xsl:choose>
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
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="li">
		<list-item>
			<xsl:apply-templates select="*"/>
		</list-item>
	</xsl:template>
	<xsl:template match="lilabel">
		<label>
			<xsl:value-of select="."/>
		</label>
	</xsl:template>
	<xsl:template match="litext">
		<p>
			<xsl:apply-templates select="* | text()"/>
		</p>
	</xsl:template>

	<xsl:template match="extent">
		<size units="pages">
			<xsl:value-of select="."/>
		</size>
	</xsl:template>
	<xsl:template match="*[contains(name(),'serial')]//extent">
		<fpage>
			<xsl:value-of select="."/>
		</fpage>
	</xsl:template>
	<xsl:template match="body"/>

	<xsl:template
		match="app | term | def | response | sig |  p | sec | bold  | sub | sup | label | subtitle | edition |  issn | italic | corresp | ack | sig-block">
		<xsl:param name="id"/>

		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*| * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="@resptp">
		<xsl:attribute name="response-type"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	
	<xsl:template match="subart">
		<sub-article>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*"/>
		</sub-article>
	</xsl:template>
	
	<xsl:template match="deflist">
		<def-list>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*"/>
		</def-list>
	</xsl:template>
	
	<xsl:template match="defitem">
		<def-item>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*"/>
		</def-item>
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
			<xsl:value-of select="."/>
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
		<xsl:attribute name="xml:lang">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="article|text" mode="dtd-version">
		<xsl:attribute name="dtd-version">3.0</xsl:attribute>
	</xsl:template>
	<xsl:template match="article|text">
		<article>
			<xsl:apply-templates select="." mode="dtd-version"/>
			<xsl:apply-templates select="@doctopic" mode="type"/>
			<xsl:apply-templates select="@language"/>
			<xsl:apply-templates select="." mode="front"/>
			<xsl:apply-templates select="." mode="body"/>
			<xsl:apply-templates select="." mode="back"/>
			<xsl:apply-templates select="response | subart"/>
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
		<xsl:value-of select="."/>
		<xsl:if test="position()!=last()">, </xsl:if>
	</xsl:template>
	<xsl:template match="front/doi | text/doi">
		<article-id pub-id-type="doi">
			<xsl:value-of select="."/>
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
	<xsl:template match="article|text" mode="article-meta">
		<xsl:variable name="l" select="@language"/>
		<article-meta>
			<xsl:if test="..//extra-scielo/issue-order">
				<article-id pub-id-type="publisher-id">S<xsl:value-of select="$JOURNAL_PID"/>
					<xsl:value-of select="substring(@dateiso,1,4)"/>
					<xsl:value-of
						select="substring(10000 + substring(..//extra-scielo/issue-order,5),2)"/>
					<xsl:value-of select="substring-after(100000 + @order,'1')"/>
				</article-id>
				<xsl:apply-templates select="front/doi|doi"/>

			</xsl:if>

			<article-categories>
				<subj-group subj-group-type="heading">
					<xsl:if test=".//toctitle">
						<xsl:variable name="t" select="normalize-space(.//toctitle)"/>

						<subject>
							<xsl:apply-templates select="." mode="format-subject">
								<xsl:with-param name="t" select="$t"/>
							</xsl:apply-templates>
						</subject>
					</xsl:if>
					<xsl:if test="not(.//toctitle)">

						<subject>Article</subject>
					</xsl:if>
				</subj-group>
			</article-categories>
			<xsl:apply-templates select="." mode="article-title"/>
			<xsl:apply-templates select=".//authgrp" mode="front"/>
			<xsl:apply-templates select="." mode="author-notes"/>

			<xsl:apply-templates select="." mode="pub-date"/>

			<xsl:apply-templates select="@volid | @issueno  | @fpage | @lpage"/>
			<xsl:apply-templates select=".//product" mode="article-meta"></xsl:apply-templates>
			<xsl:apply-templates select=".//hist" mode="front"/>
			<xsl:apply-templates select=".//back/licenses"/>
			<xsl:apply-templates select="front/related"/>
			<xsl:apply-templates select=".//abstract[@language=$l]|.//xmlabstr[@language=$l]"/>
			<xsl:apply-templates select=".//abstract[@language!=$l]|.//xmlabstr[@language!=$l]"
				mode="trans"/>
			<xsl:apply-templates select=".//keygrp"/>
			<xsl:apply-templates
				select=".//front/report | .//front/confgrp | ..//front/thesgrp | .//bibcom/report | .//bibcom/confgrp | ..//bibcom/thesgrp  | .//bbibcom/report | .//bbibcom/confgrp | ..//bbibcom/thesgrp | .//back/ack//report"/>
			<xsl:apply-templates select="." mode="counts"/>
			
			
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
					<xsl:value-of select="."/>
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
	</xsl:template>

	<xsl:template match="corpauth" mode="front">
		<xsl:variable name="teste">
			<xsl:apply-templates select="./../../authgrp" mode="text"/>
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
						<xsl:apply-templates select="orgname | orgdiv | text()" mode="nostyle"/>
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


	<xsl:template match="aff">
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
			<institution content-type="aff-pmc"><xsl:apply-templates select="*|text()" mode="aff-pmc"/></institution>
			
			<xsl:choose>
				<xsl:when test="@orgname">
					<xsl:apply-templates select="@*[name()!='id']"/>
					<xsl:if test="city or state or zipcode">
						<addr-line>
							<xsl:apply-templates select="city|state|zipcode"/>
						</addr-line>
					</xsl:if>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="*[contains(name(),'org')]"/>
					<xsl:if test="@state or @city">
						<addr-line>
							<xsl:apply-templates select="@city|@state"/>
						</addr-line>
					</xsl:if>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="country|email"></xsl:apply-templates>
		</aff>
	</xsl:template>
	<xsl:template match="aff/country| aff/email">
		<xsl:element name="{name()}">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="aff/label | aff/sup">
		<xsl:choose>
			<xsl:when test="not(../label) and name()='sup'">
				<label>
					<xsl:value-of select="."/>
				</label>
			</xsl:when>
			<xsl:otherwise>
				<label>
					<xsl:value-of select="."/>
				</label>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="aff/*" mode="aff-pmc">
		<xsl:value-of select="text()"/>
	</xsl:template>
	
	<xsl:template match="aff/email | aff/country" mode="aff-pmc">
		<named-content content-type="{name()}"><xsl:value-of select="."/></named-content>
	</xsl:template>
		
	<xsl:template match="aff/text()" mode="aff-pmc">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="aff/*" mode="original">
		<xsl:value-of select="text()"/>
	</xsl:template>
	<xsl:template match="aff//text()" mode="original">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="xref[@ref-type='aff']/@rid">
		<xsl:variable name="var_id">
			<xsl:choose>
				<xsl:when test="contains(.,' ')">aff<xsl:value-of select="substring-before(.,' ')"
					/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($var_id,'a0')">aff<xsl:value-of
					select="substring-after($var_id,'a0')"/></xsl:when>
			<xsl:otherwise>aff<xsl:value-of select="substring-after($var_id,'a')"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="aff/@id">
		<!-- quando nao ha aff/label = author/xref enquanto author/@rid = aff/@id -->
		<xsl:variable name="var_id">
			<xsl:choose>
				<xsl:when test="contains(.,' ')">aff<xsl:value-of select="substring-before(.,' ')"
					/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:attribute name="id">
			<xsl:choose>
				<xsl:when test="contains($var_id,'a0')">aff<xsl:value-of
						select="substring-after($var_id,'a0')"/></xsl:when>
				<xsl:otherwise>aff<xsl:value-of select="substring-after($var_id,'a')"
					/></xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>

	<xsl:template match="aff/@*[contains(name(),'org')] | aff/*[contains(name(),'org')]">
		<institution>
			<xsl:attribute name="content-type">
				<xsl:value-of select="name()"/>
			</xsl:attribute>
			<xsl:value-of select="."/>
		</institution>
	</xsl:template>

	<xsl:template match="aff/@city | aff/@state | aff/@country | aff/city | aff/state | aff/zipcode">
		<named-content content-type="{name()}">
			<xsl:value-of select="."/>
		</named-content>
	</xsl:template>


	<xsl:template match="e-mail|email">
		<email>
			<xsl:value-of select="."/>
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
				test="contains('abbr|finanacial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype)"/>
			<xsl:otherwise>
				<xsl:apply-templates select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="fngrp" mode="notfnauthors">
		<xsl:choose>
			<xsl:when
				test="contains('abbr|finanacial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype)">
				<xsl:apply-templates select="."/>
			</xsl:when>
			<xsl:otherwise> </xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="@volid | volid">
		<volume>
			<xsl:value-of select="."/>
		</volume>
	</xsl:template>
	<xsl:template match="part">
		<issue-part>
			<xsl:value-of select="."/>
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
			<xsl:otherwise>
				<issue>
					<xsl:value-of select="$journal_issue"/>
					<xsl:if test="../@supplvol or ../@supplno"> Suppl <xsl:value-of
							select="../@supplvol"/><xsl:value-of select="../@supplno"/></xsl:if>
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
					<xsl:value-of select="."/>
				</issue>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
	<xsl:template match="@supplvol | @supplno"> </xsl:template>
	<xsl:template match="suppl">
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
			<xsl:value-of select="."/>
		</page-range> -->

		<xsl:choose>
			<xsl:when test="substring(.,1,2)='ID'">
				<elocation-id>
					<xsl:value-of select="."/>
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
					<xsl:value-of select="."/>
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
						<xsl:value-of select="."/>
					</elocation-id>
				</xsl:if>
			</xsl:when>
			<xsl:when test="substring(.,1,1)='E'">
				<xsl:variable name="e" select="substring-after(.,'E')"/>
				<xsl:if test="normalize-space(translate($e,'0123456789','          '))=''">
					<elocation-id>
						<xsl:value-of select="."/>
					</elocation-id>
				</xsl:if>
			</xsl:when>

			<xsl:otherwise>
				<fpage>
					<xsl:value-of select="."/>
				</fpage>
				<lpage>
					<xsl:value-of select="."/>
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
		<abstract xml:lang="{@language}">
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
		<abstract xml:lang="{@language}">
			<xsl:apply-templates select="*"/>
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

	<xsl:template match="*" mode="counts">
		<counts>
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
				<xsl:with-param name="count" select="count(.//back//*[contains(name(),'citat')])"/>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="element-counts">
				<xsl:with-param name="element_name" select="'page-count'"/>
				<xsl:with-param name="count" select="@lpage - @fpage + 1"/>
			</xsl:apply-templates>

		</counts>
	</xsl:template>
	<xsl:template match="*" mode="element-counts">
		<xsl:param name="element_name"/>
		<xsl:param name="count"/>
		<xsl:if test="$count&gt;0">
			<xsl:element name="{$element_name}">
				<xsl:attribute name="count">
					<xsl:value-of select="$count"/>
				</xsl:attribute>
			</xsl:element>
		</xsl:if>
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
			<xsl:choose>
				<xsl:when test="normalize-space(text())!=''">
					<xsl:apply-templates select="*|text()"/>
				</xsl:when>
				<xsl:when test="*[name()!='bold'] or *[name()!='italic']">
					<xsl:apply-templates select="*|text()"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="*|text()" mode="ignore-style"/>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="following-sibling::node()[1 and name()='xref']"
				mode="xref-in-sectitle"/>
		</title>
	</xsl:template>
	<!--xsl:template match="@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template-->
	<!-- BACK -->
	<xsl:template match="article|text" mode="back">
		<xsl:variable name="test">
			<xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"/>
		</xsl:variable>

		<xsl:if test="$test!='' or back/ack or back/fxmlbody or back/*[@standard] or back/bbibcom">
			<back>
				<xsl:apply-templates select="back"/>
			</back>
		</xsl:if>
	</xsl:template>


	<xsl:template match="back">
		<xsl:apply-templates select="fxmlbody[@type='ack']|ack"/>
		<xsl:apply-templates select="*[@standard]"/>
		<xsl:variable name="test">
			<xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"/>
		</xsl:variable>
		<xsl:if test="$test!=''">
			<fn-group>
				<xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"/>
			</fn-group>
		</xsl:if>
	</xsl:template>

	<xsl:template match="back//isbn">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*|text()|*"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="anonym">
		<anonymous/>
	</xsl:template>
	<xsl:template match="back//fngrp[@fntype]">
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
					<xsl:value-of select="."/>
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


	<xsl:template
		match="*[contains(name(),'citat')]/text() | *[contains(name(),'citat')]//*[*]/text()"/>

	<xsl:template match="*[@standard]">
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
			<xsl:apply-templates select="*[contains(name(),'citat')]"/>
		</ref-list>
	</xsl:template>

	<xsl:template match="xref[@ref-type='bibr']/@rid">
		<xsl:choose>
			<xsl:when test="contains(., 'mkp_ref_')">
				<xsl:attribute name="rid">B<xsl:value-of
						select="substring-before(substring-after(.,'mkp_ref_'),'_')"
					/></xsl:attribute>
			</xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="rid">B<xsl:value-of select="substring(.,2)"/></xsl:attribute>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="*[@standard]/*[contains(name(),'citat')]">
		<xsl:variable name="zeros">
			<xsl:value-of select="substring('0000000000',1, $reflen - string-length(position()))"/>
		</xsl:variable>
		<xsl:variable name="id">
			<xsl:value-of select="$zeros"/>
			<xsl:value-of select="position()"/>
		</xsl:variable>
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
	<xsl:template match="back//no">
		<label>
			<xsl:value-of select="."/>
		</label>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//country">
		<xsl:choose>
			<xsl:when test="../city"> </xsl:when>
			<xsl:when test="../state"> </xsl:when>
			<xsl:otherwise>
				<publisher-loc>
					<xsl:value-of select="."/>
				</publisher-loc>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//city">
		<publisher-loc>
			<xsl:value-of select="."/>
			<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
			<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</publisher-loc>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//state">
		<xsl:choose>
			<xsl:when test="../city"> </xsl:when>
			<xsl:otherwise>
				<publisher-loc>
					<xsl:value-of select="."/>
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
	<xsl:template match="back//*[contains(name(),'corpaut')]">
		<collab>
			<xsl:apply-templates select="orgname|orgdiv|text()"/>
		</collab>
	</xsl:template>
	<xsl:template match="back//pubname">
		<publisher-name>
			<xsl:value-of select="."/>
		</publisher-name>
	</xsl:template>
	<xsl:template match="back//orgdiv"> </xsl:template>
	<xsl:template match="back//orgname">
		<publisher-name>
			<xsl:if test="../orgdiv">
				<xsl:value-of select="../orgdiv"/>, </xsl:if>
			<xsl:value-of select="."/>
		</publisher-name>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'corpaut')]/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template
		match="back//*[contains(name(),'corpaut')]/orgdiv|back//*[contains(name(),'corpaut')]/orgname">
		<xsl:value-of select="."/>
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
	<xsl:template match="back//*[previous]">
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

	<xsl:template match="back//date">
		<xsl:call-template name="display_date">
			<xsl:with-param name="dateiso">
				<xsl:value-of select="@dateiso"/>
			</xsl:with-param>
			<xsl:with-param name="date">
				<xsl:value-of select="."/>
			</xsl:with-param>
			<xsl:with-param name="format">textual</xsl:with-param>
		</xsl:call-template>
	</xsl:template>
	<xsl:template match="back//cited">
		<date-in-citation content-type="access-date">
			<xsl:value-of select="."/>
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

	<xsl:template match="url | uri">
		<xsl:choose>
			<xsl:when test="../cited">
				<comment content-type="cited">
					<xsl:variable name="text">
						<xsl:apply-templates select="../..//text()"/>
					</xsl:variable>a <xsl:choose>
						<xsl:when test="contains($text,'Available')">
							<xsl:value-of
								select="substring-before(substring-after($text, substring-before($text, 'Available')), 'http')"
							/>
						</xsl:when>
						<xsl:when test="contains($text,'Dispon')">
							<xsl:value-of
								select="substring-before(substring-after($text, substring-before($text, 'Dispon')), 'http')"
							/>
						</xsl:when>
						<xsl:otherwise>Available from:</xsl:otherwise>
					</xsl:choose>
					<ext-link ext-link-type="uri" xlink:href="{.}">
						<xsl:apply-templates/>
					</ext-link>
				</comment>
			</xsl:when>
			<xsl:otherwise>
				<ext-link ext-link-type="uri" xlink:href="{.}">
					<xsl:apply-templates/>
				</ext-link>
			</xsl:otherwise>
		</xsl:choose>

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
	<xsl:template match="uri[contains(@href,'mailto:')]">
		<email>
			<xsl:apply-templates select=".//text()"/>
		</email>
	</xsl:template>
	<!-- 
	<fig id="fg-012">
  <label>Figure 12. </label>
  <caption><title>Three Perspectives on My Dog</title></caption>
  <graphic xlink:href="frontView.png">
   <label>a.</label>
   <caption><p>View A: From the Front, Laughing</p></caption>
  </graphic>
  <graphic xlink:href="sideView.png">
   <label>b.</label>
   <caption><p>View B: From the Side, Best Profile</p></caption>
  </graphic>
  <graphic xlink:href="motionView.png">
   <label>c.</label>
   <caption><p>View C: In Motion, A Blur on Feet</p></caption>
  </graphic>
</fig>
Here is a figure group, with three figures inside, each of which contains a graphic. The figure group also has a title that applies to all the figures.
<fig-group id="dogpix4">
  <caption><title>Three perspectives on My Dog</title></caption>
  <fig id="fg-12">
   <label>a.</label>
   <caption><p>View A: From the Front, Laughing</p></caption>
     <graphic xlink:href="frontView.png"/>
  </fig>
  <fig id="fg-13">
   <label>b.</label>
   <caption><p>View B: From the Side, Best Profile</p></caption>
     <graphic xlink:href="sideView.png"/>
  </fig>
  <fig id="fg-14">
   <label>c.</label>
   <caption><p>View C: In Motion, A Blur on Feet</p></caption>
     <graphic xlink:href="motionView.png"/>
  </fig>
</fig-group>
	 -->
	<xsl:template match="figgrps[not(label)]">
		<fig-group id="{@id}">
			<xsl:apply-templates select="caption"/>
			<xsl:apply-templates select=".//figgrp"/>
		</fig-group>
	</xsl:template>
	<xsl:template match="figgrps[label]">
		<fig id="{@id}">
			<xsl:apply-templates select="label"/>
			<xsl:apply-templates select="caption"/>
			<xsl:apply-templates select=".//figgrp"/>
		</fig>
	</xsl:template>
	<xsl:template match="figgrp">
		<p>
			<fig id="{@id}">
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
		<fig id="{@id}">
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
		<p>
			<table-wrap id="{@id}">
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
		<fn id="TFN{substring(@id,4)}{$table_id}">
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
		<table-wrap id="{@id}">
			<xsl:apply-templates select=".//label"/>
			<xsl:apply-templates select=".//caption"/>
			<xsl:apply-templates select="." mode="graphic"/>
			<xsl:apply-templates select="." mode="notes"/>
			<!-- xsl:if test=".//notes">
				<table-wrap-foot>
					
					<fn><p><xsl:value-of select=".//notes"/></p></fn>
					
				</table-wrap-foot>
				</xsl:if> -->
		</table-wrap>
	</xsl:template>



	<xsl:template match="back//*[contains(name(),'contrib')]//title">
		<xsl:variable name="title">
			<xsl:apply-templates select="*|text()"/>
			<xsl:apply-templates select="../subtitle" mode="title"/>
		</xsl:variable>
		<xsl:variable name="t" select="normalize-space($title)"/>
		<xsl:choose>
			<xsl:when test="../../node()[contains(name(),'monog')] or ../../vmonog">
				<chapter-title>
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
		<xsl:value-of select="."/>
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
		<source xml:lang="{$lang}">
			<xsl:apply-templates select="*|text()"/>
		</source>
	</xsl:template>

	<xsl:template match="sertitle | stitle | vstitle/stitle">
		<source>
			<xsl:choose>
				<xsl:when test="normalize-space(text())!=''">
					<xsl:apply-templates select="*|text()"/>
				</xsl:when>
				<xsl:when test="*[name()!='bold'] or *[name()!='italic']">
					<xsl:apply-templates select="*|text()"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="*|text()" mode="ignore-style"/>
				</xsl:otherwise>
			</xsl:choose>
		</source>
	</xsl:template>
	<xsl:template match="*" mode="ignore-style">
		<xsl:apply-templates select="."/>
	</xsl:template>
	<xsl:template match="bold | italic" mode="ignore-style">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>



	<xsl:template match="back//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle"/>
	<xsl:template match="back//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle"
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
					<xsl:value-of select="."/>
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
					<xsl:apply-templates select="*[name()!='graphic']|text()" mode="nostyle"/>
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
	<xsl:template match="isstitle">
		<issue-title>
			<xsl:value-of select="."/>
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
			<graphic xlink:href="{$standardname}"/>
		</xsl:if>
		<xsl:if test=".//table">
			<xsl:copy-of select=".//table"/>
		</xsl:if>

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
				<xsl:value-of select="."/>
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
		<mml:math>
			<xsl:copy-of select="*"/>
		</mml:math>
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
	<xsl:template match="*[contains(name(),'citat')]//doi">
		<!-- ext-link ext-link-type="doi" xlink:href="{.}"><xsl:value-of select="."/></ext-link> -->
		<pub-id pub-id-type="doi">
			<xsl:value-of select="."/>
		</pub-id>
	</xsl:template>
	<xsl:template match="sec/text() | subsec/text()"/>
	<xsl:template match="thesis">
		<xsl:apply-templates select="@* | * | text()"> </xsl:apply-templates>
	</xsl:template>
	<xsl:template match="degree "> </xsl:template>



	<xsl:template match=" *[contains(name(),'contrib')]//bold |  *[contains(name(),'monog')]//bold"/>
	<xsl:template match="subsec/xref | sec/xref"> </xsl:template>
	<xsl:template match="*[*]" mode="next">
		<xsl:if test="position()=1">
			<xsl:value-of select="name()"/>
		</xsl:if>
	</xsl:template>

	<xsl:template
		match="caption//bold  | caption//sup |caption//italic |
	   subtitle//bold |  subtitle//sub | subtitle//sup | subtitle//italic |
	   sectitle//bold |  sectitle//sup | sectitle//italic |
	   title//bold |   title//sup  |
	   
	   label//bold | label//italic | label//sub | label//sup">
		<xsl:choose>
			<xsl:when test="*">
				<xsl:apply-templates select="*|text()"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>


	</xsl:template>


	<xsl:template match="*//text()[.=' ']">
		<xsl:value-of select="."/>
	</xsl:template>


	<xsl:template match="figgrps/figgrp/caption">
		<caption>
			<p>
				<xsl:apply-templates select="@*| * | text()"/>
			</p>
		</caption>
	</xsl:template>
	<xsl:template match="edition//italic | edition//bold | edition//sub | edition//sup ">
		<xsl:value-of select="."/>
	</xsl:template>
	<!--xsl:template match="p[normalize-space(.//text())='']"/-->

	<xsl:template name="display_date">
		<xsl:param name="dateiso"/>
		<xsl:param name="date" select="''"/>
		<xsl:param name="format">number</xsl:param>
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
		<year>
			<xsl:value-of select="substring($dateiso,1,4)"/>
		</year>
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
			<xsl:value-of select="."/>
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
				<xsl:value-of select="."/>
			</p>
		</disp-quote>
	</xsl:template>


	<xsl:template match="confgrp">
		<conference>
			<xsl:apply-templates select="*|text()"/>
		</conference>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//confgrp">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="confgrp/date">
		<conf-date>
			<xsl:value-of select="."/>
		</conf-date>
	</xsl:template>
	<xsl:template match="confgrp/sponsor">
		<conf-sponsor>
			<xsl:value-of select="."/>
		</conf-sponsor>
	</xsl:template>
	<xsl:template match="confgrp/city">
		<conf-loc>
			<xsl:value-of select="."/>
			<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
			<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</conf-loc>
	</xsl:template>
	<xsl:template match="confgrp/state">
		<xsl:if test="not(../city)">

			<conf-loc>
				<xsl:value-of select="."/>
				<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
			</conf-loc>
		</xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/country">
		<xsl:if test="not(../city) and not(../state)">

			<conf-loc>
				<xsl:value-of select="."/>
			</conf-loc>
		</xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/no"/>
	<xsl:template match="confgrp/confname">
		<conf-name>
			<xsl:apply-templates select="../..//confgrp" mode="fulltitle"/>
		</conf-name>
	</xsl:template>

	<xsl:template match="confgrp" mode="fulltitle">
		<xsl:apply-templates select="no|confname" mode="fulltitle"/>
	</xsl:template>

	<xsl:template match="confgrp/confname | confgrp/no" mode="fulltitle"><xsl:value-of select="."/>
		&#160; </xsl:template>

	<xsl:template match="coltitle">
		<series>
			<xsl:value-of select="."/>
		</series>
	</xsl:template>

	<xsl:template match="xref[@rid='']"/>
	<xsl:template match="thesgrp"/>
	<xsl:template match="ack">
		<xsl:choose>
			<xsl:when test=".//report">
				<ack>
					<xsl:if test=".//sectitle">
						<title>
							<xsl:value-of select=".//sectitle"/>
						</title>

					</xsl:if>
					<xsl:apply-templates select="p"/>
				</ack>
			</xsl:when>
			<xsl:otherwise>
				<ack>
					<xsl:apply-templates select="*|text()"/>
				</ack>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="ack//p">
		<p>
			<xsl:apply-templates select="*[name()!='report']|text()|report//text()"/>
		</p>
	</xsl:template>
	<xsl:template match="front//report | bbibcom//report | ack//report">
		<funding-group>
			<xsl:if test="rsponsor or .//contract or .//awarded">
				<award-group>
					<xsl:attribute name="award-type">
						<xsl:choose>
							<xsl:when test=".//contract">contract</xsl:when>
							<xsl:otherwise>grant</xsl:otherwise>
						</xsl:choose>
					</xsl:attribute>
					<xsl:apply-templates select="*"/>
				</award-group>
			</xsl:if>
			<!--xsl:if test="not($unident_back[contains(.//text,'ACK') or contains(.//text,'Ack') or contains(.//text,'Agrad') or contains(.//text,'AGRAD')])"-->
			<funding-statement>
				<xsl:apply-templates select=".//text()"/>
			</funding-statement>
			<!--/xsl:if-->
		</funding-group>
	</xsl:template>
	<xsl:template match="report/projname"> </xsl:template>
	<xsl:template match="report/awarded">
		<!--xsl:comment>report/awarded</xsl:comment-->
		<xsl:if test="orgname or orgdiv">
			<principal-award-recipient>
				<xsl:apply-templates select="orgname|orgdiv"/>
			</principal-award-recipient>
		</xsl:if>
		<xsl:if test="fname or surname">
			<principal-investigator>
				<xsl:apply-templates select="surname|fname"/>
			</principal-investigator>
		</xsl:if>
	</xsl:template>
	<xsl:template match="awarded/fname | awarded/surname | awarded/orgname | awarded/orgdiv">
		<!--xsl:comment>report/awarded/*</xsl:comment-->

		<xsl:value-of select="."/>
	</xsl:template>

	<xsl:template match="contract">
		<award-id>
			<xsl:apply-templates/>
		</award-id>
	</xsl:template>
	<xsl:template match="rsponsor/orgdiv"/>
	<xsl:template match="rsponsor/orgname">
		<funding-source>
			<xsl:value-of select="."/>
			<xsl:if test="../orgdiv">, <xsl:value-of select="../orgdiv"/>
			</xsl:if>
		</funding-source>
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
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="article|text" mode="pub-date">
		<xsl:variable name="preprint_date">
			<xsl:choose>
				<xsl:when test="@rvpdate">
					<xsl:value-of select="@rvpdate"/>
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
				<xsl:when test="normalize-space($preprint_date)=''">epub-ppub</xsl:when>
			</xsl:choose>
		</xsl:variable>
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
		<supplementary-material xlink:href="{@href}">
			<xsl:apply-templates></xsl:apply-templates>
		</supplementary-material>
	</xsl:template>
	<xsl:template match="p/supplmat">
		<inline-supplementary-material xlink:href="{@href}">
			<xsl:apply-templates></xsl:apply-templates>
		</inline-supplementary-material>
	</xsl:template>
	<xsl:template match="pubid"><xsl:element name="pub-id"><xsl:attribute name="pub-id-type"><xsl:value-of select="@idtype"/></xsl:attribute><xsl:value-of select="."/></xsl:element></xsl:template>

	<xsl:template match="related">
		<xsl:variable name="teste"><xsl:value-of select="concat('|',@doctype,'|')"/></xsl:variable>
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
			<xsl:attribute name="id">rel<xsl:value-of select="../../@order"/></xsl:attribute>
			<xsl:attribute name="{$attrib_prefix}-type"><xsl:value-of select="@doctype"/></xsl:attribute>
			
			<xsl:choose>
				<xsl:when test="$type='related-article'">
					<xsl:attribute name="href"><xsl:value-of select="@link"/></xsl:attribute>
					<xsl:attribute name="ext-link-type"><xsl:value-of select="@linktype"/></xsl:attribute>
					
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="{$attrib_prefix}-id"><xsl:value-of select="@link"/></xsl:attribute>
					
					<xsl:choose>
						<xsl:when test="@doctype='pr'">
							<xsl:attribute name="{$attrib_prefix}-id-type">press-release</xsl:attribute>
							<xsl:attribute name="specific-use">processing-only</xsl:attribute>
						</xsl:when>
						<xsl:when test="@doctype='article'">
							<xsl:attribute name="{$attrib_prefix}-id-type"><xsl:value-of select="@linktype"/></xsl:attribute>
							<xsl:attribute name="link-type">article-has-press-release</xsl:attribute>
							<xsl:attribute name="specific-use">processing-only</xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="{$attrib_prefix}-id-type"><xsl:value-of select="@linktype"/></xsl:attribute>
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
	
	<xsl:template match="product/*"  mode="article-meta"><xsl:element name="{name()}"><xsl:value-of select="."/></xsl:element>
	</xsl:template>
	<xsl:template match="product/author|product/corpauth"  mode="article-meta"><xsl:apply-templates select="."></xsl:apply-templates></xsl:template>
	<xsl:template match="product/othinfo"  mode="article-meta"><comment><xsl:value-of select="."/></comment></xsl:template>
	<xsl:template match="product/pubname"  mode="article-meta"><publisher-name><xsl:value-of select="."/></publisher-name>
		</xsl:template>
	<xsl:template match="product/city | product/state | product/country"  mode="article-meta">
		<xsl:choose>
			<xsl:when test="../city">
				<xsl:if test="../city=.">
				<publisher-loc><xsl:value-of select="."/>
					<xsl:if test="../state">, <xsl:value-of select="../state"/>
					</xsl:if>
					<xsl:if test="../country">, <xsl:value-of select="../country"/>
					</xsl:if></publisher-loc>
				</xsl:if>
			</xsl:when>
			<xsl:when test="../state">
				<xsl:if test="../state=.">
					<publisher-loc><xsl:value-of select="."/>
						<xsl:if test="../country">, <xsl:value-of select="../country"/>
						</xsl:if></publisher-loc>
				</xsl:if>
			</xsl:when>
			<xsl:when test="../country">
				<publisher-loc><xsl:value-of select="."/></publisher-loc>
			</xsl:when>
		</xsl:choose>
		
	</xsl:template>
	<xsl:template match="product/date"  mode="article-meta">
		<year><xsl:value-of select="substring(@dateiso,1,4)"/></year>
	</xsl:template>
	<xsl:template match="product/title"  mode="article-meta">
		<xsl:choose>
			<xsl:when test="../sertitle">
				<article-title><xsl:value-of select="."/></article-title>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="count(..//title)&gt;1">
						<xsl:choose>
							<xsl:when test=".=..//title[1]">
								<chapter-title><xsl:value-of select="."/></chapter-title>
							</xsl:when>
							<xsl:otherwise>
								<source><xsl:value-of select="."/></source>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:when>
					<xsl:otherwise>
						<source><xsl:value-of select="."/></source>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="p//product">
		<xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="p//product//text()">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="p//product//*"><xsl:apply-templates select="*|text()"></xsl:apply-templates></xsl:template>
	
</xsl:stylesheet>
