# Refactoring SerialDate (Refactorizando SerialDate) — Estudio

## Tarjetas de repaso

P: ¿Qué clase refactoriza este capítulo y de dónde proviene?
R: `SerialDate`, de la librería JCommon (paquete `org.jfree.date`), escrita por David Gilbert.

P: ¿Cuál es la secuencia que resume la tesis del capítulo?
R: "First, make it work. Then make it right": primero conseguir que funcione con pruebas, y después limpiarlo.

P: ¿Cómo justifica el autor la existencia de `SerialDate` pese a `java.util.Date` y `java.util.Calendar`?
R: Es una clase sobre fechas (días) en lugar de tiempos, algo que él mismo ha necesitado.

P: ¿Qué cobertura ejecutaban las pruebas originales según Clover?
R: 91 de 185 sentencias ejecutables (~50 %).

P: ¿A cuánto subió la cobertura con la suite de pruebas independientes del autor?
R: A 170 de 185 sentencias (92 %), aun con varias pruebas comentadas.

P: ¿Qué representan las pruebas que el autor dejó comentadas?
R: Comportamiento que él cree que `SerialDate` debería tener, y que irá habilitando al refactorizar.

P: ¿Qué bug tenía `getFollowingDayOfWeek` y cómo se corrigió?
R: Para el 25 de diciembre de 2004 devolvía ese mismo día en vez del sábado siguiente; se corrige la línea 685 a `if (baseDOW >= targetWeekday)`.

P: ¿Por qué se renombró `SerialDate` a `DayDate`?
R: "SerialDate" implica implementación y está en el nivel de abstracción equivocado; descartados `Date` y `Day`, `DayDate` fue el compromiso.

P: ¿Qué patrón se introduce para que la clase base no conozca a sus derivadas?
R: ABSTRACT FACTORY con una `DayDateFactory` (combinando SINGLETON, DECORATOR y ABSTRACT FACTORY), reemplazando `createInstance` por `makeDate`.

P: ¿En qué enums se convirtieron las constantes enteras del original?
R: `Month`, `Day`, `DateInterval`, `WeekInMonth` y `WeekdayRange`.

P: ¿Por qué se renombraron `addDays`/`addMonths` a `plusDays`/`plusMonths`?
R: Para romper la ambigüedad de que `date.addDays(5)` pudiera sugerir que muta el objeto.

P: ¿Qué es FEATURE ENVY en este capítulo y qué métodos lo mostraban?
R: Métodos que pertenecen a otra clase; `monthCodeToQuarter`, `monthCodeToString` y `stringToMonthCode` se movieron al enum `Month`.

P: ¿Por qué bajó la cobertura de `DayDate` a 84,9 % en la conclusión?
R: No porque se pruebe menos, sino porque la clase encogió tanto que las pocas líneas no cubiertas pesan más; son triviales.

P: ¿Qué es la Regla del Boy Scout aplicada aquí?
R: Dejar el código un poco más limpio de como se encontró.

## Preguntas de autoevaluación

P: ¿Por qué el autor sostiene que refactorizar `SerialDate` no es un acto de malicia ni arrogancia?
R: Porque una revisión de código es un acto profesional, como el que hacen médicos, pilotos y abogados; elogia a Gilbert por ofrecer su código al escrutinio público. (Sección "Lo que necesitas saber".)

P: ¿Qué papel juegan las pruebas y la herramienta Clover en la fase "First, Make It Work"?
R: No se puede refactorizar con confianza sin buena cobertura; Clover mide y hace visible qué sentencias se ejecutan, revelando código muerto y algoritmos erróneos. (Sección "First, Make It Work".)

P: ¿Cómo se detectó que el algoritmo de `getNearestDayOfWeek` estaba mal?
R: El patrón de pruebas falladas mostró fallos cuando el día más cercano estaba en el futuro; Clover confirmó que la línea 719 nunca se ejecutaba porque `adjust` siempre era negativa. (Sección "First, Make It Work".)

P: ¿Por qué se elimina el historial de cambios del encabezado de la clase?
R: Es una reliquia de los años 60; el control de versiones ya hace esa labor. Se conservan copyrights y licencias. (Sección "Then Make It Right".)

P: ¿Qué ventajas aporta convertir constantes enteras en enums?
R: Hace el código más seguro, legible y fácil de cambiar; por ejemplo, el enum `Month` elimina `isValidMonthCode` y la comprobación de códigos de mes. (Sección "Then Make It Right" / "Ideas clave".)

P: ¿Qué criterio se usa para "subir" o "bajar" métodos y datos entre `DayDate` y `SpreadsheetDate`?
R: Cada responsabilidad va donde pertenece según sus dependencias: lo que no depende de la implementación sube a `DayDate`; lo que sí (como `EARLIEST_DATE_ORDINAL`) baja a `SpreadsheetDate`. (Sección "Then Make It Right".)

P: ¿Cómo se resolvió el `switch` feo de `isInRange`?
R: Moviendo los casos al enum `DateInterval` con un método abstracto `isIn`. (Sección "Then Make It Right".)

P: ¿Valió la pena la refactorización según la conclusión, y por qué?
R: Sí; costó algo de tiempo pero subió la cobertura, se arreglaron bugs y el código quedó más claro y más pequeño. (Sección "Conclusion".)

## Checklist

- Asegurar el comportamiento con una suite de pruebas antes de limpiar ("make it work" primero).
- Medir la cobertura con una herramienta (Clover) para localizar código no ejecutado y algoritmos erróneos.
- Correr todas las pruebas tras cada cambio durante la fase de limpieza.
- Corregir bugs de condición de frontera detectados por pruebas (p. ej. `getFollowingDayOfWeek`, `getNearestDayOfWeek`).
- Renombrar al nivel de abstracción correcto, sin implicar la implementación (`SerialDate` → `DayDate`).
- Sustituir constantes enteras por enums (`Month`, `Day`, `DateInterval`, `WeekInMonth`, `WeekdayRange`).
- Aplicar ABSTRACT FACTORY para que la clase base no conozca a sus derivadas (`DayDateFactory`, `makeDate`).
- Mover cada responsabilidad a donde pertenece y eliminar FEATURE ENVY.
- Eliminar ruido: historial de cambios, comentarios redundantes, `final` superfluos y tablas sin uso.
- Nombrar para evitar ambigüedad de mutación (`addDays` → `plusDays`) y sustituir números mágicos por constantes nombradas.
- Dejar el código un poco más limpio de como se encontró (Regla del Boy Scout).
