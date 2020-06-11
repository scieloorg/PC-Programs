Última atualização Jun, 2020


# XML Package Maker

Por padrão o programa funciona considerando acesso à Internet disponível, ausência de proxy para acesso à internet e uso do packtools como validador de estrutura de XML (em substituição ao style-checker).

Para os casos em que o acesso à Internet é feito via proxy ou não há acesso à internet é necessário editar o arquivo scielo_env.ini disponível em `<caminho da aplicação>/bin/` com os seguintes parâmetros:

    PROXY_ADDRESS=(endereço do proxy)
    ENABLED_WEB_ACCESS=off (caso não haja acesso à internet)


Exemplo dos parâmetros preenchidos:

    PROXY_ADDRESS=123.456.789:1234
    ENABLED_WEB_ACCESS=off

