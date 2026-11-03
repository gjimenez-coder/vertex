# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 4 — Building Tests (Construir pruebas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

La precondición esencial para refactorizar es tener un conjunto de pruebas sólidas. Incluso con una herramienta que automatice refactorizaciones, siguen haciendo falta pruebas, porque pasará mucho tiempo antes de que se puedan automatizar todas. Fowler no lo ve como una desventaja: descubrió que escribir buenas pruebas acelera mucho la programación, aunque no se esté refactorizando, algo contraintuitivo para muchos programadores.

La tesis del capítulo es que el código autocomprobable (self-testing code) convierte un conjunto de pruebas en un potente detector de errores que reduce drásticamente el tiempo de depuración. La mayor parte del tiempo de un programador no se va en escribir código, sino en depurar; encontrar un bug puede llevar horas, aunque arreglarlo sea rápido. Con pruebas automáticas ejecutadas con frecuencia, los errores aparecen a los pocos minutos de introducirse, cuando el código recién escrito aún está fresco.

Sales sabiendo cómo empezar a construir pruebas unitarias en Java con el framework JUnit: crear casos de prueba, preparar el fixture con `setUp`/`tearDown`, escribir aserciones, ejecutar suites con un TestRunner, distinguir fallos de errores, y una estrategia de pruebas guiada por el riesgo. El libro aclara que no es un libro de testing: una cantidad notablemente pequeña de pruebas ya aporta grandes beneficios.

## El ejemplo que recorre el capítulo

El hilo conductor es construir pruebas para clases del paquete `io` de Java, concretamente una clase `FileReaderTester` que prueba un lector de ficheros sobre un fichero de datos de prueba (estadísticas de cricket: Bradman, Pollock, Headley, Sutcliffe), de 141 caracteres. A partir del método `read` se van añadiendo pruebas de lectura, de condiciones de frontera y de errores esperados.

## El valor del código autocomprobable (The Value of Self-testing Code)

El origen fue una charla en OOPSLA '92 donde alguien (cree que Dave Thomas) dijo que "las clases deberían contener sus propias pruebas". Fowler lo interpretó como que cada clase tuviera un método `test`. El salto de productividad llegó al hacer las pruebas automáticas: en vez de mirar la consola, se compara la salida esperada dentro del propio código de prueba, de modo que la clase imprime "OK" si todo va bien.

- Tip: "Make sure all tests are fully automatic and that they check their own results." (PDF p. 73)
- Tip: un conjunto de pruebas es un potente detector de errores que reduce el tiempo de encontrarlos (PDF p. 74).
- Escribir la prueba antes de programar la función obliga a pensar qué hay que hacer, centra la atención en la interfaz más que en la implementación, y da un punto claro de "he terminado": cuando la prueba pasa.
- Las pruebas frecuentes son parte importante de extreme programming [Beck, XP]; los programadores de XP son testers muy dedicados.
- El idioma estándar de Java era el "testing main" (un `main` por clase que la prueba), razonable pero incómodo para ejecutar muchas pruebas; mejor usar clases de prueba separadas en un framework.

## El framework de pruebas JUnit (The JUnit Testing Framework)

JUnit es un framework open-source de Erich Gamma y Kent Beck [JUnit]. Toda clase con pruebas hereda de la clase test-case del framework. Usa el patrón composite [Gang of Four] para agrupar pruebas en suites, que pueden contener casos u otras suites (Figura 4.1).

- Un *test fixture* son los objetos de muestra para la prueba. Se preparan con `setUp` (crea objetos) y se limpian con `tearDown` (p. ej. cerrar el fichero); ambos son métodos nulos por defecto en la clase test-case.
- La prueba automática es el método `assert`: si lo de dentro es verdadero, todo bien; si no, se señala un error.
- Una suite se crea con el método `suite()`, al que se añaden casos con `addTest`. El nombre del método a probar se pasa al constructor y se enlaza por reflexión de Java.
- Se ejecuta con `TestRunner` (hay versión GUI y versión de texto). La salida de texto imprime un punto por prueba, el tiempo, y "OK (1 tests)" si todo va bien.

```java
public void testRead() throws IOException {
    char ch = '&';
    for (int i=0; i < 4; i++)
        ch = (char) _input.read();
    assertEquals('m', ch);
}
```

