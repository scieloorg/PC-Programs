.. pcprograms documentation master file, created by
   sphinx-quickstart on Tue Mar 27 17:41:25 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
Markup versão 94 - Notas de Versão
==================================

**Markup versão 94** é uma macro para Word usada para identificar os elementos estruturais e semânticos dentro de um texto, gerando um XML compatível com SciELO PS. O XML deve ser analisado e completado, caso necessário.

A versão 94 do Markup gera XMLs compatíveis com as versões `1.6 <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.6-branch/>`_ e `1.7 <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/>`_ do SciELO PS.

As tags usadas para marcação são divididas em:

* flutuantes - que podem ocorrer em qualquer parte do texto;
* fixas - que ocorrem em estruturas específicas do documento (metadados básicos do artigo - front, corpo do texto - body e pós textuais - back)

. image:: img/tags.png
   :height: 400px
   :align: center

Neste guia serão descritas todas as tags disponíveis na versão indicando seu uso e equivalência com no XML gerado.

Tags do programa
----------------

* doc - marca todo o conteúdo do texto para gerar um arquivo XML ao final da marcação - equivalente à <article>

Na janela de metadados preencher os campos conforme os dados disponíveis no tipo de artigo a ser marcado. Não incluir dados que não existem no documento original.

.. Note:: Usar o botão **element** nos casos em que não há a tag disponível para marcação. Preencher no formulário com o nome da tag de acordo com `SciELO PS <http://docs.scielo.org/projects/scielo-publishing-schema/>`_

Metados iniciais - <front>
--------------------------

. image:: img/doc-mkp-formulario.jpg
   :height: 400px
   :align: center

* collection/journal  - selecionar o título do periódico a ser marcado - <journal-title-group>; 
* jtitle - apresenta o título do periódico como foi registrado em SciELO - <journal-title>; 
* acron - acrônimo do periódico em SciELO -  <journal-id journal-id-type="publisher-id">;
* stitle – título abreviado do periódico -  <abbrev-journal-title abbrev-type="publisher">;
* ISSN (id scielo)* – issn registrado em SciELO;
* pissn – issn impresso registrado em SciELO -  <issn pub-type="ppub-epub">;
* eissn – issn eletrônico registrado em SciELO -  <issn pub-type="epub">;
* pubname – casa publicadora do periódico -  <publisher>, <publisher-name>;
* license (url) – licença creative commons adotada pelo periódico - <permission>, <license>, <license-p>;
* volid – volume - <volume>;
* supplvol – suplemento de volume - <volume>;
* supplno – suplemento de número - <issue>;
* issueno - número do fascículo - <issue>
* dataiso – data no formato ISO ANOMÊSDIA do número. Se o número não é mensal, incluir o último mês da periodicidade. Ex: Apr/June, preencher 20170600 - <pub-date>, <day>, <month>, <year>;
* month/season – mês/meses correspondentes à periodicidade. Sempre usar sigla de três letras em inglês, exceto para os meses de June, July e May. Ex: Apr/June - <month>, <season>
* fpage – primera página do artigo - <fpage>;
* lpage – última página do artigo - <lpage>;
* @seq – caso haja um artigo que se inicia na mesma página de um artigo anterior, incluir a sequência com letra - <fpage seq="xx">;
* elocatid – usar em caso de paginação eletrônica, nesse caso não preencher fpage e lpage - <page-count>;
* order – incluir o número de ordem do artigo no sumário do periódico, com dois dígitos no mínimo e máximo de cinco - <article-id>;
* pagcount – incluir a quantidade de páginas apenas os casos de publicações eletrônicas ou em * Ahead of Print. O valor deve ser sempre 1 - <page-count>;
* doctopic - selecionar o tipo de artigo em marcação. Ex: artigo original, resenha, carta, artigo de revisão etc - <subject>;
* language - idioma do artigo - <article xml:lang>;
* version - versão do SciELO Publishing Schema vigente - 1.6, 1.7 etc - <article article-type>;
* artdate (rolling) – data de artigo publicado na modalidade contínua. Usar data ISO ANOMESDIA - <pub-date>, <day>, <month>, <year>;
* ahpdate – data de artigo publicado na modalidade ahead of print. Usar data ISO ANOMESDIA - <pub-date>, <day>, <month>, <year>.

