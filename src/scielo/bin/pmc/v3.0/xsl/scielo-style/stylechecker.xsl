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
      <xsl:when test=".//ack">
        <xsl:choose>
          <xsl:when test="contains(.//ack,'0')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'1')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'2')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'3')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'4')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'5')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'6')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'7')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'8')">maybe-has-funding-group</xsl:when>
          <xsl:when test="contains(.//ack,'9')">maybe-has-funding-group</xsl:when>
          <xsl:otherwise></xsl:otherwise>
        </xsl:choose>
        
        </xsl:when>
    </xsl:choose>
  </xsl:variable>
  <xsl:template match="aff">
    <!-- overwrite stylecheck-match-templates.xsl -->
    <xsl:call-template name="ms-stream-id-test"/>
    <xsl:if test="not(institution[@content-type='orgname'])">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">original affiliation check</xsl:with-param>
        <xsl:with-param name="description">identify original affiliation</xsl:with-param>
      </xsl:call-template>
    </xsl:if>
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
    <xsl:apply-templates select="." mode="output"/>
  </xsl:template>
  <xsl:template match="ack">
    <xsl:call-template name="empty-element-check"/>
    <xsl:call-template name="back-element-check"/>
    <xsl:call-template name="ms-stream-id-test"/>
    <xsl:if test="$check_funding='maybe-has-funding-group'">
      <xsl:call-template name="make-error">
        <xsl:with-param name="error-type">funding group check</xsl:with-param>
        <xsl:with-param name="description">It seems there is funding information (contract number) in acknowledgement. Create funding-group in article-meta</xsl:with-param>
        <xsl:with-param name="class">warning</xsl:with-param>
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
