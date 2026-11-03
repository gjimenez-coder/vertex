# Capítulo 2 — Principles in Refactoring (Principios de la refactorización) — Estudio

## Tarjetas de repaso

P: ¿Qué es un *refactoring* como sustantivo?
R: Un cambio en la estructura interna del software para hacerlo más fácil de entender y más barato de modificar, sin alterar su comportamiento observable.

P: ¿Qué es refactorizar como verbo?
R: Reestructurar el software aplicando una serie de refactorings sin cambiar su comportamiento observable.

P: ¿En qué se diferencia refactorizar de optimizar el rendimiento?
R: Refactorizar busca facilitar la comprensión y modificación; la optimización de rendimiento suele hacer el código más difícil de entender.

P: ¿Qué es la metáfora de los dos sombreros de Kent Beck?
R: El desarrollo se reparte entre añadir función (agregar capacidades medidas con tests nuevos) y refactorizar (reestructurar sin añadir función); hay que saber siempre qué sombrero se lleva.

P: ¿Cuáles son las cuatro razones para refactorizar?
R: Mejora el diseño del software, lo hace más fácil de entender, ayuda a encontrar bugs y ayuda a programar más rápido.

P: ¿Qué es la regla de tres de Don Roberts?
R: La primera vez lo haces; la segunda haces la duplicación aunque moleste; la tercera vez que haces algo similar, refactorizas ("Three strikes and you refactor").

P: ¿En qué momentos conviene refactorizar?
R: Al añadir función, al corregir un bug y al hacer revisiones de código; se hace en pequeñas ráfagas, no en tiempo agendado.

P: Según Kent Beck, ¿qué cuatro cosas vuelven un programa difícil de modificar?
R: Que sea difícil de leer, que tenga lógica duplicada, que exija cambiar código en ejecución para añadir comportamiento y que tenga lógica condicional compleja.

P: ¿Cuándo se paga sola la indirección introducida por la refactorización?
R: Cuando sirve para compartir lógica, explicar intención e implementación por separado, aislar el cambio o codificar lógica condicional como mensajes polimórficos.

P: ¿Qué es una interfaz publicada y por qué complica la refactorización?
R: Es una interfaz un paso más allá de pública, usada por código que no controlas; si una refactorización la cambia, hay que conservar la vieja (llamando a la nueva) y marcarla como *deprecated*.

P: ¿Cuándo no deberías refactorizar?
R: Cuando conviene reescribir desde cero (código muy desordenado o que no funciona) o cuando estás cerca de una fecha límite (deuda técnica a gestionar).

P: ¿Cómo cambia la refactorización el papel del diseño?
R: Reduce la presión por acertar el diseño por adelantado; el diseño inicial busca una solución razonable y el resultado es un movimiento hacia la simplicidad.

P: ¿Cuáles son los tres enfoques para lograr software rápido?
R: Presupuesto de tiempo (tiempo real duro), atención constante (común pero poco eficaz) y optimización tardía con perfilador.

P: ¿Qué lección dejan las historias de Chrysler y del sistema de nómina sobre el rendimiento?
R: Mide el rendimiento con un perfilador en vez de especular; los programas gastan la mayor parte del tiempo en una fracción pequeña del código.

## Preguntas de autoevaluación

P: ¿Por qué se degrada el diseño del software sin refactorización y qué aspecto clave lo combate?
R: Los cambios para metas a corto plazo o sin comprensión plena borran la estructura; eliminar código duplicado para decir todo "una vez y solo una vez" lo combate. (Sección: Por qué deberías refactorizar)

P: ¿Por qué un informe de error puede ser una señal para refactorizar?
R: Indica que el código no era lo bastante claro para que vieras el bug; clarificar la estructura hace visibles los errores. (Sección: Cuándo deberías refactorizar / Por qué deberías refactorizar)

P: ¿Qué recomienda Fowler decirle a un gerente orientado al calendario sobre la refactorización?
R: No se lo digas; el trabajo del profesional es construir software eficaz lo más rápido posible, y refactorizar es la vía más rápida. (Sección: Qué le digo a mi jefe)

P: ¿Cómo afrontar la refactorización cuando una aplicación está acoplada al esquema de una base de datos no orientada a objetos?
R: Interponer una capa separada entre el modelo de objetos y el modelo de datos, que puede crearse cuando se noten partes volátiles. (Sección: Problemas con la refactorización)

P: ¿Cómo afecta la refactorización al rendimiento a corto y largo plazo?
R: Suele hacer el programa más lento a corto plazo, pero más susceptible de afinarse; un programa bien factorizado da más tiempo y granularidad más fina para optimizar. (Sección: Refactorización y rendimiento)

P: Según la refactorización y el diseño, ¿cómo decidir entre una solución simple y una flexible?
R: Preguntar qué tan difícil será refactorizar la solución simple hacia la flexible; si es fácil, construir lo más simple que funcione. (Sección: Refactorización y diseño)

P: ¿Quiénes contribuyeron al origen de la refactorización y qué herramienta destacada surgió?
R: Ward Cunningham y Kent Beck con Smalltalk, Ralph Johnson en frameworks, Bill Opdyke con su tesis en C++, y John Brant y Don Roberts con el Refactoring Browser para Smalltalk. (Sección: De dónde vino la refactorización)

## Puntos a dominar

- Distinguir refactoring como sustantivo (cambio de estructura interna sin alterar comportamiento) y refactorizar como verbo.
- Separar las dos actividades de los dos sombreros y saber en cada momento cuál llevas puesto.
- Enumerar las cuatro razones para refactorizar y los momentos para hacerlo (regla de tres, al añadir función, al corregir bugs, en revisiones).
- Reconocer cuándo la indirección se paga sola y cuándo quitar la indirección parasitaria.
- Identificar los límites de la refactorización: bases de datos, interfaces publicadas y cambios de diseño difíciles.
- Saber cuándo no refactorizar: reescritura desde cero y plazos inminentes (deuda técnica).
- Explicar la relación entre refactorización, diseño simple y rendimiento: construir bien factorizado y afinar tarde midiendo con perfilador.
