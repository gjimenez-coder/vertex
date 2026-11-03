# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 12 — Emergence (Emergencia)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo, escrito por Jeff Langr, plantea la idea del *diseño emergente*: ¿qué pasaría si existieran unas reglas simples que, al seguirlas mientras programas, ayudaran a que surja un buen diseño por sí solo? La tesis es que las cuatro reglas del Diseño Simple de Kent Beck (de *Extreme Programming Explained*) cumplen justo esa función y, además, empujan al programador a respetar principios como SRP y DIP.

Según Kent, un diseño es "simple" si cumple, en orden de importancia: ejecuta todas las pruebas, no contiene duplicación, expresa la intención del programador y minimiza el número de clases y métodos. El capítulo recorre cada regla mostrando cómo, en conjunto, producen baja acoplamiento, alta cohesión y código mantenible.

Sales sabiendo que el diseño limpio no nace de un gran plan previo sino de ciclos cortos de escritura y refactorización apoyados en pruebas. Las reglas no sustituyen la experiencia, pero son una forma cristalizada de décadas de experiencia que acelera la adopción de buenos principios y patrones.

## Simple Design Rule 1: Runs All the Tests (Ejecuta todas las pruebas)

Un diseño debe producir un sistema que funcione como se pretende. Un sistema no verificable no debería desplegarse: "a system that cannot be verified should never be deployed" (PDF p. 203).

Hacer que el sistema sea testeable empuja el diseño hacia clases pequeñas y de un solo propósito, porque es más fácil probar clases que respetan el SRP. Cuantas más pruebas escribimos, más tendemos hacia lo simple de probar. Además, el acoplamiento fuerte dificulta escribir pruebas, así que escribir más pruebas nos lleva a usar DIP, inyección de dependencias, interfaces y abstracción para minimizar el acoplamiento. Una regla tan obvia como tener pruebas y ejecutarlas de forma continua termina mejorando la adhesión del sistema a las metas OO de bajo acoplamiento y alta cohesión.

## Simple Design Rules 2–4: Refactoring (Refactorización)

Con las pruebas en su sitio, podemos mantener el código limpio refactorizando de forma incremental. Tras añadir unas pocas líneas, hacemos una pausa y reflexionamos: ¿degradamos el diseño? Si fue así, lo limpiamos y ejecutamos las pruebas para demostrar que nada se rompió. Tener pruebas elimina el miedo a que limpiar el código lo rompa.

En este paso de refactorización se aplica todo el cuerpo de conocimiento sobre buen diseño: aumentar cohesión, reducir acoplamiento, separar responsabilidades, modularizar, encoger funciones y clases, elegir mejores nombres. Aquí también se aplican las tres últimas reglas: eliminar duplicación, asegurar expresividad y minimizar clases y métodos.

## No Duplication (Sin duplicación)

La duplicación es el enemigo principal de un sistema bien diseñado: representa trabajo, riesgo y complejidad innecesaria. Aparece en muchas formas: líneas idénticas, líneas similares que pueden acercarse para refactorizarlas, o duplicación de implementación. Por ejemplo, `isEmpty()` puede atarse a la definición de `size()`:

```java
boolean isEmpty() {
   return 0 == size();
}
```

El capítulo muestra cómo extraer un método privado `replaceImage` compartido entre `scaleToOneDimension` y `rotate`, eliminando las líneas repetidas (`image.dispose()`, `System.gc()`, `image = newImage`). Al extraer lo común a este nivel mínimo empezamos a reconocer violaciones de SRP y a mover métodos a otras clases, lo que eleva su visibilidad. Esta "reutilización en lo pequeño" puede reducir drásticamente la complejidad del sistema y es esencial para lograr la reutilización en lo grande.

El patrón TEMPLATE METHOD (de *Design Patterns*, GOF) sirve para eliminar duplicación de nivel más alto. En el ejemplo de `VacationPolicy`, los métodos para la división de EE. UU. y la de la UE son casi iguales salvo el cálculo de mínimos legales. Se refactoriza a una clase abstracta con `accrueVacation()` que llama a `calculateBaseVacationHours()`, `alterForLegalMinimums()` (abstracto) y `applyToPayroll()`; las subclases `USVacationPolicy` y `EUVacationPolicy` rellenan solo el "hueco" que varía.

## Expressive (Expresivo)

La mayor parte del costo de un proyecto de software está en el mantenimiento a largo plazo. Como quien mantiene el código no tendrá nuestra comprensión profunda del problema, el código debe expresar claramente la intención de su autor; cuanto más claro, menos tiempo gastarán otros en entenderlo, lo que reduce defectos y costo.

Formas de expresarse:
- Elegir buenos nombres: oír el nombre de una clase o función y no sorprenderse al descubrir sus responsabilidades.
- Mantener funciones y clases pequeñas: son fáciles de nombrar, escribir y entender.
- Usar nomenclatura estándar: los nombres de patrones de diseño (COMMAND, VISITOR) comunican el diseño de forma concisa.
- Escribir pruebas unitarias bien hechas: funcionan como documentación por ejemplo.

Pero la forma más importante de ser expresivo es *intentarlo*. A menudo dejamos el código funcionando y pasamos al siguiente problema sin pensar en el siguiente lector, que probablemente seremos nosotros mismos. Hay que tener orgullo del oficio y dedicar un poco de tiempo a cada función y clase: mejores nombres, dividir funciones grandes. "Care is a precious resource" (PDF p. 207).

## Minimal Classes and Methods (Clases y métodos mínimos)

Incluso la eliminación de duplicación, la expresividad y el SRP pueden llevarse demasiado lejos y producir demasiadas clases y métodos diminutos. Esta regla sugiere mantener bajo el conteo de funciones y clases.

Los conteos altos suelen venir de dogmatismo sin sentido: por ejemplo, un estándar que exige una interfaz para cada clase, o separar siempre datos y comportamiento en clases distintas. Hay que resistir ese dogma y adoptar un enfoque pragmático. El objetivo es mantener pequeño el sistema global sin dejar de mantener pequeñas funciones y clases. Esta regla es la de menor prioridad de las cuatro: importa más tener pruebas, eliminar duplicación y expresarse.

## Conclusión

¿Puede un conjunto de prácticas simples reemplazar la experiencia? Claramente no. Pero las prácticas de este capítulo y del libro son una forma cristalizada de décadas de experiencia de los autores. Seguir el diseño simple fomenta y permite que los desarrolladores adhieran a buenos principios y patrones que, de otro modo, tardarían años en aprender.

## Ideas clave

- Las cuatro reglas del Diseño Simple de Kent Beck, en orden de importancia: ejecutar todas las pruebas, sin duplicación, expresividad, y mínimo de clases y métodos.
- Hacer el sistema testeable empuja hacia clases pequeñas (SRP) y bajo acoplamiento (DIP, inyección de dependencias).
- La refactorización incremental y continua, respaldada por pruebas, elimina el miedo a romper el código.
- La duplicación es el enemigo principal del diseño; eliminarla incluso en pocas líneas revela violaciones de SRP.
- La "reutilización en lo pequeño" reduce la complejidad y habilita la reutilización en lo grande.
- TEMPLATE METHOD elimina duplicación de alto nivel dejando que las subclases rellenen solo lo que varía.
- El código expresivo (buenos nombres, funciones pequeñas, nomenclatura estándar, pruebas claras) abarata el mantenimiento.
- No llevar las reglas al extremo: evita el dogmatismo que multiplica clases y métodos innecesarios.
