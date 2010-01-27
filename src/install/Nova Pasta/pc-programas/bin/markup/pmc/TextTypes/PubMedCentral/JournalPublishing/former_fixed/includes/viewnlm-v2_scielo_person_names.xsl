<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
<xsl:template name="make-persons-in-mode">
		<xsl:variable name="gnms" select="string(descendant::given-names)"/>
		<xsl:variable name="GNMS" select="translate($gnms,
      'abcdefghjiklmnopqrstuvwxyz',
      'ABCDEFGHJIKLMNOPQRSTUVWXYZ')"/>
		<xsl:choose>
			<xsl:when test="$gnms=$GNMS">
				<xsl:apply-templates/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates mode="book"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="choose-person-type-string">
		<xsl:variable name="person-group-type">
			<xsl:value-of select="@person-group-type"/>
		</xsl:variable>
		<xsl:choose>
			<!-- allauthors is an exception to the usual choice pattern -->
			<xsl:when test="$person-group-type='allauthors'"/>
			<!-- the usual choice pattern: singular or plural? -->
			<xsl:when test="count(name) > 1 or etal ">
				<xsl:text>, </xsl:text>
				<xsl:value-of select="($person-strings[@source=$person-group-type]/@plural)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>, </xsl:text>
				<xsl:value-of select="($person-strings[@source=$person-group-type]/@singular)"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="choose-person-group-end-punct">
		<xsl:choose>
			<!-- compiler is an exception to the usual choice pattern -->
			<xsl:when test="@person-group-type='compiler'">
				<xsl:text>. </xsl:text>
			</xsl:when>
			<!-- the usual choice pattern: semi-colon or period? -->
			<xsl:when test="following-sibling::person-group">
				<xsl:text>; </xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>. </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<!-- ============================================================= -->
	<!--  "firstnames"                                                 -->
	<!-- ============================================================= -->
	<!-- called by match="name" in book mode,
     as part of citation handling
     when given-names is not all-caps -->
	<xsl:template name="firstnames">
		<xsl:param name="nodetotal"/>
		<xsl:param name="position"/>
		<xsl:param name="names"/>
		<xsl:param name="pgtype"/>
		<xsl:variable name="length" select="string-length($names)-1"/>
		<xsl:variable name="gnm" select="substring($names,$length,2)"/>
		<xsl:variable name="GNM">
			<xsl:call-template name="capitalize">
				<xsl:with-param name="str" select="substring($names,$length,2)"/>
			</xsl:call-template>
		</xsl:variable>
		<!--
<xsl:text>Value of $names = [</xsl:text><xsl:value-of select="$names"/><xsl:text>]</xsl:text>
<xsl:text>Value of $length = [</xsl:text><xsl:value-of select="$length"/><xsl:text>]</xsl:text>
<xsl:text>Value of $gnm = [</xsl:text><xsl:value-of select="$gnm"/><xsl:text>]</xsl:text>
<xsl:text>Value of $GNM = [</xsl:text><xsl:value-of select="$GNM"/><xsl:text>]</xsl:text>
-->
		<xsl:if test="$names">
			<xsl:choose>
				<xsl:when test="$gnm=$GNM">
					<xsl:apply-templates select="$names"/>
					<xsl:choose>
						<xsl:when test="$nodetotal!=$position">
							<xsl:text>.</xsl:text>
						</xsl:when>
						<xsl:when test="$pgtype!='author'">
							<xsl:text>.</xsl:text>
						</xsl:when>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="$names"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>


	<!-- ============================================================= -->
	<!--  51. UNMODED DATA ELEMENTS: PARTS OF A NAME                   -->
	<!-- ============================================================= -->
	<xsl:template match="name">
		<xsl:variable name="nodetotal" select="count(../*)"/>
		<xsl:variable name="position" select="position()"/>
		<xsl:choose>
			<xsl:when test="given-names">
				<xsl:comment>name, when</xsl:comment>
				<xsl:apply-templates select="surname"/>&#160;<xsl:apply-templates select="given-names"/>
				<xsl:if test="suffix">
					&#160;<xsl:apply-templates select="suffix"/>
				</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<xsl:comment>name, otherwise</xsl:comment>
				<xsl:apply-templates select="surname"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="following-sibling::aff"/>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="$nodetotal=$position">
						<xsl:choose>
							<xsl:when test="parent::person-group/@person-group-type">
								<xsl:choose>
									<xsl:when test="parent::person-group/@person-group-type='author'">
										<xsl:text>. </xsl:text>
									</xsl:when>
									<xsl:otherwise/>
								</xsl:choose>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>. </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:when>
					<xsl:otherwise>, </xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="aff">
		<xsl:variable name="nodetotal" select="count(../*)"/>
		<xsl:variable name="position" select="position()"/>
		<span class="capture-id">
			<xsl:call-template name="make-id"/>
			<xsl:text> (</xsl:text>
			<xsl:apply-templates/>
			<xsl:text>)</xsl:text>
		</span>
		<xsl:choose>
			<xsl:when test="$nodetotal=$position">. </xsl:when>
			<xsl:otherwise>, </xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="etal">
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

	<xsl:template match="surname">
		<xsl:comment>surname</xsl:comment>
		<xsl:value-of select="."/>
	</xsl:template>
	</xsl:transform>
