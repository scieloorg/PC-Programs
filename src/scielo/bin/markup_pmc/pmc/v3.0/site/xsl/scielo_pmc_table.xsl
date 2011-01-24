<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04_scielo.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	
	<xsl:template match="table-wrap[graphic]">
		<xsl:apply-templates select="." mode="display"/>
	</xsl:template>
	<xsl:template match="table-wrap" mode="display">
		<div class="table">
			<p>
				<a name="{@id}">
					<div class="table-data">
						<xsl:apply-templates select="caption"/>
					</div>
					<div class="table-content">
						<xsl:apply-templates select="graphic |  table"/>
					</div>
					<xsl:apply-templates select="table-wrap-foot"/>
				</a>
			</p>
		</div>
	</xsl:template>
	<xsl:template match="tfoot | table-wrap-foot">
		<div class="foot">
			<xsl:call-template name="make-id"/>
			<xsl:apply-templates/>
		</div>
		<xsl:call-template name="nl-1"/>
	</xsl:template>
	<xsl:template match="table-wrap/caption">
	<xsl:if test="../label"><span class="table-label">
			<xsl:value-of select="../label"/>
		</span>.
</xsl:if>
		<span class="table-{name()}">
			<xsl:apply-templates select="@* | * | text()"/>
		</span>
	</xsl:template>
	
	<xsl:template match="table-wrap/table">
		<xsl:copy-of select="."/>
	</xsl:template>
</xsl:transform>
