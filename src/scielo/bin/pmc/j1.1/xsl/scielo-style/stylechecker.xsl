<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
   	
    <xsl:import href="../nlm-style-5.15/nlm-stylechecker.xsl"/>
    
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
	            <xsl:text>version 1.1 </xsl:text>
				<xsl:text>of the </xsl:text>
				<xsl:text>JATS DTD. </xsl:text>
				<xsl:text>||</xsl:text>
				<xsl:text> The document was tagged with the language attribute value "</xsl:text>
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
    <xsl:template match="related-article">
    </xsl:template>
    <xsl:template match="related-article/@related-article-type">
    </xsl:template>
    <xsl:template match="ext-link[@ext-link-type='clinical-trial']">
         <xsl:call-template name="web-ext-link-check"/>        
         <xsl:call-template name="href-content-check"/>
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
    <xsl:template match="issn">
        <xsl:call-template name="journal-meta-issn-check"/>
        <xsl:choose>
            <xsl:when test="ancestor::product or ancestor::citation or ancestor::element-citation
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
      <!--xsl:if test="not(..//article-id[@pub-id-type='doi'])"><xsl:call-template name="make-error">
                <xsl:with-param name="error-type">DOI check</xsl:with-param>
                <xsl:with-param name="description">article must have DOI</xsl:with-param>

            </xsl:call-template></xsl:if-->
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
      <xsl:param name="context" select="."/> <!-- Will be journal-meta -->
      
      <!-- journal-title is required  in v1 and v1; journal-title-group is required in v3-->
        <xsl:choose>
            <!-- Scanning data does not require a journal-title -->
            <xsl:when test="//processing-instruction('properties')
                         [contains(.,'scanned_data')] or ancestor::issue-admin"/>
            <xsl:otherwise>
              <xsl:choose>
                <xsl:when test="journal-title[normalize-space()] or journal-title-group/journal-title[normalize-space()]">
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
        
      <!-- Check whether issn is present: but only if this is
           a "domain" that requires an issn -->
    <xsl:choose>
      <xsl:when test="//processing-instruction('noissn')"/>
      <!--  <xsl:when test="contains($domains-no-issn, concat('|',/article/front/journal-meta/journal-id[@journal-id-type='pmc'],'|'))"/>  True if not listed in param -->
      <!--  <xsl:when test="contains($domains-no-issn, concat('|',//journal-meta/pmc-abbreviation,'|'))"/>  True if not listed in param: issue-admin.xsd doc --> 
      <!-- manuscripts do not require issn -->
        <xsl:when test="$stream='manuscript' or contains(//processing-instruction('properties'),'manuscript')"/>
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
 
    <xsl:template match="contrib">
        
        <xsl:call-template name="empty-element-check"/>
        
        <xsl:choose>
            <xsl:when test="$stream='manuscript'">
                <xsl:call-template name="ms-contrib-content-test"/>
                <xsl:call-template name="ms-contrib-attribute-test-alt"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="contrib-attribute-checking"/>
            </xsl:otherwise>
        </xsl:choose>
        
        <xsl:call-template name="contrib-author-notes-test"/>
        
        <xsl:call-template name="contrib-content-test"/>
        
        <!--  <xsl:call-template name="xlink-attribute-check"/>  -->
        
        <xsl:apply-templates select="." mode="output"/>
    </xsl:template>
    <xsl:template name="ms-contrib-attribute-test-alt">
        
        <xsl:if test="not(@contrib-type)">
            <xsl:call-template name="make-error">
                <xsl:with-param name="error-type" select="'contrib attribute'"/>
                <xsl:with-param name="description">
                    <xsl:text>&lt;contrib&gt; must contain a contrib-type attribute</xsl:text>
                </xsl:with-param>
                <xsl:with-param name="tg-target" select="'tags.html#el-contrib'"/>
            </xsl:call-template>
        </xsl:if>
        
        <xsl:if test="contains('|author|editor|translator|compiler|',concat('|',@contrib-type,'|'))">
            <xsl:call-template name="make-error">
                <xsl:with-param name="error-type" select="'contrib attribute'"/>
                <xsl:with-param name="description">
                    <xsl:text>contrib-type attribute must be set to either 'author' or 'editor' or 'translator' or 'compiler'</xsl:text>
                </xsl:with-param>
                <xsl:with-param name="tg-target" select="'tags.html#el-contrib'"/>
            </xsl:call-template>
        </xsl:if>
        
        <xsl:if test="@id">
            <xsl:call-template name="make-error">
                <xsl:with-param name="error-type" select="'contrib attribute'"/>
                <xsl:with-param name="description">
                    <xsl:text>&lt;contrib&gt; should not contain an id attribute</xsl:text>
                </xsl:with-param>
                <xsl:with-param name="tg-target" select="'tags.html#el-contrib'"/>
            </xsl:call-template>
        </xsl:if>
        
        <xsl:if test="@rid">
            <xsl:call-template name="make-error">
                <xsl:with-param name="error-type" select="'contrib attribute'"/>
                <xsl:with-param name="description">
                    <xsl:text>&lt;contrib&gt; should not contain an rid attribute</xsl:text>
                </xsl:with-param>
                <xsl:with-param name="tg-target" select="'tags.html#el-contrib'"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <xsl:template match="contrib-id">
        <xsl:call-template name="empty-element-check"/>
        <!--xsl:call-template name="scielo-contrib-id-check"/-->
        <xsl:apply-templates select="." mode="output"/>
    </xsl:template>
    
    <xsl:template match="mml:math">
        
        <xsl:call-template name="ms-stream-id-test"/>
        
        <xsl:call-template name="mathml-desc-text-check"/>
        
        
        <xsl:call-template name="mathml-top-level-el-check"/>
        
        <xsl:if test="@display">
            <xsl:call-template name="mml-attr-value-check">
                <xsl:with-param name="element-name" select="local-name(.)"/>
                <xsl:with-param name="attr-name" select="'display'"/>
                <xsl:with-param name="attr-value" select="concat('|',@display,'|')"/>
                <xsl:with-param name="attr-enumerated-values" select="
                    '|block|inline|'"/>
            </xsl:call-template>
        </xsl:if>
        
        <xsl:apply-templates select="." mode="output"/>
        
    </xsl:template>
    
    <xsl:template match="xref">
        <xsl:choose>
            <xsl:when test="$stream='book'"/>
            <xsl:otherwise>
                <xsl:call-template name="punctuation-in-xref"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:call-template name="xref-check"/>
        <xsl:apply-templates select="." mode="output"/>
    </xsl:template>
    
</xsl:stylesheet>

