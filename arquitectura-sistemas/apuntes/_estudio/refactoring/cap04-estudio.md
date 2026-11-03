# Capítulo 4 — Building Tests (Construir pruebas) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la precondición esencial para refactorizar? / R: Tener un conjunto de pruebas sólidas; incluso con herramientas que automaticen refactorizaciones, siguen haciendo falta pruebas.

P: ¿Qué es el código autocomprobable (self-testing code)? / R: Código cuyas pruebas verifican sus propios resultados de forma automática, de modo que la clase señala "OK" si todo va bien, convirtiendo la suite en un potente detector de errores.

P: ¿Por qué acelera la programación tener buenas pruebas? / R: Porque la mayor parte del tiempo del programador se va en depurar; con pruebas automáticas frecuentes los errores aparecen a los pocos minutos de introducirse, cuando el código recién escrito aún está fresco.

P: ¿Qué es JUnit y quién lo creó? / R: Un framework open-source de pruebas unitarias de Erich Gamma y Kent Beck; toda clase con pruebas hereda de la clase test-case del framework.

P: ¿Qué patrón de diseño usa JUnit para agrupar pruebas? / R: El patrón composite, que permite agrupar casos de prueba en suites, y que una suite contenga casos u otras suites.

P: ¿Qué es un test fixture y cómo se gestiona? / R: Son los objetos de muestra para la prueba; se preparan con `setUp` (crea objetos) y se limpian con `tearDown` (p. ej. cerrar el fichero); ambos son métodos nulos por defecto.

P: ¿Para qué sirve `setUp`/`tearDown` en cada prueba? / R: Se ejecutan en cada prueba para aislarlas, de modo que el orden en que se ejecuten no importe.

P: ¿Cuál es la diferencia entre failures y errors en JUnit? / R: Los failures son aserciones falsas; los errors son excepciones inesperadas. Se distinguen porque surgen de forma distinta y se depuran distinto.

P: ¿Qué aporta `assertEquals` frente a un `assert` básico? / R: Compara dos valores (usa `equals()` en objetos y `==` en valores) y da un mensaje más claro, p. ej. "expected: m but was: d".

P: ¿En qué se diferencian unit tests y functional tests? / R: Las unit tests mejoran la productividad del programador y son locales a un paquete; las functional tests aseguran el sistema completo, dan garantía al cliente, tratan el sistema como caja negra y las hace un equipo distinto.

P: ¿Cómo deben guiarse las pruebas según Fowler? / R: Por el riesgo: probar lo que más preocupa, las condiciones de frontera y los errores esperados, no cada método trivial ni cada método público.

P: ¿Qué debe hacerse al recibir un informe de bug? / R: Empezar escribiendo una unit test que exponga el bug; luego cambiar el código de producción y añadir esa prueba a la suite.

P: ¿Qué son las condiciones de frontera y cuáles buscar? / R: Casos límite donde las cosas pueden fallar: el primer carácter, el último, el carácter tras el último, el fichero vacío y leer pasado el final (read past end).

P: ¿Cómo prueba Fowler herencia y polimorfismo? / R: Prueba cada alternativa según el riesgo, no todas las combinaciones (p. ej. tres clases abstractas con tres subclases dan nueve alternativas pero veintisiete combinaciones).

## Preguntas de autoevaluación

P: ¿Por qué Fowler considera una buena decisión empezar haciendo que una prueba falle? / R: Para demostrarse que la prueba realmente se ejecuta y prueba lo que él cree que prueba. (Sección: El framework de pruebas JUnit)

P: ¿Qué desventaja tenía el "testing main" de Java y cuál es la alternativa? / R: Un `main` por clase era razonable pero incómodo para ejecutar muchas pruebas; es mejor usar clases de prueba separadas dentro de un framework. (Sección: El valor del código autocomprobable)

P: ¿Por qué es mejor escribir y ejecutar pruebas incompletas que no ejecutar pruebas completas? / R: Porque intentar escribir demasiadas pruebas suele llevar a no escribir suficientes; una cantidad pequeña de pruebas ya aporta grandes beneficios. (Sección: Añadir más pruebas)

P: ¿Cómo se construye una suite evitando añadir cada caso a mano? / R: Con el constructor especial `new TestSuite(FileReaderTester.class)`, que crea un caso por cada método que empiece por `test`. (Sección: Añadir más pruebas)

P: ¿Cómo se comprueba que una excepción se lanza cuando se espera? / R: Con `try`/`fail(...)`/`catch`: si el código no lanza la excepción esperada, se llama a `fail`. (Sección: Añadir más pruebas)

P: ¿Cuándo conviene dejar de escribir pruebas? / R: No se puede probar la ausencia de bugs; hay rendimientos decrecientes, así que conviene concentrarse donde está el riesgo y donde el código se vuelve complejo. (Sección: Añadir más pruebas)

P: ¿Qué libertad permite el código de prueba que no se permite en producción? / R: Está bien copiar y editar código de prueba para generar variantes rápido, y luego refactorizar para extraer lo común. (Sección: Añadir más pruebas)

## Checklist

- [ ] Asegurar que todas las pruebas son totalmente automáticas y verifican sus propios resultados.
- [ ] Hacer que la clase de prueba herede de la clase test-case del framework (JUnit).
- [ ] Preparar el fixture en `setUp` y limpiarlo en `tearDown` (p. ej. cerrar ficheros).
- [ ] Escribir aserciones con `assert` y usar `assertEquals` para obtener mensajes claros.
- [ ] Agrupar casos en suites con `suite()`/`addTest`, o usar `new TestSuite(Clase.class)`.
- [ ] Ejecutar las pruebas con un TestRunner (GUI o texto) y hacerlo con frecuencia: al compilar y cada prueba al menos a diario.
- [ ] Al empezar, hacer que la prueba falle para confirmar que realmente se ejecuta.
- [ ] Probar condiciones de frontera: primer carácter, último, el siguiente al último, fichero vacío y leer pasado el final.
- [ ] Probar que las excepciones se lanzan cuando se espera que algo vaya mal (`try`/`fail`/`catch`).
- [ ] Ante un informe de bug, escribir primero una unit test que lo exponga y añadirla a la suite.
- [ ] Concentrar las pruebas donde está el riesgo; no probar accesores triviales.
- [ ] Combinar suites de varias clases en una `MasterTester` cuando haya varias tester classes.