- Tip: ejecuta las pruebas con frecuencia; localiza las pruebas al compilar, cada prueba al menos cada día (PDF p. 77).
- Al introducir un bug deliberado, la salida muestra `!!!FAILURES!!!` e indica qué prueba falló. El mensaje básico es poco útil; `assertEquals` compara dos valores (usa `equals()` en objetos y `==` en valores) y da un mensaje más claro, p. ej. "expected: m but was: d".
- El framework distingue *failures* (aserciones falsas) de *errors* (excepciones inesperadas), porque surgen de forma distinta y se depuran distinto.
- Fowler suele empezar haciendo que la prueba falle, para demostrarse que realmente se ejecuta y prueba lo que cree.
- La GUI de JUnit (Figura 4.2) muestra una barra verde si pasan todas y roja si hay fallos, y enlaza automáticamente los cambios de código.

## Pruebas unitarias y funcionales (Unit and Functional Tests)

- Las *unit tests* se escriben para mejorar la productividad del programador; tener contenta a QA es un efecto secundario. Son muy localizadas: cada clase de prueba trabaja dentro de un solo paquete y asume que el resto funciona.
- Las *functional tests* aseguran que el software funciona como un todo; dan garantía de calidad al cliente y deberían desarrollarlas un equipo distinto, con herramientas pesadas, que disfrute encontrando bugs. Tratan el sistema como caja negra (vía GUI, o mirando cómo cambian los datos).
- Al corregir un bug encontrado por testers o usuarios hay que cambiar el código de producción y, además, añadir una unit test que exponga el bug.
- Tip: cuando recibas un informe de bug, empieza escribiendo una unit test que lo exponga (PDF p. 79).
- JUnit es para unit tests; para refactorizar, Fowler cuenta con las unit tests, "the programmer's friend".

## Añadir más pruebas (Adding More Tests)

El estilo es mirar todo lo que la clase debería hacer y probar cada cosa ante condiciones que puedan hacerla fallar. No es lo mismo que "probar cada método público": las pruebas deben guiarse por el riesgo. No prueba accesores triviales porque es poco probable encontrar bugs ahí. Intentar escribir demasiadas pruebas suele llevar a no escribir suficientes.

- Tip: es mejor escribir y ejecutar pruebas incompletas que no ejecutar pruebas completas (PDF p. 80).
- Buscar *condiciones de frontera*: el primer carácter, el último, el carácter tras el último; para ficheros, el fichero vacío es siempre buena elección. También probar leer pasado el final (`read past end`).
- Tip: piensa en las condiciones de frontera donde las cosas pueden ir mal y concentra ahí las pruebas (PDF p. 81-82).
- El constructor especial `new TestSuite(FileReaderTester.class)` construye una suite con un caso por cada método que empiece por `test`, evitando añadirlos a mano.
- `setUp` y `tearDown` se ejecutan en cada prueba para aislarlas, de modo que el orden no importe.
- Fowler se pone en el papel de enemigo del código, pensando activamente cómo romperlo; lo considera productivo y divertido.
- Tip: no olvides probar que las excepciones se lanzan cuando se espera que algo vaya mal (PDF p. 83). Se comprueba con `try`/`fail(...)`/`catch`.
- Con varias tester classes se puede crear una `MasterTester` que combine suites de varias clases, porque una suite puede contener otras.
- ¿Cuándo parar? No se puede probar la ausencia de bugs, pero eso no impide que el testing acelere la programación. Hay rendimientos decrecientes: concéntrate donde está el riesgo, donde el código se vuelve complejo.
- Tip: no dejes que el miedo a que las pruebas no atrapen todos los bugs te impida escribir las que atraparán la mayoría (PDF p. 84).
- Herencia y polimorfismo dificultan el testing por las combinaciones (tres clases abstractas con tres subclases: nueve alternativas pero veintisiete combinaciones). Fowler prueba cada alternativa, no todas las combinaciones, según el riesgo.
- A diferencia del código de producción, está bien copiar y editar código de prueba para generar variantes rápido; luego se puede refactorizar para extraer lo común.

## Ideas clave

- Tener pruebas sólidas es la precondición para refactorizar; el código debe ser autocomprobable.
- Las pruebas automáticas que verifican sus propios resultados, ejecutadas con frecuencia, forman un detector de errores que recorta el tiempo de depuración.
- JUnit (Gamma y Beck) usa el patrón composite: casos de prueba agrupables en suites; fixture con `setUp`/`tearDown`; aserciones con `assert` y `assertEquals`.
- El framework distingue fallos (aserciones falsas) de errores (excepciones inesperadas).
- El testing debe guiarse por el riesgo: probar lo que más preocupa, las condiciones de frontera y los errores esperados, no cada método trivial.
- Es mejor ejecutar pruebas incompletas que no ejecutar pruebas completas; la perfección desanima y lleva a no probar nada.
- Las unit tests sirven a la productividad del programador y son locales por paquete; las functional tests aseguran el sistema completo y las hace otro equipo.
- Ante un bug, empieza escribiendo una prueba que lo exponga; añade pruebas a la suite a medida que refactorizas.
