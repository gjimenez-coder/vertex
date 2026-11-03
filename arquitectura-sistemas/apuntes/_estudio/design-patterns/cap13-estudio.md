# Dependency Inversion Principle (D: Principio de inversión de la dependencia) — Estudio

## Tarjetas de repaso

P: ¿Qué principio SOLID cierra la serie en este capítulo?
R: La **D**: el principio de inversión de la dependencia.

P: ¿Cuáles son las dos partes del enunciado del principio?
R: Las clases de alto nivel no deben depender de las de bajo nivel, sino ambas de abstracciones; y las abstracciones no deben depender de detalles, sino los detalles de abstracciones.

P: ¿Qué hacen las clases de bajo nivel?
R: Implementan operaciones básicas como trabajar con un disco, transferir datos por red o conectar con una base de datos.

P: ¿Qué contienen las clases de alto nivel?
R: La lógica de negocio compleja que ordena a las clases de bajo nivel que hagan algo.

P: ¿Qué problema surge al diseñar "de abajo hacia arriba"?
R: La lógica de negocio tiende a hacerse dependiente de las clases primarias de bajo nivel.

P: ¿Cuándo es habitual el diseño de abajo hacia arriba?
R: Al desarrollar un prototipo de un sistema nuevo, cuando no se tiene claro qué es posible a alto nivel porque el bajo nivel aún no está implementado o claro.

P: ¿Cuál es el primer paso para invertir la dependencia?
R: Describir interfaces para las operaciones de bajo nivel en las que se apoyarán las clases de alto nivel, preferiblemente en términos de negocio.

P: ¿Qué ejemplo de método en términos de negocio da el capítulo?
R: Invocar `abrirInforme(archivo)` en lugar de una serie de métodos `abrirArchivo(x)`, `leerBytes(n)`, `cerrarArchivo(x)`.

P: ¿De qué pasan a depender las clases de alto nivel tras el segundo paso?
R: De las interfaces definidas en términos de negocio, no de clases concretas de bajo nivel, con una dependencia mucho más débil.

P: ¿Qué ocurre en el tercer paso, cuando las clases de bajo nivel implementan las interfaces?
R: Se vuelven dependientes del nivel de la lógica de negocio, invirtiendo así la dirección de la dependencia original.

P: ¿Con qué otro principio SOLID suele ir de la mano?
R: Con el principio de abierto/cerrado, permitiendo extender las clases de bajo nivel sin descomponer las existentes.

P: ¿Qué caso recorre el capítulo?
R: Una clase de alto nivel de informes presupuestarios que usa una clase de base de datos de bajo nivel para leer y almacenar información.

P: En el ejemplo, ¿qué problema tiene la situación "ANTES"?
R: La clase de alto nivel depende de la de bajo nivel, así que un cambio en esta (p. ej. una nueva versión del servidor de base de datos) puede afectarla.

P: ¿Cuál es la solución propuesta en el ejemplo?
R: Crear una interfaz de alto nivel que describa operaciones de leer/escribir y hacer que la clase de informes la use en lugar de la clase de bajo nivel.

P: ¿Cómo queda la dependencia "DESPUÉS" en el ejemplo?
R: Las clases de bajo nivel dependen de una abstracción de alto nivel, con lo que la dirección de la dependencia original se ha invertido.

## Preguntas de autoevaluación

P: Explica con tus palabras las dos partes del enunciado del principio de inversión de la dependencia.
R: Primera: las clases de alto y bajo nivel deben depender de abstracciones, no una de otra. Segunda: las abstracciones no dependen de detalles, sino los detalles de abstracciones. (Sección: Lo que necesitas saber)

P: ¿Por qué el diseño de abajo hacia arriba lleva a acoplar mal las clases?
R: Porque al implementar primero el bajo nivel, la lógica de negocio termina construyéndose sobre clases primarias de bajo nivel y dependiendo de ellas. (Sección: El problema del diseño "de abajo hacia arriba")

P: ¿Cuáles son los tres pasos para invertir la dependencia?
R: 1) Describir interfaces de las operaciones de bajo nivel en términos de negocio; 2) hacer que las clases de alto nivel dependan de esas interfaces; 3) que las clases de bajo nivel implementen las interfaces, invirtiendo la dependencia. (Sección: Cómo invertir la dependencia)

P: ¿Por qué conviene expresar las interfaces en términos de negocio como `abrirInforme(archivo)`?
R: Porque la lógica de negocio invoca una operación de alto nivel en lugar de depender de la secuencia de bajo nivel (`abrirArchivo`, `leerBytes`, `cerrarArchivo`), y esas interfaces cuentan como de alto nivel. (Sección: Cómo invertir la dependencia)

P: En el ejemplo de informes presupuestarios, ¿qué riesgo concreto tiene depender directamente de la base de datos?
R: Que cualquier cambio en la clase de bajo nivel, como el lanzamiento de una nueva versión del servidor de base de datos, afecte a la clase de alto nivel, que no tiene por qué conocer los detalles de almacenamiento. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué relación tiene este principio con el de abierto/cerrado?
R: Suelen combinarse: al depender de abstracciones se pueden extender las clases de bajo nivel para usarlas con distintas clases de lógica de negocio sin romper las existentes. (Sección: Cómo invertir la dependencia)

P: Tras aplicar la solución, ¿en qué sentido se "invierte" la dependencia?
R: Antes el alto nivel dependía del bajo nivel; después las clases de bajo nivel dependen de abstracciones de alto nivel, quedando invertida la dirección original. (Sección: El ejemplo que recorre el capítulo)

## Puntos a dominar

- Distinguir clases de bajo nivel (operaciones básicas) de clases de alto nivel (lógica de negocio que las dirige).
- Reconocer el enunciado doble del principio: dependencia de abstracciones y detalles que dependen de abstracciones.
- Identificar por qué el diseño de abajo hacia arriba acopla la lógica de negocio al bajo nivel.
- Aplicar los tres pasos de inversión: definir interfaces de negocio, depender de ellas, implementarlas en el bajo nivel.
- Formular interfaces en términos de negocio (`abrirInforme`) en lugar de secuencias técnicas de bajo nivel.
- Relacionar el principio con el de abierto/cerrado para extender sin romper.
- Explicar el ejemplo de informes presupuestarios en sus estados ANTES, solución y DESPUÉS.
