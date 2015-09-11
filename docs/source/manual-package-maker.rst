Package Maker
=============

O programa Package Maker é uma ferramenta de validação do pacote SciELO que está de acordo com o Schema SciELO PS 1.2.
Este validador gera relatórios de erros que estão em desconformidade com o SPS 1.2 e JATS 1.0.
Veja a seguir o passo a passo para instalar e utilizar o Package Maker.



Instalação do Package Maker
---------------------------

Para instalar o programa Package Maker entre no FTP Produtos-SciELO


    server: ftp.scielo.br
    user: produtos-scielo
    password: produtos@scielo


Na pasta: current_versions

E faça o download do arquivo xpm-4.0.090-trial.EXE




Package Maker - Como utilizar
-----------------------------

Para utilizar o programa Package Maker, entre na pasta onde o validador foi instalado, depois entre na pasta xml.
Após isso, clique no arquivo "xml_package_maker.py". Veja:

.. image:: img/XMPM-c.jpg


Veja que ao clicar no "xml_package_maker.py" abre-se a seguinte janela:


.. image:: img/XPM.jpg

Nessa janela deve ser inserido o acronimo da revista que será validada no campo "Journal acronym" e em
"SPS XML Package Folder" clique no botão "choose folder" e selecione o pacote XML que deverá ser validado.
Veja no terminal DOS que o Package Maker irá validar todos os arquivos xml e ao final abrirá, automaticamente,
o relatório de erros de todos os arquivos do pacote em seu navegador. Veja:

.. image:: img/report-xmp.jpg


Verifique que o programa gera também uma pasta abaixo do pacote validado chamado: "<nome-do-pacote>_xml_package_maker_result"
Dentro dessa pasta há 6 pastas. Veja:

.. image:: img/PASTAS.jpg


	pasta erros:
	Nessa pasta há o relatório de erros de cada um dos arquivos .xml e ao final há o mesmo relatório que abre automaticamente
	em uma página do seu navegador.


	pmc_package:
	Para revistas que apresentam o título abreviado NLM, o programa retira os elementos de especificação SciELO e mantém apenas
	os elementos necessários para envio ao PMC.
	Os elementos que são retirados do documento XML para envio ao PMC são: detalhamento em afiliação, informação de financiamento
	em <funding-group> e <mixed-citation>.


	pmc_package_zips:
	Ao validar o pacote pmc_package o programa, automaticamente, zipa a pasta que está pronta para envio.


	scielo_package:
	No momento da validação do pacote XML o programa verifica as entidades (numéricas ou alfa-numéricas) que existem no documento
	e, automaticamente, converte para o caractere correspondente. Evitando futuros problemas de entidades. O ideal é utilizar os 
	arquivos .xml validados nessa pasta em vez de utilizar os xmls do pacote.


	scielo_package_zips:
	Ao validar o pacote scielo_package o programa, automaticamente, zipa a pasta já com a nomeação padrão SciELO que está pronta 
	para envio.


	work:
	é uma pasta de arquivos temporários usadas para a geração do resultado. ela pode ser apagada se desejável, mas também pode ser 
	usada para fins de suporte.




Como verificar o relatório
--------------------------

Ao gerar o relatório de erros, note que o report que abre em uma página do navegador apresenta algumas abas:


Aba - Relatório Resumido:

.. image:: img/report-resumido.jpg


Nessa primeira aba, como o próprio nome diz, o programa apresenta um resumo dos problemas encontrados no pacote validado.
Veja que ao lado há uma legenda explicativa sobre cada alerta: "Fatal Error", "Error" e "Warning".


.. image:: img/legenda.jpg




Aba - Relatório detalhado:

.. image:: img/relatorio-detalhado.jpg


Nessa aba o programa apresenta uma tabela com algumas informações gerais de cada arquivo .xml. Veja:

+----------------+-------------------------------------------------------------------------------------------+
|name            | indica o nome do documento .xml                                                           |
+----------------+-------------------------------------------------------------------------------------------+
|order           | ordem de apresentação no site que servirá para compor o PID do documento                  |
+----------------+-------------------------------------------------------------------------------------------+
|fpage           | indica a primeira página de cada arquivo (importante verificar se não há fpages iguais)   |
+----------------+-------------------------------------------------------------------------------------------+
|doi             | indica o número de DOI marcado (importante verificar se não há DOI repetido)              |
+----------------+-------------------------------------------------------------------------------------------+
|aop pid         | campo para indicação de order para arquivos Ahead Of Print                                |
+----------------+-------------------------------------------------------------------------------------------+
|toc section     | identificador de seção (importante verificar se as seções estão de acordo com o sumário)  |
+----------------+-------------------------------------------------------------------------------------------+
|article-type    | indica o valor inserido em @article-type de ``<article>``                                 |
+----------------+-------------------------------------------------------------------------------------------+
|article title   | apresenta o título de cada documento                                                      |
+----------------+-------------------------------------------------------------------------------------------+
|                | relatório de erro dos documentos. Pode apresentar validações de conteúdo e do XML         |
|                +-------------------------------------------------------------------------------------------+
| reports        |Report: Validações de conteúdo | Relatório que valida o conteúdo + especificações SciELO   |
|                +-------------------------------+------------------------------------------------------------
|                |Report: Validações do XML      | Relatório que valida contra a DTD JATS 1.0                |
+----------------+-------------------------------------------------------------------------------------------+


