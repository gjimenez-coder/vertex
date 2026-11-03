# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 9 — Unit Tests (Pruebas unitarias)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo defiende que el código de prueba es tan importante como el código de producción: no es un ciudadano de segunda clase y debe mantenerse tan limpio como el código que verifica. Martin arranca recordando cómo se probaba antes (programas desechables, ad hoc) frente a la disciplina actual impulsada por Agile y TDD, y advierte que muchos programadores, en la prisa por sumar pruebas, se han saltado los puntos sutiles de escribir buenas pruebas.

La tesis central es que las pruebas unitarias automatizadas y limpias son lo que mantiene el código de producción flexible, mantenible y reutilizable: habilitan el cambio. Si pierdes las pruebas (o las dejas sucias), pierdes la capacidad de cambiar el código sin miedo, y tanto las pruebas como la producción terminan pudriéndose.

Sales sabiendo: las Tres Leyes de TDD, por qué mantener las pruebas limpias, cómo hacerlas legibles con un lenguaje de pruebas específico del dominio, la idea de un doble estándar de ingeniería para el código de prueba, las reglas de un assert / un concepto por prueba y el acrónimo F.I.R.S.T.

## El ejemplo que recorre el capítulo

Dos casos hilan el capítulo. El primero son los tests de `SerializedPageResponderTest` de FitNesse: el Listing 9-1 muestra tres pruebas cargadas de detalle (llamadas repetidas a `addPage` y `assertSubString`, `PathParser`, construcción del request) y el Listing 9-2 las refactoriza a una forma limpia y expresiva. El segundo es `EnvironmentControllerTest`, un sistema de control ambiental donde se pasa de aserciones una a una (Listing 9-3) a un estado codificado en una cadena (`assertEquals("HBchL", hw.getState())`, Listing 9-4/9-5).

## Las Tres Leyes de TDD

TDD pide escribir las pruebas antes que el código de producción, pero eso es solo la punta del iceberg. Las tres leyes son:

- Primera: no puedes escribir código de producción hasta haber escrito una prueba unitaria que falle.
- Segunda: no puedes escribir más de una prueba unitaria de lo suficiente para que falle, y no compilar es fallar.
- Tercera: no puedes escribir más código de producción del suficiente para pasar la prueba que falla actualmente.

Estas leyes te encierran en un ciclo de unos treinta segundos. Trabajando así se escriben docenas de pruebas al día, miles al año, que cubren casi todo el código de producción; su volumen puede rivalizar con el del propio código y suponer un problema de gestión.

## Keeping Tests Clean (Mantener las pruebas limpias)

Martin relata un equipo que decidió no mantener su código de prueba al mismo estándar de calidad: "quick and dirty" era la consigna. No entendieron que tener pruebas sucias equivale, o es peor, que no tener pruebas. Las pruebas deben cambiar al evolucionar la producción; cuanto más enredadas, más difíciles de cambiar. El coste de mantener la suite subió release tras release hasta que la descartaron. Sin ella perdieron la capacidad de verificar cambios, subió la tasa de defectos, dejaron de limpiar el código por miedo y la producción se pudrió. Moraleja: el código de prueba es tan importante como el de producción y requiere diseño y cuidado.

## Tests Enable the -ilities (Las pruebas habilitan las "-ilidades")

Si no mantienes limpias tus pruebas, las perderás, y con ellas lo que mantiene flexible el código de producción. Son las pruebas unitarias las que mantienen el código flexible, mantenible y reutilizable, porque si tienes pruebas no temes cambiar el código. Cuanta más cobertura, menos miedo: puedes mejorar una arquitectura y un diseño mediocres sin temor. Las pruebas habilitan todas las "-ilities" porque habilitan el cambio; si están sucias, se merma tu capacidad de mejorar la estructura del código.

## Clean Tests (Pruebas limpias)

¿Qué hace limpia una prueba? Tres cosas: legibilidad, legibilidad y legibilidad. Lo mismo que hace legible cualquier código: claridad, simplicidad y densidad de expresión; decir mucho con las menos expresiones posibles. El Listing 9-1 falla por duplicación [G5] y por detalles que estorban la expresividad (`PathParser`, creación del responder, construcción del URL). El Listing 9-2 refactorizado hace exactamente lo mismo pero deja claro el patrón BUILD-OPERATE-CHECK: una parte construye los datos de prueba, otra opera sobre ellos y otra comprueba el resultado esperado.

