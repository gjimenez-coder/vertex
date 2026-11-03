# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 2 — Meaningful Names (Nombres significativos)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Los nombres están en todas partes del software: variables, funciones, argumentos, clases, paquetes, archivos y directorios. Dado que nombramos tanto, conviene hacerlo bien. El capítulo (escrito por Tim Ottinger) reúne reglas simples para crear buenos nombres y demuestra, con ejemplos de código, cuánto mejora la legibilidad al aplicarlas.

La tesis central es que un buen nombre debe revelar la intención: por qué existe algo, qué hace y cómo se usa. Si un nombre necesita un comentario para entenderse, entonces no revela su intención. Elegir buenos nombres cuesta tiempo, pero ahorra más del que cuesta, y conviene cambiarlos cuando se encuentran mejores.

Sales sabiendo un catálogo de reglas aplicables: usar nombres que revelan intención, evitar desinformación, hacer distinciones significativas, usar nombres pronunciables y buscables, evitar codificaciones (Hungarian Notation, prefijos de miembro), evitar el mapeo mental, nombrar clases y métodos correctamente, no ser "cuteness", elegir una palabra por concepto, no hacer juegos de palabras (puns), usar nombres del dominio de solución y del dominio del problema, y añadir contexto significativo sin excederse. La dificultad real es más un asunto de enseñanza y de habilidad descriptiva que técnico.

## El ejemplo que recorre el capítulo

Un fragmento del juego buscaminas ilustra el poder de nombrar con intención. El código original devuelve una lista sin contexto explícito:

```java
public List<int[]> getThem() {
  List<int[]> list1 = new ArrayList<int[]>();
  for (int[] x : theList)
    if (x[0] == 4)
      list1.add(x);
  return list1;
}
```

El problema no es la complejidad sino la *implicitud*: el lector debe conocer qué contiene `theList`, qué significa el subíndice cero y qué representa el valor `4`. Al dar nombres (`gameBoard`, `STATUS_VALUE`, `FLAGGED`) el código se vuelve explícito sin cambiar su estructura, y un paso más con una clase `Cell` y un método `isFlagged()` oculta los números mágicos:

```java
public List<Cell> getFlaggedCells() {
  List<Cell> flaggedCells = new ArrayList<Cell>();
  for (Cell cell : gameBoard)
    if (cell.isFlagged())
      flaggedCells.add(cell);
  return flaggedCells;
}
```

## Use Intention-Revealing Names

El nombre de una variable, función o clase debe responder las grandes preguntas: por qué existe, qué hace y cómo se usa. `int d; // elapsed time in days` no evoca nada; mejor `elapsedTimeInDays`, `daysSinceCreation`, `fileAgeInDays`, que especifican qué se mide y en qué unidad.

## Avoid Disinformation

Hay que evitar pistas falsas. No usar palabras cuyo significado asentado difiera del pretendido: `hp`, `aix`, `sco` son malos nombres porque son plataformas Unix. No llamar `accountList` a una agrupación que no es realmente una `List`; mejor `accountGroup`, `bunchOfAccounts` o `accounts`. Cuidado con nombres que varían en pequeños detalles (`XYZControllerForEfficientHandlingOfStrings` frente a `...StorageOfStrings`). Escribir conceptos similares de forma similar es información; escribirlos de forma inconsistente es desinformación. Ejemplo temible: usar la `l` minúscula y la `O` mayúscula, que se confunden con `1` y `0`.

## Make Meaningful Distinctions

No basta con cambiar un nombre de forma arbitraria para satisfacer al compilador. El nombre por serie numérica (`a1`, `a2`, … `aN`) no es desinformativo pero sí *noninformativo*: `copyChars(char a1[], char a2[])` se lee mejor con `source` y `destination`. Las *noise words* (palabras de ruido) como `Info`, `Data`, `a`, `an`, `the` no aportan distinción real: `ProductInfo` o `ProductData` no se distinguen de `Product`. La palabra `variable` no debe aparecer en un nombre de variable, ni `table` en un nombre de tabla. `getActiveAccount()`, `getActiveAccounts()`, `getActiveAccountInfo()` dejan al programador sin saber cuál llamar.

## Use Pronounceable Names

Los humanos manejan bien las palabras, y las palabras son pronunciables. Si no puedes pronunciar un nombre, no puedes discutirlo sin sonar ridículo, y la programación es una actividad social. Comparar `genymdhms`/`DtaRcrd102`/`pszqint` con `generationTimestamp`/`Customer`/`recordId`: solo con lo segundo es posible una conversación inteligente.

## Use Searchable Names

Los nombres de una sola letra y las constantes numéricas son difíciles de localizar en un cuerpo de texto. Es fácil hacer `grep` de `MAX_CLASSES_PER_STUDENT`, pero no del número `7` ni de la letra `e` (la más común del inglés). La longitud de un nombre debe corresponder al tamaño de su alcance: los nombres de una sola letra solo deberían usarse como variables locales en métodos cortos. Es preferible `WORK_DAYS_PER_WEEK` a buscar todos los lugares donde aparece `5`.

## Avoid Encodings

