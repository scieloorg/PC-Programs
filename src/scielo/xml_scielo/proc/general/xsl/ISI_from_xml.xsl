<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="reg" mode="scielo-xml-scielo-xml">
		<xsl:apply-templates select="document(xml-filename)/article" mode="scielo-xml-scielo-xml">
			<xsl:with-param name="other" select="other"/>
		</xsl:apply-templates>

	</xsl:template>
	<xsl:template match="article-title/xref"></xsl:template>
	
	<xsl:template match="article" mode="scielo-xml-scielo-xml">
		<xsl:param name="other"/>
		<xsl:if test=".//article-meta//article-title and .//article-meta//contrib">
			<Article>
				<PublisherId>SciELO</PublisherId>
				<ArticleId>
					<xsl:apply-templates select="$other" mode="scielo-xml-pii"/>
				</ArticleId>
				<Journal>

					<xsl:apply-templates select="." mode="scielo-xml-publisher_name"/>
					<xsl:apply-templates select="." mode="scielo-xml-journal_title"/>
					<xsl:apply-templates select="." mode="scielo-xml-issn"/>
					<xsl:apply-templates select="." mode="scielo-xml-volume_id"/>
					<xsl:apply-templates select="." mode="scielo-xml-issue_no"/>
					<xsl:apply-templates select="." mode="scielo-xml-publishing_dateiso"/>
				</Journal>
				<xsl:apply-templates select="." mode="scielo-xml-title"/>
				<xsl:apply-templates select=".//front//fpage|.//front//lpage"/>

				<AuthorList>
					<xsl:apply-templates select=".//front//contrib" mode="scielo-xml-author"/>

				</AuthorList>

				<xsl:if test="count(.//ref)&gt;0">
					<ReferenceList>
						<xsl:apply-templates
							select=".//ref[.//element-citation/@publication-type='journal']"><xsl:with-param name="pid" select="$other/pid"></xsl:with-param></xsl:apply-templates>
					</ReferenceList>
				</xsl:if>
			</Article>
		</xsl:if>
	</xsl:template>
	<xsl:template match="ref">
		<xsl:param name="pid"/>
		<xsl:variable name="temp">00000<xsl:value-of select="substring(@id,2)"/></xsl:variable>
		<xsl:variable name="order">
			<xsl:value-of select="substring($temp,string-length($temp)-4)"/>
		</xsl:variable>
		<xsl:variable name="ref_pid">
			<xsl:value-of select="$pid"/>
			<xsl:value-of select="$order"/>
		</xsl:variable>


		<xsl:if
			test="count(.//name)&gt;0 and .//source and .//year and .//volume and .//fpage and string-length($ref_pid)=28">
			<Reference>
				<ReferenceJournal>
					<xsl:value-of select=".//source" disable-output-escaping="no"/>
				</ReferenceJournal>
				<ReferenceYear>
					<xsl:value-of select=".//year"/>
				</ReferenceYear>
				<ReferenceVolume>
					<xsl:value-of select=".//volume"/>
				</ReferenceVolume>
				<ReferenceFirstPage>
					<xsl:value-of select=".//fpage"/>
				</ReferenceFirstPage>
				<ReferenceAuthor>
					<AuthorList>
						<xsl:apply-templates select=".//name" mode="scielo-xml-author"/>
					</AuthorList>
				</ReferenceAuthor>
				<ReferenceId>
					<xsl:value-of select="$ref_pid"/>
				</ReferenceId>
			</Reference>
		</xsl:if>
	</xsl:template>

	<xsl:template match="article" mode="scielo-xml-title">
		<xsl:element name="ArticleTitle">
			<xsl:apply-templates select=".//front//article-title[@xml:lang='en']"/>
			<xsl:apply-templates select=".//front//trans-title[@xml:lang='en']"/>
			<xsl:apply-templates
				select=".//sub-article[@article-type='translation']//front-stub//article-title[@xml:lang='en']"/>

		</xsl:element>
	</xsl:template>


	<!-- OK -->
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
			<xsl:value-of select=".//journal-meta/issn[1]"/>
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
		<xsl:apply-templates select=".//front//pub-date[1]"/>
	</xsl:template>
	<xsl:template match="pub-date/@pub-type | @date-type">
		<xsl:choose>
			<xsl:when test=".='epub'">aheadofprint</xsl:when>
			<xsl:when test=".='ppub'">ppublish</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="pub-date|date[@date-type='rev-recd']"> </xsl:template>
	<xsl:template match="pub-date|date[@date-type!='rev-recd']">
		<PubDate>
			
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
	<xsl:template match="other" mode="scielo-xml-pii">
		<xsl:apply-templates select="former-pid"/>
		<xsl:if test="not(former-pid)">
			<xsl:value-of select="pid"/>
		</xsl:if>
	</xsl:template>

	<xsl:template match="contrib" mode="scielo-xml-author">

		<Author>
			<xsl:apply-templates select="name"/>
			<!--xsl:if test="not(@affiliation_code)">
						<xsl:apply-templates select="ancestor::record/affiliation/occ"/>
					</xsl:if-->
		</Author>

	</xsl:template>
	<xsl:template match="name" mode="scielo-xml-author">
		
		<Author>
			<xsl:apply-templates select="."/>
			<!--xsl:if test="not(@affiliation_code)">
						<xsl:apply-templates select="ancestor::record/affiliation/occ"/>
					</xsl:if-->
		</Author>
		
	</xsl:template>


	<xsl:template match="name">
		<xsl:apply-templates select="given-names"/>
		<xsl:apply-templates select="surname"/>
		<xsl:apply-templates select="suffix"/>
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

</xsl:stylesheet>
