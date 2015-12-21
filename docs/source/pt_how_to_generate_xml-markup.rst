.. pt_how_to_generate_xml-markup:

==================
Como usar o Markup
==================

Introdução
==========

Este manual tem como objetivo apresentar o uso do programa de marcação `Markup <markup.html>`_ 


.. _sugestao-id:

Sugestão de Atribuição de “ID”
==============================

Alguns elementos exigem o atributo "ID".
Para composição do “ID” combine o prefixo do tipo do elemento e um número inteiro, como segue:

+------------------------+---------------------------+---------+---------------------+
| Elemento XML           | Descrição                 | Prefixo | Exemplo             |
+========================+===========================+=========+=====================+
| aff                    | Afiliação                 | aff     | aff1, aff2, ...     |
+------------------------+---------------------------+---------+---------------------+
| app                    | Apêndice                  | app     | app1, app2, ...     |
+------------------------+---------------------------+---------+---------------------+
| author-notes/fn |      | Notas de rodapé do artigo | fn      | fn1, fn2, ...       | 
| fn-group/fn            |                           |         |                     |
+------------------------+---------------------------+---------+---------------------+
| boxed-text             | Caixa de texto            | bx      | bx1, bx2, ...       |
+------------------------+---------------------------+---------+---------------------+
| corresp                | Correspondência           | c       | c1, c2, ...         |
+------------------------+---------------------------+---------+---------------------+
| def-list               | Lista de Definições       | d       | d1, d2, ...         |
+------------------------+---------------------------+---------+---------------------+
| disp-formula           | Equações                  | e       | e1, e2, ...         |
+------------------------+---------------------------+---------+---------------------+
| fig                    | Figuras                   | f       | f1, f2, ...         |
+------------------------+---------------------------+---------+---------------------+
| glossary               | Glossário                 | gl      | gl1, gl2, ...       |
+------------------------+---------------------------+---------+---------------------+
| media                  | Media                     | m       | m1, m2, ...         |
+------------------------+---------------------------+---------+---------------------+
| ref                    | Referência bibliográfica  | B       | B1, B2, ...         |
+------------------------+---------------------------+---------+---------------------+
| sec                    | Seções                    | sec     | sec1, sec2, ...     |
+------------------------+---------------------------+---------+---------------------+
| sub-article            | sub-artigo                | S       | S1, S2, ...         |
+------------------------+---------------------------+---------+---------------------+
| supplementary-material | Suplemento                | suppl   | suppl1, suppl2, ... |
+------------------------+---------------------------+---------+---------------------+
| table-wrap-foot/fn     | Notas de rodapé de tabela | TFN     | TFN1, TFN2, ...     |
+------------------------+---------------------------+---------+---------------------+
| table-wrap             | Tabela                    | t       | t1, t2, ...         |
+------------------------+---------------------------+---------+---------------------+



.. _update-titles:

Atualização de Títulos
======================

Para atualizar os títutos de periódicos SciELO, clique em iniciar (img), em seguida em "Todos os Programas", depois disso clique na pasta onde o programa Markup foi instalado e então clique em "Markup - update journals list".

O programa abre uma janela onde o usuário pode optar em carregar os títulos dos periódicos SciELO BR + SciELO rede, ou atualizar os títulos dos periódicos de uma única coleção.
Veja qual é o procedimento para atualizar os títulos de SciELO BR + SciELO Rede:
Clique em "All" e então em [download]:

.. image:: img/mkp-atualiza-all.jpg
   :height: 300px
   :align: center


O programa carrega todos os títulos dos periódicos SciELO. Para conferir clique em ‘close’, entre na pasta onde o programa foi instalado, exemplo:
C:\markup90trial\bin\markup

Dentro da pasta markup, abra o arquivo .csv "markup_journals.csv" e perceba que na planilha há  títulos de periódicos das diversas coleções do SciELO e também da coleção do SciELO BR.

.. image:: img/mkp-lista-titles.jpg
   :height: 400px
   :align: center


Caso queira atualizar os periódicos de uma única coleção, clique em iniciar, em seguida em "Markup - update journals list", selecione a coleção desejada e clique em [download]:


.. image:: img/download_journals_data.png
   :height: 300px
   :align: center


Para conferir, clique em ‘close’ e confira os títulos disponíveis no arquivo: "markup_journals.csv".

.. raw:: html
  <div>
   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=SNAXZ1BaMM0&index=5&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>
  </div>


.. raw:: html

  <div>
     <iframe width="560" height="315" src="https://www.youtube.com/watch?v=SNAXZ1BaMM0&index=5&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>
  </div>


.. _markup:

Dados Básicos
=============

Estando o arquivo formatado de acordo com o manual `Preparação de Arquivos para o Programa Markup <pt_how_to_generate_xml-prepara.html>`_ e aberto no programa `Markup <markup.html>`_, selecione a tag [doc]:

.. image:: img/doc-mkp-formulario.jpg
   :height: 400px
   :align: center


Perceba que ao clicar em [doc] o programa irá abrir uma caixa de diálogo onde deverá ser completado com os dados básicos do documento:

Insira o nome do periódico no campo “collection/journal” que o programa irá inserir as informações da revista automaticamente. 
Feito isso, o próximo passo é completar as informações nos demais campos. Veja abaixo os campos que devem ser preenchidos:


+-------------------+-----------------------------------------------------------------------------------------------+
| Campo             | Descrição                                                                                     |
+===================+===============================================================================================+
| license           | se não for inserido automaticamente, preencher com a URL da licença creative commons          |
|                   | adotada pelo periódico. Consultar licenças em:                                                |
|                   | http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.3-branch/tagset.html#license |
+-------------------+-----------------------------------------------------------------------------------------------+
| volid             | Inserir volume, se existir. Para Ahead of Print, não incluir volume                           |
+-------------------+-----------------------------------------------------------------------------------------------+
| supplvol          | Caso seja um suplemento de volume incluir sua parte ou número correspondente.                 |
|                   | **Exemplo: vol.12 supl.A**, então preencha com **A**, neste campo                             |
+-------------------+-----------------------------------------------------------------------------------------------+
| issueno           | Entre com o número do fascículo. Caso seja um artigo publicado em ahead of                    |
|                   | print, insira ahead neste campo                                                               |
+-------------------+-----------------------------------------------------------------------------------------------+
| supplno           | Caso seja um suplemento de fascículo incluir sua parte ou número                              |
|                   | correspondente. **Exemplo: n.37, supl.A**, então preencha com **A** neste campo               |
+-------------------+-----------------------------------------------------------------------------------------------+
| isidpart          | Usar em casos de press release, incluindo a sigla pr                                          |
+-------------------+-----------------------------------------------------------------------------------------------+
| dateiso           | Data de publicação formada por ano, mês e dia **(YYYYMMDD)**. Preencher sempre                |
|                   | com o último mês da periodicidade. Por exemplo, se o periódico é bimestral                    |
|                   | preencher **20140600**. Use **00** para mês e dia nos casos em não haja sua                   |
|                   | identificação. **Exemplo: 20140000**.                                                         |
+-------------------+-----------------------------------------------------------------------------------------------+
| month/season      | Entre o mês ou mês inicial barra final, em inglês (três letras) e ponto,                      |
|                   | exceto para May, June e July. **Ex.: May/June, July/Aug.**                                    |
+-------------------+-----------------------------------------------------------------------------------------------+
| fpage             | Primeira página do documento. Para artigo em Ahead of Print, incluir 00                       |
+-------------------+-----------------------------------------------------------------------------------------------+
| @seq              | Para artigos que iniciam na mesma página de um artigo anterior, incluir a                     |
|                   | sequência com letra                                                                           |
+-------------------+-----------------------------------------------------------------------------------------------+
| lpage             | Inserir a última página do documento.                                                         |
+-------------------+-----------------------------------------------------------------------------------------------+
| elocatid          | Incluir paginação eletrônica. Neste caso não preencher fpage e lpage                          |
+-------------------+-----------------------------------------------------------------------------------------------+
| order (in TOC)    | Incluir a ordem do artigo no sumário do fascículo. Deve ter, no mínimo, dois                  |
|                   | dígitos. Por exemplo, se o artigo for o primeiro do sumário, preencha este                    |
|                   | campo com **01** e assim por diante.                                                          |
+-------------------+-----------------------------------------------------------------------------------------------+
| pagcount*         | Inserir o total de paginação. Para Ahead of Print, incluir o valor 1                          |
+-------------------+-----------------------------------------------------------------------------------------------+
| doctopic*         | Informar o tipo de documento a ser marcado. Por exemplo: artigo original, resenha,            | 
|                   | carta, comentário, etc. No caso de Ahead Of Print, incluir sempre o tipo artigo original,     |
|                   | exceto para errata                                                                            |
+-------------------+-----------------------------------------------------------------------------------------------+
| language*         | Informe o idioma principal do texto a ser marcado                                             |
+-------------------+-----------------------------------------------------------------------------------------------+
| version*          | Identifica a versão da DTD usada no processo de marcação (A versão atual é 4.0)               |
+-------------------+-----------------------------------------------------------------------------------------------+
| artdate (rolling) | Obrigatório completar com a data **YYYYMMDD** quando for um artigo rolling pass.              |
|                   | Rolling pass é um modelo publicação onde o periódico publica seus artigos num volume          |
|                   | único a medida em que estes ficam prontos                                                     |
+-------------------+-----------------------------------------------------------------------------------------------+
| ahpdate           | Indicar a data de publicação de um artigo publicado em ahead of print                         |
+-------------------+-----------------------------------------------------------------------------------------------+


