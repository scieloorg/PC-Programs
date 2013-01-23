<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">

	<xsl:include href="local_dtd.xsl"/>
	
	<xsl:variable name="display_funding"><xsl:choose>
		<!--
		Verifica se a seção Agradecimentos contém o número do projeto do funding group
		Se contém, funding-group deve ser excluído
		-->
		<xsl:when test="not(//ack)">yes</xsl:when>
		<xsl:when test=".//ack and contains(.//ack//p, .//funding-group//award-id)">no</xsl:when>
		<xsl:otherwise>yes</xsl:otherwise>
		</xsl:choose></xsl:variable>

    <xsl:variable name="xml_type">
		<xsl:choose>
			<xsl:when test=".//mixed-citation and .//element-citation">scielo</xsl:when>
			<xsl:otherwise>pmc</xsl:otherwise>
		</xsl:choose>
		
	</xsl:variable>


	<xsl:template match="*">
		<xsl:element name="{name()}">
		<xsl:apply-templates select="@* | * | text()"/></xsl:element>
	</xsl:template>
	<xsl:template match="@*"><xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute></xsl:template>
	<xsl:template match="text()"><xsl:value-of select="."/></xsl:template>

	<xsl:template match="mixed-citation">
		<xsl:choose>
			<xsl:when test="$xml_type='scielo'"></xsl:when>
			<xsl:otherwise>
				<xsl:element name="{name()}"><xsl:apply-templates/></xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>


	<xsl:template match="aff//institution | aff//addr-line | aff//named-content | aff//country">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	
	<xsl:template match="aff/text()">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>

	<xsl:template match="funding-group"><xsl:if test="$display_funding='yes'"><xsl:element name="{name()}">
		<xsl:apply-templates select="@* | * | text()"/></xsl:element></xsl:if></xsl:template>

</xsl:stylesheet>
