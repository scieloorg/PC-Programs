<?xml version="1.0"?>
<!DOCTYPE xsl:stylesheet  [
	<!ENTITY nbsp   "&#160;">
	<!ENTITY copy   "&#169;">
	<!ENTITY reg    "&#174;">
	<!ENTITY trade  "&#8482;">
	<!ENTITY mdash  "&#8212;">
	<!ENTITY ldquo  "&#8220;">
	<!ENTITY rdquo  "&#8221;"> 
	<!ENTITY pound  "&#163;">
	<!ENTITY yen    "&#165;">
	<!ENTITY euro   "&#8364;">
]>
<!-- ============================================================= -->
<!--  MODULE:    HTML Preview of Journal Publishing 3.0 XML        -->
<!--  VERSION:   1.0                                               -->
<!--  DATE:      October-December 2008                             -->
<!--                                                               -->
<!-- ============================================================= -->

<!-- ============================================================= -->
<!--  SYSTEM:    NCBI Archiving and Interchange Journal Articles   -->
<!--                                                               -->
<!--  PURPOSE:   Provide an HTML preview of a journal article,     -->
<!--             in a form suitable for reading.                   -->
<!--                                                               -->
<!--  PROCESSOR DEPENDENCIES:                                      -->
<!--             None: standard XSLT 1.0                           -->
<!--             Tested using Saxon 6.5, Tranformiix (Firefox),    -->
<!--               Saxon 9.1.0.3                                   -->
<!--                                                               -->
<!--  COMPONENTS REQUIRED:                                         -->
<!--             1) This stylesheet                                -->
<!--             2) CSS styles defined in jpub-preview.css         -->
<!--                (to be placed with the results)                -->
<!--                                                               -->
<!--  INPUT:     An XML document valid to the                      -->
<!--             Journal Publishing 3.0 DTD.                       -->
<!--             (And note further assumptions and limitations     -->
<!--             below.)                                           -->
<!--                                                               -->
<!--  OUTPUT:    HTML (XHTML if a postprocessor is used)           -->
<!--                                                               -->
<!--  CREATED FOR:                                                 -->
<!--             Digital Archive of Journal Articles               -->
<!--             National Center for Biotechnology Information     -->
<!--                (NCBI)                                         -->
<!--             National Library of Medicine (NLM)                -->
<!--                                                               -->
<!--  CREATED BY:                                                  -->
<!--             Wendell Piez (based on HTML design by             -->
<!--             Kate Hamilton and Debbie Lapeyre, 2004),          -->
<!--             Mulberry Technologies, Inc.                       -->
<!--                                                               -->
<!-- ============================================================= -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  >



	<xsl:import href="jpub/main/jpub3-html.xsl"/>
	<xsl:param name="css" select="'css/jpub-preview-scielo-default.css'"/>
	<xsl:param name="path_img" select="'img/ag/v48n4/'"/>
	<xsl:param name="img_format" select="'.jpg'"/>
 