.. note:: Os campos que apresentam um asterisco ao lado, são campos obrigatórios.


.. _front:

Front
=====

Tendo preenchido todos os campos, ao clicar em [Ok] o programa irá abrir uma janela perguntando se o documento está de acordo com o modelo para efetuar a marcação automática:

.. image:: img/doc-mkp-mkp-automatic.jpg
   :height: 450px
   :align: center


Ao clicar em [Sim] veja que o programa efetua a marcação automática dos elementos básicos do documento:

.. image:: img/doc-mkp-mkp--auto.jpg
   :height: 400px
   :width: 300px
   :align: center


.. note:: Caso o arquivo esteja com a formatação recomendada, o programa Markup irá fazer a marcação automática de DOI, seção 
          (esses dois primeiros, se presente), título e títulos traduzidos, autores, label de autores e afiliações.
          Caso o arquivo não esteja na formatação recomendada em “Preparação de Arquivos para o Programa Markup”, o programa 
          não identificará corretamente os elementos.



Após a marcação automática é necessário completar a marcação dos elementos básicos. 


.. _titulo:

Doctitle
--------

Confira o idioma inserido em [doctitle] para títulos traduzidos e se necessário, corrija.
Para corrigir, selecione a tag "incorreta" e clique no botão "lápis" para editar os atributos:


.. image:: img/doc-mkp-language-doctitle.jpg
   :height: 400px
   :align: center

Faça o mesmo para os demais títulos traduzidos.


.. _autores:

Autores
-------

Alguns autores apresentam mais que 1 label ao lado do nome, porém o programa não faz a marcação automática de mais que 1 label. Para isso, selecione o label do autor e identifique com o elemento [xref]. Veja:


.. image:: img/doc-mkp-xref-label.jpg
   :height: 300px
   :align: center

Note que para identificar o label de autor relacionado à afiliação, o tipo de xref (ref-type) selecionado foi o "affiliation" e o rid "aff3" para relacionar o label 3 à afiliação correspondente.

O programa Markup não faz marcação automática de função de autor como, por exemplo, o cargo exercido. Para isso é necessário selecionar a informação que consta ao lado do nome do autor, ir para o nível inferior do elemento [author] e identificar esse dado com a tag [role]. Veja:


.. image:: img/doc-mkp-role-author.jpg
   :height: 230px
   :align: center


.. image:: img/doc-mkp-mkp-role-author.jpg
   :height: 230px
   :align: center


.. note:: O programa não identifica automaticamente símbolos ou letras como label, a qual deve ser marcada manualmente, observando-se 
          o tipo de referência cruzada a ser incluída.


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=R8YYjXZSk1c&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH&index=6" frameborder="0" allowfullscreen></iframe>


Contrib-ID
==========
Autores que apresentam registro no ORCID ou no Lattes devem inserir o link de registro ao lado do nome, após o label do autor:

 .. image:: img/mkp-contrib-id.jpg
   :height: 230px
   :align: center

Ao fazer a marcação de [doc] o programa identificará automaticamente todos os dados iniciais do documento, inclusive marcará em [author] o link de registro do autor.
Ainda que o programa inclua o link na tag [author], será necessário completar a marcação desse dado.

Para isso, entre no nível de author, selecione o link do autor e clique em [author-id].
O programa abrirá uma janela onde deverá ser indicado o tipo de registro do autor: se lattes ou ORCID. 

 .. image:: img/mkp-marcando-id-contrib.jpg
   :height: 230px
   :align: center

Selecione o tipo correto e clique em [Continuar].



.. _afiliação:

Afiliações
----------

O Programa Markup faz a identificação apenas de [normaff] de afiliações, ou seja, o detalhamento das afiliações não é feito automaticamente.
Ao fazer a marcação automática dos elementos básicos do arquivo, complete a marcação de afiliações identificando: instituição maior [orgname], divisão 1 [orgdiv1], divisão 2 [orgdiv2], cidade [city], estado [state] (esses 4 ultimos, se presentes) e o país [country].

Para fazer a identificação dos elementos acima vá para o nível inferior do elemento [normaff] e faça o detalhamento de cada afiliação. Veja:


.. image:: img/doc-mkp-detalhamento-aff.jpg
   :height: 350px
   :align: center


Após o detalhamento de afiliações o próximo passo é fazer a normalização das instituições e países. Para isso, selecione o elemento [normaff] e clique no "lapis" para editar os atributos. O programa irá apresentar uma janela para normalização dos elementos indicados nos campos em branco. Veja:


.. image:: img/doc-mkp-normalizacao-aff.jpg
   :height: 350px
   :align: center



No campo "icountry" selecione o país da instituição maior (orgname), em seguida clique em "find" para encontrar a instituição normalizada. Ao fazer esse procedimento, o programa Markup consultará nossa base de dados de instituições normalizadas e verificará se a instituição selecionada foi normalizada e consta na lista.


.. image:: img/doc-mkp-normalizadas.jpg
   :height: 350px
   :align: center



.. image:: img/doc-mkp-aff.jpg
   :height: 150px
   :align: center



.. note:: Faça a busca pelo idioma de origem da instituição, exceto para línguas não latinas, quando a consulta deverá 
         ser feita em inglês. Caso a instituição não exista na lista do Markup, selecione o elemento "No match found" e clique em [OK].


.. _resumo:

Resumos
=======

Os resumos devem ser identificados manualmente. Para marcação de resumos simples (não apresentam seções) e para os resumos estruturados (apresentam seções) utilizar o elemento [xmlabstr]. Na marcação selecione o título do resumo e o texto e em seguida marque com o botão [xmlabstr], dessa forma a interface web do SciELO assumirá a forma como o periódico adota para identificar o elemento.
Observe que ao utilizar o [xmlabstr] para resumos simples, o programa marca automaticamente o título e o parágrafo do resumo:

Resumo sem Seção:
-----------------

**selecionando:** 

.. image:: img/doc-mkp-select-abstract-s.jpg
   :height: 350px
   :align: center


Na sequência clique em [xmlabstr] o programa abrirá uma janela a qual deverá ser indicado o idioma do resumo marcado:


**marcação:** 

.. image:: img/doc-mkp-idioma-resumo.jpg
   :height: 350px
   :width: 450px
   :align: center


**Resultado**

.. image:: img/doc-mkp-mkp-abstract.jpg
   :align: center


Já em resumos estruturados, além do programa identificar o título automaticamente é identificado também cada seção do resumo e seus respectivos parágrafos. Veja:


