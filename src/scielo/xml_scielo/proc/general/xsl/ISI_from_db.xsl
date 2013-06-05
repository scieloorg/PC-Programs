<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
	<xsl:template match="occ">
		<!--xsl:comment>occ</xsl:comment-->
		<xsl:apply-templates select="text()"/>
	</xsl:template>
	<xsl:template match="@*">
		<!--xsl:comment>@*</xsl:comment-->
		<xsl:value-of select=". "/>
	</xsl:template>
	<xsl:template match="text()">
		<!--xsl:comment>text()</xsl:comment-->
		<xsl:value-of select="normalize-space(.)" disable-output-escaping="yes"/>
	</xsl:template>
	<!--xsl:template match="@*|text()">
		<xsl:comment>normal <xsl:value-of select="."/></xsl:comment>
		<xsl:comment>disable-output-scaping <xsl:value-of select="." disable-output-escaping="yes"/></xsl:comment>
	
		<xsl:variable name="text">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:variable>
		
		<xsl:choose>
			<xsl:when test="contains($text,'amp;#')">
				<xsl:comment>contains - nao faz nada</xsl:comment>
				<xsl:value-of select="$text"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:comment>not contains - disable-output-escaping</xsl:comment>
				<xsl:value-of select="$text" disable-output-escaping="yes"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="abstract/occ">
		<xsl:value-of select="." disable-output-escaping="yes"/>
	</xsl:template-->
	
	<xsl:template match="record[class_of_record/occ='h']">
		<xsl:variable name="id">
			<xsl:value-of select="publisher_id/occ"/>
		</xsl:variable>
		<xsl:if test="count(title/occ)&gt;0 and count(analytic_author/occ)&gt;0">
		<Article>
			<PublisherId>SciELO</PublisherId>
			<ArticleId>
				<xsl:apply-templates select="." mode="pii"/>
			</ArticleId>
			<Journal>
				<xsl:apply-templates select="publisher_name"/>
				<xsl:apply-templates select="../xml_scielo_title/journal-title"/>
				<xsl:apply-templates select="issn"/>
				<xsl:apply-templates select="volume_id"/>
				<xsl:apply-templates select="issue_no"/>
				<xsl:apply-templates select="publishing_dateiso"/>
			</Journal>
			<xsl:apply-templates select="title" mode="title"/>
			<xsl:apply-templates select="pages"/>
			<xsl:if test="count(analytic_author/occ)&gt;0 ">
				<AuthorList>
					<xsl:apply-templates select="analytic_author" mode="author"/>
				</AuthorList>
			</xsl:if>
			<xsl:variable name="test"><xsl:apply-templates select="..//record[class_of_record/occ='c' and publisher_id/occ=$id]"/></xsl:variable>
			<xsl:if test="string-length(normalize-space($test))&gt;0">			
				<ReferenceList>
					<xsl:apply-templates select="..//record[class_of_record/occ='c' and publisher_id/occ=$id]"/>
				</ReferenceList>
			</xsl:if>
		</Article></xsl:if>
	</xsl:template>
	<xsl:template match="record[class_of_record/occ='c']"/>
	<xsl:template match="record[class_of_record/occ='c' and string-length(normalize-space(article_title/occ))&gt;0]">
		<xsl:if test="count(analytic_author/occ)&gt;0 and article_title and publishing_dateiso and volume_id and pages/occ/@first">
			<Reference>
				<ReferenceJournal>
					<xsl:value-of select="article_title/occ" disable-output-escaping="yes"/>
				</ReferenceJournal>
				<xsl:if test="publishing_dateiso">
					<ReferenceYear>
						<xsl:value-of select="substring(normalize-space(publishing_dateiso),1,4)"/>
					</ReferenceYear>
				</xsl:if>
				<ReferenceVolume>
					<xsl:value-of select="volume_id/occ"/>
				</ReferenceVolume>
				<ReferenceFirstPage>
					<xsl:value-of select="pages/occ/@first"/>
				</ReferenceFirstPage>
				<xsl:if test="count(analytic_author/occ)&gt;0 ">
					<ReferenceAuthor>
						<AuthorList>
							<xsl:apply-templates select="analytic_author" mode="author"/>
						</AuthorList>
					</ReferenceAuthor>
				</xsl:if>
				<ReferenceId>
					<xsl:value-of select="publisher_item_identifier/occ"/>
				</ReferenceId>
			</Reference>
		</xsl:if>
	</xsl:template>
	<xsl:template match="record" mode="pii">
		<xsl:value-of select="publisher_item_identifier/occ"/>
	</xsl:template>
	<xsl:template match="title" mode="title">
		<xsl:element name="ArticleTitle">
			<xsl:apply-templates select="occ[@lang = 'en']"/>
			<xsl:if test="not (occ[@lang = 'en'])">
				<xsl:apply-templates select="occ[1]"/>
			</xsl:if>
		</xsl:element>
	</xsl:template>
	<xsl:template match="pages/occ"/>
	<xsl:template match="pages">
		<xsl:element name="FirstPage">
			<xsl:if test="occ/@first!='0'">
				<xsl:value-of select="occ/@first"/>
			</xsl:if>
		</xsl:element>
		<xsl:element name="LastPage">
			<xsl:if test="occ/@last!='0'">
				<xsl:value-of select="occ/@last"/>
			</xsl:if>
		</xsl:element>
	</xsl:template>
	<xsl:template match="analytic_author" mode="author">
		<xsl:apply-templates select="occ" mode="author"/>
	</xsl:template>
	<xsl:template match="analytic_author/occ" mode="author">
		<xsl:choose>
			<xsl:when test="@name">
				<Author>
				
					<FirstName>
					<xsl:value-of select="@name" disable-output-escaping="yes"/>
					</FirstName>
					<xsl:apply-templates select="@last_name"/>
					<xsl:apply-templates select="@suffix"/>
					<!--xsl:apply-templates select="@affiliation_code"/>
					<xsl:if test="not(@affiliation_code) and ancestor::record/affiliation/occ">
						<Affiliation>
							<xsl:apply-templates select="ancestor::record/affiliation/occ"/>
						</Affiliation>
					</xsl:if-->
				</Author>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="*" mode="author"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="occ//*[text()]" mode="author">
		<xsl:copy-of select="."/>
	</xsl:template>
	<xsl:template match="occ/*[*]" mode="author">
		<xsl:copy>
			<xsl:apply-templates select="*" mode="author"/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="occ//aff-id" mode="author">
		
	
	</xsl:template>
	<xsl:template match="@suffix">
		<Suffix>
			<xsl:apply-templates select="occ"/>
		</Suffix>
	</xsl:template>
	<xsl:template match="occ" mode="year">
		<xsl:value-of select="substring(text(),1,4)"/>
	</xsl:template>
	<xsl:template match="occ|date" mode="data">
		<xsl:if test="substring(text(),1,4)!='0000'">
			<Year>
				<xsl:value-of select="substring(text(),1,4)"/>
			</Year>
		</xsl:if>
		<xsl:if test="substring(text(),5,2)!='00'">
			<Month>
				<xsl:value-of select="substring(text(),5,2)"/>
			</Month>
		</xsl:if>
		<xsl:if test="substring(text(),7,2)!='00'">
			<Day>
				<xsl:value-of select="substring(text(),7,2)"/>
			</Day>
		</xsl:if>
	</xsl:template>
	<xsl:template match="publisher_name">
		<PublisherName>
			<xsl:apply-templates select="occ"/>
		</PublisherName>
	</xsl:template>
	<xsl:template match="article_title | journal-title">
		<JournalTitle>
			<xsl:apply-templates select="*"/>
		</JournalTitle>
	</xsl:template>
	<xsl:template match="issn">
		<Issn>
			<xsl:apply-templates select="occ"/>
		</Issn>
	</xsl:template>
	<xsl:template match="volume_id">
		<Volume>
			<xsl:apply-templates select="occ"/>
		</Volume>
	</xsl:template>
	<xsl:template match="issue_no">
		<Issue>
			<xsl:if test="not(contains(.,'ahead'))">
				<xsl:apply-templates select="occ"/>
				<xsl:if test="string-length(.//supl/occ)&gt;0">suppl.<xsl:if test="..//supl!='0'">&#160;
						<xsl:value-of select="..//supl"/>
					</xsl:if>
				</xsl:if>
			</xsl:if>
		</Issue>
	</xsl:template>
	<xsl:template match="publishing_dateiso">
		<PubDate>
			<xsl:apply-templates select="." mode="data"/>
		</PubDate>
	</xsl:template>
	<xsl:template match="*[occ]" mode="data">
		<xsl:apply-templates select="occ" mode="data"/>
	</xsl:template>
	<xsl:template match="@name">
		<xsl:value-of select="." disable-output-escaping="yes"/>
	</xsl:template>
	<xsl:template match="@last_name">
		<LastName>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</LastName>
	</xsl:template>
<xsl:template match="Author | Author/*" mode="author">
		<xsl:copy>
			<xsl:apply-templates mode="author" />
		</xsl:copy>
	</xsl:template>
	<xsl:template match="Author//aff-id" mode="author">
	</xsl:template>
	<xsl:template match="Author/*/text()" mode="author">
		<xsl:value-of select="normalize-space(.)" disable-output-escaping="yes"/>
	</xsl:template>
	</xsl:stylesheet>
