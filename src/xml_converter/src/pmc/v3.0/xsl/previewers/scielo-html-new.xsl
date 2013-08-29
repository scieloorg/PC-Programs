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
    <xsl:param name="css" select="''"/>
    <xsl:param name="xml_file" select="''"/>
    
    
    <xsl:variable name="xml_article">
        <xsl:choose>
            <xsl:when test="$xml_file">file://<xsl:value-of select="$xml_file"/></xsl:when>
            <xsl:when test="//TESTE">file://<xsl:value-of select="//TESTE"/></xsl:when>
            <xsl:otherwise>file:///<xsl:value-of
                select="concat(substring-before(.//PATH_HTDOCS,'htdocs'),'bases/xml/',.//filename)"
            /></xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <!--xsl:variable name="xml_article">file://<xsl:value-of
        select="concat(substring-before(.//PATH_HTDOCS,'htdocs'),'bases/xml/',.//filename)"
    /></xsl:variable-->
    <xsl:variable name="doc" select="document($xml_article)"/>
    <xsl:param name="PATH"><xsl:value-of select="$css"/></xsl:param>
    <xsl:param name="PAGE_LANG" select="$doc//article/@xml:lang"/>
    <xsl:param name="INTERFACE_LANG" select="$PAGE_LANG"/>
    <xsl:param name="PID" select="//ARTICLE/@PID"/>
    <xsl:param name="COLLECTION_DOMAIN" select="//CONTROLINFO//SERVER"/>
    

    <xsl:variable name="issue_label">
        <xsl:apply-templates select="$doc//front/article-meta"
            mode="plus-issue-label"/>
    </xsl:variable>

    <xsl:variable name="IMAGE_PATH">
        <xsl:choose>
            <xsl:when test="$path_img"><xsl:value-of select="$path_img"></xsl:value-of></xsl:when>
            <xsl:when test="//PATH_SERIMG and //SIGLUM and //ISSUE">
                <xsl:value-of select="//PATH_SERIMG"/>
                <xsl:value-of select="//SIGLUM"/>/<xsl:value-of select="$issue_label"/>/</xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="//image-path"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>



    <xsl:variable name="SHORT-LINK"/>
    <xsl:variable name="ref" select="$doc//ref"/>


    <xsl:variable name="THIS_URL"><xsl:if test="$COLLECTION_DOMAIN">http://<xsl:value-of select="$COLLECTION_DOMAIN"
            />/scielo.php?script=sci_arttext_plus&amp;pid=<xsl:value-of select="$PID"
            />&amp;lng=<xsl:value-of select="$INTERFACE_LANG"/>&amp;tlng=<xsl:value-of
                select="$PAGE_LANG"/>&amp;nrm=iso</xsl:if></xsl:variable>
    <xsl:variable name="THIS_ABSTRACT_URL"><xsl:if test="$COLLECTION_DOMAIN">http://<xsl:value-of select="$COLLECTION_DOMAIN"
            />/scielo.php?script=sci_abstract&amp;pid=<xsl:value-of select="$PID"
            />&amp;lng=<xsl:value-of select="$INTERFACE_LANG"/>&amp;tlng=<xsl:value-of
            select="$PAGE_LANG"/>&amp;nrm=iso</xsl:if></xsl:variable>
    <xsl:variable name="THIS_PDF_URL"><xsl:if test="$COLLECTION_DOMAIN">http://<xsl:value-of select="$COLLECTION_DOMAIN"
            />/scielo.php?script=sci_pdf&amp;pid=<xsl:value-of select="$PID"/>&amp;lng=<xsl:value-of
            select="$INTERFACE_LANG"/>&amp;tlng=<xsl:value-of select="$PAGE_LANG"
        />&amp;nrm=iso</xsl:if></xsl:variable>
    <xsl:variable name="THIS_ARTICLE_URL"><xsl:if test="$COLLECTION_DOMAIN">http://<xsl:value-of select="$COLLECTION_DOMAIN"
            />/scielo.php?script=sci_arttext&amp;pid=<xsl:value-of select="$PID"
            />&amp;lng=<xsl:value-of select="$INTERFACE_LANG"/>&amp;tlng=<xsl:value-of
            select="$PAGE_LANG"/>&amp;nrm=iso</xsl:if></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_STATISTICS">
        <xsl:if test="$PID!='' and $COLLECTION_DOMAIN!=''"
                >/applications/scielo-org/pages/services/articleRequestGraphicPage.php?pid=<xsl:value-of
                select="$PID"/>&amp;caller=<xsl:value-of select="$COLLECTION_DOMAIN"
                />&amp;lang=<xsl:value-of select="$INTERFACE_LANG"/></xsl:if>
    </xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_XML"><xsl:if test="$PID">/scieloOrg/php/articleXML.php?pid=<xsl:value-of
            select="$PID"/>&amp;lang=<xsl:value-of select="$INTERFACE_LANG"/></xsl:if>
    </xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_REFERENCES"><xsl:if test="$PID">/scieloOrg/php/reference.php?pid=<xsl:value-of
            select="$PID"/>&amp;caller=<xsl:value-of select="$COLLECTION_DOMAIN"
            />&amp;lang=<xsl:value-of select="$INTERFACE_LANG"/></xsl:if></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_AUTO_TRANSLATION"
        ><xsl:if test="$PID">/scieloOrg/php/translate.php?pid=<xsl:value-of select="$PID"/>&amp;caller=<xsl:value-of
            select="$COLLECTION_DOMAIN"/>&amp;lang=<xsl:value-of select="$INTERFACE_LANG"
            />&amp;tlang=<xsl:value-of select="$PAGE_LANG"/>&amp;script=sci_arttext</xsl:if></xsl:variable>
    <xsl:variable name="SERVICE_ARTICLE_SEND_EMAIL"
        ><xsl:if test="$PID">/applications/scielo-org/pages/services/sendMail.php?pid=<xsl:value-of select="$PID"
            />&amp;caller=<xsl:value-of select="$COLLECTION_DOMAIN"/>&amp;lang=<xsl:value-of
            select="$INTERFACE_LANG"/></xsl:if></xsl:variable>
    <xsl:variable name="SERVICE_UBIO"><xsl:if test="$THIS_URL">
        <xsl:value-of select="concat('http://www.ubio.org/tools/linkit.php?url=',$THIS_URL)"/></xsl:if>
    </xsl:variable>
    <xsl:variable name="title_subjects" select="//TITLEGROUP/SUBJECT"/>
    <xsl:variable name="show_ubio" select="//varScieloOrg/show_ubio"/>
    <xsl:variable name="SERVICE_RELATED">
        <xsl:if test="$show_ubio = '1'">
            <xsl:if test="$title_subjects = 'BIOLOGICAL SCIENCES'">YES</xsl:if>
        </xsl:if>
    </xsl:variable>
    <xsl:variable name="SERVICE_REFERENCE_LINKS"><xsl:if test="$PID">/scielo.php?script=sci_nlinks&amp;pid=<xsl:value-of
            select="$PID"/>REFERENCE_ID&amp;lng=<xsl:value-of select="$INTERFACE_LANG"
        /></xsl:if></xsl:variable>

    <xsl:variable name="original" select="$doc//article"/>
    <xsl:variable name="trans"
        select="$doc/sub-article[@article-type='translation' and @xml:lang=$PAGE_LANG]"/>


    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="$doc">
                <xsl:apply-templates select="$doc//article" mode="HTML"/>

            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article" mode="HTML"/>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>
</xsl:stylesheet>