Resumo com Seção:
-----------------

Siga os mesmos passos descritos para resumo sem seção:


**selecionando:** 

.. image:: img/doc-mkp-select-abstract.jpg
   :align: center


**marcação:**
		  
.. image:: img/doc-mkp-idioma-abstract.jpg
   :height: 400px
   :align: center


**Resultado**

.. image:: img/doc-mkp-mkp-resumo.jpg
   :align: center


.. raw:: html

   <iframe width="853" height="480" src="https://www.youtube.com/watch?v=FVTjDOIGV0Y&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH&index=7" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>


.. _palavra-chave:

Keywords
========

O programa Markup apresenta duas tags para identificação de palavra-chave, a tag [*kwdgrp] e [kwdgrp].
A tag [*kwdgrp], com asterisco, é utilizada para identificação automática de cada palavra-chave e também do título. Para isso, selecione toda a informação inclusive o título e identifique os dados com o elemento [*kwdgrp].

Marcação Automática:
--------------------

**selecionando:**
 
.. image:: img/doc-mkp-select-kwd.jpg
   :height: 300px
   :align: center


Ao clicar em [*kwdgrp] o programa abrirá uma janela a qual deverá ser indicado o idioma das palavra-chave marcada:


**marcação:** 

.. image:: img/doc-mkp-mkp-kwd.jpg
   :height: 300px
   :align: center


.. image:: img/doc-mkp-kwd-grp.jpg
   :height: 100px
   :align: center

         

Marcação Manual:
----------------

Caso a marcação automática não ocorra conforme o esperado, pode-se marcar o grupo de palavras-chave manualmente. Selecione o grupo de palavras e marque com o elemento [kwdgrp] conforme abaixo:


**marcação:**

.. image:: img/doc-mkp-selection-kwd-s.jpg
   :height: 350px
   :align: center



Feita a marcação de todos os dados de palavras-chave, o próximo passo é fazer a identificação de item por item, iniciando pelo título. Para isso selecione o título das palavras-chave e identifique com o elemento [sectitle]:

.. image:: img/doc-mkp-sec-kwd.jpg
   :height: 300px
   :align: center


Em seguida selecione palavra por palavra e identifique com o elemento [kwd]:

.. image:: img/doc-mkp-kwd-kwd.jpg
   :height: 300px
   :align: center



.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=6sNTlHF8WdU&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH&index=9" frameborder="0" allowfullscreen></iframe>



.. _historico:

History
=======

O elemento [hist] é utilizado para identificar o histórico do documento. Para isso selecione toda a informação de histórico e marque com o elemento [hist]:


.. image:: img/doc-mkp-hist-select.jpg
   :height: 250px
   :align: center



Feito isso selecione a data de recebido e identifique com o elemento [received]. Confira a data ISO indicada no campo dateiso e corrija, se necessário. A estrutura da data ISO esperada nesse campo é:
ANO MÊS DIA. Veja:

.. image:: img/doc-mkp-received.jpg
   :height: 350px
   :align: center


Caso haja a data de revisado, selecione o dado e identifique com o elemento [revised]. Faça o mesmo para a data de aceito; selecione a data e identitique com o elemento [accepted]. Confira a data ISO indicada no campo dateisso e corrija se necessário. Veja:

.. image:: img/doc-mkp-accepted.jpg
   :height: 350px
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=w4Bw7dXpS0E&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH&index=8" frameborder="0" allowfullscreen></iframe>
   


.. _correspondencia:

Correspondência
===============

CCom o elemento [corresp] é possível fazer a identificação dos dados de correspondência do autor. Essa tag possui um subnível para identificação do e-mail do autor. Para identificar esse dado, selecione toda a informação de correspondência e marque com o elemento [corresp]. Será apresentada uma janela para identificação do id de correspondência que, nesse caso, deve ser “c” + o número de ordem da correspondência.

.. image:: img/doc-mkp-corresp-select.jpg
   :height: 300px
   :align: center


Selecione o e-mail do autor correspondente e identifique com o elemento [email] e suba um nível para marcar o próximo elemento.

.. image:: img/doc-mkp-email-corresp.jpg
   :height: 300px
   :align: center

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=fuzSrOMlSvo&index=10&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _ensaio-clinico:

Ensaio Clínico
==============
Cada ensaio clínico deve ter um protocolo, ou plano de ação que descreve o que será feito no estudo, como será conduzido, e por que cada parte do estudo é necessária - incluindo detalhes como os critérios para a participação do paciente, o calendário de testes, procedimentos e medicamentos, bem como a duração do estudo. Informações retiradas do site <http://www.nlm.nih.gov/services/faqctgov.html>

Arquivos que apresentam informação de ensaio clínico com número de registro, devem ser identificados pela tag [cltrial]:

.. image:: img/doc-mkp-tag-cltrial.jpg
   :height: 150px
   :align: center


O programa abrirá uma janela com 2 campos para identificação da URL da base de dados onde o Ensaio foi indexado e um campo "ctdbid" para selecionar a base correspondente:

.. image:: img/doc-mkp-clinicaltr.jpg
   :height: 300px
   :align: center

Para encontrar a URL do ensaio clínico faça uma busca na internet pelo número de registro para preenchimento do atributo conforme exemplo abaixo.

.. image:: img/doc-mkp-ensaio.jpg
   :height: 80px
   :align: center

.. note:: Comumente a informação de ensaio clínico está posicionada abaixo de resumos ou palavras-chave.


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=0bln_fugnAA&index=12&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _referencias:

Referências
===========

As referências bibliográficas são identificadas elemento a elemento e seu formato original é mantido para apresentação no SciELO.

O programa identificará todas as referências selecionadas com a tag [ref] do tipo [book]. A alteração do tipo de referência será manual ou automática, dependendo do tipo de elemento marcado, conforme poderá ser observado adiante.


.. image:: img/doc-mkp-select-refs-mkp.jpg
   :height: 400px
   :align: center



.. image:: img/doc-mkp-mkp-refs.jpg
   :height: 400px
   :align: center

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=MoTVIJk21UM&index=13&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>   


.. _tipos-de-referencias:

Tipos de Referências
--------------------

A partir da marcação feita, alguns tipos de referência serão alterados automaticamente sem intervenção manual (ex.: tese, conferência e artigo de periódico); já para os demais casos, será necessária a alteração manual.
Para alterar o tipo de referência clique no elemento [ref] e em seguida clique no lápis "Editar Atributos" e em "reftype" selecione o tipo correto.

.. image:: img/doc-mkp-edit-ref-type.jpg
   :height: 400px
   :align: center


.. image:: img/doc-mkp-ref-editado-legal-doc.jpg
   :height: 150px
   :width: 400px
   :align: center


Entretanto, recomendamos que edite o "reftype" somente **após** marcar todos os elementos da [ref], pois dependendo dos elementos marcados o "reftype" pode ser alterado automaticamente pelo Markup. 

.. note:: Uma referência deve ter sua tipologia sempre baseada no seu conteúdo e nunca no seu suporte. Ou seja uma lei representa um
          documento legal, portanto o tipo de referência é “legal-doc”, não importa se foi publicado em um journal ou site. Uma referência de artigo de um periódico científico, mesmo que publicado em um site possui o tipo “journal”. 
          É importante entender estes aspectos nas referências para poder interpretar sua tipologia e seus elementos. Nem toda referência que possui um link é uma “webpage”, nem toda a referência que possui um volume é um “journal”, livros também podem ter volumes.


Abaixo seguem os tipos de referência suportados por SciELO e a marcação de cada [ref].


.. _tese:

Thesis
^^^^^^
Utilizada para referenciar monografias, dissertações ou teses para obtenção de um grau acadêmico, tais como livre-docência, doutorado, mestrado, bacharelado, licenciatura, etc. A seleção do elemento [thesgrp] determinará a alteração do tipo [book] para [thesis]. Ex:


   *PINHEIRO, Fernanda Domingos. Em defesa da liberdade: libertos e livres de cor nos tribunais do Antigo Regime português (Mariana e Lisboa, 1720-1819). Tese de doutorado, Departamento de História, Instituto de Filosofia e Ciências Humanas, Universidade Estadual de Campinas, 2013*

