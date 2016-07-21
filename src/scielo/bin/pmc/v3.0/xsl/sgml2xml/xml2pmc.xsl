<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"
	xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl xlink mml">

	<xsl:include href="local_dtd.xsl"/>

	<xsl:param name="new_name"/>
	<xsl:variable name="translations" select=".//sub-article[@article-type='translation']"/>
	<xsl:variable name="display_funding">
		<xsl:choose>
			<!--
		Verifica se a seção Agradecimentos contém o número do projeto do funding group
		Se contém, funding-group deve ser excluído
		-->
			<xsl:when test="not(//ack)">yes</xsl:when>
			<xsl:when test=".//ack and contains(.//ack//p, .//funding-group//award-id)"
				>no</xsl:when>
			<xsl:otherwise>yes</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<xsl:variable name="xml_type">
		<xsl:choose>
			<xsl:when test=".//mixed-citation and .//element-citation">scielo</xsl:when>
			<xsl:otherwise>pmc</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>


	<xsl:template match="*">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@* | * | text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}">
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="@article-type">
		<xsl:attribute name="{name()}">
			<xsl:choose>
				<xsl:when test=".='clinical-trial'">research-article</xsl:when>
				<xsl:when test=".='editorial-material'">editorial</xsl:when>
				<xsl:when test=".='technical-report'">research-article</xsl:when>
				<xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	
	<xsl:template match="sub-article[@article-type='translation']">
	</xsl:template>
	
	<!-- KWD-GROUP - begin -->
	<xsl:template match="article//article-meta/kwd-group">
	</xsl:template>
	
	<xsl:template match="article//article-meta/kwd-group[1]">
		<xsl:apply-templates select="..//kwd-group[@xml:lang='en']" mode="copy"/>
		<xsl:apply-templates select="$translations[@xml:lang='en']" mode="kwd-group"/>
		<xsl:apply-templates select="..//kwd-group[@xml:lang!='en']" mode="copy"/>
		<xsl:apply-templates select="$translations[@xml:lang!='en']" mode="kwd-group"/>
	</xsl:template>
	
	<xsl:template match="kwd-group" mode="copy">
		<xsl:copy-of select="."/>
	</xsl:template>
	
	<xsl:template match="sub-article[@article-type='translation']" mode="kwd-group">
		<kwd-group>
			<xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
			<xsl:apply-templates select=".//kwd-group//*"/>
		</kwd-group>
	</xsl:template>
	
	<!-- KWD-GROUP - end -->
	
	<!-- TITLE-GROUP - begin -->
	<xsl:template match="article[@xml:lang='en']//article-meta/title-group">
		<title-group>
			<xsl:apply-templates select="@*|*|text()"/>
			<xsl:apply-templates select="$translations[@xml:lang!='en']" mode="trans-title-group"/>
		</title-group>
	</xsl:template>
	
	<xsl:template match="article[@xml:lang!='en']//article-meta/title-group">
		<title-group>
			<xsl:apply-templates select="trans-title-group[@xml:lang='en']" mode="article-title"/>
			<xsl:apply-templates select="$translations[@xml:lang='en']//article-title"/>
			<trans-title-group>
				<xsl:attribute name="xml:lang"><xsl:value-of select="../../../@xml:lang"/></xsl:attribute>
				<xsl:apply-templates select="article-title" mode="trans-title"/>
			</trans-title-group>
			<xsl:apply-templates select="trans-title-group[@xml:lang!='en']"/>
			<xsl:apply-templates select="$translations[@xml:lang!='en']" mode="trans-title-group"/>
		</title-group>
	</xsl:template>
	
	<xsl:template match="sub-article[@article-type='translation' and @xml:lang!='en']" mode="trans-title-group">
		<trans-title-group>
			<xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
			<xsl:apply-templates select=".//article-title" mode="trans-title"/>
		</trans-title-group>
	</xsl:template>
	
	<xsl:template match="trans-title-group" mode="article-title">
		<article-title>
			<xsl:apply-templates select="*|text()" mode="article-title"/>
		</article-title>
	</xsl:template>
	
	<xsl:template match="trans-title" mode="article-title">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	
	<xsl:template match="article-title"  mode="trans-title">
		<trans-title>
			<xsl:apply-templates select="*|text()"/>
		</trans-title>
	</xsl:template>
	<!-- TITLE-GROUP - END -->
	
	<!-- ABSTRACT - begin -->
	<xsl:template match="article[@xml:lang='en']//abstract">
		<xsl:apply-templates select="." mode="abstract"/>
		<xsl:apply-templates select="$translations[@xml:lang!='en']" mode="trans-abstract"/>
	</xsl:template>
	
	<xsl:template match="article[@xml:lang='en']//abstract | trans-abstract" mode="abstract">
		<abstract>
			<xsl:apply-templates select="*|text()"/>
		</abstract>
	</xsl:template>
	
	<xsl:template match="sub-article[@article-type='translation' and @xml:lang!='en']" mode="trans-abstract">
		<trans-abstract>
			<xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
			<xsl:apply-templates select=".//front-stub/abstract" mode="trans-abstract"/>
		</trans-abstract>
	</xsl:template>
	
	<xsl:template match="abstract" mode="trans-abstract">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	
	<xsl:template match="article[@xml:lang!='en']/@xml:lang">
		<xsl:attribute name="{name()}">en</xsl:attribute>
	</xsl:template>
	
	<xsl:template match="article[@xml:lang!='en']//article-meta//abstract">
		<xsl:apply-templates select="..//trans-abstract[@xml:lang='en']" mode="abstract"/>
		<xsl:apply-templates select="$translations[@xml:lang='en']//abstract"/>
		<trans-abstract>
			<xsl:attribute name="xml:lang"><xsl:value-of select="../../../@xml:lang"/></xsl:attribute>
			<xsl:apply-templates select="*|text()"/>
		</trans-abstract>
		<xsl:apply-templates select="$translations[@xml:lang!='en']" mode="trans-abstract"/>
	</xsl:template>
	
	<xsl:template match="article[@xml:lang!='en']//article-meta//trans-abstract[@xml:lang='en']">
	</xsl:template>
	<!-- ABSTRACT - END -->
	
	<!-- BODY - begin -->
	<xsl:template match="article[@xml:lang!='en']/body">
		<xsl:apply-templates select="$translations[@xml:lang='en']/body"/>
	</xsl:template>
	<xsl:template match="article[@xml:lang!='en']/back">
		<back>
		<xsl:apply-templates select="$translations[@xml:lang='en']/back/ack"/>
		<xsl:apply-templates select="ref-list"/>
		<xsl:apply-templates select="$translations[@xml:lang='en']/back/*[name()!='ack']"/>
		</back>
	</xsl:template>
	<!-- BODY - end -->
	
	<xsl:template match="sub-article[@article-type='translation' and @xml:lang!='en']//article-title/xref"></xsl:template>
	<xsl:template match="sub-article[@article-type='translation']//front-stub//@xml:lang|sub-article[@article-type='translation']//front//@xml:lang"></xsl:template>
	<xsl:template match="mixed-citation">
		<xsl:choose>
			<xsl:when test="$xml_type='scielo'"/>
			<xsl:otherwise>
				<xsl:element name="{name()}">
					<xsl:apply-templates/>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="aff/institution[@content-type='original']/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="aff/institution[@content-type='original']/*">
		<xsl:copy-of select="."/>
	</xsl:template>
	
	<xsl:template match="aff/institution[@content-type='aff-pmc']/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="aff/institution[@content-type='aff-pmc']/*">
		<xsl:copy-of select="."/>
	</xsl:template>
	
	<xsl:template match="aff">
		<aff>
			<xsl:apply-templates select="@id | label"/>
			<xsl:choose>
				<xsl:when test="institution[@content-type='original']">
					<xsl:choose>
						<xsl:when test="email">
							<xsl:value-of select="substring-before(institution[@content-type='original'],email)"/>
							<email><xsl:value-of select="email"/></email>
							<xsl:value-of select="substring-after(email,institution[@content-type='original'])"/>
						</xsl:when>
						<xsl:otherwise><xsl:apply-templates select="institution[@content-type='original']"/></xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:when test="institution[@content-type='aff-pmc']">
					<xsl:apply-templates select="institution[@content-type='aff-pmc']"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:variable name="inst"><xsl:value-of select="normalize-space(institution[@content-type='orgname'])"/></xsl:variable>
					<xsl:variable name="is_full"><xsl:if test="$inst!=''"><xsl:apply-templates select="text()[string-length(normalize-space(.))&gt;=string-length($inst)]" mode="is_full"><xsl:with-param name="inst" select="$inst"></xsl:with-param></xsl:apply-templates></xsl:if></xsl:variable>
					<!--xsl:comment>is_full:<xsl:value-of select="$is_full"/> _</xsl:comment-->
					<xsl:choose>
						<xsl:when test="contains($is_full,'yes')">
							<!--xsl:comment>full</xsl:comment-->
							<xsl:apply-templates select="text()[string-length(normalize-space(.))&gt;=string-length($inst)]" mode="full">
								<xsl:with-param name="inst" select="$inst"></xsl:with-param>
							</xsl:apply-templates><xsl:apply-templates select="country|email"></xsl:apply-templates>
						</xsl:when>
						<xsl:otherwise>
							<!--xsl:comment>parts</xsl:comment-->					
							<xsl:apply-templates
								select="text()[normalize-space(.)!='' and normalize-space(.)!=','] | institution | addr-line | country | email"
								mode="aff-insert-separator"/>					
						</xsl:otherwise>
					</xsl:choose>
				</xsl:otherwise>
			</xsl:choose>
		</aff>
	</xsl:template>
	<xsl:template match="institution[@content-type='aff-pmc']">
		<xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="institution[@content-type='aff-pmc']/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="institution[@content-type='aff-pmc']/named-content">
		<xsl:element name="{@content-type}">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="institution[@content-type='original']">
		<xsl:apply-templates select="*|text()"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="institution[@content-type='original']/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="institution[@content-type='original']/named-content">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="text()" mode="is_full">
		<xsl:param name="inst"></xsl:param>
		<xsl:if test="$inst!='' and contains(.,$inst)">yes</xsl:if>
	</xsl:template>
	<xsl:template match="*" mode="full"></xsl:template>
	<xsl:template match="text()" mode="full">
		<xsl:param name="inst"></xsl:param>
		<!--xsl:comment>text():<xsl:value-of select="."/>_</xsl:comment -->
		<!-- xsl:comment>$inst:<xsl:value-of select="$inst"/>_</xsl:comment -->
		<!-- xsl:comment>contains(.,$inst):<xsl:value-of select="contains(.,$inst)"/>_</xsl:comment-->
		<xsl:if test="$inst!='' and contains(.,$inst)"><xsl:value-of select="."/></xsl:if>
		
	</xsl:template>
	
	
	<xsl:template match="aff/* | addr-line/* " mode="aff-insert-separator">
		<xsl:if test="position()!=1">, </xsl:if>
		<xsl:apply-templates select="*|text()[normalize-space(.)!='' and normalize-space(.)!=',']"
			mode="aff-insert-separator"/>
	</xsl:template>
	
	<xsl:template match="aff/text() | addr-line/text()" mode="aff-insert-separator">
		<xsl:variable name="text" select="normalize-space(.)"/>
		<!-- xsl:comment>_ <xsl:value-of select="$text"/>  _</xsl:comment -->  
		
		<xsl:if test="position()!=1">, </xsl:if>
		
		<xsl:choose>
			<xsl:when test="substring($text,string-length($text),1)=','">
				<xsl:value-of select="substring($text,1,string-length($text)-1)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text"/>
			</xsl:otherwise>
		</xsl:choose>
		
	</xsl:template>
	<xsl:template match="email">
		<email><xsl:value-of select="."/></email>
	</xsl:template>
	<xsl:template match="email" mode="aff-insert-separator">
		<xsl:if test="position()!=1">, </xsl:if>
		<xsl:copy-of select="."/>
	</xsl:template>

	<xsl:template match="funding-group">
		<xsl:if test="$display_funding='yes'">
			<xsl:element name="{name()}">
				<xsl:apply-templates select="@* | * | text()"/>
			</xsl:element>
		</xsl:if>
	</xsl:template>


	<xsl:template match="graphic/@href">
		<xsl:attribute name="{name()}">
			<xsl:choose>
				<xsl:when test="$new_name!=''"><xsl:value-of select="$new_name"/>-g<xsl:value-of
						select="../../@id"/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="equation/graphic/@href">
		<xsl:attribute name="{name()}">
			<xsl:choose>
				<xsl:when test="$new_name!=''"><xsl:value-of select="$new_name"/>-e<xsl:value-of
						select="../../@id"/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="inline-graphic/@href">
		<xsl:attribute name="{name()}">
			<xsl:if test="$new_name!=''"><xsl:value-of select="$new_name"/>-i<xsl:value-of
					select="../../@id"/></xsl:if>
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>

	<xsl:template match="related-object[@specific-use='processing-only']">
		
	</xsl:template>
	<xsl:template match="contrib-id">
		<!-- 
		    'lattes': 'http://lattes.cnpq.br/',
    'orcid': 'http://orcid.org/',
    'researchid': 'http://www.researcherid.com/rid/',
    'scopus': 'https://www.scopus.com/authid/detail.uri?authorId='
		-->
		<contrib-id>
			<xsl:attribute name="contrib-id-type"><xsl:value-of select="@contrib-id-type"/></xsl:attribute>
		<xsl:choose>
			<xsl:when test="@contrib-id-type='lattes' and not(contains(.,'http://lattes.cnpq.br/'))">http://lattes.cnpq.br/</xsl:when>
			<xsl:when test="@contrib-id-type='orcid' and not(contains(.,'http://orcid.org/'))">http://orcid.org/</xsl:when>
			<xsl:when test="@contrib-id-type='researchid'and not(contains(.,'http://www.researcherid.com/rid/'))">http://www.researcherid.com/rid/</xsl:when>
			<xsl:when test="@contrib-id-type='scopus'and not(contains(.,'https://www.scopus.com/authid/detail.uri?authorId='))">https://www.scopus.com/authid/detail.uri?authorId=</xsl:when>
		</xsl:choose><xsl:value-of select="."/>
		</contrib-id>
	</xsl:template>
	<xsl:template match="contrib/xref[normalize-space(text())='' and not(*)]"></xsl:template>
	<xsl:template match="ref/@specific-use|element-citation/@specific-use"></xsl:template>
	<xsl:template match="article/@specific-use"></xsl:template>
	
	<xsl:template match="equation/alternatives">
		<xsl:copy-of select="graphic"/>
		<xsl:if test="not(graphic)">
			<xsl:copy-of select="mml:math"/>
			<xsl:if test="not(mml:math)">
				<xsl:copy-of select="tex-math"/>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	<xsl:template match="ext-link[@ext-link-type='clinical-trial']">
		<uri>
			<xsl:attribute name="content-type"><xsl:value-of select="@ext-link-type"/></xsl:attribute>
			<xsl:apply-templates select="@xlink:href|*|text()"/>
		</uri>
	</xsl:template>
	
	<xsl:template match="funding-group"></xsl:template>
</xsl:stylesheet>
