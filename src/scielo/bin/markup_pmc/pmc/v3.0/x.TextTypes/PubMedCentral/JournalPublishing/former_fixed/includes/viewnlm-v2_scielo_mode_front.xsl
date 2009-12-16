<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!-- MODE front                                                    -->
	<!-- ============================================================= -->
	<!--
<xsl:template match="journal-meta/journal-id
                   | journal-meta/journal-title
                   | journal-meta/journal-abbrev-title
                   | journal-meta/publisher"/>
-->
	<!-- ============================================================= -->
	<!--  34) JOURNAL-META (in order of appearance in output)          -->
	<!-- ============================================================= -->
	<!-- journal-id -->
	<xsl:template match="journal-id[@journal-id-type]" mode="front">
		<span class="gen">
			<xsl:text>Journal ID (</xsl:text>
		</span>
		<xsl:value-of select="@journal-id-type"/>
		<span class="gen">
			<xsl:text>): </xsl:text>
		</span>
		<xsl:value-of select="."/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- abbrev-journal-title -->
	<xsl:template match="abbrev-journal-title" mode="front">
		<span class="gen">
			<xsl:text>Journal Abbreviation: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- issn -->
	<xsl:template match="issn" mode="front">
		<span class="gen">
			<xsl:text>ISSN: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- publisher -->
	<!-- required name, optional location -->
	<xsl:template match="publisher" mode="front">
		<xsl:apply-templates mode="front"/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="publisher-name" mode="front">
		<span class="gen">
			<xsl:text>Publisher: </xsl:text>
		</span>
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="publisher-loc" mode="front">
		<!-- if present, follows a publisher-name, so produces a comma -->
		<xsl:text>, </xsl:text>
		<xsl:apply-templates/>
	</xsl:template>
	<!-- notes -->
	<xsl:template match="notes" mode="front">
		<span class="gen">Notes: </span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  35) ARTICLE-META (in order of appearance in output)          -->
	<!-- ============================================================= -->
	<!-- ext-link -->
	<xsl:template match="ext-link" mode="front">
		<span class="gen">
			<xsl:call-template name="make-id"/>
			<xsl:text>Link: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- supplementary-material -->
	<!-- Begins with:
    Object Identifier <object-id>, zero or more
    Label (Of a Figure, Reference, Etc.) <label>, zero or one
    Caption of a Figure, Table, Etc. <caption>, zero or one
    Any combination of:
      All the accessibility elements:
        Alternate Title Text (For a Figure, Etc.) <alt-text>
        Long Description <long-desc>
      All the address linking elements:
        Email Address <email>
        External Link <ext-link>
        Uniform Resource Indicator (URI) <uri>

  Then an ordinary combination of para-level elements

  Ending with:
    Any combination of:
    Attribution <attrib>
    Copyright Statement <copyright-statement>
