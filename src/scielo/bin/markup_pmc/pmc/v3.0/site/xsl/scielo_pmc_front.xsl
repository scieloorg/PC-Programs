<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:variable name="countAFF" select="count(//aff)"/>
	<!--
		DEFAULT
	-->
	<xsl:template match="xref" mode="front">
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="*|@*|text()" mode="arabic2romanNumber">
		<xsl:param name="xref"/>
		<xsl:choose>
			<xsl:when test="$xref='1'">I</xsl:when>
			<xsl:when test="$xref='2'">II</xsl:when>
			<xsl:when test="$xref='3'">III</xsl:when>
			<xsl:when test="$xref='4'">IV</xsl:when>
			<xsl:when test="$xref='5'">V</xsl:when>
			<xsl:when test="$xref='6'">VI</xsl:when>
			<xsl:when test="$xref='7'">VII</xsl:when>
			<xsl:when test="$xref='8'">VIII</xsl:when>
			<xsl:when test="$xref='9'">IX</xsl:when>
			<xsl:when test="$xref='10'">X</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$xref"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!--
	make-front
	-->
	<xsl:template match="*" mode="make-front">
		<!-- FIXME nao tem article-categories no XML -->
		<xsl:apply-templates select=".//article-categories"/>
		<xsl:apply-templates select=".//title-group/article-title" mode="format"/>
		<xsl:apply-templates select=".//title-group//trans-title" mode="format"/>
		<xsl:if test="not(.//title-group//trans-title)">
			<xsl:apply-templates select="trans-title" mode="format"/>
		</xsl:if>
		<xsl:apply-templates select=".//contrib-group" mode="front"/>
		<xsl:if test=".//aff">
			<p>
				<xsl:apply-templates select=".//aff" mode="front"/>
			</p>
		</xsl:if>
		<xsl:apply-templates select="//author-notes" mode="format"/>
		<div>
			<xsl:apply-templates select="." mode="sections"/>
		</div>
		<hr/>
		<xsl:apply-templates select=".//abstract" mode="format"/>
		<xsl:apply-templates select=".//trans-abstract" mode="format"/>
		
	</xsl:template>
	<!--
	TITLE
	-->
	<xsl:template match="subtitle" mode="format">
		: <xsl:apply-templates select="."/>
	</xsl:template>
	<xsl:template match="article-title" mode="format">
		<a name="top">&#160;</a>
		<p class="scielo-article-title">
			<!--xsl:value-of select="." disable-output-escaping="yes"/-->
			<xsl:apply-templates/>
			<xsl:apply-templates select=" ../subtitle" mode="format"/>
		</p>
	</xsl:template>
	<xsl:template match="trans-title" mode="format">
		<xsl:variable name="lang" select="@xml:lang"/>
		<p class="scielo-article-other-titles{$languages//language[@id=$lang]/@view}">
			<xsl:apply-templates/>
			<xsl:apply-templates select=" ../subtitle" mode="format"/>
		</p>
	</xsl:template>
	<!--
	contrib-group
	-->
	<xsl:template match="contrib-group" mode="front">
		<p class="scielo-authors">
			<xsl:apply-templates select=".//contrib/name" mode="front"/>
		</p>
	</xsl:template>
	<xsl:template match="name" mode="front">
		<xsl:apply-templates select="given-names" mode="front"/>&#160;<xsl:apply-templates select="surname" mode="front"/>
		<xsl:apply-templates select="../xref" mode="front"/>
		<xsl:if test="position()!=last()">; </xsl:if>
	</xsl:template>
	<xsl:template match="xref[@ref-type='aff']" mode="front">
		<xsl:if test="$countAFF&gt;1">
			<xsl:choose>
				<xsl:when test="sup">
					<sup>
						<xsl:if test="position()&gt;1">, </xsl:if>
						<xsl:value-of select="sup"/>
					</sup>
				</xsl:when>
				<xsl:otherwise>
					<xsl:variable name="xref" select="substring-after(@rid,'aff')"/>
					<sup>
						<xsl:if test="position()&gt;1">, </xsl:if>
						<xsl:apply-templates select="." mode="arabic2romanNumber">
							<xsl:with-param name="xref" select="$xref"/>
						</xsl:apply-templates>
					</sup>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	<xsl:template match="xref[@ref-type='aff']/@rid | aff/@id" mode="front">
		<xsl:if test="$countAFF&gt;1">
			<sup>
				<xsl:apply-templates select="."/>
			</sup>
		</xsl:if>
	</xsl:template>
	<!-- 
	AFF
	-->
	<xsl:template match="aff" mode="front">
		<xsl:if test="$countAFF&gt;1">
			<xsl:if test="not(label)">
				<sup>
					<xsl:apply-templates select="." mode="arabic2romanNumber">
						<xsl:with-param name="xref" select="substring-after(@id,'aff')"/>
					</xsl:apply-templates>
				</sup>&#160;
		</xsl:if>
		</xsl:if>
		<xsl:apply-templates mode="front"/>
		<br/>
	</xsl:template>
	<xsl:template match="aff/*" mode="front">
		<xsl:apply-templates/>
		<xsl:if test="position()!=last()">, </xsl:if>
	</xsl:template>
	<!--
		AUTHOR NOTES
	-->
	<xsl:template match="xref[@ref-type='author-notes']" mode="front">
		<a href="#{@rid}">
			<xsl:apply-templates/>
		</a>
	</xsl:template>
	<xsl:template match="author-notes" mode="format">
		<xsl:variable name="xref" select="corresp/@id"/>
		<p>
			<a>
				<xsl:attribute name="href">#CORRESP</xsl:attribute>
				<xsl:apply-templates select="." mode="translate"/>
			</a>
		</p>
		<p>
			<br/>
		</p>
		<p>
			<br/>
		</p>
	</xsl:template>
	<xsl:template match="author-notes" mode="translate">
		<xsl:param name="lang">
			<xsl:choose>
				<xsl:when test="../../../../..//ARTICLE/@TEXTLANG">
					<xsl:value-of select="../../../../..//ARTICLE/@TEXTLANG"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="../../../..//@xml:lang"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:param>
		<xsl:choose>
			<xsl:when test="$lang='pt' ">Correspondencia</xsl:when>
			<xsl:when test="$lang='es' ">Correspondencia</xsl:when>
			<xsl:when test="$lang='en' ">Send correspondence to</xsl:when>
		</xsl:choose>
	</xsl:template>
	<!--
	SECTIONS
	-->
	<xsl:template match="*|@*|text" mode="sections">
		<ul class="section-list">
			<a name="topo"/>
			<xsl:if test=".//abstract">
				<li>
					<a href="#ABSTRACT">
						<xsl:value-of select="document(concat('../xml/',$mainLanguage,'/translation.xml'))//xslid[@id='sci_abstract']/text[@find='abstract']"/>
					</a>
				</li>
			</xsl:if>
			<xsl:apply-templates select="..//sec[@sec-type]" mode="link2sections"/>
		</ul>
	</xsl:template>
	<xsl:template match="sec" mode="link2sections">
		<li>
			<a href="#{@sec-type}">
				<xsl:apply-templates select="label"/>
			</a>
		</li>
	</xsl:template>
	<xsl:template match="sec//label">
		<xsl:apply-templates select="*|@*|text()"/>
	</xsl:template>
	<xsl:template match="subject">
		<span class="subject">
			<xsl:value-of select="."/>
		</span>
	</xsl:template>
	<!--
	KEYWORDS
	-->

	<xsl:template match="kwd-group">
		<p>
			<span class="scielo-authors">
				<xsl:call-template name="make-id"/>
				<xsl:choose>
					<xsl:when test="@xml:lang">
						<xsl:value-of select="document(concat('../xml/',@xml:lang,'/translation.xml'))//xslid[@id='sci_abstract']/text[@find='keywords']"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="document('../xml/en/translation.xml')//xslid[@id='sci_abstract']/text[@find='keywords']"/>
					</xsl:otherwise>
				</xsl:choose>
			</span>: 
			<xsl:apply-templates select="kwd"/>
		</p>
	</xsl:template>
	<xsl:template match="kwd" >
		<xsl:value-of select="."/><xsl:if test="position()!=last()">; </xsl:if>
	</xsl:template>
	<!--
	ABSTRACT
	-->

	<xsl:template match="abstract | trans-abstract" mode="format">
		<xsl:variable name="lang" select="@xml:lang"/>
		<a name="ABSTRACT"/>
		<div class="abstract{$languages//language[@id=$lang]/@view}">
			<span class="abstract-title">
				<!-- if there's no title, create one -->
				<xsl:apply-templates select="." mode="words-for-abstract-title"/>
			</span>: <xsl:apply-templates select="*[not(self::title)]|text()"/>
		</div>
		<xsl:apply-templates select="..//kwd-group[@xml:lang=$lang or not(@xml:lang)]"/>
		
			<hr/>
		
	</xsl:template>
	<xsl:template match="*" mode="words-for-abstract-title">
		<xsl:choose>
			<!-- if there's a title, use it -->
			<xsl:when test="title">
				<xsl:apply-templates select="title"/>
			</xsl:when>
			<!-- abstract with no title -->
			<xsl:when test="self::abstract">
				<xsl:value-of select="document(concat('../xml/',@xml:lang,'/translation.xml'))//xslid[@id='sci_abstract']/text[@find='abstract']"/>
			</xsl:when>
			<!-- trans-abstract with no title -->
			<xsl:when test="self::trans-abstract">
				<span class="gen">
					<xsl:value-of select="document(concat('../xml/',@xml:lang,'/translation.xml'))//xslid[@id='sci_abstract']/text[@find='abstract']"/>
				</span>
			</xsl:when>
			<!-- there is no logical otherwise -->
		</xsl:choose>
	</xsl:template>
</xsl:transform>
