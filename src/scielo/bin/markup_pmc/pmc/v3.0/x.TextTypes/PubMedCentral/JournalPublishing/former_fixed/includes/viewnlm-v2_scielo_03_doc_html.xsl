<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  3. "make-a-piece"                                            -->
	<!-- ============================================================= -->
	<!--  Generalized management of front, body, back, and trailing
      content, presently oeprates for sub-article and response
      exactly as for article. -->
	<!--  Organization of output:
         make-front
         make-body
         make-back
         make-figs-and-tables
         make-end-metadata
         ...then...
         do the same for any contained sub-article/response
-->
	<!-- initial context node is article -->
	<xsl:template name="make-a-piece">
		<!-- variable to be used in div id's to keep them unique -->
		<xsl:variable name="which-piece">
			<xsl:value-of select="concat(local-name(), '-level-', count(ancestor::*))"/>
		</xsl:variable>
		<!-- front matter, in table -->
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-front" class="fm">
			<!-- class is repeated on contained table elements -->
			<xsl:call-template name="nl-1"/>
			<xsl:call-template name="make-front"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<!-- body -->
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-body" class="body">
			<xsl:call-template name="nl-1"/>
			<xsl:call-template name="make-body"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-back" class="bm">
			<!-- class is repeated on contained table elements -->
			<xsl:call-template name="nl-1"/>
			<xsl:call-template name="make-back"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<!-- figures and tables -->
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-figs-and-tables" class="bm">
			<xsl:call-template name="nl-1"/>
			<xsl:call-template name="make-figs-and-tables"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<!-- retrieval metadata, at end -->
		<xsl:call-template name="nl-2"/>
		<div id="{$which-piece}-end-metadata" class="fm">
			<!-- class is repeated on contained table element -->
			<xsl:call-template name="nl-1"/>
			<xsl:call-template name="make-end-metadata"/>
			<xsl:call-template name="nl-1"/>
		</div>
		<!-- sub-article or response: calls this very template -->
		<!-- change context node -->
		<!--
  <xsl:for-each select="sub-article | response">
    <xsl:call-template name="make-a-piece"/>
  </xsl:for-each>

  <hr class="part-rule"/>
  <xsl:call-template name="nl-1"/>
  -->
	</xsl:template>
	
	<!-- ============================================================= -->
	<!--  7. MAKE-HTML-HEADER                                          -->
	<!-- ============================================================= -->
	<xsl:template name="make-html-header">
		<head>
			<xsl:call-template name="nl-1"/>
			<title>
				<xsl:choose>
					<xsl:when test="/article/front/journal-meta/journal-id
                        [@journal-id-type='pubmed']">
						<xsl:value-of select="/article/front/journal-meta/journal-id
                                [@journal-id-type='pubmed']"/>
						<xsl:text>: </xsl:text>
					</xsl:when>
					<xsl:when test="/article/front/journal-meta/journal-id
                       [@journal-id-type='publisher']">
						<xsl:value-of select="/article/front/journal-meta/journal-id
                                [@journal-id-type='publisher']"/>
						<xsl:text>: </xsl:text>
					</xsl:when>
					<xsl:when test="/article/front/journal-meta/journal-id">
						<xsl:value-of select="/article/front/journal-meta/journal-id
                                [1][@journal-id-type]"/>
						<xsl:text>: </xsl:text>
					</xsl:when>
					<xsl:otherwise/>
				</xsl:choose>
				<xsl:for-each select="/article/front/article-meta/volume">
					<xsl:text>Vol. </xsl:text>
					<xsl:apply-templates/>
					&#160;<!--xsl:text/-->
				</xsl:for-each>
				<xsl:for-each select="/article/front/article-meta/issue">
					<xsl:text>Issue </xsl:text>
					<xsl:apply-templates/>
					<xsl:text>: </xsl:text>
				</xsl:for-each>
				<xsl:if test="/article/front/article-meta/fpage">
					<xsl:choose>
						<xsl:when test="../lpage">
							<xsl:text>pp. </xsl:text>
							<xsl:value-of select="/article/front/article-meta/fpage"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="/article/front/article-meta/lpage"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:text>p. </xsl:text>
							<xsl:value-of select="/article/front/article-meta/fpage"/>
							&#160;<xsl:text/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:if>
			</title>
			<xsl:call-template name="nl-1"/>
			<link rel="stylesheet" type="text/css" href="ViewNLM.css"/>
			<xsl:call-template name="nl-1"/>
		</head>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  8. MAKE-FRONT                                                -->
	<!-- ============================================================= -->
	<!-- initial context node is /article -->
	<xsl:template name="make-front">
		<xsl:call-template name="nl-1"/>
		<!-- First Table: journal and article metadata -->
		<table width="100%" class="fm">
			<xsl:call-template name="nl-1"/>
			<xsl:call-template name="table-setup-even"/>
			<tr>
				<xsl:call-template name="nl-1"/>
				<!-- Cell 1: journal information -->
				<!-- change context node to front/journal-meta -->
				<xsl:for-each select="front/journal-meta">
					<td valign="top">
						<span class="gen">
							<xsl:text>Journal Information</xsl:text>
						</span>
						<br/>
						<xsl:call-template name="nl-1"/>
						<!-- journal id -->
						<xsl:apply-templates select="journal-id[@journal-id-type]" mode="front"/>
						<!-- abbreviated journal title -->
						<xsl:apply-templates select="abbrev-journal-title" mode="front"/>
						<!-- issn -->
						<xsl:apply-templates select="issn" mode="front"/>
						<!-- publisher -->
						<xsl:apply-templates select="publisher" mode="front"/>
						<!-- journal meta notes -->
						<xsl:apply-templates select="notes" mode="front"/>
					</td>
					<xsl:call-template name="nl-1"/>
					<!-- that's it for journal metadata: return to previous context -->
				</xsl:for-each>
				<!-- Cell 2: Article information -->
				<!-- change context to front/article-meta -->
				<xsl:for-each select="front/article-meta">
					<td valign="top">
						<span class="gen">
							<xsl:text>Article Information</xsl:text>
						</span>
						<br/>
						<xsl:call-template name="nl-1"/>
						<!-- article-level linking -->
						<xsl:apply-templates select="ext-link" mode="front"/>
						<!-- supplementary material -->
						<xsl:apply-templates select="supplementary-material" mode="front"/>
						<!-- self-uri -->
						<xsl:apply-templates select="self-uri" mode="front"/>
						<!-- product information -->
						<xsl:apply-templates select="product" mode="front"/>
						<!-- copyright: show statement -or- year -->
						<!-- Most recent version of DTD recommends using the <permissions> wrapper
               for the copyright data. We handle both cases here. -->
						<xsl:choose>
							<xsl:when test="copyright-statement | permissions/copyright-statement">
								<xsl:apply-templates select="copyright-statement | permissions/copyright-statement" mode="front"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:if test="copyright-year | permissions/copyright-year">
									<span class="gen">
										<xsl:text>Copyright: </xsl:text>
									</span>
									<xsl:apply-templates select="copyright-year | permissions/copyright-year" mode="front"/>
									<xsl:apply-templates select="copyright-holder | permissions/copyright-holder"/>
								</xsl:if>
							</xsl:otherwise>
						</xsl:choose>
						<br/>
						<!-- history/date -->
						<!-- The history element contains one or more date elements -->
						<xsl:apply-templates select="history/date" mode="front"/>
						<!-- pub-date -->
						<xsl:apply-templates select="pub-date" mode="front"/>
						<!-- other publication data -->
						<xsl:apply-templates select="volume
                                     | issue
                                     | elocation-id
                                     | fpage
                                     | lpage" mode="front"/>
						<xsl:apply-templates select="article-id"/>
						<!-- contract information -->
						<xsl:if test="contract-num | contract-sponsor ">
							<xsl:apply-templates select="contract-num" mode="front"/>
							<xsl:apply-templates select="contract-sponsor" mode="front"/>
						</xsl:if>
					</td>
					<xsl:call-template name="nl-1"/>
					<!-- that's it for article-meta; return to previous context -->
				</xsl:for-each>
			</tr>
			<xsl:call-template name="nl-1"/>
			<!-- part-rule ending this table, separating it from the title-and-authors table -->
			<tr>
				<td colspan="2" valign="top">
					<hr class="part-rule"/>
				</td>
			</tr>
			<xsl:call-template name="nl-1"/>
			<!-- end of the first table -->
		</table>
		<xsl:call-template name="nl-1"/>
		<!-- New Table: titles and author group -->
		<!-- All data comes from front/article-meta -->
		<table width="100%" class="fm">
			<xsl:call-template name="table-setup-l-wide"/>
			<!-- change context to front/article-meta (again) -->
			<xsl:for-each select="front/article-meta">
				<tr>
					<!-- table 2 row 2: article titles -->
					<td colspan="2" valign="top">
						<xsl:apply-templates select="title-group" mode="front"/>
					</td>
				</tr>
				<xsl:call-template name="nl-1"/>
				<!-- each contrib makes a row: name at left, details at right -->
				<xsl:for-each select="contrib-group/contrib">
					<tr>
						<td valign="top" align="right">
							<xsl:choose>
								<xsl:when test="@xlink:href">
									<a>
										<xsl:call-template name="make-href"/>
										<xsl:call-template name="make-id"/>
										<xsl:apply-templates select="name | collab" mode="front"/>
									</a>
								</xsl:when>
								<xsl:otherwise>
									<span class="capture-id">
										<xsl:call-template name="make-id"/>
										<xsl:apply-templates select="name | collab" mode="front"/>
									</span>
								</xsl:otherwise>
							</xsl:choose>
						</td>
						<td valign="top">
							<!-- the name element handles any contrib/xref and contrib/degrees -->
							<xsl:apply-templates select="*[not(self::name)
                                       and not(self::collab)
                                       and not(self::xref)
                                       and not(self::degrees)]" mode="front"/>
							<xsl:call-template name="nl-1"/>
						</td>
					</tr>
					<xsl:call-template name="nl-1"/>
				</xsl:for-each>
				<!-- end of contrib -->
				<!-- each aff that is NOT directly inside a contrib
           also makes a row: empty left, details at right -->
				<xsl:for-each select="aff | contrib-group/aff">
					<tr>
						<td/>
						<!-- empty cell -->
						<td valign="top">
							<xsl:apply-templates select="self::aff" mode="aff-outside-contrib"/>
						</td>
					</tr>
					<xsl:call-template name="nl-1"/>
				</xsl:for-each>
				<!-- author notes -->
				<xsl:if test="author-notes">
					<tr>
						<td/>
						<td valign="top">
							<xsl:apply-templates select="author-notes" mode="front"/>
						</td>
					</tr>
					<xsl:call-template name="nl-1"/>
				</xsl:if>
				<!-- abstract(s) -->
				<xsl:if test="abstract | trans-abstract">
					<!-- rule separates title+authors from abstract(s) -->
					<tr>
						<td colspan="2" valign="top">
							<hr class="section-rule"/>
						</td>
					</tr>
					<xsl:call-template name="nl-1"/>
					<xsl:for-each select="abstract | trans-abstract">
						<!-- title in left column, content (paras, secs) in right -->
						<tr>
							<td valign="top">
								<span class="tl-main-part">
									<!-- if there's no title, create one -->
									<xsl:call-template name="words-for-abstract-title"/>
								</span>
							</td>
							<xsl:call-template name="nl-1"/>
							<td valign="top">
								<xsl:apply-templates select="*[not(self::title)]"/>
							</td>
							<xsl:call-template name="nl-1"/>
						</tr>
						<xsl:call-template name="nl-1"/>
					</xsl:for-each>
					<!-- end of abstract or trans-abstract -->
				</xsl:if>
				<!-- end of dealing with abstracts -->
				<!-- end of the titles-and-authors context; return to previous context -->
			</xsl:for-each>
		</table>
		<xsl:call-template name="nl-2"/>
		<!-- end of big front-matter pull -->
	</xsl:template>
	<!-- ============================================================= -->
	<!--  9. MAKE-BODY                                                 -->
	<!-- ============================================================= -->
	<!-- initial context node is article -->
	<xsl:template name="make-body">
		<!-- change context node -->
		<xsl:for-each select="body">
			<xsl:call-template name="nl-1"/>
			<hr class="part-rule"/>
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates/>
			<xsl:call-template name="nl-1"/>
		</xsl:for-each>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  10. MAKE-BACK                                                -->
	<!-- ============================================================= -->
	<!-- initial context node is article -->
	<xsl:template name="make-back">
		<xsl:call-template name="nl-1"/>
		<hr class="part-rule"/>
		<!-- change context node to back -->
		<xsl:for-each select="back">
			<xsl:apply-templates select="title"/>
			<xsl:if test="preceding-sibling::body//fn-group | .//fn-group">
				<span class="tl-main-part">Notes</span>
				<xsl:apply-templates select="preceding-sibling::body//fn-group | .//fn-group"/>
				<xsl:call-template name="nl-1"/>
			</xsl:if>
			<xsl:apply-templates select="*[not(self::title) and not(self::fn-group)]"/>
			<xsl:call-template name="nl-1"/>
		</xsl:for-each>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  11. MAKE-POST-PUBLICATION                                    -->
	<!-- ============================================================= -->
	<!-- At present the transform does not support
     subarticles and responses. To include that
     support in the present structure, fill out
     this template, call the "make-a-piece"
     template to ensure the details are handled
     in the same way and by the same templates
     as for the main article body. -->
	<!-- ============================================================= -->
	<!--  12. MAKE-END-METADATA                                        -->
	<!-- ============================================================= -->
	<!-- This metadata is displayed after the back and figs-and-tables
     because (when it it exists) it will be too long to display
     with the other metadata that is displayed before the body.    -->
	<!-- It is metadata for retrieval: categories, keywords, etc.      -->
	<!-- The context node when this template is called is the article
     or, when supported, the sub-article or response.              -->
	<xsl:template name="make-end-metadata">
		<!-- change context node -->
		<xsl:for-each select="front/article-meta">
			<xsl:if test="article-categories
                | kwd-group
                | related-article
                | conference">
				<hr class="part-rule"/>
				<table width="100%" class="fm">
					<xsl:call-template name="table-setup-l-wide"/>
					<xsl:call-template name="nl-1"/>
					<tr>
						<xsl:call-template name="nl-1"/>
						<td colspan="2" valign="top">
							<!-- hierarchical subjects -->
							<xsl:apply-templates select="article-categories"/>
							<br/>
							<!-- keyword group -->
							<xsl:apply-templates select="kwd-group"/>
							<!-- related article -->
							<xsl:apply-templates select="related-article"/>
							<!-- conference information -->
							<xsl:apply-templates select="conference"/>
						</td>
						<xsl:call-template name="nl-1"/>
					</tr>
					<xsl:call-template name="nl-1"/>
				</table>
				<xsl:call-template name="nl-1"/>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
	
	</xsl:transform>
