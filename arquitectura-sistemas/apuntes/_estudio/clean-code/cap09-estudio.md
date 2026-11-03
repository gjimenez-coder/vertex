# Capítulo 9 — Unit Tests (Pruebas unitarias) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre las pruebas unitarias?
R: Las pruebas unitarias automatizadas y limpias mantienen el código de producción flexible, mantenible y reutilizable: habilitan el cambio. Si las pierdes o las dejas sucias, pierdes la capacidad de cambiar el código sin miedo.

P: ¿Qué estatus tiene el código de prueba frente al de producción?
R: Es tan importante como el código de producción; no es un ciudadano de segunda clase y debe mantenerse tan limpio como el código que verifica.

P: ¿Cuál es la Primera Ley de TDD?
R: No puedes escribir código de producción hasta haber escrito una prueba unitaria que falle.

P: ¿Cuál es la Segunda Ley de TDD?
R: No puedes escribir más de una prueba unitaria de lo suficiente para que falle, y no compilar es fallar.

P: ¿Cuál es la Tercera Ley de TDD?
R: No puedes escribir más código de producción del suficiente para pasar la prueba que falla actualmente.

P: ¿A qué ciclo te someten las Tres Leyes de TDD y qué volumen de pruebas producen?
R: A un ciclo de unos treinta segundos; trabajando así se escriben docenas de pruebas al día, miles al año, cuyo volumen puede rivalizar con el del propio código de producción.

P: ¿Por qué unas pruebas sucias pueden ser peores que no tener pruebas?
R: Porque las pruebas deben cambiar al evolucionar la producción; cuanto más enredadas, más difíciles de mantener, hasta que el coste obliga a descartarlas y se pierde la capacidad de verificar cambios.

P: ¿Qué significa que las pruebas habilitan las "-ilities"?
R: Habilitan la flexibilidad, mantenibilidad y reusabilidad porque habilitan el cambio: con cobertura de pruebas no temes modificar el código ni mejorar una arquitectura o un diseño mediocres.

P: ¿Qué hace limpia a una prueba, según el capítulo?
R: Tres cosas: legibilidad, legibilidad y legibilidad; es decir claridad, simplicidad y densidad de expresión, decir mucho con las menos expresiones posibles.

P: ¿En qué consiste el patrón BUILD-OPERATE-CHECK?
R: Una parte construye los datos de prueba, otra opera sobre ellos y otra comprueba que el resultado es el esperado.

P: ¿Qué es un lenguaje de pruebas específico del dominio?
R: Un conjunto de funciones y utilidades que envuelven las APIs normales del sistema para hacer las pruebas más fáciles de escribir y leer; no se diseña por adelantado, evoluciona del refactoring continuo del código de prueba.

P: ¿En qué consiste el doble estándar de ingeniería del código de prueba?
R: La API de pruebas debe ser simple, sucinta y expresiva, pero no necesita ser tan eficiente porque corre en un entorno de prueba; cosas sobre memoria o CPU que no harías en producción están bien, pero nunca afectan a la limpieza.

P: ¿Qué defiende la regla de un assert por prueba y cuál es la postura de Martin?
R: Que cada función de prueba tenga un único assert, lo que aporta una conclusión rápida de entender; Martin la considera una buena guía pero no teme poner más de un assert, buscando minimizar su número por prueba.

P: ¿Qué dice la regla de un solo concepto por prueba y qué problema evita?
R: Probar un único concepto por función de prueba; el problema no son los múltiples asserts por sección sino probar más de un concepto, como en testAddMonths, que mezcla tres cosas independientes.

P: ¿Qué significan las letras del acrónimo F.I.R.S.T.?
R: Fast (rápidas), Independent (independientes), Repeatable (repetibles), Self-Validating (autovalidantes, salida booleana) y Timely (oportunas, escritas justo antes del código que las hace pasar).

## Preguntas de autoevaluación

P: ¿Por qué la introducción del capítulo afirma que muchos programadores se han saltado "los puntos sutiles" de escribir buenas pruebas?
R: Porque en la prisa por sumar pruebas impulsada por Agile y TDD descuidan la calidad del código de prueba, olvidando que debe mantenerse tan limpio como el de producción. (Sección: Lo que necesitas saber)

P: ¿Qué le ocurrió al equipo que decidió mantener su código de prueba con la consigna "quick and dirty"?
R: El coste de mantener la suite subió release tras release hasta que la descartaron; sin ella subió la tasa de defectos, dejaron de limpiar el código por miedo y la producción se pudrió. (Sección: Keeping Tests Clean)

P: ¿Por qué más cobertura de pruebas equivale a menos miedo al cambio?
R: Porque si tienes pruebas no temes cambiar el código: puedes mejorar una arquitectura y un diseño mediocres sin temor, ya que las pruebas verifican que el comportamiento se mantiene. (Sección: Tests Enable the -ilities)

P: ¿Qué defectos concretos del Listing 9-1 lo hacen poco limpio y cómo los resuelve el Listing 9-2?
R: Sufre duplicación [G5] y detalles que estorban la expresividad (PathParser, creación del responder, construcción del URL); el 9-2 hace lo mismo pero deja claro el patrón BUILD-OPERATE-CHECK. (Sección: Clean Tests)

P: En el ejemplo de getState(), ¿por qué está justificado concatenar Strings en vez de usar un StringBuffer?
R: Porque el código corre en un entorno de prueba que no suele estar limitado en recursos; en un sistema embebido de tiempo real con recursos limitados sí importaría, pero aquí no afecta a la limpieza. (Sección: A Dual Standard)

P: ¿Qué regla general y qué prueba faltante afloraron al dividir testAddMonths por concepto?
R: La regla de que al incrementar el mes el día no puede superar el último del mes, y la prueba faltante de febrero 28 que debería dar marzo 28. (Sección: Single Concept per Test)

P: Según F.I.R.S.T., ¿por qué las pruebas deben ser Independent y qué pasa si no lo son?
R: No deben depender unas de otras y deben poder ejecutarse en cualquier orden; si dependen entre sí, un fallo puede causar una cascada de fallos que dificulta el diagnóstico. (Sección: F.I.R.S.T.)

P: ¿Qué exige la regla Self-Validating y qué práctica descarta?
R: Que las pruebas den una salida booleana —pasan o fallan— y descarta tener que leer logs o comparar ficheros a mano para saber el resultado. (Sección: F.I.R.S.T.)

## Puntos a dominar

- Tratar el código de prueba como ciudadano de primera clase, con el mismo cuidado de diseño que el de producción.
- Recitar y aplicar las Tres Leyes de TDD y entender el ciclo de ~30 segundos que imponen.
- Explicar por qué las pruebas sucias son iguales o peores que no tener pruebas y cómo degradan la producción.
- Relacionar las pruebas limpias con las "-ilities": habilitan el cambio sin miedo.
- Identificar la legibilidad como clave de una prueba limpia y reconocer el patrón BUILD-OPERATE-CHECK.
- Entender qué es un lenguaje de pruebas específico del dominio y que evoluciona por refactoring, no por diseño previo.
- Aplicar el doble estándar: eficiencia relajada en pruebas, nunca a costa de la limpieza.
- Minimizar asserts por prueba, probar un solo concepto por función y cumplir F.I.R.S.T.