<!-- ============================================================= -->
<!--  TOP LEVEL                                                    -->
<!-- ============================================================= -->

  <!--
      content model for article:
         (front,body?,back?,floats-group?,(sub-article*|response*))
      
      content model for sub-article:
         ((front|front-stub),body?,back?,floats-group?,
          (sub-article*|response*))
      
      content model for response:
         ((front|front-stub),body?,back?,floats-group?) -->
  
  <xsl:template match="article">
    <xsl:call-template name="make-article"/>
	<xsl:call-template name="author_notes"/>
  </xsl:template>





  <xsl:template match="front | front-stub">
    <!-- First Table: journal and article metadata -->
    <table width="100%" class="metadata two-column">
      <tr>
        <!-- Cell 1: journal information -->
        <xsl:for-each select="journal-meta">
          <!-- content model:
				    (journal-id+, journal-title-group*, issn+, isbn*, publisher?, notes?)
				    -->
          <td>
            <h4 class="generated">
              <xsl:text>Journal Information</xsl:text>
            </h4>
            <div class="metadata-group">
              <xsl:apply-templates mode="metadata"/>
            </div>
          </td>
        </xsl:for-each>

        <!-- Cell 2: Article information -->
        <xsl:for-each select="article-meta | self::front-stub">
          <!-- content model:
				    (article-id*, article-categories?, title-group,
				     (contrib-group | aff)*, 
             author-notes?, pub-date+, volume?, volume-id*,
             volume-series?, issue?, issue-id*, issue-title*,
             issue-sponsor*, issue-part?, isbn*, supplement?, 
             ((fpage, lpage?, page-range?) | elocation-id)?, 
             (email | ext-link | uri | product | 
              supplementary-material)*, 
             history?, permissions?, self-uri*, related-article*, 
             abstract*, trans-abstract*, 
             kwd-group*, funding-group*, conference*, counts?,
             custom-meta-group?)
            
            These are handled as follows:

            In the "Article Information" header cell:
              article-id
              pub-date
              volume
              volume-id
              volume-series
              issue
              issue-id
              issue-title
              issue-sponsor
              issue-part
              isbn
              supplement
              fpage
              lpage
              page-range
              elocation-id
              email
              ext-link
              uri
              product
              history
              permissions
              self-uri
              related-article
              funding-group
              conference

            In the "Article title" cell:
              title-group
              contrib-group
              aff
              author-notes
              abstract
              trans-abstract

            In the metadata footer
              article-categories
              supplementary-material
              kwd-group
              counts
              custom-meta-group

				  -->

          <td>
            <h4 class="generated">
              <xsl:text>Article Information</xsl:text>
            </h4>
            <div class="metadata-group">

              <xsl:apply-templates mode="metadata"
                select="email | ext-link | uri | self-uri"/>

              <xsl:apply-templates mode="metadata" select="product"/>

              <xsl:apply-templates mode="metadata" select="permissions"/>

              <xsl:apply-templates mode="metadata" select="history/date"/>

              <xsl:apply-templates mode="metadata" select="pub-date"/>

              <xsl:call-template name="volume-info">
                <!-- handles volume?, volume-id*, volume-series? -->
              </xsl:call-template>

              <xsl:call-template name="issue-info">
                <!-- handles issue?, issue-id*, issue-title*,
                     issue-sponsor*, issue-part? -->
              </xsl:call-template>

              <xsl:call-template name="page-info">
                <!-- handles (fpage, lpage?, page-range?) -->
              </xsl:call-template>

              <xsl:apply-templates mode="metadata" select="elocation-id"/>

              <xsl:apply-templates mode="metadata" select="isbn"/>

              <xsl:apply-templates mode="metadata"
                select="supplement | related-article | conference"/>

              <xsl:apply-templates mode="metadata" select="article-id"/>

              <xsl:apply-templates mode="metadata" select="funding-group/*">
                <!-- includes (award-group*, funding-statement*,
                     open-access?) -->
              </xsl:apply-templates>
            </div>
          </td>
        </xsl:for-each>
      </tr>
      <tr>
        <td colspan="2">
          <!-- part-rule ending this table, separating it from the
              title-and-authors table -->
          <hr class="part-rule"/>
        </td>
      </tr>
	  </table>
      <!-- change context to front/article-meta (again) -->

      <xsl:for-each select="article-meta | self::front-stub">
	  
        
            <xsl:apply-templates mode="metadata" select="title-group"/>
        
        <xsl:apply-templates mode="metadata" select="contrib-group"/>
        <!-- back in article-meta or front-stub context -->

        <!-- abstract(s) -->
        <xsl:if test="abstract | trans-abstract">
          <!-- rule separates title+authors from abstract(s) -->
          
          <xsl:for-each select="abstract | trans-abstract" >
            <!-- title in left column, content (paras, secs) in right -->

              <!--td style="text-align: right">
                <h4 class="callout-title">
                  <xsl:apply-templates select="title/node()"/>
                  <xsl:if test="not(normalize-space(title))">
                    <span class="generated">
                      <xsl:if test="self::trans-abstract">Translated </xsl:if>
                      <xsl:text>Abstract</xsl:text>
                    </span>
                  </xsl:if>
                </h4>
              </td-->
			<div class="abstracts">
				<h2 class="main-title">
					  <xsl:apply-templates select="title/node()"/>
					  <xsl:if test="not(normalize-space(title))">
							<xsl:choose>
								  <xsl:when test="@xml:lang='pt'">
										<xsl:text>Resumo</xsl:text>
								  </xsl:when>
								  <xsl:when test="@xml:lang='es'">
										<xsl:text>Resumén</xsl:text>
								  </xsl:when>
								  <xsl:otherwise>
										<xsl:text>Abstract</xsl:text>
								  </xsl:otherwise>
							</xsl:choose>
					  </xsl:if>
				</h2>
				<xsl:apply-templates select="*[not(self::title)]"/>
			</div>
	  
	  </xsl:for-each>
      <!-- end of abstract or trans-abstract -->
      </xsl:if>
      <!-- end of dealing with abstracts -->
      </xsl:for-each>
      <xsl:for-each select="notes">
        <tr>
          <td colspan="2">
            <div class="metadata-group">
              <xsl:apply-templates mode="metadata" select="."/>
            </div>
          </td>
        </tr>
      </xsl:for-each>

          <!-- part-rule ending this table, separating it from the
              title-and-authors table -->
          <hr class="part-rule"/>

    <!-- end of big front-matter pull -->
  </xsl:template>
  
 

  
	<xsl:template mode="metadata" match="contrib-group">
      <!-- content model of contrib-group:
        (contrib+, 
        (address | aff | author-comment | bio | email |
        ext-link | on-behalf-of | role | uri | xref)*) -->
      <!-- each contrib makes a row: name at left, details at right -->
	  <div class="metadata-group">
	    <xsl:for-each select="contrib">
			<xsl:if test="position() > 1 and position() != last()"><xsl:text>, </xsl:text></xsl:if>
			<xsl:if test="position() = last()"><xsl:text> and </xsl:text></xsl:if>
	  		<xsl:apply-templates/>
			<xsl:if test="position() = last()"><xsl:text>.</xsl:text></xsl:if>
    	</xsl:for-each>
	  </div>

      <xsl:variable name="misc-contrib-data"
        select="*[not(self::contrib | self::xref)]"/>
      <xsl:if test="$misc-contrib-data">
            <div class="metadata-group">
              <xsl:apply-templates mode="metadata"
                select="$misc-contrib-data"/>
            </div>
      </xsl:if>
  </xsl:template>
	
	<xsl:template match="trans-title-group/trans-title" mode="metadata">
		<p style="margin-top: 2em">
			<xsl:apply-templates/>
		</p>
	</xsl:template>

   <xsl:template name="metadata-area">
		<xsl:param name="label"/>
		<xsl:param name="contents">
		  <xsl:apply-templates/>
		</xsl:param>
		<div class="metadata-area">
		  <xsl:if test="normalize-space($label)">
			<xsl:call-template name="metadata-labeled-entry">
			  <xsl:with-param name="label">
				<xsl:copy-of select="$label"/>
			  </xsl:with-param>
			  <xsl:with-param name="contents"/>
			</xsl:call-template>
		  </xsl:if>
			<xsl:copy-of select="$contents"/>
		</div>
	</xsl:template>
	
  <xsl:template match="graphic">
		<xsl:apply-templates/>
		<a href="{concat($path_img,@xlink:href)}.jpg" title="{../label}" >
			<img alt="{@xlink:href}" class="graphic">
			  <xsl:for-each select="alt-text">
				<xsl:attribute name="alt">
				  <xsl:value-of select="normalize-space(.)"/>
				</xsl:attribute>
			  </xsl:for-each>
			  <xsl:call-template name="assign-src"/>
			</img>
		</a>
  </xsl:template>
  <xsl:template name="make-label-text">
		<xsl:param name="auto" select="false()"/>
		<xsl:param name="warning" select="false()"/>
		<xsl:param name="auto-text"/>
		<!--xsl:choose>
		  <xsl:when test="$auto">
			<span class="generated">
			  <xsl:copy-of select="$auto-text"/>
			</span>
		  </xsl:when>
		  <xsl:otherwise>
			<xsl:apply-templates mode="label-text"
			  select="label | @symbol"/>
		  </xsl:otherwise>
		</xsl:choose-->
		<xsl:apply-templates mode="label-text" select="label | @symbol"/>
	</xsl:template>
		<xsl:template name="metadata-labeled-entry"/>

	
  <xsl:template name="assign-src">
	<xsl:for-each select="@xlink:href">
	  <xsl:attribute name="src">
		<xsl:value-of select="concat($path_img,.,$img_format)"/>
	  </xsl:attribute>
	</xsl:for-each>
  </xsl:template>
  

  
  <xsl:template name="author_notes">
	  <xsl:for-each select=".//article-meta | .//self::front-stub">
		<xsl:if test="aff | author-notes">
		  <div class="metadata-group">
			<xsl:apply-templates mode="metadata" select="aff | author-notes"/>
		  </div>
		</xsl:if>
	  </xsl:for-each>
  </xsl:template>
  
</xsl:stylesheet>