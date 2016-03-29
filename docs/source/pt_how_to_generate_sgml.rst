.. _como-gerar-arquivo-sgml:

Como gerar arquivos SGML (Marcação no HTML com a DTD article e text)
====================================================================

.. toctree::
   :maxdepth: 3


.. _especificacao-arquivos:

Especificações de Arquivos
--------------------------

- Um documento (artigo ou texto) por arquivo
- .html
- Todos os arquivos relacionados ao documento devem ter o mesmo nome. Por exemplo, a01.pdf.
- Todos os arquivos 'translations' devem ter o mesmo nome precedido pelo código de duas letras (norma ISO 639-1). Por exemplo, en_a01.pdf, en_a01.html.


.. _localizacao-arquivos:

Localização dos Arquivos
------------------------

Organize os arquivos de acordo com esta estrutura de arquivos/pastas:

Arquivos para Marcação
    /scielo/serial/<acron>/<numero_identificador>/markup

body
    /scielo/serial/<acron>/<numero_identificador>/body

imagens
    /scielo/serial/<acron>/<numero_identificador>/img

pdf
    /scielo/serial/<acron>/<numero_identificador>/pdf

Por exemplo:

.. image:: img/concepts_serial_abc.jpg


.. _arquivos-markup:

Arquivos do Markup
------------------

O arquivo /scielo/bin/markup/markup_journals_list.csv não deve existir, caso o arquivo exista, exclua-o.

Em */scielo/bin/markup/* deve existir:

- ??_issue.mds: atualizar/criar como qualquer dado de número de fascículo  é atualizado/criado
- issue.mds: atualizar/criar como qualquer dado de número de fascículo  é atualizado/criado
- journal-standard.txt: atualizar/criar como o dado de qualquer revista é atualizado / criado

Estes arquivos são gerados através do `Title Manager <titlemanager.html>`_ our SciELO Manager.


.. _programa-markup:

Markup
------

Use `Markup Program <markup.html>`_.


----------------

Última atualização dessa página: agosto de 2015.
