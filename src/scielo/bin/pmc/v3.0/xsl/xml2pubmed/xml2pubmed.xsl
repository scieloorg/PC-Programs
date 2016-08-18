<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:xlink="http://www.w3.org/1999/xlink" exclude-result-prefixes="xlink">
	<!-- http://www.ncbi.nlm.nih.gov/books/NBK3828/ -->

	<!-- 
	<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.4//EN" "http://www.ncbi.nlm.nih.gov/entrez/query/static/PubMed.dtd">

	-->
	<!-- 		
				<pub-date pub-type="epub|ppub|epub-ppub|collection">
		                <month>09</month>
		                <year>2016</year>
		        </pub-date>

		AOP = 1 DATA (epub)
			* em journal-meta data do tipo aheadofprint do artigo (sempre terá dia, mês e ano)
				<PubDate PubStatus="aheadofprint"> <Year>2016</Year> <Month>07</Month> <Day>11</Day> </PubDate>
			* em history NADA
		EXCLUSÃO DE AOP = 2 DATAS (epub + collection)
			* em journal-meta data do tipo ppublish do fascículo (sempre terá mês ou intervalo de meses e ano)
				<PubDate PubStatus="ppublish"> <Month>09</Month> <Year>2016</Year> </PubDate>			
			** em history data do tipo aheadofprint do artigo (sempre terá dia, mês e ano)
				<PubDate PubStatus="aheadofprint"> <Year>2016</Year> <Month>07</Month> <Day>11</Day> </PubDate>
		RPASS = 2 DATAS (epub + ppub ou somente epub?)
			* em journal-meta data do tipo ppublish do fascículo (sempre terá ano)
				<PubDate PubStatus="ppublish"> <Year>2016</Year> </PubDate>			
			** em history data do tipo aheadofprint do artigo (sempre terá dia, mês e ano)
				<PubDate PubStatus="aheadofprint"> <Year>2016</Year> <Month>07</Month> <Day>11</Day> </PubDate>
		FASCÍCULO = 1 DATA
			* em journal-meta data do tipo ppublish do fascículo (sempre terá mês ou intervalo de meses e ano)
	        	<PubDate PubStatus="ppublish"> <Month>09</Month> <Year>2016</Year> </PubDate>
			* em history NADA
	-->
	<xsl:output 
		doctype-public="-//NLM//DTD PubMed 2.6//EN" 
		doctype-system="http://www.ncbi.nlm.nih.gov/entrez/query/static/PubMed.dtd" 
		encoding="UTF-8" method="xml" omit-xml-declaration="no" version="1.0"
		indent="yes" xml:space="default" 
	/>
	<xsl:variable name="pid_list" select="//pid-set//pid"/>
	<xsl:variable name="articles" select="//article-item"/>
	
	<xsl:template match="/">
		<ArticleSet>
			<xsl:apply-templates select="//pid-set//pid"/>
			<!--xsl:apply-templates select=".//article-set//article-item">
				<xsl:sort select="article//article-meta/pub-date[@pub-type='epub']/month" order="ascending" data-type="number"/>
				<xsl:sort select="article//article-meta/pub-date[@pub-type='epub']/day" order="ascending" data-type="number"/>
				<xsl:sort select="article//article-meta/fpage" order="ascending" data-type="number"/>
			</xsl:apply-templates-->	
			
		</ArticleSet>
	</xsl:template>
	
	<xsl:template match="pid">
		<xsl:variable name="f" select="@filename"/>
		<xsl:apply-templates select="$articles[@filename=$f]/article">
			<xsl:with-param name="pid" select="."></xsl:with-param>
		</xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="article-item">
		<xsl:variable name="f" select="@filename"/>
		<xsl:comment><xsl:value-of select="$f"/></xsl:comment>
		<xsl:apply-templates select="article">
			<xsl:with-param name="pid" select="$pid_list[@filename=$f]"></xsl:with-param>
		</xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="article">
		<xsl:param name="pid"/>
		<Article>
			<Journal>
				<xsl:apply-templates select="." mode="scielo-xml-publisher_name"/>
				<xsl:apply-templates select="." mode="scielo-xml-journal_title"/>
				<xsl:apply-templates select="." mode="scielo-xml-issn"/>
				<xsl:apply-templates select="." mode="scielo-xml-volume_id"/>
				<xsl:apply-templates select="." mode="scielo-xml-issue_no"/>
				<xsl:apply-templates select="." mode="scielo-xml-publishing_dateiso"/>
			</Journal>
			<xsl:if test=".//article-meta/article-id[@specific-use='previous-pid']">
				<Replaces IdType="pii">
					<xsl:apply-templates select=".//article-meta/article-id[@specific-use='previous-pid']" mode="scielo-xml-pii"/>
				</Replaces>
			</xsl:if>
			<xsl:apply-templates select="." mode="scielo-xml-title"/>

			<xsl:apply-templates select=".//article-meta/fpage|.//article-meta/lpage|.//article-meta/elocation-id"/>
			<ELocationID EIdType="pii">
				<xsl:value-of select="$pid"/>
			</ELocationID>
			<xsl:if test=".//article-meta/article-id[@pub-id-type='doi']">
				<ELocationID EIdType="doi">
					<xsl:value-of select=".//article-meta/article-id[@pub-id-type='doi']"/>
				</ELocationID>
			</xsl:if>
			<xsl:apply-templates
				select="@xml:lang|.//sub-article[@article-type='translation']/@xml:lang"
				mode="scielo-xml-languages"/>
			<!-- FIXED 20040504 
			Roberta Mayumi Takenaka
			Solicitado por Solange email: 20040429
			Para artigos que não tenham autores, não gerar a tag </AuthorList>.			
			-->
			<xsl:if test="count(.//front//contrib) + count(.//front//collab) &gt; 0">
				<AuthorList>
					<xsl:apply-templates select=".//front//contrib" mode="scielo-xml-author"/>
					<xsl:apply-templates select=".//front//collab" mode="scielo-xml-author"/>
				</AuthorList>
			</xsl:if>
			<PublicationType><xsl:apply-templates select="." mode="scielo-xml-publication-type"/></PublicationType>
			<ArticleIdList>
				<ArticleId IdType="pii">
					<xsl:choose>
						<xsl:when test=".//article-meta/article-id[@specific-use='previous-pid']">
							<xsl:apply-templates select=".//article-meta/article-id[@specific-use='previous-pid']" mode="scielo-xml-pii"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="$pid"/>
						</xsl:otherwise>
					</xsl:choose>
				</ArticleId>
				<ArticleId IdType="doi">
					<xsl:value-of select=".//front//article-id[@pub-id-type='doi']"/>
				</ArticleId>
			</ArticleIdList>
			<xsl:if test=".//front//history">
				<xsl:variable name="issueid"><xsl:value-of select="normalize-space(translate(concat(.//article-meta/volume,.//article-meta/issue),'0',' '))"/></xsl:variable>
				
				<History>
					<xsl:apply-templates select=".//article-meta//history/*"/>
					<xsl:if test="count(.//article-meta//pub-date)=1">
						<xsl:if test=".//article-meta//pub-date[@pub-type='epub' and day]">
							<xsl:apply-templates select=".//article-meta//pub-date[@pub-type='epub' and day]" mode="history"/>
						</xsl:if>
					</xsl:if>
				</History>
			</xsl:if>
			<xsl:apply-templates select="." mode="scielo-xml-abstract"/>
			<xsl:apply-templates select="." mode="scielo-xml-objects"/>
		</Article>
	</xsl:template>
	<xsl:template match="related-article[@related-article-type='corrected-article' or @related-article-type='retracted-article']" mode="scielo-xml-object">
		<xsl:param name="article_type"/>
		<ObjectList>
			<Object>
				<xsl:attribute name="Type"><xsl:choose>
					<xsl:when test="$article_type='correction'">Erratum</xsl:when>
					<xsl:when test="$article_type='retraction'">Retraction</xsl:when>
				</xsl:choose></xsl:attribute>
				<Param Name="type">pmid</Param>
				<Param Name="id"></Param>
			</Object>
		</ObjectList>
		<!--Object>
			<xsl:attribute name="Type"><xsl:choose>
				<xsl:when test="$article_type='correction'">Erratum</xsl:when>
				<xsl:when test="$article_type='retraction'">Retraction</xsl:when>
			</xsl:choose></xsl:attribute>
			<Param Name="type"><xsl:choose>
				<xsl:when test="@ext-link-type='doi'"><xsl:value-of select="@ext-link-type"/></xsl:when>
				<xsl:otherwise>pii</xsl:otherwise>
			</xsl:choose></Param>
			<Param Name="id"><xsl:value-of select="@xlink:href"/></Param>
		</Object-->
	</xsl:template>
	<xsl:template match="article" mode="scielo-xml-objects">
		<xsl:if test="@article-type='correction' or @article-type='retraction'">
			<ObjectList>
				<xsl:apply-templates select=".//related-article[@related-article-type='corrected-article' or @related-article-type='retracted-article']" mode="scielo-xml-object">
					<xsl:with-param name="article_type"><xsl:value-of select="@article-type"/></xsl:with-param>
				</xsl:apply-templates>
			</ObjectList>
		</xsl:if>
		<xsl:if test=".//ext-link[contains(@ext-link-type,'linical') and contains(@ext-link-type,'rial')]">
			<ObjectList>
				<xsl:apply-templates select=".//ext-link[contains(@ext-link-type,'linical') and contains(@ext-link-type,'rial')]" mode="object-clinical-trial"></xsl:apply-templates>
			</ObjectList>
		</xsl:if>
	</xsl:template>
	<xsl:template match="ext-link" mode="object-clinical-trial">
		<!-- 
		<ext-link ext-link-type="ClinicalTrial" xlink:href="https://clinicaltrials.gov/ct2/show/NCT00981734">NCT00981734</ext-link>
		-->
		<xsl:choose>
			<xsl:when test="contains(@xlink:href,'clinicaltrials.gov')">
				<Object Type="ClinicalTrials.gov">
					<Param Name="id"><xsl:choose>
						<xsl:when test="starts-with(.,'NCT')"><xsl:value-of select="."/></xsl:when>
						<xsl:when test="contains(@xlink:href,'/show/')"><xsl:value-of select="substring-after(@xlink:href,'/show/')"/></xsl:when>
						<xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
					</xsl:choose></Param>
				</Object>	
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="article[@article-type='case-report']" mode="scielo-xml-publication-type">Case Reports</xsl:template>
	<xsl:template match="article[@article-type='research-article']" mode="scielo-xml-publication-type">Journal Article</xsl:template>
	<xsl:template match="article[@article-type='corrected-article']" mode="scielo-xml-publication-type">Corrected and Republished Article</xsl:template>
	<xsl:template match="article[@article-type='correction']" mode="scielo-xml-publication-type">Published Erratum</xsl:template>
	<xsl:template match="article[@article-type='editorial']" mode="scielo-xml-publication-type">Editorial</xsl:template>
	<xsl:template match="article[@article-type='letter']" mode="scielo-xml-publication-type">Letter</xsl:template>
	<xsl:template match="article[@article-type='retraction']" mode="scielo-xml-publication-type">Retraction of Publication</xsl:template>
	<xsl:template match="article[@article-type='article-review']" mode="scielo-xml-publication-type">Review</xsl:template>
	
	<xsl:template match="article" mode="scielo-xml-publication-type">
		<xsl:choose>
			<xsl:when test="./article-meta//ext-link[@ext-link-type='ClinicalTrial']">Clinical Trial</xsl:when>
		</xsl:choose>
	</xsl:template>
	<!-- 
		case-report 	relato, descrição ou estudo de caso - pesquisas especiais que despertam interesse informativo.
		correction 	errata - corrige erros apresentados em artigos após sua publicação online/impressa.
		editorial 	editorial - uma declaração de opiniões, crenças e políticas do editor do periódico, geralmente sobre assuntos de significado científico de interesse da comunidade científica ou da sociedade.
		letter 	cartas - comunicação entre pessoas ou instituições através de cartas. Geralmente comentando um trabalho publicado
		research-article 	artigo original - abrange pesquisas, experiências clínicas ou cirúrgicas ou outras contribuições originais.
		retraction 	retratação - a retratação de um artigo científico é um instrumento para corrigir o registro acadêmico publicado equivocadamente, por plágio, por exemplo.
		review-article 	são avaliações críticas sistematizadas da literatura sobre determinado assunto.
		
		article-commentary 	comentários - uma nota crítica ou esclarecedora, escrita para discutir, apoiar ou debater um artigo ou outra apresentação anteriormente publicada. Pode ser um artigo, carta, editorial, etc. Estas publicações podem aparecer como comentário, comentário editorial, ponto de vista, etc.
		book-review 	resenha - análise críticas de livros e outras monografias.
		brief-report 	comunicação breve sobre resultados de uma pesquisa.
		in-brief 	press release - comunicação breve de linguagem jornalística sobre um artigo ou tema.
		other 	Outro tipo de documento. Pode ser considerado adendo, anexo, discussão, artigo de preocupação, introdução entre outros.
		rapid-communication 	comunicação breve sobre atualização de investigação ou outra notícia.
		reply 	resposta a carta ou ao comentário, geralmente é usado pelo autor original fazendo outros comentários a respeito dos comentários anteriores
		translation 	tradução. Utilizado para artigos que apresentam tradução de um artigo produzid
		-->
	<!-- 
	Addresses
	Bibliography
	Clinical Conference
	Congresses
	Consensus Development Conference
	Consensus Development Conference, NIH
	Festschrift
	Guideline
	Interview	
	Journal Article
	Lectures
	Meta-Analysis
	News
	Newspaper Article
	Observational Study
	Patient Education Handout
	Practice Guideline	
	
	Review
	Video-Audio Media
	Webcasts
	-->
	<xsl:template match="*" mode="scielo-xml-title">
		<!-- http://www.ncbi.nlm.nih.gov/books/NBK3828/#publisherhelp.ArticleTitle_O -->
		<xsl:element name="ArticleTitle">
			<xsl:if test="@xml:lang='en'">
				<xsl:apply-templates select=".//article-meta//title-group/article-title"/>
			</xsl:if>
			<xsl:apply-templates select=".//article-meta//title-group/article-title[@xml:lang='en']"/>
			<xsl:apply-templates select=".//article-meta//title-group/trans-title-group[@xml:lang='en']/trans-title"/>
			<xsl:apply-templates select=".//sub-article[@xml:lang='en']//article-title"/>
			<xsl:apply-templates select=".//sub-article//article-title[@xml:lang='en']"/>
		</xsl:element>
			<xsl:if test="@xml:lang != 'en'">
				<!-- http://www.ncbi.nlm.nih.gov/books/NBK3828/#publisherhelp.VernacularTitle_O -->
				<xsl:element name="VernacularTitle">
					<xsl:apply-templates select=".//article-meta//title-group//article-title"/>
				</xsl:element>
			</xsl:if>
	</xsl:template>

	<xsl:template match="@xml:lang" mode="scielo-xml-languages">
		<Language>
			<xsl:value-of select="translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
		</Language>
	</xsl:template>
	
	
	<xsl:template match="*" mode="scielo-xml-abstract">
		<Abstract>
			<xsl:if test="@xml:lang='en'">
				<xsl:apply-templates select=".//abstract"
					mode="scielo-xml-content-abstract"/>
			</xsl:if>
			
			<xsl:apply-templates select=".//*[contains(name(),'abstract') and @xml:lang='en']"
				mode="scielo-xml-content-abstract"/>
			<xsl:apply-templates select=".//sub-article[@xml:lang='en' and @article-type='translation']//abstract"
				mode="scielo-xml-content-abstract"/>
		</Abstract>
	</xsl:template>
	<xsl:template match="related-article[@related-article-type='corrected-article']" mode="label">corrects</xsl:template>
	<xsl:template match="related-article[@related-article-type='retracted-article']" mode="label">retracts</xsl:template>
	<xsl:template match="*[@article-type='correction' or @article-type='retraction']" mode="scielo-xml-abstract">
		<Abstract><xsl:apply-templates select=".//related-article[@related-article-type='corrected-article' or @related-article-type='retracted-article']" mode="related-article-abstract"></xsl:apply-templates></Abstract>
	</xsl:template>
	<xsl:template match="related-article[@related-article-type='corrected-article' or @related-article-type='retracted-article']" mode="related-article-abstract">
		[This <xsl:apply-templates select="." mode="label"/> the article <xsl:value-of select="@ext-link-type"/>: <xsl:value-of select="@xlink:href"/>]
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-content-abstract">
		<xsl:apply-templates select="*|text()" mode="scielo-xml-content-abstract"/>
	</xsl:template>
	<xsl:template match="*[sec]" mode="scielo-xml-content-abstract">
		<xsl:apply-templates select="sec|text()"  mode="scielo-xml-content-abstract"/>
	</xsl:template>
	<xsl:template match="*/sec" mode="scielo-xml-content-abstract">
		<AbstractText>
			<xsl:attribute name="Label"><xsl:apply-templates select="title"/></xsl:attribute>
			<xsl:apply-templates select="p"/>
		</AbstractText>
	</xsl:template>
	<!-- 
		<Abstract>
