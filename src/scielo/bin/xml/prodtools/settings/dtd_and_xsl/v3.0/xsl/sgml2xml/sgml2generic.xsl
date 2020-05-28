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
		<xsl:when test=".//extra-scielo/print-issn!=''">epub-ppub</xsl:when>
		<xsl:when test=".//extra-scielo/e-issn!=''">epub</xsl:when>
	</xsl:choose></xsl:variable>
	<xsl:variable name="unident" select="//unidentified"/>
	<xsl:variable name="corresp" select="//corresp"/>
	
	<xsl:variable name="allfootnotes" select=".//*[(name()='fn' or name()='fngrp') and @fntype]"/>
	<xsl:variable name="fn_deceased" select="$allfootnotes[@fntype='deceased']"/>
	<xsl:variable name="fn_eqcontrib" select="$allfootnotes[@fntype='equal']"/>
	<xsl:variable name="unident_back" select="//back//unidentified"/>
	
	
	<xsl:variable name="affs" select=".//aff"/>
	<xsl:variable name="normalized_affs" select=".//normaff"/>
	<xsl:variable name="affs_xrefs" select=".//front//author"/>
	<xsl:variable name="xref_rid" select="//xref[@rid]"/>
	<xsl:variable name="elem_id" select="//*[@id]"/>
	<xsl:variable name="qtd_ref" select="count(//*[@standard]/*)"/>
	<xsl:variable name="reflen"><xsl:choose>
		<xsl:when test="string-length($qtd_ref)&gt;2"><xsl:value-of select="string-length($qtd_ref)"/></xsl:when>
		<xsl:otherwise>2</xsl:otherwise>
	</xsl:choose></xsl:variable>
	
	<xsl:variable name="ref_no" select="//*[contains(name(),'citat')]/no"/>
	<xsl:variable name="this_doi"><xsl:choose>
		<xsl:when test="node()/front/doi"><xsl:value-of select="node()/front/doi"/></xsl:when>
		<xsl:otherwise><xsl:value-of select="node()/doi"/></xsl:otherwise>
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
	<xsl:variable name="lang"><xsl:value-of select="node()/@language"/></xsl:variable>
	<xsl:template match="*" mode="license-text">
		<xsl:param name="lang" select="$lang"/>
		<xsl:choose>
			<xsl:when test="$lang='pt'">Este é um artigo publicado em acesso aberto sob uma licença Creative Commons</xsl:when>
			<xsl:when test="$lang='es'">Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons</xsl:when>
			<xsl:otherwise>This is an open-access article distributed under the terms of the Creative Commons Attribution License</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
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
		<xsl:attribute name="{name()}"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template><!-- attributes -->
	
	<xsl:template match="text()" mode="copy-of">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>
	<!-- nodes -->
	<xsl:template match="*" mode="copy-of">
		<xsl:element name="{name()}">
		<xsl:apply-templates select="@*| * | text()" mode="copy-of"/>
		</xsl:element>
	</xsl:template>
	
	<!-- attributes -->
	<xsl:template match="@*" mode="copy-of">
		<xsl:attribute name="{name()}"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template><!-- attributes -->
	
	<xsl:template match="fngrp/@id | fn/@id">
		<xsl:attribute name="{name()}">fn<xsl:value-of select="string(number(substring(.,3)))"/></xsl:attribute>
	</xsl:template>
	
	<!--
    	mode=text
	-->
	<xsl:template match="*" mode="text-only">
		<xsl:apply-templates select="*|text()" mode="text-only"/>
	</xsl:template>
	<xsl:template match="text()" mode="text-only">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="sup">
		<xsl:param name="id"/>
		<xsl:choose>
			<xsl:when test=".='(' and following-sibling::node()[1][@ref-type='bibr']">
				<!--ignore ( que é para identificar xref numerico bibr -->
			</xsl:when>
			<xsl:when test=".=')' and preceding-sibling::node()[1][@ref-type='bibr']">
				<!--ignore ) que é para identificar xref numerico bibr  -->
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{name()}">
					<xsl:apply-templates select="@* | * | text()">
						<xsl:with-param name="id" select="$id"/>
					</xsl:apply-templates>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="sub | italic | bold">
		<xsl:param name="id"/>
		<xsl:variable name="parent_name"><xsl:apply-templates select="parent::node()" mode="name"/></xsl:variable>
		<xsl:variable name="parent_text"><xsl:apply-templates select="parent::node()" mode="text-only"/></xsl:variable>
		<xsl:variable name="text"><xsl:apply-templates select="." mode="text-only"/></xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($parent_name, 'title') or $parent_name='label'">
				<xsl:choose>
					<xsl:when test="$parent_text=$text">
						<xsl:apply-templates select="*|text()">
							<xsl:with-param name="id" select="$id"/>
						</xsl:apply-templates>
					</xsl:when>
					<xsl:otherwise>
						<!-- cria o elemento sub italic ou bold identifica parte do título e não o título completo -->
						<xsl:element name="{name()}">
							<xsl:apply-templates select="*|text()">
								<xsl:with-param name="id" select="$id"/>
							</xsl:apply-templates>
						</xsl:element>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{name()}">
					<xsl:apply-templates select="@* | * | text()">
						<xsl:with-param name="id" select="$id"/>
					</xsl:apply-templates>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="ref//sup | ref//sub | ref//bold | ref//italic">
		<xsl:param name="id"/>
		<xsl:variable name="parent_textonly"><xsl:apply-templates select="parent::node()" mode="text-only"/></xsl:variable>
		<xsl:variable name="textonly"><xsl:apply-templates select="*|text()" mode="text-only"/></xsl:variable>
		
		<xsl:choose>
			<xsl:when test="not(*) and normalize-space(translate(text(),'(),.-:;[]/','          '))=''">
				<!-- sup, sub, bold, italic é vazio: ignore -->
			</xsl:when>
			<xsl:when test="normalize-space($parent_textonly)=normalize-space($textonly)">
				<!-- ignore styles -->
				<xsl:apply-templates select="*|text()"/>
			</xsl:when>
			<xsl:otherwise>
				<!-- mantem o bold ou italic se está inserido em um elemento que contem texto alem de bold e/ou italic -->
				<xsl:element name="{name()}">
					<xsl:apply-templates select="@* | * | text()">
						<xsl:with-param name="id" select="$id"/>
					</xsl:apply-templates>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="ref/sup | ref/sub | ref/bold | ref/italic | ref/text()">
		<!-- ignore -->
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
				<xsl:apply-templates select="*[name()!='p']|text()"/>
			</title>
			<xsl:apply-templates select="p"></xsl:apply-templates>
		</caption>
	</xsl:template>

	<xsl:template match="et-al | etal">
		<etal/>
	</xsl:template>
	<xsl:template match="ign"/>
	<xsl:template match="list">
		<xsl:choose>
			<xsl:when test="parent::li or parent::quote" >
				<list>
					<xsl:apply-templates select="@*|*"/>
				</list>
			</xsl:when>
			<xsl:otherwise>
				<p>
					<list>
						<xsl:apply-templates select="@*|*"/>
					</list>
				</p>
			</xsl:otherwise>
		</xsl:choose>
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
				<xsl:when test="p">
					<xsl:apply-templates select="*[name()!='label']"/>
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
	
	<!--FIXME-STYLE
	<xsl:template match="label//bold | label//italic | label//sup">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	-->

	<xsl:template match="source">
		<xsl:param name="id"/>
		
		<xsl:element name="{name()}">
			<xsl:apply-templates select="*|text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="attrib | series | app | anonym | isbn | glossary | term | def | response | p | sec | label | subtitle | edition |  issn | corresp | ack | tbody | td | tr">
		<xsl:param name="id"/>
		
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@* | * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="label[.//text()='(']//text()">*</xsl:template>
	<xsl:template match="label[.//text()='((']//text()">**</xsl:template>
	
	<xsl:template match="appgrp">
		<xsl:param name="id"/>
		<app-group>
			<xsl:apply-templates select="*|text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</app-group>
	</xsl:template>
	
	<xsl:template match="graphic">
		<xsl:apply-templates select="." mode="elem-graphic"/>
	</xsl:template>
	
	<xsl:template match="sec/graphic">
		<p>
			<xsl:apply-templates select="." mode="elem-graphic"/>
		</p>
	</xsl:template>
	
	<xsl:template match="@resptp">
		<xsl:attribute name="response-type"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template>
	
	<xsl:template match="subart | subdoc">
		<xsl:param name="parentid"/>
		<sub-article>
			<xsl:apply-templates select="@*">
				<xsl:with-param name="parentid" select="$parentid"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="front-stub">
				<xsl:with-param name="language" select="@language"/>
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="body">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="back">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="response | subart | docresp | subdoc">
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates>
		</sub-article>
	</xsl:template>
	
	<xsl:template match="response | docresp">
		<xsl:param name="parentid"/>
		<response>
			<xsl:apply-templates select="@*">
				<xsl:with-param name="parentid" select="$parentid"></xsl:with-param>
			</xsl:apply-templates>
			<!--xsl:apply-templates select="." mode="front">
				<xsl:with-param name="language" select="@language"/>
				<xsl:with-param name="parentid" select="@id"></xsl:with-param>
			</xsl:apply-templates-->
			<xsl:apply-templates select="." mode="front-stub">
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
	
	<!--xsl:template match="subart/@id | subdoc/@id">
		<xsl:attribute name="id"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
	</xsl:template-->
	
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
			<xsl:if test="not($allfootnotes[@fntype=name()])">
				<xsl:attribute name="{name()}">yes</xsl:attribute>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="@eqcontr">
		<xsl:if test=".='yes'">
			<xsl:if test="not($allfootnotes[@fntype='eq-contrib'])">
				<xsl:attribute name="eq-contrib">yes</xsl:attribute>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="sigblock">
		<xsl:param name="id"/>
		<sig-block>
			<xsl:apply-templates select="@*| * | text()" mode="sig-block">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</sig-block>
	</xsl:template>
	
	<xsl:template match="sigblock//role">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="role" mode="sig-block">
	</xsl:template>
	
	<xsl:template match="sig" mode="sig-block">
		<xsl:element name="{name()}">
			<xsl:apply-templates select=".//text()"/><xsl:if test="..//role"><break/><xsl:apply-templates select="..//role"/></xsl:if>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="version">
		<edition>
			<xsl:value-of select="normalize-space(.)"/>
		</edition>
	</xsl:template>
	
	<xsl:template match="issn">
		<xsl:variable name="issn"><xsl:value-of select="normalize-space(.)"/></xsl:variable>
		<xsl:choose>
			<xsl:when test="string-length($issn)=9 and substring($issn,5,1)='-'">
				<issn><xsl:value-of select="$issn"/></issn>
			</xsl:when>
			<xsl:when test="contains($issn,'PMID:')">
				<pub-id pub-id-type="pmid">
					<xsl:value-of select="substring-after($issn, 'PMID:')"/>
				</pub-id>
			</xsl:when>
			<xsl:otherwise><xsl:value-of select="$issn"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="@doctopic" mode="type">
		<xsl:attribute name="article-type">
			<xsl:choose>
				<xsl:when test=".='oa'">research-article</xsl:when>
				<xsl:when test=".='co'">article-commentary</xsl:when>
				<xsl:when test=".='cr'">case-report</xsl:when>
				<xsl:when test=".='ct'">research-article</xsl:when>
				<xsl:when test=".='ed'">editorial</xsl:when>
				<xsl:when test=".='em'">editorial</xsl:when>
				<xsl:when test=".='er'">correction</xsl:when>
				<xsl:when test=".='le'">letter</xsl:when>
				<xsl:when test=".='pr'">in-brief</xsl:when>
				<xsl:when test=".='ra'">review-article</xsl:when>
				<xsl:when test=".='rc'">book-review</xsl:when>
				<xsl:when test=".='re'">retraction</xsl:when>
				<xsl:when test=".='rn'">brief-report</xsl:when>
				<xsl:when test=".='sc'">rapid-communication</xsl:when>
				<xsl:when test=".='tr'">research-article</xsl:when><!-- technical report -->
				<xsl:when test=".='zz'">other</xsl:when>
				
				<xsl:when test=".='partial-retraction'">partial-retraction</xsl:when>
				<xsl:when test=".='reply'">reply</xsl:when>
				
				<xsl:when test=".='ab'">abstract</xsl:when>
				<xsl:when test=".='an'">announcement</xsl:when>
				<xsl:when test=".='??'">other</xsl:when>
				<xsl:when test=".='addendum'">addendum</xsl:when>
				<xsl:when test=".='guideline'">guideline</xsl:when>
				<xsl:when test=".='books-received'">books-received</xsl:when>
				<xsl:when test=".='calendar'">calendar</xsl:when>
				<xsl:when test=".='??'">collection</xsl:when>
				<xsl:when test=".='discussion'">discussion</xsl:when>
				<xsl:when test=".='dissertation'">dissertation</xsl:when>
				<xsl:when test=".='??'">introduction</xsl:when>
				<xsl:when test=".='meeting-report'">meeting-report</xsl:when>
				<xsl:when test=".='news'">news</xsl:when>
				<xsl:when test=".='obituary'">obituary</xsl:when>
				<xsl:when test=".='oration'">oration</xsl:when>
				<xsl:when test=".='product-review'">product-review</xsl:when>
				<xsl:when test=".='reprint'">reprint</xsl:when>
				<xsl:when test=".='translation'">translation</xsl:when>
				<xsl:when test=".='ax'">other</xsl:when>
				<xsl:when test=".='in'">interview</xsl:when>
				<xsl:when test=".='mt'">research-article</xsl:when><!-- methodology -->
				<xsl:when test=".='pv'">editorial</xsl:when><!-- ponto de vista -->
				<!-- -->
				<xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
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
	<xsl:template match="@sps">
		<xsl:attribute name="specific-use">sps-<xsl:choose>
			<xsl:when test="contains(.,'sps-')"><xsl:value-of select="substring-after(.,'sps-')"/></xsl:when>
			<xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
		</xsl:choose></xsl:attribute>
	</xsl:template>
	<xsl:template match="article|text|doc">
		<article>
			<xsl:apply-templates select="." mode="dtd-version"/>
			<xsl:apply-templates select="@doctopic" mode="type"/>
			<xsl:apply-templates select="@language"/>
			<xsl:apply-templates select="@sps"/>
			<xsl:apply-templates select="." mode="front">
				<xsl:with-param name="language" select="@language"/>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="body"/>
			<xsl:apply-templates select="." mode="back"/>
			<xsl:apply-templates select="response | subart | docresp | subdoc"/>
		</article>
	</xsl:template>
	<xsl:template match="article|text|doc|response|docresp" mode="front">
		<xsl:param name="language"/>
		<front>
			<xsl:apply-templates select="." mode="journal-meta"/>
			<xsl:apply-templates select="." mode="article-meta">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>					
		</front>
	</xsl:template>
	<xsl:template match="subart|response|subdoc|docresp" mode="front-stub">
		<xsl:param name="language"/>
		<front-stub>
			<xsl:if test="not(.//toctitle)">
				<xsl:apply-templates select="." mode="toctitle"/>
			</xsl:if>
			<xsl:apply-templates select=".//toctitle"/>
			<xsl:apply-templates select="." mode="title-group">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>
		
			<xsl:apply-templates select="." mode="front-contrib-group"/>
			<xsl:apply-templates select="." mode="author-notes"/>
			
			<xsl:apply-templates select=".//cltrial" mode="front-clinical-trial"/>
			<xsl:apply-templates select=".//abstract|.//xmlabstr">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>
			<xsl:apply-templates select=".//keygrp|.//kwdgrp">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>									
		</front-stub>
	</xsl:template>
	<xsl:template match="article|text|doc" mode="journal-meta">
		<journal-meta>
			<xsl:if test=".//nlm-title and .//nlm-title!=''">
				<journal-id journal-id-type="nlm-ta">
					<xsl:value-of select=".//nlm-title"/>
				</journal-id>
			</xsl:if>
			<journal-id journal-id-type="publisher-id">
				<xsl:value-of select="$journal_acron"/>
			</journal-id>
			<journal-title-group>
				<xsl:if test=".//journal-title!=''">
					<xsl:apply-templates select=".//journal-title" mode="copy-of"></xsl:apply-templates>
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
				<subject><xsl:value-of select="normalize-space(.)"/></subject>
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
	
	<xsl:template match="article | text | response | subart" mode="front-contrib-group">
		<xsl:apply-templates select="front/authgrp | authgrp" mode="front-contrib-group"/>
		
		<xsl:if test="sigblock and not(authrgrp) and not(front/authgrp)">
			<contrib-group>
				<xsl:apply-templates select="sigblock/sig[fname and surname]" mode="front-contrib-group"/>
				<xsl:if test="count(normaff)=1">
					<xsl:apply-templates select="normaff"/>
				</xsl:if>
			</contrib-group>
			<xsl:if test="count(normaff)&gt;1">
				<xsl:apply-templates select="normaff"/>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="sig[fname and surname]" mode="front-contrib-group">
		<!-- author front -->
		<contrib>
			<xsl:apply-templates select="@role"/>
			<xsl:apply-templates select="."/>
			<xsl:apply-templates mode="copy-of"  select="../role"/>
			<xsl:choose>
				<xsl:when test="xref">
					<xsl:apply-templates select="xref"/>
				</xsl:when>
				<xsl:when test="@rid">
					<xref ref-type="aff" rid="{@rid}"/>
				</xsl:when>
			</xsl:choose>
		</contrib>
	</xsl:template>
	
	<xsl:template match="authgrp" mode="front-contrib-group">
		<contrib-group>
			<xsl:apply-templates select="author|corpauth" mode="front-contrib"/>
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
	
	<xsl:template match="doc | subdoc | docresp" mode="front-contrib-group">
		<xsl:choose>
			<xsl:when test=".//aff">
				<aff content-type="USE normaff instead of aff"></aff>
			</xsl:when>
			<xsl:when test="author or corpauth">
				<contrib-group>
					<xsl:apply-templates select="author|corpauth" mode="front-contrib"/>
					<xsl:if test="onbehalf">
						<on-behalf-of>
							<xsl:value-of select="onbehalf"/>
						</on-behalf-of>
					</xsl:if>
					<xsl:if test="count(normaff)=1">
						<xsl:apply-templates select="normaff"/>
					</xsl:if>
					<xsl:if test="count(afftrans)=1">
						<xsl:apply-templates select="afftrans"/>
					</xsl:if>
				</contrib-group>
				<xsl:if test="count(normaff)&gt;1">
					<xsl:apply-templates select="normaff"/>
				</xsl:if>
				<xsl:if test="count(afftrans)&gt;1">
					<xsl:apply-templates select="afftrans"/>
				</xsl:if>
			</xsl:when>
			<xsl:when test="xmlbody/sigblock">
				<contrib-group>
					<xsl:apply-templates select="xmlbody/sigblock/sig[fname and surname]" mode="front-contrib-group"/>
					<xsl:if test="count(normaff)=1">
						<xsl:apply-templates select="normaff"/>
					</xsl:if>
				</contrib-group>
				<xsl:if test="count(normaff)&gt;1">
					<xsl:apply-templates select="normaff"/>
				</xsl:if>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	<!--xsl:template match="cltrial" mode="front-clinical-trial">
		<uri>
			<xsl:attribute name="content-type">clinical-trial</xsl:attribute>
			<xsl:attribute name="xlink:href"><xsl:value-of select="ctreg/@cturl"/></xsl:attribute>
			<xsl:apply-templates select=".//text()"></xsl:apply-templates>
		</uri>
	</xsl:template>
	<xsl:template match="cltrial">
		<uri>
			<xsl:attribute name="xlink:href"><xsl:value-of select="ctreg/@cturl"/></xsl:attribute>
			<xsl:apply-templates select=".//text()"></xsl:apply-templates>
		</uri>
	</xsl:template-->
	<xsl:template match="cltrial" mode="front-clinical-trial">
		<ext-link>
			<xsl:attribute name="ext-link-type">clinical-trial</xsl:attribute>
			<xsl:attribute name="xlink:href"><xsl:value-of select="ctreg/@cturl"/></xsl:attribute>
			<xsl:apply-templates select=".//text()"></xsl:apply-templates>
		</ext-link>
	</xsl:template>
	<xsl:template match="cltrial">
		<ext-link>
			<xsl:attribute name="xlink:href"><xsl:value-of select="ctreg/@cturl"/></xsl:attribute>
			<xsl:apply-templates select=".//text()"></xsl:apply-templates>
		</ext-link>
	</xsl:template>
	
	<xsl:template match="article|text|doc" mode="article-meta">
		<xsl:param name="language"/>
		<article-meta>
			<xsl:apply-templates select="front/doi|doi"/>
			
			<xsl:variable name="fpage_number"><xsl:choose>
				<xsl:when test="@fpageseq"><xsl:value-of select="@fpage"/></xsl:when>
				<xsl:when test="contains(@fpage,'-')">
					<xsl:value-of select="substring-before(@fpage,'-')"/>
				</xsl:when>
				<xsl:when test="contains(@fpage,string(number(@fpage)))"><xsl:value-of select="@fpage"/></xsl:when>
				<xsl:otherwise>0</xsl:otherwise>
			</xsl:choose></xsl:variable>
			
			<xsl:if test="not(front/doi) and not(doi)">
				<xsl:variable name="order"><xsl:value-of select="substring-after(string(100000 + number(@order)),'1')"/></xsl:variable>
				<article-id pub-id-type="publisher-id"><xsl:value-of select="$order"/></article-id>
				<xsl:choose>
					<xsl:when test="normalize-space(translate($fpage_number,'0123456789','          '))!='' or @fpageseq!=''">
						<article-id pub-id-type="other"><xsl:value-of select="$order"/></article-id>						
					</xsl:when>
					<xsl:when test="number($fpage_number)&lt;number(@order)">
						<article-id pub-id-type="other"><xsl:value-of select="$order"/></article-id>						
					</xsl:when>
				</xsl:choose>				
			</xsl:if>
			<xsl:if test="@ahppid!=''"><article-id specific-use="previous-pid"><xsl:value-of select="@ahppid"/></article-id></xsl:if>

			<xsl:apply-templates select="front/toctitle|toctitle"></xsl:apply-templates>
			<xsl:if test="not(front/toctitle) and not(toctitle)">
				<xsl:apply-templates select="." mode="toctitle"></xsl:apply-templates>
			</xsl:if>
			
			<xsl:apply-templates select="." mode="title-group">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="front-contrib-group"/>
			<xsl:apply-templates select="." mode="author-notes"/>

			<xsl:apply-templates select="." mode="pub-date"/>

			<xsl:apply-templates select="@volid"/>
			<xsl:apply-templates select="@issueno"/>
			<xsl:apply-templates select="@fpage"/>
			<xsl:apply-templates select="@lpage"/>
			<xsl:apply-templates select="@elocatid"/>
			
			<xsl:apply-templates select="product|front/product|xmlbody/product|back/product" mode="product-in-article-meta"/>
			<xsl:apply-templates select="cltrial|front/cltrial|back//cltrial|xmlbody//cltrial" mode="front-clinical-trial"/>
			<xsl:apply-templates select="hist|front//hist|back//hist"/>
			
			<xsl:apply-templates select="cpright | licinfo"/>
			<xsl:if test="not(cpright) and not(licinfo)">
				<permissions>
				<xsl:apply-templates select="back/licenses| cc | .//extra-scielo/license"/>
				</permissions>
			</xsl:if>
			
			<xsl:apply-templates select="front/related|related" mode="front-related"/>
			<xsl:apply-templates select="back//related|xmlbody//related" mode="front-related"/>
			
			<xsl:apply-templates select="abstract[@language=$language or not(@language)]|xmlabstr[@language=$language or not(@language)]"/>
			<xsl:apply-templates select="front//abstract[@language=$language or not(@language)]|front//xmlabstr[@language=$language or not(@language)]"/>
			<xsl:apply-templates select="back//abstract[@language=$language or not(@language)]|back//xmlabstr[@language=$language or not(@language)]"/>
			
			<xsl:apply-templates select="abstract[@language!=$language]|xmlabstr[@language!=$language]"
				><xsl:with-param name="trans" select="'trans-'"/></xsl:apply-templates>
			<xsl:apply-templates select="front//abstract[@language!=$language]|front//xmlabstr[@language!=$language]"
				><xsl:with-param name="trans" select="'trans-'"/></xsl:apply-templates>
			<xsl:apply-templates select="back//abstract[@language!=$language]|back//xmlabstr[@language!=$language]"
				><xsl:with-param name="trans" select="'trans-'"/></xsl:apply-templates>
			
			<xsl:apply-templates select="front/keygrp|back/keygrp|kwdgrp">
				<xsl:with-param name="language" select="$language"/>
			</xsl:apply-templates>
			
			<xsl:apply-templates
				select="front//report | back//bbibcom/report | back/ack//report | ack//funding" mode="front-funding-group"/>
			<xsl:apply-templates
				select="fngrp//report|fngrp//funding|fn//report|fn//funding" mode="front-funding-group">
				<xsl:with-param name="statement">true</xsl:with-param>
			</xsl:apply-templates>
			
			<xsl:apply-templates
				select="confgrp | front//confgrp | back//bbibcom/confgrp | thesgrp | front//thesgrp | back//bbibcom/thesgrp"/>
		</article-meta>
	</xsl:template>
	<xsl:template match="doc | subdoc | docresp" mode="title-group">
		<xsl:param name="language"/>
		<title-group>
			<xsl:apply-templates select="doctitle[@language=$language or not(@language)] "/>
			<xsl:apply-templates select="doctitle[@language!=$language]" mode="trans-title-group"/>
			<xsl:apply-templates select="doctitle//alttitle"/>
		</title-group>
	</xsl:template>
	<xsl:template match="article | subart | response" mode="title-group">
		<xsl:param name="language"/>
		<title-group>
			<xsl:apply-templates select="front/titlegrp/title[@language=$language or not(@language)]"/>
			<xsl:apply-templates select="back/titlegrp/title[@language=$language or not(@language)]"/>
			<xsl:apply-templates select="front/titlegrp/title[@language!=$language]" mode="trans-title-group">
				<xsl:with-param name="subtitles" select="front/titlegrp/subtitle[position()!=1]"/>
			</xsl:apply-templates><xsl:apply-templates select="back/titlegrp/title[@language!=$language]" mode="trans-title-group">
				<xsl:with-param name="subtitles" select="back/titlegrp/subtitle[position()!=1]"/>
			</xsl:apply-templates>
		</title-group>
	</xsl:template>
	<xsl:template match="text" mode="title-group">
		<xsl:param name="language"/>
		<title-group>
			<xsl:apply-templates select="titlegrp/title[@language=$language or not(@language)]"/>
			<xsl:apply-templates select="titlegrp/title[@language!=$language]" mode="trans-title-group">
				<xsl:with-param name="subtitles" select="titlegrp/subtitle[position()!=1]"/>
			</xsl:apply-templates>
		</title-group>
	</xsl:template>
	<xsl:template match="titlegrp/title">
		<article-title>
			<xsl:apply-templates select="@language|*|text()"/>
		</article-title>
		<xsl:apply-templates select="../subtitle[1]"/>
	</xsl:template>
	<xsl:template match="doctitle">
		<article-title>
			<xsl:apply-templates select="*[name()!='subtitle' and name()!='alttitle'] |text()"/>
		</article-title>
		<xsl:apply-templates select="subtitle">
			<xsl:with-param name="lang"><xsl:value-of select="@language"/></xsl:with-param>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="doctitle" mode="trans-title-group">
		<trans-title-group>
			<xsl:apply-templates select="@language"/>
			<trans-title>
			<xsl:apply-templates select="*[name()!='subtitle' and name()!='alttitle'] |text()"></xsl:apply-templates>
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
		<xsl:if test="not($fn_deceased)">
			<xsl:attribute name="{name()}">yes</xsl:attribute>
		</xsl:if>
	</xsl:template>

	<xsl:template match="author/@eqcontr[.='y']">
		<xsl:if test="not($fn_eqcontrib)">
			<xsl:attribute name="equal-contrib">yes</xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template match="authorid/@*">
		<xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="authorid/@authidtp">
		<xsl:attribute name="contrib-id-type"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="authorid">
		<contrib-id>
			<xsl:apply-templates select="@*|*|text()"/>
		</contrib-id>
	</xsl:template>
	<xsl:template match="author" mode="front-contrib">
		<!-- author front -->
		<xsl:variable name="author_rid" select="@rid"/>
		<contrib>
			<!-- xsl:if test="contains($corresp,.//fname) and contains($corresp,//surname)"><xsl:attribute name="corresp">yes</xsl:attribute></xsl:if> -->
			<xsl:apply-templates select="@*[name()!='rid']"/>
			<xsl:apply-templates select=".//authorid"/>
			<xsl:apply-templates select="."/>
			<xsl:apply-templates select=".//xref|role"/>
			<xsl:if test="not(.//xref) and count(../..//afftrans)+count(../..//normaff)+count(../..//aff)=1">
				<xref ref-type="aff" rid="aff1"/>
			</xsl:if>
			<xsl:if test="onbehalf">
				<on-behalf-of>
					<xsl:value-of select="onbehalf"/>
				</on-behalf-of>
			</xsl:if>
			<xsl:apply-templates mode="copy-of"  select="../..//aff[@id=$author_rid]/role"/>
			<xsl:apply-templates mode="copy-of"  select="../..//normaff[@id=$author_rid]/role"/>
		</contrib>
	</xsl:template>
	<xsl:template match="role"><role><xsl:apply-templates/></role></xsl:template>
	<xsl:template match="corpauth" mode="front-contrib">
		<xsl:variable name="teste">
			<xsl:apply-templates select="./../../authgrp//text()"/>
			<xsl:apply-templates select="../text()"/>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($teste,'behalf')">
				<on-behalf-of>
					<xsl:apply-templates select="* | text()"/>
				</on-behalf-of>
			</xsl:when>
			<xsl:otherwise>
				<contrib contrib-type="author">
					<collab>
						<xsl:apply-templates select="* | text()" mode="text-only"/>
					</collab>
				</contrib>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="*" mode="fix-label">
		<xsl:param name="text"></xsl:param>
		<xsl:choose>
			<xsl:when test="$text='('">*</xsl:when>
			<xsl:when test="$text='(('">**</xsl:when>
			<xsl:otherwise><xsl:value-of select="$text"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="aff|normaff|afftrans" mode="label">
		<xsl:choose>
			<xsl:when test="normalize-space(.//label//text())=''">
				<!-- nao gerar label -->
			</xsl:when>
			<xsl:when test="label[sup]">
				<label><xsl:value-of select="label"/></label>
			</xsl:when>
			<xsl:otherwise><label><xsl:value-of select="label"/></label></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="aff | normaff | afftrans">
		<xsl:variable name="parentid"></xsl:variable>
		
		<aff>
			<xsl:apply-templates select="@id"/>
			<xsl:apply-templates select="." mode="label"/>
			<xsl:choose>
				<xsl:when test="institid">
					<institution-wrap>
						<xsl:apply-templates select="institid"></xsl:apply-templates>
					</institution-wrap>
					<xsl:apply-templates select="." mode="institution"></xsl:apply-templates>
					<xsl:apply-templates select="." mode="address"></xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="." mode="institution"></xsl:apply-templates>
					<xsl:apply-templates select="." mode="address"></xsl:apply-templates>
				</xsl:otherwise>
			</xsl:choose>
		</aff>
	</xsl:template>
	<xsl:template match="*" mode="institution">
		<institution content-type="original"><xsl:apply-templates select="*[name()!='label']|text()" mode="original"/></institution>
		<xsl:if test="@orgname">
			<xsl:apply-templates select="@*[name()!='id']"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="*" mode="address">
		<xsl:if test="city or state or zipcode">
			<addr-line>
				<xsl:apply-templates select="city|state|zipcode"/>
			</addr-line>
		</xsl:if>
		<xsl:apply-templates select="country"></xsl:apply-templates>
		<xsl:apply-templates select="email"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="@icountry">
		<xsl:attribute name="country"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="@ncountry">
		<country>
			<xsl:apply-templates select="../@icountry"/>
			<xsl:value-of select="normalize-space(.)"/>
		</country>
	</xsl:template>
	<xsl:template match="aff/country| normaff/country">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="../@icountry"/>
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="aff/email | normaff/email">
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
	
	<xsl:template match="aff | normaff" mode="original">
		<xsl:apply-templates select="*|text()" mode="original"/>
	</xsl:template>
	<xsl:template match="aff//* | normaff//*" mode="original">
		<xsl:value-of select="." xml:space="preserve"/>
	</xsl:template>
	<xsl:template match="aff//text() | normaff//text()" mode="original">
		<xsl:value-of select="." xml:space="preserve"/>
	</xsl:template>
	<xsl:template match="label|label/sup|label/text()" mode="original"></xsl:template>
	
	<xsl:template match="xref/@rid">
		<xsl:variable name="rid"><xsl:value-of select="."/></xsl:variable>
		<xsl:if test="$elem_id[@id=$rid]">
			<xsl:variable name="n1"><xsl:value-of select="substring(.,2)"/></xsl:variable>
			<xsl:variable name="n2"><xsl:if test="contains(.,../@ref-type)"><xsl:value-of select="substring(.,string-length(../@ref-type)+1)"/></xsl:if></xsl:variable>
			<xsl:attribute name="rid"><xsl:choose>
				<xsl:when test="substring($n1,1,1)='0'"><xsl:value-of select="substring(.,1,1)"/><xsl:value-of select="string(number($n1))"/></xsl:when>
				<xsl:when test="substring($n2,1,1)='0'"><xsl:value-of select="../@ref-type"/><xsl:value-of select="string(number($n2))"/></xsl:when>
				<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
			</xsl:choose></xsl:attribute>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="xref[@ref-type='aff']/@rid">
		<xsl:variable name="rid" select="."></xsl:variable>
		<xsl:if test="$elem_id[@id=$rid]">
			<xsl:attribute name="rid"><xsl:choose>
				<xsl:when test="contains(.,'aff')"><xsl:value-of select="normalize-space(.)"/></xsl:when>
				<xsl:otherwise>aff<xsl:value-of select="string(number(substring(.,2)))"/></xsl:otherwise>
			</xsl:choose></xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template match="xref[@ref-type='bibr']/text()">
		<xsl:choose>
			<xsl:when test="substring(.,1,1)='(' and substring(.,string-length(.)-1)=')'">
				<xsl:value-of select="substring(.,2,string-length(.)-2)"/>
			</xsl:when>
			<xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="aff/@id | normaff/@id">
		<!-- FIXMEID -->
		<!-- quando nao ha aff/label = author/xref enquanto author/@rid = aff/@id -->
		<xsl:choose>
			<xsl:when test="contains(.,'aff')"><xsl:attribute name="id"><xsl:value-of select="."/></xsl:attribute></xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="id">aff<xsl:value-of select="string(number(substring(.,2)))"/></xsl:attribute>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="normaff/orgname">
		<institution content-type="orgname"><xsl:value-of select="normalize-space(.)"/></institution>
	</xsl:template>
	<xsl:template match="normaff/*[contains(name(),'orgdiv')]">
		<institution content-type="{name()}"><xsl:value-of select="normalize-space(.)"/></institution>
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

	<xsl:template match="article|text|subart|response" mode="author-notes">
		<xsl:variable name="selectedfn">
			<xsl:apply-templates select="fngrp|fn">
				<xsl:with-param name="fntype">author-notes</xsl:with-param>
			</xsl:apply-templates>
		</xsl:variable>
		<xsl:if test="$corresp or $selectedfn!='' ">
			<author-notes>
				<xsl:apply-templates select="$corresp"/>
				<xsl:apply-templates select="fngrp|fn" mode="authorfn"/>
			</author-notes>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="doc|subdoc|docresp" mode="author-notes">
		<xsl:variable name="selectedfn"><xsl:apply-templates select="fngrp|fn" mode="authorfn"/></xsl:variable>
		<xsl:if test="corresp or $selectedfn!=''">
			<author-notes>
				<xsl:apply-templates select="corresp"/>
				<xsl:apply-templates select="fngrp|fn" mode="authorfn"/>
			</author-notes>
		</xsl:if>
	</xsl:template>
	
	
	<!-- AUTHOR FOOTNOTES -->
	<xsl:template match="fngrp[not(@fntype)]" mode="authorfn">
		<xsl:variable name="selectedfn"><xsl:apply-templates select="fn" mode="authorfn"></xsl:apply-templates></xsl:variable>
		<xsl:if test="$selectedfn!=''">
			<xsl:apply-templates select="fn" mode="authorfn"></xsl:apply-templates>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="fngrp[@fntype]|fn" mode="authorfn">
		<xsl:if test="not(contains('abbr|financial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype))">
			<xsl:apply-templates select="."/>
		</xsl:if>
	</xsl:template>
	<!-- AUTHOR FOOTNOTES - FIM -->
	
	<xsl:template match="fngrp/sectitle">
		<title><xsl:apply-templates select="*|text()"></xsl:apply-templates></title>
	</xsl:template>
	
	<xsl:template match="fngrp/@label|fn/@label">
		<xsl:if test="not(../label)">
			<label><xsl:value-of select="normalize-space(.)"/></label>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="fngrp/@fntype|fn/@fntype">
		<xsl:attribute name="fn-type">
			<xsl:choose>
				<xsl:when test=".='author'">other</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>

	<xsl:template match="fngrp[not(fn)]|fn">		
		<fn>
			<xsl:apply-templates select="@*|label"/>
			<xsl:if test="not(label) and not(@label) and @fntype='other'">
				<label><xsl:value-of select="string(number(substring-after(@id,'fn')))"/></label>
			</xsl:if>
			<p>
				<xsl:apply-templates select="*[name()!='label']|text()"/>
			</p>
		</fn>
	</xsl:template>
	
	<xsl:template match="@volid">
		<volume>
			<xsl:choose>
				<xsl:when test="number(.)=0">00</xsl:when>
				<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
			</xsl:choose>
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
			<xsl:when test=".='ahead' or number(.)=0">
				<xsl:if test="not(../@volid)">
					<volume>00</volume>
				</xsl:if>
				<issue>00</issue>
			</xsl:when>
			<xsl:otherwise>
				<issue>
					<xsl:value-of select="normalize-space(.)"/>
					<xsl:if test="../@supplno"> Suppl<xsl:if test="../@supplno!='0'"> <xsl:value-of select="concat(' ',../@supplno)"/></xsl:if></xsl:if>
					<xsl:if test="../@supplvol"> Suppl<xsl:if test="../@supplvol!='0'"> <xsl:value-of select="concat(' ',../@supplvol)"/></xsl:if></xsl:if>
					<xsl:if test="../@isidpart"><xsl:value-of select="concat(' ',../@isidpart)"/></xsl:if>
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
				<xsl:when test="number(.)=0">00</xsl:when>
				<xsl:when test="contains(.,'-')">
					<xsl:attribute name="seq"><xsl:value-of select="substring-after(.,'-')"/></xsl:attribute>
					<xsl:value-of select="substring-before(.,'-')"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:if test="../@fpageseq">
						<xsl:attribute name="seq"><xsl:value-of select="../@fpageseq"/></xsl:attribute>
					</xsl:if>
					<xsl:value-of select="normalize-space(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</fpage>
	</xsl:template>
	<xsl:template match="@lpage">
		<lpage>
			<xsl:choose>
				<xsl:when test="number(.)=0">00</xsl:when>
				<xsl:when test="contains(.,'-')">
					<xsl:attribute name="seq"><xsl:value-of select="substring-after(.,'-')"/></xsl:attribute>
					<xsl:value-of select="substring-before(.,'-')"/>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
			</xsl:choose>
		</lpage>
	</xsl:template>
	<xsl:template match="@elocatid"><elocation-id><xsl:value-of select="normalize-space(.)"/></elocation-id></xsl:template>
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
				<xsl:value-of select="$pages"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="elocatid">
		<xsl:element name="elocation-id"><xsl:value-of select="."/></xsl:element>
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
				<xsl:variable name="pagination" select="translate(normalize-space(.),',',';')"/>
				<xsl:variable name="page" select="translate($pagination,'-',';')"/>
				<xsl:variable name="lpage">
					<xsl:apply-templates select="." mode="get-lpage">
						<xsl:with-param name="pages" select="substring-after($pagination,';')"/>
					</xsl:apply-templates>
				</xsl:variable>
				<xsl:variable name="fpage"><xsl:value-of select="substring-before($page,';')"/></xsl:variable>
				<fpage><xsl:value-of select="$fpage"/></fpage>
				<lpage>
					<xsl:if test="string-length($lpage)&lt;string-length($fpage)"><xsl:value-of
							select="substring($fpage,1,string-length($fpage) - string-length($lpage))"
						/></xsl:if><xsl:value-of select="$lpage"/>
				</lpage>
				<page-range><xsl:value-of select="normalize-space(.)"/></page-range>
			</xsl:when>
			<xsl:when test="contains(.,'-')">
				<xsl:variable name="fpage" select="substring-before(normalize-space(.),'-')"/>
				<xsl:variable name="lpage" select="substring-after(normalize-space(.),'-')"/>

				<fpage><xsl:value-of select="$fpage"/></fpage>
				<lpage>
					<xsl:if test="string-length($lpage)&lt;string-length($fpage)"><xsl:value-of
						select="substring($fpage,1,string-length($fpage) - string-length($lpage))"
					/></xsl:if><xsl:value-of select="$lpage"/>
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
	<xsl:template match="hist">
		<history>
			<xsl:apply-templates select="*"/>
		</history>
	</xsl:template>
	<xsl:template match="hist/*">
		<xsl:variable name="dtype">
			<xsl:choose>
				<xsl:when test="name()='revised'">rev-recd</xsl:when>
				<xsl:when test="@datetype!=''">
					<xsl:value-of select="@datetype"/>
				</xsl:when>
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
	
	<xsl:template match="abstract|xmlabstr">
		<xsl:param name="trans" select="''"/>
		
		<xsl:element name="{$trans}abstract">
			<xsl:if test="$trans!=''">
				<xsl:attribute name="xml:lang"><xsl:value-of select="@language"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@absttype!='summary'">
				<xsl:attribute name="abstract-type"><xsl:value-of select="@absttype"/></xsl:attribute>
			</xsl:if>
			<xsl:choose>
				<xsl:when test="sectitle or p or sec">
					<xsl:apply-templates select="*|text()"/>
				</xsl:when>
				<xsl:otherwise>
					<p>
						<xsl:apply-templates select="*|text()"/>
					</p>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:element>
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
			<xsl:apply-templates select="sectitle|kwd"/>
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
						<xsl:with-param name="count" select="count(.//equation)-count(.//p/equation)"/>
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
					<xsl:if test="not(@elocatid)">
						<xsl:apply-templates select="." mode="element-counts">
							<xsl:with-param name="element_name" select="'page-count'"/>
							<xsl:with-param name="count" select="@pagcount"/>
						</xsl:apply-templates>
					</xsl:if>						
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
		<title><!--fixme bold|italic|sub|sup-->
			<xsl:apply-templates select="*|text()"/>
			<xsl:apply-templates select="following-sibling::node()[1 and name()='xref']"
				mode="xref-in-sectitle"/>
		</title>
	</xsl:template>

	<!-- BACK -->
	<xsl:template match="article|text|subart|response" mode="back">
		<xsl:if test="fngrp or fn or back/ack or back/fxmlbody or back/*[@standard]">
			<back>
				<xsl:apply-templates select="back"/>
			</back>
		</xsl:if>
	</xsl:template>
		
	<xsl:template match="xref[@ref-type='fn']" mode="fn_xref_rid">
		|<xsl:value-of select="@rid"/>|
	</xsl:template>
	
	<xsl:template match="fn[@id]|fngrp[@id]" mode="exist_fn_other_with_xref">
		<xsl:param name="id_list"></xsl:param>
		<xsl:if test="contains('abbr|financial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype) or not(@fntype)">			
			<xsl:if test="contains($id_list,concat('|',@id,'|'))">
				<xsl:apply-templates select="."></xsl:apply-templates>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="fn[@id]|fngrp[@id]" mode="exist_fn_other_without_xref">
		<xsl:param name="id_list"></xsl:param>
		<xsl:if test="contains('abbr|financial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype) or not(@fntype)">			
			<xsl:if test="not(contains($id_list,concat('|',@id,'|')))">
				<xsl:apply-templates select="."></xsl:apply-templates>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="fngrp[fn]" mode="elem_fn_other_with_xref">
		<xsl:param name="id_list"></xsl:param>
		<xsl:variable name="teste"><xsl:apply-templates select="fn" mode="exist_fn_other_with_xref">
			<xsl:with-param name="id_list" select="$id_list"></xsl:with-param>
		</xsl:apply-templates></xsl:variable>
		<xsl:if test="normalize-space($teste)!=''">
			<fn-group>
				<xsl:apply-templates select="sectitle"/>
				<xsl:apply-templates select="fn" mode="exist_fn_other_with_xref">
					<xsl:with-param name="id_list" select="$id_list"></xsl:with-param>
				</xsl:apply-templates>
			</fn-group>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="fn|fngrp[@id]" mode="elem_fn_other_with_xref">
		<xsl:param name="id_list"></xsl:param>
		<xsl:apply-templates select="." mode="exist_fn_other_with_xref">
			<xsl:with-param name="id_list" select="$id_list"></xsl:with-param>
		</xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="fngrp[fn]" mode="elem_fn_other_without_xref">
		<xsl:param name="id_list"></xsl:param>
		<xsl:variable name="teste"><xsl:apply-templates select="fn" mode="exist_fn_other_without_xref">
			<xsl:with-param name="id_list" select="$id_list"></xsl:with-param>
		</xsl:apply-templates></xsl:variable>
		<xsl:if test="normalize-space($teste)!=''">
			<fn-group>
				<xsl:apply-templates select="sectitle"/>
				<xsl:apply-templates select="fn" mode="exist_fn_other_without_xref">
					<xsl:with-param name="id_list" select="$id_list"></xsl:with-param>
				</xsl:apply-templates>
			</fn-group>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="fn|fngrp[@id]" mode="elem_fn_other_without_xref">
		<xsl:param name="id_list"></xsl:param>
		<xsl:apply-templates select="." mode="exist_fn_other_without_xref">
			<xsl:with-param name="id_list" select="$id_list"></xsl:with-param>
		</xsl:apply-templates>
	</xsl:template>
		
	<xsl:template match="doc|subdoc|docresp" mode="back">
		<xsl:variable name="local_fn_xref_rid_list"><xsl:apply-templates select="doctitle//xref[@ref-type='fn']|xmlbody//xref[@ref-type='fn']" mode="fn_xref_rid"></xsl:apply-templates></xsl:variable>
		<xsl:variable name="otherfntest">
			<xsl:apply-templates select="fn[@id]|fngrp[@id]|fngrp/fn[@id]" mode="exist_fn_other_with_xref">
			<xsl:with-param name="id_list"><xsl:value-of select="$local_fn_xref_rid_list"/></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="fn[@id]|fngrp[@id]|fngrp/fn[@id]" mode="exist_fn_other_without_xref">
				<xsl:with-param name="id_list"><xsl:value-of select="$local_fn_xref_rid_list"/></xsl:with-param>
			</xsl:apply-templates></xsl:variable>
		
		<xsl:if test="ack or normalize-space($otherfntest)!='' or refs or other or vancouv or iso690 or abnt6023 or apa or glossary or appgrp">
			<back>
				<xsl:apply-templates select="ack"/>
				<xsl:apply-templates select="other | vancouv | iso690 | abnt6023 | apa | refs"/>
				
				<xsl:apply-templates select="fn|fngrp" mode="elem_fn_other_with_xref">
					<xsl:with-param name="id_list" select="$local_fn_xref_rid_list"></xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="fn|fngrp" mode="elem_fn_other_without_xref">
					<xsl:with-param name="id_list" select="$local_fn_xref_rid_list"></xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="glossary | appgrp"/>				
			</back>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="back">
		<xsl:variable name="local_fn_xref_rid_list"><xsl:apply-templates select=".//xmlbody//xref[@ref-type='fn']" mode="fn_xref_rid"></xsl:apply-templates></xsl:variable>
		<xsl:variable name="otherfntest">
			<xsl:apply-templates select="fn[@id]|fngrp[@id]|fngrp/fn[@id]" mode="exist_fn_other_with_xref">
			<xsl:with-param name="id_list"><xsl:value-of select="$local_fn_xref_rid_list"/></xsl:with-param>
			</xsl:apply-templates>
			<xsl:apply-templates select="fn[@id]|fngrp[@id]|fngrp/fn[@id]" mode="exist_fn_other_without_xref">
				<xsl:with-param name="id_list"><xsl:value-of select="$local_fn_xref_rid_list"/></xsl:with-param>
			</xsl:apply-templates></xsl:variable>

		<xsl:apply-templates select="fxmlbody[@type='ack']|ack"/>
		<xsl:apply-templates select="*[@standard]"/>

		<xsl:apply-templates select="fn|fngrp" mode="elem_fn_other_with_xref">
			<xsl:with-param name="id_list" select="$local_fn_xref_rid_list"></xsl:with-param>
		</xsl:apply-templates>
		
		<xsl:apply-templates select="fn|fngrp" mode="elem_fn_other_without_xref">
			<xsl:with-param name="id_list" select="$local_fn_xref_rid_list"></xsl:with-param>
		</xsl:apply-templates>
		<xsl:apply-templates select="glossary | appgrp"></xsl:apply-templates>						
	</xsl:template>
	
	<xsl:template match="unidentified"> </xsl:template>

	<xsl:template match="fxmlbody[@type='ack']">
		<ack>
			<xsl:apply-templates mode="copy-of"  select="*"/>
		</ack>
	</xsl:template>

	<xsl:template match="*[contains(name(),'citat')]//bold | *[contains(name(),'citat')]//italic">
		<!--fixme styles-->
		<xsl:choose>
			<xsl:when test="normalize-space(translate(.,'(),.-:;','       '))=''"></xsl:when>
			<xsl:otherwise><xsl:apply-templates select="text()"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template
		match="*[contains(name(),'citat')]/text() | ref/text() | ref/bold | ref/italic | ref/sup | ref/sub"/>
	<xsl:template
		match="*[contains(name(),'citat')]//*[*]/text()"/>
	
	<xsl:template match="*[@standard] | refs">
		<ref-list>
			<xsl:choose>
				<xsl:when test="sectitle">
					<xsl:apply-templates select="sectitle"/>
				</xsl:when>
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
		<xsl:attribute name="rid">B<xsl:value-of select="string(number(substring(.,2)))"/></xsl:attribute>
	</xsl:template>

	<xsl:template match="*[@standard]/*[contains(name(),'citat')]">
		<xsl:variable name="id"><xsl:value-of select="position()"/></xsl:variable>
		<ref id="B{$id}">
			<xsl:apply-templates select="no"/>
			<!-- book, communication, letter, review, conf-proc, journal, list, patent, thesis, discussion, report, standard, and working-paper.  -->
			<xsl:variable name="type">
				<xsl:choose>
					<xsl:when test="viserial or aiserial or oiserial or iiserial or piserial"
						>journal</xsl:when>
					<xsl:when test=".//confgrp">confproc</xsl:when>
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
			<xsl:apply-templates select="." mode="mixed-citation"/>
			<element-citation publication-type="{$type}">
				<xsl:apply-templates select="*[name()!='no' and name()!='label' and name()!='text-ref']">
					<xsl:with-param name="position" select="position()"/>
				</xsl:apply-templates>
			</element-citation>
		</ref>
	</xsl:template>
	<xsl:template match="ref">
		<xsl:variable name="id"><xsl:choose>
			<xsl:when test="@id"><xsl:value-of select="substring(@id,2)"/></xsl:when><xsl:otherwise><xsl:value-of select="position()"/></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<ref id="B{$id}">
			<xsl:apply-templates select="label"/>
			<xsl:apply-templates select="." mode="mixed-citation"/>
			<element-citation>
				<xsl:apply-templates select="@reftype"/>
				<xsl:apply-templates select="@status|@refstatus"/>
				<xsl:apply-templates select="*[name()!='no' and name()!='label' and name()!='text-ref']">
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
			<xsl:value-of select="normalize-space(.)"/>
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
		<pub-id pub-id-type="other"><xsl:value-of select="normalize-space(.)"/></pub-id>
	</xsl:template>
	<xsl:template match="patentno">
		<patent country="{@country}"><xsl:value-of select="normalize-space(.)"/></patent>
	</xsl:template>
	<xsl:template match="letterto">
		<source><xsl:value-of select="normalize-space(.)"/></source>
	</xsl:template>
	<xsl:template match="found-at|moreinfo|othinfo">
		<comment><xsl:value-of select="normalize-space(.)"/></comment>
	</xsl:template>
	<xsl:template match="ref/contract">
		<comment content-type="award-id"><xsl:value-of select="normalize-space(.)"/></comment>
	</xsl:template>
	<xsl:template match="ref/date"></xsl:template>
	<xsl:template match="back//no">
		<label>
			<xsl:value-of select="normalize-space(.)"/>
		</label>
	</xsl:template>
	<xsl:template match="publoc">
		<publisher-loc>
			<xsl:value-of select="normalize-space(.)"/>
		</publisher-loc>
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
	<xsl:template match="pubname">
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
		<xsl:variable name="f"><xsl:value-of select="normalize-space(fname)"/></xsl:variable>
		<xsl:variable name="s"><xsl:value-of select="normalize-space(surname)"/></xsl:variable>
		<xsl:variable name="suffix"><xsl:choose>
			<xsl:when test="contains($s,',')"><xsl:value-of select="substring-after($s, ',')"/></xsl:when>
			<xsl:when test="contains($s,' ')"><xsl:value-of select="substring-after($s, ' ')"/></xsl:when>
			<xsl:otherwise></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<xsl:variable name="surname"><xsl:choose>
			<xsl:when test="contains($s,',')"><xsl:value-of select="substring-before($s, ',')"/></xsl:when>
			<xsl:when test="contains($s,' ')"><xsl:value-of select="substring-before($s, ' ')"/></xsl:when>
			<xsl:otherwise></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<xsl:variable name="ok">
			<xsl:if test="$suffix!=''">
				<xsl:choose>
					<xsl:when test="contains($suffix, 'nior') or contains($suffix, 'NIOR')">true</xsl:when>
					<xsl:when test="$suffix='Sr' or $suffix='Jr' or $suffix='Sr.' or $suffix='Jr.'">true</xsl:when>
					<xsl:when test="$suffix='Neto' or $suffix='NETO'">true</xsl:when>
					<xsl:when test="$suffix='Filho' or $suffix='FILHO'">true</xsl:when>
					<xsl:when test="$suffix='Sobrinho' or $suffix='SOBRINHO'">true</xsl:when>
				</xsl:choose>
			</xsl:if>
		</xsl:variable>
		<name>
		<xsl:choose>
			<xsl:when test="$ok='true'">
				<surname><xsl:value-of select="$surname"/></surname>
				<given-names><xsl:value-of select="$f"/></given-names>
				<xsl:if test="prefix"><prefix><xsl:value-of select="prefix"/></prefix></xsl:if>
				<suffix><xsl:value-of select="$suffix"/></suffix>
			</xsl:when>
			<xsl:otherwise>
				<surname><xsl:value-of select="$s"/></surname>
				<given-names><xsl:value-of select="$f"/></given-names>			
				<xsl:if test="prefix"><prefix><xsl:value-of select="prefix"/></prefix></xsl:if>
				<xsl:if test="suffix"><suffix><xsl:value-of select="suffix"/></suffix></xsl:if>
			</xsl:otherwise>
		</xsl:choose>
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

	<xsl:template match="back//date | ref//date">
		<xsl:call-template name="display_date">
			<xsl:with-param name="dateiso">
				<xsl:value-of select="@dateiso"/>
			</xsl:with-param>
			<xsl:with-param name="date">
				<xsl:value-of select="normalize-space(.)"/>
			</xsl:with-param>
			<xsl:with-param name="specyear"><xsl:value-of select="@specyear"/></xsl:with-param>
			<!--xsl:with-param name="format">textual</xsl:with-param-->
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
	<xsl:template match="*" mode="url-cited">
		<xsl:param name="text"/>
		<xsl:choose>
			<xsl:when test="contains($text,'.')">
				<xsl:apply-templates select="." mode="url-cited"><xsl:with-param name="text"><xsl:value-of select="substring-after($text,'.')"/></xsl:with-param></xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise><xsl:value-of select="$text"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
    <xsl:template match="url">
		<xsl:choose>
			<xsl:when test="../cited">
				<xsl:variable name="text">
					<xsl:apply-templates select="..//text()" mode="text-only"/>
				</xsl:variable>
				<xsl:variable name="term"><xsl:choose>
					<xsl:when test="contains($text,'Dispon')">Dispon</xsl:when>
					<xsl:when test="contains($text,'Available')">Available</xsl:when>
					<xsl:otherwise></xsl:otherwise>
				</xsl:choose></xsl:variable>
				<xsl:variable name="comment">
					<xsl:choose>
						<xsl:when test="$term=''"><xsl:apply-templates select="." mode="url-cited"><xsl:with-param name="text"><xsl:value-of select="substring-before($text,.)"/></xsl:with-param></xsl:apply-templates>
						</xsl:when>
						<xsl:otherwise><xsl:value-of select="substring-before(substring-after($text, substring-before($text, $term)),.)"/></xsl:otherwise>
					</xsl:choose>
				</xsl:variable>
				
				<comment>
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

	<xsl:template match="*[contains(name(),'citat')]| ref" mode="mixed-citation">
		<mixed-citation>
			<xsl:choose>
				<xsl:when test="text-ref and label and not(text-ref/*) and contains(text-ref, label)">
					<xsl:value-of select="substring-after(text-ref,label)"/>
				</xsl:when>
				<xsl:when test="text-ref">
					<xsl:apply-templates select="text-ref"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="." mode="create-mixed-citation"/>
				</xsl:otherwise>
			</xsl:choose>
		</mixed-citation>
	</xsl:template>

	<xsl:template match="*" mode="create-mixed-citation">
		<xsl:apply-templates select=" * | text() " mode="create-mixed-citation"/>
	</xsl:template>
	
	<xsl:template match="label" mode="create-mixed-citation">
	</xsl:template>
	
	<xsl:template match="italic" mode="create-mixed-citation">
		<xsl:variable name="text"><xsl:value-of select="normalize-space(text())"/></xsl:variable>
		<xsl:choose>
			<xsl:when test="* or string-length($text)&gt;1">
				<italic><xsl:apply-templates select="*|text()" mode="create-mixed-citation"></xsl:apply-templates></italic>
			</xsl:when>
			<xsl:when test="string-length($text)&lt;=1">
				<xsl:value-of select="text()"/>
			</xsl:when>
			<xsl:otherwise>
				<italic><xsl:apply-templates select="*|text()" mode="create-mixed-citation"></xsl:apply-templates></italic>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="sup | sub" mode="create-mixed-citation">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="*|text()" mode="create-mixed-citation"></xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="url" mode="create-mixed-citation">
		<xsl:apply-templates select="."/>
	</xsl:template>
	
	<xsl:template match="@*" mode="create-mixed-citation"/>

	<xsl:template match="text()" mode="create-mixed-citation">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>

	<xsl:template match="uri[contains(@href,'mailto:')]">
		<email>
			<xsl:apply-templates select=".//text()"/>
		</email>
	</xsl:template>


	<xsl:template match="figgrps[not(label)]">
		<!-- FIXMEID -->
		<fig-group id="{@id}">
			<xsl:apply-templates select="caption"/>
			<xsl:apply-templates select=".//figgrp"/>
		</fig-group>
	</xsl:template>

	<xsl:template match="figgrps[label]">
		<!-- FIXMEID -->
		<fig id="{@id}">
			<xsl:apply-templates select="label"/>
			<xsl:apply-templates select="caption"/>
			<xsl:apply-templates select=".//figgrp"/>
		</fig>
	</xsl:template>

	<xsl:template match="figgrp/@id | tabwrap/@id">
		<xsl:choose>
			<xsl:when test="substring(.,1,1)='f'">f<xsl:value-of select="substring(.,2)"/></xsl:when>
			<xsl:when test="substring(.,1,1)='t'">t<xsl:value-of select="substring(.,2)"/></xsl:when>
			<!--xsl:when test="substring(.,1,1)='f'">f<xsl:value-of select="string(number(substring(.,2)))"/></xsl:when>
			<xsl:when test="substring(.,1,1)='t'">t<xsl:value-of select="string(number(substring(.,2)))"/></xsl:when-->
			<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="figgrp" mode="elem-fig">
		<fig>
			<xsl:attribute name="id"><xsl:apply-templates select="@id"/></xsl:attribute>
			<xsl:if test="@ftype!='other'">
				<xsl:attribute name="fig-type">
					<xsl:value-of select="@ftype"/>
				</xsl:attribute>
			</xsl:if>
			<xsl:apply-templates select=".//label"/>
			<xsl:apply-templates select=".//caption"/>
			<xsl:apply-templates select=".//alttext"/>
			
			<xsl:apply-templates select="." mode="graphic"/>
			<xsl:apply-templates select="attrib | cpright | licinfo"/>
		</fig>
	</xsl:template>
	
	<xsl:template match="figgrp">
		<p>
			<xsl:apply-templates select="." mode="elem-fig"/>
		</p>
	</xsl:template>

	<xsl:template match="p/figgrp|figgrps/figgrp">
		<xsl:apply-templates select="." mode="elem-fig"/>
	</xsl:template>
	
	<xsl:template match="*[name()!='tabwrap']/table">
		<p>
			<xsl:apply-templates select="@*| * | text()" mode="tableless"/>
		</p>
	</xsl:template>
	
	<xsl:template match="tr | td | th | thead | tbody">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*| * | text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="th/bold">
		<xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="tabwrap" mode="elem-table-wrap">
		<table-wrap>
			<xsl:attribute name="id"><xsl:apply-templates select="@id"/></xsl:attribute>
			<xsl:apply-templates select="label"/>
			<xsl:apply-templates select=".//caption"/>
			<xsl:apply-templates select=".//alttext"/>
			<xsl:apply-templates select="." mode="graphic"/>
			<xsl:apply-templates select="." mode="notes"/>
			<xsl:apply-templates select="cpright | licinfo"/>
		</table-wrap>
	</xsl:template>
	
	<xsl:template match="tabwrap">
		<p><!-- FIXMEID -->
			<xsl:apply-templates select="." mode="elem-table-wrap"/>
		</p>
	</xsl:template>

	<xsl:template match="p/tabwrap">		
		<xsl:apply-templates select="." mode="elem-table-wrap"/>
	</xsl:template>
	
	<xsl:template match="tabwrap//fntable" mode="table">
		<xsl:param name="table_id"/>
		<!-- FIXMEID -->
		<xsl:variable name="id">
		<xsl:choose>
			<xsl:when test="contains(@id,'TFN')"><xsl:value-of select="@id"/></xsl:when>
			<xsl:otherwise>TFN<xsl:value-of select="string(number(substring(@id,4)))"/></xsl:otherwise>
		</xsl:choose></xsl:variable>
		
		<fn id="{$id}">
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
		<source><xsl:apply-templates select="*|text()"/></source>
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
	<!--xsl:template match="xref[@rid!='']">
		<xsl:variable name="display"><xsl:choose>
			<xsl:when test="@ref-type='bibr'">
				<xsl:apply-templates select="*[name()!='graphic']|text()"/>
			</xsl:when>
			<xsl:otherwise><xsl:value-of select="normalize-space(.//text())"/></xsl:otherwise>					
		</xsl:choose></xsl:variable>
		<xref>
			<xsl:apply-templates select="@*[name()!='label']"/>
			<xsl:choose>
				<xsl:when test="@ref-type='bibr'">
					<xsl:apply-templates select="*[name()!='graphic']|text()"/>
				</xsl:when>
				<xsl:when test="normalize-space(.//text())=''">
					<sup>
						<xsl:choose>
							<xsl:when test="@label">
								<xsl:value-of select="@label"/>
							</xsl:when>
							<xsl:when test="contains(@rid, @ref-type)">
								<xsl:value-of select="substring(@rid,string-length(@ref-type)+1)"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="@rid"/>
							</xsl:otherwise>
						</xsl:choose>
					</sup>
				</xsl:when>
				<xsl:when test=".//sup">
					<xsl:apply-templates select="*[name()!='graphic']|text()" mode="text-only"/>
					<xsl:variable name="x"><xsl:apply-templates select="*[name()!='graphic']|text()" mode="text-only"/></xsl:variable>
					<xsl:if test="normalize-space($x)=''"><xsl:value-of select="@label"/></xsl:if>
				</xsl:when>
				<xsl:otherwise>
					<sup>
						<xsl:apply-templates select="*[name()!='graphic']|text()"/>
						<xsl:variable name="x"><xsl:apply-templates select="*[name()!='graphic']|text()"/></xsl:variable>
						<xsl:if test="normalize-space($x)=''"><xsl:value-of select="@label"/></xsl:if>
					</sup>
				</xsl:otherwise>					
			</xsl:choose>
		</xref>
		<xsl:if test="graphic">
			<graphic>
				<xsl:apply-templates select="graphic/@*|graphic/*|graphic/text()"/>
				<uri>#<xsl:value-of select="@rid"/>
				</uri>
			</graphic>
		</xsl:if>
	</xsl:template-->
	<xsl:template match="xref[@rid!='']">
		<xsl:variable name="text"><xsl:apply-templates select="*[name()!='graphic']|text()" mode="text-only"/></xsl:variable>
		<xsl:variable name="alt_display"><xsl:choose>
						<xsl:when test="@label"><xsl:value-of select="@label"/></xsl:when>
			<xsl:when test="contains(@rid, @ref-type)"><xsl:value-of select="substring-after(@rid, @ref-type)"/></xsl:when>
						<xsl:otherwise><xsl:apply-templates select="@rid"/></xsl:otherwise>
					</xsl:choose>
				</xsl:variable>
		<xref>
			<xsl:apply-templates select="@*[name()!='label']"/>
			<xsl:choose>
				<xsl:when test="@ref-type='bibr'">
					<xsl:apply-templates select="*[name()!='graphic']|text()"/>
				</xsl:when>
				<xsl:when test="normalize-space($text)=''">
					<sup>
						<xsl:value-of select="$alt_display"/>
					</sup>
				</xsl:when>
				<xsl:when test=".//sup or contains(normalize-space($text),' ')">
					<xsl:apply-templates select="*[name()!='graphic']|text()"/>
				</xsl:when>
				<xsl:otherwise>
						<xsl:apply-templates select="*[name()!='graphic']|text()" mode="text-only"/>
				</xsl:otherwise>					
			</xsl:choose>
		</xref>
		<xsl:if test="graphic">
			<graphic>
				<xsl:apply-templates select="graphic/@*|graphic/*|graphic/text()"/>
				<uri>#<xsl:value-of select="@rid"/>
				</uri>
			</graphic>
		</xsl:if>
	</xsl:template>
	
	<!--xsl:template match="xref[@rid!='']">
		<xsl:variable name="rid" select="@rid"/>

		<xsl:choose>
			<xsl:when test="@ref-type='bibr'">
				<xref>
					<xsl:apply-templates select="@*"/>
					<xsl:apply-templates select="*|text()"/>
				</xref>
			</xsl:when>
			<xsl:when test="@ref-type='aff'">
				<xsl:variable name="label" select="normalize-space(.)"/>
				<xref ref-type="aff">
					<xsl:attribute name="rid"><xsl:apply-templates select="@rid"/></xsl:attribute>
					<sup>
						<xsl:value-of select="$label"/>
					</sup>
				</xref>
			</xsl:when>
			<xsl:when test="$elem_id[@id=$rid]">
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
				<xsl:apply-templates mode="copy-of"  select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template-->

	<xsl:template match="*[@id]" mode="display-id">
		<xsl:value-of select="@id"/>,</xsl:template>
	<!--xsl:template match="xref[@rid!='']">
		<xsl:variable name="rid" select="@rid"/>
		<xsl:if test="$elem_id[@id=$rid]">
			<xref>
				<xsl:apply-templates select="@*|*[name()!='graphic']|text()"/>
			</xref>
		</xsl:if>
	</xsl:template>
	<xsl:template match="xref[graphic and @rid!='']">
		<xsl:variable name="rid" select="@rid"/>
		<xsl:if test="$elem_id[@id=$rid]">
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
		<xsl:apply-templates mode="copy-of"  select="."/>
	</xsl:template>
	<xsl:template match="fname">
		<given-names>
			<xsl:apply-templates select="*|text()" mode="text-only"/>
		</given-names>
	</xsl:template>
	<xsl:template match="surname">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="*|text()" mode="text-only"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="isstitle">
		<issue-title>
			<xsl:value-of select="normalize-space(.)"/>
		</issue-title>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//p | *[contains(name(),'citat')]/text()"> </xsl:template>
	<xsl:template match="*" mode="debug"> </xsl:template>
	<xsl:template match="equation" mode="graphic">
		<xsl:variable name="standardname" select="concat($prefix, 'e', @id)"/>
		<xsl:choose>
			<xsl:when test="count(graphic) + count(texmath) + count(mmlmath) = 1">
				<xsl:apply-templates select="label|graphic|text()|texmath|mmlmath"></xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<alternatives>
					<xsl:apply-templates select="graphic|texmath|mmlmath"></xsl:apply-templates>
				</alternatives>
				<xsl:apply-templates select="label|text()"></xsl:apply-templates>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="figgrp | tabwrap" mode="graphic">
		<xsl:variable name="standardname" select="concat($prefix, 'g', @id)"/>
		<xsl:choose>
			<xsl:when test="graphic and (xhtmltable or table)">
				<alternatives>
					<xsl:apply-templates select="graphic" mode="elem-graphic"/>
					<xsl:apply-templates mode="copy-of"  select="xhtmltable/table"/>
					<xsl:apply-templates select="table" mode="pmc-table"/>
				</alternatives>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="graphic" mode="elem-graphic"/>
				<xsl:apply-templates select="table" mode="pmc-table"/>
				<xsl:apply-templates mode="copy-of"  select="xhtmltable/table"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="graphic" mode="elem-graphic">
		<graphic>
			<xsl:attribute name="xlink:href"><xsl:choose>
				<xsl:when test="substring(@href,1,1)='?'"><xsl:value-of select="concat(substring(@href,2),@id)"/></xsl:when>
				<xsl:when test="../@filename"><xsl:value-of select="../@filename"/></xsl:when>
				<xsl:otherwise><xsl:value-of select="@href"/></xsl:otherwise>
			</xsl:choose></xsl:attribute>
			<!-- cpright, licinfo, alttext -->
			<xsl:apply-templates select="*"/>
		</graphic>
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
			<xsl:choose>
				<xsl:when test="tbody//td//*">
					<xsl:apply-templates select="tbody"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates mode="copy-of"  select="tbody"/>
				</xsl:otherwise>
			</xsl:choose>
		</table>
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
	<xsl:template match="table//equation">
		<disp-formula>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="." mode="graphic"/>
		</disp-formula>
	</xsl:template>
	<xsl:template match="p//equation|caption//equation|attrib//equation">
		<inline-formula>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="." mode="graphic"/>
		</inline-formula>
	</xsl:template>
	<xsl:template match="p//graphic | caption//graphic | li//graphic | p//equation//graphic | td//graphic">
		<inline-graphic>
			<xsl:apply-templates select="@*"/>
		</inline-graphic>
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
				<xsl:apply-templates select="@*|*|text()" mode="mathml"></xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="." disable-output-escaping="yes"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="mmlmath//*" mode="mathml">
		<xsl:choose>
			<xsl:when test="contains(name(),'mml:')">
				<xsl:apply-templates mode="copy-of"  select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="mml:{name()}">
					<xsl:apply-templates select="@*|*|text()" mode="mathml"/>
				</xsl:element>
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
		<xsl:apply-templates select="*"/>	
	</xsl:template>
	<xsl:template match="ref/thesis | ref/thesgrp">
		<xsl:choose>
			<xsl:when test="parent::node()[date]">
				<xsl:apply-templates select="*[name()!='date']"></xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="*"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="degree"><comment content-type="degree"><xsl:value-of select="normalize-space(.)"/></comment></xsl:template>
	<xsl:template match="thesis/orgdiv | thesgrp/orgdiv"/>
	<xsl:template match="thesis/orgname | thesgrp/orgname">
		<publisher-name><xsl:apply-templates select="parent::node()" mode="org"/></publisher-name>
	</xsl:template>
	<xsl:template match="*[orgname or orgdiv]" mode="org">
		<xsl:apply-templates select="orgname|orgdiv" mode="org"/>
	</xsl:template>
	<xsl:template match="orgname|orgdiv" mode="org">
		<xsl:if test="position()!=1">, </xsl:if><xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	
	<xsl:template match="thesis/city | thesgrp/city | thesis/state | thesgrp/state | thesis/country | thesgrp/country">
		<xsl:apply-templates select="parent::node()" mode="location"></xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="thesis|thesgrp" mode="location">
		<publisher-loc><xsl:apply-templates select="city|state|country" mode="location"/></publisher-loc>
	</xsl:template>
	<xsl:template match="city|state|country" mode="location">
		<xsl:if test="position()!=1">, </xsl:if><xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	<!--xsl:template match=" *[contains(name(),'contrib')]//bold |  *[contains(name(),'monog')]//bold"/-->
	<xsl:template match="subsec/xref | sec/xref"> </xsl:template>
	<xsl:template match="*[*]" mode="next">
		<xsl:if test="position()=1">
			<xsl:value-of select="name()"/>
		</xsl:if>
	</xsl:template>

	<!--xsl:template match="figgrps/figgrp/caption">
		<caption>
			<p>
				<xsl:apply-templates select="@*| * | text()"/>
			</p>
		</caption>
	</xsl:template-->
	<xsl:template match="*" mode="norm-abbrev-month">
		<xsl:param name="date"/>
		<xsl:param name="month_number"/>
		<xsl:choose>
			<xsl:when test="$month_number='01'">
				<xsl:choose>
					<xsl:when test="contains($date,'Jan')">Jan</xsl:when>
					<xsl:when test="contains($date,'jan')">jan</xsl:when>
					<xsl:when test="contains($date,'ene')">ene</xsl:when>
					<xsl:when test="contains($date,'Ene')">Ene</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='02'">
				<xsl:choose>
					<xsl:when test="contains($date,'Feb')">Feb</xsl:when>
					<xsl:when test="contains($date,'Fev')">Fev</xsl:when>
					<xsl:when test="contains($date,'fev')">fev</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='03'">
				<xsl:choose>
					<xsl:when test="contains($date,'Mar')">Mar</xsl:when>
					<xsl:when test="contains($date,'mar')">mar</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='04'">
				<xsl:choose>
					<xsl:when test="contains($date,'Apr')">Apr</xsl:when>
					<xsl:when test="contains($date,'apr')">apr</xsl:when>
					<xsl:when test="contains($date,'abr')">abr</xsl:when>
					<xsl:when test="contains($date,'Abr')">Abr</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='05'">
				<xsl:choose>
					<xsl:when test="contains($date,'May')">May</xsl:when>
					<xsl:when test="contains($date,'may')">may</xsl:when>
					<xsl:when test="contains($date,'mai')">mai</xsl:when>
					<xsl:when test="contains($date,'Mai')">Mai</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='06'">
				<xsl:choose>
					<xsl:when test="contains($date,'Jun')">Jun</xsl:when>
					<xsl:when test="contains($date,'jun')">jun</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='07'">
				<xsl:choose>
					<xsl:when test="contains($date,'Jul')">Jul</xsl:when>
					<xsl:when test="contains($date,'jul')">jul</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='08'">
				<xsl:choose>
					<xsl:when test="contains($date,'Aug')">Aug</xsl:when>
					<xsl:when test="contains($date,'ago')">ago</xsl:when>
					<xsl:when test="contains($date,'Ago')">Ago</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='09'">
				<xsl:choose>
					<xsl:when test="contains($date,'Sep')">Sep</xsl:when>
					<xsl:when test="contains($date,'sep')">sep</xsl:when>
					<xsl:when test="contains($date,'Set')">Set</xsl:when>
					<xsl:when test="contains($date,'set')">set</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='10'">
				<xsl:choose>
					<xsl:when test="contains($date,'Oct')">Oct</xsl:when>
					<xsl:when test="contains($date,'oct')">oct</xsl:when>
					<xsl:when test="contains($date,'out')">out</xsl:when>
					<xsl:when test="contains($date,'Out')">Out</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='11'">
				<xsl:choose>
					<xsl:when test="contains($date,'Nov')">Nov</xsl:when>
					<xsl:when test="contains($date,'nov')">nov</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="$month_number='12'">
				<xsl:choose>
					<xsl:when test="contains($date,'Dec')">Dec</xsl:when>
					<xsl:when test="contains($date,'dez')">dez</xsl:when>
					<xsl:when test="contains($date,'Dez')">Dez</xsl:when>
					<xsl:when test="contains($date,'dic')">dic</xsl:when>
					<xsl:when test="contains($date,'Dic')">Dic</xsl:when>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="contains($date,'Dec')">Dec</xsl:when>
					<xsl:when test="contains($date,'dez')">dez</xsl:when>
					<xsl:when test="contains($date,'Dez')">Dez</xsl:when>
					<xsl:when test="contains($date,'dic')">dic</xsl:when>
					<xsl:when test="contains($date,'Dic')">Dic</xsl:when>
					<xsl:when test="contains($date,'Nov')">Nov</xsl:when>
					<xsl:when test="contains($date,'nov')">nov</xsl:when>
					<xsl:when test="contains($date,'Oct')">Oct</xsl:when>
					<xsl:when test="contains($date,'oct')">oct</xsl:when>
					<xsl:when test="contains($date,'out')">out</xsl:when>
					<xsl:when test="contains($date,'Out')">Out</xsl:when>
					<xsl:when test="contains($date,'Sep')">Sep</xsl:when>
					<xsl:when test="contains($date,'sep')">sep</xsl:when>
					<xsl:when test="contains($date,'Set')">Set</xsl:when>
					<xsl:when test="contains($date,'set')">set</xsl:when>
					<xsl:when test="contains($date,'Aug')">Aug</xsl:when>
					<xsl:when test="contains($date,'ago')">ago</xsl:when>
					<xsl:when test="contains($date,'Ago')">Ago</xsl:when>
					<xsl:when test="contains($date,'Jul')">Jul</xsl:when>
					<xsl:when test="contains($date,'jul')">jul</xsl:when>
					<xsl:when test="contains($date,'Jun')">Jun</xsl:when>
					<xsl:when test="contains($date,'jun')">jun</xsl:when>
					<xsl:when test="contains($date,'May')">May</xsl:when>
					<xsl:when test="contains($date,'may')">may</xsl:when>
					<xsl:when test="contains($date,'mai')">mai</xsl:when>
					<xsl:when test="contains($date,'Mai')">Mai</xsl:when>
					<xsl:when test="contains($date,'Apr')">Apr</xsl:when>
					<xsl:when test="contains($date,'apr')">apr</xsl:when>
					<xsl:when test="contains($date,'abr')">abr</xsl:when>
					<xsl:when test="contains($date,'Abr')">Abr</xsl:when>
					<xsl:when test="contains($date,'Mar')">Mar</xsl:when>
					<xsl:when test="contains($date,'mar')">mar</xsl:when>
					<xsl:when test="contains($date,'Feb')">Feb</xsl:when>
					<xsl:when test="contains($date,'Fev')">Fev</xsl:when>
					<xsl:when test="contains($date,'fev')">fev</xsl:when>
					<xsl:when test="contains($date,'Jan')">Jan</xsl:when>
					<xsl:when test="contains($date,'jan')">jan</xsl:when>
					<xsl:when test="contains($date,'ene')">ene</xsl:when>
					<xsl:when test="contains($date,'Ene')">Ene</xsl:when>
				</xsl:choose>
			</xsl:otherwise>
	</xsl:choose></xsl:template>
	<xsl:template match="*" mode="month-number">
		<xsl:param name="date"></xsl:param>
		<xsl:choose>
			<xsl:when test="contains($date,'Dec')">12</xsl:when>
			<xsl:when test="contains($date,'dez')">12</xsl:when>
			<xsl:when test="contains($date,'Dez')">12</xsl:when>
			<xsl:when test="contains($date,'dic')">12</xsl:when>
			<xsl:when test="contains($date,'Dic')">12</xsl:when>
			<xsl:when test="contains($date,'Nov')">11</xsl:when>
			<xsl:when test="contains($date,'nov')">11</xsl:when>
			<xsl:when test="contains($date,'Oct')">10</xsl:when>
			<xsl:when test="contains($date,'oct')">10</xsl:when>
			<xsl:when test="contains($date,'out')">10</xsl:when>
			<xsl:when test="contains($date,'Out')">10</xsl:when>
			<xsl:when test="contains($date,'Sep')">09</xsl:when>
			<xsl:when test="contains($date,'sep')">09</xsl:when>
			<xsl:when test="contains($date,'Set')">09</xsl:when>
			<xsl:when test="contains($date,'set')">09</xsl:when>
			<xsl:when test="contains($date,'Aug')">08</xsl:when>
			<xsl:when test="contains($date,'ago')">08</xsl:when>
			<xsl:when test="contains($date,'Ago')">08</xsl:when>
			<xsl:when test="contains($date,'Jul')">07</xsl:when>
			<xsl:when test="contains($date,'jul')">07</xsl:when>
			<xsl:when test="contains($date,'Jun')">06</xsl:when>
			<xsl:when test="contains($date,'jun')">06</xsl:when>
			<xsl:when test="contains($date,'May')">05</xsl:when>
			<xsl:when test="contains($date,'may')">05</xsl:when>
			<xsl:when test="contains($date,'mai')">05</xsl:when>
			<xsl:when test="contains($date,'Mai')">05</xsl:when>
			<xsl:when test="contains($date,'Apr')">04</xsl:when>
			<xsl:when test="contains($date,'apr')">04</xsl:when>
			<xsl:when test="contains($date,'abr')">04</xsl:when>
			<xsl:when test="contains($date,'Abr')">04</xsl:when>
			<xsl:when test="contains($date,'Mar')">03</xsl:when>
			<xsl:when test="contains($date,'mar')">03</xsl:when>
			<xsl:when test="contains($date,'Feb')">02</xsl:when>
			<xsl:when test="contains($date,'Fev')">02</xsl:when>
			<xsl:when test="contains($date,'fev')">02</xsl:when>
			<xsl:when test="contains($date,'Jan')">01</xsl:when>
			<xsl:when test="contains($date,'jan')">01</xsl:when>
			<xsl:when test="contains($date,'ene')">01</xsl:when>
			<xsl:when test="contains($date,'Ene')">01</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="display_date">
		<xsl:param name="dateiso"/>
		<xsl:param name="date" select="''"/>
		<xsl:param name="month_format">number</xsl:param>
		<xsl:param name="specyear"></xsl:param>
		
		<xsl:variable name="iso_day"><xsl:if test="string-length($dateiso)=8"><xsl:value-of select="substring($dateiso,7,2)"/></xsl:if></xsl:variable>
		<xsl:variable name="iso_month"><xsl:if test="string-length($dateiso)=8"><xsl:value-of select="substring($dateiso,5,2)"/></xsl:if></xsl:variable>
		<xsl:variable name="iso_year"><xsl:if test="string-length($dateiso)=8"><xsl:value-of select="substring($dateiso,1,4)"/></xsl:if></xsl:variable>
		<xsl:variable name="norm_date"><xsl:value-of select="translate(translate(translate($date,' ',''),'.',''),'/','-')"/></xsl:variable>
		<xsl:variable name="season"><xsl:choose>
			<xsl:when test="contains($norm_date,$iso_year)"><xsl:value-of select="substring-before($norm_date,$iso_year)"/><xsl:value-of select="substring-after($norm_date,$iso_year)"/></xsl:when>
			<xsl:otherwise><xsl:value-of select="$norm_date"/></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<xsl:variable name="norm_season"><xsl:choose>
			<xsl:when test="string-length($season)&lt;3"></xsl:when>
			<xsl:when test="contains($season,'Summer') or contains($season,'Winter') or contains($season,'Autumn') or contains($season,'Spring') or contains($season,'Fall')"><xsl:value-of select="$season"/></xsl:when>
			<xsl:when test="contains($season,'-')"><xsl:value-of select="substring(substring-before($season,'-'),1,3)"/>-<xsl:value-of select="substring(substring-after($season,'-'),1,3)"/></xsl:when>
			<xsl:otherwise><xsl:value-of select="substring($season,1,3)"/></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<xsl:if test="$iso_day!='00' and string-length($iso_day)=2">
			<day>
				<xsl:value-of select="$iso_day"/>
			</day>
		</xsl:if>
		<xsl:variable name="month">
			<xsl:choose>
				<xsl:when test="$month_format='number'">
					<xsl:choose>
						<xsl:when test="$iso_month!='00' and string-length($iso_month)=2">
							<xsl:value-of select="$iso_month"/>
						</xsl:when>
						<xsl:when test="$norm_season!=''">
							<xsl:apply-templates select="." mode="month-number"><xsl:with-param name="date"><xsl:value-of select="$norm_season"/></xsl:with-param></xsl:apply-templates>
						</xsl:when>
					</xsl:choose>
				</xsl:when>
				<xsl:when test="$month_format!='number'">
					<xsl:apply-templates select="." mode="norm-abbrev-month">
						<xsl:with-param name="date" select="$norm_season"/>
						<xsl:with-param name="month_number" select="$iso_month"/>
					</xsl:apply-templates>
				</xsl:when>
			</xsl:choose></xsl:variable>
		<xsl:choose>
			<xsl:when test="string-length($norm_season)&gt;3">
				<season><xsl:value-of select="$norm_season"/></season>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="$month!=''"><month><xsl:value-of select="$month"/></month></xsl:if>
			</xsl:otherwise>
		</xsl:choose>

		<xsl:variable name="year">
			<xsl:choose>
				<xsl:when test="$specyear!=''"><xsl:value-of select="$specyear"/></xsl:when>
				<xsl:otherwise><xsl:value-of select="$iso_year"/></xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="$year!=''"><year><xsl:value-of select="$year"/></year></xsl:if>
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
			<xsl:choose>
				<xsl:when test="p">
					<xsl:apply-templates select="*"/>
				</xsl:when>
				<xsl:otherwise>
					<p>
						<xsl:apply-templates select="*|text()"/>
					</p>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="cpright | licinfo"/>
		</disp-quote>
	</xsl:template>

	<xsl:template match="confgrp">
		<conference>
			<xsl:apply-templates select="*|text()"/>
		</conference>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//confgrp | ref/confgrp">
		<xsl:apply-templates select="*"/>
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
		<xsl:apply-templates select="parent::node()" mode="fulltitle"/>
	</xsl:template>

	<xsl:template match="confgrp" mode="fulltitle">
		<conf-name><xsl:apply-templates select="no|confname" mode="fulltitle"/></conf-name>
	</xsl:template>

	<xsl:template match="confgrp/confname | confgrp/no" mode="fulltitle">
		<xsl:if test="position()=2 and name()='no'">, </xsl:if><xsl:value-of select="normalize-space(.)"/>
	</xsl:template>

	<xsl:template match="colvolid"><volume><xsl:value-of select="normalize-space(.)"/></volume></xsl:template>
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
		<xsl:choose>
			<xsl:when test="string-length(normalize-space($preprint_date))&gt;0">
				<pub-date pub-type="epub">
					<xsl:call-template name="display_date">
						<xsl:with-param name="dateiso">
							<xsl:value-of select="$preprint_date"/>
						</xsl:with-param>
					</xsl:call-template>
				</pub-date>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="issue_date_type">
					<xsl:choose>
						<xsl:when test="@issueno='ahead'"></xsl:when>
						<xsl:when test="(number(@issueno)=0 or not(@issueno)) and (number(@volid)=0 or not(@volid))"></xsl:when>
						<!--xsl:when test="@artdate">collection</xsl:when--><!-- rolling pass -->
						<!--xsl:when test="@ahpdate">collection</xsl:when-->
						<xsl:otherwise><xsl:value-of select="$pub_type"/></xsl:otherwise>
					</xsl:choose>
				</xsl:variable>
				<xsl:if test="$issue_date_type!=''">
					<pub-date pub-type="{$issue_date_type}">
						<xsl:call-template name="display_date">
							<xsl:with-param name="dateiso">
								<xsl:value-of select="@dateiso"/>
							</xsl:with-param>
							<xsl:with-param name="date">
								<xsl:choose>
									<xsl:when test="@season!=''">
										<xsl:value-of select="@season"/>
									</xsl:when>
									<xsl:when test="//extra-scielo//season">
										<xsl:value-of select="//extra-scielo//season"/>
									</xsl:when>
								</xsl:choose>
							</xsl:with-param>
						</xsl:call-template>
					</pub-date>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
		
	</xsl:template>
	<xsl:template match="element">
		<xsl:element name="{@name}">
			<xsl:apply-templates select="*|text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="elemattr">
		<xsl:attribute name="{@name}">
			<xsl:apply-templates select="@value"/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="supplmat">
		<xsl:variable name="id"><xsl:choose>
			<xsl:when test="contains(@id,'smat')">suppl<xsl:value-of select="string(number(substring-after(@id,'smat')))"/></xsl:when>
			<xsl:otherwise>suppl<xsl:value-of select="string(number(substring(@id,6)))"/></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<supplementary-material id="{$id}" xlink:href="{@href}" mimetype="replace{@href}" mime-subtype="replace">			
			<xsl:apply-templates select="*|text()"/>
		</supplementary-material>
	</xsl:template>
	<xsl:template match="p/supplmat | caption//supplmat">
		<inline-supplementary-material xlink:href="{@href}" mimetype="replace{@href}" mime-subtype="replace">	
			<xsl:apply-templates select="*|text()"/>
		</inline-supplementary-material>
	</xsl:template>
	<xsl:template match="media">
		<xsl:variable name="id">m<xsl:value-of select="string(number(substring(@id,2)))"/></xsl:variable>
		
		<media  id="{$id}" xlink:href="{@href}" mimetype="replace{@href}" mime-subtype="replace">	
			<xsl:apply-templates select="*|text()"/>
		</media>
	</xsl:template>
	<xsl:template match="pubid"><xsl:element name="pub-id"><xsl:attribute name="pub-id-type"><xsl:value-of select="@idtype"/></xsl:attribute><xsl:value-of select="normalize-space(.)"/></xsl:element></xsl:template>

	<xsl:template match="related"><xsl:apply-templates select="*|text()"></xsl:apply-templates></xsl:template>
	
	<xsl:template match="related[@reltype]" mode="front-related">
		<related/>
	</xsl:template>
	<xsl:template match="related[@reltp]" mode="front-related">
		<!-- link de ? para ?? -->
		<!-- ﻿[related reltype="???" relid="????" relidtp="?????"] -->
		<!-- <related-article related-article-type="{@reltype}" id="{$this_doi}" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{@relid}" ext-link-type="{@relidtp}"/>-->
		<xsl:variable name="id"><xsl:value-of select="@id-or-doi"/><xsl:value-of select="@id-doi"/><xsl:value-of select="@pid-doi"/></xsl:variable>
		<related-article related-article-type="{@reltp}" id="A01" xmlns:xlink="http://www.w3.org/1999/xlink">
			<xsl:attribute name="xlink:href"><xsl:value-of select="$id"/></xsl:attribute>
			<xsl:attribute name="ext-link-type"><xsl:choose>
				<xsl:when test="string-length($id)=23 and substring($id,1,1)='S'">scielo-pid</xsl:when>
				<xsl:when test="contains($id,'doi')">doi</xsl:when>
				<xsl:when test="substring($id,1,4)='http'">uri</xsl:when>
				<xsl:otherwise>doi</xsl:otherwise>
			</xsl:choose></xsl:attribute>
			<xsl:apply-templates select="*|text()"></xsl:apply-templates>
		</related-article>
	</xsl:template>
	<xsl:template match="related[@reltp='corrected-article']" mode="front-related">
		<!-- errata -->
		<xsl:variable name="id"><xsl:value-of select="@id-or-doi"/><xsl:value-of select="@id-doi"/><xsl:value-of select="@pid-doi"/></xsl:variable>
		<related-article related-article-type="{@reltp}" id="ra1" xmlns:xlink="http://www.w3.org/1999/xlink">
			<xsl:attribute name="xlink:href"><xsl:value-of select="$id"/></xsl:attribute>
			<xsl:attribute name="ext-link-type"><xsl:choose>
				<xsl:when test="string-length($id)=23 and substring($id,1,1)='S'">scielo-pid</xsl:when>
				<xsl:when test="contains($id,'doi')">doi</xsl:when>
				<xsl:when test="substring($id,1,4)='http'">uri</xsl:when>
				<xsl:otherwise>doi</xsl:otherwise>
			</xsl:choose></xsl:attribute>
			<xsl:apply-templates select="*|text()"></xsl:apply-templates>
		</related-article>
	</xsl:template>
	<xsl:template match="related[@reltp='article']" mode="front-related">
		<!-- link de ? para ?? -->
		<!-- ﻿[related reltype="???" relid="????" relidtp="?????"] -->
		<!-- <related-article related-article-type="{@reltype}" id="{$this_doi}" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{@relid}" ext-link-type="{@relidtp}"/>-->
		<xsl:variable name="id"><xsl:value-of select="@id-or-doi"/><xsl:value-of select="@id-doi"/><xsl:value-of select="@pid-doi"/></xsl:variable>
		<related-article related-article-type="article-reference" id="A01" xmlns:xlink="http://www.w3.org/1999/xlink">
			<xsl:attribute name="xlink:href"><xsl:value-of select="$id"/></xsl:attribute>
			<xsl:attribute name="ext-link-type"><xsl:choose>
				<xsl:when test="string-length($id)=23 and substring($id,1,1)='S'">scielo-pid</xsl:when>
				<xsl:when test="contains($id,'doi')">doi</xsl:when>
				<xsl:when test="substring($id,1,4)='http'">uri</xsl:when>
				<xsl:otherwise>doi</xsl:otherwise>
			</xsl:choose>
			</xsl:attribute>
			<xsl:attribute name="specific-use">processing-only</xsl:attribute>
			<xsl:apply-templates select="*|text()"></xsl:apply-templates>
		</related-article>
	</xsl:template>
	<xsl:template match="related[@reltp='press-release']" mode="front-related">
		<!-- link de article para press release -->
		<!-- ﻿[related reltype="pr" relid="pr01" relidtp="press-release-id"] -->
		<!-- <related-article related-article-type="press-release" id="01" specific-use="processing-only"/>-->
		<xsl:variable name="id"><xsl:value-of select="@id-or-doi"/><xsl:value-of select="@id-doi"/><xsl:value-of select="@pid-doi"/></xsl:variable>
		<related-article related-article-type="commentary">
			<xsl:attribute name="xlink:href"><xsl:value-of select="$id"/></xsl:attribute>
			<xsl:attribute name="ext-link-type"><xsl:choose>
				<xsl:when test="string-length($id)=23 and substring($id,1,1)='S'">scielo-pid</xsl:when>
				<xsl:when test="contains($id,'doi')">doi</xsl:when>
				<xsl:when test="substring($id,1,4)='http'">uri</xsl:when>
				<xsl:otherwise>doi</xsl:otherwise>
			</xsl:choose></xsl:attribute>
			<xsl:attribute name="specific-use">processing-only</xsl:attribute>
		</related-article>
	</xsl:template>
	
	<xsl:template match="author">
		<contrib><xsl:apply-templates select="*"></xsl:apply-templates></contrib>
	</xsl:template>
	<xsl:template match="corpauth">
		<collab><xsl:apply-templates select="orgname|orgiv|text()"></xsl:apply-templates></collab>
	</xsl:template>
	<xsl:template match="product" mode="product-in-article-meta">
		<product product-type="{@prodtype}">
			<xsl:apply-templates select="*|text()" mode="product-in-article-meta"></xsl:apply-templates>
		</product>
	</xsl:template>
	
	<xsl:template match="product/*"  mode="product-in-article-meta">
		<xsl:apply-templates select="."/>
	</xsl:template>
	
	<xsl:template match="product/city | product/state | product/country"  mode="product-in-article-meta">
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
	<xsl:template match="product/date"  mode="product-in-article-meta">
		<year><xsl:value-of select="substring(@dateiso,1,4)"/></year>
	</xsl:template>
	<xsl:template match="product/title"  mode="product-in-article-meta">
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
	<xsl:template match="nographic">
		<!--xsl:comment>markup: graphic is identifying a text, not a graphical element</xsl:comment-->
		<graphic>
			<xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
		</graphic>
	</xsl:template>
	<xsl:template match="p//product">
		<xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="p//product//text()">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	
	<xsl:template match="p//product//*"><xsl:apply-templates select="*|text()"></xsl:apply-templates></xsl:template>
	
	<xsl:template match="*" mode="license-element">
		<xsl:param name="lang" select="$lang"/>
		<xsl:param name="href"/>
		
		<xsl:variable name="language"><xsl:choose>
			<xsl:when test="@language"><xsl:value-of select="@language"/></xsl:when>
			<xsl:when test="$lang"><xsl:value-of select="$lang"/></xsl:when>
		</xsl:choose></xsl:variable>
		<license xml:lang="{$language}" license-type="open-access" xlink:href="{$href}">
			<license-p>
				<xsl:apply-templates select="." mode="license-text">
					<xsl:with-param name="lang" select="$language"/>
				</xsl:apply-templates>
			</license-p>
		</license>
	</xsl:template>
	
	<xsl:template match="cc">
		<xsl:variable name="ccid"><xsl:if test="@ccid"><xsl:value-of select="translate(@ccid,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>/</xsl:if></xsl:variable>
		<xsl:variable name="cversion"><xsl:if test="@cversion"><xsl:value-of select="@cversion"/>/</xsl:if></xsl:variable>
		<xsl:variable name="cccompl"><xsl:if test="@cccompl!='nd'"><xsl:value-of select="translate(@cccompl,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>/</xsl:if></xsl:variable>
		
		<xsl:apply-templates select="." mode="license-element">
			<xsl:with-param name="href" select="concat('https://creativecommons.org/licenses/',$ccid,$cversion,$cccompl)"/>
		</xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="extra-scielo/license">
		<xsl:variable name="ccid"><xsl:value-of select="../license-type"/>/</xsl:variable>
		<xsl:variable name="cversion"><xsl:value-of select="../license-version"/></xsl:variable>
		<xsl:variable name="cccompl">/<xsl:value-of select="../license-complement"/></xsl:variable>
		
		<xsl:apply-templates select="." mode="license-element">
			<xsl:with-param name="href" select="concat('https://creativecommons.org/licenses/',$ccid,$cversion,$cccompl)"/>
		</xsl:apply-templates>
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
	
	<xsl:template match="contract" mode="front-funding-group">
		<award-id>
			<xsl:apply-templates/>
		</award-id>
	</xsl:template>
	
	<xsl:template match="rsponsor | fundsrc" mode="front-funding-group">
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
	<xsl:template match="report" mode="front-funding-group">
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
	
	<xsl:template match="ack//funding|fngrp//funding|fn//funding" mode="front-funding-group">
		<xsl:param name="statement"/>
		<xsl:if test=".//contract">
			<funding-group>
				<xsl:apply-templates select="award[contract]" mode="front-funding-group"></xsl:apply-templates>
				<xsl:if test="$statement='true'">
					<funding-statement><xsl:apply-templates select=".//text()"/></funding-statement>
				</xsl:if>
			</funding-group>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="award" mode="front-funding-group">
		<!-- formato que pareia orgname e numero
		<xsl:apply-templates select=".//fundsrc" mode="award-group">
			<xsl:with-param name="contract" select=".//contract"/>
		</xsl:apply-templates>
		-->
		<!-- agrupa todos orgnames + numero -->
		<award-group>
			<xsl:attribute name="award-type">contract</xsl:attribute>
			<xsl:apply-templates select=".//fundsrc" mode="front-funding-group"/>
			<xsl:apply-templates select=".//contract" mode="front-funding-group"/>
		</award-group>
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
			<xsl:apply-templates select="$fundsrc" mode="front-funding-group"/>
			<xsl:apply-templates select="." mode="front-funding-group"/>
		</award-group>
	</xsl:template>
	
	<xsl:template match="edition/sup">
		<xsl:apply-templates select="text()"/>
	</xsl:template>
	
	<xsl:template match="boxedtxt">
		<boxed-text>
			<xsl:apply-templates select="@id"/>
			<xsl:choose>
				<xsl:when test="sectitle">
					<sec>
						<xsl:apply-templates select="*|text()"/>
					</sec>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="*|text()"/>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="cpright | licinfo"/>
		</boxed-text>
	</xsl:template>
	
	<xsl:template match="@reftype">
		<xsl:attribute name="publication-type"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	
	<xsl:template match="ref/@status|@refstatus">
		<xsl:if test=".='incomplete'">
			<xsl:attribute name="specific-use">display-only</xsl:attribute>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="versegrp">
		<verse-group>
			<xsl:apply-templates select="@*|*|text()"/>
		</verse-group>
	</xsl:template>
	
	<xsl:template match="versline">
		<verse-line><xsl:apply-templates select="@*|*|text()"/></verse-line>
	</xsl:template>
	
	<xsl:template match="alttitle">
		<xsl:param name="lang">
			<xsl:choose>
				<xsl:when test="@language">
					<xsl:value-of select="@language"/>
				</xsl:when>
				<xsl:when test="../@language">
					<xsl:value-of select="../@language"/>
				</xsl:when>
				<xsl:when test="../../@language">
					<xsl:value-of select="../../@language"/>
				</xsl:when>
			</xsl:choose>
		</xsl:param>
		<alt-title>
			<xsl:if test="$lang!=''">
				<xsl:attribute name="xml:lang"><xsl:value-of select="$lang"/></xsl:attribute>
			</xsl:if>
			<xsl:apply-templates select="@*|*|text()"/></alt-title>
	</xsl:template>
	
	<xsl:template match="alttext">
		<alt-text><xsl:apply-templates select="@*|*|text()"/></alt-text>
	</xsl:template>
	<xsl:template match="xref[@ref-type='other']">
		<xsl:variable name="rid"><xsl:value-of select="@rid"/></xsl:variable>
		<xsl:if test="$elem_id[@id=$rid]">
			<xref>
				<xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
			</xref>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="licinfo">
		<xsl:if test="not(../cpright)">
			<permissions>
				<xsl:apply-templates select="." mode="license"/>
				<xsl:apply-templates select="..//subdoc[@subarttp='translation']" mode="license-element"/>
			</permissions>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="cpright">
		<permissions>
			<xsl:apply-templates select="." mode="copyright"/>
			<xsl:choose>
				<xsl:when test="../licinfo">
					<xsl:apply-templates select="../licinfo" mode="license"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="../back/licenses| ../cc | ..//extra-scielo/license"/>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="..//subdoc[@subarttp='translation']" mode="license-element"/>
		</permissions>
	</xsl:template>
	
	<xsl:template match="cpright" mode="copyright">
		<copyright-statement><xsl:apply-templates select="cpyear | cpholder | text()" mode="text-only"/></copyright-statement>
		<xsl:if test="cpyear">
			<copyright-year><xsl:value-of select="cpyear"/></copyright-year>
		</xsl:if>
		<xsl:if test="cpholder">
			<copyright-holder><xsl:value-of select="cpholder"/></copyright-holder>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="cpright//text()" mode="text-only">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="cpright/*" mode="text-only">
		<xsl:apply-templates select="*|text()" mode="text-only"/>
	</xsl:template>
	<xsl:template match="licinfo/@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="licinfo/@language">
		<xsl:attribute name="xml:lang"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="licinfo" mode="license">
		<license>
			<xsl:attribute name="license-type">open-access</xsl:attribute>
			<xsl:apply-templates select="@*"/>
			<xsl:choose>
				<xsl:when test="not(*)">
					<license-p>
						<xsl:apply-templates select="text()"/>
					</license-p>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="*|text()"/>
				</xsl:otherwise>
			</xsl:choose>
			
		</license>
	</xsl:template>
	
	<xsl:template match="*" mode="name">
		<xsl:value-of select="name()"/>
	</xsl:template>

	<xsl:template match="@ref-type[.='author-notes']">
		<xsl:attribute name="ref-type">fn</xsl:attribute>
	</xsl:template>

</xsl:stylesheet>
