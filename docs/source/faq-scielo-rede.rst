.. _faq-scielo-rede:

Perguntas Frequentes SciELO Rede
================================

Processo de Adoção da publicação em XML
---------------------------------------

.. _eventos:

1. Onde encontro as apresentações das reuniões sobre a produção de XML e  o “Processo de Adoção do novo Sistema de Marcação de texto completo”?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As apresentações de todas as reuniões realizadas desde 2012, sobre o “Processo de Adoção do novo Sistema de Marcação de texto completo do SciELO” estão disponíveis no site SciELO Eventos:
 <http://eventos.scielo.org/>


.. _parceiros:

2. Existem empresas que prestam serviços de produção de XML conforme o padrão requisitado por SciELO? Como posso localizar essas empresas?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sim. Existem algumas empresas parceiras que são certificadas pelo SciELO e que prestam serviços de produção de arquivos XML segundo o SciELO Publishing Schema. Disponibilizamos o contato dessas empresas em:
<http://www.scielo.org/php/level.php?lang=pt&component=56&item=58>


.. _xml:

3. Como podemos ter mais informações sobre o XML?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nas reuniões realizadas com editores de periódicos SciELO foram realizadas apresentações e fornecidos esclarecimentos sobre as principais características  do  XML (eXtensible Markup Language). As apresentações estão disponíveis em: 

<http://eventos.scielo.org/>

Além das apresentações em reuniões, foi publicado um post  no blog SciELO em Perspectiva esclarecendo as principais razões da adoção dessa linguagem de marcação. Consulte em:

<http://blog.scielo.org/blog/2014/04/04/xml-porque/#.U1j4tT95iig>
 

.. _especificacao-scielo:

4. Quais as características do XML a ser enviado ao  SciELO?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O arquivo XML que o SciELO necessita deve estar em conformidade com o SciELO Publishing Schema (SciELO PS).
Para um maior entendimento sobre o SciELO PS, consulte  a documentação detalhada disponível em:

<http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.3-branch/index.html>


.. _indesign:

5. Existe a possibilidade de gerar o arquivo XML SciELO PS a partir do InDesign?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ainda não temos mecanismos eficaz para produzir arquivos XML com a estrutura requerida a partir do InDesign. No momento a SciELO disponibiliza um programa de marcação que possibilita identificar todas as informações de um arquivo em .doc e/ou em .html. Verificar em: 

<http://docs.scielo.org/projects/scielo-pc-programs/en/latest/>


.. _formato-diagramacao:

6. Com esse novo processo de produção da revista em XML, a diagramação do periódico impresso sofrerá alterações?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A diagramação do impresso poderá continuar da mesma forma como é realizada atualmente.


.. _programa-markup:

7. O SciELO oferece algum software que auxilie os editores a produzir os artigos em XML?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O SciELO desenvolveu algumas ferramentas para validação do XML segundo SciELO Publishing Schema. Caso o editor não possua nenhuma ferramenta para a geração de XML, poderá usar os programas de marcação e produção do XML, bem como, ferramentas de validação utilizadas no processo de produção e publicação segundo SciELO PS (ver item :ref:`ferramentas`). 
O programa de Marcação, desenvolvido por SciELO, funciona apenas em Windows, ou seja, não há a possibilidade de utilizar o programa com diferentes sistemas operacionais como Linux, por exemplo. 
Ele é um pug-in do word, o qual encontra-se disponível em:

<http://docs.scielo.org/projects/scielo-pc-programs/en/latest/download.html>

Mais informação sobre os programas e ferramentas utilizadas podem ser encontradas em:

<http://docs.scielo.org/projects/scielo-pc-programs/en/latest/>


.. _doc-markup:

8 . Há algum manual de instruções para a utilização desse programa?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sim, verifique a documentação online de instrução de uso do programa Markup disponibilizada em:

<http://docs.scielo.org/projects/scielo-pc-programs/en/latest/pt_how_to_generate_xml.html>


.. _ferramentas:

9 . Existe algum programa onde eu possa verificar se meu arquivo XML está compatível com o solicitado pelo SciELO?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sim. O SciELO desenvolveu uma ferramenta que ajuda na validação do arquivo .xml. Veja abaixo:

Package Maker: este programa está disponível no FTP SciELO produtos (xpm-4.0.090.EXE). Para instalar o programa consultar o link [1]. Este programa apresenta um relatório de erros informando possíveis problemas no XML, renomeia arquivos de acordo com o padrão SciELO PS e separa em pacotes.
Verifique no link [2] o manual de uso do validador.


[1] <http://docs.scielo.org/projects/scielo-pc-programs/en/latest/installation.html#installation>

[2] <http://docs.scielo.org/projects/scielo-pc-programs/en/latest/xml_package_maker.html>



.. _exemplos:

10 . SciELO disponibiliza modelos de arquivos XML compatívies com as especificações de SciELO PS?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sim. Para receber modelos de arquivos em XML é necessário enviar e-mail para scielo@scielo.org solicitando o envio desses documentos.


.. _manual-scielops:

11 . Como verifico quais são as possíveis tags no arquivo XML-SciELO?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O guia de uso dos elementos e atributos do SciELO Publishing Schema descreve o estilo de marcação adotado pelo projeto SciELO para a submissão de documentos no formato XML. Essa documentação é composta pela DTD JATS 1.0 + especificações PMC + Estilo SciELO, que são regras que especializam aspectos da especificação. Verificar em:

<http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.2-branch/tagset.html>



.. _site-xml:

12 . Posso usar os arquivos XML na página da minha revista?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sim. O editor pode disponibilizar o arquivo xml não só na página SciELO, mas também em seu próprio site. Verificar procedimento disponível em:

<http://docs.scielo.org/projects/scielo-pc-programs/en/latest/workflow_publishing.html>