Codificar el tipo o el alcance en el nombre añade una carga de descifrado. La *Hungarian Notation* y los prefijos de tipo eran necesarios en lenguajes antiguos sin comprobación de tipos, pero hoy son impedimentos: dificultan cambiar el nombre o el tipo (`PhoneNumber phoneString;` quedó sin actualizar). Tampoco hacen falta prefijos de miembro como `m_`: las clases deben ser pequeñas y el entorno resalta los miembros. Para interfaces e implementaciones, el autor prefiere dejar la interfaz sin adornos: mejor `ShapeFactory` (interfaz) y `ShapeFactoryImp` que `IShapeFactory`.

## Avoid Mental Mapping

El lector no debería traducir mentalmente tus nombres a otros que ya conoce. Un contador de bucle puede llamarse `i`, `j` o `k` (nunca `l`) en alcances muy pequeños, pero en otros contextos una sola letra es un marcador que obliga a mapear. La diferencia entre un programador listo y uno profesional es que el profesional entiende que *la claridad es el rey* y escribe código que otros entienden.

## Class Names y Method Names

Las clases y objetos deben tener nombres de sustantivo o frase nominal (`Customer`, `WikiPage`, `Account`, `AddressParser`); hay que evitar `Manager`, `Processor`, `Data`, `Info`, y una clase nunca debe ser un verbo. Los métodos deben tener nombres de verbo o frase verbal (`postPayment`, `deletePage`, `save`). Los accessors, mutators y predicados se prefijan con `get`, `set`, `is` según el estándar JavaBean. Al sobrecargar constructores, usar métodos factoría estáticos que describan los argumentos (`Complex.FromRealNumber(23.0)`).

## Don't Be Cute

Si los nombres son demasiado ingeniosos, solo los recordará quien comparta el sentido del humor del autor. Elegir claridad sobre valor de entretenimiento: `DeleteItems` mejor que `HolyHandGrenade`; no usar `whack()` por `kill()` ni `eatMyShorts()` por `abort()`. Di lo que quieres decir y quiere decir lo que dices.

## Pick One Word per Concept y Don't Pun

Elegir una palabra por cada concepto abstracto y mantenerla: es confuso tener `fetch`, `retrieve` y `get` como equivalentes en distintas clases, o mezclar `controller`, `manager` y `driver`. Un léxico consistente es una gran ayuda. A la inversa, no hacer *puns*: no usar la misma palabra para dos propósitos distintos. Si tienes muchos `add` que concatenan valores y ahora un método mete un parámetro en una colección, llámalo `insert` o `append`, no `add`.

## Use Solution/Problem Domain Names

Como el código lo leen programadores, está bien usar términos de ciencias de la computación, nombres de algoritmos y de patrones (`AccountVisitor` para quien conoce el patrón VISITOR, `JobQueue`). Cuando no existe un término técnico, usar el nombre del dominio del problema, para que quien mantenga el código pueda preguntar a un experto del dominio. Separar los conceptos de ambos dominios es parte del trabajo de un buen diseñador.

## Add Meaningful Context / Don't Add Gratuitous Context

Pocos nombres son significativos por sí solos. Variables como `firstName`, `lastName`, `street`, `state`, `zipcode` juntas sugieren una dirección, pero `state` por sí sola no. Se puede añadir contexto con prefijos (`addrState`) o, mejor, con una clase `Address`. En el ejemplo de `printGuessStatistics`, extraer `number`, `verb` y `pluralModifier` a una clase `GuessStatisticsMessage` da contexto claro y permite dividir el método en funciones más pequeñas. Pero no añadir contexto gratuito: prefijar toda clase con `GSD` trabaja contra las herramientas; `GSDAccountAddress` tiene 10 de 17 caracteres redundantes. Los nombres cortos son mejores que los largos mientras sean claros.

## Final Words

Lo más difícil de elegir buenos nombres es que requiere habilidad descriptiva y un trasfondo cultural compartido; es un asunto de enseñanza. La gente teme renombrar por miedo a objeciones ajenas, pero las herramientas modernas manejan los detalles y conviene renombrar para mejorar. El objetivo es que el código se lea como párrafos y frases.

## Ideas clave

- El nombre debe revelar su intención: por qué existe, qué hace y cómo se usa; si requiere un comentario, no la revela.
- Evitar desinformación: no usar términos con significado asentado distinto, ni nombres casi idénticos, ni `l`/`O`.
- Las distinciones deben significar algo: evitar series numéricas y *noise words* (`Info`, `Data`, `variable`).
- Usar nombres pronunciables y buscables; la longitud del nombre debe ajustarse al tamaño de su alcance.
- Evitar codificaciones (Hungarian Notation, prefijos `m_`, `I` de interfaz) y el mapeo mental; la claridad es el rey.
- Clases = sustantivos; métodos = verbos con prefijos `get`/`set`/`is`; usar factorías estáticas al sobrecargar constructores.
- Una palabra por concepto y nada de *puns*; preferir claridad sobre ingenio.
- Añadir contexto con clases o prefijos cuando falta, pero sin contexto gratuito; nombres cortos y claros.
