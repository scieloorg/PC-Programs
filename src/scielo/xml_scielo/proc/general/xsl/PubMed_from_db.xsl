<?xml version="1.0" encoding="iso-8859-1"?>
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
		<!--xsl:comment>
			<xsl:value-of select="ignore-sections/occ"/>
		</xsl:comment>
		<xsl:comment>ignored <xsl:value-of select="section_code/occ"/>
		</xsl:comment-->
	</xsl:template>
	<xsl:template match="record[class_of_record/occ='h' and not(ignore/occ='true')]">
		<!--xsl:comment>
			<xsl:value-of select="ignore-sections/occ"/>
		</xsl:comment>
		<xsl:comment>
			<xsl:value-of select="section_code/occ"/>
		</xsl:comment-->
		
		<Article>
			<Journal>
				<xsl:apply-templates select="publisher_name"/>
				<xsl:apply-templates select="article_title"/>
				<xsl:apply-templates select="issn"/>
				<xsl:apply-templates select="volume_id"/>
				<xsl:apply-templates select="issue_no"/>
				<xsl:apply-templates select="publishing_dateiso"/>
			</Journal>
			<xsl:if test=".//former_pids[occ]">
				<Replaces IdType="pii">
					<xsl:apply-templates select="." mode="pii"/>
				</Replaces>
			</xsl:if>
			<xsl:apply-templates select="title/occ" mode="title"/>
			<xsl:variable name="lang" select="article_language/occ"/>
			<xsl:if test="$lang!='en'">
				<xsl:apply-templates select="title/occ[@lang=$lang]" mode="titles"/>
			</xsl:if>
			<xsl:apply-templates select="pages"/>
			<ELocationID EIdType="pii">
				<xsl:apply-templates select="." mode="pii"/>
			</ELocationID>
			<xsl:apply-templates select="text-languages"/>
			<!-- FIXED 20040504 
			Roberta Mayumi Takenaka
			Solicitado por Solange email: 20040429
			Para artigos que não tenham autores, não gerar a tag </AuthorList>.			
			-->
			<xsl:if test="count(analytic_author/occ)&gt;0 or count(corporate_autor/occ)&gt;0">
				<AuthorList>
					<xsl:apply-templates select="analytic_author" mode="author"/>
					<xsl:apply-templates select="corporate_autor" mode="author"/>
				</AuthorList>
			</xsl:if>
			<PublicationType/>
			<ArticleIdList>
				<ArticleId IdType="pii">
					<xsl:apply-templates select="." mode="pii"/>
				</ArticleId>
				<xsl:choose>
					<xsl:when test="doi/occ">
						<ArticleId IdType="doi"><xsl:value-of select="normalize-space(.//doi/occ)"/></ArticleId>
					</xsl:when>
					<xsl:when  test="$doi_prefix and $doi_prefix!=''">
						<xsl:if test="not(contains(.//issue_no,'review'))">
							<ArticleId IdType="doi">
								<xsl:value-of select="$doi_prefix"/>/<xsl:apply-templates select="." mode="pii"/>
							</ArticleId>
						</xsl:if>
					</xsl:when>
				</xsl:choose>
			</ArticleIdList>
			<xsl:if test=".//received_dateiso[occ] or .//accepted_dateiso[occ] or .//rvpdate[occ] or .//ahpdate[occ]">
				<History>
					<xsl:apply-templates select=".//received_dateiso"/>
					<xsl:apply-templates select=".//accepted_dateiso"/>
					<xsl:if test="(.//ahpdate[occ] or .//rvpdate[occ] ) and not(contains(.//issue_no,'review')) and not(contains(.//issue_no,'ahead'))">
						<PubDate PubStatus="aheadofprint">
							<xsl:choose>
								<xsl:when test=".//rvpdate[occ]">
									<xsl:apply-templates select=".//rvpdate[occ]" mode="data"/>
								</xsl:when>
								<xsl:when test=".//ahpdate[occ]">
									<xsl:apply-templates select=".//ahpdate[occ]" mode="data"/>
								</xsl:when>
							</xsl:choose>
						</PubDate>
					</xsl:if>
				</History>
			</xsl:if>
			<xsl:apply-templates select="abstract"/>
		</Article>
	</xsl:template>
	<xsl:template match="analytic_author" mode="author-group">
	</xsl:template>
	<xsl:template match="corporate_autor" mode="author-group">
	</xsl:template>
	<xsl:template match="occ" mode="title">
		<xsl:if test="@lang = 'en'">
			<xsl:element name="ArticleTitle">
				<xsl:apply-templates select="."/>
			</xsl:element>
		</xsl:if>
	</xsl:template>
	<xsl:template match="occ" mode="titles">
		<xsl:if test="@lang != 'en'">
			<xsl:element name="VernacularTitle">
				<xsl:apply-templates select="."/>
			</xsl:element>
		</xsl:if>
	</xsl:template>
	<xsl:template match="article_language">
	       
	</xsl:template>
	<xsl:template match="text-languages">
		<xsl:apply-templates select="occ"/>
	</xsl:template>
	<xsl:template match="text-languages/occ">
		<Language><xsl:value-of select="translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/></Language>
	</xsl:template>
	<xsl:template match="record" mode="pii">
		<xsl:choose>
			<xsl:when test=".//former_pids[occ]">
				<xsl:apply-templates select=".//former_pids/occ[1]"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="publisher_item_identifier/occ"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="record" mode="piidoi">
		<xsl:choose>
			<xsl:when test=".//former_pids[occ]">
				<xsl:choose>
					<xsl:when test=".//rvpdate[occ]"/>
					<xsl:otherwise>
						<xsl:apply-templates select=".//former_pids/occ[last()]"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="publisher_item_identifier/occ"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="occ" mode="year">
		<xsl:value-of select="substring(text(),1,4)"/>
	</xsl:template>
	<xsl:template match="occ|date" mode="data">
		<xsl:param name="day"></xsl:param>
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
		<xsl:choose>
			<xsl:when test="substring(text(),7,2)!='00'"><Day><xsl:value-of select="substring(text(),7,2)"/></Day></xsl:when>
			<xsl:when test="$day!=''"><Day><xsl:value-of select="$day"/></Day></xsl:when>
			<xsl:otherwise></xsl:otherwise>
			</xsl:choose>
	</xsl:template>
	<xsl:template match="abstract">
		<Abstract>
			<xsl:apply-templates select="occ[@lang = 'en']"/>
		</Abstract>
	</xsl:template>
	<xsl:template match="publisher_name">
		<PublisherName>
			<xsl:apply-templates select="occ"/>
		</PublisherName>
	</xsl:template>
	<xsl:template match="article_title">
		<JournalTitle>
			<xsl:apply-templates select="occ"/>
		</JournalTitle>
	</xsl:template>
	<xsl:template match="issn">
		<Issn>
			<xsl:choose>
				<xsl:when test="$replaceISSN">
					<xsl:value-of select="$replaceISSN"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="occ"/>
				</xsl:otherwise>
			</xsl:choose>
		</Issn>
	</xsl:template>
	<xsl:template match="volume_id">
		<Volume>
			<xsl:apply-templates select="occ"/>
			<xsl:if test="string-length(..//supl/occ)&gt;0"> Suppl<xsl:if test="..//supl!='0'">&#160;<xsl:value-of select="..//supl/occ"/></xsl:if></xsl:if>
		</Volume>
	</xsl:template>
	<xsl:template match="issue_no">
		<Issue>
			<xsl:if test="not(contains(.,'ahead')) and not(contains(.,'review'))">
				<xsl:apply-templates select="occ"/>
				<xsl:if test="string-length(..//numsupl/occ)&gt;0"> Suppl<xsl:if test="..//numsupl!='0'">&#160;<xsl:value-of select="..//numsupl/occ"/></xsl:if>
			</xsl:if>

			</xsl:if>
		</Issue>
	</xsl:template>
	<xsl:template match="publishing_dateiso">
		<xsl:choose>
			<xsl:when test="contains(..//issue_no/occ,'review') or contains(..//issue_no/occ,'ahead')">
				<!-- significa que é um artigo ahead -->
				<PubDate PubStatus="aheadofprint">
					<xsl:choose>
						<xsl:when test="../rvpdate/occ">
							<xsl:apply-templates select="../rvpdate" mode="data"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:apply-templates select="../ahpdate" mode="data"/>
						</xsl:otherwise>
					</xsl:choose>
				</PubDate>
			</xsl:when>
			<xsl:otherwise>
				<PubDate PubStatus="ppublish">
					<xsl:variable name="year"><xsl:value-of select="substring(occ,1,4)"/></xsl:variable>
					<xsl:variable name="month"><xsl:value-of select="substring(occ,5,2)"/></xsl:variable>
					
					<xsl:if test="$year!='0000'">
						<Year><xsl:value-of select="$year"/></Year>
					</xsl:if>
					<xsl:choose>
						<xsl:when test="contains(../publishing_date/occ,$year)">
							<Month><xsl:value-of select="substring-before(../publishing_date/occ,concat('/',$year))"/></Month>
						</xsl:when>
						<xsl:when test="../publishing_date/occ">
							<Month><xsl:value-of select="../publishing_date/occ"/></Month>
						</xsl:when>
						<xsl:when test="$month!='00'">
							<Month><xsl:value-of select="$month"/></Month>
						</xsl:when>
					</xsl:choose>
				</PubDate>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="accepted_dateiso"/>
	<xsl:template match="accepted_dateiso[occ]">
		<PubDate PubStatus="accepted">
			<xsl:apply-templates select="." mode="data"><xsl:with-param name="day">01</xsl:with-param></xsl:apply-templates>
		</PubDate>
	</xsl:template>
	<xsl:template match="received_dateiso"/>
	<xsl:template match="received_dateiso[occ]">
		<PubDate PubStatus="received">
			<xsl:apply-templates select="." mode="data"><xsl:with-param name="day">01</xsl:with-param></xsl:apply-templates>
		</PubDate>
	</xsl:template>
	<xsl:template match="*[occ]" mode="data">
		<xsl:apply-templates select="occ" mode="data"/>
	</xsl:template>
	<xsl:template match="pages/occ"/>
	<xsl:template match="pages">
		<xsl:element name="FirstPage">
			<xsl:choose>
				<xsl:when test="occ/@elocation_id!=''">
					<xsl:value-of select="occ/@elocation_id"/>
				</xsl:when>
				<xsl:when test="occ/@first!='0'">
					<xsl:value-of select="occ/@first"/>
				</xsl:when>
			</xsl:choose>
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
	<xsl:template match="corporate_autor" mode="author">
		<xsl:apply-templates select="occ" mode="author"/>
	</xsl:template>
	<xsl:template match="analytic_author/occ" mode="author">
		<xsl:choose>
			<xsl:when test="@name">
				<Author>
					<xsl:apply-templates select="@name"/>
					<xsl:apply-templates select="@last_name"/>
					<xsl:apply-templates select="@suffix"/>
					<xsl:apply-templates select="@affiliation_code"/>
					<xsl:if test="not(@affiliation_code)">
						<xsl:apply-templates select="ancestor::record/affiliation/occ"/>
					</xsl:if>
				</Author>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="*" mode="author"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="occ/Author " mode="author">
		<xsl:copy>
			<xsl:apply-templates select="*|text()"/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="occ/Author/aff-id" mode="author">
		<xsl:apply-templates select="."/>
	</xsl:template>
	<xsl:template match="corporate_autor/occ" mode="author">
		<Author>
			<CollectiveName>
				<xsl:if test="@d">
					<xsl:apply-templates select="@d"/>, </xsl:if>
				<xsl:apply-templates select="text()"/>
			</CollectiveName>
		</Author>
	</xsl:template>
	<xsl:template match="@name | FirstName ">
		<FirstName>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</FirstName>
	</xsl:template>
	<xsl:template match="@last_name | LastName">
		<LastName>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</LastName>
	</xsl:template>
	<xsl:template match="@suffix | Suffix">
		<Suffix>
			<xsl:apply-templates select="occ"/>
		</Suffix>
	</xsl:template>
	<xsl:template match="@affiliation_code | aff-id ">
		<xsl:variable name="code">
		<xsl:choose>
			<xsl:when test="contains(.,' ')"><xsl:value-of select="substring-before(.,' ')"></xsl:value-of></xsl:when>
			<xsl:otherwise><xsl:value-of select="."></xsl:value-of></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<Affiliation>
			<xsl:apply-templates select="ancestor::record/affiliation/occ[@code = $code]"/>
		</Affiliation>
	</xsl:template>
	<!--xsl:template match="affiliation/occ">
		<xsl:variable name="b" select="//xml_scielo/record/affiliation/occ"/>
		<xsl:choose>
			<xsl:when test="@city">
				<xsl:apply-templates select="@s3" mode="place"/>
				<xsl:if test="@s3 !=''">, </xsl:if>
				<xsl:apply-templates select="@departament" mode="place"/>
				<xsl:if test="@departament!=''">, </xsl:if>
				<xsl:apply-templates select="@institute" mode="place"/>
				<xsl:if test="@institute != ''">, </xsl:if>
				<xsl:value-of select="." disable-output-escaping="yes"/>
				<xsl:if test=" normalize-space(text()) != '' ">, </xsl:if>
				<xsl:apply-templates select="@city" mode="place1"/>
				<xsl:if test="@city !=''">, </xsl:if>
				<xsl:apply-templates select="@state" mode="place1"/>
				<xsl:if test="@state != ''">, </xsl:if>
				<xsl:apply-templates select="@z" mode="place1"/>
				<xsl:if test="@z != ''">, </xsl:if>
				<xsl:apply-templates select="@country" mode="place1"/>				
				<xsl:if test="@e != ''">, </xsl:if>
				<xsl:apply-templates select="@e"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="@s3"/>
				<xsl:if test="@s3 !=''">, </xsl:if>
				<xsl:apply-templates select="@departament" mode="place"/>
				<xsl:if test="@departament!=''">, </xsl:if>
				<xsl:apply-templates select="@institute" mode="place"/>
				<xsl:if test="@institute != ''">, </xsl:if>
				<xsl:value-of select="." disable-output-escaping="yes"/>
				<xsl:variable name="var" select="@institute"/>
				<xsl:apply-templates select="$b[@institute = $var]/@city" mode="ttt1"/>
				<xsl:apply-templates select="$b[@institute = $var]/@state" mode="ttt2"/>
				<xsl:apply-templates select="$b[@institute = $var]/@z" mode="ttt3"/>
				<xsl:apply-templates select="$b[@institute = $var]/@country" mode="ttt4"/>
				<xsl:if test="$b[@institute = $var]/@e != ''">, </xsl:if>
				<xsl:apply-templates select="$b[@institute = $var]/@e"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="@city" mode="ttt1">
		<xsl:if test="normalize-space(.)">, </xsl:if>
		<xsl:value-of select="." disable-output-escaping="yes"/>, 
	</xsl:template>
	<xsl:template match="@state" mode="ttt2">
		<xsl:value-of select="."/>, 
	</xsl:template>
	<xsl:template match="@z" mode="ttt3">
		<xsl:value-of select="."/>,
	</xsl:template>
	<xsl:template match="@country" mode="ttt4">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="@e">
		<xsl:value-of select="." disable-output-escaping="yes"/>
	</xsl:template>
	<xsl:template match="@*" mode="place">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="@*" mode="place1">
		<xsl:value-of select="." disable-output-escaping="yes"/>
	</xsl:template-->
	<xsl:template match="affiliation/occ">
		<xsl:variable name="others" select="//xml_scielo/record/affiliation/occ"/>
		<xsl:variable name="aff" select="normalize-space(institution)"/>
		<xsl:choose>
			<xsl:when test="institution or address or e-mail">
				<xsl:value-of select="institution" disable-output-escaping="yes"/>, <xsl:value-of select="address" disable-output-escaping="yes"/>
				<xsl:if test="not(address)">
					<xsl:apply-templates select="$others[normalize-space(institution)=$aff]" mode="address"/>
				</xsl:if>
				<xsl:if test="e-mail">, <xsl:value-of select="e-mail/text()"/>
				</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="@s3"/>
				<xsl:apply-templates select="@departament"/>
				<xsl:apply-templates select="@institute"/>
				<xsl:value-of select="." disable-output-escaping="yes"/>
				<xsl:if test=" normalize-space(text()) != '' ">,&#160;</xsl:if>
				<xsl:choose>
					<xsl:when test="@city">
						<xsl:apply-templates select="." mode="address"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates select="$others[normalize-space(.)=$aff]" mode="address"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="affiliation/occ/@*">
		<xsl:if test="normalize-space(.)!=''">
			<xsl:value-of select="."/>,&#160;
		</xsl:if>
	</xsl:template>
	<xsl:template match="affiliation/occ" mode="address">
		<xsl:choose>
			<xsl:when test="address">
				<xsl:value-of select="address" disable-output-escaping="yes"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="@city" mode="address">
					<xsl:with-param name="insertComma" select="normalize-space(concat(@state,@z,@e))"/>
				</xsl:apply-templates>
				<xsl:apply-templates select="@state" mode="address">
					<xsl:with-param name="insertComma" select="normalize-space(concat(@z,@e))"/>
				</xsl:apply-templates>
				<xsl:apply-templates select="@z" mode="address">
					<xsl:with-param name="insertComma" select="normalize-space(@e)"/>
				</xsl:apply-templates>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="affiliation/occ/@*" mode="address">
		<xsl:param name="insertComma"/>
		<xsl:comment>
			<xsl:value-of select="name()"/>
		</xsl:comment>
		<xsl:if test="normalize-space(.)!=''">
			<xsl:value-of select="."/>
			<xsl:if test="string-length($insertComma)&gt;0">,&#160;</xsl:if>
		</xsl:if>
	</xsl:template>
	<xsl:template match="@*" mode="x">
		<xsl:value-of select="." disable-output-escaping="yes"/>
		<xsl:value-of select="." disable-output-escaping="no"/>
		<xsl:value-of select="concat('&lt;![CDATA[',.,']]>')" disable-output-escaping="yes"/>
	</xsl:template>
</xsl:stylesheet>
