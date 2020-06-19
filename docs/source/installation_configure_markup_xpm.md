Última atualização Jun, 2020


# Como instalar Markup

1. Executar o instalador
2. Completar:

   - **Application's folder:** complete com o nome da aplicação que aparecerá no Menu de Programas
   - **URL:** endereço do site público da coleção
   - **Programs's destination folder:** localização da pasta dos programas (**bin**). Ex.: c:\scielo
   - **Data destination folder:** localização da pasta dos dados (**serial**). Inserir o **mesmo** valor do campo anterior

    ![Formulário de Instalação](./img/installation_setup.png)


3. Selecionar:

   - **Markup:** programa para identificar elementos de um artigo/texto
   - **Markup - Automata files** (opcionalmente): exemplos de arquivos para marcação automática de referências bibliográficas


    ![Seleção de programas](./img/howtoinstall_programs.png)


# XML Package Maker e XML Markup

Por padrão o programa funciona considerando acesso à Internet disponível, ausência de proxy para acesso à internet e uso do packtools como validador de estrutura de XML (em substituição ao style-checker).

Para os casos em que o acesso à Internet é feito via proxy ou não há acesso à internet é necessário editar o arquivo scielo_env.ini disponível em `<caminho da aplicação>/bin/` com os seguintes parâmetros:

    PROXY_ADDRESS=(endereço do proxy)
    ENABLED_WEB_ACCESS=off (caso não haja acesso à internet)


Exemplo dos parâmetros preenchidos:

    PROXY_ADDRESS=123.456.789:1234
    ENABLED_WEB_ACCESS=off

