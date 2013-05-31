<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="xml" indent="yes" encoding="UTF-8" doctype-public="-//NLM//DTD PubMed 2.4//EN" doctype-system="http://www.ncbi.nlm.nih.gov/entrez/query/static/PubMed.dtd"/>
	<xsl:variable name="doi_prefix" select="//xml_scielo//doi-configuration//doi-prefix"/>
	<xsl:variable name="replaceISSN" select="//xml_scielo//issn-for-pubmed"/>
	
	<xsl:include href="PubMed_from_db.xsl"/>
	<xsl:include href="PubMed_from_xml.xsl"/>
	
	<xsl:template match="xml_scielo">
		<ArticleSet>
			<xsl:choose>
				<xsl:when test="record[class_of_record/occ='h']">
					<xsl:apply-templates select="record[class_of_record/occ='h']"/>
				</xsl:when>
				<xsl:when test=".//reg">
					<xsl:apply-templates select=".//reg" mode="scielo-xml-scielo-xml"/>
				</xsl:when>
			</xsl:choose>
		</ArticleSet>
	</xsl:template>
	
</xsl:stylesheet>
