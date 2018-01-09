.. how_to_install:

=============
Como instalar
=============

XML Package Maker
=================

1. Instalar e/ou verificar os `pré-requisitos <pt_installation_requirements.html>`_
2. Fazer o `download <pt_installation_download.html>`_ dos instaladores
3. Executar o instalador
4. Indicar a localização da aplicação


    .. image:: img/howtoinstall_xpm.png


5. Abrir um terminal (cmd) e executar os seguintes comandos:

Executar o comando abaixo para entrar na pasta onde está o programa **install_requirements.bat**:

    .. code-block:: code

      cd <LOCAL DE INSTALACAO XPM>\xml

Exemplo:

    .. image:: img/installation_configure_xpm_01.png

Resultado esperado:

    .. image:: img/installation_configure_xpm_02.png


Executar o comando abaixo para instalar os pré-requisitos **install_requirements.bat**:

    .. code-block:: code

      install_requirements.bat

Exemplo:

    .. image:: img/installation_configure_xpm_03.png

Resultado esperado:

    .. image:: img/installation_configure_xpm_04.png
    .. image:: img/installation_configure_xpm_05.png
    .. image:: img/installation_configure_xpm_06.png


Markup
======

1. Instalar e/ou verificar os `pré-requisitos <pt_installation_requirements.html>`_
2. Fazer o `download <pt_installation_download.html>`_ dos instaladores
3. Executar o instalador
4. Configurar:

   - **Application's folder:** complete com o nome da aplicação que aparecerá no Menu de Programas
   - **URL:** endereço do site público da coleção
   - **Programs's destination folder:** localização da pasta dos programas (**bin**)
   - **Data destination folder:** localização da pasta dos dados (**serial**). Repetir o mesmo valor do anterior.

    .. image:: img/installation_setup.jpg


5. Selecionar:

   - **Markup**: programa para identificar elementos de um artigo/texto
   - **Markup - Automata files** (opcionalmente): examplos de arquivos para marcação automática de referências bibliográficas


    .. image:: img/howtoinstall_programs.png


6. Abrir um terminal (cmd) e executar os seguintes comandos:

    Executar o comando abaixo para entrar na pasta onde está o programa **install_requirements.bat**:

        .. code-block:: code

           cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    Exemplo:

        .. image:: img/installation_requirements_mkp_01.png

    Resultado esperado:

        .. image:: img/installation_requirements_mkp_02.png


    Executar o comando abaixo para instalar os pré-requisitos **install_requirements.bat**:

        .. code-block:: code

          install_requirements.bat

    Exemplo:

        .. image:: img/installation_requirements_mkp_03.png

    
    Este comando executará várias linhas, mas o resultado principal esperado é:

        .. image:: img/installation_requirements_mkp_04.png


SciELO PC Programs Completo: Title Manager, Converter, Markup, XPM etc
======================================================================

1. Instalar e/ou verificar os `pré-requisitos <pt_installation_requirements.html>`_
2. Fazer o `download <pt_installation_download.html>`_ dos instaladores
3. Executar o instalador

4. Configurar:

   - **Application's folder:** complete com o nome da aplicação que aparecerá no Menu de Programas
   - **URL:** endereço do site público da coleção
   - **Programs's destination folder:** localização da pasta dos programas (**bin**)
   - **Data destination folder:** localização da pasta dos dados (**serial**). 


    .. image:: img/installation_setup.jpg


5. Selecionar os programas:

  - Title Manager: programa para gestão da coleção de periódicos
  - Converter: programa de conversão de documentos marcados para a base de dados
  - XML SciELO: (opcional) programa para criar formato XML para a base de dados PubMed


    .. image:: img/howtoinstall_programs.png

6. Abrir um terminal (cmd) e executar os seguintes comandos:

    Executar o comando abaixo para entrar na pasta onde está o programa **install_requirements.bat**:

        .. code-block:: code

          cd <LOCAL DE INSTALACAO SciELO Markup>\xml

    Exemplo:

        .. image:: img/installation_requirements_mkp_01.png

    Resultado esperado:

        .. image:: img/installation_requirements_mkp_02.png


    Executar o comando abaixo para instalar os pré-requisitos **install_requirements.bat**:

        .. code-block:: code

          install_requirements.bat

    Exemplo:

        .. image:: img/installation_requirements_mkp_03.png

    
    Este comando executará várias linhas, mas o resultado principal esperado é:

        .. image:: img/installation_requirements_mkp_04.png

===============
Como configurar
===============

XML Package Maker e XML Markup
==============================

Por padrão o programa funciona considerando acesso à Internet disponível, ausência de proxy para acesso à internet e uso do packtools como validador de estrutura de XML (em substituição ao style-checker).

Para os casos em que o acesso à Internet é feito via proxy ou não há acesso à internet é necessário editar o arquivo scielo_env.ini disponível em ?/bin/ com os seguintes parâmetros:

  .. code:: text

    PROXY_ADDRESS=(endereço do proxy)
    ENABLED_WEB_ACCESS=off (caso não haja acesso à internet)
    XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER=packtools|java (nesse caso a validação será feita preferencialmente usando a ferramenta packtools substituindo à validação no style checker, na ordem inversa usa-se o Java).


Exemplo dos parâmetros preenchidos:

  .. code:: text

    PROXY_ADDRESS=123.456.789:1234
    ENABLED_WEB_ACCESS=off
    XML_STRUCTURE_VALIDATOR_PREFERENCE_ORDER=java|packtools


Title Manager e Converter
=========================

Configurar a variável de ambiente: Painel de controle -> Segurança e Manutenção -> Sistema -> Configurações avançadas do Sistema -> Variáveis de ambiente.

  Verifique se a variável já existe. 
  Em caso negativo, clique em Novo e adicione o valor.

    .. image:: img/installation_setup_bap.jpg


XML Converter
=============

PDF, XML e imagens para o site local
------------------------------------

Para que XML Converter copie os arquivos pdf, img, xml para o site local, editar o arquivo correspondente a **c:\\scielo\\bin\\scielo_paths.ini**, na linha:

.. code::

  SCI_LISTA_SITE=c:\home\scielo\www\proc\scilista.lst

Trocar **c:\\home\\scielo\\www** pela localização do site local. Por exemplo:

.. code::

  SCI_LISTA_SITE=c:\var\www\scielo\proc\scilista.lst


Validação de tabelas e fórmulas
-------------------------------

Para SciELO Brasil, o padrão de exigência para tabelas e fórmulas é que elas sejam codificadas.

Para alterar este nível, editar o arquivo que correspond a **c:\\scielo\\bin\\scielo_collection.ini**:

.. code::

  CODED_FORMULA_REQUIRED=off
  CODED_TABLE_REQUIRED=off


**off** é para que o XML Converter não exija os elementos codificados


Menu de aplicação
=================

Em alguns casos, o menú da aplicação será criado apenas com o usuário de administrador. 

.. code::

  C:\\Documents and Settings\\Administrador\\Menu Iniciar\\Programas

Neste caso, copie a pasta SciELO para a pasta Usuários para que todos os usuários tenham o menú disponível. 

.. code::

  C:\\Documents and Settings\\All Users\\Menu Iniciar\\Programas