.. image:: img/doc-mkp-ref-thesis.jpg
   :height: 200px
   :align: center



.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=h1ytjcXZv5U&index=21&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _conferencia:

Confproc
^^^^^^^^
Utilizada para referenciar documentos relacionados à eventos: atas, anais, resultados, proceedings, convenções, conferências entre outros. Ao marcar o elemento [confgrp] o programa alterará o tipo de referência para [confproc]. Ex.:


   *FABRE, C. Interpretation of nominal compounds: combining domain-independent and domain-specific information. In: INTERNATIONAL CONFERENCE ON COMPUTATIONAL LINGUISTICS (COLING), 16, 1996, Stroudsburg. Proceedings... Stroudsburg: Association of Computational Linguistics, 1996. v.1, p.364-369.*


.. image:: img/doc-mkp-ref-confproc.jpg
   :height: 250px
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=k0OWNjboFWE&index=16&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>



.. _relatorio:

Report
^^^^^^
Utilizada para referenciar relatórios técnicos, normalmente de autoria institucional. Ao marcar o elemento [reportid] o programa alterará o tipo de referência para [report]. Ex.:


   *AMES, A.; MACHADO, F.; RENNÓ, L. R. SAMUELS, D.; SMITH, A.E.; ZUCCO, C. The Brazilian Electoral Panel Studies (BEPS): Brazilian Public Opinion in the 2010 Presidential Elections. Technical Note No. IDB-TN-508, Inter-American Development Bank, Department of Research and Chief Economist, 2013.*


.. image:: img/doc-mkp-ref-report.jpg
   :height: 250px
   :align: center



.. _patente:

Patent
^^^^^^

Utilizada para referenciar patentes; a patente representa um título de propriedade que confere ao seu titular o direito de impedir terceiros explorarem sua criação.. Ex.:


   *SCHILLING, C.; DOS SANTOS, J. Method and Device for Linking at Least Two Adjoinig Work Pieces by Friction Welding, U.S. Patent WO/2001/036144, 2005.*

.. image:: img/doc-mkp-patent.jpg
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=4BffTcmIkF8&index=20&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _lei:

legal-doc
^^^^^^^^^

Utilizada para referenciar documentos jurídicos, incluem informações sobre, legislação, jurisprudência e doutrina. Ex.:


   *Brasil. Portaria no 1169/GM em 15 de junho de 2004. Institui a Política Nacional de Atenção Cardiovascular de Alta Complexidade, e dá outras providências. Diário Oficial 2004; seção 1, n.115, p.57.*

.. image:: img/doc-mkp-ref-legal-doc1.jpg
   :height: 180px
   :align: center


.. _jornal:

Newspaper
^^^^^^^^^
Utilizada para referenciar publicações seriadas sem cunho científico, como revistas e jornais. Ex.:


   *TAVARES de ALMEIDA, M. H. "Mais do que meros rótulos". Artigo publicado no Jornal Folha de S. Paulo, no dia 25/02/2006, na coluna Opinião, p. A. 3.*

.. image:: img/doc-mkp-newspaper.jpg
   :align: center


.. _livro:

Book
^^^^

Utilizada para referenciar livros ou parte deles (capítulos, tomos, séries e etc), manuais, guias, catálogos, enciclopédias, dicionários entre outros.
Ex.: 

   *LORD, A. B. The singer of tales. 4th. Cambridge: Harvard University Press, 1981.*


.. image:: img/doc-mkp-ref-book.jpg
   :height: 180px
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=geq2_UgMYa0&index=17&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>



.. _livro-inpress:

Book no prelo
^^^^^^^^^^^^^

Livros finalizados, porém em fase de edição geralmente ao final da referência é apresentado a informação "no prelo", "forthcomming" ou "“in press”". A marcação para referências do tipo book com essa particularidade deve ser feita conforme segue na imagem abaixo:


   *CIRENO, F.; LUBAMBO, C. Estratégia eleitoral e eleições para Câmara dos Deputados no Brasil em 2006, no prelo.*

.. image:: img/doc-mkp-ref-book-no-prelo.jpg
   :height: 180px
   :align: center

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=P2fiGsmitqM&index=15&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _capitulo-de-livro:

Book Chapter
^^^^^^^^^^^^

Divisão de um documento (título do artigo e seus respectivos autores - Podendo ou não constar informação de autores- , seguido do título do livro e seus respectivos autores) numerado ou não


   *Lastres, H.M.M.; Ferraz, J.C. Economia da informação, do conhecimento e do aprendizado. In: Lastres, H.M.M.; Albagli, S. (Org.). Informação e globalização na era do conhecimento. Rio de Janeiro: Campus, 1999. p.27-57.*

.. image:: img/doc-mkp-ref-chapter-book.jpg
   :height: 300px
   :align: center


.. _revista:

journal
^^^^^^^

Utilizada para referenciar publicações seriadas científicas, como revistas, boletins e jornais, editadas em unidades sucessivas, com designações numéricas e/ou cronológicas e destinada a ser continuada indefinidamente. Ao marcar [arttile] o programa alterará o tipo de referência para [journal]. Ex.:


   *Cardinalli, I. (2011). A saúde e a doença mental segundo a fenomenologia existencial. Revista da Associação Brasileira de Daseinsanalyse, São Paulo, 16, 98-114.*

.. image:: img/doc-mkp-ref-journal.jpg
   :height: 200px
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=2gD6Ej1v0h4&index=14&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>



Nas referências abaixo, seu tipo deverá ser alterado manualmente de [book] para o tipo correspondente.


.. _base-de-dados:

Database
^^^^^^^^ 

Utilizada para referenciar bases e bancos de dados. Ex.:


	*IPEADATA. Disponível em: http://www.ipeadata.gov.br.  Acesso em: 12 fev. 2010.*

.. image:: img/doc-mkp-ref-database.jpg
   :height: 100px
   :align: center


.. _software:

Software
^^^^^^^^

Utilizada para referenciar um software, um programa de computador. Ex.:


	*Nelson KN. Comprehensive body composition software [computer program on disk]. Release 1.0 for DOS. Champaign (IL): Human Kinetics, c1997. 1 computer disk: color, 3 1/2 in.*

.. image:: img/doc-mkp-ref-software.jpg
   :height: 200px
   :align: center

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=KMaiNAJ__U4&index=18&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _web:

Webpage
^^^^^^^

Utilizada para referenciar, web sites ou informações contidas em blogs, twiter, facebook, listas de discussões dentre outros. 

**Exemplo 1**

   *UOL JOGOS. Fórum de jogos online: Por que os portugas falam que o sotaque português do Brasil é açucarado???, 2011. Disponível em <http://forum.jogos.uol.com.br/_t_1293567>. Acessado em 06 de fevereiro de 2014.*

.. image:: img/doc-mkp-ref-web-uol.jpg
   :align: center


**Exemplo 2**

   *BANCO CENTRAL DO BRASIL. Disponível em: www.bcb.gov.br.*

.. image:: img/doc-mkp-ref-web-bb.jpg
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=EwufVmJ4R74&index=19&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _outro:

Other
^^^^^

Utilizada para referenciar tipos não previstos pelo SciELO. Ex.:


   *INAC. Grupo Nacional de Canto e Dança da República Popular de Moçambique. Maputo, [s.d.].*

.. image:: img/doc-mkp-ref-other.jpg
   :align: center



.. _previous:

"Previous" em Referências
=========================

Há normas que permitem que as obras que referenciam a mesma autoria repetidamente, sejam substituídas por um traço sublinear equivalente à seis espaços. Ex.:


*______. Another one bites the dust: Merck cans hep C fighter Victrelis as new meds take flight [Internet]. Washington: FiercePharma; 2015.*

Ao fazer a marcação de [refs] o programa duplicará a referência com previous da seguinte forma:

