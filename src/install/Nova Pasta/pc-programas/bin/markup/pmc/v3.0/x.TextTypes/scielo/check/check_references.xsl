<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="ref">
		<p id="{@id}">
			<xsl:apply-templates select="label"/>
			<xsl:apply-templates select="citation|nlm-citation"/>
			<!--xsl:apply-templates select="citation/pub-id|nlm-citation/pub-id" mode="link"/-->
			<xsl:apply-templates select=".//pub-id" mode="link"/>
			<xsl:call-template name="nl-1"/>
		</p>
		<xsl:apply-templates select="citation|nlm-citation" mode="check-unmarked-text"/>
		<xsl:apply-templates select="citation|nlm-citation" mode="check-lang"/>

	</xsl:template>
	<xsl:template match="*[@citation-type]" mode="check-unmarked-text">
		<xsl:if test="text() or italic">
			<p class="warning">There are some texts should have been marked</p>
			<p class="xml">
				<quote>
					<xsl:apply-templates select="." mode="show-xml"/>
				</quote>
			</p>
		</xsl:if>
	</xsl:template>
	<xsl:template match="*" mode="show-xml">
		<span class="limiter">&lt;</span>
		<span class="element">
			<xsl:value-of select="name()"/>
		</span>
		<xsl:apply-templates select="@*" mode="show-xml"/>
		<span class="limiter">&gt;</span>
		<xsl:if test="*">
			<br/>
		</xsl:if>
		<xsl:apply-templates select="*|text()" mode="show-xml"/>
		<span class="limiter">&lt;/</span>
		<span class="element">
			<xsl:value-of select="name()"/>
		</span>
		<span class="limiter">&gt;</span>
		<br/>
	</xsl:template>
	<xsl:template match="text()" mode="show-xml">
		<xsl:choose>
			<xsl:when test="../citation or  ../nlm-citation or ../italic">
				<span class="destaque">
					<xsl:value-of select="."/>
				</span>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="italic" mode="show-xml">
		<xsl:choose>
			<xsl:when test="../citation or  ../nlm-citation or ../italic">
				<span class="destaque">
					<span class="limiter">&lt;</span>
					<span class="element">
						<xsl:value-of select="name()"/>
					</span>
					<xsl:apply-templates select="@*" mode="show-xml"/>
					<span class="limiter">&gt;</span>
					<xsl:if test="*">
						<br/>
					</xsl:if>
					<xsl:apply-templates select="*|text()" mode="show-xml"/>
					<span class="limiter">&lt;/</span>
					<span class="element">
						<xsl:value-of select="name()"/>
					</span>
					<span class="limiter">&gt;</span>
					<br/>
				</span>
			</xsl:when>
			<xsl:otherwise>
				<span class="limiter">&lt;</span>
		<span class="element">
			<xsl:value-of select="name()"/>
		</span>
		<xsl:apply-templates select="@*" mode="show-xml"/>
		<span class="limiter">&gt;</span>
		<xsl:if test="*">
			<br/>
		</xsl:if>
		<xsl:apply-templates select="*|text()" mode="show-xml"/>
		<span class="limiter">&lt;/</span>
		<span class="element">
			<xsl:value-of select="name()"/>
		</span>
		<span class="limiter">&gt;</span>
		<br/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="@*" mode="show-xml">
		<span class="element">
&#160;<xsl:value-of select="name()"/>
		</span>
		<span class="limiter">="</span>
		<xsl:value-of select="."/>
		<span class="limiter">"</span>
	</xsl:template>
	<xsl:template match="*[@citation-type]" mode="check-errors">
		<xsl:choose>
			<xsl:when test="person-group or collab"/>
			<xsl:otherwise>missing person-group or collab</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'source'"/>
			<xsl:with-param name="name2" select="'trans-source'"/>
		</xsl:apply-templates>
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'year'"/>
			<xsl:with-param name="name2" select="'trans-source'"/>
		</xsl:apply-templates>
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'volume'"/>
			<xsl:with-param name="name2" select="'issue'"/>
			<xsl:with-param name="name3" select="'supplement'"/>
		</xsl:apply-templates>
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'publisher-loc'"/>
			<xsl:with-param name="name2" select="'publisher-name'"/>
		</xsl:apply-templates>
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'fpage'"/>
			<xsl:with-param name="name2" select="'lpage'"/>
			<xsl:with-param name="name3" select="'page-count'"/>
		</xsl:apply-templates>
		<xsl:apply-templates select="." mode="check-specific-errors"/>
	</xsl:template>
	<xsl:template match="*[@citation-type='book']" mode="check-specific-errors">
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'series'"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="*[@citation-type='commun']" mode="check-specific-errors"/>
	<xsl:template match="*[@citation-type='confproc']" mode="check-specific-errors">
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'conf-name'"/>
			<xsl:with-param name="name2" select="'conf-loc'"/>
			<xsl:with-param name="name3" select="'conf-date'"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="*[@citation-type='discussion']" mode="check-specific-errors"/>
	<xsl:template match="*[@citation-type='gov']" mode="check-specific-errors"/>
	<xsl:template match="*[@citation-type='journal']" mode="check-specific-errors">
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'article-title'"/>
			<xsl:with-param name="name2" select="'trans-title'"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="*[@citation-type='list']" mode="check-specific-errors"/>
	<xsl:template match="*[@citation-type='other']" mode="check-specific-errors"/>
	<xsl:template match="*[@citation-type='patent']" mode="check-specific-errors">
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'patent'"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="*[@citation-type='thesis']" mode="check-specific-errors"/>
	<xsl:template match="*[@citation-type='web']" mode="check-specific-errors">
		<xsl:apply-templates select="." mode="check">
			<xsl:with-param name="name1" select="'access-date'"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="*" mode="check">
		<xsl:param name="name1"/>
		<xsl:param name="name2"/>
		<xsl:param name="name3"/>
		<p>
			<xsl:choose>
				<xsl:when test="not(.//node()[name()=$name1])">
				missing <xsl:value-of select="$name1"/>
				</xsl:when>
				<xsl:when test="$name2 and not(.//node()[name()=$name2])">
				or <xsl:value-of select="$name2"/>
				</xsl:when>
				<xsl:when test="$name3 and not(.//node()[name()=$name3])">
				or <xsl:value-of select="$name3"/>
				</xsl:when>
			</xsl:choose>
		</p>
	</xsl:template>
</xsl:transform>
