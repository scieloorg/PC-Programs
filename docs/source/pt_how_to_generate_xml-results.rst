.. pt_how_to_generate_xml-results:

Relatórios
==========
Ao gerar o arquivo .xml o programa Markup apresenta três relatórios: :ref:`report-arquivos`, :ref:`report-estilos` e :ref:`report-conteudo`.
Veja abaixo a função de cada relatório apresentado.


.. _report-arquivos:

Relatório de Erros de Arquivos
------------------------------

Perceba que ao clicar em "Markup: Gerar o XML" o programa apresenta um Relatório com as informações das alterações feitas no documento.

.. image:: img/doc-mkp-report-name.jpg

O resultado disso, é um relatório que apresenta as ações do programa ao gerar o XML a partir do arquivo .doc. O programa altera o nome do arquivo que, em .doc, era apresentado como "12-Artigo.doc" para ISSN-acronimo-volume-numero-paginação.xml e as imagens são extraídas do documento já com a nomeação convertida para o padrão SciELO.


.. _report-estilos:

Relatório de Estilos SciELO
---------------------------

Em seguida clique no botão ao lado "Relatório de Estilos SciELO" e verifique se há algum erro no documento:

.. image:: img/doc-mkp-gerar-report-scielo.jpg
   :align: center

O programa irá apresentar úm relatório parecido com o que segue abaixo:

.. image:: img/doc-mkp-report-style.jpg
   :align: center

Veja que o relatório de erros não apresenta nenhum erro. Isso porque o xml gerado está de acordo com a estrutura de estilos requerida.


.. _report-conteudo:

Relatório de Erros de Conteúdo
------------------------------

Feita a verificação no Relatório de Estilos SciELO, o próximo passo é gerar o relatório de erros de dados/conteúdo.

Esse relatório é exatamente o mesmo que o programa Package Maker gera. Portanto, para verificar o manual de uso para validação e verificação dos erros apresentados, vá para o projeto :ref:`` e confira as funcionalidades dessa ferramenta.


.. _relatorios-pastas:

Pastas Geradas
==============

Ao gerar o arquivo .xml o programa Markup cria 6 pastas no mesmo nível que "src" e "scielo_markup". Veja abaixo as pastas geradas e o que cada uma apresenta.

.. image:: img/doc-mkp-pastas-geradas.jpg


	*pasta erros:*
	Nessa pasta há o relatório de erros de cada um dos arquivos .xml e ao final há o mesmo relatório que abre automaticamente
	em uma página do seu navegador.


	*pmc_package:*
	Para revistas que apresentam o título abreviado NLM, o programa retira os elementos de especificação SciELO e mantém apenas
	os elementos necessários para envio ao PMC.
	Os elementos que são retirados do documento XML para envio ao PMC são: detalhamento em afiliação, informação de financiamento
	em <funding-group> e <mixed-citation>.


	*pmc_package_zips:*
	Ao validar o pacote pmc_package o programa, automaticamente, zipa a pasta que está pronta para envio.


	*scielo_package:*
	No momento da validação do pacote XML o programa verifica as entidades (numéricas ou alfa-numéricas) que existem no documento
	e, automaticamente, converte para o caractere correspondente. Evitando futuros problemas de entidades. O ideal é utilizar os 
	arquivos .xml validados nessa pasta em vez de utilizar os xmls do pacote.


	*scielo_package_zips:*
	Ao validar o pacote scielo_package o programa, automaticamente, zipa a pasta já com a nomeação padrão SciELO que está pronta 
	para envio.


	*work:*
	é uma pasta de arquivos temporários usadas para a geração do resultado. ela pode ser apagada se desejável, mas também pode ser 
	usada para fins de suporte.

Essa estrutura de pastas é a mesma apresentada se o usuário utilizar o programa Package Maker (AQUI REFERENCIAR). Para verificar os relatórios apresentados, basta entrar na pasta "errors" e abrir o documento com extensão: ".contents.html".


Suporte SciELO
==============

Em caso de dúvidas com relação à utilização do programa Markup ou erros apresentados ao gerar o arquivo .xml, enviar e-mail para a lista de discussões SciELO-discuss:

<scielo-discuss@googlegroups.com>