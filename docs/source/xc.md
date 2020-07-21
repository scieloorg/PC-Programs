Última atualização Jun, 2020


# XML Converter

_XML Converter_, ou simplesmente _XC_, é uma das ferramentas que fazem parte do _SciELO PC Programs_, e é para **usuários gestores de coleção SciELO**.

Sua principal função é fornecer dados para a geração do sítio web clássico:
- geração de bases de dados _ISIS_ nas pastas que seguem o padrão: `serial/<acron>/<volnum>/base/<volnum>` usadas pelo _GeraPadrao_
- organização dos arquivos do pacote nas pastas `xml`, `pdf`, `img/revistas` do sítio web de _Controle de Qualidade_.

_XML Converter_ executa as mesmas validações feitas pelo _XML Package Maker_, mas também valida os dados dos pacotes contra os dados registrados nas bases _title_ e _issue_. Somente se os pacotes forem válidos, sua base de dados correspondente será criada.

A partir da versão 4.0.097, pode-se configurar a disponibilização dos pacotes para a nova plataforma de publicação _SciELO Publishing Framework_ (com a condição de que a coleção esteja em operação com a nova plataforma).


# XML Converter for server

Na versão _XML Converter for server_, pode-se configurar opcionalmente para:

 - baixar, de um outro servidor via _FTP_, os pacotes compactados de documentos SciELO (https://scielo.readthedocs.io/projects/scielo-publishing-schema/pt_BR/latest/).
 - acionar a execução do _GeraPadrao_ do sítio web de _Controle de Qualidade_.
 - disponibilizar (publicar) os arquivos de bases, pdf, imagens, xml etc em um servidor remoto, caso o sítio web de _Controle de Qualidade_ não rode no mesmo servidor em que é executado o _GeraPadrao_ do sítio web de controle de qualidade. 


## Pré-requisitos

 - Linux
 - CISIS
 - Python 3.x
 - SciELO Packtools


## Instalação

Criar a seguinte estrutura de pasta: 

 - `<raíz>`
   - `xml` (pasta com os programas)
   - `config` (arquivos de configuração)

Os nomes `xml` e `config` são fixos.
O diretório `<raíz>` se refere à versão do _XC_, por exemplo, `xc_2020`.

**Nota:** Uma mesma instalação (instância) pode servir para mais de uma coleção.
Não é necessário criar diferentes instâncias para cada coleção. Basta criar um arquivo de configuração para cada coleção.


Obtenha o arquivo `SciELO_Production_Tools-4.0.97-py3-none-any.whl` (local a definir).

Crie um ambiente virtual:

	python3 -m venv .venv


Ative o ambiente virtual

	source .venv/bin/activate


Execute a instalação

	pip install -U SciELO_Production_Tools-4.0.97-py3-none-any.whl


## Configuração

O arquivo de configuração deve ficar em `<raíz>/config`.
O seu nome deve ser seguir o seguinte padrão: `<collection_acron>.xc.ini`.


### Configurações obrigatórias

Indique o **caminho dos utilitários CISIS**, ou seja, a pasta cisis que contém os utilitários CISIS que são usados no _GeraPadrao_. No caso, da versão _XC server_ usar o mesmo caminho para ambas variáveis.

No Windows, normalmente há as duas versões CISIS 1030 (usado nas bases serial: title, issue e revistas) e CISIS 1660 (sítio web local). Para o Linux, não faz diferença pois somente há o sítio web.

Exemplo:

```
PATH_CISIS_1030=/bases/xml.000/proc/cisis
PATH_CISIS_1660=/bases/xml.000/proc/cisis
```

Indique respectivamente as **bases de dados _ISIS_ de _issue_ e _title_ que são enviadas continuamente** pelo utilitário _EnviaBasesXML.bat_ instalado no servidor local Windows. Estas bases serão copiadas todas as vezes que iniciar um processo do _XC_.

**Nota**: Caso já exista uma instância ou versão de _XC_ anteriormente instalada, use a mesma configuração.

Exemplo:

```
SOURCE_ISSUE_DB=/bases/xml.000/serial_proc/issue/issue
SOURCE_TITLE_DB=/bases/xml.000/serial_proc/title/title
```

Indique respectivamente as **cópias** bases de dados _ISIS_ de _issue_ e _title_ que são enviadas pelo utilitário _EnviaBasesXML.bat_ instalado no servidor local Windows. Estas bases serão criadas e indexadas todas as vezes que iniciar um processo do _XC_.

Exemplo:

```
ISSUE_DB_COPY=/bases/xml.000/collections/scl/xmldata/issue/issue
TITLE_DB_COPY=/bases/xml.000/collections/scl/xmldata/title/title
```

Indique onde está instalado a estrutura da aplicação _Web_ (sítio web da metodologia Clássica) onde corre _GeraPadrao_ para o sítio web de _Controle de Qualidade_.

**Nota**: Caso já exista uma instância ou versão de _XC_ anteriormente instalada, use a mesma configuração.

Exemplo:

```
LOCAL_WEB_APP_PATH=/bases/xml.000/collections/scl/scl.000
```

Indique onde está localizada a **estrutura da pasta _serial_** que tem duas funções principais: armazenamento das bases de dados para o _GeraPadrao_ do sítio web de _Controle de Qualidade_ e também para que a cada entrada de pacotes o _XC_ possa validar os novos pacotes com os dados anteriormente registrados.

**Nota**: Caso já exista uma instância ou versão de _XC_ anteriormente instalada, use a mesma configuração.

**IMPORTANTE:** Esta pasta tem o mesmo papel da pasta _serial_ do servidor Windows e deve-se ter _backup_.

Exemplo:

```
PROC_SERIAL_PATH=/bases/xml.000/collections/scl/scl.000/serial
```

Indique os caminhos dos diretórios usados pelo _XC_ como **área de trabalho**. 

**IMPORTANTE:** Estas pastas **devem ser exclusivas** por instalação de _XC_ e por coleção. 
**NÃO USE A MESMA CONFIGURAÇÃO** de outra instância/versão de _XC_.

Pasta para criar arquivos **temporários**

```
TEMP_PATH=
```

Pasta para as **filas** dos pacotes a serem processados pelo _XC_.

```
QUEUE_PATH=
```

Pasta para **receber** os pacotes via FTP ou mesmo manualmente. O _XC_ lê esta pasta e **move** para `QUEUE_PATH`.

```
DOWNLOAD_PATH=
```

Pasta para **arquivar** os pacotes, caso seja desejável mantê-los, caso contrário, deixar em branco. Mas pode ocupar espaço considerável.

```
ARCHIVE_PATH=
```

### Configurações para a nova plataforma _SciELO Publishing Framework_ 

Configurar **somente se** a coleção opera com a nova plataforma _SciELO Publishing Framework_ 

A variável de configuração PID_MANAGER é responsável por indicar o endereço para uma base de dados que associa versões de PIDs dos artigos SciELO. É fundamental que esta base seja persistida e mantida de forma segura.

Indique o **endereço do banco de dados `pid_manager.db`**

Exemplos:

```
PID_MANAGER=/bases/xml.000/xc/pid_manager_database.db
PID_MANAGER=sqlite:////bases/xml.000/xc/pid_manager_database.db
```
**IMPORTANTE**:
- Deve ser persistente
- Deve ser mantida mesmo que novas versões de _XC_ sejam instaladas
- Deve haver 1 base de dados por coleção.
- Deve-se ter **backup** desta base de dados.


#### Disponibilização de pacotes para o Airflow

Airflow é um componente da nova Plataforma _SciELO Publishing Framework_.

**Por FTP**

Preencher apenas o necessário para executar a transferência. Dependendo da infraestrutura, pode ser o suficiente apenas o endereço do servidor remoto e o caminho do destino.

```
KG_server=
KG_user=
KG_password=
KG_remote_path=
```

**Por cópia**

```
KG_destination_path=
```

### Configurações Desejáveis

O _XC_ no servidor se comunica com o usuário pelas mensagens na tela mas também por email.
Funciona sem esta configuração, no entanto, a comunicação fica comprometida.

**Nota**: Caso já exista uma instância ou versão de _XC_ anteriormente instalada, use a mesma configuração com exceção de: `[XC_VERSION]`

Indique se a funcionalidade de **envio de email** está ou não ativa. Valores possíveis: **on** ou **off**

Exemplo:

```
EMAIL_SERVICE_STATUS=
```

Indique os dados do **remetente** das mensagens.

```
SENDER_NAME=
SENDER_EMAIL=
```

Indique o endereço de email ou endereços separados por ';' dos **usuários do _XC_**.

```
EMAIL_TO=
```

Indique o endereço de email para receber **mensagens de exceções**.

```
EMAIL_TO_ADM=
```

Configure o **assunto** e **conteúdo** de cada tipo de mensagem.
Troque `COLLECTION_NAME` pelo nome da coleção.
Troque `XC_VERSION` pela identificação da instância (número ou ano da versão) de _XC_.
Os arquivos `*.txt` ficam em `<raíz>/xml/prodtools/settings/email/`.

**Nota:** Alterar o conteúdo destes arquivos pode impactar nas mensagens do _XC_ para outras coleções.
Para criar mensagens personalizadas, crie novos arquivos.

```
EMAIL_SUBJECT_PACKAGE_EVALUATION=[XC_VERSION] [COLLECTION_NAME] Evaluation report of  
EMAIL_TEXT_PACKAGE_EVALUATION=email.txt

EMAIL_SUBJECT_PACKAGES_RECEIPT=[XC_VERSION] [COLLECTION_NAME] Packages receipt report
EMAIL_TEXT_PACKAGES_RECEIPT=email_download.txt

EMAIL_SUBJECT_GERAPADRAO=[XC_VERSION] [COLLECTION_NAME] homolog.xml.scielo.br is updated
EMAIL_TEXT_GERAPADRAO=email_gerapadrao.txt

EMAIL_SUBJECT_INVALID_PACKAGES=[XC_VERSION] [COLLECTION_NAME] Invalid packages
EMAIL_TEXT_INVALID_PACKAGES=email_invalid_packages.txt

EMAIL_SUBJECT_CONVERSION_FAILURE=[XC_VERSION] [COLLECTION_NAME] Packages conversion failure
```

#### Recepção de pacotes por FTP

Preencher somente o _XC_ baixará os pacotes por FTP.

**IMPORTANTE:** Esta configuração **deve ser exclusiva** por instalação de _XC_ e por coleção. Caso já exista uma instância ou versão de _XC_ anteriormente instalada, pode ser usada a mesma configuração **com exceção de: `FTP_DIR`**. 

Indique os dados do **local de onde os pacotes serão baixados**.

```
FTP_SERVER=
FTP_USER=
FTP_PASSWORD=
FTP_DIR=
```

#### Execução do GeraPadrao

Caso seja desejável que o _XC_ acione a execução do _GeraPadrao_, todas as variáveis abaixo devem ser configuradas.

**Nota**: Caso já exista uma instância ou versão de _XC_ anteriormente instalada, **escolher apenas 1** delas para acionar a execução do _GeraPadrao_.

Indique onde está instalado **proc** do _GeraPadrao_.

Exemplo:

```
PROC_PATH=/bases/xml.000/collections/scl/scl.000/proc
```

Indique **o caminho do arquivo temporário scilista da coleção** que contém ítens processados com sucesso pelo _XC_. Neste arquivo ficam acumulados todos os ítens validados pelo _XC_ até que o _GeraPadrao_ o consuma.

Exemplo:

```
COL_SCILISTA=/bases/xml.000/collections/scl/xmldata/minha_scilista.txt
```

Indique **o caminho do arquivo que controla a execução do _GeraPadrao_** que contém os valores **FINISHED** ou **running**. Serve como um semáforo impedindo que mais de um processo de _GeraPadrao_ rode concorrentemente para a mesma coleção.

Exemplo:

```
GERAPADRAO_PERMISSION=/bases/xml.000/collections/scl/xmldata/gerapadrao.controle.txt
```

#### Publicação do sítio web de controle de qualidade

Preencher somente se o resultado será visualizado em um **sítio web de controle de qualidade**.

**Nota**: Caso já exista uma instância ou versão de _XC_ anteriormente instalada e o sítio web de controle de qualidade continua sendo o mesmo, pode ser usada a mesma configuração.

Exemplo:

```
WEB_APP_SITE=homolog.xml.scielo.br
```

### Configurações opcionais

#### Disponibilização de arquivos para o **sítio web de controle de qualidade** se é **remoto**

Preencher somente se o sítio web de controle de qualidade é remoto.

**Nota**: Caso já exista uma instância ou versão de _XC_ anteriormente instalada e o sítio web de controle de qualidade continua sendo o mesmo, use a mesma configuração.

Indique **a transferência** está ou não ativa. Valores possíveis: **on** ou **off**

Exemplo:

```
TRANSFERENCE_STATUS=
```

Indique os dados do **destino do sítio web de controle de qualidade**.

```
TRANSFER_USER=
TRANSFER_SERVER=
REMOTE_WEB_APP_PATH=
```

#### NÍVEL DE VALIDAÇÕES DOS PACOTES

Preencher somente se a coleção tem grau de exigência menor quanto a:
- critérios de ingresso
- fórmulas codificadas
- tabelas codificadas

```
BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA=OFF
CODED_FORMULA_REQUIRED=OFF
CODED_TABLE_REQUIRED=OFF
```

## Execução

Combinações possíveis de comandos:

Para executar a função principal do _XC_, ou seja, a geração de dados para o sítio web clássico.

`cd <raíz>/xml;xc_server <collection_acron>`


Para executar primeiro o download dos pacotes e depois a geração de dados para o sítio web clássico.

`cd <raíz>/xml;xc_server <collection_acron> --download`


Para executar primeiro o download dos pacotes, a geração de dados para o sítio web clássico e, por fim, aciona a execução do _GeraPadrao_ do sítio web de controle de qualidade.

`cd <raíz>/xml;xc_server <collection_acron> --download --gerapadrao`


Para executar a geração de dados para o sítio web clássico e, por fim, aciona a execução do _GeraPadrao_ do sítio web de controle de qualidade.

`cd <raíz>/xml;xc_server <collection_acron> --gerapadrao`


Pode-se deixar agendado a execução dos comandos conforme a necessidade.
Por exemplo, colocar com mais frequência:

`cd <raíz>/xml;xc_server <collection_acron> --download`

e menor frequência:

`cd <raíz>/xml;xc_server <collection_acron> --download --gerapadrao`


Pode-se deixar agendado a execução de _XC_ a cada 5 minutos, dentro de um período, por exemplo, de 7h às 19h.
No entanto, o horário não deve coincidir com outras instâncias/versões de _XC_ que podem rodar concorrentemente.
O motivo é que todas as instâncias de _XC_ fazem modificações na mesma pasta `serial`.

Caso exista **mais de uma** instância de _XC_ executando concorrentemente, **escolher apenas 1** delas para acionar a execução do _GeraPadrao_.

