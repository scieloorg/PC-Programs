= Automata 1 =
 * pacote: [wiki:SciELO_PCPrograms SciELO PC Programs]
 * ferramenta embutida no [wiki:SciELO_PCPrograms_Markup Markup]
 * objetivo de reconhecer automaticamente as referencias bibliográficas

= Conceitos = 
Segundo Wikipedia, um autômato ou autômata funciona como um reconhecedor de uma determinada linguagem e serve para modelar uma máquina ou um computador simples. [http://en.wikipedia.org/wiki/Automata_theory]

Um conceito fundamental nos autômatos é o conceito de estado. Este conceito é aplicado a qualquer sistema, por exemplo, à televisão. Uma televisão pode estar ligada(on) ou desligada(off), temos então um autômata com dois estados. Ou seja, quando acionado o botão LIGAR, a televisão passa do estado de DESLIGADA a LIGADA.

= Autômata na metodologia SciELO = 
Para a metodologia SciELO, o autômata foi implementado para reconhecer automaticamente as referências bibliográficas de artigos ou texto dentro do programa [wiki:SciELO_PCPrograms_Markup Markup].

Analogamente à televisão, nas referencias bibliográfica, os delimitadores (ponto, vírgula, ponto-e-vírgula, dois-pontos, et-al, e outros caracteres ou conjuntos de caracteres) são os botões. À medida em que os caracteres da referencia bibliográfica são lidos e de acordo com as regras de transição pré-definidas, sabe-se qual trecho da referencia deve ser identificada como qual elemento (autor, título, data, etc).

Por exemplo:
As regras dizem que:
 * os autores são separados por ponto-e-vírgula
 * primeiro é o sobrenome e depois o prenome e são separados por vírgula

Então, o autômata reconhecerá que entre os ponto-e-vírgulas estão os autores (author) e, reconhece que antes da vírgula é o sobrenome (lname) e após a vírgula é prenome (fname).

O autômata trabalha com a idéia de estados (situações) diferentes. Deve-se prever todos os estados que podem ocorrer na referência bibliográfica, aos quais é possível fazer o autômata. Estas referências podem ser de artigos de periódicos, capítulos de livros ou teses e dissertações, etc.

O usuario do programa Markup, estando dentro do programa, com um artigo aberto, seleciona uma referencia bibliográfica e depois clica no botão Automata 1. O autômata lê a referencia selecionada e tenta reconhecer seus elementos (autores, títulos, etc). O autômata retornará 1 a varias possibilidades de marcação.

{{{
DICA IMPORTANTE: o arquivo de regras, ou aquele que simplesmente chamamos de autômata, 
não necessariamente precisa ser programado para reconhecer todos os tipos de referencias bibliográficas. 

É melhor que ele seja feito para reconhecer apenas um ou dois tipos de referencias bibliográficas mais frequentes. 
Pois sendo assim, certamente ele reconhecerá bem, pois reduzirá as ambiguidades.
}}}


= Como definir as regras para o autômata  = 

== Preparação ==

 * indispensável que as referências bibliográficas dos artigos científicos sigam um padrão, não importa que Norma (ABNT, ISO, APA, etc)  utilize.
 * necessaria a existencia dos arquivos de entrada no sistema:
   * automata.mds: lista de periódicos que possuem automatas
   * <acronimo do periodico>.amd: arquivo que contém as "regras" para o autômata

=== Arquivo automata.mds ===
Lista de periódicos que possuem autômatas.

Formato:

Para cada título:
 * Uma linha contém cada um destes itens abaixo, separados por ponto-e-vírgula:
   * ISSN do periódico
   * nome da norma utilizada (ocitat, vcitat, icitat, ...)
   * <acronimo>.amd
   * <arquivo_da_norma>.amd
 * Uma linha em branco

Exemplo:
Ex.: 1234-5678;ocitat;abb.amd;tgother.amd

 * 1234-5678: ISSN , conforme a title
 * ocitat: indica que a tag ocitat é utilizada nas referências bibliográficas
 * abb.amd: sigla ou acrônimo do periódico, conforme a title
 * tgother: indica que a norma other é adotada pelo periódico

{{{

1478-5236;acitat;acb.amd;tgabnt.amd

9632-5874;ocitat;aob.amd;tgother.amd

8523-6996;vcitat;ape.amd;tgvanc.amd


}}}

=== Arquivo <acronimo>.amd ===

Abaixo está o exemplo do autômata do periódico Abc Bxyz Bghj (abb.amd).

O autômata foi programado para reconhecer somente referencias bibliográficas de artigos de periódicos (contrib de oiserial).
Começando do nível geral (ocitat) para o específico, indicando cada uma das partes que a compõe, no caso: ocontrib e oiserial.

Referencia:
{{{
Carlson, R.E.; Monem, N.N.; Arjmand, O. & Shaw, R.H. 1979. Leaf condutance and leaf-water potential 
relationship for two soybeans cultivars grown under controlled irrigation. Agronomy Journal, 71: 321-325.
}}}

{{{
ocitat
o1
o3
o1;o2;NT;ocontrib;". "
o2;o3;NT;oiserial;"."

ocontrib
oc1
oc6
oc1;oc1;NT;oauthor;"; "
oc1;oc2;NT;oauthor;"&"
oc1;oc3;NT;oauthor;" ";"&"
oc2;oc3;NT;oauthor;" ";"&"
oc3;oc4;T;date;". "
oc4;oc5;T;title;": "
oc5;oc6;T;subtitle;". "
oc4;oc6;T;title;". "

oauthor
oa1
oa3
oa1;oa2;T;surname;", "
oa2;oa3;NT;fname;"; "
oa2;oa3;NT;fname;"&"
oa2;oa3;NT;fname;" ";"&"

oiserial
oi1
oi5
oi1;oi2;NT;sertitle;" "
oi2;oi3;T;volid;"("
oi3;oi4;T;issueno;"):"
oi2;oi4;T;volid;":";"("
oi4;oi5;T;pages;"."

fname
f1
f3
f1;f3;T;ign;"; "
f1;f3;T;ign;"&"
f1;f2;T;ign;" "
f2;f3;T;ign;" "
f1;f3;T;ign;" "

sertitle
s1
s2
s1;s1;T;ign;" "
s1;s2;T;ign;" "

}}}


==== Formato do arquivo <acronimo>.mds ====
Varios blocos com o seguinte formato:

 * A primeira linha contém o elemento a ser marcado. Ex.: ocitat
 * A segunda linha é o estado inicial. Ex.: o1
 * A terceira linha é o estado final. Ex.: o3
 * As demais linhas são as transições dos estados. E cada informação das transições estão separados por ponto-e-vírgula.
    {{{
    o1;o2;NT;ocontrib;". "
    o2;o3;NT;oiserial;"."
    }}}
 * linha em branco

No caso acima temos três estados: o1, o2 e o3. Sendo o inicial o1 e o final o3.

{{{
NOTAS: 
 * Os nomes dos estados não devem se repetir entre os blocos.
 * Os nomes podem ser quaisquer e1, e2, e3, estado1, estado2, inclusive e2 até poderia chamar-se e5. 
 * O importante é um estado levar ao outro. 
}}}

===== As transições =====
{{{
o1;o2;NT;ocontrib;". "
o2;o3;NT;oiserial;"."
}}}

A linha 
{{{
o1;o2;NT;ocontrib;". "
}}}
significa que do estado o1 para o estado o2 será inserida a tag ocontrib na referência e o delimitador será o ponto e o espaço (". "). Está entre aspas para agrupar o conjunto de caracteres.

O '''NT''' indica que o '''ocontrib''' é um elemento '''não-terminal''', ou seja, dentro dele há outros elementos a serem marcados e, por isso, haverá neste arquivo '''um bloco para o ocontrib''', da mesma forma que houve com ocitat.
         
A linha 
{{{
o2;o3;NT;oiserial;"."
}}}
significa que do estado o2 para o estado o3 será marcada a tag oiserial, do local onde fechar o ocontrib até o ponto final (".").

