<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" exclude-result-prefixes="xs math xd"
    version="3.0">


    <xsl:import href="../web/plus/layout.xsl"/>
    <xsl:import href="../web/plus/data.xsl"/>

   
    <xsl:output method="html" indent="yes" />

    <xsl:param name="path_img" select="'/'"/>

    <xsl:variable name="doc" select="."/>
    <xsl:variable name="issue_label">
        <xsl:apply-templates select="document($xml_article)//front/article-meta"
            mode="plus-issue-label"/>
    </xsl:variable>
	<xsl:variable name="xml_article"/>
    <xsl:param name="IMAGE_PATH"><xsl:value-of select="$path_img"/></xsl:param>
    <!--xsl:param name="PATH">/xsl/plus</xsl:param>
    <xsl:param name="PAGE_LANG" select="//ARTICLE/@TEXTLANG"/>
    <xsl:param name="INTERFACE_LANG" select="//CONTROLINFO/LANGUAGE"/>
    <xsl:param name="PID" select="//ARTICLE/@PID"/>
    <xsl:param name="COLLECTION_DOMAIN" select="//CONTROLINFO//SERVER"/-->
    


    <xsl:variable name="SHORT-LINK"/>
    <xsl:variable name="ref" select="//ref"/>

    
    <xsl:variable name="THIS_URL"></xsl:variable>
    <xsl:variable name="THIS_ABSTRACT_URL"></xsl:variable>
    <xsl:variable name="THIS_PDF_URL"></xsl:variable>
    <xsl:variable name="THIS_ARTICLE_URL"></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_STATISTICS"></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_XML"></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_REFERENCES"></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_AUTO_TRANSLATION"></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_SEND_EMAIL"></xsl:variable>
    <xsl:variable name="SERVICE_UBIO"></xsl:variable>
    <xsl:variable name="title_subjects" select="//TITLEGROUP/SUBJECT"/>
    <xsl:variable name="show_ubio" select="//varScieloOrg/show_ubio"/>
    <xsl:variable name="SERVICE_RELATED"><xsl:if test="$show_ubio = '1'">
        <xsl:if test="$title_subjects = 'BIOLOGICAL SCIENCES'">YES</xsl:if></xsl:if>
    </xsl:variable>
    <xsl:variable name="SERVICE_REFERENCE_LINKS"></xsl:variable>
    
    <xsl:variable name="original" select="//article"/>
    <xsl:variable name="trans" select=".//sub-article[@article-type='translation' and @xml:lang=$PAGE_LANG]"/>
    
    
    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="$xml_article">
                <xsl:apply-templates select="document($xml_article)//article" mode="HTML"/>

            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article" mode="HTML"/>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>
</xsl:stylesheet>