<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="article_xml_lang" select="//*[front]/@xml:lang"/>
	<xsl:template match="abstract | trans-abstract | trans-title | article-title | source[not(../article-title)] | kwd-group " mode="check">
		<xsl:if test="not(@xml:lang)">
			<p class="warning">
				<xsl:value-of select="substring-before($translations//message[@key='TextViewer.text.page.warning.missingLanguage'],'@xml:lang')"/>
				<xsl:value-of select="name()"/>/@xml:lang <xsl:value-of select="substring-after($translations//message[@key='TextViewer.text.page.warning.missingLanguage'],'@xml:lang')"/>  (<xsl:value-of select="$article_xml_lang"/>)</p>
			<p class="xml">
				<quote>
					<xsl:apply-templates select="." mode="show-xml"/>
				</quote>
			</p>
		</xsl:if>
	</xsl:template>
	<xsl:template match="abstract" mode="format">
		<xsl:variable name="lang" select="@xml:lang"/>
		<span class="abstract-title">
			<!-- if there's no title, create one -->
			<xsl:apply-templates select="." mode="words-for-abstract-title"/>
		</span>
		<div class="abstract{$languages//language[@id=$lang]/@view}">
			<xsl:apply-templates select="*[not(self::title)]|text()"/>
		</div>
		<xsl:apply-templates select="." mode="check"/>
		<xsl:apply-templates select="..//kwd-group[@xml:lang=$lang or not(@xml:lang)]"/>
		<xsl:apply-templates select="..//kwd-group" mode="check"/>
		<xsl:if test="position()!=last()">
			<hr/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="*[@citation-type='journal']" mode="check-lang">
		<xsl:if test=".//article-title[not(@xml:lang)]">
			<xsl:apply-templates select=".//article-title" mode="check"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="*[@citation-type!='journal']" mode="check-lang">
		<xsl:if test=".//source[not(@xml:lang)]">
			<xsl:apply-templates select=".//source" mode="check"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="text()" mode="show-xml">
		<xsl:choose>
			<xsl:when test="../name()='citation' or ../name()='nlm-citation' or ../name()='italic'">
				<span class="destaque">
					<xsl:value-of select="."/>
				</span>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="title-group" mode="front">
		<span class="tl-document">
			<xsl:apply-templates select="article-title" mode="front"/>
			<xsl:apply-templates select="subtitle" mode="front"/>
			<xsl:apply-templates select="trans-title | alt-title" mode="front"/>
			<xsl:apply-templates select="article-title|trans-title" mode="check"/>
		</span>
	</xsl:template>
</xsl:transform>
