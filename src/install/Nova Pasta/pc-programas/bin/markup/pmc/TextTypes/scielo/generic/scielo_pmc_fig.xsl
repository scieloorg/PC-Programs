<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:template match="fig/*[name()!='graphic']">
		<div class="fig-text">
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<xsl:template match="fig/label | fig/caption">
		<span class="fig-{name()}">
			<xsl:apply-templates/>
		</span>
	</xsl:template>
	<xsl:template match="fig">
		<a name="{@id}"/>
		<div class="fig">
			<div class="fig-id">
				<span class="gen">
					<xsl:call-template name="make-id"/>
				</span>
			</div>
			<div class="fig-data">
				<xsl:apply-templates select="child::*[not(self::graphic)]"/>
			</div>
			<div class="fig-file">
				<xsl:apply-templates select="graphic"/>
			</div>
		</div>
	</xsl:template>
	<xsl:template match="graphic/@xlink:href| inline-graphic/@xlink:href">
		<xsl:variable name="id" select="."/>
		<xsl:choose>
			<xsl:when test="$var_IMAGES_INFO">
				<xsl:value-of select="$var_IMAGES_INFO//image[@id=$id]"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$var_IMAGE_PATH"/><xsl:value-of select="."/>.gif
			</xsl:otherwise>
		</xsl:choose>
		</xsl:template>	
</xsl:transform>
