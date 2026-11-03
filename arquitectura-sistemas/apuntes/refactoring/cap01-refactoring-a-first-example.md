# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 1 — Refactoring, a First Example (Refactorización, un primer ejemplo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF (PDF p. N).

## Lo que necesitas saber

Fowler abre el libro con un ejemplo en lugar de con historia y principios, porque considera que es con ejemplos como se entiende realmente qué ocurre al refactorizar. Reconoce la paradoja del autor: un programa grande sería demasiado complejo para seguirlo, y uno pequeño hace que la refactorización parezca innecesaria. Pide al lector imaginar el pequeño programa de ejemplo como parte de un sistema mucho mayor, donde las mejoras sí importan.

El capítulo recorre, paso a paso, la transformación de un programa que calcula e imprime el recibo de alquiler de películas de un videoclub. La tesis central es que un diseño pobre no molesta al compilador pero sí al humano cuando hay que cambiar el sistema: un sistema mal diseñado es difícil de cambiar porque cuesta localizar dónde modificar y es fácil introducir errores. La refactorización reestructura el código para hacer esos cambios fáciles antes de hacerlos.

Sales sabiendo el ritmo esencial de la refactorización: probar, cambio pequeño, probar, cambio pequeño. Verás aplicadas varias refactorizaciones con nombre (Extract Method, Move Method, Replace Temp with Query, Replace Type Code with State/Strategy, Replace Conditional with Polymorphism) y cómo cada una redistribuye responsabilidades hacia la clase que posee los datos.

## El ejemplo que recorre el capítulo

El programa calcula el recibo de cargos de un cliente de un videoclub. Hay tres tipos de película: regular, infantil (`CHILDRENS`) y novedad (`NEW_RELEASE`). Los cargos dependen de cuántos días se alquiló la película y de su tipo. Además del cargo, el recibo calcula puntos de cliente frecuente (frequent renter points), que varían según si la película es novedad.

Clases iniciales: `Movie` (clase de datos simple con título y código de precio), `Rental` (representa el alquiler de una película por un cliente, con película y días alquilados) y `Customer` (tiene el nombre, un `Vector` de alquileres y el método largo `statement()`).

El problema: el método `statement()` de `Customer` hace demasiado y muchas de sus tareas corresponden a otras clases. Llegan dos cambios pedidos por los usuarios: imprimir el recibo en HTML y modificar la clasificación de películas (reglas de cargo y de puntos). Con el diseño inicial, el recibo HTML obligaría a duplicar `statement()` por copiar y pegar, y los cambios de reglas habría que mantenerlos consistentes en dos sitios.

> "When you find you have to add a feature to a program, and the program's code is not structured in a convenient way... first refactor" (PDF p. 17)

## El primer paso: construir pruebas

Antes de refactorizar, Fowler construye un conjunto sólido de pruebas para esa parte del código. Crea varios clientes con distintos alquileres, genera las cadenas del recibo y las compara contra cadenas de referencia verificadas a mano. Las pruebas se ejecutan con un solo comando Java, tardan pocos segundos y son autoverificables: dicen "OK" o imprimen la lista de líneas que difieren. Las pruebas dan la seguridad necesaria para cambiar el programa.

> Antes de empezar a refactorizar, comprueba que tienes un conjunto sólido de pruebas, y que estas sean autoverificables (PDF p. 18).

## Descomponer y redistribuir statement()

El primer objetivo es el método largo `statement()`. La meta es partirlo en piezas pequeñas y moverlas a mejores clases para facilitar escribir luego el recibo HTML con poca duplicación.

- **Extract Method sobre el `switch`**: se extrae el cálculo del cargo a un método `amountFor(Rental each)`. Antes de extraer, Fowler analiza las variables locales del fragmento: `each` (no modificada, pasa como parámetro) y `thisAmount` (modificada, se devuelve). Al extraer cometió un error (declaró el retorno `int` en vez de `double`, y Java redondea sin avisar); las pruebas lo detectaron de inmediato. Es la lección del proceso: como cada cambio es muy pequeño, los errores son fáciles de encontrar.

> Refactoring changes the programs in small steps. If you make a mistake, it is easy to find the bug (PDF p. 21).

- **Renombrar variables**: dentro de `amountFor` renombra `each` a `aRental` y `thisAmount` a `result`. El buen código comunica su propósito, y los nombres son clave para la claridad.

> Any fool can write code that a computer can understand. Good programmers write code that humans can understand (PDF p. 22).

- **Move Method**: como `amountFor` usa datos del alquiler y no del cliente, el método está en el objeto equivocado. Se mueve a `Rental` renombrado como `getCharge()` (sin parámetro). Un método debería estar en el objeto cuyos datos usa. Se primero delega desde `Customer` y luego se ajustan las referencias y se elimina el método viejo (el compilador avisa de lo que falte).

- **Replace Temp with Query**: `thisAmount` queda redundante y se elimina usando directamente `each.getCharge()`. Fowler prefiere eliminar temporales: provocan parámetros innecesarios y ensucian los métodos largos. Acepta que el cargo ahora se calcula dos veces: un coste de rendimiento que se optimiza mejor cuando el código está bien factorizado.

