<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" exclude-result-prefixes="xs math xd"
    version="3.0">

    <xsl:template match="article-meta" mode="plus-issue-label">
        <xsl:if test="volume and translate(volume, '0', '')!=''">v<xsl:value-of select="volume"
            /></xsl:if>
        <xsl:if test="issue">
            <xsl:choose>
                <xsl:when test="translate(issue, '0', '')=''"><xsl:apply-templates
                        select=".//pub-date[@pub-type='epub']/year"/>nahead</xsl:when>
                <xsl:when test="contains(issue,'Suppl')">
                    <xsl:variable name="n"><xsl:value-of
                            select="normalize-space(substring-before(issue,'Suppl'))"
                        /></xsl:variable>
                    <xsl:variable name="s"><xsl:value-of
                            select="normalize-space(substring-after(issue,'Suppl'))"
                        /></xsl:variable>
                    <xsl:if test="$n!=''">n<xsl:value-of select="$n"/></xsl:if>s<xsl:value-of
                        select="$s"/><xsl:if test="$s=''">0</xsl:if>
                </xsl:when>
                <xsl:otherwise>n<xsl:value-of select="issue"/></xsl:otherwise>
            </xsl:choose>

        </xsl:if>
        <xsl:if test="supplement"><xsl:variable name="s"><xsl:choose>
                    <xsl:when test="contains(supplement, 'Suppl')"><xsl:value-of
                            select="substring-after(supplement,'Suppl')"/></xsl:when>
                    <xsl:otherwise><xsl:value-of select="supplement"/></xsl:otherwise>
                </xsl:choose></xsl:variable>s<xsl:value-of select="$s"/><xsl:if test="$s=''"
                >0</xsl:if>
        </xsl:if>
    </xsl:template>
    <xsl:template match="article-meta" mode="bibstrip">
        <xsl:if test="volume and volume!='00'">vol. <xsl:value-of select="volume"/></xsl:if>
        <xsl:if test="issue">
            <xsl:choose>
                <xsl:when test="translate(.,'0','')=''">
                    <xsl:apply-templates select=".//pub-date[@pub-type='epub']/year"/>
                </xsl:when>
                <xsl:when test="contains(issue,'Suppl')">
                    <xsl:variable name="n"><xsl:value-of
                            select="normalize-space(substring-before(issue,'Suppl'))"
                        /></xsl:variable>
                    <xsl:variable name="s"><xsl:value-of
                            select="normalize-space(substring-after(issue,'Suppl'))"
                        /></xsl:variable>
                    <xsl:if test="$n!=''">n. <xsl:value-of select="$n"/></xsl:if> Suppl
                        <xsl:value-of select="$s"/>
                </xsl:when>
                <xsl:otherwise>n. <xsl:value-of select="issue"/></xsl:otherwise>
            </xsl:choose>

        </xsl:if>
        <xsl:if test="supplement"><xsl:variable name="s"><xsl:choose>
                    <xsl:when test="contains(supplement, 'Suppl')"><xsl:value-of
                            select="substring-after(supplement,'Suppl')"/></xsl:when>
                    <xsl:otherwise><xsl:value-of select="supplement"/></xsl:otherwise>
                </xsl:choose></xsl:variable>Suppl <xsl:value-of select="$s"/>
        </xsl:if>
    </xsl:template>
    <xsl:variable name="DISPLAY_ARTICLE_TITLE">
        <xsl:apply-templates
            select="$doc//front//article-title[@xml:lang=$PAGE_LANG] | $doc//front//subtitle[@xml:lang=$PAGE_LANG]"/>
        <xsl:apply-templates
            select="$doc//front//trans-title-group[@xml:lang=$PAGE_LANG]/trans-title| $doc//front//trans-title-group[@xml:lang=$PAGE_LANG]/trans-subtitle"/>
        <xsl:apply-templates
            select="$doc//front-stub//article-title[@xml:lang=$PAGE_LANG] | $doc//front-stub//subtitle[@xml:lang=$PAGE_LANG]"
        />
    </xsl:variable>
    <xsl:variable name="ARTICLE_TITLE">
        <xsl:apply-templates
            select="$doc//front//article-title[@xml:lang=$PAGE_LANG]//text() | $doc//front//subtitle[@xml:lang=$PAGE_LANG]//text()"/>
        <xsl:apply-templates
            select="$doc//front//trans-title-group[@xml:lang=$PAGE_LANG]/trans-title//text()| $doc//front//trans-title-group[@xml:lang=$PAGE_LANG]/trans-subtitle//text()"/>
        <xsl:apply-templates
            select="$doc//front-stub//article-title[@xml:lang=$PAGE_LANG]//text() | $doc//front-stub//subtitle[@xml:lang=$PAGE_LANG]//text()"
        />
    </xsl:variable>

    <xsl:template match="@*" mode="DATA-DISPLAY">
        <xsl:attribute name="{name()}">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    <xsl:template match="*" mode="DATA-DISPLAY">
        <xsl:apply-templates select="*|text()" mode="DATA-DISPLAY"/>
    </xsl:template>
    <xsl:template match="sup | sub " mode="DATA-DISPLAY">
        <xsl:element name="{name()}">
            <xsl:apply-templates select="@* | *|text()" mode="DATA-DISPLAY"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="italic" mode="DATA-DISPLAY">
        <em>
            <xsl:apply-templates select="@* | *|text()" mode="DATA-DISPLAY"/>
        </em>
    </xsl:template>
    <xsl:template match="bold" mode="DATA-DISPLAY">
        <strong>
            <xsl:apply-templates select="@* | *|text()" mode="DATA-DISPLAY"/>
        </strong>
    </xsl:template>



    <xsl:template match="article" mode="HTML-HEAD-META">
        <meta name="citation_journal_title" content="{.//journal-meta//journal-title}"/>
        <meta name="citation_journal_title_abbrev" content="{.//journal-meta//abbrev-journal-title}"/>
        <meta name="citation_publisher" content="{.//journal-meta//publisher-name}"/>
        <meta name="citation_title" content="{$ARTICLE_TITLE}"/>

        <meta name="citation_date"
            content="{.//article-meta//pub-date[1]//month}/{.//article-meta//pub-date[1]//year}"/>
        <meta name="citation_volume" content="{.//article-meta//volume}"/>
        <meta name="citation_issue" content="{.//article-meta//issue}"/>
        <meta name="citation_issn" content="{.//journal-meta//issn[1]}"/>
        <meta name="citation_doi" content="{.//article-meta//article-id[@pub-id-type='doi']}"/>
        <!-- adicionar links para os parâmetros abaixo -->
        <meta name="citation_abstract_html_url" content="{$THIS_ABSTRACT_URL}"/>
        <meta name="citation_fulltext_html_url" content="{$THIS_URL}"/>
        <meta name="citation_pdf_url" content="{$THIS_PDF_URL}"/>
        <xsl:apply-templates select=".//article-meta//contrib//name" mode="HTML-HEAD-META"/>
        <xsl:apply-templates select=".//article-meta//collab" mode="HTML-HEAD-META"/>

        <meta name="citation_firstpage" content="{.//article-meta//fpage}"/>
        <meta name="citation_lastpage" content="{.//article-meta//lpage}"/>
        <meta name="citation_id" content="{.//article-meta//article-id[@pub-id-type='doi']}"/>

    </xsl:template>
    <xsl:template match="name" mode="HTML-HEAD-META">
        <meta name="citation_author">
            <xsl:attribute name="content">
                <xsl:apply-templates select="name" mode="DATA-DISPLAY"/>
            </xsl:attribute>
        </meta>

    </xsl:template>
    <xsl:template match="collab" mode="HTML-HEAD-META">
        <meta name="citation_author" content="{.//text()}"/>
    </xsl:template>
    <xsl:template match="aff" mode="HTML-HEAD-META">
        <meta name="citation_author_institution" content="{.//text()}"/>
    </xsl:template>
    <xsl:template match="*" mode="DATA-publication-title">
        <xsl:value-of select=".//journal-meta//journal-title"/>
    </xsl:template>
    <xsl:template match="*" mode="DATA-DISPLAY-ISSN">
        <xsl:apply-templates select=".//journal-meta//issn" mode="DATA-DISPLAY"/>
    </xsl:template>

    <xsl:template match="issn" mode="DATA-DISPLAY">
        <p><xsl:choose>
                <xsl:when test="@pub-type='epub'">Online version</xsl:when>
                <xsl:when test="@pub-type='ppub'">Print
                        version</xsl:when><xsl:otherwise><xsl:value-of select="@pub-type"
                    /></xsl:otherwise>
            </xsl:choose> ISSN <xsl:value-of select="."/></p>
    </xsl:template>
    <xsl:template match="*" mode="DATA-issue-label">
        <xsl:value-of select=".//journal-meta//abbrev-journal-title"/>&#160; <xsl:apply-templates
            select=".//article-meta" mode="bibstrip"/>
    </xsl:template>
    <xsl:template match="*" mode="DATA-article-categories">
        <xsl:value-of select=".//article-categories"/>
    </xsl:template>
    <xsl:template match="*" mode="DATA-DISPLAY-article-title">
        <xsl:value-of select="$DISPLAY_ARTICLE_TITLE"/>
    </xsl:template>
    

    <xsl:template match="contrib" mode="DATA-DISPLAY">
        <xsl:apply-templates select=".//name" mode="DATA-DISPLAY"/>
        <xsl:apply-templates select=".//collab" mode="DATA-DISPLAY"/>
    </xsl:template>
    <xsl:template match="name" mode="DATA-DISPLAY"><xsl:apply-templates select="surname"
            /><xsl:apply-templates select="suffix"/>, <xsl:apply-templates select="given-names"
            /><xsl:apply-templates select="prefix"/></xsl:template>
    <xsl:template match="aff" mode="DATA-label">
        <xsl:value-of select="label"/>
    </xsl:template>
    <xsl:template match="aff" mode="DATA-DISPLAY">
        
            
            <xsl:variable name="inst"><xsl:value-of select="normalize-space(institution[@content-type='orgname'])"/></xsl:variable>
            <xsl:variable name="is_full"><xsl:if test="$inst!=''"><xsl:apply-templates select="text()[string-length(normalize-space(.))&gt;=string-length($inst)]" mode="is_full"><xsl:with-param name="inst" select="$inst"></xsl:with-param></xsl:apply-templates></xsl:if></xsl:variable>
            <xsl:comment>is_full:<xsl:value-of select="$is_full"/> _</xsl:comment>
            <xsl:choose>
                <xsl:when test="contains($is_full,'yes')">
                    <xsl:comment>full</xsl:comment>
                    <xsl:apply-templates select="text()[string-length(normalize-space(.))&gt;=string-length($inst)]" mode="full">
                        <xsl:with-param name="inst" select="$inst"></xsl:with-param>
                    </xsl:apply-templates><xsl:apply-templates select="email"></xsl:apply-templates>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:comment>parts</xsl:comment>					
                    <xsl:apply-templates
                        select="text()[normalize-space(.)!='' and normalize-space(.)!=','] | institution | addr-line | country | email"
                        mode="aff-insert-separator"/>					
                </xsl:otherwise>
            </xsl:choose>
        
    </xsl:template>
    <xsl:template match="text()" mode="is_full">
        <xsl:param name="inst"></xsl:param>
        <xsl:if test="$inst!='' and contains(.,$inst)">yes</xsl:if>
    </xsl:template>
    <xsl:template match="*" mode="full"></xsl:template>
    <xsl:template match="text()" mode="full">
        <xsl:param name="inst"></xsl:param>
        <xsl:comment>text():<xsl:value-of select="."/>_</xsl:comment>
        <xsl:comment>$inst:<xsl:value-of select="$inst"/>_</xsl:comment>
        <xsl:comment>contains(.,$inst):<xsl:value-of select="contains(.,$inst)"/>_</xsl:comment>
        <xsl:if test="$inst!='' and contains(.,$inst)"><xsl:value-of select="."/></xsl:if>
        
    </xsl:template>
    
    
    <xsl:template match="aff/* | addr-line/* " mode="aff-insert-separator">
        <xsl:if test="position()!=1">, </xsl:if>
        <xsl:apply-templates select="*|text()[normalize-space(.)!='' and normalize-space(.)!=',']"
            mode="aff-insert-separator"/>
    </xsl:template>
    
    <xsl:template match="aff/text() | addr-line/text()" mode="aff-insert-separator">
        <xsl:variable name="text" select="normalize-space(.)"/>
        <xsl:comment>_ <xsl:value-of select="$text"/>  _</xsl:comment>  
        
        <xsl:if test="position()!=1">, </xsl:if>
        
        <xsl:choose>
            <xsl:when test="substring($text,string-length($text),1)=','">
                <xsl:value-of select="substring($text,1,string-length($text)-1)"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$text"/>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    <xsl:template match="email" mode="aff-insert-separator">
        <xsl:if test="position()!=1">, </xsl:if>
        <a href="mailto:{text()}">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>
    <xsl:template match="permissions" mode="DATA-DISPLAY">
        <p>
            <xsl:apply-templates select=".//license-p" mode="DATA-DISPLAY"/>
        </p>
        <!--TRANSLATE-->
        <a href="{license/@xlink:href}" target="_blank">See license permissions</a>

    </xsl:template>
    <xsl:template match="kwd-group" mode="DATA-DISPLAY-TITLE">
        <xsl:apply-templates select="title"/>
        <xsl:if test="not(.//title)">Key words</xsl:if>
    </xsl:template>
    <xsl:template match="abstract|trans-abstract" mode="DATA-DISPLAY-TITLE">

        <xsl:apply-templates select="title"/>
        <xsl:if test="not(.//title)">Abstract</xsl:if>
        <!-- FIXME -->

    </xsl:template>
    <xsl:template match="ref-list" mode="DATA-DISPLAY-TITLE">

        <xsl:apply-templates select="title"/>
        <xsl:if test="not(.//title)">References</xsl:if>
        <!-- FIXME -->

    </xsl:template>

    <xsl:template match="ack" mode="DATA-DISPLAY-TITLE">

        <xsl:apply-templates select="title"/>
        <xsl:if test="not(.//title)">Acknowledgements</xsl:if>
        <!-- FIXME -->

    </xsl:template>
    <xsl:template match="person-group" mode="DATA-DISPLAY-ref">

        <xsl:apply-templates select="name" mode="DATA-DISPLAY-ref"/>
    </xsl:template>
    <xsl:template match="name" mode="DATA-DISPLAY-ref">
        <xsl:if test="position()!=1">, </xsl:if>
        <xsl:apply-templates select="." mode="DATA-DISPLAY"/>
    </xsl:template>
    <xsl:template match="pub-id" mode="DATA-DISPLAY">
        <xsl:value-of select="@pub-id-type"/>: <xsl:value-of select="."/>
    </xsl:template>
    <xsl:template match="pub-id[@pub-id-type='doi']| comment[contains(.,'doi:')]"
        mode="DATA-DISPLAY"> http://dx.doi.org/<xsl:value-of select="."/>
    </xsl:template>
    <xsl:template match="suffix">
        <xsl:value-of select="concat(' ',.)"/>
    </xsl:template>
    <xsl:template match="prefix">
        <xsl:value-of select="concat(', ',.)"/>
    </xsl:template>
    <xsl:template match="month" mode="HTML-label-en">
        <xsl:choose>
            <xsl:when test="text() = '01' or text() = '1'">January</xsl:when>
            <xsl:when test="text() = '02' or text() = '2'">February</xsl:when>
            <xsl:when test="text() = '03' or text() = '3'">March</xsl:when>
            <xsl:when test="text() = '04' or text() = '4'">April</xsl:when>
            <xsl:when test="text() = '05' or text() = '5'">May</xsl:when>
            <xsl:when test="text() = '06' or text() = '6'">June</xsl:when>
            <xsl:when test="text() = '07' or text() = '7'">July</xsl:when>
            <xsl:when test="text() = '08' or text() = '8'">August</xsl:when>
            <xsl:when test="text() = '09' or text() = '9'">September</xsl:when>
            <xsl:when test="text() = '10'">October</xsl:when>
            <xsl:when test="text() = '11'">November</xsl:when>
            <xsl:when test="text() = '12'">December</xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="month" mode="HTML-label-es">
        <xsl:choose>
            <xsl:when test="text() = '01' or text() = '1'">Enero</xsl:when>
            <xsl:when test="text() = '02' or text() = '2'">Febrero</xsl:when>
            <xsl:when test="text() = '03' or text() = '3'">Marzo</xsl:when>
            <xsl:when test="text() = '04' or text() = '4'">Abril</xsl:when>
            <xsl:when test="text() = '05' or text() = '5'">Mayo</xsl:when>
            <xsl:when test="text() = '06' or text() = '6'">Junio</xsl:when>
            <xsl:when test="text() = '07' or text() = '7'">Julio</xsl:when>
            <xsl:when test="text() = '08' or text() = '8'">Agosto</xsl:when>
            <xsl:when test="text() = '09' or text() = '9'">Septiembre</xsl:when>
            <xsl:when test="text() = '10'">Octubre</xsl:when>
            <xsl:when test="text() = '11'">Noviembre</xsl:when>
            <xsl:when test="text() = '12'">Diciembre</xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="month" mode="HTML-label-pt">
        <xsl:choose>
            <xsl:when test="text() = '01' or text() = '1'">Janeiro</xsl:when>
            <xsl:when test="text() = '02' or text() = '2'">Fevereiro</xsl:when>
            <xsl:when test="text() = '03' or text() = '3'">Março</xsl:when>
            <xsl:when test="text() = '04' or text() = '4'">Abril</xsl:when>
            <xsl:when test="text() = '05' or text() = '5'">Maio</xsl:when>
            <xsl:when test="text() = '06' or text() = '6'">Junho</xsl:when>
            <xsl:when test="text() = '07' or text() = '7'">Julho</xsl:when>
            <xsl:when test="text() = '08' or text() = '8'">Agosto</xsl:when>
            <xsl:when test="text() = '09' or text() = '9'">Setembro</xsl:when>
            <xsl:when test="text() = '10'">Outubro</xsl:when>
            <xsl:when test="text() = '11'">Novembro</xsl:when>
            <xsl:when test="text() = '12'">Dezembro</xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
