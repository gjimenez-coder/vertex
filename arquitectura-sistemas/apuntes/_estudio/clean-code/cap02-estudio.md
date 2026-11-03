# Meaningful Names (Nombres significativos) — Estudio

## Tarjetas de repaso

P: ¿Qué debe revelar un buen nombre según la tesis central del capítulo? / R: Su intención: por qué existe algo, qué hace y cómo se usa; si necesita un comentario para entenderse, no revela su intención.

P: ¿Por qué `int d; // elapsed time in days` es un mal nombre? / R: Porque no evoca nada; es mejor `elapsedTimeInDays`, `daysSinceCreation` o `fileAgeInDays`, que especifican qué se mide y en qué unidad.

P: ¿Qué es evitar desinformación? / R: No usar palabras cuyo significado asentado difiera del pretendido (como `hp`, `aix`, `sco`), ni llamar `accountList` a lo que no es una `List`, ni usar `l`/`O` que se confunden con `1`/`0`.

P: ¿Qué diferencia una distinción significativa de una noninformativa? / R: Las series numéricas (`a1`, `a2`) y las *noise words* (`Info`, `Data`, `variable`, `the`) no aportan distinción real; `source`/`destination` sí, frente a `a1`/`a2`.

P: ¿Por qué importan los nombres pronunciables? / R: La programación es una actividad social; si no puedes pronunciar un nombre no puedes discutirlo. `generationTimestamp` permite conversar; `genymdhms` no.

P: ¿Qué hace que un nombre sea buscable? / R: Que se pueda localizar con `grep`; constantes como `MAX_CLASSES_PER_STUDENT` o `WORK_DAYS_PER_WEEK` son buscables, pero el número `7` o la letra `e` no.

P: ¿Cómo debe relacionarse la longitud de un nombre con su alcance? / R: La longitud debe corresponder al tamaño de su alcance; los nombres de una sola letra solo deberían usarse como variables locales en métodos cortos.

P: ¿Por qué se deben evitar las codificaciones como la Hungarian Notation o `m_`? / R: Añaden carga de descifrado y dificultan cambiar nombre o tipo; las clases pequeñas y el entorno hacen innecesarios los prefijos de miembro.

P: ¿Qué convención prefiere el autor para interfaces e implementaciones? / R: Dejar la interfaz sin adornos: `ShapeFactory` (interfaz) y `ShapeFactoryImp`, en lugar de `IShapeFactory`.

P: ¿Cómo deben nombrarse las clases y los métodos? / R: Las clases con sustantivos o frases nominales (`Customer`, `AddressParser`), evitando `Manager`/`Processor`/`Data`; los métodos con verbos o frases verbales (`postPayment`, `deletePage`).

P: ¿Qué prefijos siguen los accessors, mutators y predicados, y qué hacer al sobrecargar constructores? / R: Se prefijan con `get`, `set`, `is` según el estándar JavaBean; al sobrecargar constructores se usan métodos factoría estáticos descriptivos (`Complex.FromRealNumber(23.0)`).

P: ¿Qué significa "Don't Be Cute"? / R: Elegir claridad sobre ingenio: `DeleteItems` mejor que `HolyHandGrenade`; no usar `whack()` por `kill()` ni `eatMyShorts()` por `abort()`.

P: ¿Qué son "Pick One Word per Concept" y "Don't Pun"? / R: Usar una sola palabra por concepto abstracto y mantenerla (no mezclar `fetch`/`retrieve`/`get`), y no usar la misma palabra para dos propósitos distintos (usar `insert`/`append` en vez de reutilizar `add`).

P: ¿Cuándo usar nombres del dominio de solución y del dominio del problema? / R: Términos de ciencias de la computación, algoritmos y patrones (`AccountVisitor`, `JobQueue`) cuando el lector los conoce; el nombre del dominio del problema cuando no existe término técnico.

P: ¿Cómo se añade contexto significativo sin excederse? / R: Con una clase (`Address`, `GuessStatisticsMessage`) o prefijos (`addrState`) cuando falta contexto, pero sin contexto gratuito como prefijar todo con `GSD`; los nombres cortos y claros son mejores.

## Preguntas de autoevaluación

P: En el ejemplo del buscaminas, ¿cuál es el verdadero problema del método `getThem()` y cómo se resuelve? / R: El problema no es la complejidad sino la implicitud: el lector debe saber qué contiene `theList`, qué significa el subíndice cero y qué representa el `4`. Se resuelve dando nombres (`gameBoard`, `STATUS_VALUE`, `FLAGGED`) y, un paso más allá, con una clase `Cell` y un método `isFlagged()`. (Sección "El ejemplo que recorre el capítulo")

P: ¿Por qué `accountList` puede ser un mal nombre aunque describa un grupo de cuentas? / R: Porque induce a desinformación si la agrupación no es realmente una `List`; es mejor `accountGroup`, `bunchOfAccounts` o `accounts`. (Sección "Avoid Disinformation")

P: ¿Por qué `getActiveAccount()`, `getActiveAccounts()` y `getActiveAccountInfo()` son problemáticos? / R: Porque no hacen distinciones significativas: `Info` es una *noise word* y el programador queda sin saber cuál método llamar. (Sección "Make Meaningful Distinctions")

P: ¿Qué quiere decir "la claridad es el rey" y qué distingue a un programador profesional? / R: Que el lector no debería tener que traducir mentalmente los nombres; el profesional entiende que la claridad manda y escribe código que otros entienden. (Sección "Avoid Mental Mapping")

P: ¿Por qué dejar de usar un nombre que ya no encaja genera miedo y cómo lo aborda el capítulo? / R: La gente teme renombrar por miedo a objeciones ajenas, pero las herramientas modernas manejan los detalles y conviene renombrar para mejorar. (Sección "Final Words")

P: ¿Qué papel juega el número `4` como número mágico en el ejemplo y qué lo elimina? / R: Es un valor sin contexto; nombrarlo (`FLAGGED`, `STATUS_VALUE`) y encapsularlo en `cell.isFlagged()` lo oculta y lo hace explícito. (Sección "El ejemplo que recorre el capítulo")

P: ¿Por qué el capítulo afirma que la dificultad de nombrar es más de enseñanza que técnica? / R: Porque elegir buenos nombres requiere habilidad descriptiva y un trasfondo cultural compartido; es un asunto de enseñanza. (Sección "Final Words")

## Puntos a dominar

- Distinguir cuándo un nombre revela intención y cuándo requiere un comentario que delata su fallo.
- Reconocer desinformación: significados asentados distintos, nombres casi idénticos y caracteres confundibles (`l`/`O`).
- Diferenciar distinciones significativas de series numéricas y *noise words*.
- Evaluar si un nombre es pronunciable y buscable, y ajustar su longitud al tamaño del alcance.
- Identificar y evitar codificaciones (Hungarian Notation, `m_`, `I` de interfaz) y el mapeo mental.
- Aplicar la convención sustantivo para clases y verbo con `get`/`set`/`is` para métodos, y factorías estáticas al sobrecargar constructores.
- Mantener una palabra por concepto, evitar *puns* y preferir claridad sobre ingenio.
- Añadir contexto mediante clases o prefijos sin caer en contexto gratuito.
