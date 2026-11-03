# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 7 — Simplicity (Simplicidad)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo introduce la Ley de la Simplicidad: la facilidad de mantenimiento de cualquier pieza de software es proporcional a la simplicidad de sus piezas individuales. Cuanto más simples sean las piezas, más fácil será cambiar las cosas en el futuro. El mantenimiento perfecto es imposible, pero esa es la meta hacia la que se trabaja: cambio total o código nuevo infinito sin dificultad.

La ley habla de la simplicidad de las piezas individuales, no del sistema completo, porque un programa de tamaño medio es tan complejo que ningún humano puede comprenderlo todo de una vez. Siempre hay una estructura grande y compleja para el programa entero; lo que importa es que cada pieza se entienda al mirarla. Eso es clave al entregar código a otros o al volver a tu propio código meses después.

Sales sabiendo que la simplicidad es el factor que reduce defectos y mantiene el código mantenible, que es relativa a la audiencia y el contexto, y que exige diseño consciente. El autor también desarrolla la consistencia, la legibilidad (espaciado, nombres, comentarios) y la necesidad de diseñar deliberadamente para evitar el crecimiento hacia la complejidad.

## La analogía de la arquitectura

Imagina construir una estructura de acero de 30 pies. Puedes hacerla con muchas vigas pequeñas (piezas simples) o forjar tres piezas enormes y complejas y unirlas.

- Con las vigas: es fácil fabricar o comprar las piezas; si una se rompe, la reemplazas por un repuesto idéntico. Construcción y mantenimiento simples.
- Con las tres piezas enormes: hay que fabricarlas a medida y trabajarlas mucho; cada una es tan grande que es difícil encontrar y corregir sus defectos. Si aparecen fallos tras terminar el edificio, no puedes reemplazarlas (el edificio se caería), así que sueldas parches feos y esperas que aguante.

El software es igual: con piezas simples y autocontenidas, corregir defectos y mantener el sistema es fácil; con bloques grandes y complejos, cada pieza da mucho trabajo, recibe menos pulido y el sistema se vuelve difícil de mantener, lleno de parches y hacks. La gente usa los bloques grandes por un ahorro de tiempo percibido al inicio (encajan de golpe), pero la calidad es menor y el coste futuro mayor. A largo plazo, lo eficiente es la simplicidad, no la complejidad.

Para aplicar la ley: hacer los componentes tan simples como sea posible y mantenerlos así con el tiempo, por ejemplo usando el método de desarrollo y diseño incremental (hay un paso de "rediseño" antes de añadir cada nueva función que sirve para simplificar). Hay que rediseñar piezas continuamente conforme surgen nuevas situaciones y requisitos.

## Simplicidad y la Ecuación del Diseño de Software

La ley indica lo más importante que podemos hacer ahora mismo para reducir el esfuerzo de mantenimiento: hacer el código más simple. No hace falta predecir el futuro; basta mirar el código, ver si es complejo y hacerlo menos complejo ya. Así se logra un esfuerzo de mantenimiento que decrece con el tiempo. Simplificar cuesta algo de trabajo ahora, pero ahorra mucho tiempo después y, al reducir el esfuerzo de mantenimiento, aumenta la deseabilidad de todos los cambios posibles.

## La simplicidad es relativa

Lo que es simple depende de la audiencia objetivo. Algo puede parecerte simple porque lo entiendes por dentro, pero resultar muy complicado a quien lo ve por primera vez. Para entender ese punto de vista, lee código que nunca hayas visto e intenta comprender no solo las líneas, sino qué hace todo el programa y cómo lo modificarías.

Por eso conviene documentación con secciones tipo "New to This Code?" con explicaciones simples, escritas como si el lector no supiera nada. Muchos proyectos fallan aquí: muestran una masa de enlaces sin dirección, que parece simple al desarrollador veterano pero es complicada para el recién llegado. Lo único peor que la documentación compleja es no tener documentación.

