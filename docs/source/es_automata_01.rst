==========
Automata 1
==========
* paquete: `SciELO PC Programs <http://docs.scielo.org/projects/scielo-pc-programs/en/latest/>`_
* herramienta integrada al `Markup <http://docs.scielo.org/projects/scielo-pc-programs/en/latest/markup.html>`_
* objetivo de reconocer automáticamente las citas bibliográficas

Qué es un automata?
-------------------

En realidad, automata es un modelo matemático. Por ejemplo, segun Wikipedia, un autómato o autómata funciona como un identificador de una determinada lenguaje y sirve para modelar una máquina o un computador simples. (http://en.wikipedia.org/wiki/Automata_theory).

Un concepto fundamental en los autómatos es el concepto de estado. Este concepto es aplicado a cualquier sistema, por ejemplo, a la televisión. 
Una televisión puede estar encendida(on) o apagada(off), tenemos entonces un autómata con dos estados. 
Es decir, cuando accionado el botón ENCENDER, la televisón va del estado APAGADA para ENCENDIDA.

Autómata en la metodología SciELO
---------------------------------
Para la metodología SciELO, el autómata fue implementado para reconocer automáticamente las citas bibliográficas de artículos o textos, y está integrado al programa `Markup <http://docs.scielo.org/projects/scielo-pc-programs/en/latest/markup.html>`_.
Se seleciona una cita y después haz un clic en el botón Automata 1, el programa automata es ejecutado y muestra las posibilidades de marcación en una ventana. 
El usuario verifica cuales de las posibilidades es la más adecuada y la elige. A veces, el automata no es preciso, podiendo el usuario aprovechar lo que el automata identificó, y corregir lo que no está bien.

Análogamente a la televisión, en las citas bibliográfica, los delimitadores (punto, coma, punto-y-coma, dos-puntos, et-al, y otros caracteres o conjuntos de caracteres) 
son los botones de la televisión. A la medida em que os caracteres de la cita bibliográfica son encontrados y de acordo con las reglas de transición pré-definidas, 
el automata aplica las etiquetas correspondientes a los elementos (autor, título, data, etc).
Es decir, al reconocer en las citas los delimitadores, hay el cambio de estado y una acción es ejecutada.

En la metodología SciELO, llamamos de automata de la revista, justamente al archivo texto que describe las reglas de cambio de estado y acciones tomadas.

Por ejemplo:

Las reglas dicen que:

* los autores son separados por punto-y-coma
* primero está el  apellido y después el nombre y son separados por coma

Entonces, el autómata reconocerá que entre los punto-y-comas están los autores (author) y, reconoce que antes de la coma está el apellido (lname) y después a la coma está el nombre (fname).


    IMPORTANTE:
    Seria posible preveer todos los estados que pueden ocurrir en las citas bibliográficas, es decir, artículos de revistas, capítulos de libros, libros, tesis, disertaciones etc.
    Pero en realidad esto seria muy poco eficiente. Vale más la pena hacer un autómata que identifique el tipo de cita que más ocurre. Para algunas revistas el tipo que más ocurre es lo de artículo de revista, en otras revistas la gran parte es la de libros.


Preparación
-----------
* todas las citas bibliográficas de mismo tipo de documento deben obedecer a un estándar, no necesariamente ABNT, ISO, APA, etc, pues lo que importa es la regularidad.
* el nombre del archivo de automata de la revista debe ser <acronimo del periodico>.amd


Creando Archivo <acronimo>.amd
------------------------------
Abajo está el ejemplo de autómata de la revista Abc Bxyz Bghj (abb.amd). La norma que esta revista sigue es other, entonces, por eso se usa las etiquetas oiserial, oauthor, ocontrib, etc.

El autómata fue programado para reconocer solamente citas bibliográficas de artículos de revistas (ocontrib de oiserial).
Empezando del nivel general (ocitat) para lo específico, indicando cada una de las partes que la compone, en el caso: ocontrib y oiserial.

Cita:

    Carlson, R.E.; Monem, N.N.; Arjmand, El. & Shaw, R.H. 1979. Leaf condutance and leaf-water potential relationship for two soybeans cultivars grown under controlled irrigation. Agronomy Journal 71: 321-325.

    ::
    
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



Blocos
------

Varios blocos con el siguiente formato:

* La primera línea contiene el elemento a ser marcado. Ex.: ocitat
* La segunda línea el  estado inicial. Ex.: o1
* La terceira línea el  estado final. Ex.: o3
* Cada una de las otras líneas es una transición de estado. Cada información está separada por punto-y-coma.
    

    ::
  
        o1;o2;NT;ocontrib;". "
        o2;o3;NT;oiserial;"."
    

* una línea en blanco (para separar los blocos)

en el caso encima tenemos tres estados: o1, o2 y o3. Siendo lo inicial o1 y lo final o3.


.. attention::

    * Los nombres de los estados NO DEBEN REPETIRSE EN BLOCOS DISTINTOS.
    * Los nombres pueden ser cuaisquer e1, e2, e3, estado1, estado2, incluso los números no necesitan estar en secuencia, e2 podría llamarse e5. 

  


Cada bloco describe un nivel de la cita.
* bloco ocitat: nivel más alto, pues identifica la cita completamente, del inicio al punto final.
* bloco ocontrib: describe como se marca ocontrib.
* bloco oauthor: describe como se marca oauthor (autores).

Note que al ejecutar el bloco ocitat, en algun momento, se ejecutará el bloco ocontrib, pues ocontrib está dentro de ocitat.

Estado final
------------
Las líneas  que describen cómo se llega al estado final, obligatoriamente tienen que tener el último caracter igual en los dos blocos, lo superior y lo vigente.

Ejemplo: en el bloco ocitat, ocontrib termina con ". " (punto y espacio), entonces, obligatoriamente el bloco ocontrib, en estado final tiene que terminar con ". ".


    ::

        ocitat
        o1
        o3
        o1;o2;NT;ocontrib;". " <== termina ocontrib
        o2;o3;NT;oiserial;"."  <== termina oiserial, termina ocitat

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
        oc4;oc6;T;title;". " <== termina ocontrib

        oiserial
        oi1
        oi5
        oi1;oi2;NT;sertitle;" "
        oi2;oi3;T;volid;"("
        oi3;oi4;T;issueno;"):"
        oi2;oi4;T;volid;":";"("
        oi4;oi5;T;pages;"." <== termina oiserial, termina ocitat


Transiciones de estado
----------------------

    ::

        o1;o2;NT;ocontrib;". "
        o2;o3;NT;oiserial;"."


La línea 

    ::
        
        o1;o2;NT;ocontrib;". "


significa que desde del estado o1 para el estado o2 será insertada la etiqueta ocontrib en la cita y el delimitador será el punto y espacio (". "). Está entre comillas para agrupar el conjunto de caracteres.

El **NT** indica que **ocontrib** es un elemento **no-terminal**, o sea, él agrupa otros elementos.
Todos los elementos no-terminal tendrán un bloco para describir cómo marcar sus elementos, de la misma forma que hay el bloco ocitat.
         
La línea 

    ::

        o2;o3;NT;oiserial;"."


significa que desde del estado o2 para el estado o3 será marcada la etiqueta oiserial, es decir,  desde del local donde termina ocontrib (o1->o2) al punto final (".").


Elementos que se repiten
------------------------

Hay elementos que se repiten como autores.


    ::

        ocontrib
        oc1
        oc6
        oc1;oc1;NT;oauthor;"; "    <== queda en el mismo estado, marcando repetidas veces la etiqueta oauthor, hasta que no encuentra más el punto-y-coma
        oc1;oc2;NT;oauthor;"&"
        oc1;oc3;NT;oauthor;" ";"&"
        oc2;oc3;NT;oauthor;" ";"&"
        oc3;oc4;T;date;". "
        oc4;oc5;T;title;": "
        oc5;oc6;T;subtitle;". "
        oc4;oc6;T;title;". " 


Qué hacer con elementos opcionales
----------------------------------

A veces hay elementos que dependiendo de la cita están o no presentes. Por ejemplo, suplementos, subtítulos, número.

Cita:

    ::

        Carlson, R.E.; Monem, N.N.; Arjmand, El. & Shaw, R.H. 1979. Leaf condutance and leaf-water potential 
relationship for two soybeans cultivars grown under controlled irrigation. Agronomy Journal 71: 321-325.

        CASATTI, L.; MENDES, HF. & FERREIRA, KM. 2003. Aquatic macrophytes as feeding site for small fishes in the Rosana reservoir, 
Paranapanema river, southeastern Brazil. Revista Brasileira de Biologia 63(2): 213-222.



    ::

        oiserial
        oi1
        oi5
        oi1;oi2;NT;sertitle;" "
        oi2;oi3;T;volid;"("      <== oi2->oi3 marca volumen cuando tiene número
        oi3;oi4;T;issueno;"):"
        oi2;oi4;T;volid;":";"("  <== oi2->oi4 marca volumen cuando no hay número, va directo a pages
        oi4;oi5;T;pages;"." 



Desde o1, hay dos opciones de oi2. El automata elige la opción de acuerdo con los delimitadores que encuentra "(" ó ":".


Qué hacer cuando no hay un delimitador?
---------------------------------------

En la cita, este caso ocurre con el título de la revista. Pero puede pasar con nombres y apellidos, cuando hay más de un nombre y después el apellido.

    ::

        Agronomy Journal 71: 321-325.
        Revista Brasileira de Biologia 63(2): 213-222.

El delimitador del título de la revista es espacio, que es el mismo caracter que está entre las palabras del título de la revista.

Para solucionar esto, hay un artificio:


    ::

        oiserial
        oi1
        oi5
        oi1;oi2;NT;sertitle;" " <== sertitle queda no-terminal (NT), a pesar de no tener ningun elemento dentro de él.
        oi2;oi3;T;volid;"("
        oi3;oi4;T;issueno;"):"
        oi2;oi4;T;volid;":";"("
        oi4;oi5;T;pages;"."

        ...

        sertitle <== bloco para sertitle
        s1
        s2
        s1;s1;T;ign;" " <== uso de la etiqueta ign (ignore)
        s1;s2;T;ign;" "


CUESTIONES IMPORTANTES
----------------------

Mejor probar mientras crea el automata
......................................
En el programa Markup, abra un artículo marcado (podendo ter citas marcadas o no).  
Si las tiene marcadas, desmarque la que quiere probar el automata.
Seleccionela y haga un clic en Automata 1.
Siempre probar el automata con todas las citas anteriormente probadas, pues cualquier nueva actualización en el autómata puede hacerlo menos eficiente o introducir errores, que a veces son terriblemente dificil de encontrar.

Mejor hacer en pequeños pasos
..........................
Como no hay un depurador para identificar cualquier error en un archivo de automata y, solamente una persona con experiencia en automata podría identificar un error al mirarlo,
mejor que el desarrollo de automata sea paso a paso y a cada paso una prueba sea hecha.

Cómo seria el paso a paso?

Por ejemplo, seria tener solamente:

{{{
ocitat
o1
o3
o1;o2;T;ocontrib;". "  <== probar ocontrib como si fuera terminal
o2;o3;T;oiserial;"."  <== probar oiserial como si fuera terminal
}}}


Desarrollar oiserial o ocontrib, que cambia menos.  Pruebe, avance, pruebe, avance, pruebe, incluso las citas anteriormente probadas.

== Mejor poner esfuerzos en pocas variaciones de tipo de cita ==
Nada le impide de crear automatas para todos los tipos de citas (conferencia, tesis, libro, artículo, etc), pero mejor crear un autómata que sepa reconocer con 100% de aciertos los tipos más frecuentes.
Esto es recomendable principalmente cuando el desarrollador de automatas tiene poca experiencia.

 