## Extraer los puntos de cliente frecuente

Se aplica lo mismo al cálculo de puntos. Con Extract Method se saca a `Rental.getFrequentRenterPoints()`, que devuelve 2 para novedad alquilada más de un día y 1 en el resto. La variable `frequentRenterPoints` tiene valor previo pero el cuerpo extraído no lo lee, así que basta con una asignación acumulativa (`+=`) sin pasarla como parámetro. Se hace extraer–compilar–probar y luego mover–compilar–probar: con pasos pequeños menos puede salir mal.

## Eliminar temporales con consultas (queries)

Las temporales `totalAmount` y `frequentRenterPoints` se reemplazan por métodos de consulta en `Customer`: `getTotalCharge()` y `getTotalFrequentRenterPoints()`, cada uno con su propio bucle sobre los alquileres. No es el caso más simple de Replace Temp with Query, porque las temporales se asignaban dentro de un bucle, así que hay que copiar el bucle a la consulta.

Esta refactorización aumenta el código (los bucles de suma en Java 1.1 requieren muchas líneas de apoyo) y ejecuta el bucle tres veces en vez de una. Fowler recalca "if" y "might": no se debe preocupar por el rendimiento al refactorizar; eso se mide y optimiza después, cuando además habrá mejores opciones. Las consultas quedan disponibles para toda la clase y evitan que otros métodos tengan que conocer los alquileres y construir bucles.

Con estas consultas listas, `htmlStatement()` se escribe fácilmente reutilizando todo el código de cálculo del recibo original, sin copiar y pegar: si cambian las reglas de cargo hay un solo lugar que tocar.

## Reemplazar la lógica condicional del precio por polimorfismo

El `switch` sobre el código de precio es un problema: es mala idea hacer un `switch` basado en un atributo de otro objeto; si debe usarse, que sea sobre los datos propios.

- **Move Method** de `getCharge` a `Movie`, pasándole `daysRented`. Fowler prefiere pasar la duración del alquiler a la película (y no el tipo al alquiler) porque los cambios previstos añaden tipos: la información de tipo es más volátil y quiere minimizar el efecto dominó. Igual se mueve `getFrequentRenterPoints` a `Movie`, manteniendo juntos en la clase del tipo los dos cálculos que varían con él.

- **Herencia y el patrón State**: parecería trabajo de subclases de `Movie`, pero una película puede cambiar de clasificación durante su vida y un objeto no puede cambiar de clase. La solución es el patrón State [Gang of Four]: una jerarquía `Price` separada a la que `Movie` delega, lo que permite cambiar el precio cuando haga falta. Fowler señala la duda State vs. Strategy: al principio lo piensa como estado de la película; si luego Strategy comunica mejor la intención, refactorizaría cambiando los nombres.

- Tres refactorizaciones encadenadas: **Replace Type Code with State/Strategy** (empezando por Self Encapsulate Field para que todo acceso al código de precio pase por getters/setters, y creando `Price` abstracta con `RegularPrice`, `ChildrensPrice`, `NewReleasePrice`), **Move Method** del `switch` a `Price`, y **Replace Conditional with Polymorphism**, convirtiendo cada rama del `switch` en un método sobreescrito en la subclase (compilar y probar tras cada rama) hasta declarar `Price.getCharge` abstracto.

- Para `getFrequentRenterPoints` no se hace abstracto el método de la superclase: se deja una implementación por defecto en `Price` (devuelve 1) y solo `NewReleasePrice` la sobreescribe.

Montar el patrón State costó esfuerzo, pero facilita mucho cambiar el comportamiento del precio, añadir precios o comportamiento dependiente del precio; el resto de la aplicación no se entera. Todos fueron pasos pequeños: nunca hubo que abrir el depurador, así que el proceso fluyó rápido.

## Reflexiones finales

El ejemplo usa Extract Method, Move Method y Replace Conditional with Polymorphism, que conducen a mejor distribución de responsabilidades y código más fácil de mantener. El resultado parece distinto del código procedural y cuesta acostumbrarse, pero luego es difícil volver atrás.

> The most important lesson from this example is the rhythm of refactoring: test, small change, test, small change (PDF p. 45).

## Ideas clave

- Refactoriza primero para hacer fácil el cambio, luego haz el cambio; un diseño pobre duele cuando hay que modificarlo, no al compilador.
- Antes de refactorizar, ten un conjunto de pruebas sólido y autoverificable que te dé seguridad.
- El ritmo es: probar, cambio pequeño, probar; con pasos pequeños los errores son fáciles de localizar.
- Un método debe estar en el objeto cuyos datos usa (Move Method); el buen código comunica su propósito, incluso en los nombres de variables.
- Elimina temporales con Replace Temp with Query; no te preocupes por el rendimiento mientras refactorizas, mídelo y optimiza después.
- Extraer los cálculos a consultas permitió reutilizarlos en `htmlStatement()` sin copiar y pegar.
- Evita hacer `switch` sobre datos de otro objeto; reemplaza la lógica condicional por polimorfismo.
- Como una película cambia de clasificación en vida, se usa el patrón State (jerarquía `Price`) en lugar de subclasear `Movie` directamente.
