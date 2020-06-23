
## Glossário


### Servidor local

É um computador Windows onde executará o SciELO Website local e as ferramentas de gestão: Title Manager e Converter.


### Coleção ou Instância SciELO

Chamamos de **Coleção ou Instância SciELO** o website, o conjunto de artigos, bases de dados etc que adotaram a metodologia SciELO de publicação. 

Exemplos: SciELO Brazil, SciELO Chile, SciELO Salud Pública, PePSIC, Rev@Enf entre outros


### Tipos de fascículos

**regular:** fascículo que se publica dentro de uma frequência esperada

**supplement:** fascículo que se publica esporadicamente

**ahead:** artigos já aprovado e publicados antes do fechamento do fascículo. Publicação Adiantada.

**publicação contínua:** fascículo em que se publica os artigos, antes do fechamento.


### Número sequencial

É um número formado por ano com 4 dígitos, seguido da posição do fascículo dentro do ano.

Tem dois propósitos:
- ordenar os fascículos dentro do ano na grade de fascículos no website
- formar o ID do fascículo

Por convenção, a **posição do fascículo** dentro do ano é:

- 50 para _ahead_


Exemplo:


    ================   =================
    Fascículo          Número sequencial
    ================   =================
    v.40 n.1           20091
    v.40 n.2           20092
    v.40 suppl.        20093
    v.40 suppl.2       20094
    v.40 n.2 suppl.1   20095
    ahead              200950
    ================   =================



### Estrutura de pastas

**SciELO PC Programs** possui principalmente as seguintes pastas:

- programas: **bin** e **xml_scielo**
- dados: **serial**

**Nota:** A pasta de dados faz mais sentido para os gestores de coleção, que armazenam os dados nesta estrutura e devem fazer cópias de segurança da pasta **serial**. 

Os programas e os dados podem ser instalados em pastas diferentes, até memso em _drivers_ diferentes.
Por padrão, tem sido instalados em:

```
- c:\scielo\bin
- c:\scielo\serial
```


Outros exemplos:

```
- g:\scielo\bin
- v:\scielo\serial
```

```
- g:\40097\scielo\bin
- v:\scielo\serial
```


### Pasta serial

Nesta pasta ficam as bases de dados:

- **title:** cada registro contém dados de um periódico
- **section:** cada registro contém todas as seções usadas por um periódico
- **issue:** cada registro contém dados de um fascículo
- **code:** cada registro contém uma tabela de pares: chaves/valores

Também ficam as pastas:
- **PubMed:** contém arquivos para serem exportados para **PubMed**
- **ISI:** contém arquivos para serem exportados para **ISI**

Também há:
- várias pastas cujos nomes são **acrônimos dos periódicos**


### Pastas acrônimos de periódicos e seus fascículos

Em `<local da aplicação>\serial`, há várias pasta cujo nomes são **acrônimos dos periódicos**.

  
![conteúdo da pasta serial](./img/concepts_serial.jpg)


Em cada uma delas, há pastas e **cada uma** contém arquivos relacionados a **um fascículo**.
  

![conteúdo da pasta do acrônimo abc](./img/concepts_serial_abc.jpg)


### Pasta de um fascículo SGML/HTML

Contém:

- markup: arquivos marcados com o programa [Markup](markup.md)
- body: mesmos arquivos de **markup**, mas sem marcação
- pdf: arquivos **pdf** com nomes correspondentes, prefixados com o idioma das traduções. No caso do idioma original, não há prefixo.
- img: arquivo de imagens dos documentos
- base: base de dados isis geradas pelo programa [Converter](converter.md)


#### Regras para dar nomes às pastas de um fascículo

**ahead**

Ano com 4 dígitos, seguidos da palavra `nahead`.

Exemplo:

- 2009nahead 


**fascículos regulares**

- **v** seguido da identificação de volume
- **n** seguido da identificação do número
- **s** seguido da identificação do suplemento. Caso rótulo é ausente, use **0**.

Exemplos:

- v31n1 (volume 31, number 1)
- v31n1s1 (volume 31, number 1, supplement 1)
- v31n1s0 (volume 31, number 1, supplement)
- v31s0 (volume 31, supplement)
- v31s1 (volume 31, supplement 1)
- v31nspe (volume 31, special number)
- v31n3a (volume 31, number 3A)

