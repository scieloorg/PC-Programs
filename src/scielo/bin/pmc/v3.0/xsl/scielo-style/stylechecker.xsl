<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
   	
    <xsl:import href="../nlm-style-4.6.6/nlm-stylechecker.xsl"/>
	<xsl:param name="filename"/>
	
    <xsl:variable name="check_funding">
        <xsl:choose>
            <xsl:when test=".//funding-group">funding-group</xsl:when>
            <xsl:when test=".//ack">maybe-has-funding-group</xsl:when>
        </xsl:choose>
    </xsl:variable>
	<xsl:template match="aff">
		<!-- overwrite stylecheck-match-templates.xsl -->
		<xsl:call-template name="ms-stream-id-test"/>
		<xsl:if test="not(institution)">
			<xsl:call-template name="make-error">
			 	<xsl:with-param name="error-type">aff institution check</xsl:with-param>
			 	<xsl:with-param name="description">aff must have institution</xsl:with-param>

			</xsl:call-template>
         </xsl:if>
         <xsl:if test="not(addr-line)">
			<xsl:call-template name="make-error">
                <xsl:with-param name="error-type">aff addr-line check</xsl:with-param>
                <xsl:with-param name="description">aff should have addr-line, including city</xsl:with-param>
                
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
                <xsl:with-param name="description">if there is funding information in acknowledgement, create funding-group in article-meta</xsl:with-param>
                <xsl:with-param name="class">warning</xsl:with-param>
            </xsl:call-template>
        </xsl:if>
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
        <xsl:call-template name="empty-element-check"/>
        
        <xsl:apply-templates select="." mode="output"/>
    </xsl:template>
</xsl:stylesheet>
