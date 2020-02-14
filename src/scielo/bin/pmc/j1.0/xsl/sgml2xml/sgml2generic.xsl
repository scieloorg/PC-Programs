<?xml version="1.0" encoding="UTF-8"?>
<!--  xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" 
xmlns:ie5="http://www.w3.org/TR/WD-xsl" 


-->
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"
	xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:include href="../../../v3.0/xsl/sgml2xml/sgml2generic.xsl"/>

	<xsl:template match="ctrbid">
		<contrib-id contrib-id-type="{@ctrbidtp}">
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</contrib-id>
	</xsl:template>
	<xsl:template match="article|text|doc" mode="dtd-version">
		<xsl:attribute name="dtd-version">1.0</xsl:attribute>
	</xsl:template>
	<xsl:template match="article | text | doc" mode="new-pub-date">
		<!-- anteriormente somente @pub-type -->
		
		<!-- 
		date-type — must be used with @publication-format; 
			suggested values include pub, corrected, retracted, preprint. Must not be used with @pub-type.
		pub-type — The values depend on the model of publication used. See above for details.
        publication-format — Must be used with @date-type; values include "print", "electronic", or "electronic-print". Must not be used with @pub-type.
		-->
		
		
		<xsl:variable name="preprint_date">
			<xsl:choose>
				<xsl:when test="@rvpdate">
					<xsl:value-of select="@rvpdate"/>
				</xsl:when>
				<xsl:when test="@ahpdate">
					<xsl:value-of select="@ahpdate"/>
				</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="string-length(normalize-space($preprint_date))&gt;0">
			<pub-date>
				<!--  pub-type="epub" -->
				<xsl:attribute name="date-type">preprint</xsl:attribute>
				<xsl:attribute name="publication-format">electronic</xsl:attribute>
				<xsl:attribute name="iso-8601-date"><xsl:apply-templates select="$preprint_date" mode="dateiso"></xsl:apply-templates></xsl:attribute>
				
				<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso">
						<xsl:value-of select="$preprint_date"/>
					</xsl:with-param>
				</xsl:call-template>
			</pub-date>
		</xsl:if>
		<xsl:variable name="dateiso"><xsl:choose>
					<xsl:when test="@artdate!=''"><xsl:value-of select="@artdate"/></xsl:when>
						<xsl:otherwise><xsl:value-of select="@dateiso"/></xsl:otherwise>
		</xsl:choose></xsl:variable>
		<xsl:variable name="date"><xsl:choose>
			<xsl:when test="@artdate!=''"><xsl:value-of select="@artdate"/></xsl:when>
					<xsl:otherwise><xsl:value-of select="//extra-scielo//season"/></xsl:otherwise>
				</xsl:choose></xsl:variable>
		<pub-date>
			<!-- pub-type="{$date_type}" -->
			<xsl:attribute name="date-type">pub</xsl:attribute>
			<xsl:attribute name="publication-format"><xsl:value-of select="$pub_type"/></xsl:attribute>
			<xsl:attribute name="iso-8601-date"><xsl:choose>
				<xsl:when test="@artdate!=''"><xsl:apply-templates select="@artdate" mode="dateiso"/></xsl:when>
				<xsl:otherwise><xsl:apply-templates select="@dateiso" mode="dateiso"/></xsl:otherwise>
			</xsl:choose></xsl:attribute>
			
			<xsl:call-template name="display_date">
				<xsl:with-param name="dateiso" select="$dateiso"/>
				<xsl:with-param name="date" select="$date"/>
			</xsl:call-template>
		</pub-date>
		
		<xsl:if test="$pub_type='electronic'">
			<pub-date>
				<!-- pub-type="{$date_type}" -->
				<xsl:attribute name="date-type">collection</xsl:attribute>
				<xsl:attribute name="publication-format"><xsl:value-of select="$pub_type"/></xsl:attribute>
				<xsl:attribute name="iso-8601-date"><xsl:apply-templates select="@dateiso" mode="dateiso"></xsl:apply-templates></xsl:attribute>
				
				<xsl:call-template name="display_date">
					<xsl:with-param name="dateiso">
						<xsl:value-of select="@dateiso"/>
					</xsl:with-param>
					<xsl:with-param name="date">
						<xsl:value-of select="//extra-scielo//season"/>
					</xsl:with-param>
				</xsl:call-template>
			</pub-date>
		</xsl:if>
	</xsl:template>
	<xsl:template match="back//cited | doc//cited">
		<date-in-citation content-type="access-date">
			<xsl:attribute name="iso-8601-date"><xsl:apply-templates select="@dateiso" mode="dateiso"></xsl:apply-templates></xsl:attribute>
			
			<xsl:value-of select="."/>
		</date-in-citation>
	</xsl:template>
	<xsl:template match="@* | * | text()" mode="dateiso">
		<xsl:if test=".!=''">
		<xsl:value-of select="substring(.,1,4)"/>-<xsl:value-of select="substring(.,5,2)"/>-<xsl:value-of select="substring(.,7)"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="ref/text()"></xsl:template>
</xsl:stylesheet>
