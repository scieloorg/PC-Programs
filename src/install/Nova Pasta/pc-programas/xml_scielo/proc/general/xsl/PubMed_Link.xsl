<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="xml" indent="yes" encoding="UTF-8" doctype-public="-//NLM//DTD LinkOut 1.0//EN" doctype-system="http://www.ncbi.nlm.nih.gov/entrez/linkout/doc/LinkOut.dtd"/>
	<!--xsl:variable name="PubmedCreateDate" select="document('../xml/xmlDatePubmed.xml')"/-->
	<xsl:variable name="doi_prefix" select="//xml_scielo//doi-configuration//doi-prefix"/>
	<xsl:variable name="replaceISSN" select="//xml_scielo//replace-issn"/>
	<xsl:template match="/">
		<!--xsl:variable name="PubmedCreateDate" select="document(c:/xml_scielo/proc/xml/xmlDatePubmed.xml)"/-->
		<xsl:choose>
			<xsl:when test="//scielo-url='' or //xml_scielo_title/pubmed-control/start-date=''">
				<ul>
					<xsl:if test="//scielo-url=''">
						<li>
							<p>
								<b>Error: Missing url. e.g.: http://www.scielo.br</b>
								<br/>
						Solution: Edit the file  /xml_scielo/config/PubMed/journals/journals.seq, with the following format:<br/>
						journal_abbrev start_year_that_make_part_of_the_query <b>url</b>
								<br/>
							</p>
							<!--p>
								<b>Problema: Falta URL del sitio. Ej.: http://www.scielo.br</b>
								<br/>
						Solución: Edite el archivo /xml_scielo/config/PubMed/journals/journals.seq, con el siguiente formato:<br/>
						acrónimo_de_la_revista año_inicio_que_hace_parte_de_la_query <b>url</b>
								<br/>
							</p>
							<p>
								<b>Problema: Falta URL do site. Ex.: http://www.scielo.br</b>
								<br/>
						Solução: Edite o arquivo /xml_scielo/config/PubMed/journals/journals.seq, com o seguinte formato:<br/>
						acrônimo_da_revista ano_inicio_que_faz_parte_da_query <b>url</b>
								<br/>
							</p-->
						</li>
					</xsl:if>
					<xsl:if test="//xml_scielo_title/pubmed-control/start-date=''">
						<li>
							<p>
								<b>Error: Missing year. e.g.: 1999</b>
								<br/>
						Solution: Edit the file  /xml_scielo/config/PubMed/journals/journals.seq, with the following format:<br/>
						journal_abbrev <b>start_year_that_make_part_of_the_query</b> url								<br/>
							</p>
							<!--p>
								<b>Problema: Falta año. Ej.: 1999</b>
								<br/>
						Solución: Edite el archivo /xml_scielo/config/PubMed/journals/journals.seq, con el siguiente formato:<br/>
						acrónimo_de_la_revista <b>año_inicio_que_hace_parte_de_la_query</b> url
								<br/>
							</p>
							<p>
								<b>Problema: Falta ano. Ex.: 1999</b>
								<br/>
						Solução: Edite o arquivo /xml_scielo/config/PubMed/journals/journals.seq, com o seguinte formato:<br/>
						acrônimo_da_revista <b>ano_inicio_que_faz_parte_da_query</b> url
								<br/>
							</p-->
						</li>
					</xsl:if>
				</ul>
			</xsl:when>
			<xsl:otherwise>
				<LinkSet>
					<Link>
						<LinkId>3</LinkId>
						<ProviderId><xsl:value-of select="//provider-id"/></ProviderId>
						<IconUrl>
							<xsl:value-of select="//scielo-url"/>/img/scielo.gif</IconUrl>
						<ObjectSelector>
							<Database>Pubmed</Database>
							<ObjectList>
								<!--Query><xsl:value-of select="//issn/occ"/> [TA] <xsl:value-of select="substring(//publishing_dateiso/occ, 1, 4)"/>/<xsl:value-of select="substring(//publishing_dateiso/occ, 5, 2)"/>:2010 [dp]</Query-->
								<Query>
									<xsl:value-of select="$replaceISSN"/><xsl:if test="$replaceISSN=''"><xsl:value-of select="//issn/occ"/></xsl:if> [TA] <xsl:apply-templates select="." mode="pubDate"/>:2010 [dp]</Query>
							</ObjectList>
						</ObjectSelector>
						<ObjectUrl>
							<Base>
								<xsl:value-of select="//scielo-url"/>
							</Base>
							<!-- FIXED 20040504 
			Roberta Mayumi Takenaka
			Solicitado por Solange email: 20040429
			Trocar &amp;lo.pii; por &lo.pii;
			--><!-- FIXED 20070320 
			Roberta Mayumi Takenaka
			Solicitado por Solange pessoalmente devido a um chamado do Chile
			Trocar cgi-bin/fbpe/fbtext? por /scielo.php?script=sci_arttext&amp;
			-->
							<Rule>/scielo.php?script=sci_arttext&amp;pid=<xsl:text disable-output-escaping="yes">&amp;lo.pii;</xsl:text>&amp;lng=en&amp;nrm=iso&amp;tlng=en</Rule>
							<Attribute>full-text online</Attribute>
						</ObjectUrl>
					</Link>
					<!--it><xsl:value-of select="$PubmedCreateDate//item/@issn"/></it-->
				</LinkSet>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="*" mode="pubDate">
		<!--xsl:variable name="issnReal" select="//issn[position() = 1]/occ"/>
		<xsl:apply-templates select="$PubmedCreateDate//item[$issnReal = @issn]/@beginDate"/-->
		<!-- FIXED 20040504 
			Roberta Mayumi Takenaka
			Solicitado por Solange email: 20040429
			Falta o ano de início de encvio dos dados		
			foi acrescentado mais uma coluna no arquivo journals.seq 
			que corresponde ao valor do ano de início de envio dos dados (v2)
			-->
		<xsl:value-of select="xml_scielo_title/pubmed-control/start-date"/>
		<!--xsl:value-of select="$issnReal"/-->
	</xsl:template>
	<xsl:template match="publishing_dateiso" mode="listData">
		<xsl:value-of select="substring(occ, 1, 4)"/>:<xsl:value-of select="substring(occ, 5, 4)"/>:2010 [dp]</xsl:template>
	<xsl:template match="occ" mode="year">
		<xsl:value-of select="substring(text(),1,4)"/>
	</xsl:template>
</xsl:stylesheet>
