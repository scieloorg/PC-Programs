<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"  >
	

    <xsl:variable name="issue_label">
		<xsl:choose>
			<xsl:when test="//ISSUE/@NUM = 'AHEAD'"><xsl:value-of select="substring(//ISSUE/@PUBDATE,1,4)"/>
				<xsl:if test="//ISSUE/@NUM">nahead</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="//ISSUE/@VOL">v<xsl:value-of select="//ISSUE/@VOL"/>
				</xsl:if>
				<xsl:if test="//ISSUE/@NUM">n<xsl:value-of select="//ISSUE/@NUM"/>
				</xsl:if>
				<xsl:if test="//ISSUE/@SUPPL">s<xsl:value-of select="//ISSUE/@SUPPL"/>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

    <xsl:variable name="var_IMAGE_PATH">
		<xsl:choose>
			<xsl:when test="//PATH_SERIMG and //SIGLUM and //ISSUE">
				<xsl:value-of select="//PATH_SERIMG"/>
				<xsl:value-of select="//SIGLUM"/>/<xsl:value-of select="$issue_label"/>/</xsl:when>
			<xsl:when test="$path_img!=''"><xsl:value-of select="$path_img"/></xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="//image-path"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<xsl:variable name="article_lang"><xsl:value-of select="$xml_article_lang"/></xsl:variable>
	
	<xsl:variable name="display_objects"><xsl:value-of select="$xml_display_objects"/></xsl:variable>
	
	<xsl:template match="article" mode="text-content">
		
			<xsl:apply-templates select=".//article-meta//article-categories"/>
			
			<xsl:apply-templates select=".//article-meta//title-group"/>
			
			<xsl:apply-templates select=".//article-meta//contrib-group"/>
			
			<xsl:apply-templates select=".//article-meta//aff"/>
			
			<xsl:apply-templates select=".//article-meta//abstract"/>
			
			<xsl:apply-templates select=".//article-meta//trans-abstract"/>
			
			<div class="body">
			<xsl:apply-templates select=".//body"/></div>
			
			<xsl:apply-templates select=".//back "/>
			
			<div class="foot-notes">
				<xsl:apply-templates select=".//article-meta//history"/>
				
				<xsl:apply-templates select=".//article-meta//author-notes"/>
				
				<xsl:apply-templates select=".//article-meta//permissions"/>
				
			</div>
		
		
	</xsl:template>
	
	<!--xsl:template match="sub | sup | p">
		<xsl:element name="{name()}">
			<xsl:apply-templates select=" * | text()"/>
		</xsl:element>
	</xsl:template-->
	

	<!--Define itálicos e negritos-->
	<!--xsl:template match="italic">
		<i>
		<xsl:apply-templates select="*|text()"/>
		</i>
	</xsl:template>
	<xsl:template match="bold">
		<b>
		<xsl:apply-templates select="*|text()"/>
		</b>
	</xsl:template>
	<xsl:template match="disp-quote">
		<blockquote>
			<xsl:apply-templates/>
		</blockquote>
	</xsl:template-->
	<!-- inibe -->
	<xsl:template match="article-meta/article-id"/>
		<xsl:template match="article-meta//pub-date"/>
		<xsl:template match="article-meta/fpage"/>
		<xsl:template match="article-meta/lpage"/>
		<xsl:template match="article-meta/volume"/>
		<xsl:template match="article-meta/issue"/>
		<!--Títulos do Artigo-->
	<xsl:template match="title-group/article-title">
		<div>
			<p class="title">
				<xsl:apply-templates select="* | text() "/>
								<xsl:apply-templates select="../subtitle" mode="subtitle"/>
			</p>
		</div>
	</xsl:template>
	<xsl:template match="trans-title-group/trans-title">
		<div>
			<p class="trans-title">
				<xsl:apply-templates select="* | text() "/>
								<xsl:apply-templates select="../trans-subtitle" mode="subtitle"/>
			</p>
		</div>
	</xsl:template>
	<!--Subtitulos do artigo-->
	<xsl:template match="title-group/subtitle | trans-title-group/trans-subtitle" mode="subtitle">
		<span>
		<xsl:apply-templates select="* | text()"/>
		</span>
	</xsl:template>
	<xsl:template match="title-group/subtitle | trans-title-group/trans-subtitle"/>
		<!--Categoria do artigo     	Talvez seja desenecessária essa informação     -->
	<xsl:template match="subj-group/subject">
		<p class="categoria"><xsl:value-of select="."/></p>
	</xsl:template>
	<!--Div contendo nome dos autores-->
	<xsl:template match="contrib-group">
		<div class="autores">
			<xsl:apply-templates select="contrib"/>
		</div>
	</xsl:template>
	<xsl:template match="contrib">
		<xsl:if test="position()!=1">, </xsl:if><xsl:apply-templates select="name"/>
        <xsl:if test="xref">
		<xsl:apply-templates select="." mode="xref-list"/></xsl:if>
	</xsl:template>
	<xsl:template match="contrib/name">
		<xsl:apply-templates select="given-names"/>&#160;<xsl:apply-templates select="surname"/>
	</xsl:template>
	
	<xsl:template match="*[xref]" mode="xref-list">
		<sup>
		<xsl:apply-templates select="xref"  mode="xref"/>
		</sup>
	</xsl:template>
	<xsl:template match="xref" mode="xref">
		<xsl:if test="position() &gt; 1">,</xsl:if>
		<a href="#{@rid}" ><!--FIXME-->
		<xsl:apply-templates select="label|text()"/>
		</a>
		
	</xsl:template>
	<!--Afiliações e notas do autor-->
	<xsl:template match="author-notes">
		<div class="author-note">
			<xsl:apply-templates select="* | text()"/>
		</div>
		<div class="fn-author">
			<xsl:apply-templates select="fn" mode="fn-author"/>
		</div>
	</xsl:template>
	<xsl:template match="author-notes/corresp">
		<p class="corresp">
			<xsl:apply-templates select="* | text() | @*"/>
		</p>
	</xsl:template>
	<xsl:template match="author-notes/fn" mode="fn-author">
		<p class="fn-author-p"><a name="{@id}">
			<xsl:apply-templates select="* | text()"/>
			</a></p>
	</xsl:template>
	<xsl:template match="author-notes/fn"/>
		<xsl:template match="fn/label">
		<sup>
			<xsl:apply-templates select="* | text()"/>
		</sup>
	</xsl:template>
	<xsl:template match="author-notes/fn/p">
		<xsl:apply-templates select="* | text()"/>
	</xsl:template>
	<xsl:template match="aff">
		<p class="aff"><a name="{@id}">
			<xsl:apply-templates select="label"/>
			</a>
			<xsl:apply-templates select="institution[@content-type='orgdiv3']"/><xsl:if test="institution[@content-type='orgdiv3']">, </xsl:if>
			<xsl:apply-templates select="institution[@content-type='orgdiv2']"/><xsl:if test="institution[@content-type='orgdiv2']">, </xsl:if>
			<xsl:apply-templates select="institution[@content-type='orgdiv1']"/><xsl:if test="institution[@content-type='orgdiv1']">, </xsl:if>
			<xsl:apply-templates select="institution[@content-type='orgname']"/>
			<xsl:apply-templates select="addr-line | country | email"/>
			</p>
	</xsl:template>
	
	<xsl:template match="addr-line//text()"><xsl:value-of select="normalize-space(.)"/><xsl:if test="contains(.,',')">&#160; 
