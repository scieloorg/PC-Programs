<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<!-- ============================================================= -->
	<!--  CITATION AND NLM-CITATION                                    -->
	<!-- ============================================================= -->
	<!-- NLM Archiving DTD:
       - citation uses mode nscitation.

     NLM Publishing DTD:
       - nlm-citation uses several modes,
         including book, edited-book, conf, and "none".
-->
	<!-- ============================================================= -->
	<!--  52. BACK MATTER: REF-LIST                                    -->
	<!-- ============================================================= -->
	<xsl:template match="ref-list">
		<xsl:if test="position()>1">
			<hr class="section-rule"/>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="not(title)">
				<span class="tl-main-part">References</span>
				<xsl:call-template name="nl-1"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="title"/>
			</xsl:otherwise>
		</xsl:choose>
		<table width="100%" class="bm">
			<xsl:choose>
				<xsl:when test="ref/label">
					<xsl:call-template name="table-setup-l-wide"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="table-setup-l-narrow"/>
				</xsl:otherwise>
			</xsl:choose>
		</table>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- suppress the ref-list title so it doesn't reappear -->
	<xsl:template match="ref-list/title" mode="nscitation"/>
	<!-- ============================================================= -->
	<!--  53. REF                                                      -->
	<!-- ============================================================= -->
	<!-- each ref is a table row -->
	<xsl:template match="ref">
		<tr>
			<xsl:call-template name="nl-1"/>
			<td id="{@id}" valign="top" align="right">
				<xsl:if test="not(label)">
					<xsl:value-of select="@id"/>
				</xsl:if>
				<xsl:apply-templates select="label"/>
			</td>
			<xsl:call-template name="nl-1"/>
			<td valign="top">
				<xsl:apply-templates select="citation|nlm-citation"/>
			</td>
			<xsl:call-template name="nl-1"/>
		</tr>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- becomes content of table cell, column 1-->
	<xsl:template match="ref/label">
		<xsl:comment>ref/label</xsl:comment>
		<b>
			<i>
				<xsl:apply-templates/>
				<xsl:text>. </xsl:text>
			</i>
		</b>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  54. CITATION (for NLM Archiving DTD)                         -->
	<!-- ============================================================= -->
	<!-- The citation model is mixed-context, so it is processed
     with an apply-templates (as for a paragraph)
       -except-
     if there is no PCDATA (only elements), spacing and punctuation
     also must be supplied = mode nscitation. -->
	<xsl:template match="ref/citation">
		<xsl:choose>
			<xsl:when test="*">
				<xsl:choose>
					<!-- if has no significant text content, presume that
	           punctuation is not supplied in the source XML
	           = transform will supply it. -->
					<xsl:when test="not(text()[normalize-space()])">
						<xsl:comment>* and not(text()[normalize-space()])</xsl:comment>
						<xsl:apply-templates mode="none"/>
					</xsl:when>
					<!-- if have only element content, presume that
	           punctuation not supplied = generate it. -->
					<xsl:otherwise>
						<xsl:comment>* and text()</xsl:comment>
						<xsl:apply-templates mode="none"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<!-- if have only text(), presume that
           punctuation supplied  -->
			<xsl:otherwise>
				<xsl:comment>nscitation</xsl:comment>
				<xsl:apply-templates mode="nscitation"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  55. NLM-CITATION (for NLM Publishing DTD)                    -->
	<!-- ============================================================= -->
	<!-- The nlm-citation model allows only element content, so
     it takes a pull template and adds punctuation. -->
	<!-- Processing of nlm-citation uses several modes, including
     citation, book, edited-book, conf, inconf, and mode "none".   -->
	<!-- Each citation-type is handled in its own template. -->
	<!-- Book or thesis -->
	<xsl:template match="ref/nlm-citation[@citation-type='book']
                   | ref/nlm-citation[@citation-type='thesis']">
		<xsl:variable name="augroupcount" select="count(person-group) + count(collab)"/>
		<xsl:choose>
			<xsl:when test="$augroupcount>1 and
                    person-group[@person-group-type!='author'] and
                    article-title ">
				<xsl:apply-templates select="person-group[@person-group-type='author']" mode="book"/>
				<xsl:apply-templates select="collab" mode="book"/>
				<xsl:apply-templates select="article-title" mode="editedbook"/>
				<xsl:text>In: </xsl:text>
				<xsl:apply-templates select="person-group[@person-group-type='editor']
                                 | person-group[@person-group-type='allauthors']
                                 | person-group[@person-group-type='translator']
                                 | person-group[@person-group-type='transed'] " mode="book"/>
				<xsl:apply-templates select="source" mode="book"/>
				<xsl:apply-templates select="edition" mode="book"/>
				<xsl:apply-templates select="volume" mode="book"/>
				<xsl:apply-templates select="trans-source" mode="book"/>
				<xsl:apply-templates select="publisher-name | publisher-loc" mode="none"/>
				<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
				<xsl:apply-templates select="fpage | lpage" mode="book"/>
			</xsl:when>
			<xsl:when test="person-group[@person-group-type='author'] or
                    person-group[@person-group-type='compiler']">
				<xsl:apply-templates select="person-group[@person-group-type='author']
                                 | person-group[@person-group-type='compiler']" mode="book"/>
				<xsl:apply-templates select="collab" mode="book"/>
				<xsl:apply-templates select="source" mode="book"/>
				<xsl:apply-templates select="edition" mode="book"/>
				<xsl:apply-templates select="person-group[@person-group-type='editor']
                                 | person-group[@person-group-type='translator']
                                 | person-group[@person-group-type='transed'] " mode="book"/>
				<xsl:apply-templates select="volume" mode="book"/>
				<xsl:apply-templates select="trans-source" mode="book"/>
				<xsl:apply-templates select="publisher-name | publisher-loc" mode="none"/>
				<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
				<xsl:apply-templates select="article-title | fpage | lpage" mode="book"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="person-group[@person-group-type='editor']
                                 | person-group[@person-group-type='translator']
                                 | person-group[@person-group-type='transed']
                                 | person-group[@person-group-type='guest-editor']" mode="book"/>
				<xsl:apply-templates select="collab" mode="book"/>
				<xsl:apply-templates select="source" mode="book"/>
				<xsl:apply-templates select="edition" mode="book"/>
				<xsl:apply-templates select="volume" mode="book"/>
				<xsl:apply-templates select="trans-source" mode="book"/>
				<xsl:apply-templates select="publisher-name | publisher-loc" mode="none"/>
				<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
				<xsl:apply-templates select="article-title | fpage | lpage" mode="book"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:call-template name="citation-tag-ends"/>
	</xsl:template>
	<!-- Conference proceedings -->
	<xsl:template match="ref/nlm-citation[@citation-type='confproc']">
		<xsl:variable name="augroupcount" select="count(person-group) + count(collab)"/>
		<xsl:choose>
			<xsl:when test="$augroupcount>1 and person-group[@person-group-type!='author']">
				<xsl:apply-templates select="person-group[@person-group-type='author']" mode="book"/>
				<xsl:apply-templates select="collab"/>
				<xsl:apply-templates select="article-title" mode="inconf"/>
				<xsl:text>In: </xsl:text>
				<xsl:apply-templates select="person-group[@person-group-type='editor']
                                 | person-group[@person-group-type='allauthors']
                                 | person-group[@person-group-type='translator']
                                 | person-group[@person-group-type='transed'] " mode="book"/>
				<xsl:apply-templates select="source" mode="conf"/>
				<xsl:apply-templates select="conf-name | conf-date | conf-loc" mode="conf"/>
				<xsl:apply-templates select="publisher-loc" mode="none"/>
				<xsl:apply-templates select="publisher-name" mode="none"/>
				<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
				<xsl:apply-templates select="fpage | lpage" mode="book"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="person-group" mode="book"/>
				<xsl:apply-templates select="collab" mode="book"/>
				<xsl:apply-templates select="article-title" mode="conf"/>
				<xsl:apply-templates select="source" mode="conf"/>
				<xsl:apply-templates select="conf-name | conf-date | conf-loc" mode="conf"/>
				<xsl:apply-templates select="publisher-loc" mode="none"/>
				<xsl:apply-templates select="publisher-name" mode="none"/>
				<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
				<xsl:apply-templates select="fpage | lpage" mode="book"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:call-template name="citation-tag-ends"/>
	</xsl:template>
	<!-- Government and other reports, other, web, and commun -->
	<xsl:template match="ref/nlm-citation[@citation-type='gov']
                   | ref/nlm-citation[@citation-type='web']
                   | ref/nlm-citation[@citation-type='commun']
                   | ref/nlm-citation[@citation-type='other']">
		<xsl:apply-templates select="person-group" mode="book"/>
		<xsl:apply-templates select="collab"/>
		<xsl:choose>
			<xsl:when test="publisher-loc | publisher-name">
				<xsl:apply-templates select="source" mode="book"/>
				<xsl:choose>
					<xsl:when test="@citation-type='web'">
						<xsl:apply-templates select="edition" mode="none"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates select="edition"/>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:apply-templates select="publisher-loc" mode="none"/>
				<xsl:apply-templates select="publisher-name" mode="none"/>
				<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
				<xsl:apply-templates select="article-title|gov" mode="none"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="article-title|gov" mode="book"/>
				<xsl:apply-templates select="source" mode="book"/>
				<xsl:apply-templates select="edition"/>
				<xsl:apply-templates select="publisher-loc" mode="none"/>
				<xsl:apply-templates select="publisher-name" mode="none"/>
				<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates select="fpage | lpage" mode="book"/>
		<xsl:call-template name="citation-tag-ends"/>
	</xsl:template>
	<!-- Patents  -->
	<xsl:template match="ref/nlm-citation[@citation-type='patent']">
		<xsl:apply-templates select="person-group" mode="book"/>
		<xsl:apply-templates select="collab" mode="book"/>
		<xsl:apply-templates select="article-title | trans-title" mode="none"/>
		<xsl:apply-templates select="source" mode="none"/>
		<xsl:apply-templates select="patent" mode="none"/>
		<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
		<xsl:apply-templates select="fpage | lpage" mode="book"/>
		<xsl:call-template name="citation-tag-ends"/>
	</xsl:template>
	<!-- Discussion  -->
	<xsl:template match="ref/nlm-citation[@citation-type='discussion']">
		<xsl:apply-templates select="person-group" mode="book"/>
		<xsl:apply-templates select="collab"/>
		<xsl:apply-templates select="article-title" mode="editedbook"/>
		<xsl:text>In: </xsl:text>
		<xsl:apply-templates select="source" mode="none"/>
		<xsl:if test="publisher-name | publisher-loc">
			<xsl:text> [</xsl:text>
			<xsl:apply-templates select="publisher-loc" mode="none"/>
			<xsl:value-of select="publisher-name"/>
			<xsl:text>]; </xsl:text>
		</xsl:if>
		<xsl:apply-templates select="year | month | time-stamp | season | access-date" mode="book"/>
		<xsl:apply-templates select="fpage | lpage" mode="book"/>
		<xsl:call-template name="citation-tag-ends"/>
	</xsl:template>
	<!-- If none of the above citation-types applies,
     use mode="none". This generates punctuation. -->
	<!-- (e.g., citation-type="journal"              -->
	<xsl:template match="nlm-citation">
		<xsl:apply-templates select="*[not(self::annotation) and
                                 not(self::edition) and
                                 not(self::lpage) and
                                 not(self::comment)]|text()" mode="none"/>
		<xsl:call-template name="citation-tag-ends"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!-- person-group, mode=book                                       -->
	<!-- ============================================================= -->
	<xsl:template match="person-group" mode="book">
		<xsl:comment>person-group, book</xsl:comment>
		<!-- XX needs fix, value is not a nodeset on the when -->
		<!--
  <xsl:choose>

    <xsl:when test="@person-group-type='editor'
                  | @person-group-type='assignee'
                  | @person-group-type='translator'
                  | @person-group-type='transed'
                  | @person-group-type='guest-editor'
                  | @person-group-type='compiler'
                  | @person-group-type='inventor'
                  | @person-group-type='allauthors'">

      <xsl:call-template name="make-persons-in-mode"/>
      <xsl:call-template name="choose-person-type-string"/>
      <xsl:call-template name="choose-person-group-end-punct"/>

    </xsl:when>

    <xsl:otherwise>
      <xsl:apply-templates mode="book"/>
    </xsl:otherwise>

  </xsl:choose>
