<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="aff/city | aff/state | aff/@orgdiv1 | aff/@orgdiv2 | aff/@orgdiv3"/>
	<xsl:template match="aff/@orgdiv1 | aff/@orgdiv2 | aff/@orgdiv3" mode="org-aff">
		<xsl:value-of select="."/>, 
	</xsl:template>
	<xsl:template match="aff/@orgname">
		<institution>
			<xsl:apply-templates select="../@orgdiv3" mode="org-aff"/>
			<xsl:apply-templates select="../@orgdiv2" mode="org-aff"/>
			<xsl:apply-templates select="../@orgdiv1" mode="org-aff"/>
			<xsl:value-of select="."/>
		</institution>
	</xsl:template>
	<xsl:template match="xref[@rid='']"/>
	<xsl:template match="report | thesgrp"/>
	<xsl:template match="rsponsor/*"/>
	<xsl:template match="rsponsor">
		<award-group award-type="contract">
			<xsl:apply-templates/>
		</award-group>
	</xsl:template>
	<xsl:template match="rsponsor/text()">
		<!--xsl:comment><xsl:apply-templates/></xsl:comment-->
	</xsl:template>
	<xsl:template match="contract">
		<award-id>
			<xsl:apply-templates/>
		</award-id>
	</xsl:template>
	<xsl:template match="rsponsor/orgname">
		<funding-source>
			<xsl:value-of select="."/>
			<xsl:value-of select="../orgdiv"/>
		</funding-source>
	</xsl:template>
	<xsl:template match="report/text()"/>
	<xsl:template match="report">
		<funding-group>
			<xsl:apply-templates/>
		</funding-group>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'monog')]//state | back//*[contains(name(),'monog')]//country"/>
	<xsl:template match="back//*[contains(name(),'monog')]//city">
		<publisher-loc>
			<xsl:value-of select="."/>
			<xsl:if test="../state">, <xsl:value-of select="../state"/>
			</xsl:if>
			<xsl:if test="../country">, <xsl:value-of select="../country"/>
			</xsl:if>
		</publisher-loc>
	</xsl:template>
	<xsl:template match="confgrp">
		<conference>
			<conf-date>
				<xsl:value-of select="date"/>
			</conf-date>
			<conf-name>
				<xsl:apply-templates select="no | confname"/>
			</conf-name>
			<xsl:if test="city or state or country">
				<conf-loc>
					<xsl:value-of select="city"/>
					<xsl:if test="city and state">, </xsl:if>
					<xsl:value-of select="state"/>
				<xsl:if test="(city or state) and country">,</xsl:if>

					<xsl:value-of select="country"/>
				</conf-loc>
			</xsl:if>
			<xsl:if test="sponsor">
				<conf-sponsor>
					<xsl:value-of select="sponsor"/>
				</conf-sponsor>
			</xsl:if>
		</conference>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//confgrp">
		<conf-date>
			<xsl:value-of select="date"/>
		</conf-date>
		<conf-name>
			<xsl:apply-templates select="no | confname"/>
		</conf-name>
		<xsl:if test="city or state or country">
			<conf-loc>
				<xsl:value-of select="city"/>
				<xsl:if test="city and state">, </xsl:if>
				<xsl:value-of select="state"/>
				<xsl:if test="(city or state) and country">,</xsl:if>
				<xsl:value-of select="country"/>
			</conf-loc>
		</xsl:if>
		<xsl:if test="sponsor">
			<conf-sponsor>
				<xsl:value-of select="sponsor"/>
			</conf-sponsor>
		</xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/no | confgrp/confname">
		<xsl:value-of select="."/>&#160;</xsl:template>
</xsl:stylesheet>
