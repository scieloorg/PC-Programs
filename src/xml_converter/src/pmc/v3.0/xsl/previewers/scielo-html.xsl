<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
	<xsl:import href="../jpub/main/jpub3-html.xsl"/>
    <xsl:import href="../scielo-fulltext.xsl"/>
    
    <xsl:param name="css" select="'scielo.css'"/>
	<xsl:param name="path_img" select="'/'"/>
	<xsl:param name="img_format" select="'.jpg'"/>

    <xsl:variable name="xml_article"></xsl:variable>
    <xsl:variable name="xml_article_lang"><xsl:choose><xsl:when test="./article/@xml:lang"></xsl:when><xsl:otherwise>en</xsl:otherwise></xsl:choose></xsl:variable>
    <xsl:variable name="xml_display_objects"/>
    <xsl:variable name="PID"/>

    <xsl:output method="html" omit-xml-declaration="no"
    encoding="utf-8" indent="no"/>
  
    
	<xsl:template match="/">
		<html>
			<xsl:call-template name="make-html-header"/>
			<body>
				<xsl:apply-templates select="article"  mode="text-content"/>
			</body>
		</html>
	</xsl:template>

	<xsl:template name="make-html-header">
    <head>
      <title>
        <xsl:variable name="authors">
          <xsl:call-template name="author-string"/>
        </xsl:variable>
        <xsl:value-of select="normalize-space($authors)"/>
        <xsl:if test="normalize-space($authors)">: </xsl:if>
        <xsl:value-of
          select="/article/front/article-meta/title-group/article-title[1]"/>
      </title>
      <style type="text/css">
  
  	  BODY {
	background: #FFF;
	font-family: verdana, arial;
	font-size: 85%;
}

IMG {
	border: 0px;
}

P {
	font-size: 97%;
}
.container {

	width: 760px;
	max-width: 760px;
	min-width: 550px;
	margin: 0px auto;
}

.top {
	position: relative;
	width: 100%;
}

.navigation {
	width: 75%;
	float: left;
}

.content {
	clear: both;
	padding: 50px 0px 20px 0px;
}

#group {
	float: right;
	width: 250px;
}

#toolBox {
	width: 190px;
}

.footer {

}
#scieloLogo {
	background: url('../../image/en/fbpelogp.gif') no-repeat;
	width: 110px;
	height: 57px;
	float: left;
	margin-right: 20px;
	margin-top: 0px;
}

#scieloLogo A {
	display: block;
	width: 110px;
	height: 57px;
}

#scieloLogo SPAN {
	display: none;
}

.navigation DIV#issues, .navigation DIV#articles, .navigation DIV#articlesSearch, .navigation DIV#journalNavigation {
	float: left;
	margin-right: 10px;
}

.navigation DIV DIV {
	width: auto;
}

.navigation DIV#journalNavigation {
	padding-top: 25px;	
}

#toolBox {
	font-family: arial;
	font-size: 90%;
	border: 1px solid #CCCCCC;
	padding: 8px;
	margin: 0px 0px 10px 20px;
}

.toolBoxSection{
    border-bottom:1px solid #CCCCCC;
}

.content .toolBoxSection H2 {
    font-family: arial;
    color: #666666;
    font-size: 100%;
    font-weight: bold; 
    margin-top: 10px; 
}

.content .box A {
    text-decoration: none;
}

#toolsSection {
	color: #900;
	font-weight: bold;
	font-size: 100%;
	padding-bottom: 4px;
	margin-top: 5px;
	border-bottom: 1px solid #BE9595;
}

#toolBox UL {
	list-style: none;
	padding: 0px;
	margin: 10px 0px 0px 0px;
}

#toolBox UL UL {
	list-style: none;
	padding: 0px;
	margin: 0px 0px 0px 28px;
	font-size: 95%;
}

#toolBox LI {
	margin-bottom: 5px;
}

#toolBox UL UL LI {
	margin-bottom: 2px;
}

#toolBox A {
	color: #000;
	text-decoration: none;
}

#toolBox A:hover {
	text-decoration: underline;
}

#toolBox IMG {
	margin-right: 5px;
	vertical-align: middle;
}

.content {
	border-bottom: 1px solid #8D8D8D;
}

.content H2 {
	font-weight: normal;
	font-size: 140%;
	color: #000080;
	margin: 0px;
}

.content H2#printISSN {
	font-weight: normal;
	font-size: 90%;
	margin: 0px;
}

.content H3 {
	font-family: times;
	color: #800000;
	font-size: 110%;
}

.content H4 {
	font-size: 98%;
	margin-bottom: 5px;
	font-weight: normal;
	color: #800000;
}

HTML>BODY .content H4 {
	font-size: 110%;
}

.content H4#doi {
	font-weight: normal;
	font-size: 80%;
	margin: 0px;
}

#author {
	font-weight: bold;
	margin: 0px;
}

#affiliation {
	font-size: 90%;
	margin: 0px;
}

.articleLinks LI {
	display: inline;
	margin-right: 20px;
	font-size: 95%;
	
}

.footer {
	text-align: center;
	font-size: 90%;
	font-weight: bold;
	color: #000080;
}
.email {
	font-weight: normal;
	color: #000080;
}

.popUp {
	margin: 0px;
	border-top: 7px solid #990000;
	font-size: 75%;
}

.popUp .container {
	width: 95% !important;
	padding: 10px;
}

.popUp H5 {
	color: #990000;
}

.popUp H6 {
	font-size: 90%;
	border-bottom: 1px solid #EEE;
	margin-bottom: 3px;
}