DOI
---
* doi – identifica o  DOI do artigo <article-id pub-id-type="doi">;

Título da seção
---------------

* toctitle – Identifica título da seção do artigo no sumário do número - <subj-group>, <subject>;

Título do Artigo
----------------

* doctitle – Identifica título(s) do artigo - <title-group>, <article-title>, <trans-title-group>, <trans-title>;

Autores - <contrib-group>
-------------------------

* author – marca cada autor de um artigo - <contrib contrib-type="author">, <name>;
    * fname-surname – marca nome e sobrenome de um autor;
    * fname-spanish-surname – marca nomes de autores espanhóis;
    * surname-fname – marca sobrenome e nome de um autor;
    * surname – marca o sobrenome de um autor - <surname>;
    * fname – marca nome de um autor - <given-names>;
    * prefix – identifica o prefixo de um autor como Sr., Prof., etc - <prefix>;
    * suffix –  identifica o sufixo de um autor como Filho, Neto, etc - <sufix>;
    * role –  identifica o papel de um autor - <role>
    * authorid – identifica o ID de um autor de um base de dados - <contrib-id>
    * onbehalf – identifica a instituição/grupo ao qual autor representa. Exemplo: John Smith em nome do Grupo XXX - <on-behalf-of>.
    * xref - identifica uma referência cruzada de um elemento/item relacionado ao autor, normalmente afiliação <xref ref-tye="aff" rid="xx"> e de nota de rodapé <xref ref-type="fn" rid="xx">
* corpauth - Identifica autor corporativo do artigo - <collab>;

Afiliação - <aff id="xx">
-------------------------

* normaff - Identifica cada afiliação de autor - <aff id="xx">, <institution content-type="original">;
 	* label – Identifica um label que relaciona o autor à afiliação - <label>;
 	* role –  Identifica o papel do autor - <role>; 
 	* orgname - Identifica a instituição maior de afiliação do autor - <institution content-type="orgname">;
 	* orgdiv1 - Identifica a primeira subdivisão da instituição de afiliação do autor - <institution content-type="orgdiv1">;
 	* orgdiv2 - Identifica a segunda subdivisão da instituição de afiliação do autor - <institution content-type="orgdiv2">;
 	* city - Identifica a cidade de afiliação - <addr-line>, <named-content content-type="city">, <city>;
 	* state - Identifica o estado/região da afiliação - <addr-line>, <named-content content-type="state">, <state>;
 	* zipcode - Identifica o código postal da afiliação - <addr-line>, <postal-code>;
 	* country - Identifica o país de afiliação - <country country="XX">;
 	* email - email - <email>.
* institid - Marca o identificador de uma instituição de acordo com as bases ISNI ou Ringgold - <institution-wrap>, <institution-id institution-id-type="XX">

Notas de autor - <author-notes>
-------------------------------

* corresp - marca autor de correspondência - <author-notes>, <corresp id="XX">;
	* label - Identifica um label que relaciona o autor à nota de correspondência - <label>;
	* email - email - <email>
* fn - marca notas relacionadas ao autor (ver tipos de `notas de autor <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/tagset.html#notas-de-autor>`_) - <author-notes>, <fn>;
	* label - Identifica um label que relaciona o autor à nota de autor - <label>;
	* p - Identifica a nota de autor - <p>

Livro resenhado - <product>
---------------------------

* product – Agrupa dados de um item resenhado - <product>;
	* authors – Agrupa dados de autoria de uma referencia - <person-group>;
		* pauthor – Identifica automaticamente as parte do nome de um autor - <name>, <surname>, <given-names>;
		* pauthor – Identifica as parte do nome de um autor - <name>;
		* fname-surname – Marca nome e sobrenome de um autor;
    	* fname-spanish-surname – Marca nomes de autores espanhóis;
   	 	* surname-fname – Marca sobrenome e nome de um autor;
   	 	* surname – Marca o sobrenome de um autor - <surname>;
   		* fname – Marca nome de um autor - <given-names>;
    	* prefix – Identifica o prefixo de um autor como Sr., Prof., etc - <prefix>;
    	* suffix – Identifica o sufixo de um autor como Filho, Neto, etc - <sufix>;
		* cauthor – Identifica un autor corporativo - <collab>;
		* et-al – et-al - <et-al/>
	* chptitle – Identifica o título do capíutlo de um livro resenhado - <chapter-title>;
	* source – Identifica o título da fonte principal resenhada - <source>;
	* pubname – Identifica a casa publicadora - <publisher-name>; 
	* publoc – Identifica o local de publicação - <publisher-loc>; 
	* date – Identifica a data ISO de publicação - <day>, <month> and/or <year>;
	* isbn - ISBN de um livro - <isbn>;
	* extent – Identifica a extensão de uma obra - <size units="pages">
	* series – Identifica o título de uma série/coleção - <series>;
	* moreinfo – Identifica outros dados - <comment>.

