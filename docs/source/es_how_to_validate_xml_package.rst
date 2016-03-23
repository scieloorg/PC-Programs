.. _es_como_validar_paquete_xml

Como validar el paquete XML
===========================

Use o Programa XPM para gerar o pacote XML para SciELO e PMC.


Package Maker - ¿Cómo usar?
---------------------------

Para utilizar o programa Package Maker clique no meu Iniciar do Windows, procure a pasta do Programa Markup que foi istalado em sua máquina e com o mouse verifique os itens disponíveis na pasta.
Clique no botão *XML Package Maker*


.. image:: img/scielo_menu_xpm.png

.. image:: img/xpm_gui.png


Agora clique no botão "Choose Folder" para escolher a pasta que contém os arquivos que serão validados 


.. image:: img/xpm_gui_selected_folder.png



E clique em **XML Package Maker**.


Resultados
----------

* Para arquivos XML SciELO (verifique a pasta scielo_package e/ou scielo_package_zips)
* Para arquivos XML PMC (verifique a pasta pmc_package)
* Para Relatório de arquivos (verifique a pasta errors)

A pasta que é gerada pelo XPM "ISSN-acronimo-volume-numero_xml_package_maker_result" estará disponível no mesmo nível da pasta que foi utilizada para gerar o pacote:


.. image:: img/xpm_result_folders.png



Informes
--------

Depois de validar e gerar os pacotes os relatórios serão disponibilizados automaticamente em um Web Browser.



Informes Resumidos
.................

Estatísticas de Validaciones
::::::::::::::::::::::::::::

É apresentado o total de Erros fatais (Fatal Errors), erros (Errors), e alertas (Warnings), encontrados em todo o pacote.

FATAL ERRORS
   Representa os erros relacionados aos indicadores bibliométricos.

ERRORS
   Representa outros tipos de erros.

WARNINGS
   Representa algo que precisa de mais atenção.


.. image:: img/xpm_report.png


Informe Detallado
.................

Informe Detallado - Validaciones del Paquete
::::::::::::::::::::::::::::::::::::::::::::

Primeiro de tudo O XPM valida alguns dados do pacote:

- Elementos que apresentam o mesmo valor em todos os arquivos XML, tais como:

 * journal-title
 * journal id NLM
 * journal ISSN
 * publisher name
 * issue label
 * issue pub date

-  Elementos que apresentam um valor único em cada arquivo XML, tais como:

 * doi
 * elocation-id, if applicable
 * fpage and fpage/@seq
 * order (used to generated article PID)


Exemplo de Erros Fatais (Fatal Error) por apresentar valor diferente para o elemento ``<publisher-name>`` 

 .. image:: img/xml_reports__toc_fatal_error_required_equal_publisher.jpg


Exemplo de Erros Fatais (Fatal Error) por apresentar valores diferentes em ``<pub-date>``

 .. image:: img/xml_reports_toc_fatal_error_required_equal_date.png


Exemplo de Erros Fatais (Fatal Error) pois é requerido um valor único

 .. image:: img/xml_reports_toc_fatal_error_unique.png.jpg


Informe Detallado - Validaciones del Documento
::::::::::::::::::::::::::::::::::::::::::::::

O documento é apresentado em uma Tabela.

As colunas 'order', 'aop pid', 'toc section', '@article-type' estão destacadas, pois contém dados importantes.

A coluna **reports** possui **botões** para abrir/fechar o relatório detalhado de cada documento.

Cada linha possui um dado do documento:

.. image:: img/xpm_report_detail.png


Informe Detallado - Validaciones
::::::::::::::::::::::::::::::::

Clique em **Validação de Conteúdo" para verificar os problemas apresentados.
O relatório detalhado é apresentado abaixo da linha.

.. image:: img/xpm_report_detail_validations.png


Archivos/Carpetas
.................

Apresenta os Arquivos e Pastas que foram gerados e validados.

.. image:: img/xpm_report_folder.png


Visión General de Paquete
.........................

Visión General de Paquete - idiomas
:::::::::::::::::::::::::::::::::::

Apresenta os elementos que contém o atributo de idioma ``@xml:lang``. 

.. image:: img/xpm_report_overview_lang.png


Visión General de Paquete - datos
:::::::::::::::::::::::::::::::::

Apresenta os dados encontrados no documento: publicação e histórico.
Apresenta o tempo esperado entre:  data de recebido e aceito, aceito e publicado, aceito e a data atual.

.. image:: img/xpm_report_overview_date.png


Visión General de Paquete - afiliaciones
::::::::::::::::::::::::::::::::::::::::


.. image:: img/xpm_report_overview_aff.png


Visión General de Paquete - Citas bibliograficas
::::::::::::::::::::::::::::::::::::::::::::::::


.. image:: img/xpm_report_overview_ref.png


Informes fonte
..............

.. image:: img/xpm_report_sources.png

.. image:: img/xpm_report_sources_journals.png

.. image:: img/xpm_report_sources_books.png

.. image:: img/xpm_report_sources_others.png
