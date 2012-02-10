<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="unident" select="//unidentified"/>
	<xsl:variable name="corresp" select="$unident[contains(.//text(),'Corresp')]"/>
	<xsl:variable name="corresp2" select="$unident[.//email]"/>
	<xsl:variable name="cit" select="$unident[not(sec) and contains(.,'Refer') ]"/>
	<xsl:variable name="xref_id" select="//*[@id]"/>
	<xsl:variable name="journal_acron" select="//extra-scielo/journal-acron"/>
	<xsl:variable name="JOURNAL_PID" select="node()/@issn"/>
	<xsl:variable name="journal_vol" select="node()/@volid"/>
	<xsl:variable name="subject" select="$unident[1]//text()"/>
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
	
	-->
	<xsl:template match="text()">
		<xsl:value-of select="." disable-output-escaping="no"/>
	</xsl:template>
	<xsl:template match="text()[normalize-space(.)='']"/>
	<xsl:template match="*">
		<xsl:apply-templates select="@*| * | text()"/>
	</xsl:template>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template>
	<xsl:template match="@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
		<!--xsl:value-of select="name()"/>="<xsl:value-of select="normalize-space(.)"/>" -->
	</xsl:template>
	<xsl:template match="fname">
		<given-names>
			<xsl:apply-templates/>
		</given-names>
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
	<xsl:template match="aff/zipcode | aff/city | aff/state">
		<addr-line content-type="{name()}">
			<xsl:value-of select="."/>
		</addr-line>
	</xsl:template>
	<xsl:template match="et-al">
		<etal>
			<xsl:value-of select="."/>
		</etal>
	</xsl:template>
	<xsl:template match="ign"></xsl:template>
	<xsl:template match="list">
		<xsl:variable name="label"><xsl:value-of select="normalize-space(item[1]/label)"/></xsl:variable>
	    <xsl:variable name="label2"><xsl:if test="count(item)&gt;1"><xsl:value-of select="normalize-space(item[2]/label)"/></xsl:if>
	    </xsl:variable>
	    <xsl:variable name="pattern">
			<xsl:choose>
			    <xsl:when test="@type='bullet'"><xsl:value-of select="@type"/></xsl:when>
				<xsl:when test="$label!=''">
					<xsl:choose>
						<xsl:when test="contains($label,'1')"><xsl:value-of select="concat(substring-before($label,'1'),'#',substring-after($label,'1'))"/></xsl:when>
						<xsl:when test="contains($label,'a')"><xsl:value-of select="concat(substring-before($label,'a'),'#',substring-after($label,'a'))"/></xsl:when>
						<xsl:when test="contains($label,'A')"><xsl:value-of select="concat(substring-before($label,'A'),'#',substring-after($label,'A'))"/></xsl:when>
						<xsl:when test="contains($label,'i')"><xsl:value-of select="concat(substring-before($label,'i'),'#',substring-after($label,'i'))"/></xsl:when>
						<xsl:when test="contains($label,'I')"><xsl:value-of select="concat(substring-before($label,'I'),'#',substring-after($label,'I'))"/></xsl:when>
						<xsl:otherwise>?</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:when test="$label2!=''">
					<xsl:choose>
						<xsl:when test="contains($label2,'2')"><xsl:value-of select="concat(substring-before($label2,'2'),'#',substring-after($label2,'2'))"/></xsl:when>
						<xsl:when test="contains($label2,'b')"><xsl:value-of select="concat(substring-before($label2,'b'),'#',substring-after($label2,'b'))"/></xsl:when>
						<xsl:when test="contains($label2,'B')"><xsl:value-of select="concat(substring-before($label2,'B'),'#',substring-after($label2,'B'))"/></xsl:when>
						<xsl:when test="contains($label2,'ii')"><xsl:value-of select="concat(substring-before($label2,'ii'),'#',substring-after($label2,'ii'))"/></xsl:when>
						<xsl:when test="contains($label2,'I')"><xsl:value-of select="concat(substring-before($label2,'II'),'#',substring-after($label2,'II'))"/></xsl:when>
						<xsl:otherwise>?</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>?</xsl:otherwise>
	       	</xsl:choose>
	    </xsl:variable>
	       	<!--  se pattern != '' entao priorizar label, senao ignorar label, usar list-type -->
		
	    
	    <xsl:variable name="t">
	    	<xsl:choose>
			    <xsl:when test="$pattern='#'">
					<xsl:choose>
						<xsl:when test="contains($label,'1') or contains($label2,'2')">order</xsl:when>
						<xsl:when test="contains($label,'a') or contains($label2,'b')">alpha-lower</xsl:when>
						<xsl:when test="contains($label,'i') or contains($label2,'ii')">roman-lower</xsl:when>
						<xsl:when test="contains($label,'A') or contains($label2,'B')">alpha-upper</xsl:when>
						<xsl:when test="contains($label,'I') or contains($label2,'II')">roman-upper</xsl:when>
					</xsl:choose>
				</xsl:when>
				<xsl:when test="$pattern='bullet'">bullet</xsl:when>
				<xsl:otherwise></xsl:otherwise>
	       	</xsl:choose></xsl:variable>
	    <xsl:variable name="first">
			<xsl:choose>
				<xsl:when test="$pattern='#'">
					<xsl:choose>
						<xsl:when test="$t='order'">1</xsl:when>
						<xsl:when test="$t='alpha-lower'">a</xsl:when>
						<xsl:when test="$t='roman-lower'">I</xsl:when>
						<xsl:when test="$t='alpha-upper'">A</xsl:when>
						<xsl:when test="$t='roman-upper'">II</xsl:when>
					</xsl:choose>
				</xsl:when>
				<xsl:when test="$t='bullet'"></xsl:when>
				<xsl:otherwise>
				<xsl:choose>
						<xsl:when test="contains($label,'1') or contains($label2,'2')"><xsl:value-of select="translate($pattern,'#','1')"/></xsl:when>
						<xsl:when test="contains($label,'a') or contains($label2,'b')"><xsl:value-of select="translate($pattern,'#','a')"/></xsl:when>
						<xsl:when test="contains($label,'i') or contains($label2,'ii')"><xsl:value-of select="translate($pattern,'#','i')"/></xsl:when>
						<xsl:when test="contains($label,'A') or contains($label2,'B')"><xsl:value-of select="translate($pattern,'#','A')"/></xsl:when>
						<xsl:when test="contains($label,'I') or contains($label2,'II')"><xsl:value-of select="translate($pattern,'#','I')"/></xsl:when>
					</xsl:choose>
				</xsl:otherwise>
	       	</xsl:choose>
		</xsl:variable>
	    
		<list>
			<xsl:choose>
				<xsl:when test="$t!='' and ($pattern='#' or $pattern='bullet')">
					<xsl:attribute name="list-type"><xsl:value-of select="$t"/></xsl:attribute>
					<xsl:apply-templates select=".//item[li]">
						<xsl:with-param name="first" select="$first"/>
					</xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select=".//item[li]" mode="label">
						<xsl:with-param name="first" select="$first"/>
					</xsl:apply-templates>
				</xsl:otherwise>
	       	</xsl:choose>
	       	
		</list>
	</xsl:template>
	<xsl:template match="item"><list-item><p><xsl:apply-templates select="li"/></p></list-item>
	</xsl:template>
	<xsl:template match="item" mode="label">
		<xsl:param name="first"/> 
		<list-item><label><xsl:choose>
				<xsl:when test="label=''">
					<xsl:value-of select="normalize-space($first)"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(label)"/>
				</xsl:otherwise>
	       	</xsl:choose></label>
	       	
			<p><xsl:apply-templates select="li"/></p>
		</list-item>
	</xsl:template>
	<xsl:template match="extent">
		<size units="pages">
			<xsl:value-of select="."/>
		</size>
	</xsl:template>
	<xsl:template match="body"/>
	<xsl:template match="uri">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*"/>
			<xsl:value-of select="text()"/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="p | sec | bold  | sub | sup |  label | subtitle | edition | aff/country | issn | italic">
		<xsl:param name="id"/>
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@*| * | text()">
				<xsl:with-param name="id" select="$id"/>
			</xsl:apply-templates>
		</xsl:element>
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
			<xsl:apply-templates select="unidentified" mode="front">
				<xsl:with-param name="requiredname">xmlbody</xsl:with-param>
			</xsl:apply-templates>
		</front>
	</xsl:template>
	<xsl:template match="article|text" mode="journal-meta">
		<journal-meta>
			<xsl:copy-of select=".//journal-id"/>
			<journal-id journal-id-type="publisher-id">
				<xsl:value-of select="$JOURNAL_PID"/>
			</journal-id>
			<journal-title-group>
				<abbrev-journal-title abbrev-type="publisher">
					<xsl:value-of select="@stitle"/>
				</abbrev-journal-title>
				<xsl:copy-of select=".//journal-title"/>
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
	<xsl:template match="article|text" mode="article-meta">
		<xsl:variable name="l" select="@language"/>
		<article-meta>
			<xsl:if test="..//extra-scielo/issue-order">
				<article-id pub-id-type="publisher-id">S<xsl:value-of select="$JOURNAL_PID"/>
					<xsl:value-of select="substring(@dateiso,1,4)"/>
					<xsl:value-of select="substring(10000 + substring(..//extra-scielo/issue-order,5),2)"/>
					<xsl:value-of select="substring-after(100000 + @order,'1')"/>
				</article-id>
				
			</xsl:if>
			
			<article-categories>
					<subj-group>
						<subject>
							<xsl:choose>
								<xsl:when test="normalize-space($subject)!=''">
									<xsl:value-of select="$subject"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="..//extra-scielo/subject/text()"/>
								</xsl:otherwise>
							</xsl:choose>
							
						</subject>
					</subj-group>
				</article-categories>
			<xsl:apply-templates select="." mode="article-title"/>
			<xsl:apply-templates select=".//authgrp" mode="front"/>
			<xsl:apply-templates select="." mode="author-notes"/>
			<xsl:variable name="dateepub">
				<xsl:choose>
					<xsl:when test="@rvpdate">
						<xsl:value-of select="@rvpdate"/>
					</xsl:when>
					<xsl:when test="@ahpdate">
						<xsl:value-of select="@ahpdate"/>
					</xsl:when>
					
				</xsl:choose>
			</xsl:variable>
			<xsl:if test="string-length($dateepub)&gt;0">
				<pub-date pub-type="epub">
					<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso"><xsl:value-of select="$dateepub"/></xsl:with-param>
					</xsl:call-template>
				</pub-date>
			</xsl:if>
			
			<xsl:variable name="date">
				<xsl:choose>
					<xsl:when test="@rvpdate">
						<xsl:value-of select="@rvpdate"/>
					</xsl:when>
					<xsl:when test="@ahpdate">
						<xsl:value-of select="@ahpdate"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="@dateiso"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<xsl:variable name="datetype">
				<xsl:choose>
					<xsl:when test="@rvpdate">epub</xsl:when>
					<xsl:when test="@ahpdate">epub</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$PUB_TYPE"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<pub-date pub-type="{$datetype}">
				<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso"><xsl:value-of select="$date"/></xsl:with-param>
					</xsl:call-template>
			</pub-date>
			<xsl:apply-templates select="@volid | @issueno | @supplvol | @supplno | @fpage | @lpage"/>
			<xsl:apply-templates select=".//hist" mode="front"/>
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
	<xsl:template match="aff/@orgdiv1 | aff/@orgdiv2 | aff/@orgdiv3"/>
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
			<xsl:when test="$corresp2//p">
				<author-notes>
					<xsl:apply-templates select="$corresp2//p" mode="corresp"/>
				</author-notes>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="$unident" mode="find-corresp"/>
			</xsl:otherwise>
		</xsl:choose>
		<!--xsl:choose>
			<xsl:when test="$corresp//p">
				<xref ref-type="corresp" rid="corresp">
				</xref>
			</xsl:when>
			<xsl:when test="$corresp2//p">
				<xref ref-type="corresp" rid="corresp">
				</xref>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="$unident" mode="find-corresp"/>
			</xsl:otherwise>
		</xsl:choose-->
	</xsl:template>
	<xsl:template match="unidentified" mode="find-corresp">
		<xsl:variable name="teste">
			<xsl:apply-templates select="*|text()" mode="find-corresp"/>
		</xsl:variable>
		<xsl:if test="contains($teste,'@')">
			<author-notes>
				<xsl:apply-templates select=".//p" mode="corresp"/>
			</author-notes>
		</xsl:if>
	</xsl:template>
	<xsl:template match="unidentified//text()" mode="find-corresp">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="unidentified//*" mode="find-corresp">
		<xsl:apply-templates select="*|text()" mode="find-corresp"/>
	</xsl:template>
	<xsl:template match="p" mode="corresp">
		<corresp>
			<xsl:choose>
				<xsl:when test="contains(.,'@') and not(contains(normalize-space(.),' '))">
					<email>
						<xsl:apply-templates select="bold | italic | sup | sub | uri | text()"/>
					</email>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="bold | italic | sup | sub | uri | text()"/>
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
			<xsl:apply-templates select="xmlbody| unidentified[normalize-space(text())!='']"/>
		</body>
	</xsl:template>
	<xsl:template match="sec[contains(.//sectitle//text(),'Materials and methods')]/@sec-type"><xsl:attribute name="sec-type">materials|methods</xsl:attribute></xsl:template>
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
	<!--xsl:template match="@href">
		<xsl:attribute name="xlink:href"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template-->
	<!-- BACK -->
	<xsl:template match="*[back]" mode="back">
		<back>
			<xsl:apply-templates select="back" mode="back"/>
		</back>
	</xsl:template>
	<xsl:template match="back" mode="back">
		<xsl:variable name="preceding" select="*[@standard]/preceding-sibling::node()"/>
		<xsl:variable name="following" select="*[@standard]/following-sibling::node()"/>
		<xsl:if test="$preceding[normalize-space(.//text())!='']!='' and not(..//report)">
			<ack>
				<xsl:apply-templates select="$preceding[normalize-space(.//text())!='']" mode="back"/>
			</ack>
		</xsl:if>
		<xsl:apply-templates select="*[@standard]" mode="back"/>
		
			<xsl:apply-templates select="$following[normalize-space(.//text())!='']" mode="back-fn"/>
		
	</xsl:template>
	<xsl:template match="back//*" mode="back">
		<xsl:apply-templates select="*|text()" mode="back"/>
	</xsl:template>
	<xsl:template match="back/*" mode="back-fn">
		<xsl:variable name="text">
			<xsl:apply-templates select="*|text()" mode="text"/>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="contains($text,'@')">
				<!--xsl:attribute name="id">corresp</xsl:attribute>
				<xsl:attribute name="fn-type">corresp</xsl:attribute-->
			</xsl:when>
			<xsl:otherwise>
				<fn-group><fn>
					<xsl:apply-templates select="." mode="back"/>
				</fn></fn-group>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="back/licenses" mode="back-fn">
	</xsl:template>
	<xsl:template match="back/*" mode="back">
		<xsl:choose>
			<xsl:when test="normalize-space(.//text())=''"/>
			<xsl:when test=".//*[name()='p']">
				<xsl:apply-templates select="*|text()"/>
			</xsl:when>
			<xsl:otherwise>
			<xsl:if test="normalize-space(.//text())!=''">
				<p>
					<xsl:apply-templates select="*|text()" mode="back"/>
				</p>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="*[@standard]" mode="back">
		<ref-list>
			<xsl:choose>
				<xsl:when test="$cit">
					<xsl:apply-templates select="$cit/*"/>
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
		<xsl:if test=".//*[fname]">
			<person-group person-group-type="{$type}">
				<xsl:apply-templates select=".//*[fname]"/>
			</person-group>
		</xsl:if>
		<xsl:apply-templates select="*[not(fname)]"/>
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
		<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso"><xsl:value-of select="@dateiso"/></xsl:with-param>
			</xsl:call-template>
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
	<xsl:template match="*[contains(name(),'contrib')]">
		<xsl:param name="position"/>
		<xsl:if test=".//fname or .//surname">
		<person-group person-group-type="author">
			<xsl:apply-templates select="*[contains(name(),'aut')] | *[contains(name(),'corpaut')]">
				<xsl:with-param name="position" select="$position"/>
			</xsl:apply-templates>
		</person-group>
		</xsl:if>
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
		<ext-link ext-link-type="uri" xlink:href=".">
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
			<fig id="{@id}" fig-type="{@ftype}">
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
		<fig id="{@id}" fig-type="{@ftype}">
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
		<xsl:choose>
			<xsl:when test="contains(.,'DOI:') and contains(.,'PMID:')">
				<xsl:variable name="teste1" select="substring-after(.,': ')"/>
				<xsl:choose>
					<xsl:when test="contains($teste1,'PMID')">
						<!-- DOI vem antes de PMID -->
						<xsl:variable name="doi" select="substring-before($teste1,'. PMID: ')"/>
						<xsl:variable name="pmid" select="substring-after(.,'PMID: ')"/>
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
			<xsl:when test="contains(.,'DOI: ')">
				<pub-id pub-id-type="doi">
					<xsl:value-of select="substring-after(.,'DOI: ')"/>
				</pub-id>
			</xsl:when>
			<xsl:when test="contains(.,'PMID: ')">
				<pub-id pub-id-type="pmid">
					<xsl:value-of select="substring-after(.,'PMID: ')"/>
				</pub-id>
			</xsl:when>
			<xsl:otherwise>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="xref/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="xref/@rid">
		<xsl:variable name="rid" select="."/>
		<xsl:if test="$xref_id[@id=$rid]">
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
	<xsl:template match="*[contains(name(),'citat')]//p | *[contains(name(),'citat')]//unidentified | *[contains(name(),'citat')]/text()">

	</xsl:template>
	<xsl:template match="*" mode="debug">
	</xsl:template>
	<xsl:template match="xmlbody[sec]/p | unidentified[../xmlbody[sec]]"/>
	<xsl:template match="figgrp | tabwrap | equation" mode="graphic">
		<!--xsl:variable name="filename1">
			<xsl:choose>
				<xsl:when test="@filename">
					<xsl:value-of select="@filename"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select=".//graphic/@href"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="filename" select="substring-before($filename1,'.jpg')"/>
		<xsl:variable name="file">
			<xsl:choose>
				<xsl:when test="contains($filename,'\')">
					<xsl:value-of select="substring-before(substring-after($filename,'img\'),'.')"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$filename"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable-->
		<xsl:variable name="standardname">
			<xsl:value-of select="$prefix"/>
			<xsl:choose>
				<xsl:when test="name()='equation'">e</xsl:when>
				<xsl:otherwise>g</xsl:otherwise>
			</xsl:choose>
			<xsl:value-of select="@id"/>
		</xsl:variable>
		<graphic xlink:href="{$standardname}"/>
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
	<xsl:template match="*[contains(name(),'citat')]//doi">
		<elocation-id>
			<xsl:value-of select="."/>
		</elocation-id>
	</xsl:template>
	<xsl:template match="sec/text() | subsec/text()"/>
	<xsl:template match="thesis">
		<xsl:apply-templates select="@* | * | text()">
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="degree ">
	</xsl:template>
	<xsl:template match="fngrp">
	</xsl:template>
	<xsl:template match="fngrp[p or fn]">
		<fn-group>
			<xsl:apply-templates select="fn|p"/>
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
	</xsl:template>
	<xsl:template match="unidentified" mode="front">
	</xsl:template>
	<xsl:template match="unidentified[*] | unidentified[normalize-space(text())!='']" mode="front">
		<xsl:param name="requiredname"/>
		<xsl:variable name="next" select="following-sibling::*"/>
		<xsl:variable name="name">
			<xsl:choose>
				<xsl:when test="following-sibling::*">
					<xsl:apply-templates select="following-sibling::*" mode="next"/>
				</xsl:when>
				<xsl:when test="normalize-space($next)=''"/>
				<xsl:otherwise/>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="$name = $requiredname">
			<xsl:if test="* or normalize-space(text())!=''">
				<notes>
					<xsl:choose>
						<xsl:when test="$name='xmlbody'">
							<disp-quote>
								<xsl:apply-templates select="*|text()"/>
							</disp-quote>
						</xsl:when>
						<xsl:otherwise>
							<xsl:apply-templates select="*|text()"/>
						</xsl:otherwise>
					</xsl:choose>
				</notes>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	<xsl:template match="*[*]" mode="next">
		<xsl:if test="position()=1">
			<xsl:value-of select="name()"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="unidentified">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="back/bold[contains(text(),'ACK') or contains(text(),'Ack') ]" mode="back">
		<title>
			<xsl:value-of select="."/>
		</title>
	</xsl:template>
	<xsl:template match="back/bold" mode="back">
		<xsl:if test="contains(., 'ACK') or contains(.,'Ack')">
			<title>
				<xsl:value-of select="."/>
			</title>
		</xsl:if>
	</xsl:template>
	<xsl:template match="text/unidentified | article/unidentified">
		<xsl:choose>
			<xsl:when test="not(contains(.,'Corresp')) and not(contains(.,'Ack') or contains(.,'ACK') or contains(.,'Agradec') or contains(.,'AGRADEC')) and not(contains(.,'Refer'))">
				<xsl:apply-templates select="* | text()"/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	<!--xsl:template match="unidentified"	 mode="text">
		{{uni:<xsl:apply-templates select="*|text()" mode="text"/>}}
	</xsl:template>
	<xsl:template match="unidentified//*" mode="text">
		{{*:<xsl:apply-templates select="*|text()" mode="text"/>}}
	</xsl:template>
	<xsl:template match="unidentified//text()" mode="text">
		{{val:<xsl:value-of select="."/>}}
	</xsl:template-->
	<xsl:template match="caption/bold | caption/sub | caption/sup | subtitle/bold |  subtitle/sub | subtitle/sup | sectitle/bold | sectitle/sub | sectitle/sup |title/bold |  title/sub | title/sup | article-title/bold |  article-title/sub | article-title/sup | label/bold | label/italic | label/sub | label/sup">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="figgrps/figgrp/caption"><caption>
			<p>
				<xsl:apply-templates select="@*| * | text()"/>
			</p>
		</caption>
	</xsl:template>
	<xsl:template match="edition/italic | edition/bold | edition/sub | edition/sup "><xsl:value-of select="."/></xsl:template>
	<xsl:template match="p[normalize-space(text())='']"></xsl:template>
	
	<xsl:template name="display_date">
		<xsl:param name="dateiso"/>
		
		<xsl:if test="substring($dateiso,7,2)!='00'"><day><xsl:value-of select="substring($dateiso,7,2)"/></day></xsl:if>
		<xsl:if test="substring($dateiso,5,2)!='00'"><month><xsl:value-of select="substring($dateiso,5,2)"/></month></xsl:if>
					
		<year>
			<xsl:value-of select="substring($dateiso,1,4)"/>
		</year>
	</xsl:template>	

	<xsl:template match="sciname | caption/italic | subtitle/italic |title/italic | sectitle/italic | article-title/italic | p/italic">
		<named-content content-type="scientific-name">
			<xsl:apply-templates/>
		</named-content>
	</xsl:template>
</xsl:stylesheet>
