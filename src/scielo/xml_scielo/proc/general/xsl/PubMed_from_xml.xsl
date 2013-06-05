<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="reg" mode="scielo-xml-scielo-xml">
		<xsl:apply-templates select="document(xml-filename)/article" mode="scielo-xml-scielo-xml">
			<xsl:with-param name="other" select="other"/>
		</xsl:apply-templates>

	</xsl:template>

	<xsl:template match="article" mode="scielo-xml-scielo-xml">
		<xsl:param name="other"/>
		<Article>
			<Journal>
				<xsl:apply-templates select="." mode="scielo-xml-publisher_name"/>
				<xsl:apply-templates select="." mode="scielo-xml-journal_title"/>
				<xsl:apply-templates select="." mode="scielo-xml-issn"/>
				<xsl:apply-templates select="." mode="scielo-xml-volume_id"/>
				<xsl:apply-templates select="." mode="scielo-xml-issue_no"/>
				<xsl:apply-templates select="." mode="scielo-xml-publishing_dateiso"/>
			</Journal>
			<xsl:if test="$other/former_pid">
				<Replaces IdType="pii">
					<xsl:apply-templates select="$other" mode="scielo-xml-pii"/>
				</Replaces>
			</xsl:if>
			<xsl:apply-templates select="." mode="scielo-xml-title"/>

			<xsl:apply-templates select="fpage|lpage"/>
			<ELocationID EIdType="pii">
				<xsl:apply-templates select="$other" mode="scielo-xml-pii"/>
			</ELocationID>
			<xsl:apply-templates
				select="@xml:lang|.//sub-article[@article-type='translation']/@xml:lang"
				mode="scielo-xml-languages"/>
			<!-- FIXED 20040504 
			Roberta Mayumi Takenaka
			Solicitado por Solange email: 20040429
			Para artigos que não tenham autores, não gerar a tag </AuthorList>.			
			-->
			<xsl:if test="count(.//front//contrib) + count(.//front//collab) &gt; 0">
				<AuthorList>
					<xsl:apply-templates select=".//front//contrib" mode="scielo-xml-author"/>
					<xsl:apply-templates select=".//front//collab" mode="scielo-xml-author"/>
				</AuthorList>
			</xsl:if>
			<PublicationType/>
			<ArticleIdList>
				<ArticleId IdType="pii">
					<xsl:apply-templates select="$other" mode="scielo-xml-pii"/>
				</ArticleId>
				<ArticleId IdType="doi">
							<xsl:value-of select=".//front//article-id[@pub-id-type='doi']"/>
						</ArticleId>
					
			</ArticleIdList>
			<xsl:if
				test=".//front//history">
				<History>
					<xsl:apply-templates select=".//front//history/*"/>
					<xsl:apply-templates select=".//front//pub-date[@pub-type='epub']"></xsl:apply-templates>
				</History>
			</xsl:if>
			<xsl:apply-templates select="." mode="scielo-xml-abstract"/>
		</Article>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-title">
		<xsl:choose>
			<xsl:when test="@xml:lang = 'en'">
				<xsl:element name="ArticleTitle">
					<xsl:apply-templates select=".//article-meta//title-group//article-title"/>
				</xsl:element>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="VernacularTitle">
					<xsl:apply-templates select=".//article-meta//title-group//article-title"/>
				</xsl:element>
			</xsl:otherwise>

		</xsl:choose>
	</xsl:template>

	<xsl:template match="@xml:lang" mode="scielo-xml-languages">
		<Language>
			<xsl:value-of select="."/>
		</Language>
	</xsl:template>


	<xsl:template match="*" mode="scielo-xml-abstract">
		<Abstract>
			<xsl:apply-templates select=".//*[contains(name(),'abstract') and @xml:lang='en']" mode="scielo-xml-content-abstract"/>
		</Abstract>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-content-abstract">
		<xsl:apply-templates select="*|text()" mode="scielo-xml-content-abstract"/>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-publisher_name">
		<PublisherName>
			<xsl:value-of select=".//journal-meta//publisher-name"/>
		</PublisherName>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-journal_title">
		<JournalTitle>
			<xsl:apply-templates select=".//journal-meta/journal-id[@journal-id-type='nlm-ta']"/>
		</JournalTitle>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-issn">
		<Issn>
			<xsl:choose>
				<xsl:when test="$replaceISSN">
					<xsl:value-of select="$replaceISSN"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select=".//journal-meta/issn[1]"/>
				</xsl:otherwise>
			</xsl:choose>
		</Issn>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-volume_id">
		<Volume>
			<xsl:apply-templates select=".//front//volume"/>
			<xsl:if test="substring(.//front//issue,1,5)='Suppl'">
				<xsl:value-of select=".//front//issue"/>
			</xsl:if>
		</Volume>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-issue_no">
		<Issue>
			<xsl:if test=".//front//issue!='00'">
				<xsl:value-of select=".//front//issue"/>

			</xsl:if>
		</Issue>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-publishing_dateiso">
		<xsl:choose>
			<xsl:when test=".//front//pub-date[@date-type='ppub']">
				<xsl:apply-templates select=".//front//pub-date[@date-type='ppub']"/>
			</xsl:when>
			<xsl:when test=".//front//pub-date[@date-type='epub-ppub']">
				<xsl:apply-templates select=".//front//pub-date[@date-type='epub-ppub']"/>
			</xsl:when>
			<xsl:when test=".//front//pub-date[@date-type='epub']">
				<xsl:apply-templates select=".//front//pub-date[@date-type='epub']"/>
			</xsl:when>
			<xsl:otherwise><xsl:apply-templates select=".//front//pub-date[1]"/></xsl:otherwise>
		</xsl:choose>
		
	</xsl:template>
	<xsl:template match="pub-date/@pub-type | @date-type" >
		<xsl:choose>
			<xsl:when test=".='epub'">aheadofprint</xsl:when>
			<xsl:when test=".='ppub'">ppublish</xsl:when>
			<xsl:when test=".='epub-ppub'">ppublish</xsl:when>
			<xsl:when test=".='collection'">ppublish</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="pub-date|date[@date-type='rev-recd']">
	</xsl:template>
	<xsl:template match="pub-date|date[@date-type!='rev-recd']">
		<PubDate>
			<xsl:attribute name="PubStatus">
				<xsl:apply-templates select="@*"/>
			</xsl:attribute>
			<xsl:apply-templates select="year"/>
			<xsl:apply-templates select="month"/>
			<xsl:apply-templates select="day"/>
		</PubDate>
	</xsl:template>
	<xsl:template match="month">
		<Month>
			<xsl:value-of select="."/>
		</Month>
	</xsl:template>
	<xsl:template match="year">
		<Year>
			<xsl:value-of select="."/>
		</Year>
	</xsl:template>
	<xsl:template match="day">
		<Day>
			<xsl:value-of select="."/>
		</Day>
	</xsl:template>

	<xsl:template match="fpage">
		<xsl:element name="FirstPage">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>

	<xsl:template match="lpage">
		<xsl:element name="LastPage">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>

	<xsl:template match="contrib" mode="scielo-xml-author">

		<Author>
			<xsl:apply-templates select="name|xref[@ref-type='aff'][1]"/>
			<!--xsl:if test="not(@affiliation_code)">
						<xsl:apply-templates select="ancestor::record/affiliation/occ"/>
					</xsl:if-->
		</Author>

	</xsl:template>
	<xsl:template match="article-title/text()"><xsl:value-of select="."></xsl:value-of></xsl:template>
	<xsl:template match="article-title/*"><xsl:value-of select="."></xsl:value-of></xsl:template>
	<xsl:template match="article-title/xref"></xsl:template>
	<xsl:template match="collab" mode="scielo-xml-author">
		<Author>
			<CollectiveName>
				<xsl:value-of select="."/>
			</CollectiveName>
		</Author>
	</xsl:template>
	<xsl:template match="name">
		<xsl:apply-templates select="given-names"></xsl:apply-templates>
		<xsl:apply-templates select="surname"></xsl:apply-templates>
		<xsl:apply-templates select="suffix"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="given-names | FirstName ">
		<FirstName>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</FirstName>
	</xsl:template>
	<xsl:template match="surname | LastName">
		<LastName>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</LastName>
	</xsl:template>
	<xsl:template match="suffix | Suffix">
		<Suffix>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</Suffix>
	</xsl:template>
	<xsl:template match="prefix ">
		<Prefix>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</Prefix>
	</xsl:template>
	<xsl:template match="xref[@ref-type='aff']  | aff-id ">
		<xsl:variable name="code" select="@rid"/>
		<Affiliation>
			<xsl:apply-templates select="../../..//aff[@id = $code]" mode="scielo-xml-text"/>
		</Affiliation>
	</xsl:template>

	
	<xsl:template match="aff" mode="scielo-xml-text">
		<xsl:apply-templates select="*[name()!='label']" mode="scielo-xml-text"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="aff//*" mode="scielo-xml-text"><xsl:if test="position()!=1">, </xsl:if><xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="aff//label" mode="scielo-xml-text"></xsl:template>
	<xsl:template match="aff//text()" mode="scielo-xml-text"><xsl:if test="normalize-space(.)=','"></xsl:if></xsl:template>
	<xsl:template match="@*" mode="scielo-xml-x">
		<xsl:value-of select="." disable-output-escaping="yes"/>
		<xsl:value-of select="." disable-output-escaping="no"/>
		<xsl:value-of select="concat('&lt;![CDATA[',.,']]&gt;')" disable-output-escaping="yes"/>
	</xsl:template>

	<xsl:template match="other" mode="scielo-xml-pii">
		<xsl:apply-templates select="former-pid"/>
		<xsl:if test="not(former-pid)">
			<xsl:value-of select="pid"/>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
