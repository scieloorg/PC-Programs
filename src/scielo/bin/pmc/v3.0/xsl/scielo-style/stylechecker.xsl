<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">

  <xsl:import href="../nlm-style-4.6.6/nlm-stylechecker.xsl"/>
  <xsl:param name="filename"/>
  <xsl:template match="/">
    <ERR>
      <xsl:processing-instruction name="SC-DETAILS">
        <xsl:if test="$stream != $style">
          <xsl:text>******* ERROR: $style WAS NOT PASSED CORRECTLY *******</xsl:text>
          </xsl:if>
        <xsl:text>Style checking applied for document with the root element "</xsl:text>
        <xsl:value-of select="$document-type"/>
        <xsl:text>"  with version </xsl:text>
        <xsl:value-of select="$stylechecker-version"/>
        <xsl:text> of the SciELO XML StyleChecker. </xsl:text>
        <xsl:text>||</xsl:text>
        <xsl:text>The document is being checked against the SciELO Tagging Guidlines rules for "</xsl:text>
        <xsl:value-of select="$stream"/>
        <xsl:text>" for content tagged using </xsl:text>
        <xsl:choose>
          <xsl:when test="$dtd-version='2'">
            <xsl:text> version 2.3 or earlier </xsl:text>
            </xsl:when>
          <xsl:when test="$dtd-version='3'">
            <xsl:text> version 3.0 </xsl:text>
            </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$dtd-version"/>
            </xsl:otherwise>
          </xsl:choose>
        <xsl:text>of the NLM DTD. </xsl:text>
        <xsl:text>||</xsl:text>
        <xsl:text>The document was tagged with the language attribute value "</xsl:text>
        <xsl:value-of select="$art-lang-att"/>
        <xsl:text>". </xsl:text>
        </xsl:processing-instruction>
      <xsl:processing-instruction name="TITLE">
        <xsl:value-of select="$content-title"/>
        </xsl:processing-instruction>
      <xsl:apply-templates/>
    </ERR>
  </xsl:template>
  <xsl:variable name="check_funding">
    <xsl:choose>
      <xsl:when test=".//funding-group">funding-group</xsl:when>
      <xsl:when test=".//ack">maybe-has-funding-group</xsl:when>
    </xsl:choose>
  </xsl:variable>
  <xsl:template match="aff">
    <!-- overwrite stylecheck-match-templates.xsl -->
    <xsl:call-template name="ms-stream-id-test"/>
    <xsl:if test="not(institution[@content-type='orgname'])">
      <xsl:call-template name="make-error">
        <xsl:with-param name="class">error</xsl:with-param>
        <xsl:with-param name="error-type">aff institution check</xsl:with-param>
        <xsl:with-param name="description">aff must have institution</xsl:with-param>

      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(institution[@content-type='orgdiv1'])">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">aff institution check</xsl:with-param>
        <xsl:with-param name="description">aff must have institution</xsl:with-param>
        
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(addr-line)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">aff addr-line check</xsl:with-param>
        <xsl:with-param name="description">aff should have addr-line, including
          city</xsl:with-param>

      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(country)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">aff country check</xsl:with-param>
        <xsl:with-param name="description">aff must have country</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="normalize-space(translate(text(),',.;-/', '     '))=''">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">full affiliation check</xsl:with-param>
        <xsl:with-param name="description">aff must have full affiliation</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <xsl:template match="ack">
    <xsl:call-template name="empty-element-check"/>
    <xsl:call-template name="back-element-check"/>
    <xsl:call-template name="ms-stream-id-test"/>
    <xsl:if test="$check_funding='maybe-has-funding-group'">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">funding group check</xsl:with-param>
        <xsl:with-param name="description">if there is funding information in acknowledgement,
          create funding-group in article-meta</xsl:with-param>
        <xsl:with-param name="class">warning</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  
  <xsl:template match="ref">
    <xsl:call-template name="ms-stream-id-test"/>
    <xsl:call-template name="empty-element-check"/>
    <xsl:call-template name="ref-check"/>
    <xsl:if test="not(mixed-citation)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">mixed-citation check</xsl:with-param>
        <xsl:with-param name="description">ref must have mixed-citation</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(element-citation)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">element-citation check</xsl:with-param>
        <xsl:with-param name="description">ref must have element-citation</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  
  <xsl:template match="element-citation">
    <xsl:choose>
      <xsl:when test="@publication-type='journal'"></xsl:when>
      <xsl:when test="@publication-type='book'"></xsl:when>      
      <xsl:when test="@publication-type='thesis'"></xsl:when>
      <xsl:when test="@publication-type='patent'"></xsl:when>
      <xsl:when test="@publication-type='report'"></xsl:when>
      <xsl:when test="@publication-type='software'"></xsl:when>
      <xsl:when test="@publication-type='web'"></xsl:when>
      <xsl:when test="@publication-type='conf-proc'"></xsl:when>
      <xsl:otherwise>
        
       <xsl:variable name="expected">
          <xsl:choose>
            <xsl:when test="conf-name">conf-proc</xsl:when>
            <xsl:when test="version">software</xsl:when>
            <xsl:when test="patent">patent</xsl:when>
            <xsl:when test="contains(.//text(),'eport') or contract">report</xsl:when>
            <xsl:when test="chapter or count(.//person-group)&gt;1">book</xsl:when>
            <xsl:when test="article-title and publisher-name">thesis</xsl:when>
            <xsl:when test="article-title">journal</xsl:when>     
            <xsl:when test="date-in-citation">web</xsl:when>
            <xsl:otherwise>one of journal | book | thesis | conf-proc | patent | report | software | web</xsl:otherwise>
          </xsl:choose>  
        </xsl:variable>
        <xsl:call-template name="make-error">
          <xsl:with-param name="class">warning</xsl:with-param>
          <xsl:with-param name="error-type">publication type check</xsl:with-param>
          <xsl:with-param name="description"><xsl:value-of select="@id"/>: invalid <xsl:value-of select="@publication-type"/>. Expected: <xsl:value-of select="$expected"/>" 
            </xsl:with-param>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="." mode="type"></xsl:apply-templates>    
    <xsl:if test="not(year)">
      <xsl:call-template name="make-error">
        <!--xsl:with-param name="class">warning</xsl:with-param-->
        <xsl:with-param name="error-type">year check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have year</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(source)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">source check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have source</xsl:with-param>
      </xsl:call-template>
    </xsl:if>    
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  
  <xsl:template match="element-citation[@publication-type='journal']" mode="type">    
    <xsl:if test="not(article-title)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">article-title check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have article-title</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(article-title/@language)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">article-title/@language check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have article-title/@language</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <xsl:template match="element-citation[@publication-type='thesis']" mode="type">    
    <xsl:if test="not(article-title/@language)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">article-title/@language check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have article-title/@language</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(publisher-name)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">publisher-name check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have publisher-name</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(publisher-loc)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">publisher-loc check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have publisher-loc</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <xsl:template match="element-citation[@publication-type='conf-proc']" mode="type">  
    <xsl:if test="not(article-title/@language)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">article-title/@language check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have article-title/@language</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(conf-name)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">conf-name check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have conf-name</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(conf-num)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">conf-name check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have conf-num</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <xsl:template match="element-citation[@publication-type='web']" mode="type">    
    <xsl:if test="not(uri) or not(ext-link)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">uri or ext-link check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have uri or ext-link</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(date-in-citation[@content-type='access-date'])">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">date-in-citation[@content-type='access-date'] check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have date-in-citation[@content-type='access-date']</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <xsl:template match="element-citation[@publication-type='book']" mode="type"> 
    <xsl:choose>
      <xsl:when test="count(person-group) &lt;=1">
        <!-- book -->
        <xsl:if test="not(source/@language)">
          <xsl:call-template name="make-error">
            <xsl:with-param name="error-type">source/@language check</xsl:with-param>
            <xsl:with-param name="description"><xsl:value-of select="@id"/>: book citation must have source/@language</xsl:with-param>
          </xsl:call-template>
        </xsl:if>    
      </xsl:when>
      <xsl:otherwise>
        <!-- book chapter -->
        <xsl:if test="article-title">
          <xsl:call-template name="make-error">
            <xsl:with-param name="error-type">chapter-title check</xsl:with-param>
            <xsl:with-param name="description"><xsl:value-of select="@id"/>: book citation must have chapter-title instead of article-title</xsl:with-param>
          </xsl:call-template>
        </xsl:if>
        <xsl:if test="not(chapter-title)">
          <xsl:call-template name="make-error">
            <xsl:with-param name="error-type">chapter-title check</xsl:with-param>
            <xsl:with-param name="description"><xsl:value-of select="@id"/>: book citation must have chapter-title</xsl:with-param>
          </xsl:call-template>
        </xsl:if>
        <xsl:if test="chapter-title and not(chapter-title/@language)">
          <xsl:call-template name="make-error">
            <xsl:with-param name="error-type">chapter-title/@language check</xsl:with-param>
            <xsl:with-param name="description"><xsl:value-of select="@id"/>: book citation must have chapter-title/@language</xsl:with-param>
          </xsl:call-template>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="not(publisher-name)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">publisher-name check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have publisher-name</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(publisher-loc)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">publisher-loc check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have publisher-loc</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template> 
  <xsl:template match="element-citation[@publication-type='patent']" mode="type">    
    <xsl:if test="not(patent)">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">patent check</xsl:with-param>
        <xsl:with-param name="description"><xsl:value-of select="@id"/>: must have patent</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <!--
    issn
  -->
  <xsl:template match="issn">
    <xsl:call-template name="journal-meta-issn-check"/>
    <xsl:choose>
      <xsl:when
        test="ancestor::product or ancestor::citation or ancestor::element-citation
                 or ancestor::mixed-citation or ancestor::nlm-citation or $stream='manuscript'">
        <!-- Don't test these -->
      </xsl:when>
      <xsl:otherwise>
        <!-- Test 2 -->
        <xsl:call-template name="pub-type-check">
          <xsl:with-param name="context" select="."/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <xsl:template match="article-id">
    <xsl:call-template name="attribute-present-not-empty">
      <xsl:with-param name="context" select="@pub-id-type"/>
      <xsl:with-param name="attribute-name" select="'pub-id-type'"/>
      <xsl:with-param name="test-name" select="'pub-id-type attribute check'"/>
    </xsl:call-template>
    <xsl:call-template name="pub-id-type-check"/>
    <xsl:call-template name="article-id-content-check"/>
    <xsl:if test="@pub-id-type = 'doi'">
      <xsl:call-template name="doi-check">
        <xsl:with-param name="value" select="."/>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="not(..//article-id[@pub-id-type='doi'])">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">DOI check</xsl:with-param>
        <xsl:with-param name="description">article must have DOI</xsl:with-param>

      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>

  <!-- *********************************************************** -->
  <!-- Template: journal-meta-check 
   
        If article has a journal-meta element, then:
        1) journal-title is required
        2) issn is required
     -->
  <!-- *********************************************************** -->
  <xsl:template name="journal-meta-check">
    <xsl:param name="context" select="."/>
    <!-- Will be journal-meta -->

    <!-- journal-title is required  in v1 and v1; journal-title-group is required in v3-->
    <xsl:choose>
      <!-- Scanning data does not require a journal-title -->
      <xsl:when
        test="//processing-instruction('properties')
                         [contains(.,'scanned_data')] or ancestor::issue-admin"/>
      <xsl:otherwise>
        <xsl:choose>
          <xsl:when
            test="journal-title[normalize-space()] or journal-title-group/journal-title[normalize-space()]">
            <!-- data is okay -->
          </xsl:when>
          <xsl:otherwise>
            <xsl:call-template name="make-error">
              <xsl:with-param name="error-type">journal-meta-check</xsl:with-param>
              <xsl:with-param name="description">
                <xsl:text>journal-title is required</xsl:text>
              </xsl:with-param>
              <xsl:with-param name="tg-target" select="'tags.html#el-jmeta'"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="not(.//abbrev-journal-title[@abbrev-type='publisher'])">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">abbrev title check</xsl:with-param>
        <xsl:with-param name="description">journal must have abbrev title</xsl:with-param>

      </xsl:call-template>
    </xsl:if>
    <!-- Check whether issn is present: but only if this is
           a "domain" that requires an issn -->
    <xsl:choose>
      <xsl:when test="//processing-instruction('noissn')"/>
      <!--  <xsl:when test="contains($domains-no-issn, concat('|',/article/front/journal-meta/journal-id[@journal-id-type='pmc'],'|'))"/>  True if not listed in param -->
      <!--  <xsl:when test="contains($domains-no-issn, concat('|',//journal-meta/pmc-abbreviation,'|'))"/>  True if not listed in param: issue-admin.xsd doc -->
      <!-- manuscripts do not require issn -->
      <xsl:when
        test="$stream='manuscript' or contains(//processing-instruction('properties'),'manuscript')"/>
      <xsl:when test="$stream='rrn' "/>
      <xsl:otherwise>
        <!-- Check that issn is present -->
        <xsl:if test="not(issn[normalize-space()])">
          <xsl:call-template name="make-error">
            <xsl:with-param name="error-type">journal-meta-check</xsl:with-param>
            <xsl:with-param name="description">
              <xsl:text>issn is required</xsl:text>
            </xsl:with-param>
            <xsl:with-param name="tg-target" select="'tags.html#el-jmeta'"/>
          </xsl:call-template>
        </xsl:if>
        <xsl:if test="count(issn) &gt; 1">
          <xsl:if test="issn[0] = issn[1]">
            <xsl:call-template name="make-error">
              <xsl:with-param name="error-type">journal-meta-check</xsl:with-param>
              <xsl:with-param name="description">
                <xsl:text>issn can not have the same value</xsl:text>
              </xsl:with-param>
              <xsl:with-param name="tg-target" select="'tags.html#el-jmeta'"/>
            </xsl:call-template>
          </xsl:if>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>

  </xsl:template>

</xsl:stylesheet>
