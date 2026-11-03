# Objects and Data Structures (Objetos y estructuras de datos) — Estudio

## Tarjetas de repaso

P: ¿Qué pregunta incómoda abre el capítulo sobre los accesores? / R: Si mantenemos las variables privadas para no depender de su tipo o implementación, ¿por qué tantos programadores añaden automáticamente getters y setters que las exponen como si fueran públicas?

P: ¿Qué es un objeto según Martin? / R: Algo que oculta sus datos tras abstracciones y expone funciones que operan sobre ellos.

P: ¿Qué es una estructura de datos según Martin? / R: Algo que expone sus datos y no tiene funciones significativas.

P: ¿En qué consiste realmente la abstracción de datos? / R: En ocultar la implementación mediante interfaces abstractas que permiten manipular la esencia de los datos sin conocer su implementación; no basta con poner una capa de funciones (getters/setters) sobre las variables.

P: ¿Qué diferencia al `Point` abstracto del `Point` con `x` e `y` públicos? / R: El abstracto no revela si la implementación es rectangular, polar o ninguna, e impone una política: las coordenadas se leen por separado pero se fijan juntas como operación atómica.

P: ¿Por qué `getPercentFuelRemaining()` es mejor que `getFuelTankCapacityInGallons()` y `getGallonsOfGasoline()`? / R: Porque expresa el dato en términos abstractos, mientras que los otros son accesores concretos que exponen la implementación.

P: ¿Qué enuncia la anti-simetría datos/objeto? / R: El código procedimental facilita añadir funciones nuevas sin cambiar las estructuras de datos; el código OO facilita añadir clases nuevas sin cambiar las funciones existentes.

P: ¿Qué dificulta cada paradigma? / R: El procedimental dificulta añadir estructuras de datos nuevas (hay que cambiar todas las funciones); el OO dificulta añadir funciones nuevas (hay que cambiar todas las clases).

P: ¿Qué enuncia la Ley de Demeter? / R: Que un módulo no debe conocer las entrañas de los objetos que manipula: habla con amigos, no con extraños.

P: ¿A qué métodos puede llamar un método `f` de una clase `C` según Demeter? / R: A los de `C`, a los de un objeto creado por `f`, a los de un objeto pasado como argumento a `f` y a los de un objeto guardado en una variable de instancia de `C`.

P: ¿Qué es un "train wreck"? / R: Un encadenamiento de llamadas sobre valores devueltos (p. ej. `ctxt.getOptions().getScratchDir().getAbsolutePath()`); es estilo descuidado y conviene partirlo en variables intermedias.

P: ¿De qué depende que un train wreck viole la Ley de Demeter? / R: De si los elementos encadenados son objetos (violación clara) o estructuras de datos (exponen su estructura naturalmente y Demeter no aplica).

P: ¿Qué es una estructura híbrida y por qué es mala? / R: Es mitad objeto mitad estructura de datos (funciones importantes y a la vez variables públicas o accesores); dificulta añadir funciones y estructuras nuevas, siendo lo peor de ambos mundos.

P: ¿Qué es un Data Transfer Object (DTO)? / R: La forma por excelencia de estructura de datos: una clase con variables públicas y sin funciones, útil al comunicarse con bases de datos o parsear mensajes de sockets.

P: ¿Qué es un Active Record y cómo debe tratarse? / R: Un DTO especial con variables públicas (o beans) más métodos de navegación como `save` y `find`; debe tratarse como estructura de datos, poniendo las reglas de negocio en objetos separados que oculten sus datos.

## Preguntas de autoevaluación

P: ¿Por qué ocultar la implementación no se logra simplemente poniendo getters y setters? / R: Porque es cuestión de abstracciones: una clase debe exponer interfaces abstractas que manipulen la esencia de los datos, no empujar sus variables hacia afuera accesor por accesor. (Sección "Abstracción de datos")

P: En el ejemplo de las formas, ¿qué pasa al añadir una forma nueva en la versión procedimental frente a la OO? / R: En la procedimental hay que cambiar todas las funciones de `Geometry`; en la OO no se afectan las funciones existentes porque cada forma implementa su propio `area()` polimórfico. (Sección "Anti-simetría datos/objeto")

P: ¿Por qué dice Martin que "todo es un objeto" es un mito? / R: Porque objetos y estructuras de datos ofrecen flexibilidades contrarias y a veces conviene de verdad una estructura de datos simple con procedimientos operando sobre ella. (Sección "Lo que necesitas saber" / "Ideas clave")

P: ¿Cómo se reescribe el acceso a `ctxt` para no violar la Ley de Demeter? / R: Diciéndole al objeto que haga algo en lugar de navegar por sus internos, p. ej. `ctxt.createScratchFileStream(classFileName)` en vez de pedirle el path absoluto. (Sección "Ocultar la estructura")

P: ¿Por qué el uso de accesores confunde el análisis de la Ley de Demeter? / R: Porque con `ctxt.options.scratchDir.absolutePath` ni siquiera nos preguntaríamos por Demeter; frameworks y estándares como los beans exigen accesores y mutadores incluso en estructuras simples. (Sección "Train wrecks")

P: ¿Qué distingue a un bean de un DTO con variables públicas, y qué aporta? / R: El bean tiene variables privadas manipuladas por getters y setters; esa cuasi-encapsulación tranquiliza a puristas OO pero normalmente no aporta ningún otro beneficio. (Sección "Data Transfer Objects (DTO)")

P: ¿Cuál es el error frecuente con los Active Record y cuál la solución? / R: Tratarlos como objetos metiéndoles reglas de negocio, creando un híbrido; la solución es tratarlos como estructura de datos y crear objetos separados con las reglas de negocio que oculten sus datos. (Sección "Active Record")

## Puntos a dominar

- Distinguir abstracción de datos real frente a getters/setters mecánicos sobre las variables.
- La dicotomía objeto (oculta datos, expone comportamiento) vs. estructura de datos (expone datos, sin comportamiento).
- La anti-simetría: qué facilita y qué dificulta cada paradigma al añadir funciones o tipos nuevos.
- Enunciar la Ley de Demeter y los cuatro casos de métodos que un método puede invocar.
- Reconocer train wrecks e híbridos, y saber cuándo violan Demeter según sean objetos o estructuras de datos.
- Identificar DTO, beans y Active Record como estructuras de datos y ubicar las reglas de negocio en objetos aparte.
