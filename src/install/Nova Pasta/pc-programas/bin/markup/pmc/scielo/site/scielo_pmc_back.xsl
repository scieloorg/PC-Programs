<?xml version="1.0" encoding="utf-8"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" xmlns:ie5="http://www.w3.org/TR/WD-xsl" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:fns="http://www.w3.org/2002/Math/preference" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:pref="http://www.w3.org/2002/Math/preference" pref:renderer="mathplayer" exclude-result-prefixes="util xsl">
	
	<xsl:template match="*" mode="make-back">
		<xsl:apply-templates select=".//back"/>
		<xsl:apply-templates select=".//back/ref-list"/>
		<xsl:apply-templates select="//author-notes" mode="back"/>
		<xsl:apply-templates select="//history" mode="back"/>
		<!--xsl:apply-templates select="//fn-group" mode="back"/-->
	</xsl:template>
	
	<xsl:template match="back">
		<xsl:apply-templates select="*[not(self::title) and not(self::fn-group) and not(self::ref-list)]"/>
		<xsl:apply-templates select="title"/>
		<xsl:if test="preceding-sibling::body//fn-group | .//fn-group">
			<xsl:apply-templates select="preceding-sibling::body//fn-group | .//fn-group"/>
		</xsl:if>
	</xsl:template>
	
</xsl:transform>
