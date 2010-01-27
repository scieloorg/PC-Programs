<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!-- BACK (unmoded templates)                                      -->
	<!-- ============================================================= -->
	<!-- ============================================================= -->
	<!--  38. BACK MATTER: ACKNOWLEDGEMENTS                            -->
	<!-- ============================================================= -->
	<xsl:template match="ack">
		<xsl:call-template name="nl-1"/>
		<xsl:if test="position()>1">
			<hr class="section-rule"/>
		</xsl:if>
		<xsl:call-template name="nl-1"/>
		<div class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:if test="not(title)">
				<span class="tl-main-part">Acknowledgments</span>
				<xsl:call-template name="nl-1"/>
			</xsl:if>
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  39. BACK-MATTER: APPENDIX                                    -->
	<!-- ============================================================= -->
	<xsl:template match="app">
		<xsl:text>&#xA;</xsl:text>
		<xsl:if test="position()>1">
			<hr class="section-rule"/>
		</xsl:if>
		<xsl:call-template name="nl-1"/>
		<div class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
			<xsl:call-template name="nl-1"/>
		</div>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  40. BACK-MATTER: FOOTNOTE-GROUP and FN                       -->
	<!-- ============================================================= -->
	<xsl:template match="fn-group">
		<xsl:call-template name="nl-1"/>
		<xsl:if test="position()>1">
			<hr class="section-rule"/>
		</xsl:if>
		<xsl:call-template name="nl-1"/>
		<xsl:apply-templates/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  Footnote                                                     -->
	<!-- ============================================================= -->
	<!-- symbol or id is displayed by the first para within the fn     -->
	<xsl:template match="fn">
		<div id="{@id}">
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  41. BACK-MATTER: NOTES                                       -->
	<!-- ============================================================= -->
	<xsl:template match="notes">
		<xsl:call-template name="nl-1"/>
		<xsl:if test="position()>1">
			<hr class="section-rule"/>
		</xsl:if>
		<xsl:call-template name="nl-1"/>
		<div class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:if test="not(title)">
				<span class="tl-main-part">Notes</span>
				<xsl:call-template name="nl-1"/>
			</xsl:if>
			<xsl:apply-templates/>
			<xsl:call-template name="nl-1"/>
		</div>
	</xsl:template>
	<xsl:template match="note">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<small>
				<xsl:apply-templates/>
			</small>
		</span>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  42. BACK MATTER: GLOSSARY                                    -->
	<!-- ============================================================= -->
	<xsl:template match="glossary">
		<xsl:call-template name="nl-1"/>
		<xsl:if test="position()>1">
			<hr class="section-rule"/>
		</xsl:if>
		<xsl:call-template name="nl-1"/>
		<div class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:if test="not(title)">
				<span class="tl-main-part">
					<xsl:call-template name="make-id"/>
					<xsl:text>Glossary</xsl:text>
				</span>
				<xsl:call-template name="nl-1"/>
			</xsl:if>
			<xsl:apply-templates/>
		</div>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="gloss-group">
		<xsl:call-template name="nl-1"/>
		<xsl:if test="not(title)">
			<span class="tl-main-part">Glossary</span>
			<xsl:call-template name="nl-1"/>
		</xsl:if>
		<xsl:apply-templates/>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="def-list">
		<xsl:apply-templates select="title"/>
		<xsl:call-template name="nl-1"/>
		<table width="100%" cellpadding="2" class="bm">
			<xsl:call-template name="nl-1"/>
			<xsl:call-template name="table-setup-l-wide"/>
			<xsl:if test="term-head|def-head">
				<tr>
					<td valign="top" align="right">
						<i>
							<xsl:apply-templates select="term-head"/>
						</i>
					</td>
					<td valign="top">
						<i>
							<xsl:apply-templates select="def-head"/>
						</i>
					</td>
				</tr>
				<xsl:call-template name="nl-1"/>
			</xsl:if>
			<xsl:apply-templates select="def-item"/>
			<xsl:call-template name="nl-1"/>
		</table>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="def-item">
		<tr>
			<xsl:call-template name="make-id"/>
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates/>
		</tr>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="term">
		<td valign="top" align="right">
			<xsl:call-template name="make-id"/>
			<b>
				<xsl:apply-templates/>
			</b>
		</td>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="def">
		<td valign="top">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</td>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  43. TARGET OF A REFERENCE                                    -->
	<!-- ============================================================= -->
	<xsl:template match="target">
		<a>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</a>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  44. XREFS                                                    -->
	<!-- ============================================================= -->
	<!-- xref for fn, table-fn, or bibr becomes a superior number -->
	<!-- Displays the @rid, not the element content (if any) -->
	<xsl:template match="xref[@ref-type='fn']
                  | xref[@ref-type='table-fn']
                  | xref[@ref-type='bibr']">
		<span class="xref">
			<xsl:call-template name="make-id"/>
			<sup>
				<!-- if immediately-preceding sibling was an xref, punctuate
           (otherwise assume desired punctuation is in the source).-->
				<xsl:if test="local-name(preceding-sibling::node()[1])='xref'">
					<span class="gen">
						<xsl:text>, </xsl:text>
					</span>
				</xsl:if>
				<a xxtarget="xrefwindow" href="#{@rid}">
					<xsl:value-of select="@rid"/>
				</a>
			</sup>
		</span>
	</xsl:template>
	<xsl:template match="text()[normalize-space(.)='-']">
		<xsl:choose>
			<!-- if a hyphen is the only thing in a text node
         and it's between two xrefs, we conclude that
         it's expressing a range, and we superscript it -->
			<xsl:when test="local-name(following-sibling::node()[1])='xref'
                and local-name(preceding-sibling::node()[1])='xref'">
				<sup>-</sup>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>-</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- In xref of type fig or of type table,
     the element content is the figure/table number
     and typically part of a sentence,
     so -not- a superior number. -->
	<xsl:template match="xref[@ref-type='fig'] | xref[@ref-type='table']">
		<span class="xref">
			<xsl:call-template name="make-id"/>
			<a xtarget="xrefwindow" href="#{@rid}">
				<xsl:value-of select="."/>
			</a>
		</span>
	</xsl:template>
	<!-- default: if none of the above ref-types -->
	<xsl:template match="xref">
		<span class="xref">
			<xsl:call-template name="make-id"/>
			<a xtarget="xrefwindow" href="#{@rid}">
				<xsl:choose>
					<!-- if xref not empty -->
					<xsl:when test="child::node()">
						<xsl:apply-templates/>
					</xsl:when>
					<xsl:otherwise>
						<!-- if empty -->
						<xsl:value-of select="@rid"/>
					</xsl:otherwise>
				</xsl:choose>
			</a>
		</span>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  45. EXTERNAL LINKS                                           -->
	<!-- ============================================================= -->
	<!-- xlink:href attribute makes a link -->
	<xsl:template match="ext-link | uri">
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
	<!-- xlink:href attribute makes a link -->
	<xsl:template match="mailto">
		<xsl:choose>
			<xsl:when test="@xlink:href">
				<a>
					<xsl:call-template name="make-email"/>
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
		</xsl:transform>