</xsl:if>
	</xsl:template>
	
	<xsl:template match="addr-line | country">, <xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="aff/label">
		<sup><xsl:value-of select="."/></sup>
	</xsl:template>
	<!--     *****     Email     **********************************************************************************     Nota:Se houver algum e-mail no resto do artigo também serpa aplicado este template     **********************************************************************************     -->
	<xsl:template match="email">
		<a href="mailto:{text()}"><xsl:value-of select="."/></a>
	</xsl:template>
	<xsl:template match="email" mode="element-content">
		&#160;<a href="mailto:{text()}"><xsl:value-of select="."/></a>
	</xsl:template>
	<xsl:template match="email" mode="mixed-content">
		<a href="mailto:{text()}"><xsl:value-of select="."/></a>
	</xsl:template>
	<xsl:template match="aff/email">, <a href="mailto:{text()}"><xsl:value-of select="."/></a>
	</xsl:template>
	<!--Fim de Notas de autor--><!--Recebido e aceito-->
	<xsl:template match="history">
		<!--xsl:variable name="lang" select="@xml:lang"/> 		<xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords-with-abstract" /-->
		<div class="history">
			<p>
				<xsl:choose>
					<xsl:when test="$article_lang='en'">
						<xsl:apply-templates select="date" mode="en"/>
					</xsl:when>
					<xsl:when test="$article_lang='pt'">
						<xsl:apply-templates select="date" mode="pt"/>
					</xsl:when>
					<xsl:when test="$article_lang='es'">
						<xsl:apply-templates select="date" mode="es"/>
					</xsl:when>
				</xsl:choose>
			</p>
		</div>
	</xsl:template>
	<!--     *********************************************************     Recebido e aceito quando o idioma do artigo for em INGLÊS     *********************************************************     -->
	<xsl:template match="date" mode="en">
		<xsl:choose>
			<xsl:when test="@date-type='received'">
				Received
			</xsl:when>
			<xsl:when test="@date-type='accepted'">
				Accepted
			</xsl:when>
		</xsl:choose>
		<xsl:apply-templates select="month" mode="date-month-en"/>
				<xsl:apply-templates select="day"/>, 
				<xsl:apply-templates select="year"/>
				<xsl:choose>
			<xsl:when test="@date-type='received'">;</xsl:when>
			<xsl:when test="@date-type='accepted'">.</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="month" mode="date-month-en">
		<xsl:choose>
			<xsl:when test="text() = 01">
				January
			</xsl:when>
			<xsl:when test="text() = 02">
				February
			</xsl:when>
			<xsl:when test="text() = 03">
				March
			</xsl:when>
			<xsl:when test="text() = 04">
				April
			</xsl:when>
			<xsl:when test="text() = 05">
				May
			</xsl:when>
			<xsl:when test="text() = 06">
				June
			</xsl:when>
			<xsl:when test="text() = 07">
				July
			</xsl:when>
			<xsl:when test="text() = 08">
				August
			</xsl:when>
			<xsl:when test="text() = 09">
				September
			</xsl:when>
			<xsl:when test="text() = 10">
				October
			</xsl:when>
			<xsl:when test="text() = 11">
				November
			</xsl:when>
			<xsl:when test="text() = 12">
				December
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
	<!--     ******************************************     fim de recebido e aceito em idioma 	INGLES     ******************************************     --><!--     ************************************************************     Recebido e aceito quando o idioma do artigo for em PORGUGUÊS     ************************************************************     -->
	<xsl:template match="date" mode="pt">
		<xsl:choose>
			<xsl:when test="@date-type='received'">
				Recebido em
			</xsl:when>
			<xsl:when test="@date-type='accepted'">
				Aceito em
			</xsl:when>
		</xsl:choose>
		<xsl:apply-templates select="day"/> de 
		<xsl:apply-templates select="month" mode="date-pt"/> de 
		<xsl:apply-templates select="year"/>
				<xsl:choose>
			<xsl:when test="@date-type='received'">;</xsl:when>
			<xsl:when test="@date-type='accepted'">.</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="month" mode="date-pt">
		<xsl:choose>
			<xsl:when test="text() = 01">
				Janeiro
			</xsl:when>
			<xsl:when test="text() = 02">
				Fevereiro
			</xsl:when>
			<xsl:when test="text() = 03">
				Março
			</xsl:when>
			<xsl:when test="text() = 04">
				Abril
			</xsl:when>
			<xsl:when test="text() = 05">
				Maio
			</xsl:when>
			<xsl:when test="text() = 06">
				Junho
			</xsl:when>
			<xsl:when test="text() = 07">
				Julho
			</xsl:when>
			<xsl:when test="text() = 08">
				Agosto
			</xsl:when>
			<xsl:when test="text() = 09">
				Setembro
			</xsl:when>
			<xsl:when test="text() = 10">
				Outubro
			</xsl:when>
			<xsl:when test="text() = 11">
				Novembro
			</xsl:when>
			<xsl:when test="text() = 12">
				Dezembro
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
	<!--     *********************************************     fim de recebido e aceito em idioma 	PORTUGUES     *********************************************     --><!--     ***********************************************************     Recebido e aceito quando o idioma do artigo for em ESPANHOL     ***********************************************************     -->
	<xsl:template match="date" mode="es">
		<xsl:choose>
			<xsl:when test="@date-type='received'">
				Recebido el
			</xsl:when>
			<xsl:when test="@date-type='accepted'">
				Aceptado el
			</xsl:when>
		</xsl:choose>
		<xsl:apply-templates select="day" /> de 
		<xsl:apply-templates select="month" mode="date-es"/> de 
		<xsl:apply-templates select="year"/>
				<xsl:choose>
			<xsl:when test="@date-type='received'">;</xsl:when>
			<xsl:when test="@date-type='accepted'">.</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="month" mode="date-es">
		<xsl:choose>
			<xsl:when test="text() = 01">
				enero
			</xsl:when>
			<xsl:when test="text() = 02">
				febrero
			</xsl:when>
			<xsl:when test="text() = 03">
				marzo
			</xsl:when>
			<xsl:when test="text() = 04">
				abril
			</xsl:when>
			<xsl:when test="text() = 05">
				mayo
			</xsl:when>
			<xsl:when test="text() = 06">
				junio
			</xsl:when>
			<xsl:when test="text() = 07">
				julio
			</xsl:when>
			<xsl:when test="text() = 08">
				agosto
			</xsl:when>
			<xsl:when test="text() = 09">
				septiembre
			</xsl:when>
			<xsl:when test="text() = 10">
				octubre
			</xsl:when>
			<xsl:when test="text() = 11">
				noviembre
			</xsl:when>
			<xsl:when test="text() = 12">
				diciembre
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
		<!--Licenças-->
	<xsl:template match="license-p">
		<div>
			<p class="lic"><xsl:value-of select="text() |  @*"/></p>
		</div>
	</xsl:template>
	<!--Resumos-->
	<xsl:template match="abstract | trans-abstract">
		<xsl:variable name="lang" select="@xml:lang"/>
		<div><!--Apresenta o título da seção conforme a lingua existente-->
			<xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
			<xsl:if test="not(.//title)">
			<xsl:choose>
				<xsl:when test="$lang='pt'">
					<p class="sec"><a name="resumo">RESUMO</a></p>
				</xsl:when>
				<xsl:when test="$lang='es'">
					<p class="sec"><a name="resumen">RESUMÉN</a></p>
				</xsl:when>
				<xsl:otherwise>
					<p class="sec"><a name="abstract">ABSTRACT</a></p>
				</xsl:otherwise>
			</xsl:choose></xsl:if>
			<xsl:apply-templates select="* | text()"/>
						<xsl:apply-templates select="..//kwd-group[normalize-space(@xml:lang)=normalize-space($lang)]" mode="keywords-with-abstract"/>
		</div>
	</xsl:template>
	<!--Lilsta as palavras chave dentro de Abstract-->
	<xsl:template match="@* | text()" mode="debug">
		|<xsl:value-of select="."/>|
	</xsl:template>
	<!--Lilsta as palavras chave dentro de Abstract-->
	<xsl:template match="kwd-group" mode="keywords-with-abstract">
		<xsl:variable name="lang" select="normalize-space(@xml:lang)"/>
		<!--xsl:param name="test" select="1"/>     <xsl:value-of select="$test"/-->
		<p><!--Define o nome a ser exibido a frente das palavras-chave conforme o idioma-->
			<xsl:choose>
				<xsl:when test="$lang='es'">
					<b>Palabras-clave: </b>
				</xsl:when>
				<xsl:when test="$lang='pt'">
					<b>Palavras-Chave: </b>
				</xsl:when>
				<xsl:otherwise>
					<b>Keywords: </b>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select=".//kwd"/>
		</p>
	</xsl:template>
	<xsl:template match="kwd-group"/>
		<!--Adiciona vírgulas as palavras-chave-->
	<xsl:template match="kwd">
		<xsl:if test="position()!= 1">, </xsl:if> 
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="body/sec | ack/sec">
		<div>
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<!--Exibe o título das seções classe 'sec' no css-->
	<xsl:template match="body/sec/title | ack/sec/title | back/sec/title">
		<p class="sec"><a name="{.}">
			<xsl:apply-templates select="@* | * | text()"/>
			</a></p>
	</xsl:template>
	<!--Exibe uma subseção dos artigos-->
	<xsl:template match="body/sec/sec/title | abstract/sec/title |trans-abstract/sec/title">
		<p class="subsec">
			<xsl:apply-templates select="@* | * | text()"/>
		</p>
	</xsl:template>
	<!--Exibe uma subseção de terceiro nível-->
	<xsl:template match="body/sec/sec//title">
		<p class="sub-subsec">
			<xsl:apply-templates select="@* | * | text()"/>
		</p>
	</xsl:template>
	<!--Imagens e referências cruzadas entre as mesmas-->
	<xsl:template match="supplementary-material">
		<div class="xref-img"><a name="{@id}">
			<xsl:apply-templates/>
			</a></div>
	</xsl:template>
	
	<xsl:template match=" caption/title | caption/title ">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="fig/label | table-wrap/label | fig/caption | table-wrap/caption">
		<span class="{name()}"><xsl:apply-templates select="* | text()"/></span>
	</xsl:template>
	<xsl:template match="inline-graphic | graphic"><a target="_blank"><xsl:apply-templates select="@xlink:href" mode="href"/>
		<img class="graphic"><xsl:apply-templates select="@xlink:href" mode="src"/></img></a>		
	</xsl:template>
	<xsl:template match="inline-graphic | graphic" mode="thumbnail">
		<img class="thumbnail"><xsl:apply-templates select="@xlink:href" mode="src"/></img>		
	</xsl:template>

	<xsl:template match="fig">

		<div class="figure"><a name="{@id}"></a>
		    <xsl:apply-templates select="graphic"/>
			<div class="label_caption">
			    <xsl:apply-templates select="label"/><xsl:if test="label and caption"> - <xsl:apply-templates select="caption"/>
			     </xsl:if>
		    </div>
			
		</div>
	</xsl:template>
	<!--Tabelas-->
	<xsl:template match="table-wrap">
		<div class="xref-tab"><a name="{@id}"/>
			<div class="label_caption">
			    <xsl:apply-templates select="label"/><xsl:if test="label and caption"> - <xsl:apply-templates select="caption"/>
			     </xsl:if>
		    </div>
		    <xsl:apply-templates select="table | graphic | table-wrap-foot"/>

		</div>
	</xsl:template>
	<!--Tabela se estiver como imagem-->
	<xsl:template match="table-wrap/graphic">
		<img class="graphic"><xsl:apply-templates select="@xlink:href" mode="src"/></img>
	</xsl:template>

	<xsl:template match="@href | @xlink:href" mode="src">
        <xsl:variable name="src"><xsl:value-of select="$var_IMAGE_PATH"/>/<xsl:choose><xsl:when test="contains(., '.tif')"><xsl:value-of select="substring-before(.,'.tif')"/></xsl:when><xsl:otherwise><xsl:value-of select="."/></xsl:otherwise></xsl:choose></xsl:variable>
        <xsl:attribute name="src"><xsl:value-of select="$src"/>.jpg</xsl:attribute>
	</xsl:template>
	<xsl:template match="@href | @xlink:href" mode="href">
        <xsl:variable name="src"><xsl:value-of select="$var_IMAGE_PATH"/>/<xsl:choose><xsl:when test="contains(., '.tif')"><xsl:value-of select="substring-before(.,'.tif')"/></xsl:when><xsl:otherwise><xsl:value-of select="."/></xsl:otherwise></xsl:choose></xsl:variable>
        <xsl:attribute name="href"><xsl:value-of select="$src"/>.jpg</xsl:attribute>
	</xsl:template>
	<!--Tabela codificada-->
	<xsl:template match="table"><div class="table">
		<xsl:copy-of select="."/></div>
	</xsl:template>
	<xsl:template match="thead">
		<thead>
			<xsl:apply-templates select="@* | *"/>
		</thead>
	</xsl:template>
	<xsl:template match="tbody">
		<tbody>
			<xsl:apply-templates select="@* | *"/>
		</tbody>
	</xsl:template>
	<xsl:template match="tr">
		<tr>
			<xsl:apply-templates select="@* | *"/>
		</tr>
	</xsl:template>
	<xsl:template match="td">
		<td><xsl:apply-templates select="@* | *| text()"/>
		</td>
	</xsl:template>
	<xsl:template match="th">
		<th><xsl:apply-templates select="@* | *| text()"/>
		</th>
	</xsl:template>
	
	<xsl:template match="table-wrap-foot/fn">
		<p class="fn"><a name="{@id}">
			<xsl:apply-templates select="* | text()"/>
			</a></p>
	</xsl:template>
	<xsl:template match="table-wrap-foot/fn/p">
		<xsl:apply-templates/>
	</xsl:template>
	<!--Fim dos labels e captions--><!--SigBlock--><!--sig-block>             <sig>Joel <bold>FAINTUCH</bold>                 <sup>1</sup>             </sig>             <sig>Ricardo Guilherme <bold>VIEBIG</bold>                 <sup>2</sup>             </sig> 		</sig-block-->
	<xsl:template match="sig-block">
		<xsl:apply-templates select="* | text()"/>
	</xsl:template>
	<xsl:template match="sig">
		<p class="sig">
			<xsl:apply-templates/>
		</p>
	</xsl:template>
	<xsl:template match="sig/bold">
		<b>&#160;
		<xsl:apply-templates/>
		</b>
	</xsl:template>
		


	<!--xsl:template match="list[@list-type='simple'] | list[@list-type='bullet']">
		<ul>
			<xsl:apply-templates select="list-item"/>
		</ul>
	</xsl:template>
	<xsl:template match="list[@list-type='alpha-upper']">
		<ol type="A">
			<xsl:apply-templates select="list-item"/>
		</ol>
	</xsl:template>
	<xsl:template match="list[@list-type='alpha-lower']">
		<ol type="a">
			<xsl:apply-templates select="list-item"/>
		</ol>
	</xsl:template>
	<xsl:template match="list[@list-type='order']">
		<ol>
			<xsl:apply-templates select="list-item"/>
		</ol>
	</xsl:template>
	<xsl:template match="list-item/p">
		<xsl:apply-templates select="* | text()"/>
		
	</xsl:template-->
	<!--     *****************************     Referências     *****************************     --><!--Define referências-->
	<xsl:template match=" back/ref-list">
		<div>
			<xsl:choose>
				<xsl:when test="title">
					<p class="sec">
						<xsl:apply-templates select="title" mode="reflist-title"/>
					</p>
				</xsl:when>
				<xsl:otherwise>
					<p class="sec"><a name="references">
						<xsl:choose>
							<xsl:when test="$article_lang='pt'">
								REFERÊNCIAS
							</xsl:when>
							<xsl:when test="$article_lang='es'">
								REFERENCIAS
							</xsl:when>
							<xsl:otherwise>
								REFERENCES
							</xsl:otherwise>
						</xsl:choose>
						</a></p>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="ref"/>
		</div>
	</xsl:template>
	<xsl:template match="ref-list/title"/>
		<xsl:template match="ref-list/title" mode="reflist-title">
		<a name="{.}"><xsl:value-of select="."/></a>
	</xsl:template>
	<xsl:template match="ref">
		<p class="ref">
			<a name="{@id}"><!--Imprime o label das referências-->
			<xsl:if test=".//label">
					<xsl:choose>
					<xsl:when test="mixed-citation">
						<xsl:apply-templates select="mixed-citation"/>			
					</xsl:when>
					<xsl:when test="element-citation">
                        <xsl:apply-templates select="element-citation"/>			
					</xsl:when>
					<xsl:when test="citation">
                        <xsl:apply-templates select="citation"/>			
					</xsl:when>
					<xsl:when test="nlm-citation">
                        <xsl:apply-templates select="nlm-citation"/>			
					</xsl:when>

				</xsl:choose>

				</xsl:if>
				<xsl:if test="not(.//label)">
					<xsl:value-of select="position()"/>.&#160;
				<xsl:choose>
					<xsl:when test="mixed-citation">
                        <xsl:apply-templates select="mixed-citation"/>			
					</xsl:when>
					<xsl:when test="element-citation">
                        <xsl:apply-templates select="element-citation"/>			
					</xsl:when>
					<xsl:when test="citation">
                        <xsl:apply-templates select="citation"/>			
					</xsl:when>
					<xsl:when test="nlm-citation">
                        <xsl:apply-templates select="nlm-citation"/>			
					</xsl:when>

				</xsl:choose>
				</xsl:if>
			</a>


            <xsl:variable name="aref">000000<xsl:value-of select="position()"/></xsl:variable>

             <xsl:variable name="ref"><xsl:value-of select="substring($aref, string-length($aref) - 5)"/></xsl:variable>
            <xsl:variable name="pid"><xsl:value-of select="$PID"/><xsl:value-of select="substring($ref,2)"/></xsl:variable>

			[&#160;<a href="javascript:void(0);" onclick="javascript: window.open('/scielo.php?script=sci_nlinks&amp;pid={$pid}&amp;lng=en','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">Links</a>&#160;]
		</p>
	</xsl:template>
	<!--mixed-citation-->
	<xsl:template match="mixed-citation">
		<xsl:apply-templates select="* | text()" mode="mixed-content"/>
	</xsl:template>
	<xsl:template match="name" mode="mixed-content">
		<xsl:apply-templates select="surname"/>&#160;<xsl:apply-templates select="given-names"/>
		<xsl:if test="suffix">&#160;<xsl:apply-templates select="suffix"/></xsl:if>
	</xsl:template>
	<!--element-citation e citation-->
	<xsl:template match="text()" mode="element-content">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	<xsl:template match="element-citation | citation">
		<xsl:choose>
			<xsl:when test="name">
				<xsl:apply-templates select="." mode="name-element-citation"/>
				<xsl:apply-templates select="*[name()!='name']" mode="element-content"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="*" mode="element-content"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!--Lista de autores,tanto mixed como element citation--><!--xsl:template match="person-group" mode="mixed-content"> 		<xsl:apply-templates select="name | collab" mode="list-author-ref"/>     </xsl:template-->
	<xsl:template match="element-citation" mode="name-element-citation">
		<xsl:apply-templates select="name" mode="element-content"/>
	</xsl:template>
	<xsl:template match="person-group" mode="element-content">
		<xsl:apply-templates select="*" mode="element-content"/>
	</xsl:template>
	<xsl:template match="name" mode="element-content">
		<span class="ref-autor">
		<xsl:if test="position() &gt; 1">, </xsl:if>
		<xsl:apply-templates select="surname"/>&#160;<xsl:apply-templates select="given-names"/>
		<xsl:if test="suffix">&#160;<xsl:apply-templates select="suffix"/></xsl:if>
		<xsl:if test="position() = last()">
			<xsl:choose>
				<xsl:when test="..//etal"/>
				<xsl:when test="../@person-group-type='transed'">,translator and editor.</xsl:when>
				<xsl:when test="../@person-group-type != 'author'">
					<xsl:choose>
						<xsl:when test="position() = 1 and position() = last()">, <xsl:value-of select="../@person-group-type"/>.
						</xsl:when>
						<xsl:otherwise>,<xsl:value-of select="../@person-group-type"/>s.</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>.</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		</span>
	</xsl:template>
	<xsl:template match="collab" mode="element-content">
		<span class="ref-autor">
		<xsl:if test="position() &gt; 1">;
		</xsl:if>
		<xsl:apply-templates select="* | text()"/>
				<xsl:if test="@collab-type">
			<xsl:choose>
						<xsl:when test="position() = 1 and position() = last()">,<xsl:value-of select="@collab-type"/>
				</xsl:when>
						<xsl:otherwise>,<xsl:value-of select="@collab-type"/>s
				</xsl:otherwise>
					</xsl:choose>
		</xsl:if>
		<xsl:if test="position() = last()">
			<xsl:choose>
				<xsl:when test="..//etal">
					<xsl:apply-templates select="etal"/>
				</xsl:when>
				<xsl:otherwise>.</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		</span>
	</xsl:template>
	<xsl:template match="string-name" mode="element-content">
		<span class="ref-autor">
		<xsl:if test="position() &gt; 1">;
		</xsl:if>
		<xsl:apply-templates select="* | text()"/>
				<xsl:if test="suffix">
			&#160;
			<xsl:apply-templates select="suffix"/>
				</xsl:if>
		<xsl:if test="position() = last()">
			<xsl:choose>
				<xsl:when test="..//etal">
					<xsl:apply-templates select="etal"/>
				</xsl:when>
				<xsl:otherwise>.</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		</span>
	</xsl:template>
	<xsl:template match="aff" mode="element-content">(<xsl:apply-templates/>
		)
	</xsl:template>
	<xsl:template match="article-title | chapter-title" mode="element-content">
		<span class="ref-title">&#160;
		<xsl:apply-templates/>
			<xsl:choose>
				<xsl:when test="../trans-title"/>
				<xsl:otherwise>.</xsl:otherwise>
			</xsl:choose>
		</span>
	</xsl:template>
	<xsl:template match="trans-title | trans-source" mode="element-content">
		<span class="ref-title-t">
		<xsl:choose>
			<xsl:when test="contains(.,'[')">&#160;
				<xsl:apply-templates/>.</xsl:when>
			<xsl:otherwise>&#160;[
				<xsl:apply-templates/>
				].
			</xsl:otherwise>
		</xsl:choose>
		</span>
	</xsl:template>
	<xsl:template match="source" mode="element-content">
		<span class="ref-source">&#160;
		<xsl:apply-templates/>
				<xsl:choose>
			<xsl:when test="../@publication-type='confproc'">
						<xsl:choose>
					<xsl:when test="../conf-name">.</xsl:when>
					<xsl:when test="../conf-loc |../conf-date">;</xsl:when>
				</xsl:choose>
					</xsl:when>
			<xsl:when test="../@publication-type='journal'">
						<xsl:choose>
							<xsl:when test="../edition |../trans-source"/>
														<xsl:otherwise>.</xsl:otherwise>
				</xsl:choose>
					</xsl:when>
			<xsl:when test="../@publication-type='patent'"/>
										<xsl:otherwise>.</xsl:otherwise>
		</xsl:choose>
		</span>
	</xsl:template>
	<xsl:template match="patent" mode="element-content">
		&#160;<xsl:value-of select="."/>.
	</xsl:template>
	<xsl:template match="edition" mode="element-content">
		<xsl:choose>
			<xsl:when test="../@publication-type = 'journal' or ../@publication-type='newspaper' or ../@citation-type='journal' or ../@citation-type='newspaper'">(<xsl:apply-templates/>
				).
			</xsl:when>