[ref id="r16" reftype="book"] [text-ref]______. Another one bites the dust: Merck cans hep C fighter Victrelis as new meds take flight &#91;Internet&#93;. Washington: FiercePharma; 2015[/text-ref]. *______. Another one bites the dust: Merck cans hep C fighter Victrelis as new meds take flight &#91;Internet&#93;. Washington: FiercePharma; 2015*[/ref]

A marcação da referência deverá ser feita após *[/text-ref]*

.. note:: Em referências que apresentam o elemento [text-ref], o dado a ser marcado deverá ser o que consta após o [/text-ref]. 
          Nunca fazer a marcação da referência que consta em [text-ref][/text-ref].

Para identificação de referências com esse tipo de dado, selecione os traços sublineares e identifique com a tag [*authors] com asterisco. Dessa forma o programa recuperará o nome do autor da referência anterior e fará a identificação automática do grupo de autores, identificando o sobrenome e o primeiro nome.



.. _automata:

Marcação Automática
-------------------

O programa Markup dispõe de uma funcionalidade que otimiza o processo de marcação das referências bibliográficas que seguem “à risca” a norma Vancouver. Caso haja adaptações o programa não fará a identificação corretamente.


**Selecione todas as referências**

.. image:: img/doc-mkp-automata-select.jpg
   :align: center


**Clique no botão "Markup: Marcação Automática 2"**

.. image:: img/doc-mkp-automata.jpg
   :align: center


Após esse procedimento, todas as referências foram marcadas automaticamente e de forma detalhada.

.. image:: img/doc-mkp-ref-mkup-automata.jpg
   :align: center


Apesar do programa fazer a marcação automática das referências, o responsável pela marcação deve analisar atentamente referência por referência afim de verificar se alguma referência não foi identificada corretamente ou se alguma ref não foi marcada.
Caso alguma referência não tenha sido identificada ou tenha sido identificada incorretamente, basta entrar no nível de [refs] em "Barras de Ferramentas Personalizadas" e fazer a identificação dos elementos necessários.

.. note:: Essa identificação automática só é possível caso as referências bibliográficas estejam de acordo com a norma Vancouver, seguindo-a literalmente. 
          Para outras normas não existe esta funcionalidade, devendo a marcação ser manual..


.. _nota-de-rodape:

Notas de Rodapé
===============

As notas de rodapé podem ser identificadas antes do corpo do texto ou depois. Não há uma posição específica dentro do arquivo .doc. Entretando é necessário avaliar a nota indicada, pois dependendo do tipo de nota inserido em fn-type, o programa gera o arquivo .xml com informações de notas de autores nos metadados do artigo ou em ``<back>``. Para mais informações sobre essa divisão consultar na documentação SPS os itens <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.2-branch/tagset.html#notas-de-autor> e <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.2-branch/tagset.html#notas-gerais>.

Para identificar uma nota selecione o dado indicado e marque com o elemento [fngrp].

.. image:: img/doc-mkp-select-fn-contri.jpg
   :height: 350px
   :align: center


Caso a nota apresente um título ou um símbolo, selecione a informação e identifique com o elemento [label]:

.. image:: img/doc-mkp-fn-label-con.jpg
   :height: 200px
   :align: center


Tipos de notas
--------------

Suporte sem Informação de Financiamento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Para notas de rodapé que apresentam informação de suporte de entidade, instituição ou pessoa física sem informação de financiamento e número de contrato, selecionar o tipo "Pesquisa na qual o artigo é baseado foi apoiado por alguma entidade":


.. image:: img/doc-mkp-fn-supp.jpg
   :height: 250px
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=a_b9uzylEUU&index=30&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


Suporte com Informação de Financiamento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Notas de rodapé que apresentam informação de financiamento com número de contrato devem ter como "fntype" a informação "Declaração ou negação de recebimento de financiamento em apoio à pesquisa na qual o artigo é baseado". Esse tipo de nota de rodapé que possui um número de contrato, será necessária a marcação de dados de financiamento.
Para marcar o financiamento selecione toda nota e identifique com o elemento [funding]:

.. image:: img/doc-mkp-select-fn-fdiscl.jpg
   :height: 300px
   :align: center


Feito isso, o próximo passo é selecionar o primeiro grupo de instituição financiadora + número de contrato e identificar com o elemento [award].

.. image:: img/doc-mkp-award-select.jpg
   :height: 200px
   :align: center


Após a identificação de [award] selecione a instituição financiadora e marque com o elemento [fundsrc]:

.. image:: img/doc-mkp-fund-source-fn.jpg
   :height: 200px
   :align: center


Depois selecione cada número de contrato e identifique com o elemento [contract]:

.. image:: img/doc-mkp-contract-fn.jpg
   :height: 300px
   :align: center


Caso a nota de rodapé apresente mais que uma instituição financiadora e número de contrato, faça a marcação conforme segue o exemplo abaixo:

.. image:: img/doc-mkp-mkp-fn-fund-2.jpg
   :height: 300px
   :align: center
   

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=FVTnNPGqWiU&index=31&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _fn-automatico:

Notas - Identificação Automática
=========================

Para notas de rodapé que estão posicionadas ao fim de cada página no documento, com formatação de notas de rodapé do Word, é possível fazer a marcação automática do número referenciado no documento e da nota de rodapé.

As chamadas no corpo do texto para notas de rodapé deverão estar com uma formatação simples: em formato numérico e em "sup".
Já as notas deverão estar com a formatação de nota de rodapé do Word e além disso,  deve ser inserido um espaço antes da nota. Veja:

.. image:: img/mkp-espaco-fn.jpg
   :height: 300px
   :align: center

Estando formatado corretamente, clique com o mouse em qualquer parágrafo e em seguida clique na tag [*fn].

.. image:: img/mkp-botao-fn.jpg
   :height: 300px
   :align: center

Ao clicar em [*fn] o programa faz a marcação automática de [xref] no corpo do texto e também da nota ao pé da página.

.. image:: img/mkp-nota-automatico.jpg
   :height: 300px
   :align: center



.. _apendice:

Apêndices
=========

A identificação de apêndices, anexos e materiais suplementares devem ser feitas pela tag [appgrp]:

.. image:: img/doc-mkp-element-app.jpg
   :height: 100px
   :align: center

Selecione todo o grupo de de apêndice, inclusive o título, se existir. Depois clique em [appgrp]:


.. image:: img/doc-mkp-app.jpg
   :height: 300px
   :align: center


Selecione apêndice por apêndice e identifique com o elemento [app]

.. image:: img/doc-mkp-id-app.jpg
   :height: 300px
   :align: center

.. note:: o id deve ser sempre único no documento.

Caso o apêndice seja de figura, tabela, quadro etc, selecione o título de apêndice e identifique com o elemento [sectitle]. Em seguida utilize os botões flutuantes (tabwrap, figgrp, *list, etc) do programa Markup para identificação do objeto que será marcado.

**botões flutuantes**

.. image:: img/doc-mkp-tags-flutuantes.jpg
   :height: 100px
   :align: center

Exemplo, selecione a figura com seu respectivo label e caption e identifique com o elemento [figgrp]

.. image:: img/doc-mkp-app-fig1.jpg
   :height: 300px
   :align: center


.. image:: img/doc-mkp-app-fig2.jpg
   :height: 350px
   :width: 350px
   :align: center

.. note:: Assegure-se de que o id da figura de apêndice é único no documento.


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=ZqjFc0Hg4P8&index=34&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


Para apêndices que apresentam parágrafos, selecione o título do apêndice e identifique com o elemento [sectitle]

.. image:: img/doc-mkp-sectitle-app-paragrafo1.jpg
   :height: 300px
   :align: center


Em seguida, selecione o parágrafo e marque com a tag [p]

.. image:: img/doc-mkp-sectitle-app-paragrafo2.jpg
   :height: 300px
   :align: center


.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/watch?v=_BM7cKHcWoA&index=32&list=PLQZT93bz3H79NTc-aUFMU_UZgo4Vl2iUH" frameborder="0" allowfullscreen></iframe>


.. _agradecimentos:

Agradecimentos
==============

