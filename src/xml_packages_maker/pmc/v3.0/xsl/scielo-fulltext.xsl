<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">


	<xsl:variable name="HOWTODISPLAY"><xsl:choose>
		<xsl:when test="//SIGLUM='bjmbr'">STANDARD</xsl:when><xsl:otherwise>STANDARD</xsl:otherwise>
	</xsl:choose></xsl:variable>
	
	<xsl:variable name="refpos">
		<xsl:choose>
			<xsl:when test="$xml_article">
				<xsl:apply-templates select="document($xml_article)//ref" mode="scift-position"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select=".//ref" mode="scift-position"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>



	<xsl:variable name="article_lang">
		<xsl:value-of select="$xml_article_lang"/>
	</xsl:variable>

	<xsl:variable name="display_objects">
		<xsl:value-of select="$xml_display_objects"/>
	</xsl:variable>

	<xsl:template match="ref" mode="scift-position">{<xsl:value-of select="@id"/>}<xsl:value-of
			select="position()"/>{/<xsl:value-of select="@id"/>}</xsl:template>
	<xsl:template match="ref" mode="scift-get_position">
		<xsl:variable name="id" select="@id"/>
		<xsl:value-of
			select="substring-after(substring-before($refpos,concat('{/',$id,'}')),concat('{',$id,'}'))"
		/>
	</xsl:template>


	<xsl:template match="article" mode="text-content">
		<xsl:call-template name="scift-make-article"/>		
	</xsl:template>
	<xsl:template match="sub-article | response">
		<hr class="part-rule"/>
		<xsl:call-template name="scift-make-article"/>
	</xsl:template>
	<xsl:template name="scift-make-article">
		<!-- Generates a series of (flattened) divs for contents of any
	       article, sub-article or response -->
		
		<!-- variable to be used in div id's to keep them unique -->
		<xsl:variable name="this-article">
			<xsl:apply-templates select="." mode="id"/>
		</xsl:variable>
		
		<div id="{$this-article}-front" class="front">
			<xsl:apply-templates select="front | front-stub"/>
		</div>
		
		<!-- body -->
		<xsl:for-each select="body">
			<div id="{$this-article}-body" class="body">
				<xsl:apply-templates/>
			</div>
		</xsl:for-each>
		
		<xsl:if test="back | $loose-footnotes">
			<!-- $loose-footnotes is defined below as any footnotes outside
           front matter or fn-group -->
			<div id="{$this-article}-back" class="back">
				<xsl:call-template name="make-back"/>
			</div>
		</xsl:if>
		
		<xsl:for-each select="floats-group">
			<div id="{$this-article}-floats" class="back">
				<xsl:call-template name="main-title">
					<xsl:with-param name="contents">
						<span class="generated">Floating objects</span>
					</xsl:with-param>
				</xsl:call-template>
				<xsl:apply-templates/>
			</div>
		</xsl:for-each>
		
		<div class="foot-notes">
			<xsl:apply-templates select="front//article-meta//history"/>
			<xsl:apply-templates select="front//article-meta//author-notes"/>
		</div>
		<xsl:apply-templates select="sub-article | response"/>
		<div class="foot-notes">
			<xsl:apply-templates select="front//article-meta//permissions"/>
		</div>
	</xsl:template>
	<xsl:template match="front">
		<xsl:apply-templates select="article-meta//article-categories"/>
		<xsl:apply-templates select="article-meta//title-group"/>
		<xsl:apply-templates select="../sub-article[@article-type='translation']//title-group"/>
		<xsl:apply-templates select="article-meta//contrib-group"/>
		<xsl:apply-templates select="article-meta//aff"/>
		<xsl:apply-templates
			select="article-meta//abstract | ../sub-article[@article-type='translation']//abstract"/>
		<xsl:apply-templates select="article-meta//trans-abstract"/>
	</xsl:template>
	<xsl:template match="front-stub">
	</xsl:template>
	<xsl:template match="abstract | trans-abstract">
		<xsl:variable name="lang" select="@xml:lang"/>
		<div>
			<!--Apresenta o título da seção conforme a lingua existente-->
			<xsl:attribute name="class">
				<xsl:value-of select="name()"/>
			</xsl:attribute>
			<xsl:if test="not(title)">
				<xsl:choose>
					<xsl:when test="$lang='pt'">
						<p class="sec">
							<a name="resumo">RESUMO</a>
						</p>
					</xsl:when>
					<xsl:when test="$lang='es'">
						<p class="sec">
							<a name="resumen">RESUMEN</a>
						</p>
					</xsl:when>
					<xsl:otherwise>
						<p class="sec">
							<a name="abstract">ABSTRACT</a>
						</p>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			<xsl:apply-templates select="* | text()"/>
			<xsl:apply-templates
				select="..//kwd-group[normalize-space(@xml:lang)=normalize-space($lang)]"
				mode="keywords-with-abstract"/>
		</div>
	</xsl:template>
	
	<xsl:template match="kwd-group" mode="keywords-with-abstract">
		<xsl:variable name="lang" select="normalize-space(@xml:lang)"/>
		<!--xsl:param name="test" select="1"/>     <xsl:value-of select="$test"/-->
		<p>
			<!--Define o nome a ser exibido a frente das palavras-chave conforme o idioma-->
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
		<xsl:if test="position()!= 1">; </xsl:if>
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template name="main-title"
		match="abstract/title | body/*/title |
		back/title | back[not(title)]/*/title">
		<xsl:param name="contents">
			<xsl:apply-templates/>
		</xsl:param>
		<xsl:if test="normalize-space($contents)">
			<!-- coding defensively since empty titles make glitchy HTML -->
			<p class="sec">
				<xsl:copy-of select="$contents"/>
			</p>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="section-title"
		match="abstract/*/title | trans-abstract/*/title | body/*/*/title |
		back[title]/*/title | back[not(title)]/*/*/title">
		<xsl:param name="contents">
			<xsl:apply-templates/>
		</xsl:param>   
		<xsl:if test="normalize-space($contents)">
			<!-- coding defensively since empty titles make glitchy HTML -->
			<p class="sub-subsec">
				<xsl:copy-of select="$contents"/>
			</p>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="subsection-title"
		match="abstract/*/*/title | body/*/*/*/title |
		back[title]/*/*/title | back[not(title)]/*/*/*/title">
		<xsl:param name="contents">
			<xsl:apply-templates/>
		</xsl:param>   
		<xsl:if test="normalize-space($contents)">
			<!-- coding defensively since empty titles make glitchy HTML -->
			<p class="subsection-title">
				<xsl:copy-of select="$contents"/>
			</p>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="title-group/article-title">
		<div>
			<p class="title">
				<xsl:apply-templates select="* | text() "/>
				<xsl:apply-templates select="../subtitle"  mode="scift-subtitle"/>
			</p>
		</div>
	</xsl:template>
	<xsl:template match="trans-title-group/trans-title">
		<div>
			<p class="trans-title">
				<xsl:apply-templates select="* | text() "/>
				<xsl:apply-templates select="../trans-subtitle"  mode="scift-subtitle"/>
			</p>
		</div>
	</xsl:template>
	<!--Subtitulos do artigo-->
	<xsl:template match="title-group/subtitle | trans-title-group/trans-subtitle"  mode="scift-subtitle">
		<span>
			<xsl:apply-templates select="* | text()"/>
		</span>
	</xsl:template>
	<xsl:template match="title-group/subtitle | trans-title-group/trans-subtitle"/>
	<!--Categoria do artigo     	Talvez seja desenecessária essa informação     -->
	<xsl:template match="subj-group/subject">
		<p class="categoria">
			<xsl:value-of select="."/>
		</p>
	</xsl:template>
	<!--Div contendo nome dos autores-->
	<xsl:template match="contrib-group">
		<div class="autores">
			<xsl:apply-templates select="contrib"/>
		</div>
	</xsl:template>
	<xsl:template match="role">, <xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="sub-article//role">
		<p class="role">
			<xsl:value-of select="."/>
		</p>
	</xsl:template>
	<xsl:template match="contrib">
		<xsl:if test="position()!=1">, </xsl:if>
		<xsl:apply-templates select="*|text()"/>
		
	</xsl:template>
	<xsl:template match="contrib/name">
		<xsl:if test="prefix"><xsl:apply-templates select="prefix"/>&#160;</xsl:if>
		<xsl:apply-templates select="given-names"/>&#160;<xsl:apply-templates select="surname"/>
		<xsl:if test="suffix">&#160;<xsl:apply-templates select="suffix"/></xsl:if>
	</xsl:template>
	<xsl:template match="aff">
		<p class="aff">
			<xsl:variable name="text">
				<xsl:apply-templates select="text() | add-line/text()" mode="aff-text"/>
			</xsl:variable>
			<xsl:comment><xsl:value-of select="$text"/></xsl:comment>
			<xsl:comment><xsl:value-of select="string-length($text)"></xsl:value-of></xsl:comment>
			<xsl:variable name="parts" select="count(text()[normalize-space(.)!=''] | institution | addr-line | country | email)"/>
			
			<xsl:if test="label">
				<a name="{@id}">
					<xsl:apply-templates select="label"/>
				</a>
			</xsl:if>
			
			
			<xsl:choose>
				<xsl:when test="$text=''">
					<xsl:comment>aff has no separators = work around to insert separtors</xsl:comment>
					<xsl:apply-templates select="institution | addr-line | country | email"
						mode="aff-insert-separator"/>
				</xsl:when>
				<xsl:when test="translate($text,',', '')!=''">
					<xsl:comment>text unlabeled = ok</xsl:comment>
					<xsl:apply-templates select="text()[normalize-space(.)!=''] | institution | addr-line | country | email"/>
				</xsl:when>
				<xsl:when test="string-length($text) = $parts - 1">
					<xsl:comment>aff has <xsl:value-of select="string-length($text)"/> separators</xsl:comment>
					<xsl:apply-templates select="text()[normalize-space(.)!=''] | institution | addr-line | country | email"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:comment>aff has <xsl:value-of select="string-length($text)"/> separators. Deberia ter <xsl:value-of select="$parts - 1"/></xsl:comment>
					<xsl:apply-templates select="text()[normalize-space(.)!=''] | institution | addr-line | country | email"
						mode="aff-insert-separator"/>
				</xsl:otherwise>
			</xsl:choose>
			
			
		</p>
	</xsl:template>
	<xsl:template match="text()" mode="aff-text">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
	<xsl:template match="text()[normalize-space(.)=',']" mode="aff-insert-separator">
	</xsl:template>
	<xsl:template match="aff/*" mode="aff-insert-separator"><xsl:if test="position()!=1">, </xsl:if>
		<xsl:apply-templates select="*|text()" mode="aff-insert-separator"/>
	</xsl:template>
	<xsl:template match="aff/addr-line" mode="aff-insert-separator"><xsl:if test="position()!=1">, </xsl:if>
		<xsl:apply-templates select="*" mode="aff-insert-separator"/>
	</xsl:template>
	<xsl:template match="addr-line/*">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	
	<xsl:template match="addr-line/*" mode="aff-insert-separator"><xsl:if test="position()!=1">, </xsl:if>
		<xsl:apply-templates select="*|text()" mode="aff-insert-separator"/>
	</xsl:template>
	
	<xsl:template match="aff/label">
		<sup>
			<xsl:value-of select="."/>
		</sup>
	</xsl:template>
	<!--     *****     Email     **********************************************************************************     Nota:Se houver algum e-mail no resto do artigo também serpa aplicado este template     **********************************************************************************     -->
	<xsl:template match="email">
		<a href="mailto:{text()}">
			<xsl:value-of select="."/>
		</a>
	</xsl:template>
	<xsl:template match="email" mode="element-content"> &#160;<a href="mailto:{text()}"
		><xsl:value-of select="."/></a>
	</xsl:template>
	<xsl:template match="email" mode="mixed-content">
		<a href="mailto:{text()}">
			<xsl:value-of select="."/>
		</a>
	</xsl:template>
	<xsl:template match="aff/email">, <a href="mailto:{text()}"><xsl:value-of select="."/></a>
	</xsl:template>
	
	<xsl:template match="xref">
		
		<a href="#{@rid}">
			
			<xsl:apply-templates select="*|text()"/>
		</a>
		
	</xsl:template>
	
	
	
	
	<xsl:template match="xref[@ref-type='bibr']">
		
		<xsl:choose>
			<xsl:when test="normalize-space(.//text())=''"><sup>
				<a href="#{@rid}">
					<xsl:apply-templates select="key('element-by-id',@rid)"
						mode="label-text">
						<xsl:with-param name="warning" select="true()"/>
					</xsl:apply-templates>
				</a>
			</sup></xsl:when>
			<xsl:when test="not(.//sup)"><sup>
				<a href="#{@rid}">
					<xsl:apply-templates select="*|text()"/>
				</a>
				</sup></xsl:when>
			<xsl:otherwise>
				<a href="#{@rid}">
					<xsl:apply-templates select="*|text()"/>
				</a>
			</xsl:otherwise>
		</xsl:choose>				
	</xsl:template>
	<xsl:template match="fig | table-wrap">
		<xsl:comment><xsl:value-of select="$HOWTODISPLAY"/></xsl:comment>
		<xsl:choose>
			<xsl:when test="$HOWTODISPLAY = 'THUMBNAIL'">
				<!--xsl:apply-templates select="." mode="scift-thumbnail"></xsl:apply-templates-->				
			</xsl:when>
			<xsl:when test="$HOWTODISPLAY = 'STANDARD'">				
				<xsl:apply-templates select="." mode="scift-standard"/>
			</xsl:when>		
			
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="fig" mode="scift-standard">
		<div class="figure">
			
			<xsl:call-template name="named-anchor"/>
			<xsl:apply-templates select="graphic"/>
			<p class="label_caption">
				<xsl:apply-templates select="label | caption" mode="scift-label-caption-graphic"/>
				
			</p>
			
		</div>
	</xsl:template>
	<xsl:template match="table-wrap" mode="scift-standard">
		<div class="table-wrap">
			
			<xsl:call-template name="named-anchor"/>
			
			<p class="label_caption">
				<xsl:apply-templates select="label | caption" mode="scift-label-caption-graphic"/>
				
			</p>
			<xsl:apply-templates select="graphic | table"/>
			<xsl:apply-templates mode="footnote" select=".//fn"/>
		</div>
	</xsl:template>
	<xsl:template match="fig/label | table-wrap/label | fig/caption | table-wrap/caption">
		<span class="{name()}">
			<xsl:apply-templates select="* | text()"/>
		</span>
	</xsl:template>
	<xsl:template match="table-wrap[not(.//graphic)]" mode="scift-thumbnail">
		<xsl:apply-templates select="." mode="scift-standard"></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="fig | table-wrap[.//graphic]" mode="scift-thumbnail">
		<div class="{local-name()} panel">
			<xsl:call-template name="named-anchor"/>
			<table class="table_thumbnail">
				<tr>
					<td class="td_thumbnail"><xsl:apply-templates select=".//graphic" mode="scift-thumbnail"/></td>
					<td class="td_label_caption">
						<p class="label_caption">
							<xsl:apply-templates select="label | caption" mode="scift-label-caption-graphic"/>
							
						</p>
						<xsl:apply-templates mode="footnote"
							select=".//fn"/>
					</td>					
				</tr>				
			</table>
		</div>
	</xsl:template>
	<xsl:template match="disp-formula">
		<p class="{local-name()} panel">
			<xsl:apply-templates/>
		</p>
	</xsl:template>
	<xsl:template match="graphic">
		<a target="_blank">			
			<xsl:apply-templates select="@xlink:href" mode="scift-attribute-href"/>
			<img class="graphic">
				<xsl:apply-templates select="@xlink:href" mode="scift-attribute-src"/>
			</img>
		</a>
	</xsl:template>
	
	<xsl:template match="inline-graphic | disp-formula/graphic">
		<a target="_blank">			
			<xsl:apply-templates select="@xlink:href" mode="scift-attribute-href"/>
			<img class="formula">
				<xsl:apply-templates select="@xlink:href" mode="scift-attribute-src"/>
			</img>
		</a>
	</xsl:template>
	<xsl:template match="graphic" mode="scift-thumbnail">
		<a target="_blank">			
			<xsl:apply-templates select="@xlink:href" mode="scift-attribute-href"/>
			<img class="thumbnail">
				<xsl:apply-templates select="@xlink:href" mode="scift-attribute-src"/>
			</img>
		</a>
	</xsl:template>
	<xsl:template match="@href | @xlink:href" mode="scift-fix-href">		
		<xsl:variable name="src"><xsl:value-of select="$var_IMAGE_PATH"/><xsl:choose><xsl:when
		test="contains(., '.tif')"><xsl:value-of select="substring-before(.,'.tif')"
		/></xsl:when><xsl:otherwise><xsl:value-of select="."
		/></xsl:otherwise></xsl:choose></xsl:variable>
		<xsl:value-of select="$src"/><xsl:if test="not(contains($src,'.jpg'))">.jpg</xsl:if>
	</xsl:template>
	<xsl:template match="@href | @xlink:href" mode="scift-attribute-href">
		<xsl:attribute name="href">
			<xsl:apply-templates select="." mode="scift-fix-href"/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="@href | @xlink:href" mode="scift-attribute-src">
		<xsl:attribute name="src">
			<xsl:apply-templates select="." mode="scift-fix-href"/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template match="label|caption" mode="scift-label-caption-graphic">
		<span class="{name()}"><xsl:apply-templates select="text() | *" mode="scift-label-caption-graphic"/>&#160;</span>
	</xsl:template>
	<xsl:template match="title" mode="scift-label-caption-graphic">
		<xsl:apply-templates select="text() | *" />			
	</xsl:template>
	
	
	<xsl:template match="sec[@sec-type]">
		<div class="section">
			<xsl:call-template name="named-anchor"/>
			<xsl:apply-templates select="title"/>
			<xsl:apply-templates select="sec-meta"/>
			<xsl:apply-templates mode="drop-title"/>
		</div>
		<xsl:choose>
			<xsl:when test="$HOWTODISPLAY= 'STANDARD'"></xsl:when>
			<xsl:when test="$HOWTODISPLAY= 'THUMBNAIL'">
				<xsl:apply-templates select=".//fig|.//table-wrap[.//graphic]" mode="scift-thumbnail">
					<xsl:sort select="@id"/>
				</xsl:apply-templates>
			<hr/>
			</xsl:when>
		</xsl:choose>		
		
	</xsl:template>
	
	<xsl:template match=" back/ref-list">
		<div>
			<a name="references"></a>
			<p class="sec">
			<xsl:apply-templates select="title"/>
			
			<xsl:if test="not(title)">
				<xsl:choose>					
					<xsl:when test="$article_lang='pt'"> REFERÊNCIAS </xsl:when>
					<xsl:when test="$article_lang='es'"> REFERENCIAS </xsl:when>
					<xsl:otherwise> REFERENCES </xsl:otherwise>
				</xsl:choose>
			</xsl:if>			</p>
			<xsl:apply-templates select="ref"/>
		</div>
	</xsl:template>
	
	<xsl:template match="ref">
		<p class="ref">
			<a name="{@id}"></a>
			<xsl:choose>
				<xsl:when test="label and mixed-citation">
					<xsl:if test="substring(mixed-citation,1,string-length(label))!=label">
						<xsl:value-of select="label"/>.&#160; 
					</xsl:if>
				</xsl:when>
				<xsl:when test="label"><xsl:value-of select="label"/>.&#160; </xsl:when>
				<!--xsl:otherwise><xsl:value-of select="position()"/>.&#160; </xsl:otherwise-->
			</xsl:choose> 
			<xsl:choose>
				<xsl:when test="mixed-citation">						
					<xsl:apply-templates select="mixed-citation"/>
				</xsl:when>
				<xsl:when test="$version='xml'">
					<xsl:apply-templates select="citation"/>
				</xsl:when>
				<!--xsl:when test="element-citation">
					<xsl:apply-templates select="element-citation"/>
				</xsl:when>
				<xsl:when test="citation">
					<xsl:apply-templates select="citation"/>
				</xsl:when>
				<xsl:when test="nlm-citation">
					<xsl:apply-templates select="nlm-citation"/>
				</xsl:when-->
				<xsl:otherwise><xsl:comment>missing mixed-citation</xsl:comment></xsl:otherwise>
			</xsl:choose>
			
			<xsl:variable name="aref">000000<xsl:apply-templates select="." mode="scift-get_position"
			/></xsl:variable>
			<xsl:variable name="ref"><xsl:value-of
				select="substring($aref, string-length($aref) - 5)"/></xsl:variable>
			<xsl:variable name="pid"><xsl:value-of select="$PID"/><xsl:value-of
				select="substring($ref,2)"/></xsl:variable> [&#160;<a href="javascript:void(0);"
					onclick="javascript: window.open('/scielo.php?script=sci_nlinks&amp;pid={$pid}&amp;lng=en','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');"
					>Links</a>&#160;] </p>
	</xsl:template>
	
	
	<xsl:template match="mixed-citation | element-citation | nlm-citation | citation ">
		<xsl:apply-templates select="* | text()"/>
	</xsl:template>
	
	<xsl:template match="table">
		<xsl:variable name="class"><xsl:choose>
			<xsl:when test="$version='xml'">dotted_table</xsl:when><xsl:otherwise>table</xsl:otherwise>
		</xsl:choose></xsl:variable>
		<div  class="table">
			
			<table class="{$class}">
				<xsl:apply-templates select="@*|*|text()"></xsl:apply-templates></table>
		</div>
	</xsl:template>
	<xsl:template match="table//@*"><xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="table//*">
		<xsl:element name="{name()}">
			<xsl:if test=" name() = 'td' and $version='xml'">
				<xsl:attribute name="class">td</xsl:attribute>
			</xsl:if>
			
			<xsl:apply-templates select="@* | * | text()"/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="table-wrap-foot/fn">
		<p class="fn">
			<a name="{@id}">
				<xsl:apply-templates select="* | text()"/>
			</a>
		</p>
	</xsl:template>
	<xsl:template match="table-wrap-foot/fn/label"><sup><xsl:value-of select="."/></sup>
	</xsl:template>
	<xsl:template match="table-wrap-foot/fn/p">
		<xsl:apply-templates/>
	</xsl:template>
	
	<xsl:template match="history">
		<div class="history">
			<p>
				<xsl:apply-templates select="date"></xsl:apply-templates>
			</p>
		</div>
	</xsl:template>
	<xsl:template match="month" mode="date-month-en">
		<xsl:choose>
			<xsl:when test="text() = '01' or text() = '1'">January</xsl:when>
			<xsl:when test="text() = '02' or text() = '2'">February</xsl:when>
			<xsl:when test="text() = '03' or text() = '3'">March</xsl:when>
			<xsl:when test="text() = '04' or text() = '4'">April</xsl:when>
			<xsl:when test="text() = '05' or text() = '5'">May</xsl:when>
			<xsl:when test="text() = '06' or text() = '6'">June</xsl:when>
			<xsl:when test="text() = '07' or text() = '7'">July</xsl:when>
			<xsl:when test="text() = '08' or text() = '8'">August</xsl:when>
			<xsl:when test="text() = '09' or text() = '9'">September</xsl:when>
			<xsl:when test="text() = '10'">October</xsl:when>
			<xsl:when test="text() = '11'">November</xsl:when>
			<xsl:when test="text() = '12'">December</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="month" mode="date-month-es">
		<xsl:choose>
			<xsl:when test="text() = '01' or text() = '1'">Enero</xsl:when>
			<xsl:when test="text() = '02' or text() = '2'">Febrero</xsl:when>
			<xsl:when test="text() = '03' or text() = '3'">Marzo</xsl:when>
			<xsl:when test="text() = '04' or text() = '4'">Abril</xsl:when>
			<xsl:when test="text() = '05' or text() = '5'">Mayo</xsl:when>
			<xsl:when test="text() = '06' or text() = '6'">Junio</xsl:when>
			<xsl:when test="text() = '07' or text() = '7'">Julio</xsl:when>
			<xsl:when test="text() = '08' or text() = '8'">Agosto</xsl:when>
			<xsl:when test="text() = '09' or text() = '9'">Septiembre</xsl:when>
			<xsl:when test="text() = '10'">Octubre</xsl:when>
			<xsl:when test="text() = '11'">Noviembre</xsl:when>
			<xsl:when test="text() = '12'">Diciembre</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="month" mode="date-month-pt">
		<xsl:choose>
			<xsl:when test="text() = '01' or text() = '1'">Janeiro</xsl:when>
			<xsl:when test="text() = '02' or text() = '2'">Fevereiro</xsl:when>
			<xsl:when test="text() = '03' or text() = '3'">Março</xsl:when>
			<xsl:when test="text() = '04' or text() = '4'">Abril</xsl:when>
			<xsl:when test="text() = '05' or text() = '5'">Maio</xsl:when>
			<xsl:when test="text() = '06' or text() = '6'">Junho</xsl:when>
			<xsl:when test="text() = '07' or text() = '7'">Julho</xsl:when>
			<xsl:when test="text() = '08' or text() = '8'">Agosto</xsl:when>
			<xsl:when test="text() = '09' or text() = '9'">Setembro</xsl:when>
			<xsl:when test="text() = '10'">Outubro</xsl:when>
			<xsl:when test="text() = '11'">Novembro</xsl:when>
			<xsl:when test="text() = '12'">Dezembro</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="history/date/@date-type" mode="scift-as-label-en">
		<xsl:choose>
			<xsl:when test=". = 'rev-recd'">Revised</xsl:when>
			<xsl:otherwise><xsl:value-of select="translate(substring(.,1,1), 'ar', 'AR')"/><xsl:value-of select="substring(.,2)"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="history/date/@date-type" mode="scift-as-label-pt">
		<xsl:choose>
			<xsl:when test=". = 'rev-recd'">Revisado</xsl:when>
			<xsl:when test=". = 'accepted'">Aceito</xsl:when>
			<xsl:when test=". = 'received'">Recebido</xsl:when>
			</xsl:choose>
	</xsl:template>
	<xsl:template match="history/date/@date-type" mode="scift-as-label-es">
		<xsl:choose>
			<xsl:when test=". = 'rev-recd'">Revisado</xsl:when>
			<xsl:when test=". = 'accepted'">Aprobado</xsl:when>
			<xsl:when test=". = 'received'">Recibido</xsl:when>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="history/date">		
		<xsl:choose>
			<xsl:when test="$article_lang='en'">
				<xsl:apply-templates select="@date-type" mode="scift-as-label-en"/>: <xsl:apply-templates select="month" mode="date-month-en"/><xsl:value-of select="concat(' ',day)"/>,  <xsl:value-of select="year"/>
			</xsl:when>
			<xsl:when test="$article_lang='pt'">
				<xsl:apply-templates select="@date-type" mode="scift-as-label-pt"/>: <xsl:value-of select="day"/> de <xsl:apply-templates select="month" mode="date-month-pt"/> de <xsl:value-of select="year"/>
			</xsl:when>
			<xsl:when test="$article_lang='es'">
				<xsl:apply-templates select="@date-type" mode="scift-as-label-es"/>: <xsl:value-of select="day"/> de <xsl:apply-templates select="month" mode="date-month-es"/> de <xsl:value-of select="year"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="@date-type" mode="scift-as-label-en"/>: <xsl:apply-templates select="month" mode="date-month-en"/>
				<xsl:value-of select="concat(' ',day)"/>,  <xsl:value-of select="year"/>
			</xsl:otherwise>
		</xsl:choose><xsl:if test="position()!=last()">; </xsl:if>
	</xsl:template>
	
	
	<xsl:template match="author-notes">
		<div class="author-notes">
			<xsl:apply-templates select=" corresp | .//fn | text()"></xsl:apply-templates>
		</div>		
	</xsl:template>
	
	<xsl:template match="author-notes//@id"><a name="{.}"/></xsl:template>
	<xsl:template match="author-notes/corresp">
		<p class="corresp">
			<xsl:apply-templates select="@* | *|text()"></xsl:apply-templates>
		</p>	
	</xsl:template>
	
	<xsl:template match="author-notes/fn">
		<xsl:apply-templates select="@* | *|text()"></xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="corresp/label | author-notes/fn/label">
		<sup>
			<xsl:value-of select="."/>
		</sup>	
	</xsl:template>
	
	<xsl:template match="author-notes//fn/@fn-type">
	</xsl:template>
	<xsl:template match="author-notes//fn/p">
		<p class="fn-author">
			<xsl:apply-templates select="*|text()"></xsl:apply-templates>
		</p>
	</xsl:template>
	<xsl:template match="fn-group/fn/p">
		<p class="fn">
			<xsl:apply-templates select="*|text()"></xsl:apply-templates>
		</p>
	</xsl:template>
	
	<xsl:template match="sub-article[@article-type!='translation' or not(@article-type)]">
		<div class="sub-article" id="{@id}">
			<xsl:apply-templates select=".//title-group"/>
			
			
			<xsl:apply-templates select=".//abstract"/>
			
			<xsl:apply-templates select=".//trans-abstract"/>
			
			<div class="body">
				<xsl:apply-templates select="body"/>
			</div>
			
			<xsl:apply-templates select="back "/>
			
			<div class="sig-block">
				<xsl:apply-templates select=".//contrib-group"/>
				
				<xsl:apply-templates select=".//aff"/>
			</div>
			
		</div>
		
	</xsl:template>
	
	<xsl:template match="sub-article[@article-type='translation']">
		<div class="sub-article" id="{@id}">
			<xsl:apply-templates select=".//title-group"/>
			
			<div class="body">
				<xsl:apply-templates select="body"/>
			</div>
			
			<xsl:apply-templates select="back "/>
			
			
		</div>
		
	</xsl:template>
</xsl:stylesheet>
