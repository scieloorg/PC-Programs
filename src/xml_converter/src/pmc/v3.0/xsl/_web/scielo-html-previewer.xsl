<?xml version="1.0"?>
<!-- ============================================================= -->
<!--  MODULE:    HTML Preview of Journal Publishing 3.0 XML        -->
<!--  VERSION:   1.0                                               -->
<!--  DATE:      October-December 2008                             -->
<!--                                                               -->
<!-- ============================================================= -->

<!-- ============================================================= -->
<!--  SYSTEM:    NCBI Archiving and Interchange Journal Articles   -->
<!--                                                               -->
<!--  PURPOSE:   Provide an HTML preview of a journal article,     -->
<!--             in a form suitable for reading.                   -->
<!--                                                               -->
<!--  PROCESSOR DEPENDENCIES:                                      -->
<!--             None: standard XSLT 1.0                           -->
<!--             Tested using Saxon 6.5, Tranformiix (Firefox),    -->
<!--               Saxon 9.1.0.3                                   -->
<!--                                                               -->
<!--  COMPONENTS REQUIRED:                                         -->
<!--             1) This stylesheet                                -->
<!--             2) CSS styles defined in jpub-preview.css         -->
<!--                (to be placed with the results)                -->
<!--                                                               -->
<!--  INPUT:     An XML document valid to the                      -->
<!--             Journal Publishing 3.0 DTD.                       -->
<!--             (And note further assumptions and limitations     -->
<!--             below.)                                           -->
<!--                                                               -->
<!--  OUTPUT:    HTML (XHTML if a postprocessor is used)           -->
<!--                                                               -->
<!--  CREATED FOR:                                                 -->
<!--             Digital Archive of Journal Articles               -->
<!--             National Center for Biotechnology Information     -->
<!--                (NCBI)                                         -->
<!--             National Library of Medicine (NLM)                -->
<!--                                                               -->
<!--  CREATED BY:                                                  -->
<!--             Wendell Piez (based on HTML design by             -->
<!--             Kate Hamilton and Debbie Lapeyre, 2004),          -->
<!--             Mulberry Technologies, Inc.                       -->
<!--                                                               -->
<!-- ============================================================= -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">



  <!--<xsl:output method="xml" indent="no" encoding="UTF-8"
    doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/>-->

	<xsl:import href="jpub/main/jpub3-html.xsl"/>
	<xsl:param name="css" select="'xsl/pmc/v3.0/css/jpub-preview.css'"/>
	<xsl:param name="path_img" select="'img/ag/v48n4/'"/>
	<xsl:param name="img_format" select="'.jpg'"/>
	
	<!---
	*************************************************
	Templates para aplicar o efeito do script TOOLTIP
	*************************************************
	-->
	
	<xsl:template match="article">
		<xsl:call-template name="make-article"/>
		<xsl:call-template name="make_miniatures"/>
		<xsl:call-template name="js"/>
	</xsl:template>

	
	<xsl:template match="graphic">
		<xsl:apply-templates/>
		<a href="{concat($path_img,@xlink:href)}.jpg" title="{../label}" class="thickbox">
			<img alt="{@xlink:href}" class="graphic">
			  <xsl:for-each select="alt-text">
				<xsl:attribute name="alt">
				  <xsl:value-of select="normalize-space(.)"/>
				</xsl:attribute>
			  </xsl:for-each>
			  <xsl:call-template name="assign-src"/>
			</img>
		</a>
	</xsl:template>
	
  
	<xsl:template match="xref">
		<a href="#{@rid}"  data-tooltip="t{@rid}" class="anchorLink">
		  <xsl:apply-templates/>
		</a>
	</xsl:template>
	
	<xsl:template name="named-anchor">
		<!-- generates an HTML named anchor, using
			 the source ID when found, otherwise a unique ID -->
		<xsl:variable name="id">
		  <xsl:value-of select="@id"/>
		  <xsl:if test="not(normalize-space(@id))">
			<xsl:value-of select="generate-id(.)"/>
		  </xsl:if>
		</xsl:variable>
		<a name="{$id}" id="{$id}">
		  <xsl:comment> named anchor </xsl:comment>
		</a>
	</xsl:template>
	<xsl:template name="assign-src">
		<xsl:for-each select="@xlink:href">
		  <xsl:attribute name="src">
			<xsl:value-of select="concat($path_img,.,$img_format)"/>
		  </xsl:attribute>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template name="make_miniatures">
	  <div  id="mystickytooltip" class="stickytooltip">
		<div style="padding:5px">
			<xsl:apply-templates select="*" mode="tooltip"/>
			<xsl:apply-templates select="*"	mode="tooltip_fn"/>
		</div>
	  <!--Mensagem de instrução,status da miniatura.-->
	   <div class="stickystatus"/>
	  </div>
	</xsl:template>
	
	
	<xsl:template match="*" mode="tooltip">
		<xsl:apply-templates mode="tooltip"/>
	</xsl:template>
	<xsl:template match="text()" mode="tooltip"/>
	
	<xsl:template match="*" mode="tooltip_fn">
		<xsl:apply-templates mode="tooltip_fn"/>
	</xsl:template>
	<xsl:template match="text()" mode="tooltip_fn"/>
	
	<xsl:template match="fn" mode="tooltip_fn">
		<div class="atip" id="t{@id}" style="width: 250px">
		  <xsl:apply-templates/>
		</div>
	</xsl:template>
	
	<xsl:template match="fig | table-wrap | ref | aff" mode="tooltip">
	  <xsl:call-template name="miniature">
		  <xsl:with-param name="width_t">
			<xsl:choose>
			  <xsl:when test="name() = 'ref' or name() = 'aff'">350</xsl:when>
			  <xsl:when test="name() = 'fig' or name() = 'table-wrap'">500</xsl:when>
			</xsl:choose>
		  </xsl:with-param>
	  </xsl:call-template>
	</xsl:template>
	
	
	
	<!--
	******************
	Qualquer link que represente uma referência cruzada(âncora) pode chamar este template para que ao passar o mouse sobre o link mostre uma miniatura do destino
	Deve ser passado um atributo para definir a largura no parametro "width_t"
	
	Para usar:
	* Ter um template com o mode="tooltip"  para a tag pai
	* Chamar o template: <xsl:call-template name="miniature">
	* Passar o parametro da largura que se pretende ter na miniatura:
		  <xsl:with-param name="width_t">10860168</xsl:stylesheet>
		  O valor passado será a largura colocada em pixels posteriormente
	* Formatar o próximo template com o mode="tooltip_content"
	* Pronto =D
	-->
	<xsl:template name="miniature">
	<xsl:param  name="width_t"/>
	<div class="atip" id="t{@id}" style="width: {normalize-space($width_t)}px">
	  <xsl:choose>
		<xsl:when test="name() = 'ref'">
		  <b><xsl:call-template name="make-label-text"/></b>
		</xsl:when>
		<xsl:when test="name() = 'aff'">
		  <xsl:call-template name="make-label-text"/>
		</xsl:when>
		<xsl:otherwise>
		  <xsl:call-template name="make_label_tooltip"/>
		</xsl:otherwise>
	  </xsl:choose>
	  <xsl:apply-templates mode="tooltip_content"/>
	</div>
	</xsl:template>
	<xsl:template match="label | caption" mode="tooltip_content"/>
	
	
	<xsl:template name="make_label_tooltip">
	<p class="label_tooltip">
	  <b><xsl:call-template name="make-label-text"/></b>
	  <xsl:value-of select=".//caption"/>
	</p>
	</xsl:template>
	
	<xsl:template mode="tooltip_content"
	match="nlm-citation | element-citation | mixed-citation">
	  <xsl:text>&#160;</xsl:text>
	  <xsl:apply-templates select="*"/>
	  <xsl:text>.</xsl:text>
	</xsl:template>
	
	
	<xsl:template match="graphic" mode="tooltip_content">
	<xsl:apply-templates/>
	<a href="{concat($path_img,@xlink:href,$img_format)}">
		<img alt="{@xlink:href}" class="tooltip_img">
		  <xsl:for-each select="alt-text">
			<xsl:attribute name="alt">
			  <xsl:value-of select="normalize-space(.)"/>
			</xsl:attribute>
		  </xsl:for-each>
		  <xsl:call-template name="assign-src"/>
		</img>
	</a>
	</xsl:template>
	
	<xsl:template mode="tooltip_content"
				match="table | thead | tbody | tfoot | col | colgroup | tr | th | td">
	<xsl:copy>
	  <xsl:if test="name() = 'table'">
		<xsl:attribute name="width">98%</xsl:attribute>
	  </xsl:if>
	  <xsl:apply-templates select="@*" mode="table_copy_tooltip"/>
	  <xsl:apply-templates/>
	</xsl:copy>
	</xsl:template>
	
	<xsl:template match="@*" mode="table_copy_tooltip">
	<xsl:copy-of select="."/>
	</xsl:template>
	<xsl:template match="table/@width" mode="table_copy_tooltip"/>
	
	
	<xsl:template match="fn" mode="tooltip_content">
	<div class="footnote">
	  <xsl:apply-templates/>
	</div>
	</xsl:template>
	
	<xsl:template match="supplementary-material" mode="tooltip_body">
	  <xsl:apply-templates select="." mode="label"/>
	  <xsl:apply-templates />
	</xsl:template>
	
	<xsl:template name="js">
		<script type="text/javascript" src="xsl/pmc/v3.0/js/jquery.min.js"></script>
		<script type="text/javascript" src="xsl/pmc/v3.0/js/stickytooltip.js">
		/***********************************************
		* Sticky Tooltip script- (c) Dynamic Drive DHTML code library (www.dynamicdrive.com)
		* This notice MUST stay intact for legal use
		* Visit Dynamic Drive at http://www.dynamicdrive.com/ for this script and 100s more
		***********************************************/
		</script>
		<script type="text/javascript" src="xsl/pmc/v3.0/js/executartooltip.js"></script>
		<script type="text/javascript" src="xsl/pmc/v3.0/js/jquery.anchor.js"></script>
		<script type="text/javascript" src="xsl/pmc/v3.0/js/thickbox.js"></script>
		<script type="text/javascript" src="xsl/pmc/v3.0/js/ddsmoothmenu.js">
		/***********************************************
		* Smooth Navigational Menu- (c) Dynamic Drive DHTML code library (www.dynamicdrive.com)
		* This notice MUST stay intact for legal use
		* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
		***********************************************/
		</script>
		<script type="text/javascript" src="xsl/pmc/v3.0/js/ddsmoothmenu-init.js"></script>
	</xsl:template>
	
</xsl:stylesheet>