A informação de agradecimento fica entre o final do corpo do texto e antes de referências bibliográficas. Para marcação automática dos elementos de agradecimento selecione todo o texto, inclusive o título desse item, e identifique com o elemento [ack]. 


**selecionando [ack]**

.. image:: img/doc-mkp-ack-nofunding.jpg
   :height: 200px
   :align: center

**Resultado esperado**

.. image:: img/doc-mkp-ack-fim.jpg
   :height: 150px
   :align: center

Comumente os dados de agradecimentos apresentam informação de financiamento, com número de contrato e instituição financiadora. Para esse tipo de marcação é necessário fazer a identificação desses elementos de financiamento em agradecimentos através do elemento [funding].
Após a marcação de [ack], o próximo passo é selecionar toda a informação de instituição financiadora e número de contrato pelo elemento [funding].

.. image:: img/doc-mkp-nivel-inf-ack.jpg
   :height: 200px
   :align: center

Em seguida, selecione o primeiro conjunto de instituição e número de contrato e identifique com o elemento [award]:

.. image:: img/doc-mkp-select-1-award-ack.jpg
   :height: 200px
   :align: center

Feito a identificação de [award], selecione a instituição financiadora e identifique com o elemento [fundsrc]:

.. image:: img/doc-mkp-fundsrc1.jpg
   :height: 200px
   :align: center

.. note:: Caso haja mais que uma instituição financiadora para o mesmo número de contrato, selecione cada instituição em um [fundsrc]


Agora selecione o número de contrato e identifique com o elemento [contract]:

.. image:: img/doc-mkp-ack-contract1.jpg
   :height: 200px
   :align: center

Quando houver mais de uma instituição financiadora e número de contrato, marcar conforme segue:

.. image:: img/doc-mkp-ack-finaliz.jpg
   :height: 230px
   :align: center


.. _glossario:

Glossário
=========
A identificação de glossário é basicamente a mesma que a lista de definições, pois ao selecionar um glossário e identificar com o elemento [glossary] o próximo passo é selecionar toda a lista e marcar com o elemento :ref:`lista-definição`. No entanto a diferença é que o glossário deve ser identificado apenas "back", "app" ou "boxed-text". Segue marcação de glossário abaixo de referências, em "back":

.. image:: img/doc-mkp-glossary-.jpg
   :height: 200p
   :align: center

Selecione todos os dados de glossário e marque com o elemento :ref:`lista-definicao`:

.. image:: img/doc-mkp-select-gdef.jpg
   :height: 200px
   :align: center

Abaixo o resultado da marcação de glossário:

.. image:: img/doc-mkp-glossary.jpg
   :height: 200px
   :align: center


.. _xmlbody:

xmlbody
=======


Tendo formatado o corpo do texto de acordo com o ítem `Formatação do Arquivo <pt_how_to_generate_xml-prepara.html#formatacao-do-arquivo>`_ e após a identificação das referências bibliográficas, é possível fazer a marcação do [xmlbody].

Primeiramente, selecione todo o corpo do texto e clique no botão [xmlbody], confira as informações de seções, subseções, citações etc as quais são apresentadas na caixa de diálogo e, se necessário, corrija em seguida e clique em “Aplicar”.

.. image:: img/doc-mkp-select-xmlbody.jpg
   :height: 300px
   :align: center


.. image:: img/doc-mkp-xmlbody-select.jpg
   :height: 350px
   :width: 350px
   :align: center

.. note:: Caso haja alguma informação incorreta, selecione o item a ser corrigido na janela, clique no menu dropdown ao lado do 
          botão “Modificar”, selecione a opção correta e clique em “Modificar”. Confira novamente e clique em “Aplicar”.


Ao clicar em "Aplicar" o programa abrirá uma janela perguntando se as referências no corpo do texto obedecem o padrão author-data. Se o documento apresenta esse padrão clique em [sim], caso contrário, clique em [não].


.. image:: img/doc-mkp-refs-padrao.jpg
   :height: 300px
   :align: center

**Sistema author-data**

.. image:: img/doc-mkp-ref-author.jpg
   :height: 200px
   :align: center

**Sistema numérico**

.. image:: img/doc-mkp-ref-num.jpg
   :height: 250px
   :align: center


É a partir da formatação do documento indicada no `Formatação do Arquivo <pt_how_to_generate_xml-prepara.html#formatacao-do-arquivo>`_ que o programa  identifica automaticamente seções, subseções, parágrafos, referências de autores no corpo do texto, chamadas de figuras e tabelas, equações em linha etc. Veja:

.. image:: img/doc-mkp-complete.jpg
   :height: 300px
   :width: 200px
   :align: center

O próximo passo após a marcação automática do corpo do texto é verificar se os dados foram marcados corretamente e completar a marcação dos elementos disponíveis no documento.


.. _seção:

Seções e Subseções
------------------

Após a marcação automática do [xmlbody], certifique-se de que os tipos de seções foram selecionados corretamente.

.. image:: img/doc-mkp-section-combinada.jpg
   :align: center

No entanto, caso o programa não faça a identificação automática correta de seções simples ou compostas, é necessário editar a tag e selecionar o tipo adequado. Para editar selecione a tag de seção e clique no lápis "Editar Atributos" e indique o tipo correspondente. Veja:

.. image:: img/doc-mkp-sec-compost.jpg
   :height: 250px
   :align: center


**Resultado**

.. image:: img/doc-mkp-section-combinada.jpg
   :height: 200px
   :align: center

.. note:: no menu dropdown as seções combinadas são precedidas por asterisco


.. _xref:

Referência Cruzada
------------------

Referências no sistema autor-data serão identificados automaticamente no corpo do texto somente se o sobrenome do autor e a data estiverem com a identificação correta em Referências Bibliográficas e, apenas se o sobrenome do autor estiver identificado no corpo do texto exatamente igual ao que foi marcado em Refs.
Há alguns casos que o programa Markup não irá fazer a marcação automática de [xref] do documento. Ex.:

**Citações de autor**


*Sobrenome do autor + informação "in press" ou derivados:*

.. image:: img/doc-mkp-xref-noprelo.jpg
   :height: 200px
   :align: center


*Autor corporativo:*

.. image:: img/doc-mkp-ref-cauthor.jpg
  :height: 150px
  :align: center

Para identificar o [xref] das citações que não foram marcadas, primeiramente verifique qual o id da referência bibliográfica não identificada, em seguida selecione a citação desejada e identifique com a tag flutuante [xref]. Veja:

.. image:: img/doc-mkp-xref-manual.jpg
   :height: 300px
   :align: center


Preencher apenas os campos "ref-type" e "rid". Em "ref-type" selecione o tipo de referência cruzada que será feito, nesse caso o valor deve ser "Referencia Bibliográfica", em seguida indique o id correspondente à referência bibliográfica citada. Confira e clique no botão [Continuar].

.. image:: img/doc-mkp-xref-manual-refs.jpg
   :height: 180px
   :align: center

.. note:: Não insira hiperlink na informação identificada. O importante é fazer a identificação correta do dado.


**Chamada de Quadros, Equações e Caixas de Texto:**

A identificação das referências cruzadas de quadros, equações e caixas de texto segue as mesmas etapas descritas em referências bibliográficas.


**Quadro:**

Selecionar [ref-type] do tipo figura e indicar a sequência do ID no documento para este elemento.

.. image:: img/doc-mkp-chart.jpg
   :height: 100px
   :align: center


   *Resultado*

.. image:: img/doc-mkp-xref-chart.jpg
   :align: center


**Equações:**

Selecionar [ref-type] do tipo equação e indicar a sequência do ID no documento para este elemento.


.. image:: img/doc-mkp-eq-man.jpg
   :align: center


   *Resultado*

.. image:: img/doc-mkp-xref-equation.jpg
   :height: 80px
   :align: center


**Caixa de Texto:**

Selecionar [ref-type] do tipo caixa de texto e indicar a sequência do ID no documento para este elemento.

.. image:: img/doc-mkp-box-man.jpg
   :height: 280px
   :align: center


   *Resultado*

