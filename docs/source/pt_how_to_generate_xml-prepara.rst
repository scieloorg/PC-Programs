
.. _doc-mkp:

Documentação de uso Markup
==========================

Manual de marcação de arquivos para geração de XML de acordo com SciELO Publishing Schema (SciELO PS). 


.. _introdução:

Introdução
==========

Este manual tem como objetivo auxiliar no processo de marcação de arquivos para geração de XML de acordo com SciELO PS.
Para padrões de nomeação de arquivos consultar Regra de Nomeação de Arquivos em <http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.2-branch/narr/regra-nomeacao.html>



.. _requisitos-markup:

 Requisitos para iniciar a Marcação
 ===================================
 
 Antes de iniciar o processo de marcação, é necessário seguir alguns passos para preparação do arquivo que será marcado.
 Veja abaixo os requisitos para a marcação do documento.
 
 * Os arquivos devem estar em formato Word (.doc) ou (.docx).
 * A estrutura de pastas deve seguir o padrão SciELO
 * Os arquivos devem ser formatados de acordo com a Formatação SciELO.
 

.. note:: A nomeação dos arquivos que serão trabalhados não deve conter espaços, acentos ou
         caracteres especiais. Caso seja necessário separar uma informação de outra use underline. 
         Apenas dessa forma as imagens marcadas no corpo do texto serão renomeadas e geradas corretamente. 
         Exemplo: ACB_2345.doc


.. _estrutura-de-pastas:

Estrutura de pastas
===================

Antes de iniciar a marcação, é necessário garantir que a estrutura de pastas
esteja como segue:


.. image:: img/doc-mkp-estrutura.jpg
   :height: 200px
   :align: center



Veja que dentro da pasta "markup_xml" foi inserido 2 pastas, no mesmo nível:

 * src: A pasta src (source) é utilizada para inserir os arquivos .pdf, vídeos e suplementos.
 * scielo_markup: Nessa pasta deve ser inserido os arquivos .doc ou .docx.


..  note:: Caso o responsável pela marcação não siga a recomendação de estrutura apresentada acima, não será 
           possível iniciar a marcação do documento e gerar o arquivo .xml.


.. _formato-scielo:

Formatação SciELO
------------------

Para otimizar o processo de marcação dos elementos básicos do arquivo, é necessário seguir o padrão de formatação SciELO disponível abaixo:

**Instruções para formatação de dados básicos do artigo:**

 * Linha 1: inserir número de DOI (somente se presente), caso não exista deixar linha em branco;
 * Linha 2: inserir a seção do sumário (Se ausente, deixar linha em branco);
 * Linha 3: Título do artigo;
 * Linhas seguintes: Títulos traduzidos do arquivo;
 * Para separar autores de título, pular 1 linha;
 * Cada autor deve estar em uma linha e usar "sup" para label;
 * Pular 1 linha para separar autores de afiliações;
 * Cada afiliação deve estar em uma linha;
 * Pular 1 linha para separar afiliação de resumos;
 * Resumos estruturados: negrito no nome da seção;
 * Palavras-chave: os separadores devem ser ou ponto-e-vírgula ou vírgula;
 * Seções: negrito, Times New Roman, 16, centralizadas;
 * Subseções: negrito, Times New Roman, 14, centralizadas;
 * Subseção de subseção: negrito Times New Roman, 13, centralizadas;
 * Texto: formatação livre;
 * Para tabelas, label e caption na linha antes da imagem, mas os demais, após a imagem;
 * Separador de label e caption: dois-pontos e espaço ou espaço + hífen + espaço ou ponto + espaço;
 * Para tabelas codificadas, o cabeçalho deve estar em negrito;
 * A citação de autor/data no corpo do texto deve ser: sobrenome do autor, ano;
 * Para citação no sistema numérico no corpo do texto: "sup" e entre parênteses;
 * Notas de rodapé no corpo do texto podem estar em "sup", mas não estarão entre parênteses;
 * Citações (quote), recuo de 4 cm da margem esquerda;


Exemplo:

.. image:: img/doc-mkp-2mostra.jpg
   :height: 400px
   :width: 200px
   :align: center



.. note:: As imagens dos arquivos devem estar disponíveis no arquivo .doc e marcado com o elemento indicado.



.. _atribuição-id:

Sugestão de Atribuição de “ID”
-----------------------------

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



.. _elementos-markup:

Marcação dos elementos básicos do documento
===========================================


Após formatar os dados básicos do arquivo, o próximo passo é dar início a marcação XML. 
Primeiramente, abra o arquivo .doc no Word e selecione a tag [doc]:

