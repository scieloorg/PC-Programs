.. _relatorios:

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



Suporte SciELO
==============

Em caso de dúvidas com relação à utilização do programa Markup ou erros apresentados ao gerar o arquivo .xml, enviar e-mail para a lista de discussões SciELO-discuss:

<scielo-discuss@googlegroups.com>