.. image:: img/doc-mkp-xref-boxed.jpg
   :align: center


.. _paragrafo:

Parágrafos
----------

Os parágrafos são identificados automaticamente no corpo do texto ao fazer a identificação de [xmlbody], porém caso o programa não tenha identificado um parágrafo ou caso a marcação automática tenha identificado um parágrafo com o elemento incorreto, é possível fazer a marcação manual desse dado. Para isso selecione o parágrafo desejado, verifique se o parágrafo pertence a alguma seção ou subseção e encontre o elemento [p] nos níveis de [sec] ou [subsec].


.. image:: img/doc-mkp-subsec-p.jpg
   :height: 250px
   :align: center


*Resultado*

.. image:: img/doc-mkp-element-p.jpg
   :height: 100px
   :align: center


.. _figura:
Figuras
-------

Ao fazer a marcação de [xmlbody] o programa identifica automaticamente o "graphic" da imagem, entretanto o responsável pela marcação do documento deve completar a marcação dos dados como label, caption e fonte (esse último, se existir).

* Selecione a imagem envolvendo o label, caption e fonte e identifique com o elemento [figgrp].

.. image:: img/doc-mkp-select-fig.jpg
   :height: 400px
   :align: center

* O programa irá abrir uma janela com um campo para identificação do "id" da figura.

.. image:: img/doc-mkp-id-fig.jpg
   :height: 200px
   :align: center

Certifique-se de que o id de figura é único no documento.


.. image:: img/doc-mkp-fig-incomp.jpg
   :height: 400px
   :align: center

.. note:: A marcação completa de figura é de extrema  importância. Se a figura não for marcada com o elemento [figgrp] 
          e seus respectivos dados, o programa não gerará o elemento [fig] correspondente no documento.


* Após a marcação de [figgrp] caso a imagem apresente informação de fonte, selecione o dado e identique com o elemento [attrib]:

.. image:: img/doc-mkp-attrib-fig.jpg
   :height: 400px
   :align: center


.. note:: A marcação de label e caption é automática,, isso porque esses dados estão em conformidade com 
          a `Formatação do Arquivo <pt_how_to_generate_xml-prepara.html#formatacao-do-arquivo>`_, com label e caption abaixo da imagem no arquivo .doc. A informação de fonte deve estar acima 
          da imagem. Veja o exemplo da imagem acima.


.. _tabela:

Tabelas
-------

As tabelas podem ser apresentadas como imagem ou em texto para codificação dos elementos que compõem a tabela. As tabelas que estão como imagem devem apresentar o label, caption e notas (essa última, se existir) em texto, para que todos os elementos sejam identificados.
As tabelas devem estar, preferencialmente, em formato texto, usandos-se figuras para tabelas complexas (com células mescladas, símbolos, fórmulas, imagens etc).


Tabelas em Imagem
^^^^^^^^^^^^^^^^^

Ao fazer a marcação de [xmlbody] o programa identifica automaticamente o "graphic" da tabela. Selecione todos os dados da tabela (imagem, label, caption e notas de rodapé, se houver) e identifique com o elemento [tabwrap].

Mesmo estando na forma de figura, o id do elemento deverá ser o indicado para tabelas (t1, t2, t3 ...). Certifique-se de que o id de tabela é único no documento.

* Selecione toda a informação de tabela e identique com o elemento [tabwrap]

.. image:: img/doc-mkp-select-tableimg.jpg
   :height: 450px
   :width: 300px
   :align: center

* O programa irá abrir uma janela com um campo para identificação do "id" da tabela.

.. image:: img/doc-mkp-id-figimg.jpg
   :align: center

Certifique-se de que o id de figura é único no documento.

.. image:: img/doc-mkp-tabimg.jpg
   :height: 450px
   :width: 300px
   :align: center

.. note:: O programa faz a marcação automática de label, caption e notas de rodapé de tabela.


Tabelas em Texto
^^^^^^^^^^^^^^^^

O programa também codifica tabelas em texto. Para isso, selecionte toda a informação de tabela (label, caption, corpo da tabela e notas de rodapé, esse ultimo se existir) e identifique com o elemento [tabwrap].

.. image:: img/doc-mkp-select-tab-text.jpg
   :height: 350px
   :align: center


.. note:: O cabeçalho da tabela deve estar em negrito. Essa formatação é essencial para que o programa consiga fazer a identificação 
          correta de [thead] e os elementos que o compõe.

* O programa irá abrir uma janela com um campo para identificação do "id" da tabela.

.. image:: img/doc-mkp-id-tabtext.jpg
   :height: 200px
   :align: center

Certifique-se de que o id de tabela é único no documento.


.. image:: img/doc-mkp-tabcomplete.jpg
   :height: 400px
   :width: 280px
   :align: center

Veja que o programa fez a marcação automática de label, caption, notas de rodapé e ainda, a codificação da tabela.


.. note:: Tabelas irregulares, com células mescladas ou com tamanhos extensos possivelmente apresentarão problemas de marcação.
          Nesse caso alguns elementos deverão ser identificados manualmente por meio do programa Markup ou no XML quando este for gerado.


.. _equação:

Equações
--------

Há dois tipos de equações que o programa suporta: as equações em linha (em meio a um parágrafo) e as equações em parágrafo.

**Equação em linha**

As equações em linha devem ser inseridas no parágrafo como imagem. A identificação é feita automaticamente pelo programa Markup ao fazer a identificação de [xmlbody].

.. image:: img/doc-mkp-eqline.jpg
   :height: 200px
   :align: center

Se o programa Markup não fizer a marcação automática da equação em linha, é possível fazer a marcação manualmente. Para isso selecione a equação em linha e identifique com o elemento [graphic].

.. image:: img/doc-mkp=eqline-man.jpg
   :height: 250px
   :align: center

Note que o programa abre uma janela com um campo para a identificação do "href" da equação. Nesse campo insira o nome do arquivo:

.. image:: img/doc-mkp-eq-line-href.jpg
   :height: 200px
   :align: center

O resultado será:

.. image:: img/doc-mkp-eqline.jpg
   :height: 200px
   :align: center

**Equações**

As equações disponíveis como parágrafos devem ser identificadas com a tag [equation]

.. image:: img/doc-mkp-eq1.jpg
   :height: 200px
   :align: center

Será aberta uma janela com um campo para a identificação do "id" da equação. Certifique-se de que o id da equação é único no documento.

.. image:: img/doc-mkp-eq2.jpg
   :height: 200px
   :align: center

Ao fazer a marcação da equação o programa identifica o elemento [equation] e, caso haja informação de label na equação, é possível identificar esse dado com o botão [label].

.. image:: img/doc-mkp-eq3.jpg
   :height: 200px
   :align: center

.. _caixa-de-texto:

Caixa de Texto
--------------

As caixas de texto podem apresentar figuras, equações, listas, glossários ou um texto. Para identificar esse elemento selecione toda a informação de caixa de texto, inclusive o label e caption e identifique com o botão [*boxedtxt]:

.. image:: img/doc-mkp-boxselect.jpg
   :height: 300px
   :align: center

Preencha o campo de ID da caixa de texto na janela que se abrirá após a seleção de [*boxedtxt]. Certifique-se de que o id de boxed-text é unico no documento.

.. image:: img/doc-mkp-id-bxt.jpg
   :height: 200px
   :align: center

Utilizando o botão [*boxedtxt] o programa faz a marcação automática de [sectitle] da caixa de texto e também dos parágrafos:

.. image:: img/doc-mkp-resultboxed.jpg
   :height: 400px
   :align: center

Caso a caixa de texto apresente uma figura, uma tabela, listas etc, é possível também utilizar o elemento [*boxedtxt] e depois fazer a identificação desses objetos através das tags flutuantes do programa.



.. _verso:

Marcação de Versos
------------------

Para identificar versos ou poemas no corpo do texto, selecione toda a informação, inclusive título e autoria, se existir, e identifique com o elemento [versegrp]: 

.. image:: img/doc-mkp-selectverse.jpg
   :height: 150px
   :align: center

