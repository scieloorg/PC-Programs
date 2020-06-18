# Open Peer Review

## Markup

# Identificação do atributo "article-type" do elemento "article" 

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


# Identificação do atributo "article-type" do elemento "sub-article" 

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

