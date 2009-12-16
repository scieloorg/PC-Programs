<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="*" mode="check-unmarked-text">
		<xsl:if test="text() or italic">
			<p class="warning"><xsl:value-of select="$translations//message[@key='TextViewer.text.page.warning.missingMarkup']"/></p>
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
	
</xsl:transform>