-->
		<xsl:call-template name="make-persons-in-mode"/>
		<xsl:call-template name="choose-person-type-string"/>
		<xsl:call-template name="choose-person-group-end-punct"/>
	</xsl:template>
	<!-- if given names aren't all-caps, use book mode -->
	<!-- ============================================================= -->
	<!--  56. Citation subparts (mode "none" separately at end)        -->
	<!-- ============================================================= -->
	<!-- names -->
	<xsl:template match="name" mode="nscitation">
		<xsl:value-of select="surname"/>
		<xsl:text>, </xsl:text>
		<xsl:value-of select="given-names"/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="name" mode="book">
		<xsl:variable name="nodetotal" select="count(../*)"/>
		<xsl:variable name="penult" select="count(../*)-1"/>
		<xsl:variable name="position" select="position()"/>
		<xsl:choose>
			<!-- if given-names -->
			<xsl:when test="given-names">
				<xsl:comment>name, book</xsl:comment>
				<xsl:apply-templates select="surname"/>
				<xsl:text>, </xsl:text>
				<xsl:call-template name="firstnames">
					<xsl:with-param name="nodetotal" select="$nodetotal"/>
					<xsl:with-param name="position" select="$position"/>
					<xsl:with-param name="names" select="given-names"/>
					<xsl:with-param name="pgtype">
						<xsl:choose>
							<xsl:when test="parent::person-group[@person-group-type]">
								<xsl:value-of select="parent::person-group/@person-group-type"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="'author'"/>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:with-param>
				</xsl:call-template>
				<xsl:if test="suffix">
					<xsl:text>, </xsl:text>
					<xsl:apply-templates select="suffix"/>
				</xsl:if>
			</xsl:when>
			<!-- if no given-names -->
			<xsl:otherwise>
				<xsl:comment>name, book, otherwise</xsl:comment>
				<xsl:apply-templates select="surname"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:choose>
			<!-- if have aff -->
			<xsl:when test="following-sibling::aff"/>
			<!-- if don't have aff -->
			<xsl:otherwise>
				<xsl:choose>
					<!-- if part of person-group -->
					<xsl:when test="parent::person-group/@person-group-type">
						<xsl:choose>
							<!-- if author -->
							<xsl:when test="parent::person-group/@person-group-type='author'">
								<xsl:choose>
									<xsl:when test="$nodetotal=$position">. </xsl:when>
									<xsl:when test="$penult=$position">
										<xsl:choose>
											<xsl:when test="following-sibling::etal">, </xsl:when>
											<xsl:otherwise>; </xsl:otherwise>
										</xsl:choose>
									</xsl:when>
									<xsl:otherwise>; </xsl:otherwise>
								</xsl:choose>
							</xsl:when>
							<!-- if not author -->
							<xsl:otherwise>
								<xsl:choose>
									<xsl:when test="$nodetotal=$position"/>
									<xsl:when test="$penult=$position">
										<xsl:choose>
											<xsl:when test="following-sibling::etal">, </xsl:when>
											<xsl:otherwise>; </xsl:otherwise>
										</xsl:choose>
									</xsl:when>
									<xsl:otherwise>; </xsl:otherwise>
								</xsl:choose>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:when>
					<!-- if not part of person-group -->
					<xsl:otherwise>
						<xsl:choose>
							<xsl:when test="$nodetotal=$position">. </xsl:when>
							<xsl:when test="$penult=$position">
								<xsl:choose>
									<xsl:when test="following-sibling::etal">, </xsl:when>
									<xsl:otherwise>; </xsl:otherwise>
								</xsl:choose>
							</xsl:when>
							<xsl:otherwise>; </xsl:otherwise>
						</xsl:choose>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="collab" mode="book">
		<xsl:comment>collab - book</xsl:comment>
		<xsl:apply-templates/>
		<xsl:if test="@collab-type='compilers'">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:if test="@collab-type='assignee'">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="etal" mode="book">
		<xsl:text>et al.</xsl:text>
		<xsl:choose>
			<xsl:when test="parent::person-group/@person-group-type">
				<xsl:choose>
					<xsl:when test="parent::person-group/@person-group-type='author'">
						&#160;<xsl:text/>
					</xsl:when>
					<xsl:otherwise/>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				&#160;<xsl:text/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- affiliations -->
	<xsl:template match="aff" mode="book">
		<xsl:variable name="nodetotal" select="count(../*)"/>
		<xsl:variable name="position" select="position()"/>
		<xsl:text> (</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>)</xsl:text>
		<xsl:choose>
			<xsl:when test="$nodetotal=$position">. </xsl:when>
			<xsl:otherwise>, </xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- publication info -->
	<xsl:template match="article-title" mode="nscitation">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="article-title" mode="book">
		<xsl:apply-templates/>
		<xsl:choose>
			<xsl:when test="../fpage or ../lpage">
				<xsl:text>; </xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="article-title" mode="editedbook">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="article-title" mode="conf">
		<xsl:apply-templates/>
		<xsl:choose>
			<xsl:when test="../conf-name">
				<xsl:text>. </xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>; </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="article-title" mode="inconf">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="source" mode="nscitation">
		<i>
			<xsl:apply-templates/>
		</i>
	</xsl:template>
	<xsl:template match="source" mode="book">
		<xsl:choose>
			<xsl:when test="../trans-source">
				<xsl:apply-templates/>
				<xsl:choose>
					<xsl:when test="../volume | ../edition">
						<xsl:text>. </xsl:text>
					</xsl:when>
					<xsl:otherwise>
						&#160;<xsl:text/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="source" mode="conf">
		<xsl:apply-templates/>
		<xsl:text>; </xsl:text>
	</xsl:template>
	<xsl:template match="trans-source" mode="book">
		<xsl:text> [</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>]. </xsl:text>
	</xsl:template>
	<xsl:template match="volume" mode="nscitation">
		&#160;<xsl:text/>
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="volume | edition" mode="book">
		<xsl:apply-templates/>
		<xsl:if test="@collab-type='compilers'">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:if test="@collab-type='assignee'">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<!-- dates -->
	<xsl:template match="month" mode="nscitation">
		<xsl:apply-templates/>
		<xsl:text>.</xsl:text>
	</xsl:template>
	<xsl:template match="month" mode="book">
		<xsl:variable name="month" select="."/>
		<xsl:choose>
			<xsl:when test="$month='01' or $month='1' or $month='January'">Jan</xsl:when>
			<xsl:when test="$month='02' or $month='2' or $month='February'">Feb</xsl:when>
			<xsl:when test="$month='03' or $month='3' or $month='March'">Mar</xsl:when>
			<xsl:when test="$month='04' or $month='4' or $month='April'">Apr</xsl:when>
			<xsl:when test="$month='05' or $month='5' or $month='May'">May</xsl:when>
			<xsl:when test="$month='06' or $month='6' or $month='June'">Jun</xsl:when>
			<xsl:when test="$month='07' or $month='7' or $month='July'">Jul</xsl:when>
			<xsl:when test="$month='08' or $month='8' or $month='August'">Aug</xsl:when>
			<xsl:when test="$month='09' or $month='9' or $month='September'">Sep</xsl:when>
			<xsl:when test="$month='10' or $month='October'">Oct</xsl:when>
			<xsl:when test="$month='11' or $month='November'">Nov</xsl:when>
			<xsl:when test="$month='12' or $month='December'">Dec</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$month"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="../day">
			&#160;<xsl:text/>
			<xsl:value-of select="../day"/>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="../time-stamp">
				<xsl:text>, </xsl:text>
				<xsl:value-of select="../time-stamp"/>
				&#160;<xsl:text/>
			</xsl:when>
			<xsl:when test="../access-date"/>
			<xsl:otherwise>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="day" mode="nscitation">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="year" mode="nscitation">
		&#160;<xsl:text/>
		<xsl:apply-templates/>
		&#160;<xsl:text/>
	</xsl:template>
	<xsl:template match="year" mode="book">
		<xsl:choose>
			<xsl:when test="../month or ../season or ../access-date">
				<xsl:apply-templates/>
				&#160;<xsl:text/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="time-stamp" mode="nscitation">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="time-stamp" mode="book"/>
	<xsl:template match="access-date" mode="nscitation">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="access-date" mode="book">
		<xsl:text> [</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>]. </xsl:text>
	</xsl:template>
	<xsl:template match="season" mode="book">
		<xsl:apply-templates/>
		<xsl:if test="@collab-type='compilers'">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:if test="@collab-type='assignee'">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<!-- pages -->
	<xsl:template match="fpage" mode="nscitation">
		<xsl:apply-templates/>
		<xsl:if test="../lpage">
			<xsl:text>-</xsl:text>
			<xsl:value-of select="../lpage"/>
		</xsl:if>
		&#160;<xsl:text/>
	</xsl:template>
	<xsl:template match="fpage" mode="book">
		<xsl:text>p. </xsl:text>
		<xsl:apply-templates/>
		<xsl:if test="../lpage">
			<xsl:text>.</xsl:text>
		</xsl:if>
	</xsl:template>
	<xsl:template match="lpage" mode="book">
		<xsl:choose>
			<xsl:when test="../fpage">
				<xsl:text>-</xsl:text>
				<xsl:apply-templates/>
				<xsl:text>.</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
				<xsl:text> p.</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="lpage" mode="nscitation"/>
	<!-- misc stuff -->
	<xsl:template match="pub-id[@pub-id-type='pmid']" mode="nscitation">
		<xsl:variable name="pmid" select="."/>
		<xsl:variable name="href" select="'http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&amp;db=PubMed&amp;dopt=abstract&amp;list_uids='"/>
		<xsl:text> [</xsl:text>
		<a>
			<xsl:attribute name="href"><xsl:value-of select="concat($href,$pmid)"/></xsl:attribute>
			<xsl:attribute name="target"><xsl:text>_new</xsl:text></xsl:attribute>PubMed
  </a>
		<xsl:text>]</xsl:text>
	</xsl:template>
	<xsl:template match="annotation" mode="nscitation">
		<blockquote>
			<xsl:apply-templates/>
		</blockquote>
	</xsl:template>
	<xsl:template match="comment" mode="nscitation">
		<xsl:if test="not(self::node()='.')">
			<br/>
			<small>
				<xsl:apply-templates/>
			</small>
		</xsl:if>
	</xsl:template>
	<xsl:template match="conf-name | conf-date" mode="conf">
		<xsl:apply-templates/>
		<xsl:text>; </xsl:text>
	</xsl:template>
	<xsl:template match="conf-loc" mode="conf">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	
	<!-- ============================================================= -->
	<!-- mode=none                                                     -->
	<!-- ============================================================= -->
	<!-- This mode assumes no punctuation is provided in the XML.
     It is used, among other things, for the citation/ref
     when there is no significant text node inside the ref.        -->
	<xsl:template match="name" mode="none">
		<xsl:value-of select="surname"/>
		<xsl:text>, </xsl:text>
		<xsl:value-of select="given-names"/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="article-title" mode="none">
		<xsl:apply-templates/>
		<xsl:if test="../trans-title">
			<xsl:text>. </xsl:text>
		</xsl:if>
	</xsl:template>
	<xsl:template match="volume" mode="none">
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="edition" mode="none">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	<xsl:template match="supplement" mode="none">
		&#160;<xsl:text/>
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="issue" mode="none">
		<xsl:text>(</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>)</xsl:text>
	</xsl:template>
	<xsl:template match="publisher-loc" mode="none">
		<xsl:apply-templates/>
		<xsl:text>: </xsl:text>
	</xsl:template>
	<xsl:template match="publisher-name" mode="none">
		<xsl:apply-templates/>
		<xsl:text>; </xsl:text>
	</xsl:template>
	<xsl:template match="person-group" mode="none">
		<xsl:comment>person-group, none</xsl:comment>
		<xsl:variable name="gnms" select="string(descendant::given-names)"/>
		<xsl:variable name="GNMS">
			<xsl:call-template name="capitalize">
				<xsl:with-param name="str" select="$gnms"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="$gnms=$GNMS">
				<xsl:apply-templates/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="node()" mode="book"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="collab" mode="none">
		<xsl:apply-templates/>
		<xsl:if test="@collab-type">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="following-sibling::collab">
				<xsl:text>; </xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="collab">
		<xsl:apply-templates/>
		<xsl:if test="@collab-type">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="@collab-type"/>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="following-sibling::collab">
				<xsl:text>; </xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="source" mode="none">
		<xsl:text>&#160;</xsl:text>
		<xsl:apply-templates/>
		<xsl:choose>
			<xsl:when test="../access-date">
				<xsl:if test="../edition">
					<xsl:text> (</xsl:text>
					<xsl:apply-templates select="../edition" mode="plain"/>
					<xsl:text>)</xsl:text>
				</xsl:if>
				<xsl:text>. </xsl:text>
			</xsl:when>
			<xsl:when test="../volume | ../fpage">
				<xsl:if test="../edition">
					<xsl:text> (</xsl:text>
					<xsl:apply-templates select="../edition" mode="plain"/>
					<xsl:text>)</xsl:text>
				</xsl:if>
				<xsl:text>&#160;</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="../edition">
					<xsl:text> (</xsl:text>
					<xsl:apply-templates select="../edition" mode="plain"/>
					<xsl:text>)</xsl:text>
				</xsl:if>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="trans-title" mode="none">
		<xsl:text> [</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>]. </xsl:text>
	</xsl:template>
	<xsl:template match="month" mode="none">
		<xsl:variable name="month" select="."/>
		<xsl:choose>
			<xsl:when test="$month='01' or $month='1' ">Jan</xsl:when>
			<xsl:when test="$month='02' or $month='2' ">Feb</xsl:when>
			<xsl:when test="$month='03' or $month='3' ">Mar</xsl:when>
			<xsl:when test="$month='04' or $month='4' ">Apr</xsl:when>
			<xsl:when test="$month='05' or $month='5' ">May</xsl:when>
			<xsl:when test="$month='06' or $month='6'">Jun</xsl:when>
			<xsl:when test="$month='07' or $month='7'">Jul</xsl:when>
			<xsl:when test="$month='08' or $month='8' ">Aug</xsl:when>
			<xsl:when test="$month='09' or $month='9' ">Sep</xsl:when>
			<xsl:when test="$month='10' ">Oct</xsl:when>
			<xsl:when test="$month='11' ">Nov</xsl:when>
			<xsl:when test="$month='12' ">Dec</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$month"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="../day">
			&#160;<xsl:text/>
			<xsl:value-of select="../day"/>
		</xsl:if>
		<xsl:text>;</xsl:text>
	</xsl:template>
	<xsl:template match="day" mode="none"/>
	<xsl:template match="year" mode="none">
		<xsl:choose>
			<xsl:when test="../month or ../season or ../access-date">
				<xsl:apply-templates mode="none"/>
				&#160;<xsl:text/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates mode="none"/>
				<xsl:if test="../volume or ../issue">
					<xsl:text>;</xsl:text>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="access-date" mode="none">
		<xsl:text> [</xsl:text>
		<xsl:apply-templates/>
		<xsl:text>];</xsl:text>
	</xsl:template>
	<xsl:template match="season" mode="none">
		<xsl:apply-templates/>
		<xsl:text>;</xsl:text>
	</xsl:template>
	<xsl:template match="fpage" mode="none">
		<xsl:variable name="fpgct" select="count(../fpage)"/>
		<xsl:variable name="lpgct" select="count(../lpage)"/>
		<xsl:variable name="hermano" select="name(following-sibling::node())"/>
		<xsl:choose>
			<xsl:when test="preceding-sibling::fpage">
				<xsl:choose>
					<xsl:when test="following-sibling::fpage">
						&#160;<xsl:text/>
						<xsl:apply-templates/>
						<xsl:if test="$hermano='lpage'">
							<xsl:text>&#8211;</xsl:text>
							<xsl:apply-templates select="following-sibling::lpage[1]"/>
						</xsl:if>
						<xsl:text>,</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						&#160;<xsl:text/>
						<xsl:apply-templates/>
						<xsl:if test="$hermano='lpage'">
							<xsl:text>&#8211;</xsl:text>
							<xsl:apply-templates select="following-sibling::lpage[1]"/>
						</xsl:if>
						<xsl:text>.</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>:</xsl:text>
				<xsl:apply-templates/>
				<xsl:choose>
					<xsl:when test="$hermano='lpage'">
						<xsl:text>&#8211;</xsl:text>
						<xsl:apply-templates select="following-sibling::lpage[1]"/>
						<xsl:text>.</xsl:text>
					</xsl:when>
					<xsl:when test="$hermano='fpage'">
						<xsl:text>,</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:text>.</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="lpage" mode="none">
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="gov" mode="none">
		<xsl:choose>
			<xsl:when test="../trans-title">
				<xsl:apply-templates/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="patent" mode="none">
		<xsl:apply-templates/>
		<xsl:text>. </xsl:text>
	</xsl:template>
	</xsl:transform>
