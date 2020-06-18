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


# Identificação do atributo "specific-use" do elemento "contrib/role"

Para que seja gerado

```xml
<role specific-use="reviewer">Reviewer</role>
```

ou

```xml
<role specific-use="editor">Editor</role>
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
   