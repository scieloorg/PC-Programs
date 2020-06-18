
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

   [Formulário para preencher o valor do atributo doctopic do elemento doc]: img/doc-mkp-formulario-doctopic.png "Formulário para preencher o valor do atributo doctopic do elemento doc"


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

   [Formulário para preencher o valor do atributo subarttp do elemento subdoc]: img/mkp-subdoc-subarttp.png "Formulário para preencher o valor do atributo subarttp do elemento subdoc"


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
        <xref ref-type="aff" rid="aff1"/>
</contrib>
```


no arquivo marcado deve conter, no elemento `role`, o atributo `specuse` com valor `reviewer` ou `editor`

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

