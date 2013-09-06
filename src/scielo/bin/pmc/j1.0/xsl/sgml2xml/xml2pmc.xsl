<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"
	xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl xlink mml">

	<xsl:include href="local_dtd.xsl"/>

	<xsl:param name="new_name"/>
	<xsl:variable name="display_funding">
		<xsl:choose>
			<!--
		Verifica se a seção Agradecimentos contém o número do projeto do funding group
		Se contém, funding-group deve ser excluído
		-->
			<xsl:when test="not(//ack)">yes</xsl:when>
			<xsl:when test=".//ack and contains(.//ack//p, .//funding-group//award-id)"
				>no</xsl:when>
			<xsl:otherwise>yes</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<xsl:variable name="xml_type">
		<xsl:choose>
			<xsl:when test=".//mixed-citation and .//element-citation">scielo</xsl:when>
			<xsl:otherwise>pmc</xsl:otherwise>
		</xsl:choose>

	</xsl:variable>


	<xsl:template match="*">
		<xsl:element name="{name()}">
			<xsl:apply-templates select="@* | * | text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}">
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="text()">
		<xsl:value-of select="."/>
	</xsl:template>

	<xsl:template match="mixed-citation">
		<xsl:choose>
			<xsl:when test="$xml_type='scielo'"/>
			<xsl:otherwise>
				<xsl:element name="{name()}">
					<xsl:apply-templates/>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="aff">
		<aff>
			<xsl:apply-templates select="@id | label"/>

			<xsl:variable name="inst"><xsl:value-of select="normalize-space(institution[@content-type='orgname'])"/></xsl:variable>
			<xsl:variable name="is_full"><xsl:if test="$inst!=''"><xsl:apply-templates select="text()[string-length(normalize-space(.))&gt;=string-length($inst)]" mode="is_full"><xsl:with-param name="inst" select="$inst"></xsl:with-param></xsl:apply-templates></xsl:if></xsl:variable>
			<!-- xsl:comment>is_full:<xsl:value-of select="$is_full"/> _</xsl:comment-->
			<xsl:choose>
				<xsl:when test="contains($is_full,'yes')">
					<!-- xsl:comment>full</xsl:comment -->
					<xsl:apply-templates select="text()[string-length(normalize-space(.))&gt;=string-length($inst)]" mode="full">
						<xsl:with-param name="inst" select="$inst"></xsl:with-param>
					</xsl:apply-templates><xsl:apply-templates select="email"></xsl:apply-templates>
				</xsl:when>
				<xsl:otherwise>
					<!-- xsl:comment>parts</xsl:comment -->					
					<xsl:apply-templates
						select="text()[normalize-space(.)!='' and normalize-space(.)!=','] | institution | addr-line | country | email"
						mode="aff-insert-separator"/>					
				</xsl:otherwise>
			</xsl:choose>
		</aff>
	</xsl:template>
	<xsl:template match="text()" mode="is_full">
		<xsl:param name="inst"></xsl:param>
		<xsl:if test="$inst!='' and contains(.,$inst)">yes</xsl:if>
	</xsl:template>
	<xsl:template match="*" mode="full"></xsl:template>
	<xsl:template match="text()" mode="full">
		<xsl:param name="inst"></xsl:param>
		<!--xsl:comment>text():<xsl:value-of select="."/>_</xsl:comment -->
		<!-- xsl:comment>$inst:<xsl:value-of select="$inst"/>_</xsl:comment -->
		<!-- xsl:comment>contains(.,$inst):<xsl:value-of select="contains(.,$inst)"/>_</xsl:comment-->
		<xsl:if test="$inst!='' and contains(.,$inst)"><xsl:value-of select="."/></xsl:if>
		
	</xsl:template>
	
	
	<xsl:template match="aff/* | addr-line/* " mode="aff-insert-separator">
		<xsl:if test="position()!=1">, </xsl:if>
		<xsl:apply-templates select="*|text()[normalize-space(.)!='' and normalize-space(.)!=',']"
			mode="aff-insert-separator"/>
	</xsl:template>
	
	<xsl:template match="aff/text() | addr-line/text()" mode="aff-insert-separator">
		<xsl:variable name="text" select="normalize-space(.)"/>
		<!-- xsl:comment>_ <xsl:value-of select="$text"/>  _</xsl:comment -->  
		
		<xsl:if test="position()!=1">, </xsl:if>
		
		<xsl:choose>
			<xsl:when test="substring($text,string-length($text),1)=','">
				<xsl:value-of select="substring($text,1,string-length($text)-1)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text"/>
			</xsl:otherwise>
		</xsl:choose>
		
	</xsl:template>
	<xsl:template match="email">
		<email><xsl:value-of select="."/></email>
	</xsl:template>
	<xsl:template match="email" mode="aff-insert-separator">
		<xsl:if test="position()!=1">, </xsl:if>
		<xsl:copy-of select="."/>
	</xsl:template>

	<xsl:template match="funding-group">
		<xsl:if test="$display_funding='yes'">
			<xsl:element name="{name()}">
				<xsl:apply-templates select="@* | * | text()"/>
			</xsl:element>
		</xsl:if>
	</xsl:template>


	<xsl:template match="graphic/@href">
		<xsl:attribute name="{name()}">
			<xsl:choose>
				<xsl:when test="$new_name!=''"><xsl:value-of select="$new_name"/>-g<xsl:value-of
						select="../../@id"/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="equation/graphic/@href">
		<xsl:attribute name="{name()}">
			<xsl:choose>
				<xsl:when test="$new_name!=''"><xsl:value-of select="$new_name"/>-e<xsl:value-of
						select="../../@id"/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="inline-graphic/@href">
		<xsl:attribute name="{name()}">
			<xsl:if test="$new_name!=''"><xsl:value-of select="$new_name"/>-i<xsl:value-of
					select="../../@id"/></xsl:if>
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>


</xsl:stylesheet>
