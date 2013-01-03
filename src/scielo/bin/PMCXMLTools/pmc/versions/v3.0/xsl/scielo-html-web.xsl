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
	<xsl:param name="css" select="'css/jpub-preview-scielo-web.css'"/>
	<xsl:param name="path_img" />
	<xsl:param name="img_format" select="'.jpg'"/>


	<xsl:template match="/">
		<html>
			<xsl:call-template name="make-html-header"/>
			<body>
				<xsl:apply-templates/>
			</body>
		</html>
	</xsl:template>
  
	<xsl:template match="article">
		<xsl:call-template name="make-article"/>
		<xsl:call-template name="make_miniatures"/>
		<xsl:call-template name="js"/>
	</xsl:template>

	<xsl:template match="trans-title-group/trans-title" mode="metadata">
		<xsl:apply-templates/>
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
        <xsl:if test="aff | author-notes">
              <div class="metadata-group">

                <xsl:apply-templates mode="metadata" select="aff | author-notes"/>
              </div>
        </xsl:if>
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
			<div class="main-title">
				<div class="sec_title">
				<xsl:variable name="name_anchor">
					<xsl:choose>
						<xsl:when test="title"><xsl:value-of select="title"/></xsl:when>
						<xsl:when test="@xml:lang='pt'">RESUMO</xsl:when>
						<xsl:when test="@xml:lang='es'">RESUMÉN</xsl:when>
						<xsl:otherwise>ABSTRACT</xsl:otherwise>
					</xsl:choose> 
				</xsl:variable>
				<a name="nav_id_{$name_anchor}" id="nav_id_{$name_anchor}"/>
				<h2>
					<xsl:value-of select="$name_anchor"/>
				</h2>
				</div>
				<xsl:call-template name="section_nav"/>
			</div>
			
			<xsl:apply-templates select="*[not(self::title)]"/>
	  
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
	  <div class="metadata-group" style="margin-top: 3em; font-weight: bold; font-size: 10pt">
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
		<a href="{concat($path_img,@xlink:href)}.jpg" title="{../label}" class="thickbox">
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
	
  
	<xsl:template match="xref">
		<a href="#{@rid}"  data-tooltip="t{@rid}" class="anchorLink">
		  <xsl:apply-templates/>
		</a>
	</xsl:template>
	
	<xsl:template name="named-anchor">
		<!-- generates an HTML named anchor, using
			 the source ID when found, otherwise a unique ID -->
		<xsl:variable name="id">
		  <xsl:value-of select="@id"/>
		  <xsl:if test="not(normalize-space(@id))">
			<xsl:value-of select="generate-id(.)"/>
		  </xsl:if>
		</xsl:variable>
		<a name="{$id}" id="{$id}">
		  <xsl:comment> named anchor </xsl:comment>
		</a>
	</xsl:template>
	<xsl:template name="assign-src">
		<xsl:for-each select="@xlink:href">
		  <xsl:attribute name="src">
			<xsl:value-of select="concat($path_img,.,$img_format)"/>
		  </xsl:attribute>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template name="main-title"
				  match="body/*/title |
	              back/title | back[not(title)]/*/title">
		<xsl:param name="contents">
			<xsl:apply-templates/>
		</xsl:param>
		<xsl:if test="normalize-space($contents)">
		  <!-- coding defensively since empty titles make glitchy HTML -->
			<div class="main-title">
			  <div class="sec_title">
				<a name="nav_{$contents}" id="nav_{$contents}"></a>
				<h2>
					<xsl:copy-of select="$contents"/>
				</h2>
			  </div>
			  <xsl:call-template name="section_nav"/>
			</div>
		</xsl:if>
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
	
	
	<!---
	*************************************************
	Templates para aplicar o efeito do script TOOLTIP
	*************************************************
	-->
	<xsl:template name="metadata-labeled-entry"/>
	
	<xsl:template name="make_miniatures">
	  <div  id="mystickytooltip" class="stickytooltip">
		<div style="padding:5px">
			<xsl:apply-templates select="*" mode="tooltip"/>
			<xsl:apply-templates select="*"	mode="tooltip_fn"/>
		</div>
	  <!--Mensagem de instrução,status da miniatura.-->
	   <div class="stickystatus"/>
	  </div>
	</xsl:template>
	
	
	<xsl:template match="*" mode="tooltip">
		<xsl:apply-templates mode="tooltip"/>
	</xsl:template>
	<xsl:template match="text()" mode="tooltip"/>
	
	<xsl:template match="*" mode="tooltip_fn">
		<xsl:apply-templates mode="tooltip_fn"/>
	</xsl:template>
	<xsl:template match="text()" mode="tooltip_fn"/>
	
	<xsl:template match="fn" mode="tooltip_fn">
		<div class="atip" id="t{@id}" style="width: 250px">
		  <xsl:apply-templates/>
		</div>
	</xsl:template>
	
	<xsl:template match="fig | table-wrap | ref | aff" mode="tooltip">
	  <xsl:call-template name="miniature">
		  <xsl:with-param name="width_t">
			<xsl:choose>
			  <xsl:when test="name() = 'ref' or name() = 'aff'">350</xsl:when>
			  <xsl:when test="name() = 'fig' or name() = 'table-wrap'">500</xsl:when>
			</xsl:choose>
		  </xsl:with-param>
	  </xsl:call-template>
	</xsl:template>
	
	
	
	<!--
	******************
	Qualquer link que represente uma referência cruzada(âncora) pode chamar este template para que ao passar o mouse sobre o link mostre uma miniatura do destino
	Deve ser passado um atributo para definir a largura no parametro "width_t"
	
	Para usar:
	* Ter um template com o mode="tooltip"  para a tag pai
	* Chamar o template: <xsl:call-template name="miniature">
	* Passar o parametro da largura que se pretende ter na miniatura:
		  <xsl:with-param name="width_t">10860168</xsl:stylesheet>
		  O valor passado será a largura colocada em pixels posteriormente
	* Formatar o próximo template com o mode="tooltip_content"
	* Pronto =D
	-->
	<xsl:template name="miniature">
	<xsl:param  name="width_t"/>
	<div class="atip" id="t{@id}" style="width: {normalize-space($width_t)}px">
	  <xsl:choose>
		<xsl:when test="name() = 'ref'">
		  <b><xsl:call-template name="make-label-text"/></b>
		</xsl:when>
		<xsl:when test="name() = 'aff'">
		  <xsl:call-template name="make-label-text"/>
		</xsl:when>
		<xsl:otherwise>
		  <xsl:call-template name="make_label_tooltip"/>
		</xsl:otherwise>
	  </xsl:choose>
	  <xsl:apply-templates mode="tooltip_content"/>
	</div>
	</xsl:template>
	<xsl:template match="label | caption" mode="tooltip_content"/>
	
	
	<xsl:template name="make_label_tooltip">
	<p class="label_tooltip">
	  <b><xsl:call-template name="make-label-text"/></b>
	  <xsl:value-of select=".//caption"/>
	</p>
	</xsl:template>
	
	<xsl:template mode="tooltip_content"
	match="nlm-citation | element-citation | mixed-citation">
	  <xsl:text>&#160;</xsl:text>
	  <xsl:apply-templates select="*"/>
	  <xsl:text>.</xsl:text>
	</xsl:template>
	
	
	<xsl:template match="graphic" mode="tooltip_content">
	<xsl:apply-templates/>
	<a href="{concat($path_img,@xlink:href,$img_format)}">
		<img alt="{@xlink:href}" class="tooltip_img">
		  <xsl:for-each select="alt-text">
			<xsl:attribute name="alt">
			  <xsl:value-of select="normalize-space(.)"/>
			</xsl:attribute>
		  </xsl:for-each>
		  <xsl:call-template name="assign-src"/>
		</img>
	</a>
	</xsl:template>
	
	<xsl:template mode="tooltip_content"
				match="table | thead | tbody | tfoot | col | colgroup | tr | th | td">
	<xsl:copy>
	  <xsl:if test="name() = 'table'">
		<xsl:attribute name="width">98%</xsl:attribute>
	  </xsl:if>
	  <xsl:apply-templates select="@*" mode="table_copy_tooltip"/>
	  <xsl:apply-templates/>
	</xsl:copy>
	</xsl:template>
	
	<xsl:template match="@*" mode="table_copy_tooltip">
	<xsl:copy-of select="."/>
	</xsl:template>
	<xsl:template match="table/@width" mode="table_copy_tooltip"/>
	
	
	<xsl:template match="fn" mode="tooltip_content">
	<div class="footnote">
	  <xsl:apply-templates/>
	</div>
	</xsl:template>
	
	<xsl:template match="supplementary-material" mode="tooltip_body">
	  <xsl:apply-templates select="." mode="label"/>
	  <xsl:apply-templates />
	</xsl:template>
	
	<xsl:template name="js">
	<script type="text/javascript" src="js/jquery.min.js"></script>
	<script type="text/javascript" src="js/stickytooltip.js">
	/***********************************************
	* Sticky Tooltip script- (c) Dynamic Drive DHTML code library (www.dynamicdrive.com)
	* This notice MUST stay intact for legal use
	* Visit Dynamic Drive at http://www.dynamicdrive.com/ for this script and 100s more
	***********************************************/
	</script>
	<script type="text/javascript" src="js/executartooltip.js"></script>
	<script type="text/javascript" src="js/jquery.anchor.js"></script>
	<script type="text/javascript" src="js/thickbox.js"></script>
	<script type="text/javascript" src="js/ddsmoothmenu.js">
	/***********************************************
	* Smooth Navigational Menu- (c) Dynamic Drive DHTML code library (www.dynamicdrive.com)
	* This notice MUST stay intact for legal use
	* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
	***********************************************/
	</script>
	<script type="text/javascript" src="js/ddsmoothmenu-init.js"></script>
	</xsl:template>
	
	<xsl:template name="section_nav">
	<div class="sec_nav">
		  <div  id="smoothmenu1" class="ddsmoothmenu">
			  <xsl:call-template name="anchor_nav"/>
			  <ul>
				<li><a>Go to:</a>
					<ul>
						<xsl:call-template name="itens_nav"/>
					</ul>
				</li>
			  </ul>
		  </div>
	  </div>
	</xsl:template>
	
	<xsl:template name="anchor_nav">
	<a name="nav_id_{normalize-space(.)}" id="nav_id_{normalize-space(.)}"/>
	</xsl:template>
	
	
	<xsl:template name="itens_nav">
		<xsl:for-each select="/article">
			<xsl:for-each select="front//abstract | front//trans-abstract">
				<li><xsl:call-template name="item_nav_abstract"/></li>
			</xsl:for-each>
			<xsl:for-each select="body/*/title |
								  back/title | back[not(title)]/*/title">			  
				<li>
					<a href="#nav_id_{normalize-space(.)}" class="anchorLink">
						<xsl:value-of select="."/>
					</a>
				</li>
			</xsl:for-each>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template name="item_nav_abstract">
		<xsl:variable name="name_anchor">
			<xsl:choose>
				<xsl:when test="title"><xsl:value-of select="title"/></xsl:when>
				<xsl:when test="@xml:lang='pt'">RESUMO</xsl:when>
				<xsl:when test="@xml:lang='es'">RESUMÉN</xsl:when>
				<xsl:otherwise>ABSTRACT</xsl:otherwise>
			</xsl:choose> 
		</xsl:variable>
		<a href="#nav_id_{normalize-space($name_anchor)}" class="anchorLink">
			<xsl:value-of select="$name_anchor"/>
		</a>
	</xsl:template>

</xsl:stylesheet>