<xsl:when test="../@publication-type='book' or ../@publication-type='report' or ../@citation-type='book' or ../@citation-type='report'">&#160;
				<xsl:apply-templates/>.</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="publisher-loc" mode="element-content">
		<xsl:choose>
			<xsl:when test="../@publication-type='journal'">(<xsl:apply-templates/>
				).
			</xsl:when>
			<xsl:when test="../@publication-type='book'">&#160;
				<xsl:apply-templates/>
				:
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="publisher-name" mode="element-content">&#160;<xsl:apply-templates/>
		;
	</xsl:template>
	<xsl:template match="conf-name" mode="element-content">&#160;<xsl:apply-templates/>
				<xsl:choose>
			<xsl:when test="../conf-date or  conf-loc">;</xsl:when>
			<xsl:otherwise>.</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="conf-date" mode="element-content">&#160;<xsl:apply-templates/>
				<xsl:choose>
			<xsl:when test="../conf-loc">;</xsl:when>
			<xsl:otherwise>.</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="conf-loc" mode="element-content">&#160;<xsl:apply-templates/>.</xsl:template>
	<xsl:template match="year" mode="element-content">
		<span class="data">&#160;
		<xsl:apply-templates/>
				<xsl:choose>
			<xsl:when test="../month or ../day or ../season">&#160;</xsl:when>
			<xsl:when test="../size[@units='page']">.</xsl:when>
			<xsl:otherwise>;</xsl:otherwise>
		</xsl:choose>
		</span>
	</xsl:template>
	<xsl:template match="month" mode="element-content">
		<span class="data">
		<xsl:apply-templates/>
				<xsl:choose>
			<xsl:when test="../day or ../season ">&#160;</xsl:when>
			<xsl:when test="../volume  or ../issue  or  issue-part  or ../supplement">;</xsl:when>
			<xsl:when test="../size[@units='page']">.</xsl:when>
			<xsl:otherwise>:</xsl:otherwise>
		</xsl:choose>
		</span>
	</xsl:template>
	<xsl:template match="day | season" mode="element-content">
		<xsl:apply-templates/>
				<xsl:choose>
			<xsl:when test="../size[@units='page']">.</xsl:when>
			<xsl:otherwise>;</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="volume" mode="element-content">
		<span class="data">
		<xsl:apply-templates/>
				<xsl:choose>
					<xsl:when test="../issue or ../supplement"/>
										<xsl:otherwise>:</xsl:otherwise>
		</xsl:choose>
		</span>
	</xsl:template>
	<xsl:template match="issue" mode="element-content">
		<span class="data">
		<xsl:choose>
			<xsl:when test="../issue-title">(<xsl:apply-templates/>
			</xsl:when>
			<xsl:otherwise>(<xsl:apply-templates/>):</xsl:otherwise>
		</xsl:choose>
		</span>
	</xsl:template>
	<xsl:template match="issue-part" mode="element-content">(<xsl:apply-templates/>):</xsl:template>
	<xsl:template match="issue-title" mode="element-content">&#160;<xsl:apply-templates/>):</xsl:template>
	<xsl:template match="supplement" mode="element-content">&#160;<xsl:apply-templates/>
				<xsl:choose>
			<xsl:when test="../fpage or ../lpage">:</xsl:when>
			<xsl:otherwise/>
				</xsl:choose>
	</xsl:template>
	<xsl:template match="fpage" mode="element-content">
		<xsl:choose>
			<xsl:when test="../page-range"/>
						<xsl:otherwise>
				<span class="data"><xsl:value-of select="."/></span>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="lpage" mode="element-content">
		<xsl:choose>
			<xsl:when test="../page-range"/>
						<xsl:when test="../fpage =.">.</xsl:when>
			<xsl:otherwise>
				<span class="data">-<xsl:value-of select="."/>.</span>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="page-range" mode="element-content">
		<span class="data"><xsl:value-of select="."/>.</span>
	</xsl:template>
	<xsl:template match="size" mode="element-content">
		&#160;<xsl:value-of select="."/>.
	</xsl:template>
	<xsl:template match="series" mode="element-content">
		<span class="data">&#160;(<xsl:value-of select="."/>).</span>
	</xsl:template>
	<xsl:template match="date-in-citation" mode="element-content">
		<xsl:choose>
			<xsl:when test="@content-type='epub'">&#160;
				<xsl:apply-templates/>.</xsl:when>
			<xsl:otherwise>
				[
				<xsl:apply-templates/>
				];
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="etal" mode="element-content">
		&#160;<i>et al.</i>
	</xsl:template>
	<xsl:template match="comment" mode="element-content">&#160;<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="isbn" mode="element-content">
		&#160;ISBN:<xsl:value-of select="."/>.
	</xsl:template>
	<xsl:template match="uri">
		&#160;<a href="{.}" target="_blank"><xsl:value-of select="."/></a>
	</xsl:template>
	<xsl:template match="ext-link" mode="mixed-content">
		<a href="{@xlink:href}" target="_blank">
		<xsl:apply-templates/>
		</a>
	</xsl:template>
	<xsl:template match="uri" mode="mixed-content">
		<a href="{.}"><xsl:value-of select="."/></a>
	</xsl:template>
	<xsl:template match="pub-id" mode="element-content">
		<xsl:choose>
			<xsl:when test="@pub-id-type='pmid'">&#160;PMID<a href="http://www.ncbi.nlm.nih.gov/pubmed/{normalize-space(.)}" target="_blank"><xsl:value-of select="."/></a>
			</xsl:when>
			<xsl:when test="@pub-id-type='doi'">&#160;doi:<xsl:value-of select="."/>
			</xsl:when>
			<xsl:otherwise>&#160;<xsl:value-of select="."/>.
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="pub-id" mode="mixed-content">
		<xsl:choose>
			<xsl:when test="@pub-id-type='pmid'">&#160;PMID<a href="http://www.ncbi.nlm.nih.gov/pubmed/{normalize-space(.)}" target="_blank"><xsl:value-of select="."/></a>
			</xsl:when>
			<xsl:when test="@pub-id-type='doi'">&#160;doi:<xsl:value-of select="."/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	<!--   Fim das referências 3.0   --><!--     ************************************     Referências na versão citation (2.?)     ************************************     --><!--     **********************     Fim de referências 2.?     **********************     --><!--Notas do Artigo [foot notes]-->
	<xsl:template match="fn-group">
		<div><a name="footnotes-nav">
			<xsl:choose>
				<!--Exibição das notas para o artigo para título em inglês-->
				<xsl:when test="../../@xml:lang='en'">
					<p class="sec">Footnotes</p>
				</xsl:when>
				<!--Exibição para artigo em português-->
				<xsl:when test="../../@xml:lang='pt'">
					<p class="sec">Notas de Rodapé</p>
				</xsl:when>
				<!--Exibição para artigo em espanhol-->
				<xsl:when test="../../@xml:lang='es'">
					<p class="sec">Notas al pie</p>
				</xsl:when>
			</xsl:choose>
			</a>
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	<xsl:template match="fn-group/fn">
		<a name="{@id}">
		<p class="fn">
			<xsl:apply-templates select="*" mode="fn-group"/>
		</p>
		</a>
	</xsl:template>
	<xsl:template match="fn-group/fn[@fn-type='supplementary-material']/label" mode="fn-group">
		<sup><xsl:value-of select="."/></sup>
	</xsl:template>
	<xsl:template match="ext-link">
		<a href="{@xlink:href}" target="_blank"><xsl:value-of select="text()"/></a>
	</xsl:template>
	<xsl:template match="xref">

		<xsl:if test="text()!='' or label">
            
            	<!--a href="#{@rid}" data-tooltip="t{@rid}"-->
				<a href="#{@rid}">
				    <xsl:apply-templates select=".//text()"/>
				</a>
			
		</xsl:if>
	</xsl:template>
    <xsl:template match="xref[@ref-type='bibr']">
		<sup>
		<xsl:if test="text()!='' or label">
            
            	<!--a href="#{@rid}" data-tooltip="t{@rid}"-->
				<a href="#{@rid}">
				    <xsl:apply-templates select=".//text()"/>
				</a>
			
		</xsl:if></sup>
	</xsl:template>
	<xsl:template match="sup/xref[@ref-type='bibr']">
		
		<xsl:if test="text()!='' or label">
            
            	<!--a href="#{@rid}" data-tooltip="t{@rid}"-->
				<a href="#{@rid}">
				    <xsl:apply-templates select=".//text()"/>
				</a>
			
		</xsl:if>
	</xsl:template>
    <xsl:template match="ack//title">
    	<p class="sec">
            	<xsl:apply-templates select="*|text()"/></p>
    </xsl:template>

    <xsl:template match="ack">
        <xsl:if test="not(.//title)">
            <p class="sec">
            	Acknowledgements</p>
            </xsl:if>
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="day|year"><xsl:value-of select="."/></xsl:template>
</xsl:stylesheet>
