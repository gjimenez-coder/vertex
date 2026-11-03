# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 16 — Refactoring SerialDate (Refactorizando SerialDate)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo es un estudio de caso práctico: el autor toma una clase real, `SerialDate`, de la librería JCommon (paquete `org.jfree.date`, escrita por David Gilbert), y la refactoriza públicamente. El autor subraya que no se trata de un acto de malicia ni de arrogancia, sino de una revisión profesional: algo que médicos, pilotos y abogados hacen, y que los programadores también deben aprender a hacer y a aceptar. Elogia a Gilbert por tener el valor y la buena voluntad de ofrecer su código abierto al escrutinio público.

`SerialDate` es una clase que representa una fecha en Java, a pesar de que ya existen `java.util.Date` y `java.util.Calendar`. El autor justifica su existencia: es una clase sobre fechas (días) en lugar de tiempos, algo que él mismo ha necesitado. La tesis central del capítulo es la secuencia "First, make it work. Then make it right": primero conseguir que el código funcione (con pruebas que lo respalden) y después limpiarlo, aplicando al final la Regla del Boy Scout —dejar el código un poco más limpio de como se encontró.

Sales sabiendo cómo encarar una refactorización disciplinada apoyada en pruebas, y verás en acción muchas de las heurísticas (smells) codificadas como `[Gn]`, `[Nn]`, `[Cn]`, `[Tn]`, `[Jn]`, `[Fn]` que el libro cataloga en el capítulo 17.

## El ejemplo que recorre el capítulo

Toda la discusión gira en torno a `SerialDate` (Listing B-1), sus pruebas originales `SerialDateTests` (Listing B-2) y las nuevas pruebas independientes del autor (Listing B-4). El resultado final es una clase renombrada `DayDate`, con sus derivadas y enums, contenido en los Listings B-7 a B-16.

## First, Make It Work (Primero, haz que funcione)

Las pruebas originales pasaban, pero no cubrían todo `[T1]`. Una búsqueda de "Find Usages" mostró que `monthCodeToQuarter` (línea 334) no se usaba `[F4]`. Con la herramienta Clover, el autor midió la cobertura: las pruebas originales ejecutaban solo 91 de 185 sentencias ejecutables (~50 %) `[T2]`.

Para entender y refactorizar la clase, escribió su propia suite de pruebas independientes, elevando la cobertura a 170 de 185 sentencias (92 %) aun con varias pruebas comentadas. Las pruebas comentadas representan comportamiento que él cree que `SerialDate` debería tener, y que irá habilitando al refactorizar.

Hallazgos y correcciones durante esta fase:
- `testWeekdayCodeToString` no debería ser sensible a mayúsculas; se arregló usando `equalsIgnoreCase` en las líneas 259 y 263 `[G2]`.
- Dejó comentadas las pruebas de "tues" y "thurs" porque no está claro que deban soportarse.
- Un bug en `getFollowingDayOfWeek` (línea 672): para el 25 de diciembre de 2004 (sábado) devolvía ese mismo día en vez del sábado siguiente (1 de enero de 2005). Es un error típico de condición de frontera `[T5]`; se corrige la línea 685 a `if (baseDOW >= targetWeekday)`.
- El historial de cambios (línea 43) revelaba que ya se habían "arreglado" bugs en estos métodos de día de la semana `[T6]`.
- En `getNearestDayOfWeek` (línea 705), el patrón de pruebas falladas mostraba que el algoritmo fallaba si el día más cercano estaba en el futuro `[T7]`. Clover confirmó que la línea 719 nunca se ejecutaba: la variable `adjust` siempre es negativa, así que el `if` de la línea 718 siempre es falso. El algoritmo estaba mal `[T8]`.
- Las pruebas de las líneas 417 y 429 se hacen pasar lanzando `IllegalArgumentException` en lugar de devolver una cadena de error.

Con estos cambios, todas las pruebas pasan y el autor considera que `SerialDate` ahora funciona.

## Then Make It Right (Después, hazlo correcto)

El autor recorre la clase de arriba abajo, corriendo todas las pruebas de JCommon tras cada cambio. Decisiones principales:

- Eliminar el historial de cambios del encabezado (reliquia de los años 60; el control de versiones ya hace esa labor) `[C1]`; conservar copyrights y licencias.
- Acortar los imports usando `java.text.*` y `java.util.*` `[J1]`.
- El Javadoc de la línea 67 mezcla cuatro lenguajes (Java, inglés, Javadoc y HTML) `[G1]`; propone envolver el comentario en `<pre>`.

Renombrado de la clase: el nombre `SerialDate` implica una implementación (un "número serial" = días desde el 30 de diciembre de 1899). El término "serial number" no es realmente correcto; "ordinal" sería más descriptivo `[N1]`. Además, al ser una clase abstracta no debería insinuar nada de la implementación, por lo que el nombre está en el nivel de abstracción equivocado `[N2]`. Descartando `Date` y `Day` por estar ya muy usados, eligió `DayDate` como compromiso.

Constantes a enums:
- `MonthConstants` se hereda solo para evitar escribir `MonthConstants.January`; es un mal truco `[J2]`. Se convierte en un enum `Month`, lo que elimina `isValidMonthCode` y la comprobación de códigos de mes `[G5]`.
- Los días se convierten en un enum `Day` `[J3]`; al crecer, se mueve a su propio archivo `[G13]`.
- `INCLUDE_NONE/FIRST/SECOND/BOTH` pasan al enum `DateInterval` (`OPEN`, `CLOSED_LEFT`, `CLOSED_RIGHT`, `CLOSED`), usando nomenclatura matemática de intervalos `[N3]`.
- La selección de semana dentro del mes pasa al enum `WeekInMonth`; la búsqueda de día de la semana al enum `WeekdayRange` (`LAST`, `NEXT`, `NEAREST`).

