Última atualização Jun, 2020


# Configurações de Title Manager

Configurar a variável de ambiente: Painel de controle -> Segurança e Manutenção -> Sistema -> Configurações avançadas do Sistema -> Variáveis de ambiente.

Verifique se a variável já existe. 
Em caso negativo, clique em Novo e adicione o valor.


    [Variável BAP]: img/installation_setup_bap.png "Variável BAP"


# Configurações de XML Converter

# Caminho do site local

Para que XML Converter copie os arquivos pdf, img, xml para o site local, editar o arquivo correspondente a **c:\\scielo\\bin\\scielo_paths.ini**, na linha:

  SCI_LISTA_SITE=c:\home\scielo\www\proc\scilista.lst


Trocar **c:\\home\\scielo\\www** pela localização do site local. Por exemplo:

  SCI_LISTA_SITE=c:\var\www\scielo\proc\scilista.lst


# Validação de tabelas e fórmulas

Para SciELO Brasil, o padrão de exigência para tabelas e fórmulas é que elas sejam codificadas.

Para alterar o nível de exigência, editar/criar o arquivo correspondente a **c:\\scielo\\bin\\scielo_collection.ini**:

  CODED_FORMULA_REQUIRED=off
  CODED_TABLE_REQUIRED=off


**off** é para desligar


# Validação em relação aos critérios da coleção

Para SciELO Brasil, algumas validações bloqueiam a entrada de documentos no sistema (XML Converter).

Para alterar o nível de exigência, editar/criar o arquivo correspondente a **c:\\scielo\\bin\\scielo_collection.ini**:

  BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA=off


**off** é para desligar