El contexto también importa: tecnologías avanzadas pueden llevar a la simplicidad si se usan bien, pero la misma estructura interna mostrada como única interfaz en una web no sería simple. Mucho texto en una valla de carretera es excesivo; mucho texto explicativo en un manual es más simple que una sola frase. Lograr simplicidad no es imposible: cada cosa tiene una audiencia y un contexto limitados, así que el problema siempre es resoluble.

## La guerra de editores

El ejemplo más famoso es la disputa entre los editores de texto vi y Emacs. En realidad rara vez hay una herramienta fundamentalmente superior; solo hay una que ciertas personas encuentran más simple para la tarea. Parte depende de diferencias individuales, pero en mayor medida la simplicidad percibida depende de la familiaridad: quien usa mucho una herramienta la vuelve simple desde su punto de vista. Para los no programadores ambos editores parecerían complejos, otro ejemplo de que la simplicidad es relativa. Salvo que una herramienta tenga problemas que la hagan inadecuada ("Bad Technologies", cap. 8), su simplicidad relativa es lo que permite a cada programador decidir qué es mejor.

## Cuán simple tienes que ser

Si quieres tener éxito de verdad: "Stupid, dumb simple" (ridícula, tontamente simple). Lo bueno de ese nivel es que lo usable por gente normal también lo es por genios, ampliando el rango de usuarios posibles.

El ejemplo del mapa del centro comercial: los mejores tienen un gran punto rojo con "YOU ARE HERE" en letras enormes; los peores, un diminuto triángulo amarillo difícil de encontrar. Al diseñador le parece razonable porque le dedicó tiempo; para el usuario es una parte mínima de su vida que solo quiere resolver rápido. Muchos programadores cometen ese error: asumen que otros dedicarán mucho tiempo a aprender su código. No es cuestión de inteligencia sino de conocimiento: el que llega nuevo no sabe nada y hay que facilitarle el aprendizaje (documentación simple, diseño simple, tutoriales paso a paso).

Si el código no es tontamente simple de aprender, la gente lo usará mal, creará bugs y vendrá a preguntarte a ti. A veces complicamos las cosas para no parecer condescendientes o para que admiren nuestra inteligencia, pero eso no ayuda. Hacer algo estúpidamente simple permite a la gente entenderlo y sentirse capaz. La audiencia del código siguen siendo otros programadores (la familia no tiene que leerlo), pero a ellos debe parecerles muy simple, usando toda la tecnología avanzada que haga falta para lograr esa simplicidad.

## Sé consistente

La consistencia es gran parte de la simplicidad: si haces algo de una manera en un sitio, hazlo así en todos. Si nombras una variable `somethingLikeThis`, todas deben seguir ese estilo; si usas `named_like_this`, todas en minúsculas con guiones bajos. El código inconsistente es más difícil de leer, igual que una frase escrita sin las convenciones del idioma.

Hay situaciones donde no importa cómo lo hagas mientras siempre lo hagas igual; mejor consistente y simple, pero si no puedes ser del todo simple, al menos sé consistente. La consistencia total facilita programar: si todos los objetos tienen un campo `name`, un solo trozo de código lo maneja; si el Objeto A usa `a_name` y el B `name_of_mine`, necesitas código especial para cada uno. El programa también debe comportarse de forma consistente internamente: si usar la Parte A requiere llamar tres funciones y escribir algo de código, la Parte B debería ser similar; una función `dump` en A debe hacer lo mismo que una `dump` en B. Tú mandas en el mundo de tu programa, así que puedes hacerlo simple y consistente.

## Legibilidad

El código se lee más veces de las que se escribe, por eso debe ser fácil de leer: la legibilidad depende sobre todo de cómo el espacio es ocupado por letras y símbolos. El espacio mantiene las cosas separadas; demasiado espacio dificulta ver cómo se relacionan y muy poco dificulta ver que están separadas. No hay regla exacta, salvo que el espaciado sea consistente e informe sobre la estructura.