<AbstractText Label="OBJECTIVE">To assess the effects...</AbstractText>
<AbstractText Label="METHODS">Patients attending lung...</AbstractText>
<AbstractText Label="RESULTS">Twenty-five patients...</AbstractText>
<AbstractText Label="CONCLUSIONS">The findings suggest...</AbstractText>
</Abstract>
		-->
	<xsl:template match="text()" mode="scielo-xml-content-abstract">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-publisher_name">
		<PublisherName>
			<xsl:value-of select=".//journal-meta//publisher-name"/>
		</PublisherName>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-journal_title">
		<JournalTitle>
			<xsl:apply-templates select=".//journal-meta/journal-id[@journal-id-type='nlm-ta']"/>
		</JournalTitle>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-issn">
		<Issn>
			<xsl:choose>
				<xsl:when test=".//journal-meta/issn[@pub-type='epub']">
					<xsl:value-of select=".//journal-meta/issn[@pub-type='epub']"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select=".//journal-meta/issn[@pub-type='ppub']"/>
				</xsl:otherwise>
			</xsl:choose>
		</Issn>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-volume_id">
		<xsl:variable name="volume"><xsl:apply-templates select=".//front//volume"/>
		<xsl:if test="substring(.//front//issue,1,5)='Suppl'">
			<xsl:value-of select=".//front//issue"/>
		</xsl:if></xsl:variable>
		<Volume><xsl:if test="$volume!='' and $volume!='00'">
			<xsl:value-of select="$volume"/>
		</xsl:if></Volume>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-issue_no">
		<Issue><xsl:if test=".//front//issue!='00' and .//front//issue!=''"><xsl:value-of select=".//front//issue"/></xsl:if></Issue>
	</xsl:template>
	<xsl:template match="*" mode="scielo-xml-publishing_dateiso">
		<xsl:choose>
			<xsl:when test=".//front//pub-date[@pub-type='collection']">
				<xsl:apply-templates select=".//front//pub-date[@pub-type='collection']"/>
			</xsl:when>
			<xsl:when test=".//front//pub-date[@pub-type='ppub']">
				<xsl:apply-templates select=".//front//pub-date[@pub-type='ppub']"/>
			</xsl:when>
			<xsl:when test=".//front//pub-date[@pub-type='epub-ppub']">
				<xsl:apply-templates select=".//front//pub-date[@pub-type='epub-ppub']"/>
			</xsl:when>
			<xsl:when test=".//front//pub-date[@pub-type='epub']">
				<xsl:apply-templates select=".//front//pub-date[@pub-type='epub']"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select=".//front//pub-date[1]"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="pub-date/@pub-type | @date-type">
		<xsl:variable name="issueid"><xsl:value-of select="normalize-space(translate(concat(../../volume,../../issue),'0',' '))"/></xsl:variable>
		<xsl:choose>
			<xsl:when test=".='epub' and $issueid=''">aheadofprint</xsl:when>
			<xsl:when test=".='epub' and $issueid!=''">ppublish</xsl:when>
			<xsl:when test=".='epub' and ../day">aheadofprint</xsl:when>
			<xsl:when test=".='ppub'">ppublish</xsl:when>
			<xsl:when test=".='epub-ppub'">ppublish</xsl:when>
			<xsl:when test=".='collection'">ppublish</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="date[@date-type='rev-recd']"> </xsl:template>
	
	<xsl:template match="pub-date|date[@date-type!='rev-recd']">
		<xsl:variable name="issueid"><xsl:value-of select="normalize-space(translate(concat(../volume,../issue),'0',' '))"/></xsl:variable>
		<PubDate>
			<xsl:attribute name="PubStatus"><xsl:apply-templates select="@pub-type|@date-type"/></xsl:attribute>
			<xsl:apply-templates select="year"/>
			<xsl:choose>
				<xsl:when test="@date-type">
					<!-- history -->
					<xsl:apply-templates select="month|season"/>
					<xsl:apply-templates select="day"/>	
				</xsl:when>
				<xsl:when test="@pub-type='epub' and $issueid=''">
					<!-- aop -->
					<xsl:apply-templates select="month|season"/>
					<xsl:apply-templates select="day"/>	
				</xsl:when>
				<xsl:when test="@pub-type='epub' and $issueid!=''"><!-- rolling pass --></xsl:when>
				<xsl:when test="month='Jan-Dec' or season='Jan-Dec'"></xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="month|season"/>
				</xsl:otherwise>
			</xsl:choose>
		</PubDate>
	</xsl:template>
	<xsl:template match="pub-date" mode="history">
		<PubDate>
			<xsl:attribute name="PubStatus">aheadofprint</xsl:attribute>
			<xsl:apply-templates select="year"/>
			<xsl:apply-templates select="month|season"/>
			<xsl:apply-templates select="day"/>
		</PubDate>
	</xsl:template>
	<xsl:template match="month|season">
		<Month>
			<xsl:value-of select="."/>
		</Month>
	</xsl:template>
	<xsl:template match="year">
		<Year>
			<xsl:value-of select="."/>
		</Year>
	</xsl:template>
	<xsl:template match="day">
		<Day>
			<xsl:value-of select="."/>
		</Day>
	</xsl:template>

	<xsl:template match="fpage">
		<xsl:element name="FirstPage">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="article-meta/elocation-id">
		<xsl:element name="FirstPage">
			<xsl:attribute name="LZero">save</xsl:attribute>
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="lpage">
		<xsl:element name="LastPage">
			<xsl:value-of select="."/>
		</xsl:element>
	</xsl:template>

	<xsl:template match="contrib" mode="scielo-xml-author">

		<Author>
			<xsl:apply-templates select="name"/>
			<xsl:choose>
				<xsl:when test="count(xref[@ref-type='aff'])=1">
					<xsl:apply-templates select="xref[@ref-type='aff']"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="xref[@ref-type='aff']" mode="multiple-aff"/>
				</xsl:otherwise>
			</xsl:choose>
			
			<!--xsl:if test="not(@affiliation_code)">
						<xsl:apply-templates select="ancestor::record/affiliation/occ"/>
					</xsl:if-->
			<xsl:apply-templates select="contrib-id"></xsl:apply-templates>
		</Author>

	</xsl:template>
	<xsl:template match="contrib-id">
		<Identifier Source="{@contrib-id-type}"><xsl:value-of select="."/></Identifier>
	</xsl:template>
	<xsl:template match="contrib-id[@contrib-id-type='orcid' and not(contains(.,'orcid.org'))]">
		<Identifier Source="{@contrib-id-type}">http://orcid.org/<xsl:value-of select="."/></Identifier>
	</xsl:template>
	<xsl:template match="article-title/text()">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="article-title/*">
		<xsl:value-of select="."/>
	</xsl:template>
	<xsl:template match="article-title/xref"/>
	<xsl:template match="collab" mode="scielo-xml-author">
		<Author>
			<CollectiveName>
				<xsl:value-of select="."/>
			</CollectiveName>
		</Author>
	</xsl:template>
	<xsl:template match="name">
		<xsl:apply-templates select="given-names"/>
		<xsl:apply-templates select="surname"/>
		<xsl:apply-templates select="suffix"/>
	</xsl:template>
	<xsl:template match="given-names | FirstName ">
		<FirstName>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</FirstName>
	</xsl:template>
	<xsl:template match="surname | LastName">
		<LastName>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</LastName>
	</xsl:template>
	<xsl:template match="suffix | Suffix">
		<Suffix>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</Suffix>
	</xsl:template>
	<xsl:template match="prefix ">
		<Prefix>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</Prefix>
	</xsl:template>
	<xsl:template match="xref[@ref-type='aff']  | aff-id ">
		<xsl:variable name="code" select="@rid"/>
		<Affiliation>
			<xsl:apply-templates select="../../..//aff[@id = $code]/institution[@content-type='original']" mode="scielo-xml-text"/>
		</Affiliation>
	</xsl:template>
	<xsl:template match="xref[@ref-type='aff']  | aff-id " mode="multiple-aff">
		<xsl:variable name="code" select="@rid"/>
		<AffiliationInfo>
			<Affiliation>
				<xsl:apply-templates select="../../..//aff[@id = $code]/institution[@content-type='original']" mode="scielo-xml-text"/>
			</Affiliation>
		</AffiliationInfo>
	</xsl:template>
	
	<xsl:template match="institution[@content-type='original']" mode="scielo-xml-text">
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	
	<xsl:template match="aff" mode="scielo-xml-text">
		<xsl:apply-templates select="*[name()!='label']" mode="scielo-xml-text"/>
	</xsl:template>
	<xsl:template match="aff//*" mode="scielo-xml-text">
		<xsl:if test="position()!=1">, </xsl:if>
		<xsl:apply-templates select="*|text()"/>
	</xsl:template>
	<xsl:template match="aff//label" mode="scielo-xml-text"/>
	<xsl:template match="aff//text()" mode="scielo-xml-text">
		<xsl:if test="normalize-space(.)=','"/>
	</xsl:template>
	<xsl:template match="@*" mode="scielo-xml-x">
		<xsl:value-of select="." disable-output-escaping="yes"/>
		<xsl:value-of select="." disable-output-escaping="no"/>
		<xsl:value-of select="concat('&lt;![CDATA[',.,']]&gt;')" disable-output-escaping="yes"/>
	</xsl:template>

	<xsl:template match="article-id" mode="scielo-xml-pii">
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="italic | bold | sup | sub">
		<xsl:apply-templates></xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="article[@article-type='book-review']">
	</xsl:template>
	
	
</xsl:stylesheet>