-->
	<xsl:template match="supplementary-material" mode="front">
		<span class="gen">
			<xsl:text>Supplementary Material:</xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- self-uri -->
	<xsl:template match="self-uri" mode="front">
		<a href="@xlink:href">
			<span class="gen">
				<xsl:text>Self URI: </xsl:text>
			</span>
		</a>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- product -->
	<!-- uses mode="product" within -->
	<xsl:template match="product" mode="front">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<span class="gen">
						<xsl:text>Product Information: </xsl:text>
					</span>
					<xsl:apply-templates mode="product"/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="gen">
					<xsl:text>Product Information: </xsl:text>
				</span>
				<xsl:apply-templates mode="product"/>
			</xsl:otherwise>
		</xsl:choose>
		<br/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- The product element allows a mixed-content model,
     but perhaps sometimes only element nodes will be used.
     Rough test:
       - if the next sibling is another element,
         add a space to make the content somewhat legible. -->
	<xsl:template match="*" mode="product">
		<xsl:apply-templates/>
		<xsl:if test="generate-id(following-sibling::node()[1])
                 =generate-id(following-sibling::*[1])">
			&#160;<xsl:text/>
		</xsl:if>
	</xsl:template>
	<!-- copyright-statement, copyright-year, copyright-holder -->
	<xsl:template match="copyright-statement | copyright-year | copyright-holder" mode="front">
		<xsl:apply-templates/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- history -->
	<xsl:template match="history/date" mode="front">
		<xsl:variable name="the-type">
			<xsl:choose>
				<xsl:when test="@date-type='accepted'">Accepted</xsl:when>
				<xsl:when test="@date-type='received'">Received</xsl:when>
				<xsl:when test="@date-type='rev-request'">Revision Requested</xsl:when>
				<xsl:when test="@date-type='rev-recd'">Revision Received</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="@date-type">
			<span class="gen">
				<xsl:value-of select="$the-type"/>
				&#160;<xsl:text/>
			</span>
		</xsl:if>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- pub-date -->
	<xsl:template match="pub-date" mode="front">
		<xsl:choose>
			<xsl:when test="@pub-type='ppub'">
				<span class="gen">Print </span>
			</xsl:when>
			<xsl:when test="@pub-type='epub'">
				<span class="gen">Electronic </span>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="@pub-type"/>
			</xsl:otherwise>
		</xsl:choose>
		<span class="gen">
			<xsl:text> publication date: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- volume -->
	<xsl:template match="volume" mode="front">
		<span class="gen">
			<xsl:text>Volume: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<xsl:if test="../issue">
			&#160;<xsl:text/>
		</xsl:if>
	</xsl:template>
	<!-- issue -->
	<xsl:template match="issue" mode="front">
		<span class="gen">
			<xsl:text>Issue: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- elocation-id -->
	<xsl:template match="elocation-id" mode="front">
		<span class="gen">
			<xsl:text>E-location ID: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- fpage, lpage -->
	<xsl:template match="fpage" mode="front">
		<span class="gen">
			<xsl:text>First Page: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<xsl:choose>
			<xsl:when test="../lpage">
				&#160;<xsl:text/>
			</xsl:when>
			<xsl:otherwise>
				<br/>
				<xsl:call-template name="nl-1"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="lpage" mode="front">
		<span class="gen">
			<xsl:text>Last Page: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	
	<!-- article-id -->
	<xsl:template match="article-id">
		<xsl:choose>
			<xsl:when test="@pub-id-type='coden'">
				<span class="gen">
					<xsl:text>Coden: </xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='doi'">
				<span class="gen">
					<xsl:text>DOI: </xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='medline'">
				<span class="gen">
					<xsl:text>Medline Id: </xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='pii'">
				<span class="gen">
					<xsl:text>Publisher Item Identifier: </xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='pmid'">
				<span class="gen">
					<xsl:text>PubMed Id: </xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='publisher-id'">
				<span class="gen">
					<xsl:text>Publisher Id: </xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='sici'">
				<span class="gen">
					<xsl:text>Serial Item and Contribution Identifier: </xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='doaj'">
				<span class="gen">
					<xsl:text>Directory of Open Access Journals</xsl:text>
				</span>
			</xsl:when>
			<xsl:when test="@pub-id-type='other'">
				<span class="gen">
					<xsl:text>Article Id: </xsl:text>
				</span>
			</xsl:when>
			<xsl:otherwise>
				<span class="gen">
					<xsl:text>ID: </xsl:text>
				</span>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- contract-num, contract-sponsor -->
	<xsl:template match="contract-num | contract-sponsor" mode="front">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
					<br/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="capture-id">
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</span>
				<br/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  36) TITLE-GROUP                                              -->
	<!-- ============================================================= -->
	<!-- title-group -->
	<!-- Appears only in article-meta -->
	<!-- The fn-group, if any, is output in the "back" of the
     HTML page, together with any other fn-group. -->
	<xsl:template match="title-group" mode="front">
		<span class="tl-document">
			<xsl:apply-templates select="article-title" mode="front"/>
			<xsl:apply-templates select="subtitle" mode="front"/>
			<xsl:apply-templates select="trans-title | alt-title" mode="front"/>
		</span>
	</xsl:template>
	<xsl:template match="article-title" mode="front">
		<xsl:apply-templates/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- subtitle runs in with title -->
	<xsl:template match="subtitle" mode="front">
		<xsl:text>: </xsl:text>
		<xsl:apply-templates/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="trans-title" mode="front">
		<span class="tl-section-level">
			<span class="gen">Translated title: </span>
			<xsl:apply-templates/>
		</span>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="alt-title" mode="front">
		<span class="tl-default">
			<xsl:choose>
				<xsl:when test="@alt-title-type='right-running-head'">
					<span class="gen">Title for RRH: </span>
				</xsl:when>
				<xsl:otherwise>
					<span class="gen">Alternate Title: </span>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates/>
		</span>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  37) PARTS OF CONTRIB                                         -->
	<!-- ============================================================= -->
	<!-- collab -->
	<!-- A mixed-content model; process it as given -->
	<xsl:template match="collab" mode="front">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="capture-id">
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</span>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- name -->
	<!-- uses mode="contrib" within -->
	<xsl:template match="name" mode="front">
		<xsl:apply-templates select="prefix" mode="contrib"/>
		<xsl:apply-templates select="given-names" mode="contrib"/>
		<xsl:apply-templates select="surname" mode="contrib"/>
		<xsl:apply-templates select="suffix" mode="contrib"/>
		<xsl:apply-templates select="../degrees" mode="contrib"/>
		<xsl:apply-templates select="../xref" mode="contrib"/>
	</xsl:template>
	<xsl:template match="prefix | given-names" mode="contrib">
		<xsl:apply-templates/>
		&#160;<xsl:text/>
	</xsl:template>
	<xsl:template match="surname" mode="contrib">
		<xsl:comment>surname,contrib</xsl:comment>
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="suffix" mode="contrib">
		<xsl:text>, </xsl:text>
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="degrees" mode="contrib">
		<xsl:text>, </xsl:text>
		<xsl:apply-templates/>
	</xsl:template>
	<!-- the formatting is sometimes in the source XML,
     e.g., <sup><italic>a</italic></sup> -->
	<xsl:template match="xref[@ref-type='author-notes']" mode="contrib">
		<xsl:choose>
			<xsl:when test="'*'">
				<xsl:apply-templates/>
			</xsl:when>
			<xsl:when test="not(.//italic) and not (.//sup)">
				<sup>
					<i>
						<xsl:apply-templates/>
					</i>
				</sup>
			</xsl:when>
			<xsl:when test="not(.//italic)">
				<i>
					<xsl:apply-templates/>
				</i>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- the formatting is sometimes in the source XML,
     e.g., <sup><italic>a</italic></sup> -->
	<xsl:template match="xref[@ref-type='aff']" mode="contrib">
		<xsl:choose>
			<xsl:when test="'*'">
				<xsl:apply-templates/>
			</xsl:when>
			<xsl:when test="not(.//italic) and not (.//sup)">
				<sup>
					<i>
						<xsl:apply-templates/>
					</i>
				</sup>
			</xsl:when>
			<xsl:when test="not(.//italic)">
				<i>
					<xsl:apply-templates/>
				</i>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- author-comment -->
	<!-- optional title, one-or-more paras -->
	<xsl:template match="author-comment | bio" mode="front">
		<xsl:variable name="the-title">
			<xsl:choose>
				<xsl:when test="title">
					<xsl:apply-templates select="title" mode="front"/>
				</xsl:when>
				<xsl:when test="self::author-comment">
					<xsl:text>Author Comment: </xsl:text>
				</xsl:when>
				<xsl:when test="self::bio">
					<xsl:text>Bio: </xsl:text>
				</xsl:when>
				<!-- no logical otherwise -->
			</xsl:choose>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<xsl:call-template name="make-id"/>
					<xsl:value-of select="$the-title"/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="make-id"/>
				<xsl:value-of select="$the-title"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates select="*[not(self::title)]" mode="front"/>
	</xsl:template>
	<xsl:template match="author-comment/title | bio/title" mode="front">
		<xsl:apply-templates/>
	</xsl:template>
	<!-- author-comment/p and bio/p in HTML give too much vertical
     space for the display situation; so we force them to produce
     only breaks. -->
	<xsl:template match="author-comment/p | bio/p" mode="front">
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- parts of contrib: address -->
	<xsl:template match="address" mode="front">
		<span class="gen">
			<xsl:call-template name="make-id"/>
			<xsl:text>Address: </xsl:text>
		</span>
		<xsl:apply-templates mode="front"/>
		<br/>
	</xsl:template>
	<xsl:template match="institution" mode="front">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="capture-id">
					<xsl:call-template name="make-id"/>
					<xsl:apply-templates/>
				</span>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="following-sibling::*">
			&#160;<xsl:text/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="address/*" mode="front">
		<xsl:apply-templates/>
		<xsl:if test="following-sibling::*">
			&#160;<xsl:text/>
		</xsl:if>
	</xsl:template>
	<!-- aff -->
	<!-- These affs are inside a contrib element -->
	<xsl:template match="aff" mode="front">
		<span class="gen">
			<xsl:call-template name="make-id"/>
			<xsl:text>Affiliation: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- aff -->
	<!-- These affs are NOT inside a contrib element -->
	<xsl:template match="aff" mode="aff-outside-contrib">
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- on-behalf-of -->
	<xsl:template match="on-behalf-of" mode="front">
		<span class="gen">
			<xsl:text>On behalf of: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- role -->
	<xsl:template match="role" mode="front">
		<span class="gen">
			<xsl:text>Role: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- email -->
	<xsl:template match="email" mode="front">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-href"/>
					<span class="gen">
						<xsl:text>Email: </xsl:text>
					</span>
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<span class="gen">
					<xsl:text>Email: </xsl:text>
				</span>
				<xsl:apply-templates/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- author-notes -->
	<xsl:template match="author-notes" mode="front">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates mode="front"/>
		</span>
	</xsl:template>
	<!-- author-notes/title -->
	<xsl:template match="author-notes/title" mode="front">
		<b>
			<xsl:apply-templates/>
		</b>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- author-notes/corresp -->
	<!-- mixed-content; process it as given -->
	<xsl:template match="author-notes/corresp" mode="front">
		<span class="gen">
			<xsl:call-template name="make-id"/>
			<xsl:text>Correspondence: </xsl:text>
		</span>
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- author-notes/fn -->
	<!-- optional label, one or more paras -->
	<!-- unmoded (author-notes only appears in article-meta) -->
	<xsl:template match="author-notes/fn" mode="front">
		<xsl:apply-templates/>
		<br/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- author-notes/fn/label -->
	<xsl:template match="author-notes/fn/label">
		<xsl:apply-templates/>
	</xsl:template>
	<!-- author-notes/fn/p[1] -->
	<xsl:template match="author-notes/fn/p[1]" priority="2">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:choose>
				<xsl:when test="parent::fn/@fn-type='com'">
					<span class="gen">
						<xsl:text>Communicated by footnote: </xsl:text>
					</span>
				</xsl:when>
				<xsl:when test="parent::fn/@fn-type='con'">
					<span class="gen">
						<xsl:text>Contributed by footnote: </xsl:text>
					</span>
				</xsl:when>
				<xsl:when test="parent::fn/@fn-type='cor'">
					<span class="gen">
						<xsl:text>Correspondence: </xsl:text>
					</span>
				</xsl:when>
				<xsl:when test="parent::fn/@fn-type='financial-disclosure'">
					<span class="gen">
						<xsl:text>Financial Disclosure: </xsl:text>
					</span>
				</xsl:when>
				<xsl:when test="parent::fn/@symbol">
					<sup>
						<xsl:value-of select="parent::fn/@symbol"/>
					</sup>
					&#160;<xsl:text/>
				</xsl:when>
				<xsl:when test="@fn-type">
					<xsl:text>[</xsl:text>
					<xsl:value-of select="@fn-type"/>
					<xsl:text>]</xsl:text>
					&#160;<xsl:text/>
				</xsl:when>
				<xsl:otherwise>
					<span class="gen">
						<xsl:text>*</xsl:text>
					</span>
					&#160;<xsl:text/>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates/>
		</span>
	</xsl:template>
	<!-- author-notes/fn/p processed as ordinary unmoded p-->
	<!-- abstract and trans-abstract are handled entirely
     within the make-front template -->
	
	</xsl:transform>
