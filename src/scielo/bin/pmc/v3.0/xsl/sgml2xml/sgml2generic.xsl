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
	<xsl:variable name="xref_id" select="//*[@id]"/>
	<xsl:variable name="qtd_ref" select="count(//*[contains(name(),'citat')])"/>
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
	<xsl:variable name="PUB_TYPE" select=".//extra-scielo/issn-type"/>
	<xsl:variable name="CURRENT_ISSN" select=".//extra-scielo/current-issn"/>
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
			<xsl:when test="$normalized_page='00000'"><xsl:value-of select="$normalized_order"/>
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
		match="sig |  p | sec | bold  | sub | sup |  label | subtitle | edition |  issn | italic | corresp | ack | sig-block">
		<xsl:param name="id"/>

		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*| * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
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
				<xsl:when test=".='??'">addendum</xsl:when>
				<xsl:when test=".='??'">book-review</xsl:when>
				<xsl:when test=".='??'">books-received</xsl:when>
				<xsl:when test=".='??'">brief-report</xsl:when>
				<xsl:when test=".='??'">calendar</xsl:when>
				<xsl:when test=".='??'">collection</xsl:when>
				<xsl:when test=".='??'">correction</xsl:when>
				<xsl:when test=".='??'">discussion</xsl:when>
				<xsl:when test=".='??'">dissertation</xsl:when>
				<xsl:when test=".='??'">in-brief</xsl:when>
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
				<xsl:otherwise>other</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="@language">
		<xsl:attribute name="xml:lang">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:attribute>
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
			<xsl:if test=".//nlm-title and .//nlm-title!=''">
				<journal-id journal-id-type="nlm-ta">
					<xsl:value-of select=".//nlm-title"/>
				</journal-id>
			</xsl:if>
			<xsl:if test="not(.//nlm-title) or .//nlm-title=''">
				<xsl:comment>Is a NLM journal title? If yes, missing 
				&lt;journal-id journal-id-type="nlm-ta"&gt;???&lt;/journal-id&gt;
			</xsl:comment>
			</xsl:if>


			<xsl:if test="string-length($JOURNAL_PID)=9">
				<journal-id journal-id-type="publisher-id">
					<xsl:value-of select="$JOURNAL_PID"/>
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
			<issn pub-type="{$PUB_TYPE}">
				<xsl:value-of select="$CURRENT_ISSN"/>
			</issn>
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

			<xsl:apply-templates select="@volid | @issueno  | @fpage | @lpage"/>
			<xsl:apply-templates select=".//hist" mode="front"/>
			<xsl:apply-templates select=".//back/licenses"/>
			<xsl:apply-templates select=".//abstract[@language=$l]|.//xmlabstr[@language=$l]"/>
			<xsl:apply-templates select=".//abstract[@language!=$l]|.//xmlabstr[@language!=$l]"
				mode="trans"/>
			<xsl:apply-templates select=".//keygrp"/>
			<xsl:apply-templates
				select=".//front/report | .//front/confgrp | ..//front/thesgrp | .//bibcom/report | .//bibcom/confgrp | ..//bibcom/thesgrp  | .//bbibcom/report | .//bbibcom/confgrp | ..//bbibcom/thesgrp "/>
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
		<contrib>
			<!-- xsl:if test="contains($corresp,.//fname) and contains($corresp,//surname)"><xsl:attribute name="corresp">yes</xsl:attribute></xsl:if> -->
			<xsl:apply-templates select="@*[name()!='rid']"/>
			<xsl:apply-templates select="."/>
			<xsl:choose>
				<xsl:when test="xref[@ref-type='aff'] and count($affs)&gt;1">
					<xsl:apply-templates select="xref[@ref-type='aff']"/>
				</xsl:when>
				<xsl:when test="@rid!='' and count($affs)&gt;1">
					<xsl:apply-templates select="@rid"/>
				</xsl:when>
			</xsl:choose>


			<xsl:apply-templates select="xref[@ref-type!='aff']"/>
		</contrib>
	</xsl:template>

	<xsl:template match="authgrp/corpauth" mode="front">
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
	<xsl:template match="author/sup">
		<xsl:value-of select=".//text()"/>
	</xsl:template>
	<xsl:template match="author/sup" mode="aff-label">
		<xsl:variable name="sup" select="."/>
		<xsl:if test="not($xref_id[@id=$sup])">
			<xsl:value-of select=".//text()"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="author/@rid">
		<xref ref-type="aff" rid="aff{substring(normalize-space(.),3,1)}">
			<xsl:apply-templates select="..//sup" mode="aff-label"/>
		</xref>
		<xsl:if test="string-length(normalize-space(.))&gt;3">
			<xref ref-type="aff" rid="aff{substring(substring-after(normalize-space(.),' '),3,1)}">
				<xsl:apply-templates select="..//sup" mode="aff-label"/>
			</xref>
		</xsl:if>
	</xsl:template>

	<xsl:template match="aff">
		<aff>
			<xsl:apply-templates select="@id"/>
			<xsl:apply-templates select="label|sup|text()"/>

			
			<xsl:apply-templates select="@*[name()!='id']"/>
			<xsl:if test="country | city">, </xsl:if>
			<xsl:apply-templates select="*[name()!='label' and name()!='sup']"/>


		</aff>
	</xsl:template>

	<xsl:template match="aff/label | aff/country">
		<xsl:element name="{name()}">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="aff/text()"> </xsl:template>
	<xsl:template match="aff/sup">
		<xsl:if test="not(../label)">
			<label>
				<xsl:value-of select="."/>
			</label>
		</xsl:if>
	</xsl:template>

	<xsl:template match="aff/@id">
		<xsl:attribute name="id">aff<xsl:value-of select="substring(.,3)"/></xsl:attribute>
	</xsl:template>

	<xsl:template match="aff/@orgdiv1 | aff/@orgdiv2 | aff/@orgdiv3 | aff/@orgname">
		<xsl:if test="name()!='orgname'">, </xsl:if> 
		<institution>
			<xsl:attribute name="content-type"><xsl:value-of select="name()"/></xsl:attribute>
			<xsl:value-of select="."/>
		</institution></xsl:template>

	<xsl:template match="aff/city">
		<addr-line>
			<named-content content-type="city"><xsl:value-of select="."/></named-content>, <xsl:if
				test="../state">
				<named-content content-type="state"><xsl:value-of select="../state"
					/></named-content>, </xsl:if>
			<xsl:if test="../zipcode">
				<named-content content-type="zipcode"><xsl:value-of select="../zipcode"
					/></named-content>, </xsl:if></addr-line>
	</xsl:template>

	<xsl:template match="aff/state">
		<xsl:if test="not(../city)">
			<addr-line><named-content content-type="state"><xsl:value-of select="."
					/></named-content>, <xsl:if test="../zipcode">
					<named-content content-type="zipcode"><xsl:value-of select="../zipcode"
						/></named-content>, </xsl:if></addr-line>
		</xsl:if>
	</xsl:template>

	<xsl:template match="aff/zipcode">
		<xsl:if test="not(../city) and not(../state)">
			<addr-line><named-content content-type="zipcode"><xsl:value-of select="../zipcode"
					/></named-content>,</addr-line>
		</xsl:if>
	</xsl:template>



	<xsl:template match="e-mail|email">
		<email>
			<xsl:apply-templates/>
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
				<xsl:variable name="fpage">
					<xsl:value-of select="substring-before(.,'-')"/>
				</xsl:variable>
				<xsl:variable name="lpage">
					<xsl:value-of select="substring-after(.,'-')"/>
				</xsl:variable>

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

	<xsl:template match="tified"> </xsl:template>

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

	<xsl:template match="*[@standard]/*[contains(name(),'citat')]">
		<xsl:variable name="id">
			<xsl:if test="position()&lt;10">0</xsl:if>
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
					<xsl:when test=".//degree">thesis</xsl:when>
					<xsl:when test=".//patgrp">patent</xsl:when>
					<xsl:when test=".//report">report</xsl:when>
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
		<xsl:if test=".//*[fname] or .//*[contains(name(),'corpaut')]">
			<person-group person-group-type="{$type}">
				<xsl:apply-templates
					select=".//*[fname] | .//*[contains(name(),'corpaut')] | .//et-al"
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
	<xsl:template match="*[contains(name(),'author')]">
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
		<xsl:apply-templates select="$data4previous[$position - 1]//*[contains(name(),'author')]">
			<xsl:with-param name="position" select="$position - 1"/>
		</xsl:apply-templates>
	</xsl:template>


	<xsl:template match="back//date">
		<xsl:call-template name="display_date">
			<xsl:with-param name="dateiso">
				<xsl:value-of select="@dateiso"/>
			</xsl:with-param>
			<xsl:with-param name="date">
				<xsl:value-of select="."/>
			</xsl:with-param>
		</xsl:call-template>
	</xsl:template>
	<xsl:template match="back//cited">
		<date-in-citation content-type="access-date">
			<xsl:value-of select="."/>
		</date-in-citation>
	</xsl:template>

	<xsl:template match="*[contains(name(),'contrib')]">
		<xsl:param name="position"/>

		<xsl:if test=".//fname or .//surname or .//orgname">
			<person-group person-group-type="author">
				<xsl:apply-templates select="*[contains(name(),'aut')]|et-al">
					<xsl:with-param name="position" select="$position"/>
				</xsl:apply-templates>
			</person-group>
		</xsl:if>

		<xsl:apply-templates select=".//title"/>
	</xsl:template>


	<xsl:template match="*[contains(name(),'serial')]">
		<xsl:apply-templates/>
	</xsl:template>

	<xsl:template match="url | uri">
		<ext-link ext-link-type="uri" xlink:href="{.}">
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


	<xsl:template match="back//*[contains(name(),'monog')]//title">
		<xsl:variable name="lang">
			<xsl:value-of select="../../../..//title/@language"/>
		</xsl:variable>
		<source xml:lang="{$lang}">
			<xsl:apply-templates select="*|text()"/>
			<xsl:apply-templates select="../subtitle" mode="title"/>
		</source>

	</xsl:template>
	<xsl:template match="back//*[contains(name(),'contrib')]//title">
		<xsl:variable name="title">
			<xsl:apply-templates select="*|text()"/>
			<xsl:apply-templates select="../subtitle" mode="title"/>
		</xsl:variable>
		<xsl:variable name="t" select="normalize-space($title)"/>
		<xsl:choose>
			<xsl:when
				test="../..//node()[contains(name(),'monog')] or ../../..//node()[contains(name(),'vmonog')]">
				<chapter-title>
					<xsl:apply-templates select="*|text()"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
				</chapter-title>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
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
	<xsl:template match="stitle | vmonog/vtitle/title ">
		<xsl:variable name="lang">
			<xsl:value-of select="../../../..//title/@language"/>
		</xsl:variable>
		<source xml:lang="{$lang}">

			<xsl:apply-templates select="*|text()"/>
		</source>
	</xsl:template>
	<xsl:template match="*[contains(name(),'serial')]/sertitle">
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
	<xsl:template match="xref/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="xref/@rid">
		<xsl:variable name="rid" select="."/>

		<xsl:if test="$xref_id[@id=$rid] or 'r'=substring($rid,1,1)">
			<xsl:choose>

				<xsl:when test="../@ref-type='aff'">
					<xsl:attribute name="rid">aff<xsl:value-of select="substring(.,3,1)"
						/></xsl:attribute>
				</xsl:when>
				<xsl:when test="../@ref-type='bibr'">
					<xsl:attribute name="rid">B<xsl:value-of select="substring(.,2)"
						/></xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="rid">
						<xsl:value-of select="."/>
					</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>

		</xsl:if>
	</xsl:template>

	<xsl:template match="xref[@rid!='']">
		<xsl:variable name="rid" select="@rid"/>

		<xsl:choose>
			<xsl:when test="@ref-type='bibr'">
				<xref>
					<xsl:apply-templates select="@*"/>
					<xsl:apply-templates select="*|text()"/>
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
				<xsl:comment><xsl:value-of select="$rid"/><xsl:apply-templates select="$xref_id" mode="display-id"/></xsl:comment>
				<xsl:value-of select="."/>
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
		<disp-formula>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="." mode="graphic"/>
		</disp-formula>
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
	<xsl:template match="p[normalize-space(.//text())='']"/>

	<xsl:template name="display_date">
		<xsl:param name="dateiso"/>
		<xsl:param name="date" select="''"/>
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
		<comment>
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
	<xsl:template match="front//report | bbibcom//report">
		<funding-group>
			<xsl:apply-templates select="rsponsor | projname "/>
			<!--xsl:if test="not($unident_back[contains(.//text,'ACK') or contains(.//text,'Ack') or contains(.//text,'Agrad') or contains(.//text,'AGRAD')])"-->
			<funding-statement>
				<xsl:apply-templates select=".//text()"/>
			</funding-statement>
			<!--/xsl:if-->
		</funding-group>
	</xsl:template>
	<xsl:template match="front//rsponsor | front//projname| bbibcom//rsponsor | bbibcom//projname">
		<xsl:if test="orgname or contract">
			<award-group>
				<xsl:attribute name="award-type">
					<xsl:choose>
						<xsl:when test=".//contract">contract</xsl:when>
						<xsl:otherwise>grant</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:apply-templates select="orgname"/>
				<xsl:apply-templates select="contract"/>

			</award-group>
		</xsl:if>
	</xsl:template>
	<xsl:template match="front//contract | bbibcom//contract">
		<award-id>
			<xsl:apply-templates/>
		</award-id>
	</xsl:template>
	<xsl:template match="front//rsponsor/orgdiv | bbibcom//orgdiv"/>
	<xsl:template match="front//rsponsor/orgname | bbibcom//orgname">
		<funding-source>
			<xsl:value-of select="."/>
			<xsl:if test="../orgdiv">, <xsl:value-of select="../orgdiv"/>
			</xsl:if>
		</funding-source>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//report">
		<comment>
			<xsl:apply-templates select="*|text()"/>
		</comment>
	</xsl:template>
	<xsl:template
		match="*[contains(name(),'citat')]//report//* | *[contains(name(),'citat')]//report//rsponsor">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>

	<xsl:template match="*[contains(name(),'citat')]//report//text()">
		<xsl:value-of select="."/>
	</xsl:template>
</xsl:stylesheet>
