<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="xref[@rid='']"/>
	<xsl:template match="thesgrp"/>
	<xsl:template match="report">
		<funding-group>
			<xsl:apply-templates select="rsponsor | projname "/>
			<xsl:if test="not($unident_back[contains(.//text,'ACK') or contains(.//text,'Ack') or contains(.//text,'Agrad') or contains(.//text,'AGRAD')])">
			<funding-statement>
				<xsl:apply-templates select=".//text()"/>
			</funding-statement></xsl:if>
		</funding-group>
	</xsl:template>
	<xsl:template match="rsponsor | projname">
	<xsl:if test="orgname or contract">
		<award-group>
			<xsl:attribute name="award-type"><xsl:choose><xsl:when test=".//contract">contract</xsl:when><xsl:otherwise>grant</xsl:otherwise></xsl:choose></xsl:attribute>
			<xsl:apply-templates select="orgname"/>
						<xsl:apply-templates select="contract"/>

		</award-group>
		</xsl:if>
	</xsl:template>
	<xsl:template match="contract">
		<award-id>
			<xsl:apply-templates/>
		</award-id>
	</xsl:template>
	<xsl:template match="rsponsor/orgdiv"/>
	<xsl:template match="rsponsor/orgname">
		<funding-source>
			<xsl:value-of select="."/>
			<xsl:if test="../orgdiv">, 
				<xsl:value-of select="../orgdiv"/>
			</xsl:if>
		</funding-source>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//country">
		<xsl:choose>
			<xsl:when test="../city">
					
			</xsl:when>
			<xsl:when test="../state">
				
			</xsl:when>
			<xsl:otherwise>
				<publisher-loc><xsl:value-of select="."/></publisher-loc>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//city">
		<publisher-loc><xsl:value-of select="."/>
		<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
		<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</publisher-loc>
	</xsl:template>
	<xsl:template match="back//*[contains(name(),'citat')]//state">
		<xsl:choose>
			<xsl:when test="../city">
					
			</xsl:when>
			<xsl:otherwise>
				<publisher-loc><xsl:value-of select="."/><xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if></publisher-loc>
			</xsl:otherwise>
		</xsl:choose>
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
	<xsl:template match="confgrp">
		<conference><xsl:apply-templates select="*|text()"/></conference>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//confgrp">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="confgrp/date">
		<conf-date><xsl:value-of select="."/></conf-date>
	</xsl:template>
	<xsl:template match="confgrp/sponsor">
		<conf-sponsor><xsl:value-of select="."/></conf-sponsor>
	</xsl:template>
	<xsl:template match="confgrp/city">
		<conf-loc><xsl:value-of select="."/>
		<xsl:if test="../state">, <xsl:value-of select="../state"/></xsl:if>
		<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</conf-loc>
	</xsl:template>
	<xsl:template match="confgrp/state">
		<xsl:if test="not(../city)">
		
		<conf-loc><xsl:value-of select="."/>
		<xsl:if test="../country">, <xsl:value-of select="../country"/></xsl:if>
		</conf-loc></xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/country">
		<xsl:if test="not(../city) and not(../state)">
		
		<conf-loc><xsl:value-of select="."/>
		</conf-loc></xsl:if>
	</xsl:template>
	<xsl:template match="confgrp/no"/>
	<xsl:template match="confgrp/confname"><conf-name><xsl:apply-templates select="../..//confgrp" mode="fulltitle"/></conf-name></xsl:template>
		
	<xsl:template match="confgrp" mode="fulltitle">
		<xsl:apply-templates select="no|confname" mode="fulltitle"/></xsl:template>
		
	<xsl:template match="confgrp/confname | confgrp/no"  mode="fulltitle"><xsl:value-of select="."/> &#160; </xsl:template>
	
</xsl:stylesheet>