## Domain-Specific Testing Language (Lenguaje de pruebas específico del dominio)

En lugar de usar las APIs normales del sistema, se construye un conjunto de funciones y utilidades que las envuelven y hacen las pruebas más fáciles de escribir y leer. Esa API especializada es un lenguaje de pruebas. No se diseña por adelantado: evoluciona del refactoring continuo del código de prueba que se ha contaminado con detalle que oscurece.

## A Dual Standard (Un doble estándar)

El código de la API de pruebas tiene un conjunto de estándares de ingeniería distinto al del código de producción. Debe seguir siendo simple, sucinto y expresivo, pero no necesita ser tan eficiente, porque corre en un entorno de prueba, no de producción. En `getState()` (Listing 9-6) se concatenan Strings en vez de usar un `StringBuffer`; en un sistema embebido de tiempo real con recursos limitados importaría, pero el entorno de prueba no suele estar limitado. Hay cosas que nunca harías en producción y están bien en pruebas —normalmente sobre memoria o CPU— pero nunca afectan a la limpieza.

## One Assert per Test (Un assert por prueba)

Una corriente sostiene que cada función de prueba debería tener un único `assert`. La regla parece draconiana, pero aporta una conclusión rápida de entender (Listing 9-5). El Listing 9-7 divide una prueba en dos, cada una con su aserción, usando la convención given-when-then; el inconveniente es la duplicación, que podría eliminarse con el patrón TEMPLATE METHOD o con `@Before`, aunque a veces es demasiado mecanismo para un problema menor. Martin considera la regla una buena guía, pero no teme poner más de un assert: lo mejor es minimizar el número de asserts por prueba.

## Single Concept per Test (Un concepto por prueba)

Quizá mejor regla: probar un único concepto por función de prueba. El Listing 9-8 (`testAddMonths`) mezcla tres cosas independientes y debería dividirse; al enunciarlo así aflora una regla general (al incrementar el mes, el día no puede superar el último del mes) y se detecta una prueba faltante (febrero 28 → marzo 28). El problema no son los múltiples asserts por sección, sino probar más de un concepto. Conclusión: minimizar los asserts por concepto y probar un solo concepto por función.

## F.I.R.S.T.

Las pruebas limpias siguen cinco reglas:

- Fast (Rápidas): deben correr rápido; si son lentas no las ejecutarás con frecuencia y no encontrarás problemas a tiempo.
- Independent (Independientes): no deben depender unas de otras; deben poder ejecutarse en cualquier orden, para que un fallo no cause una cascada.
- Repeatable (Repetibles): deben poder ejecutarse en cualquier entorno (producción, QA, tu portátil sin red).
- Self-Validating (Autovalidantes): deben dar una salida booleana, pasan o fallan; nada de leer logs o comparar ficheros a mano.
- Timely (Oportunas): escritas justo antes del código de producción que las hace pasar; escritas después, el código puede resultar difícil de probar.

## Ideas clave

- El código de prueba es tan importante como el de producción; no es un ciudadano de segunda clase.
- Las Tres Leyes de TDD encierran en un ciclo de ~30 segundos donde prueba y producción se escriben juntas.
- Pruebas sucias equivalen a, o son peores que, no tener pruebas: cuanto más enredadas, más difíciles de mantener.
- Las pruebas unitarias habilitan las "-ilities" (flexibilidad, mantenibilidad, reusabilidad) porque habilitan el cambio sin miedo.
- La clave de una prueba limpia es la legibilidad; el patrón BUILD-OPERATE-CHECK la hace evidente.
- Conviene construir un lenguaje de pruebas específico del dominio, que evoluciona por refactoring.
- Rige un doble estándar: la API de pruebas puede ser menos eficiente, pero nunca menos limpia.
- Minimiza asserts por prueba, prueba un solo concepto por función y cumple F.I.R.S.T.