.popUp .close {
	position: absolute;
	right: 10px;
	top: 10px;

}

.popUp .close A {
	color: black;
}
.invisible {display: none}

.license P, .license  A, .license  SPAN{
	text-align: center;
	font-size: 8pt;
	color: black
}

.license img {
	
}
.article-title {
	font-weight: bold;
}@charset "utf-8";

.container {
	width: auto;
	max-width: 760px;
	/* font-family: Verdana, Arial, Helvetica, sans-serif; */
}

/* ------- FRONT ----- */
/*Seção do artigo*/
.categoria{
	text-align: right;
	text-transform: uppercase;
}

/*Títulos do artigo*/
.title{
	/* font-size: 16pt; */
	font-weight: bold;
	font-size: 135%;
}

/*Titulo traduzido do artigo*/
.trans-title{
	font-size: 120%;
	margin-top: 80px;
	margin-bottom: 80px;
}

/*Formatação do grupo de autores*/
.autores{
	margin-bottom: 25px;
	font-weight: bold;
	font-size: 97%;
}
.role {
	
	font-weight: normal;
}
.sig .autores {
	margin-bottom: 0
}

.aff{
	margin: 0px;
}

.abstract .sec, .trans-abstract .sec {
	
	text-transform: uppercase;
	margin-top: 10px;
}
.abstract {
	border-top: 1px solid;
	border-bottom: 1px solid;
	margin-top: 45px;
	font-size: 97%;

}
.trans-abstract {
	border-bottom: 1px solid;
	margin-top: 45px;
	font-size: 97%;
	
}

/* ------------------ */

/* -- FOOTNOTES -- */
/*Formata as notas do autor*/

.author-note{
	padding-top: 5px;
	
}
/*Notas dos autores*/
.fn-author {
	margin-top: 50px;
}

.fn-author-p{
	padding: 0px;
	margin-top: 5px;
	margin-bottom: 0px;
}
.foot-notes {
	padding-top: 20px;
	padding-bottom: 40px;

}
/*Licença do artigo*/
.lic{
	padding-top: 5%;
	font-size: 13px;
	border-top: 1px double #CCC ;
}

.corresp {
	
}
/*Caption de Tabelas e Imagens*/
.fn {
	margin: 0;
	}
.history {
   
}
/*Sig Block*/
.sig {
	text-align: right;
	padding-top: 5%; 
}
/* ------------------ */

/* ---- BODY --- */
/*Título das Seções*/

.body { padding-top: 20px }

.sub-article .body { 
	padding-top: 0%
}

.sec{
	/* clear:both; 
	font-size: 15pt;*/
	/* border-bottom: #CCC double thick; */
	margin-top: 40px;
	font-weight: bold;
	font-size: 120%;
	text-transform: uppercase;	
}
/*Título das Subseções do artigo*/
.subsec{
	font-size: 110%;
	margin-bottom: 0px;
	font-weight: bold;
}

/*Título das Subseções do artigo*/
.sub-subsec{
	font-size: 100%;
	font-weight: bold;
}
.xref-fn{
	width: 200px;
}

.xref-autornote{
	margin: 0px;
	width: auto;
	max-width: 330px;
	padding: 0;
}

.xref-ref{
	width: auto;
	max-width: 300px;
}
/*Tirar estilo da lista*/
.list-none{
	list-style: none;
}
/*DIV da imagem*/
.xref-img, .xref-tab, .figure {
	width: auto;
	border-color: transparent;
	padding: 10px;
	
	text-align: center;
}

/*
.xref-img:hover, .xref-tab:hover{
	border: groove;
	border-color: #09F;
}*/
/*Figura*/
.thumbnail{
	width: auto;
	max-height: 50px;
	text-align: center;

}
.label_caption {
	text-align: center;
	padding: 20px;
	font-size: 80%;

}
.label {
	font-weight: bold;
}

.graphic{
	
    width: auto;
    max-width:600px;
	
}

.table {
	font-size: 90%;
	text-align: center;
}

.table table {
	font-size: 90%;
	text-align: center; 
	width: 100%;
}

.xref-div-img{
	width: auto;
	max-width: 600px;
	float: left;
}




/*Estilo para os tooltips(vem com o código da biblioteca do jquery)*/
.stickytooltip{
	box-shadow: 5px 5px 8px #818181; /*shadow for CSS3 capable browsers.*/
	-webkit-box-shadow: 5px 5px 8px #818181;
	-moz-box-shadow: 5px 5px 8px #818181;
	display:none;
	position:absolute;
	display:none;
	border: 1px double #CCC ; /*Border around tooltip*/
	background:white;
	z-index:3000;
}


.stickytooltip .stickystatus{ /*Style for footer bar within tooltip*/
	background: white;
	color:  #000;
	padding-top: 3px;
	text-align:center;
	font:bold 8pt Verdana, Geneva, sans-serif;
}

.tab-tooltip{
	width:100%;
	background: #FFF;
}


/*Classes '.atip' são referentes as miniaturas*/
.atip{
	padding: 0;
	font-size: 9pt;
	background: 	#9F6;
}

.xref-img-tooltip, .xref-tab-tooltip{
	padding: 0px;
	width: auto;
	max-width: 580px;
}

.stickytooltip div{
	background: #E9E9E9;
}


.article-title {
	font-weight: bold;
}

.sub-article {
    border-top: 1px double #CCC ;
    padding-top: 5%;
    padding-bottom: 5%;
	}</style>
      <!-- XXX check: any other header stuff? XXX -->
    </head>
  </xsl:template>
</xsl:stylesheet>
