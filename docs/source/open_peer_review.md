
# Open Peer Review: Markup e Geração do XML para Pareceres

Este guia apresenta como identificar no programa de marcação os dados relacionados a **pareceres**.


## Identificação que o documento é um parecer

Identificação do atributo "article-type" do elemento "article"

Para que seja gerado

```xml
<article article-type="referee-report">
```

no arquivo marcado deve conter, no elemento `doc`, o atributo `doctopic` com valor `referee-report`

```xml
[doc doctopic="referee-report" ... ]
```

O valor `referee-report` é apresentado com uma das opções do campo `doctopic` do formulário do elemento principal `doc`.

   ![Formulário para preencher o valor do atributo doctopic do elemento doc](./img/doc-mkp-formulario-doctopic.png)



## Identificação dos pareceres anexados ao documento revisado

Quando cada parecer está em anexo ao documento avaliado.

Identificação do atributo "article-type" do elemento "sub-article"

Para que seja gerado

```xml
<sub-article article-type="referee-report">
```

no arquivo marcado deve conter, no elemento `subdoc`, o atributo `subarttp` com valor `referee-report`

```xml
[subdoc subarttp="referee-report" ... ]
```

O valor `referee-report` é apresentado com uma das opções do campo `subarttp` do formulário do elemento `subdoc`.

   ![Formulário para preencher o valor do atributo subarttp do elemento subdoc](./img/mkp-subdoc-subarttp.png)



## Identificação do papel do parecerista (revisor ou editor)

Para que seja gerado

```xml
<role specific-use="reviewer">Reviewer</role>
```

ou

```xml
<role specific-use="editor">Editor</role>
```

em 

```xml
<contrib contrib-type="author">
    <name>
        <surname>Doe</surname>
        <given-names>Jane X</given-names>
    </name>
    <role specific-use="reviewer">Reviewer</role>
</contrib>
```


no arquivo marcado deve conter, no elemento `oprrole`, o atributo `specuse` com valor `reviewer` ou `editor`


```xml
[oprrole specuse="reviewer"]Reviewer[/oprrole]
```

ou

```xml
[oprrole specuse="editor"]Editor[/oprrole]
```

Os valores `reviewer` e `editor` são apresentados com opções do campo `specuse` do formulário do elemento `role`.


   ![Formulário para preencher os atributos do elemento oprrole](./img/mkp-oprrole-specuse-reviewer-revisor-form.png)

   ![Elemento oprrole com atributo specuse](./img/mkp-oprrole-specuse-reviewer-revisor-marcado.png)

   

## Identificação do anonimato do parecerista (revisor ou editor)

Para que seja gerado

```xml
<anonymous/>
```

em 

```xml
<contrib contrib-type="author">
    <anonymous/>
    <role specific-use="reviewer">Reviewer</role>
</contrib>
```

no arquivo marcado deve conter, no elemento `anonymous` e é obrigatório o uso de `role`.

```sgml
[anonymous][/anonymous]
```

```xml
[role specuse="reviewer"]Reviewer[/role]
```

ou

```xml
[role specuse="editor"]Editor[/role]
```

Os valores `reviewer` e `editor` são apresentados com opções do campo `specuse` do formulário do elemento `role`.

   [Formulário para preencher os atributos do elemento role]: img/mkp-role-specuse-reviewer-revisor-form.png "Formulário para preencher os atributos do elemento role"
   [Elemento role com atributo specuse]: img/mkp-role-specuse-reviewer-revisor-marcado.png "Elemento role com atributo specuse"
   

## Identificação do artigo revisado

Indicar **artigo revisado** no documento do **parecer** da seguinte forma:

```xml
<related-object
	object-type="peer-reviewed-material"
	id="r01"
	xlink:href="10.1590/abd1806-4841.20142998"
	ext-link-type="doi"/>        
```

no arquivo marcado deve conter, no elemento `related` com o atributo `reltp` cujo valor é `peer-reviewed-material`

```sgml
[related reltp="peer-reviewed-material" pid-doi="10.1590/abd1806-4841.20142998"][/related]
```

Para o atributo `pid-doi`, preencher com o valor do PID ou DOI do artigo revisado.


   [Elemento related com atributo reltp cujo valor é peer-reviewed-material]: img/mkp-related-reltp-peer-reviewed-material.png "Elemento related com atributo reltp cujo valor é peer-reviewed-material"

   [Formulário para preencher related]: img/mkp-form-related.png "Formulário para preencher related"


## Identificação do parecer externo

Indicar o **parecer** que está publicado em outro site da seguinte forma:

```xml
<related-object
	object-type="referee-report"
	ext-link-type="uri"
	xlink:href="https://publons.com/publon/000000/#review-2020xxx"
	>Publons</related-object>        
```

no arquivo marcado deve conter, no elemento `related` com o atributo `reltp` cujo valor é `referee-report`

```sgml
[related reltp="referee-report" pid-doi="https://publons.com/publon/000000/#review-2020xxx"]Publons[/related]
```

Para o atributo `pid-doi`, preencher com o valor do PID ou DOI do artigo revisado.


   [Elemento related com atributo reltp cujo valor é referee-report]: img/mkp-related-reltp-referee-report.png "Elemento related com atributo reltp cujo valor é referee-report"

   [Formulário para preencher related]: img/mkp-form-related.png "Formulário para preencher related"



## Identificação da data de recebimento do parecer

A representação da data de recebimento do parecer é feita por:

```xml
<history>
    <date date-type="referee-report-received">
      <day>10</day>
      <month>01</month>
      <year>2020</year>
    </date>
</history>
```

no arquivo marcado deve conter, no elemento `hist`, o elemento `histdate`, com o atributo `datetype` cujo valor é `referee-report-received`


   [Elemento histdate marcado com datetype igual a referee-report-received]: img/mkp-histdate-datetype-referee-report-received.png "Elemento histdate marcado com datetype igual a referee-report-received"

   [Formulário para preencher quaisquer tipo de histdate]: img/mkp-form-histdate.png "Formulário para preencher quaisquer tipo de histdate"


