<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<!-- ============================================================= -->
	<!--  13. PARAGRAPH WITH ITS SUBTLETIES                            -->
	<!-- ============================================================= -->
	
	<xsl:template match="p">
		<xsl:comment>p</xsl:comment>
		<p>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</p>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- The first p in a footnote displays the fn symbol or,
     if no symbol, the fn ID -->
	<xsl:template match="fn/p[1]">
		<p>
			<xsl:call-template name="make-id"/>
			<xsl:if test="../@symbol | ../@id">
				<sup>
					<xsl:choose>
						<xsl:when test="../@symbol">
							<xsl:value-of select="../@symbol"/>
						</xsl:when>
						<xsl:when test="../@id">
							<xsl:value-of select="../@id"/>
						</xsl:when>
						<xsl:otherwise/>
					</xsl:choose>
				</sup>
			</xsl:if>
			<xsl:apply-templates/>
		</p>
	</xsl:template>
	<xsl:template match="speech/p[1]">
		<p>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates select="preceding-sibling::speaker" mode="show-it-here"/>
			&#160;<xsl:text/>
			<xsl:apply-templates/>
		</p>
	</xsl:template>
	<!-- prevent the first def/p from causing a p tag
     which would display an unwanted break -->
	<xsl:template match="def/p[1]">
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</span>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  14. SECTION                                                  -->
	<!-- ============================================================= -->
	<!-- the first body/sec puts out no rule at its top,
     because body already puts out a part-rule at its top;
     subsequent body/secs do put out a section-rule -->
	<xsl:template match="body/sec">
		<xsl:comment>sec</xsl:comment>
		<xsl:call-template name="nl-1"/>
		<xsl:if test="position()>'1'">
			<hr class="section-rule"/>
			<xsl:call-template name="nl-1"/>
		</xsl:if>
		<div>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</div>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- no other level of sec puts out a rule -->
	<xsl:template match="sec">
		<div>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</div>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  15. LIST and its Internals                                   -->
	<!-- ============================================================= -->
	<xsl:template match="list">
		<xsl:call-template name="nl-1"/>
		<xsl:choose>
			<xsl:when test="@list-type='bullet'">
				<xsl:call-template name="nl-1"/>
				<ul>
					<xsl:call-template name="nl-1"/>
					<xsl:apply-templates/>
					<xsl:call-template name="nl-1"/>
				</ul>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="nl-1"/>
				<ol>
					<xsl:call-template name="nl-1"/>
					<xsl:apply-templates/>
					<xsl:call-template name="nl-1"/>
				</ol>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="list-item">
		<xsl:call-template name="nl-1"/>
		<li>
			<xsl:apply-templates/>
		</li>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  16. DISPLAY-QUOTE                                            -->
	<!-- ============================================================= -->
	<xsl:template match="disp-quote">
		<xsl:call-template name="nl-1"/>
		<blockquote>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</blockquote>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  17. SPEECH and its internals                                 -->
	<!-- ============================================================= -->
	<!-- first p will pull in the speaker
     in mode "show-it-here" -->
	<xsl:template match="speech">
		<blockquote>
			<xsl:call-template name="make-id"/>
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates/>
			<xsl:call-template name="nl-1"/>
		</blockquote>
	</xsl:template>
	<xsl:template match="speaker" mode="show-it-here">
		<b>
			<xsl:apply-templates/>
		</b>
	</xsl:template>
	<!-- in no mode -->
	<xsl:template match="speaker"/>
	<!-- ============================================================= -->
	<!--  18. STATEMENT and its internals                              -->
	<!-- ============================================================= -->
	<xsl:template match="statement">
		<div class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:call-template name="nl-1"/>
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<xsl:template match="statement/label | statement/title">
		<xsl:call-template name="nl-1"/>
		<p>
			<b>
				<xsl:apply-templates/>
			</b>
		</p>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  19. VERSE-GROUP and its internals                            -->
	<!-- ============================================================= -->
	<xsl:template match="verse-group">
		<xsl:call-template name="nl-1"/>
		<blockquote>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</blockquote>
	</xsl:template>
	<xsl:template match="verse-line">
		<xsl:call-template name="nl-1"/>
		<xsl:apply-templates/>
		<br/>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  20. BOXED-TEXT                                               -->
	<!-- ============================================================= -->
	<xsl:template match="boxed-text">
		<xsl:call-template name="nl-1"/>
		<table border="4" cellpadding="10pt" width="100%">
			<xsl:call-template name="make-id"/>
			<!-- the box is achieved by means of a table, and
         tables don't seem to inherit class attributes,
         so we repeat the class attribute here -->
			<xsl:attribute name="class"><xsl:choose><xsl:when test="ancestor::front">fm</xsl:when><xsl:when test="ancestor::body">body</xsl:when><xsl:when test="ancestor::back">bm</xsl:when><xsl:otherwise>body</xsl:otherwise></xsl:choose></xsl:attribute>
			<xsl:call-template name="nl-1"/>
			<tr>
				<td valign="top">
					<xsl:apply-templates/>
				</td>
			</tr>
		</table>
	</xsl:template>
	<!-- ============================================================= -->
	<!--  21. PREFORMAT                                                -->
	<!-- ============================================================= -->
	<xsl:template match="preformat" name="format-as-line-for-line">
		<pre>
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</pre>
	</xsl:template>
	

	
</xsl:transform>
