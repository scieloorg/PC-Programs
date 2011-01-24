<?xml version="1.0" encoding="utf-8"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:doc="http://www.dcarlisle.demon.co.uk/xsldoc" xmlns:ie5="http://www.w3.org/TR/WD-xsl" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:fns="http://www.w3.org/2002/Math/preference" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:pref="http://www.w3.org/2002/Math/preference" pref:renderer="mathplayer" exclude-result-prefixes="util xsl">

<!-- 
	back
	-->
	<xsl:template match="*" mode="make-back">
		<xsl:comment>*, make-back</xsl:comment>
		<xsl:variable name="layout" select="'float'"/>
		<xsl:choose>
			<xsl:when test=".//back//table-wrap or .//body//sec//fig">
				<xsl:apply-templates select=".//back/*[.//table-wrap] | .//back/*[.//fig] "/>
			</xsl:when>
			<xsl:when test=".//body//sec//table-wrap or .//body//sec//fig">
				<xsl:comment>no graphic here</xsl:comment>
			</xsl:when>
			<xsl:otherwise>
				<xsl:comment>layout float</xsl:comment>
				<xsl:apply-templates select="." mode="figures-and-tables"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="//ack">
			<div id="ack" class="sec">			
			<xsl:apply-templates select="//ack"/>
			</div>
		</xsl:if>
		<xsl:if test=".//back/ref-list">
			<div id="ref-list" class="sec">			
				<xsl:apply-templates select=".//back/ref-list"/>
			</div>
		</xsl:if>
		<xsl:if test="//author-notes">
			<div id="author-notes" class="sec">			
				<a name="corresp"></a>
				<a href="#back_corresp">^</a>
				<xsl:apply-templates select="//author-notes" mode="back"/>
			</div>
		</xsl:if>
		
		<xsl:if test="//permissions">
			<div id="permissions" class="sec">			
				<xsl:apply-templates select="//permissions" mode="back"/>
			</div>
		</xsl:if>
		<xsl:if test=".//back/*[name()!='ref-list'  and name()!='ack' and not(.//table-wrap)]">
			<div class="sec">
		<xsl:apply-templates select=".//back/*[name()!='ref-list'  and name()!='ack' and not(.//table-wrap)]"/>
			
			</div>
		</xsl:if>
	</xsl:template>
	<xsl:template match="ref-list/label">
		<h3><xsl:apply-templates /></h3>
	</xsl:template>
	
	
	<!--
	 footnotes
	-->
	<xsl:template match="fn">
		<p>
			<xsl:apply-templates select="@*|*|text()"/>
		</p>
	</xsl:template>
	<xsl:template match="fn/p">
		<xsl:apply-templates select="text()"/>
	</xsl:template>
	<xsl:template match="fn/@*">
	</xsl:template>
	<xsl:template match="fn/@id">
		<sup>
			<a name="{.}"/>
			<a href="#back_fn{.}">
				<xsl:value-of select="."/>
			</a>
		</sup><xsl:text> </xsl:text>
	</xsl:template>
	<xsl:template match="xref[@ref-type='fn']">
		<a name="back_fn{@rid}">
			</a>
		<sup>
			<xsl:text> </xsl:text>
			<a href="#{@rid}">
				<xsl:value-of select="."/>
			</a>
		</sup>
		<xsl:text> </xsl:text>
	</xsl:template>
	<xsl:template match="back/*[.//table-wrap]">
		<div id="tables">
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<xsl:template match="back/*[.//fig]">
		<div id="figs">
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<xsl:template match="permissions" mode="back">
		<p>
			<xsl:value-of select="copyright-year"/>
			<xsl:value-of select="copyright-statement"/>
			<xsl:apply-templates select="license"/>
		</p>
	</xsl:template>
	
</xsl:transform>