O programa identificará cada linha como [verseline]. Caso o poema apresente título, exclua a marcação de verseline, selecione o elemento e identifique com o botão [label]. A autoria do poema deve ser identificada com o elemento [attrib].

.. image:: img/doc-mkp-versee.jpg
   :height: 150px
   :align: center


.. image:: img/doc-mkp-versline-attr.jpg
   :height: 180px
   :align: center

.. _citação:

Citações Diretas
----------------

As citações são identificadas automaticamente no corpo do texto, ao fazer a marcação de [xmlbody]. Para isso, as citações devem ser alinhadas à direita com 4cm de recuo.

.. image:: img/mkp-doc-quoteok.jpg
   :height: 200px
   :align: center

Caso o programa não faça a marcação automática, selecione a citação desejada e em seguida marque com o botão [quote]:

.. image:: img/doc-mkp-quotee.jpg
   :height: 300px
   :align: center

O resultado deve ser:

.. image:: img/mkp-doc-quoteok.jpg
   :height: 200px
   :align: center

.. _lista:

Listas
------

Para identificar listas selecione todos os itens e identifique com o elemento [*list]. O programa abrirá uma janela, onde deve-se selecionar o tipo de lista:

.. image:: img/doc-mkp-list-type.jpg
   :height: 400px
   :width: 380px
   :align: center

Verifique os tipos possíveis de lista em :ref:`elemento-list` e selecione o tipo mais adequado:

.. image:: img/doc-mkp-list.jpg
   :height: 250px
   :align: center

.. note:: O programa Markup não faz a marcação de sublistas. Portanto, para verificar como identificar sublistas, 
         consulte a documentação "Markup_90_O_que_ha_novo.pdf" item "Processos Manuais".


.. _elemento-list:

O atributo ``@list-type`` especifica o prefixo a ser utilizado no marcador da 
lista. Os valores possíveis são:

+----------------+-------------------------------------------------------------------+
| Valor          | Descrição                                                         |
+================+===================================================================+
| order          | Lista ordenada, cujo prefixo utilizado é um número ou letra       |
|                | dependendo do estilo.                                             |
+----------------+-------------------------------------------------------------------+
| bullet         | Lista desordenada, cujo prefixo utilizado é um ponto, barra ou    |
|                | outro símbolo.                                                    |
+----------------+-------------------------------------------------------------------+
| alpha-lower    | Lista ordenada, cujo prefixo é um caractere alfabético minúsculo. |
+----------------+-------------------------------------------------------------------+
| alpha-upper    | Lista ordenada, cujo prefixo é um caractere alfabético maiúsculo. |
+----------------+-------------------------------------------------------------------+
| roman-lower    | Lista ordenada, cujo prefixo é um numeral romano minúsculo.       |
+----------------+-------------------------------------------------------------------+
| roman-upper    | Lista ordenada, cujo prefixo é um numeral romano maiúsculo.       |
+----------------+-------------------------------------------------------------------+
| simple         | Lista simples, sem prefixo nos itens.                             |
+----------------+-------------------------------------------------------------------+


.. _lista-definicao:

Lista de Definição
------------------

Para identificar listas de definições selecione todos os dados, inclusive o título se existir, e marque com o elemento [*deflist]

.. image:: img/doc-mkp-deflistselect.jpg
   :height: 300px
   :align: center

Na janela que será aberta pelo programa, preencha o campo de identificação de id da lista. Certifique-se de que o id é único no documento.

.. image:: img/doc-mkp-def-selec.jpg
   :height: 200px
   :align: center


Após isso, confirme o título da lista de definição e em seguida a marcação do título:

.. image:: img/doc-mkp-question-def.jpg
   :height: 150px
   :align: center


.. image:: img/doc-mkp-def-sectitle.jpg
   :height: 150px
   :align: center


Ao finalizar, verifique se a marcação automática de cada termo e definição da lista de definição estão de acordo com o modelo abaixo.

.. image:: img/doc-mkp-deflist.jpg
   :height: 300px
   :align: center

.. note:: O programa faz a marcação automática de cada item da lista de definições apenas se a lista estiver com 
          a formatação requerida pelo SciELO: com o termo em negrito, hífen como separador e a definição do termo sem formatação.

Caso o programa não faça a marcação automática da lista de definições, é possível identificar os elementos manualmente. Veja:

* Selecione toda a lista de denifições e identifique com o elemento [deflist], sem asterisco:

.. image:: img/doc-mkp-mandef1.jpg
   :height: 300px
   :align: center


* Identifique o título com o elemento [sectitle] (apenas se houver informação de título):

.. image:: img/doc-mkp-defsect.jpg
   :height: 250px
   :align: center

* Selecione o termo e a definição e identifique com o botão [defitem]:

.. image:: img/doc-mkp-defitem.jpg
   :height: 250px
   :align: center

* Selecione apenas o termo e marque com o botão [term]:

.. image:: img/doc-mkp-term.jpg
   :height: 80px
   :align: center

* O próximo passo é selecionar a definição e identificar com o botão [def]:

.. image:: img/mkp-doc-def.jpg
   :height: 200px
   :align: center


Faça o mesmo para os demais termos e definições.


.. _material-suplementar:

Material Suplementar
--------------------

A identificação de materiais suplementares deve ser feita pela tag [supplmat]. A indicação de Material suplementar pode estar em linha, como um parágrafo "solto" no documento ou como apêndice.


.. _suplemento-em-paragrafo:

Objeto Suplementar em [xmlbody]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Selecione toda a informação de material suplementar, incluindo label e caption - se existir - e identifique com o elemento [supplmat]:

.. image:: img/doc-mkp-suppl-f.jpg
   :height: 300px
   :align: center


Na janela aberta pelo programa,  preencha o campo de "id", o qual deverá ser único no documento, e o campo "href" com o nome do arquivo .doc:


.. image:: img/doc-mkp-supplfig.jpg
   :height: 200px
   :align: center

Na sequência, faça a identificação do label do material suplementar e em seguida selecione toda a informação de figura e marque com o botão [figgrp]. A marcação deverá ser conforme segue o exemplo abaixo:

.. image:: img/doc-mkp-suppl2.jpg
   :height: 300px
   :align: center


.. _suplemento-em-linha:

Material Suplementar em Linha
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Selecione a informação de material suplementar e identifique com o elemento [supplmat]:

.. image:: img/doc-mkp-selectms.jpg
   :height: 180px
   :align: center

Na janela aberta pelo programa,  preencha o campo de "id", o qual deverá ser único no documento, e o campo "href" com o nome do pdf suplementar exatamente como consta na pasta "src". Veja:

.. image:: img/doc-mkp-camposms.jpg
   :height: 200px
   :align: center


A marcação deverá ser conforme segue abaixo:

.. image:: img/doc-nkp-supple.jpg
   :align: center

.. note:: Antes de iniciar a marcação de material suplementar certifique-se de que o PDF suplementar foi incluído na 
          pasta "src" comentado em `Estrutura de Pastas <pt_how_to_generate_xml-prepara.html#estrutura-de-pastas>`_.


.. _suplemento-em-apendice:

Material Suplementar em Apêndice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nesse caso, marca-se, primeiramente, o objeto com o elemento [appgrp] e em seguida com os elementos de [app]. 

.. image:: img/doc-mkp-suppl-appo.jpg
  :height: 400px
  :width: 350px
  :align: center

Selecione novamente toda a informação desse material suplementar e identifique com o elemento [app]. Em seguida, marque o label do material com a tag [sectitle]:

.. image:: img/doc-mkp-suppl-app.jpg
   :height: 400px
   :width: 350px
   :align: center


Selecione o material suplementar e identifique com a tag [supplmat]:

.. image:: img/doc-mkp-app-suuol.jpg
   :height: 400px
   :width: 350px
   :align: center
   

Após a marcação de [supplmat] identifique o objeto do material com as tags flutuantes:

.. image:: img/doc-mkp-suppl4.jpg
   :height: 400px
   :width: 350px
   :align: center