Ubicación de responsabilidades:
- `EARLIEST_DATE_ORDINAL`, `LATEST_DATE_ORDINAL`, `MINIMUM/MAXIMUM_YEAR_SUPPORTED` y `leapYearCount` se bajan a `SpreadsheetDate`, donde realmente se usan `[G6]`.
- Las clases base no deberían conocer a sus derivadas. Se detecta que `DayDate` crea instancias de `SpreadsheetDate` vía `createInstance` `[G7]`. Se introduce el patrón ABSTRACT FACTORY con una `DayDateFactory` (combinando SINGLETON, DECORATOR y ABSTRACT FACTORY), reemplazando `createInstance` por `makeDate` `[N1]`.
- Tablas como `AGGREGATE_DAYS_TO_END_OF_MONTH` sin uso se eliminan `[G9]`; otras se hacen privadas `[G8]` o se mueven junto a su uso `[G10]` por consistencia `[G11]`.

Limpieza de métodos:
- Se borran comentarios redundantes `[C2]`,`[C3]` y Javadocs que solo son ruido `[G12]`.
- Se elimina el `serialVersionUID` (línea 91), prefiriendo el control automático de serialización `[G4]` (decisión que algunos revisores discuten en nota al pie).
- Se eliminan los `final` de argumentos y variables por considerarlos ruido sin valor real `[G12]`, discrepando de Robert Simmons.
- `stringToWeekdayCode` y `weekdayCodeToString` se mueven al enum `Day` (como `parse` y `toString`); `monthCodeToQuarter`, `monthCodeToString` y `stringToMonthCode` huelen a FEATURE ENVY `[G14]` y se mueven al enum `Month`.
- Se evita pasar un flag que selecciona el formato de salida `[G15]`.
- Métodos como `addDays`, `addMonths`, `getPreviousDayOfWeek`, `getFollowingDayOfWeek` se convierten de estáticos a métodos de instancia `[G18]` y se aclaran con EXPLAINING TEMPORARY VARIABLES `[G19]`.
- Ambigüedad de nombres: `date.addDays(5)` podría sugerir que muta el objeto `[G20]`; se renombran a `plusDays` y `plusMonths` para romper la ambigüedad `[N4]`.

Métodos abstractos:
- `toSerial` → `toOrdinal` → finalmente `getOrdinalDay` `[N1]`.
- `toDate`, `getDayOfWeek`, `compare` y otros se "suben" a `DayDate` porque no dependen de la implementación concreta `[G6]`. Para `getDayOfWeek` se descubre una dependencia lógica implícita (el día de la semana del día 0); las dependencias lógicas incómodas `[G22]` se materializan con un método abstracto `getDayOfWeekForOrdinalZero` (que en `SpreadsheetDate` devuelve `Day.SATURDAY`).
- `compare` se renombra a `daysSince` porque no comunica suficiente `[N1]`, y se le escriben pruebas que faltaban.
- El `switch` feo de `isInRange` `[G23]` se sustituye moviendo los casos al enum `DateInterval` con un método abstracto `isIn`.

Pasada final: se actualiza el comentario de cabecera `[C2]`, se sacan los enums a sus propios archivos `[G12]`, se crea una clase `DateUtil` para variables y métodos estáticos `[G6]`, se renombra `Month.make` a `Month.fromInt` `[N1]`, se eliminan duplicaciones extrayendo `correctLastDayOfMonth` `[G5]`, y se sustituye el número mágico `1` por `Month.JANUARY.toInt()` o `Day.SUNDAY.toInt()` `[G25]`.

## Conclusion (Conclusión)

Se siguió de nuevo la Regla del Boy Scout: el código se dejó un poco más limpio de como se encontró. Curiosamente, la cobertura de `DayDate` bajó a 84,9 % (45 de 53 sentencias), no porque se pruebe menos, sino porque la clase encogió tanto que las pocas líneas no cubiertas pesan más; esas líneas son tan triviales que no merecían prueba. Costó algo de tiempo, pero valió la pena: subió la cobertura, se arreglaron bugs y el código quedó más claro y más pequeño.

## Ideas clave

- "First, make it work. Then make it right": asegura el comportamiento con pruebas antes de limpiar.
- Una revisión de código es un acto profesional, no de malicia; hay que saber darla y recibirla.
- No se puede refactorizar con confianza sin buena cobertura de pruebas; herramientas como Clover la hacen visible.
- Los nombres deben estar en el nivel de abstracción correcto y no implicar la implementación (`SerialDate` → `DayDate`).
- Las clases base no deben conocer a sus derivadas: ABSTRACT FACTORY resuelve la creación de instancias.
- Sustituir constantes enteras por enums hace el código más seguro, legible y fácil de cambiar.
- Mover cada responsabilidad a donde pertenece (FEATURE ENVY, subir/bajar métodos según sus dependencias).
- Eliminar ruido: historiales de cambios, comentarios redundantes y `final` superfluos.
- Nombrar para evitar ambigüedad de mutación (`addDays` → `plusDays`) y borrar números mágicos.
- Regla del Boy Scout: deja el código un poco más limpio que como lo encontraste.
