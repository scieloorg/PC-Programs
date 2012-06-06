<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="unident" select="//unidentified"/>
	<xsl:variable name="corresp" select="//corresp"/>
	<xsl:variable name="deceased" select="//fngrp[@fntype='deceased']"/>
	<xsl:variable name="eqcontrib" select="//fngrp[@fntype='equal']"/>
	<xsl:variable name="unident_back" select="//back//unidentified"/>
	<xsl:variable name="fn_author" select=".//fngrp[@fntype='author']"/>
	<xsl:variable name="fn" select=".//fngrp"/>
	
	<xsl:variable name="xref_id" select="//*[@id]"/>
	<xsl:variable name="journal_acron" select="//extra-scielo/journal-acron"/>
	<xsl:variable name="JOURNAL_PID" select="node()/@issn"/>
	<xsl:variable name="journal_vol" select="node()/@volid"/>
	<xsl:variable name="PUB_TYPE" select=".//extra-scielo/issn-type"/>
	<xsl:variable name="CURRENT_ISSN" select=".//extra-scielo/current-issn"/>
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
	<xsl:variable name="prefix" select="concat($JOURNAL_PID,'-',$journal_acron,'-',$journal_vol,'-',$article_page,'-')"/>
	<!--xsl:variable name="g" select="//*[name()!='equation' and .//graphic]"/>
	<xsl:variable name="e" select="//equation[.//graphic]"/-->
	<xsl:variable name="data4previous" select="//back//*[contains(name(),'citat')]"/>
	<!--
    	mode=text
	-->
	<xsl:template match="*" mode="text"><xsl:apply-templates select="*|text()" mode="text"/></xsl:template>
	<xsl:template match="text()" mode="text"><xsl:value-of select="."/></xsl:template>
	<xsl:template match="text()">
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
	</xsl:template>
	
	<xsl:template match="@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
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
				<xsl:apply-templates select="@*| * | text()"/>
			</title>
		</caption>
	</xsl:template>
	
	<xsl:template match="aff/zipcode | aff/city | aff/state | aff/country ">
		<!-- addr-line content-type="{name()}">
			<xsl:value-of select="."/>
		</addr-line> -->
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="et-al">
		<etal/>
	</xsl:template>
	<xsl:template match="ign"></xsl:template>
	<xsl:template match="list"><p>
		<list>
			<xsl:apply-templates select="@*|*"/>
		</list></p>
	</xsl:template>
	<xsl:template match="@listtype"><xsl:attribute name="list-type"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="li">
		<list-item>
			<xsl:apply-templates select="*"/>
		</list-item>
	</xsl:template>
	<xsl:template match="lilabel"><label><xsl:value-of select="."/></label>
	</xsl:template>
	<xsl:template match="litext"><p><xsl:apply-templates select="* | text()"/></p>
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
	
	<xsl:template match="uri | p | sec | bold  | sub | sup |  label | subtitle | edition |  issn | italic | corresp | ack | sig-block">
		<xsl:param name="id"/>
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*| * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@corresp | @deceased"><xsl:if test=".='yes'"><xsl:if test="not($fn[@fntype=name()])"><xsl:attribute name="{name()}">yes</xsl:attribute></xsl:if></xsl:if>
	</xsl:template>
	<xsl:template match="@eqcontr"><xsl:if test=".='yes'"><xsl:if test="not($fn[@fntype='eq-contrib'])"><xsl:attribute name="eq-contrib">yes</xsl:attribute></xsl:if></xsl:if>
	</xsl:template>
	<xsl:template match="sigblock">
		<xsl:param name="id"/>
		<sig-block>
			<xsl:apply-templates select="@*| * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</sig-block>
	</xsl:template>
	<xsl:template match="version"><edition><xsl:value-of select="."/></edition>
	</xsl:template>
	<xsl:template match="issn[contains(.,'PMID:')]">
		<pub-id pub-id-type="pmid"><xsl:value-of select="substring-after(., 'PMID:')"/></pub-id>
	</xsl:template>
	<xsl:template match="@doctopic" mode="type">
		<xsl:attribute name="article-type"><xsl:choose><xsl:when test=".='oa'">research-article</xsl:when><xsl:when test=".='ab'">abstract</xsl:when><xsl:when test=".='an'">announcement</xsl:when><xsl:when test=".='co'">article-commentary</xsl:when><xsl:when test=".='cr'">case-report</xsl:when><xsl:when test=".='ed'">editorial</xsl:when><xsl:when test=".='le'">letter</xsl:when><xsl:when test=".='ra'">review-article</xsl:when><xsl:when test=".='sc'">rapid-communication</xsl:when><xsl:when test=".='??'">addendum</xsl:when><xsl:when test=".='??'">book-review</xsl:when><xsl:when test=".='??'">books-received</xsl:when><xsl:when test=".='??'">brief-report</xsl:when><xsl:when test=".='??'">calendar</xsl:when><xsl:when test=".='??'">collection</xsl:when><xsl:when test=".='??'">correction</xsl:when><xsl:when test=".='??'">discussion</xsl:when><xsl:when test=".='??'">dissertation</xsl:when><xsl:when test=".='??'">in-brief</xsl:when><xsl:when test=".='??'">introduction</xsl:when><xsl:when test=".='??'">meeting-report</xsl:when><xsl:when test=".='??'">news</xsl:when><xsl:when test=".='??'">obituary</xsl:when><xsl:when test=".='??'">oration</xsl:when><xsl:when test=".='??'">partial-retraction</xsl:when><xsl:when test=".='??'">product-review</xsl:when><xsl:when test=".='??'">reply</xsl:when><xsl:when test=".='??'">reprint</xsl:when><xsl:when test=".='??'">retraction</xsl:when><xsl:when test=".='??'">translation</xsl:when><xsl:otherwise>other</xsl:otherwise></xsl:choose></xsl:attribute>
	</xsl:template>
	<xsl:template match="@language">
		<xsl:attribute name="xml:lang"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
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
			<xsl:if test=".//nlm-title"><journal-id journal-id-type="nlm-ta"><xsl:value-of select=".//nlm-title"/></journal-id></xsl:if>
			<journal-id journal-id-type="publisher-id">
				<xsl:value-of select="$JOURNAL_PID"/>
			</journal-id>
			<journal-title-group>
			<xsl:copy-of select=".//journal-title"/>
				<abbrev-journal-title abbrev-type="publisher">
					<xsl:value-of select="@stitle"/>
				</abbrev-journal-title>
				
			</journal-title-group>
			<issn pub-type="{$PUB_TYPE}">
				<xsl:value-of select="$CURRENT_ISSN"/>
			</issn>
			<publisher>
				<publisher-name>
					<xsl:apply-templates select="..//extra-scielo/publisher/publisher-name"/>
				</publisher-name>
			</publisher>
			
		</journal-meta>
	</xsl:template>
	<xsl:template match="extra-scielo/publisher/publisher-name">
		<xsl:value-of select="."></xsl:value-of><xsl:if test="position()!=last()">, </xsl:if>
	</xsl:template>
	<xsl:template match="front/doi | text/doi">
		<article-id pub-id-type="doi"><xsl:value-of select="."/></article-id>
	</xsl:template>
	<xsl:template match="article|text" mode="article-meta">
		<xsl:variable name="l" select="@language"/>
		<article-meta>
			<xsl:if test="..//extra-scielo/issue-order">
				<article-id pub-id-type="publisher-id">S<xsl:value-of select="$JOURNAL_PID"/>
					<xsl:value-of select="substring(@dateiso,1,4)"/>
					<xsl:value-of select="substring(10000 + substring(..//extra-scielo/issue-order,5),2)"/>
					<xsl:value-of select="substring-after(100000 + @order,'1')"/>
				</article-id>
				<xsl:apply-templates select="front/doi|doi"></xsl:apply-templates>
				
			</xsl:if>
			
			<article-categories>
					<subj-group>
						<xsl:if test=".//toctitle">
						<subject><xsl:value-of select="normalize-space(.//toctitle)"/></subject></xsl:if>
					</subj-group>
				</article-categories>
			<xsl:apply-templates select="." mode="article-title"/>
			<xsl:apply-templates select=".//authgrp" mode="front"/>
			<xsl:apply-templates select="." mode="author-notes"/>
			<xsl:variable name="epub_date"><xsl:choose>
					<xsl:when test="@rvpdate">
						<xsl:value-of select="@rvpdate"/>
					</xsl:when>
					<xsl:when test="@ahpdate">
						<xsl:value-of select="@ahpdate"/>
					</xsl:when></xsl:choose></xsl:variable>
			
			<xsl:if test="string-length($epub_date)&gt;0">
				<pub-date pub-type="epub">
					<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso"><xsl:value-of select="$epub_date"/></xsl:with-param>
					</xsl:call-template>
				</pub-date>
			</xsl:if>
			
			
			<xsl:variable name="date_type"><xsl:choose><xsl:when test="$PUB_TYPE='epub'">collection</xsl:when><xsl:otherwise>ppub</xsl:otherwise></xsl:choose>
			</xsl:variable>
			<pub-date pub-type="{$date_type}">
				<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso"><xsl:value-of select="@dateiso"/></xsl:with-param>
					<xsl:with-param name="date"><xsl:value-of select="//extra-scielo//season"/></xsl:with-param>
					</xsl:call-template>
			</pub-date>
			
			<xsl:apply-templates select="@volid | @issueno | @supplvol | @supplno | @fpage | @lpage"/>
			<xsl:apply-templates select=".//hist" mode="front"/>
			<xsl:apply-templates select=".//back/licenses"/>
			<xsl:apply-templates select=".//abstract[@language=$l]|.//xmlabstr[@language=$l]"/>
			<xsl:apply-templates select=".//abstract[@language!=$l]|.//xmlabstr[@language!=$l]" mode="trans"/>
			<xsl:apply-templates select=".//keygrp"/>
			<xsl:apply-templates select=".//front/report | .//front/confgrp | ..//front/thesgrp | .//bibcom/report | .//bibcom/confgrp | ..//bibcom/thesgrp  | .//bbibcom/report | .//bbibcom/confgrp | ..//bbibcom/thesgrp "/>
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
			<xsl:if test="onbehalf"><on-behalf-of><xsl:value-of select="onbehalf"/></on-behalf-of></xsl:if>
			<xsl:if test="count(..//aff)=1"><xsl:apply-templates select="..//aff"/></xsl:if>
		</contrib-group>
		<xsl:if test="count(..//aff)&gt;1"><xsl:apply-templates select="..//aff"/></xsl:if>
	</xsl:template>
	<xsl:template match="@role">
		<xsl:attribute name="contrib-type"><xsl:choose><xsl:when test=".='nd'">author</xsl:when><xsl:when test=".='ed'">editor</xsl:when><xsl:when test=".='tr'">translator</xsl:when><xsl:when test=".='rev'">rev</xsl:when></xsl:choose></xsl:attribute>
	</xsl:template>
	<xsl:template match="author/@*[.='y']" ><xsl:if test="not($corresp)"><xsl:attribute name="{name()}">yes</xsl:attribute>
	</xsl:if></xsl:template>
	
	<xsl:template match="author/@deceased[.='y']" ><xsl:if test="not($deceased)"><xsl:attribute name="{name()}">yes</xsl:attribute>
	</xsl:if></xsl:template>
	
	<xsl:template match="author/@eqcontr[.='y']" ><xsl:if test="not($eqcontrib)"><xsl:attribute name="equal-contrib">yes</xsl:attribute>
	</xsl:if></xsl:template>
	<xsl:template match="author" mode="front">
		<contrib>
		<!-- xsl:if test="contains($corresp,.//fname) and contains($corresp,//surname)"><xsl:attribute name="corresp">yes</xsl:attribute></xsl:if> -->
			<xsl:apply-templates select="@*[name()!='rid']"/>
			<xsl:apply-templates select="."/>
			<xsl:apply-templates select="@rid"/>
			<xsl:apply-templates select="xref"/>
		</contrib>
	</xsl:template>
	
	<xsl:template match="authgrp/corpauth" mode="front">
		<xsl:variable name="teste"><xsl:apply-templates select="./../../authgrp" mode="text"/></xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($teste,'behalf')">
			<on-behalf-of>
			<xsl:apply-templates select="orgdiv"/><xsl:if test="orgdiv and orgname">, </xsl:if><xsl:apply-templates select="orgname"/>
			</on-behalf-of>
			</xsl:when>
			<xsl:otherwise>
			<contrib>
			<xsl:apply-templates select="@role"/>
			<xsl:apply-templates select="."/>
			<xsl:apply-templates select="@rid"/>
		</contrib>
			</xsl:otherwise>
		</xsl:choose>
		
	</xsl:template>
	<xsl:template match="author/sup"><xsl:value-of select=".//text()"/>
	</xsl:template>
	<xsl:template match="author/@rid">
		<xref ref-type="aff" rid="aff{substring(normalize-space(.),3,1)}"><xsl:apply-templates select="../sup" mode="label"/></xref>
		<xsl:if test="string-length(normalize-space(.))&gt;3">
			<xref ref-type="aff" rid="aff{substring(substring-after(normalize-space(.),' '),3,1)}"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="aff">
		<aff id="aff{substring(@id,3)}">
			<!-- xsl:apply-templates select="@*[name()!='id']"/> -->
			<xsl:apply-templates select="*|text()"/>
		</aff>
	</xsl:template>
	
	<!-- xsl:template match="aff/@orgdiv1 | aff/@orgdiv2 | aff/@orgdiv3"/>
	<xsl:template match="aff/@orgdiv1 | aff/@orgdiv2 | aff/@orgdiv3" mode="org-aff">
		<xsl:value-of select="."/>, 
	</xsl:template>
	<xsl:template match="aff/@orgname">
		<institution>
			<xsl:apply-templates select="../@orgdiv3" mode="org-aff"/>
			<xsl:apply-templates select="../@orgdiv2" mode="org-aff"/>
			<xsl:apply-templates select="../@orgdiv1" mode="org-aff"/>
			<xsl:value-of select="."/>
		</institution>
	</xsl:template> -->
	<xsl:template match="e-mail|email">
		<email>
			<xsl:apply-templates/>
		</email>
	</xsl:template>
	<xsl:template match="*" mode="author-notes">
		<xsl:variable name="fnauthors"><xsl:apply-templates select="$fn" mode="fnauthors"/></xsl:variable>
	<xsl:if test="$corresp or $fnauthors!='' ">
		<author-notes>
		<xsl:apply-templates select="$corresp"></xsl:apply-templates>	
		<xsl:apply-templates select="$fn" mode="fnauthors"/>
		</author-notes></xsl:if>
	</xsl:template>
	
	<xsl:template match="fngrp" mode="fnauthors">
		<xsl:choose>
			<xsl:when test="contains('abbr|finanacial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype)"></xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="."/>
			</xsl:otherwise>
			</xsl:choose>
	</xsl:template>
	<xsl:template match="fngrp" mode="notfnauthors">
		<xsl:choose>
			<xsl:when test="contains('abbr|finanacial-disclosure|other|presented-at|supplementary-material|supported-by',@fntype)">
			<xsl:apply-templates select="."/>
			</xsl:when>
			<xsl:otherwise>
				
			</xsl:otherwise>
			</xsl:choose>
	</xsl:template>
	<xsl:template match="@fntype[.='author']"><xsl:attribute name="fn-type">other</xsl:attribute>
	</xsl:template>
	
	<xsl:template match="@volid | volid">
		<volume>
			<xsl:value-of select="."/>
		</volume>
	</xsl:template>
	<xsl:template match="part"><issue-part><xsl:value-of select="."/></issue-part>
	</xsl:template>
	<xsl:template match="@issueno | issueno">
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
		<!-- page-range>
			<xsl:value-of select="."/>
		</page-range> -->
		
		<xsl:choose>
			<xsl:when test="substring(.,1,1)='e'">
				<xsl:variable name="e" select="substring-after(.,'e')"/>
			    <xsl:if test="normalize-space(translate($e,'0123456789','          '))=''">
				<elocation-id><xsl:value-of select="."/></elocation-id></xsl:if>
			</xsl:when>
			<xsl:when test="substring(.,1,1)='E'">
				<xsl:variable name="e" select="substring-after(.,'E')"/>
			    <xsl:if test="normalize-space(translate($e,'0123456789','          '))=''">
				<elocation-id><xsl:value-of select="."/></elocation-id></xsl:if>
			</xsl:when>
			<xsl:when test="contains(.,';') or contains(.,',')">
				<page-range><xsl:value-of select="."/></page-range>
			</xsl:when>
			<xsl:when test="contains(.,'-')">
				<xsl:variable name="fpage"><xsl:value-of select="substring-before(.,'-')"/></xsl:variable>
				<xsl:variable name="lpage"><xsl:value-of select="substring-after(.,'-')"/></xsl:variable>
				
				<fpage><xsl:value-of select="$fpage"/></fpage>
				<lpage>
				<xsl:if test="string-length($lpage)&lt;string-length($fpage)">
					<xsl:value-of select="substring($fpage,1,string-length($fpage)-string-length($lpage))"/>
				</xsl:if><xsl:value-of select="substring-after(.,'-')"/></lpage>
			</xsl:when>
			<xsl:otherwise>
				<fpage><xsl:value-of select="."/></fpage>
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
					<xsl:with-param name="dateiso"><xsl:value-of select="@dateiso"/></xsl:with-param>
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
			<fig-count count="{count(.//figgrp)}"/>
			<table-count count="{count(.//tabwrap)}"/>
			<equation-count count="{count(.//equation)}"/>
			<ref-count count="{count(.//back//*[contains(name(),'citat')])}"/>
			<page-count count="{@lpage - @fpage + 1}"/>
			<!--word-count count="2847"/-->
		</counts>
	</xsl:template>
	<xsl:template match="@sec-type[.='nd']">
	</xsl:template>
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
			<xsl:apply-templates select="following-sibling::node()[1 and name()='xref']" mode="xref-in-sectitle"/>
		</title>
	</xsl:template>
	<!--xsl:template match="@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template-->
	<!-- BACK -->
	<xsl:template match="article|text" mode="back">
		<xsl:if test="back/fngrp[@fntype] or back/ack or back/fxmlbody or back/*[@standard] or back/bbibcom">
			<back>
				<xsl:apply-templates select="back"/>
			</back>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template match="back">
				<xsl:apply-templates select="fxmlbody[@type='ack']|ack"/>
				<xsl:apply-templates select="*[@standard]"/>
				<xsl:variable name="test"><xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"></xsl:apply-templates></xsl:variable>
				<xsl:if test="$test!=''">
					<fn-group>
						<xsl:apply-templates select=".//fngrp[@fntype]" mode="notfnauthors"></xsl:apply-templates>
					</fn-group> 
				</xsl:if>
	</xsl:template>
	
	
	<xsl:template match="back//fngrp[@fntype]">
		<fn><xsl:apply-templates select="@*|label"/><p><xsl:apply-templates select="*[name()!='label']|text()"/></p></fn>
	</xsl:template>
	<xsl:template match="fngrp/@fntype">
		<xsl:attribute name="fn-type"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	
	<xsl:template match="tified">
	</xsl:template>
	
	<xsl:template match="fxmlbody[@type='ack']">
		<ack>
			<xsl:copy-of select="*"/>
		</ack>
	</xsl:template>
	
	
	<xsl:template match="*[contains(name(),'citat')]/text() | *[contains(name(),'citat')]//*[*]/text()"/>
	
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
		<xsl:variable name="id"><xsl:if test="position()&lt;10">0</xsl:if><xsl:value-of select="position()"/></xsl:variable>
		<ref id="r{$id}">
			<xsl:apply-templates select="no"/>
			<!-- book, communication, letter, review, conf-proc, journal, list, patent, thesis, discussion, report, standard, and working-paper.  -->
			<xsl:variable name="type">
				<xsl:choose>
					<xsl:when test="viserial or aiserial or oiserial or iiserial or piserial">journal</xsl:when>
					<xsl:when test=".//confgrp">conf-proc</xsl:when>
					<xsl:when test=".//degree">thesis</xsl:when>
					<xsl:when test=".//patgrp">patent</xsl:when>
					<xsl:when test=".//report">report</xsl:when>
					<xsl:when test=".//version">software</xsl:when>
					<xsl:when test=".//url and .//cited and not (.//pages or .//extent)">web</xsl:when>
					<xsl:when test="vmonog or amonog or omonog or imonog or pmonog">book</xsl:when>
					<xsl:otherwise>other</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<element-citation publication-type="{$type}">
				<xsl:apply-templates select="*[name()!='no' and name()!='text-ref']">
					<xsl:with-param name="position" select="position()"/>
				</xsl:apply-templates>
				<xsl:apply-templates select="." mode="text-ref"/>
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
			<xsl:when test="../city">
					
			</xsl:when>
			<xsl:when test="../state">
				
			</xsl:when>
			<xsl:otherwise>
				<publisher-loc><xsl:value-of select="."/></publisher-loc>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//city">
		<publisher-loc><xsl:value-of select="."/>
		<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
		<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</publisher-loc>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//state">
		<xsl:choose>
			<xsl:when test="../city">
					
			</xsl:when>
			<xsl:otherwise>
				<publisher-loc><xsl:value-of select="."/><xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if></publisher-loc>
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
		<xsl:if test=".//*[fname] or .//*[orgname]">
			<person-group person-group-type="{$type}">
				
				<xsl:apply-templates select=".//*[fname] | .//*[orgname] | .//et-al">
				
			</xsl:apply-templates>
			</person-group>
		</xsl:if>
		<xsl:apply-templates select="*[not(fname) and not(orgname)]"/>
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
	<xsl:template match="back//orgdiv">
	</xsl:template>
	<xsl:template match="back//orgname">
		<publisher-name>
			<xsl:if test="../orgdiv">
				<xsl:value-of select="../orgdiv"/>, </xsl:if>
			<xsl:value-of select="."/>
		</publisher-name>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'corpaut')]/text()"><xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'corpaut')]/orgdiv|back//*[contains(name(),'corpaut')]/orgname"><xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="*[contains(name(),'author')]">
		<name>
		<xsl:choose>
			<xsl:when test="contains(surname,' ')">
			<xsl:choose>
			<xsl:when test="contains(surname,' Jr') or contains(surname,' Sr') or contains(surname,'nior')">
				<surname><xsl:value-of select="substring-before(surname,' ')"/></surname>
				
			</xsl:when>
			<xsl:when test="contains(surname,' Neto')">
				<surname><xsl:value-of select="substring-before(surname,' Neto')"/></surname>
				
			</xsl:when>
			<xsl:when test="contains(surname,' Filho')">
				<surname><xsl:value-of select="substring-before(surname,' Filho')"/></surname>
				
			</xsl:when>
			<xsl:when test="contains(surname,' Sobrinho')">
				<surname><xsl:value-of select="substring-before(surname,' Sobrinho')"/></surname>
				
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="surname"/>
			</xsl:otherwise>
			</xsl:choose>
			</xsl:when>
			<xsl:otherwise><xsl:apply-templates select="surname"/></xsl:otherwise>
		</xsl:choose>
			
		<xsl:apply-templates select="fname"/>
			
		<xsl:if test="contains(surname,' ')">
				<xsl:choose>
					<xsl:when test="contains(surname,' Jr') or contains(surname,' Sr') or contains(surname,'nior')">
						
						<suffix><xsl:value-of select="substring-after(surname,' ')"/></suffix>
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
					<xsl:otherwise>
						
					</xsl:otherwise>
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
					<xsl:with-param name="dateiso"><xsl:value-of select="@dateiso"/></xsl:with-param>
					<xsl:with-param name="date"><xsl:value-of select="."/></xsl:with-param>
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
	
	<xsl:template match="url">
		<ext-link ext-link-type="uri" xlink:href="{.}">
			<xsl:apply-templates/>
		</ext-link>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]" mode="text-ref">
		<!-- mixed-citation specific-use="archive-only">
			<xsl:choose>
				<xsl:when test="text-ref">
					<xsl:value-of select="text-ref" disable-output-escaping="yes"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="." mode="create-text-ref"/>
				</xsl:otherwise>
			</xsl:choose>
		</mixed-citation> -->
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
			<xsl:if test="@ftype!='other'"><xsl:attribute name="fig-type"><xsl:value-of select="@ftype"/></xsl:attribute></xsl:if>
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
			<xsl:if test="@ftype!='other'"><xsl:attribute name="fig-type"><xsl:value-of select="@ftype"/></xsl:attribute></xsl:if>
			<xsl:apply-templates select=".//label"/>
			<xsl:apply-templates select=".//caption"/>
			<xsl:apply-templates select="." mode="graphic"/>
		</fig>
	</xsl:template>
	<xsl:template match="tabwrap">
		<p>
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
		</p>
	</xsl:template>
	<xsl:template match="tabwrap//notes" mode="table">
		<fn><p><xsl:value-of select="."/></p></fn>
	</xsl:template>
	<xsl:template match="tabwrap" mode="notes">
		<xsl:if test=".//notes">
		
				<table-wrap-foot>
					<xsl:apply-templates select=".//notes" mode="table"/>
					
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
	    <xsl:variable name="lang"><xsl:value-of select="../../../..//title/@language"/></xsl:variable>
				<source xml:lang="{$lang}">
					<xsl:apply-templates select="*|text()"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
				</source>
			
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'contrib')]//title">
		
		<xsl:choose>
			<xsl:when test="../../..//node()[contains(name(),'monog')]">
				<chapter-title>
					<xsl:apply-templates select="*|text()"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
				</chapter-title>
			</xsl:when>
			<xsl:otherwise>
			<xsl:choose><xsl:when test="substring(.,1,1)='[' and substring(.,string-length(.),1)=']'">
			<trans-title>
					<xsl:apply-templates select="@language"/>
					<xsl:variable name="t"><xsl:apply-templates select="*|text()"/></xsl:variable>
					<xsl:value-of select="translate(translate($t,'[',''),']','')"/>
					<xsl:apply-templates select="../subtitle" mode="title"/>
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
		<xsl:variable name="lang"><xsl:value-of select="../../../..//title/@language"/></xsl:variable>
				<source xml:lang="{$lang}">
		
			<xsl:apply-templates select="*|text()"/>
		</source>
	</xsl:template>
	<xsl:template match="*[contains(name(),'serial')]/sertitle">
			<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle"/>
	<xsl:template match="back//*[contains(name(),'monog') or contains(name(),'contrib')]//subtitle" mode="title">
		<xsl:variable name="texts"><xsl:choose>
			<xsl:when test="../../vtitle">
				<xsl:value-of select="../../../text-ref/text()"/></xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="..//text()"/></xsl:otherwise>
		</xsl:choose></xsl:variable><xsl:value-of select="substring(substring-after($texts,../title),1,2)"/>				
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	
	
	<xsl:template match="othinfo | vmonog/text()">
		<xsl:variable name="valor"><xsl:choose><xsl:when test="contains(.,'doi:')"><xsl:value-of select="substring-before(.,'doi:')"/>DOI:<xsl:value-of select="substring-after(.,'doi:')"/></xsl:when><xsl:otherwise><xsl:value-of select="."/></xsl:otherwise></xsl:choose></xsl:variable>
		<xsl:variable name="valor2"><xsl:choose><xsl:when test="contains($valor,'pmid:')"><xsl:value-of select="substring-before($valor,'pmid:')"/>PMID:<xsl:value-of select="substring-after($valor,'pmid:')"/></xsl:when><xsl:otherwise><xsl:value-of select="$valor"/></xsl:otherwise></xsl:choose></xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($valor2,'DOI:') and contains($valor2,'PMID:')">
				<xsl:variable name="teste1" select="substring-after($valor2,': ')"/>
				<xsl:choose>
					<xsl:when test="contains($teste1,'PMID')">
						<!-- DOI vem antes de PMID -->
						<xsl:variable name="doi" select="substring-before($teste1,'. PMID: ')"/>
						<xsl:variable name="pmid" select="substring-after($teste1,'PMID: ')"/>
						<pub-id pub-id-type="doi">
							<xsl:value-of select="$doi"/>
						</pub-id>
						<pub-id pub-id-type="pmid">
							<xsl:value-of select="$pmid"/>
						</pub-id>
					</xsl:when>
					<xsl:otherwise>
						<!-- DOI vem depois de PMID -->
						<xsl:variable name="pmid" select="substring-before($teste1, '. DOI: ')"/>
						<xsl:variable name="doi" select="substring-after($teste1,' DOI: ')"/>
						<pub-id pub-id-type="pmid">
							<xsl:value-of select="$pmid"/>
						</pub-id>
						<pub-id pub-id-type="doi">
							<xsl:value-of select="$doi"/>
						</pub-id>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="contains($valor2,'DOI: ')">
				<pub-id pub-id-type="doi">
					<xsl:value-of select="substring-after($valor2,'DOI: ')"/>
				</pub-id>
			</xsl:when>
			<xsl:when test="contains($valor2,'PMID: ')">
				<pub-id pub-id-type="pmid">
					<xsl:value-of select="substring-after($valor2,'PMID: ')"/>
				</pub-id>
			</xsl:when>
			<xsl:when test="contains($valor2,'serie')">
				<series>
					<xsl:value-of select="."/>
				</series>
			</xsl:when>
			<xsl:otherwise><comment><xsl:value-of select="."/></comment>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="xref/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="xref/@rid">
		<xsl:variable name="rid" select="."/>
		
		<xsl:if test="$xref_id[@id=$rid] or 'r'=substring($rid,1,1)">
			<xsl:attribute name="rid"><xsl:value-of select="."/></xsl:attribute>
		</xsl:if>
	</xsl:template>
	<xsl:template match="xref[@rid!='']">
		<xsl:variable name="rid" select="@rid"/>
		<xsl:if test="not($xref_id[@id=$rid])">
		</xsl:if>
		<xref>
			<xsl:apply-templates select="@*|*[name()!='graphic']|text()"/>
		</xref>
		<xsl:if test="graphic">
			<graphic>
				<xsl:apply-templates select="graphic/@*|graphic/*|graphic/text()"/>
				<uri>#<xsl:value-of select="@rid"/>
				</uri>
			</graphic>
		</xsl:if>
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
	<xsl:template match="*[contains(name(),'citat')]//p | *[contains(name(),'citat')]/text()">
	</xsl:template>
	<xsl:template match="*" mode="debug">
	</xsl:template>
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
		<graphic xlink:href="{$standardname}"/></xsl:if>
		<xsl:if test=".//table">
		<xsl:copy-of select=".//table"/></xsl:if>
		
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
	<xsl:template match="license/text()"><xsl:if test="normalize-space(.)!=''">

		<license-p>
			<xsl:value-of select="."/>
		</license-p></xsl:if>

	</xsl:template>
	<xsl:template match="licensep">
		<xsl:if test="normalize-space(.)!=''">
		<license-p>
			<xsl:apply-templates/>
		</license-p></xsl:if>
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
		<ext-link ext-link-type="doi" xlink:href="{$doi}"><xsl:value-of select="$doi"/></ext-link>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//doi">
		<!-- ext-link ext-link-type="doi" xlink:href="{.}"><xsl:value-of select="."/></ext-link> -->
			<pub-id pub-id-type="doi">
							<xsl:value-of select="."/>
						</pub-id>
	</xsl:template>
	<xsl:template match="sec/text() | subsec/text()"/>
	<xsl:template match="thesis">
		<xsl:apply-templates select="@* | * | text()">
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="degree ">
	</xsl:template>
	
	
	
	<xsl:template match=" *[contains(name(),'contrib')]//bold |  *[contains(name(),'monog')]//bold"/>
	<xsl:template match="subsec/xref | sec/xref">
	</xsl:template>
	<xsl:template match="*[*]" mode="next">
		<xsl:if test="position()=1">
			<xsl:value-of select="name()"/>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="caption//bold  | caption//sup |caption//italic |
	   subtitle//bold |  subtitle//sub | subtitle//sup | subtitle//italic |
	   sectitle//bold |  sectitle//sup | sectitle//italic |
	   title//bold |   title//sup  |
	   
	   label//bold | label//italic | label//sub | label//sup">
	   <xsl:choose>
	   	<xsl:when  test="*">
	   		<xsl:apply-templates select="*|text()"/>
	   	</xsl:when>
	   	<xsl:otherwise>
	   		<xsl:value-of select="."/>
	   	</xsl:otherwise>
	   </xsl:choose>
	   		
	   	
	</xsl:template>
	
	
	<xsl:template match="*//text()[.=' ']"><xsl:value-of select="."/>
	</xsl:template>
	
	
	<xsl:template match="figgrps/figgrp/caption"><caption>
			<p>
				<xsl:apply-templates select="@*| * | text()"/>
			</p>
		</caption>
	</xsl:template>
	<xsl:template match="edition//italic | edition//bold | edition//sub | edition//sup "><xsl:value-of select="."/></xsl:template>
	<xsl:template match="p[normalize-space(text())='']"></xsl:template>
	
	<xsl:template name="display_date">
		<xsl:param name="dateiso"/>
		<xsl:param name="date" select="''"/>
		<xsl:variable name="y"><xsl:value-of select="substring($dateiso,1,4)"/></xsl:variable>
				
		<xsl:choose>
			<xsl:when test="$date=''">
				<xsl:if test="substring($dateiso,7,2)!='00'"><day><xsl:value-of select="substring($dateiso,7,2)"/></day></xsl:if>
				<xsl:if test="substring($dateiso,5,2)!='00'"><month><xsl:value-of select="substring($dateiso,5,2)"/></month></xsl:if>
			</xsl:when>
			
			<xsl:when test="contains($date,'-') or contains($date,'/') or contains($date,'Summer') or contains($date,'Winter') or contains($date,'Autumn') or contains($date,'Fall') or contains($date,'Spring')">
				<xsl:choose>
					<xsl:when test="contains($date,$y)">
					<xsl:variable name="d"><xsl:value-of select="substring-before($date,$y)"/><xsl:value-of select="substring-after($date,$y)"/></xsl:variable>
					<xsl:variable name="season"><xsl:value-of select="translate(translate(translate($d,' ',''),'.',''),'/','-')"/></xsl:variable>
					
					<xsl:if test="$season!=''">
						<season><xsl:value-of select="$season"/></season></xsl:if>
					</xsl:when>
					<xsl:otherwise>
							<season><xsl:value-of select="translate(translate(translate($date,' ',''),'.',''),'/','-')"/></season>
					</xsl:otherwise>
				</xsl:choose>
				
			</xsl:when>
			
			<xsl:otherwise>
				
			</xsl:otherwise>
		</xsl:choose>
					
		<year>
			<xsl:value-of select="substring($dateiso,1,4)"/>
		</year>
	</xsl:template>	

	<xsl:template match="inpress"><comment><xsl:value-of select="."/></comment>
	</xsl:template>	

	<xsl:template match="sciname | title//sciname">
		<named-content content-type="scientific-name">
			<xsl:apply-templates/>
		</named-content>
	</xsl:template>
	<xsl:template match="quote"><disp-quote><p><xsl:value-of select="."/></p></disp-quote></xsl:template>
	
	
	<xsl:template match="confgrp">
		<conference><xsl:apply-templates select="*|text()"/></conference>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//confgrp">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="confgrp/date">
		<conf-date><xsl:value-of select="."/></conf-date>
	</xsl:template>
	<xsl:template match="confgrp/sponsor">
		<conf-sponsor><xsl:value-of select="."/></conf-sponsor>
	</xsl:template>
	<xsl:template match="confgrp/city">
		<conf-loc><xsl:value-of select="."/>
		<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
		<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</conf-loc>
	</xsl:template>
	<xsl:template match="confgrp/state">
		<xsl:if test="not(../city)">
		
		<conf-loc><xsl:value-of select="."/>
		<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</conf-loc></xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/country">
		<xsl:if test="not(../city) and not(../state)">
		
		<conf-loc><xsl:value-of select="."/>
		</conf-loc></xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/no"/>
	<xsl:template match="confgrp/confname"><conf-name><xsl:apply-templates select="../..//confgrp" mode="fulltitle"/></conf-name></xsl:template>
		
	<xsl:template match="confgrp" mode="fulltitle">
		<xsl:apply-templates select="no|confname" mode="fulltitle"/></xsl:template>
		
	<xsl:template match="confgrp/confname | confgrp/no"  mode="fulltitle"><xsl:value-of select="."/> &#160; </xsl:template>
	
	<xsl:template match="coltitle"><series><xsl:value-of select="."/></series></xsl:template>
	
</xsl:stylesheet>