Histórico do artigo - <history>
-------------------------------

* hist - Identifica o histórico de um artigo - <history>;
	* received - Identifica a data ISO em que o artigo foi recebido para revisão por pares - <date date-type="received">, <day>, <month>, <year>;
	* revised - Identifica a data ISO em que o artigo foi revisado - <date date-type="revised">, <day>, <month>, <year>;
	* accepted - Identifica a data ISO em que o artigo foi aceito para publicação - <date date-type="accepted">, <day>, <month>, <year>.

Licença CC e Copyright - <permissions>
--------------------------------------

* cpright – Agrupa dados de copyright. Pode estar relacionado à objetos do texto (tabelas e figuras) - <copyright-statement>;
	* cpyear – Identifica o ano do copyright - <copyright-year>;
	* cpholder – Identifica o detentor do copyright - <copyright-holder>.
* licinfo - Identifica dados de licença Creative Commons - <permission>, <license>, <license-p>.

Resumos - <abstract>, <trans-abstract>
--------------------------------------

* xmlabstr - Identifica o grupo de dados de um resumo - <abstract>, <trans-abstract>.

Palavras-chave - <kwd-group>
----------------------------

* \*kwdgrp - Identifica automaticamente todo o grupo de palavras-chave de um idioma - <kwd-group xml:lang="xx">, <kwd>;
* kwdgrp - Identifica o grupo de palavras-chave de um idioma - <kwd-group xml:lang="xx">;
	* kwd - Identifica uma palavra-chave - <kwd>.

Dados de financiamento - <funding-group>
----------------------------------------

Os dados de financiamento podem ser marcados em nota de rodapé ou em agradecimentos. Ambos os itens fazem parte dos elementos pós-textuais, contudo ao marcar os dados de financiamento, o programa se encarrega de agrupá-los em <front>.

Artigos relacionados
--------------------

* related - Identifica um artigo relacionado ao artigo em marcação. (ver tipos de `artigos relacionados aqui <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/tagset/elemento-related-article.html>`_) - <related-article id="XX" related-article-type="XX">

Corpo do Texto - <body>
-----------------------

Caso a formatação do texto tenha sido feita de acordo com as instruções de preparo de arquivos antes da marcação, alguns itens serão marcados automaticamente, tais como: parágrafos - <p>, seções - <sec> e citações diretas - <disp-quote>.

