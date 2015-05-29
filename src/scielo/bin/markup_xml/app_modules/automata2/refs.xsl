<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" >
	<!--
		1. Vieira AML, Souza CE, Labruna MB, Mayo RC, Souza SSL, Camargo-Neves VLF. Manual de vigilância acarológica, Estado de São Paulo. São Paulo: Secretaria de Estado da Saúde de São Paulo; 2004.
		2. Roux V, Rydkina E, Eremeeva M, Raoult D. Citrate synthase gene comparison, a new tool for phylogenetic analysis and its application for the Rickettsiae. Int J Syst Bacteriol 1997; 47:252-61.
	-->
	<!--
		Genericos
	-->
	<xsl:output indent="no" method="text" encoding="iso-8859-1"  />
	<xsl:template match="*">[<xsl:value-of select="name()"/><xsl:apply-templates select="@*"/>]<xsl:apply-templates select="*|text()"/>[/<xsl:value-of select="name()"/>]</xsl:template>
	<xsl:template match="@*"><xsl:value-of select="concat(' ',name(),'=')"/><xsl:value-of select="."/></xsl:template>
	
	
	<!--
		Reference list
	-->
	<xsl:template match="insert-main-tag"/>
	<xsl:template match="ref-list">
		<xsl:variable name="count" select="count(.//ref) + count(.//unknown)"/>
		<xsl:if test="$count &gt;0">
		<xsl:if test="insert-main-tag">[refs]</xsl:if>
		<xsl:apply-templates select="ref"/>		
		<xsl:if test="insert-main-tag">[/refs]</xsl:if>
		</xsl:if>
		<xsl:text>
		</xsl:text>
	</xsl:template>
	
	<!--
		Reference 
	-->
	<xsl:template match="ref">[ref reftype="<xsl:value-of select=".//@citation-type"/>"]<xsl:apply-templates select="originalRef"/><xsl:if test="not(label)">[label]<xsl:value-of select="substring(@id,2)"/>[/label]</xsl:if><xsl:apply-templates select="nlm-citation/*"/>[/ref]
</xsl:template>
	<!--
		Unknown
	-->
	<xsl:template match="ref[@status='unknown']">[ref reftype="book"][text-ref]<xsl:value-of select="normalize-space(citation)"/>[/text-ref] <xsl:value-of select="normalize-space(citation)"/>[/ref]
	
</xsl:template>
	<!-- text-ref -->
	<xsl:template match="originalRef">[text-ref]<xsl:value-of select="."/>[/text-ref] </xsl:template>
	<!-- -->
	<xsl:template match="person-group">[authors role="<xsl:value-of select="@person-group-type"/>"]<xsl:apply-templates select="*"/>[/authors]</xsl:template>
	<xsl:template match="name">[pauthor]<xsl:apply-templates select="*"/>[/pauthor]</xsl:template>
	<xsl:template match="given-names">[fname]<xsl:apply-templates select="*|text()"/>[/fname]</xsl:template>
	<xsl:template match="collab">[cauthor]<xsl:apply-templates select="*|text()"/>[/cauthor]</xsl:template>
	<xsl:template match="*[@citation-type='journal']/article-title">[doctitle]<xsl:apply-templates select="*|text()"/>[/doctitle]</xsl:template>
	<xsl:template match="*[@citation-type='book']/article-title">[chptitle]<xsl:apply-templates select="*|text()"/>[/chptitle]</xsl:template>
	<xsl:template match="year">[date dateiso="<xsl:value-of select="."/>0000"]<xsl:apply-templates select="*|text()"/>[/date]</xsl:template>
	<xsl:template match="volume">[volid]<xsl:apply-templates select="*|text()"/>[/volid]</xsl:template>
	<xsl:template match="fpage">[pages]<xsl:apply-templates select="*|text()"/><xsl:if test="../lpage">-<xsl:value-of select="../lpage"/></xsl:if>[/pages]</xsl:template>
	<xsl:template match="lpage"></xsl:template>
	<xsl:template match="publisher-loc">[publoc]<xsl:apply-templates select="*|text()"/>[/publoc]</xsl:template>
	<xsl:template match="publisher-name">[pubname]<xsl:apply-templates select="*|text()"/>[/pubname]</xsl:template>
</xsl:stylesheet>
