<?xml version="1.0" encoding="utf-8"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" xmlns:ie5="http://www.w3.org/TR/WD-xsl" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:fns="http://www.w3.org/2002/Math/preference" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:pref="http://www.w3.org/2002/Math/preference" pref:renderer="mathplayer" exclude-result-prefixes="util xsl">

	<xsl:template match="*" mode="make-body">
		<xsl:apply-templates select=".//body/*"/>
	</xsl:template>
	<xsl:template match="sec[@sec-type]">
		<div class="section">
			<a name="{@sec-type}"/>
			<xsl:apply-templates select="label | title" mode="body"/>
			<xsl:apply-templates select="*[name()!='label' and name()!='title']"/>
		</div>
	</xsl:template>
	<xsl:template match="sec/label | sec/title" mode="body">
		<h3>
			<xsl:apply-templates/>
			<a href="#topo">-</a>
		</h3>
	</xsl:template>
	<xsl:template match="sec/sec | sec[not(@sec-type)]">
		<div class="subsection">
			<xsl:apply-templates select="*|text()"/>
		</div>
	</xsl:template>

</xsl:transform>