* xmlbody - Identifica o corpo do texto - <body>;
	* p – Identifica um parágrafo no corpo do texto - <p>;
		* xref - Identifica a chamada de um elemento (figuras, tabelas etc) no corpo do texto (clique em `xref <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/tagset/elemento-xref.html#xref>`_ para ver todos tipos de referência cruzada) - <xref ref-type="xx" rid="xx">;
		* uri - Identifica uma url. Pode ocorrer em <front>, <body> e <back> - <ext-link ext-link-type="xx" xlink:href="xx">;
	* media - Identifica uma mídia. Pode aparecer em <body> e <back> sendo mais comum em <body> (clique em `media <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/tagset/elemento-media.html>`_-  <media mimetype="xx" mime-subtype="xx" xlink:href="nomedoarquivodemidia.extensãodoarquivodemídia"/>;
	* sec - Identifica uma seção e seus tipos mais comuns - <sec sec-type="xx">;
		* sectitle - Identifica o título de uma seção - <title>;
		* p – Identifica um parágrafo dentro de uma seção - <p>;
		* subsec - Identifica uma subseção - <sec>;
 			* sectitle - Identifica o título da subseção - <sec>;
			*	p – Identifica um parágrafo em uma subseção - <p>;
	* deflist - Identifica uma lista de definições no corpo do texto - <def-list id="xx">;
		* sectitle - Identifica o título de uma lista de definições - <title>;
		* defitem - Identifica um item da lista de definições - <def-item>
			* term - Identifica o termo a ser definido - <term>;
			* def - Identifica a definição do termo - <def>;
	* \*deflist - Identifica automaticamente todos os itens de uma lista de definições - <def-list id="xx">;
	* sigblock – Agrupa dados de uma assinatura de um artigo - <sig-block>;
		* sig – Identifica a assinatura do autor - <sig>;
	* boxedtxt - Identifica uma caixa de texto. Pode marcar caixas de texto em <front>, <body> e <back> sendo mais comum sua presença em <body> - <boxed-text>;
		* p - Identifica um parágrafo - <p>;
		* sec - Identifica uma seção em uma caixa de texto - <sec>;
			* sectitle - Identifica o título da seção - <title>;
			* p - Identifica um parágrafo - <p>;
				* subsec - Identifica uma subseção - <sec>;
 					* sectitle - Identifica o título da subseção - <title>;
					* p - Identifica um parágrafo - <p>;
		* \*boxedtxt - Identifica automaticamente os dados de uma caixa de texto - <boxed-text>;
	* equation - Identifica uma fórmulas/equação. Pode ocorrer em <front>, <body> e <back> sendo mais comum sua presença em <body> - <disp-formula id="xx"> quando em um parágrafo, <inline-formula> quando no meio de um parágrafo;
		* graphic - Identifica uma imagem de uma fórmula/equação - <graphic xlink:href="nomedoarquivodaimagem.extensãodaimagem"/>;
			* alttext - Identifica um texto que descreve a imagem - <alt-text>;
		* textmath - Identifica uma fórmulas/equação em formato LaTeX - <tex-math>;
		* mmlmath - Identifica uma fórmulas/equação em formato MathML - <mml:math>;
		* label - Identifica um label de uma fórmula num parágrafo - <label>;
	* figgrp - Agrupa dados de uma figura. Pode ocorrer em <front>, <body> e <back> sendo mais comum sua presença em <body> e <back> - <fig id="xx">;
		* graphic - Identifica uma imagem - <graphic xlink:href="nomedoarquivodaimagem.extensãodaimagem"/>;
			* alttext - Identifica um texto que descreve a imagem - <alt-text>;
		* attrib - Identifica a fonte da figura - <attrib>;
		* label - Identifica um label da figura - <label>;
		* caption - Identifica a legenda da figura - <caption>;
	* quote - Identifica uma citação direta. Pode ocorrer em <body> e <back> sendo mais comum em <body> - <disp-quote>;
	* list - Identifica uma lista. Pode ocorrer em <body> e <back> sendo mais comum sua presenta em <body> - <list list-type="xx">;
			* li - Identifica um item de uma lista - <list-item> <p>;
				* label - Identifica o label de um item, se hiuver - <label>;
	* \*list - Identifica automaticamente os elementos de uma lista;
	* tabwrap - Agrupa dados de uma tabela> Pode ocorrer em  <body> e <back> sendo mais comum em <body> - <table-wrap id="xx">;
		* label - Identifica um label de uma tabela - <label>;
		* caption - Identifica a legenda uma tabela - <caption>;
		* xhtml - Identifica uma tabel codificada em XHTML, incluindo-se o nome do arquivo disponível na pasta src com sua extensão. Exemplo: artigo01tab.html;
		* graphic - Identifica uma imagem de uma tabela - <graphic xlink:href="nomedoarquivodaimagem.extensãodaimagem"/>
			* alttext - Identifica um texto que descreve a imagem - <alt-text>;
		* table - Identifica uma tabela - <table>;
			* tr - Identifica uma linha de uma tabela - <tr>;
				* th - Identifica uma célula do cabeçalho de uma tabela - <th>;
				* td - Identifica uma célula do corpo de uma tabela - <td>;
	* fntable - Agrupa dados de nota uma tabela - <table-wrap-foot>;
		* label - Identifica o label de uma nota de tabela - <label>;
	* versegrp - Agrupa dados de um verso. Pode ocorrer em <body> e <back> sendo mais comum em <body> - <verse-group>;
		* label - Identifica o label - <label>;
		* versline - Identifica uma linha do verso - <verse-line>;
		* attrib - Identifica a autoria do verso - <attrib>; 
	* supplmat - Identifica um suplemento. Pode ocorrer em <front>, <body> e <back> sendo mais comum em <body> -  <supplementary-material id="xx" mimetype="xx" mime-subtype="xx" xlink:href="nomedoarquivodosuplemento.extensãodoarquivo"/>;
		* label - Identifica o label - <label>;
		* caption - Identifica a legenda - <caption>.

Dados pós-textuais - <back>
---------------------------

Agradecimentos - <ack>
----------------------

* ack - agrupa os elementos de agradecimentos - <ack>;
 	* sectitle - Identifica o título da seção agradecimento - <title>;
	* p - Identifica um parágrafo na seção agardecimentos - <p>;
		* funding - Agrupa os dados de financiamento quando presentes em agradecimentos - <funding-group>
 			* award - Agrupa dados do número de contrato e a gência de fomento/financiador - <award-group>;
 			 	* fundsrc - Identifica a agência de fomento/financiador - <funding-source>;
 				* contract - Identifica o número do projeto ou contrato do financiamento - <award-id>;

Notas de rodapé
^^^^^^^^^^^^^^^

* page-fn - Identifica automaticamente todas as notas de rodapé e suas referências no corpo do texto desde que inseridas como notas de rodapé do word - <fn-group>, <fn>;
* fngrp - Agrupa notas de um texto - <fn-group>;
	* fn - Identifica uma nota - <fn fn-type="xx" id="xx">.

Apêndices/Anexos - <app-group>
------------------------------

* appgrp - Agrupa dados de apêndices/anexos - <app-group>;
	* app - Identifica um anexo/apêndice - <app id="xx">;
		* label - Identifica o label de um anexo/apêndice - <label>;
 		* sectitle - Identifica o título de um anexo/apêndice - <title>;
		* sec - Identifica uma seção e seus tipos mais comuns - <sec sec-type="xx">;
			* sectitle - Identifica o título de uma seção - <title>;
			* p – Identifica um parágrafo dentro de uma seção - <p>;
				* subsec - Identifica uma subseção - <sec>;
 					* sectitle - Identifica o título da subseção - <sec>;
					*	p – Identifica um parágrafo em uma subseção - <p>;
	* p – Identifica um parágrafo no corpo do texto - <p>;
		* glossary - Identifica um glossário, pode ser usada para marcar um glossário em <front>, <body> e <back>, sendo mais comum sua presença em <back> - <glossary id="xx">;
 			* label - Identifica o label do glossário - <label>;
 			* sectitle - Identifica p título do gloassário - <title>;
			* deflist - Identifica uma lista de definições no glossário - <def-list id="xx">;
				* defitem - Identifica um item da lista de definições no glossário - <def-item>;
					* term - Identifica o termo a ser definido no glossário - <term>;
					* def - Identifica a definição do termo no gloassário - <def>;
			* \*deflist - Identifica automaticamente todos os itens de uma lista de definições no gloassário;

Referências bibliográficas - <ref-list>
---------------------------------------

* refs - Identifica uma lista de referências bibliográficas - <ref-list>;
	* sectitle - Identifica o título da seção de referências - <title>;
	* ref - Agrupa os dados de uma referência bibliográfica. Clique  `aqui <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/tagset/elemento-element-citation.html>`_ para consultar os tipos possíveis de referência bibliográfica - <ref>, <element-citation publication-type="xx">, <mixed-citation>;
		* text-ref - Identifica a forma original da referência - <mixed-citation>;
		* label - Identifica o label de uma referência - <label>;
		* \*authors - Identifica automaticamente todos os elementos de uma autoria;
		* authors - Agrupa dados de autoria de una referencia - <person-group person-group-type="xx">;
			* \*pauthor - Identifica automaticamente partes do nome de UM autor;
			* pauthor - Agrupa partes do nome de UM autor - <name>;
				* fname-surname - marca nome e sobrenome de um autor;
				* fname-spanish-surname - marca nome e sobrenome de autores espanhós;
				* surname-fname - marca sobrenome e nome de um autor;
				* fname - marca os nomes de um autor - <given-names>;
				* surname - marca o sobrenome de um autor - <surname>;
				* prefix - identifica o prefixo de um autor como Sr., Prof., etc - <prefix>;
				* suffix -  identifica o sufixo de um autor como Filho, Neto, etc - <suffix>;
			* cauthor - Identifica um autor corporativo - <collab>;
			* et-al - et-al - <etal>;
		* arttitle - Identifica o título de um artigo - <article-title>;
		* chptitle - Identifica o título de um capítulo de livro - <chapter-title>;
		* cited - Identifica a data ISO da consulta da fonte citada -  <date-in-citation content-type="access-date">;
		* series - Identifica o título de uma serie - <serie>;
		* confgrp - Agrupa dados de uma conferencia:
			* confname - Identifica o nome da conferência - <conf-name>;
			* no - Identifica o número da conferência;
			* date - Identifica a data ISO da conferência - <conf-date>;
			* city - Identifica a cidade da conferência - <conf-loc>;
			* state - Identifica o estado/região da conferência - <conf-loc>;
			* country - Identifica o país da conferência - <conf-loc>;
			* sponsor - Identifica a instituição responsável pela conferencia - <publisher-name>;
		* date - Identifica a data ISO da refêrencia - <day> <month> <season> <year>;
		* edition - Identifica a edição da referência - <edition>;
		* elocation - Identifica o identificador eletrênico da referência - <elocation-id>;
		* extent - Identifica a extensão de uma referência - <size units="pages">;
		* issn - ISSN - <issn>;
		* isbn - ISBN - <isbn>;
		* issueno - Identifica o número - <issue>;
		* moreinfo - outros dados importantes - <comment>;
		* pages - Identifica um intervalo de páginas - <fpage> <lpage>;
		* part- Identifica uma parte de uma referencia - <part-title>;
		* patentno - Identifica o número de uma patente - <patent country="XX">;
		* pubid - Identifica um id de qualquer tipo de base de dados externa. Clique  `aqui <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/tagset/elemento-pub-id.html>`_ para ver tipos possíveis -  <pub-id pub-id-type="xx">;
		* publoc- Identifica o local de publicação da referência - <publisher-loc>; 
		* pubname- Identifica a casa publicadora da referência - <publisher-name>; 
		* \*publoc/pubname- Identifica automaticamente local de publicação e casa publicadora;
		* \*pubname/publoc- Identifica automaticamente casa publicadora e local de publicação;
		* reportid - Identifica o nome ou número de um relatório - <pub-id pub-id-type="other">;
		* \*source - Identifica automaticamente o título da fonte principal de uma referência e suas repetições na lista de referencias - <source>;
		* source - Identifica o título da fonte principal da referência - <source>;
		* suppl - Identifica o número de um suplemento - <supplement>;
		* thesgrp - Agrupa dados de uma tese/dissertação;
			* date - Identifica a data ISO da tese - <day> <month> <season> <year>;
			* city - Identifica a cidade da tese - <publisher-loc>;
			* state - Identifica o estado/região da tese - <publisher-loc>;
			* country - Identifica o país da tese - <publisher-loc>;
			* orgname - Identifica a instituição onde a tese foi defendida/depositada - <publisher-name>;
		* url - Identifica uma url - <ext-link ext-link-type="uri" xlink:href="http://xxxx">;
		* volid - Identifica o volume de uma referência - <volume>.

Artigos relacionados ao artigo principal - <sub-article>
--------------------------------------------------------

* subdoc - Identifica um artigo relacionado ao artigo principal e pode conter todos os elementos descritos anteriormente (ver tipos de `disponíveis aqui <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.7-branch/tagset.html#notas-de-autor>`_). - <sub-article article-type="xx" xml:lang="xx" id="xx">;

.. Note:: Traduções e outros artigos relacionados ao artigo principal devem fazer parte de um mesmo arquivo .docx. No caso de traduções, as referências bibliográficas não devem ser marcadas novamente.