Ejemplo de espaciado, mismo código con tres densidades:

```
x=1+2;y=3+4;z=x+y;if(z>y+x){print"error";}
```

Con demasiado espacio también resulta difícil de leer. Con espaciado razonable:

```
x = 1 + 2;
y = 3 + 4;
z = x + y;
if (z > y + x) {
    print "error";
}
```

Un código legible también es más fácil de arreglar: aquí se ve que `z` nunca será mayor que `y + x` (siempre es igual), así que el bloque `if (z > y + x)` sobra. Ante código muy buggy y difícil de leer, lo primero es hacerlo más legible para ver dónde están los bugs.

### Nombrar las cosas

Los nombres deben ser lo bastante largos para comunicar qué es o qué hace algo, sin ser tan largos que cuesten de leer. Hay que pensar cómo se usará: una función llamada una sola vez en su propia línea puede tener nombre largo; una usada con frecuencia en expresiones complejas debe ser corta pero suficiente.

```
q = s(j, f, m);
p(q);
```

Nombres pobres. Con buenos nombres:

```
quarterly_total = sum(january, february, march);
print(quarterly_total);
```

Nombres excesivamente largos vuelven a ocupar demasiado espacio y estorban la lectura, así que nombrar también depende de cómo letras y símbolos ocupan el espacio.

### Comentarios

Los buenos comentarios ayudan a la legibilidad, pero en general no deben decir qué hace un trozo de código (eso debe ser obvio al leerlo; si no lo es, simplifica el código). Solo si no puedes hacerlo más simple, añade un comentario que explique qué hace. El verdadero propósito de los comentarios es explicar por qué hiciste algo cuando la razón no es obvia; si no lo explicas, otros podrían eliminar partes importantes al cambiar el código. La legibilidad es muy importante y suele ser el primer paso hacia un buen diseño, pero no lo es todo: puedes tener código legible y aun así un sistema demasiado complejo.

## La simplicidad requiere diseño

La gente no construye sistemas simples de forma natural; sin atención al diseño, un sistema evoluciona hacia una bestia enorme y complicada. Un proyecto sin buen diseño que sigue creciendo acaba hundido en complejidad y, pese a todas las excusas (cultura corporativa de "solo hackeamos nuevas features"), un día fallará.

Diseñar bien suele dar poco crédito: los fallos catastróficos son grandes y visibles, mientras que los pequeños incrementos hacia un buen diseño son invisibles para quien no está muy conectado con el código. Manejar un gran fallo recibe agradecimiento; prevenir uno, rara vez se nota. Aun así hay recompensas: software que funciona, releases a tiempo, un código claro y la confianza en tu propio trabajo. A los programadores junior o colegas puede costarles entender por qué diseñar bien; leer este libro ayuda, y si no, hay que guiarlos hacia buenas decisiones de diseño hasta que, en un par de años como mucho, vean cómo compensan.

## Ideas clave

- Ley de la Simplicidad: la facilidad de mantenimiento es proporcional a la simplicidad de las piezas individuales, no del sistema completo.
- Piezas pequeñas y simples (como vigas) frente a bloques grandes y complejos: lo simple es más barato de mantener a largo plazo.
- Simplificar el código ahora reduce el esfuerzo de mantenimiento y aumenta la deseabilidad de todos los cambios futuros.
- La simplicidad es relativa a la audiencia y al contexto; mucha simplicidad percibida viene de la familiaridad (ejemplo vi vs Emacs).
- Para tener éxito hay que ser "stupid, dumb simple": fácil de aprender para quien no sabe nada del código.
- La consistencia es parte esencial de la simplicidad: haz las cosas igual en todas partes, incluso en el comportamiento interno del programa.
- La legibilidad depende del uso del espacio, buenos nombres y comentarios que expliquen el porqué, no el qué.
- La simplicidad requiere diseño deliberado; sin él, el sistema crece hacia la complejidad y el proyecto termina fallando.
