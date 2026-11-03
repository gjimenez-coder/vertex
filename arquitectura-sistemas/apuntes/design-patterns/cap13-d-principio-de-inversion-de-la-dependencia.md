# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 13 — Dependency Inversion Principle (D: Principio de inversión de la dependencia)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación de párrafos) y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo cierra los principios SOLID con la **D**: el principio de inversión de la dependencia. Su enunciado es doble: las clases de alto nivel no deben depender de clases de bajo nivel, sino que ambas deben depender de abstracciones; y las abstracciones no deben depender de detalles, sino los detalles de abstracciones.

El capítulo parte de una distinción entre dos niveles de clases que suele aparecer al diseñar software. Las clases de bajo nivel implementan operaciones básicas (trabajar con un disco, transferir datos por una red, conectar con una base de datos), mientras que las clases de alto nivel contienen la lógica de negocio compleja que ordena a las de bajo nivel que hagan algo. El problema habitual es que, cuando se diseñan primero las clases de bajo nivel, la lógica de negocio termina dependiendo de ellas.

Sales sabiendo cómo invertir esa dirección de dependencia mediante interfaces definidas en términos de negocio, de modo que las clases de bajo nivel pasen a depender del nivel de la lógica de negocio y no al revés.

## El problema del diseño "de abajo hacia arriba"

Algunas personas diseñan primero las clases de bajo nivel y sólo después trabajan con las de alto nivel. Es habitual al desarrollar un prototipo de un sistema nuevo, cuando no se tiene claro qué es posible a alto nivel porque el contenido de bajo nivel todavía no está implementado o claro. Con este enfoque, las clases de la lógica de negocio tienden a hacerse dependientes de clases primarias de bajo nivel.

## Cómo invertir la dependencia

El principio sugiere cambiar la dirección de esa dependencia en tres pasos:

1. Describir **interfaces para las operaciones de bajo nivel** en las que se apoyarán las clases de alto nivel, preferiblemente en términos de negocio. Por ejemplo, la lógica de negocio debe invocar un método `abrirInforme(archivo)` en lugar de una serie de métodos `abrirArchivo(x)`, `leerBytes(n)`, `cerrarArchivo(x)`. Estas interfaces cuentan como de alto nivel.
2. Hacer que las **clases de alto nivel dependan de esas interfaces**, en lugar de clases concretas de bajo nivel. Esta dependencia será mucho más débil que la original.
3. Una vez que las **clases de bajo nivel implementan esas interfaces**, se vuelven dependientes del nivel de la lógica de negocio, invirtiendo así la dirección de la dependencia original.

El capítulo señala que este principio suele ir de la mano del **principio de abierto/cerrado**: se pueden extender las clases de bajo nivel para usarlas con distintas clases de lógica de negocio sin descomponer las clases existentes.

## El ejemplo que recorre el capítulo

El ejemplo usa una clase de alto nivel que se ocupa de **informes presupuestarios** y utiliza una clase de **base de datos** de bajo nivel para leer y almacenar su información.

- **ANTES:** la clase de alto nivel depende de la clase de bajo nivel. Esto significa que cualquier cambio en la clase de bajo nivel —por ejemplo, el lanzamiento de una nueva versión del servidor de la base de datos— puede afectar a la clase de alto nivel, que no tiene por qué conocer los detalles de almacenamiento de datos.
- **La solución:** crear una **interfaz de alto nivel** que describa operaciones de leer/escribir y hacer que la clase de informes utilice esa interfaz en lugar de la clase de bajo nivel. Después se puede cambiar o extender la clase de bajo nivel original para que implemente la nueva interfaz de leer/escribir declarada por la lógica de negocio.
- **DESPUÉS:** las clases de bajo nivel dependen de una abstracción de alto nivel. Como resultado, la dirección de la dependencia original se ha invertido: las clases de bajo nivel dependen ahora de abstracciones de alto nivel.

## Ideas clave

- El enunciado tiene dos partes: alto y bajo nivel dependen de abstracciones; las abstracciones no dependen de detalles, los detalles de abstracciones.
- Las clases de bajo nivel hacen operaciones básicas; las de alto nivel contienen la lógica de negocio que las dirige.
- Diseñar de abajo hacia arriba tiende a que la lógica de negocio dependa de clases de bajo nivel.
- La solución es definir interfaces en términos de negocio (p. ej. `abrirInforme(archivo)` en vez de `abrirArchivo`/`leerBytes`/`cerrarArchivo`).
- Las clases de alto nivel dependen de esas interfaces, no de clases concretas; la dependencia se vuelve más débil.
- Al implementar las interfaces, las clases de bajo nivel pasan a depender del nivel de negocio: la dependencia queda invertida.
- Este principio suele combinarse con el de abierto/cerrado, permitiendo extender sin romper clases existentes.
- En el ejemplo de informes presupuestarios, introducir una interfaz de leer/escribir aísla el alto nivel de los detalles de almacenamiento.