.. image:: img/doc-mkp-formulario.jpg
   :height: 400px
   :align: center


Perceba que ao clicar em [doc] o programa irá abrir uma caixa de diálogo onde deverá ser inserido os metadados do arquivo:

Insira o nome da revista no campo jtitle* que o programa irá inserir as informações da revista automaticamente. 
Feito isso, o próximo passo é completar as informações nos demais campos. Veja abaixo os campos que devem ser preenchidos:


+-------------------+---------------------------------------------------------------------------------------+
| Campo             | Descrição                                                                             |
+===================+=======================================================================================+
| license           | se não for inserido automaticamente, preencher com a URL da licença creative commons  |
|                   | adotada pelo periódico                                                                |
+-------------------+---------------------------------------------------------------------------------------+
| volid             | Inserir volume, se existir                                                            |
+-------------------+---------------------------------------------------------------------------------------+
| supplvol          | Caso seja um suplemento de volume incluir sua parte ou número correspondente.         |
|                   | **Exemplo: vol.12 supl.A**, então preencha com **A**, neste campo                     |
+-------------------+---------------------------------------------------------------------------------------+
| issueno           | Entre com o número do fascículo. Caso seja um artigo publicado em ahead of            |
|                   | print, insira ahead neste campo                                                       |
+-------------------+---------------------------------------------------------------------------------------+
| supplno           | Caso seja um suplemento de fascículo incluir sua parte ou número                      |
|                   | correspondente. **Exemplo: n.37, supl.A**, então preencha com **A** neste campo       |
+-------------------+---------------------------------------------------------------------------------------+
| isidpart          | Usar em casos de press release, incluindo a sigla pr                                  |
+-------------------+---------------------------------------------------------------------------------------+
| dateiso           | Data de publicação formada por ano, mês e dia **(YYYYMMDD)**. Preencher sempre        |
|                   | com o último mês da periodicidade. Por exemplo, se o periódico é bimestral            |
|                   | preencher **20140600**. Use **00** para mês e dia nos casos em não haja sua           |
|                   | identificação. **Exemplo: 20140000**.                                                 |
+-------------------+---------------------------------------------------------------------------------------+
| month/season      | Entre o mês ou mês inicial barra final, em inglês (três letras) e ponto,              |
|                   | exceto para May, June e July. **Ex.: May/June, July/Aug.**                            |
+-------------------+---------------------------------------------------------------------------------------+
| fpage             | Primeira página do documento                                                          |
+-------------------+---------------------------------------------------------------------------------------+
| @seq              | Para artigos que iniciam na mesma página de um artigo anterior, incluir a             |
|                   | sequência com letra                                                                   |
+-------------------+---------------------------------------------------------------------------------------+
| lpage             | Inserir a última página do documento                                                  |
+-------------------+---------------------------------------------------------------------------------------+
| elocatid          | Elocatid                                                                              |
+-------------------+---------------------------------------------------------------------------------------+
| order (in TOC)    | Incluir a ordem do artigo no sumário do fascículo. Deve ter, no mínimo, dois          |
|                   | dígitos. Por exemplo, se o artigo for o primeiro do sumário, preencha este            |
|                   | campo com **01** e assim por diante.                                                  |
+-------------------+---------------------------------------------------------------------------------------+
| pagcount*         | Inserir o total de paginação                                                          |
+-------------------+---------------------------------------------------------------------------------------+
| doctopic*         | Informar o tipo de documento a ser marcado. Por exemplo: artigo original, resenha,    | 
|                   | carta, comentário, etc                                                                |
+-------------------+---------------------------------------------------------------------------------------+
| language*         | Informe o idioma principal do texto a ser marcado                                     |
+-------------------+---------------------------------------------------------------------------------------+
| version*          | Identifica a versão da DTD usada no processo de marcação (A versão atual é 4.0)       |
+-------------------+---------------------------------------------------------------------------------------+
| artdate (rolling) | Obrigatório completar com a data **YYYYMMDD** quando for um artigo rolling pass.      |
|                   | Rolling pass é um modelo publicação onde o periódico publica seus artigos num volume  |
|                   | único a medida em que estes ficam prontos                                             |
+-------------------+---------------------------------------------------------------------------------------+
| ahpdate           | Indicar a data de publicação de um artigo publicado em ahead of print                 |
+-------------------+---------------------------------------------------------------------------------------+


.. note:: Os campos que apresentam um asterisco ao lado, são campos obrigatórios.
