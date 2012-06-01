<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="xref[@rid='']"/>
	<xsl:template match="thesgrp"/>
	<xsl:template match="front//report | bbibcom//report">
		<funding-group>
			<xsl:apply-templates select="rsponsor | projname "/>
			<xsl:if test="not($unident_back[contains(.//text,'ACK') or contains(.//text,'Ack') or contains(.//text,'Agrad') or contains(.//text,'AGRAD')])">
			<funding-statement>
				<xsl:apply-templates select=".//text()"/>
			</funding-statement></xsl:if>
		</funding-group>
	</xsl:template>
	<xsl:template match="front//rsponsor | front//projname| bbibcom//rsponsor | bbibcom//projname">
	<xsl:if test="orgname or contract">
		<award-group>
			<xsl:attribute name="award-type"><xsl:choose><xsl:when test=".//contract">contract</xsl:when><xsl:otherwise>grant</xsl:otherwise></xsl:choose></xsl:attribute>
			<xsl:apply-templates select="orgname"/>
						<xsl:apply-templates select="contract"/>

		</award-group>
		</xsl:if>
	</xsl:template>
	<xsl:template match="front//contract | bbibcom//contract">
		<award-id>
			<xsl:apply-templates/>
		</award-id>
	</xsl:template>
	<xsl:template match="front//rsponsor/orgdiv | bbibcom//orgdiv"/>
	<xsl:template match="front//rsponsor/orgname | bbibcom//orgname">
		<funding-source>
			<xsl:value-of select="."/>
			<xsl:if test="../orgdiv">, 
				<xsl:value-of select="../orgdiv"/>
			</xsl:if>
		</funding-source>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//report">
		<comment><xsl:apply-templates select="*|text()"/></comment>
	</xsl:template>
	<xsl:template match="*[contains(name(),'citat')]//report//* | *[contains(name(),'citat')]//report//rsponsor">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	
	<xsl:template match="*[contains(name(),'citat')]//report//text()">
		<xsl:value-of select="."/>
	</xsl:template>
	
	
</xsl:stylesheet>
