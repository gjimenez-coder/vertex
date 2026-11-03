# Refactoring, a First Example (Refactorización, un primer ejemplo) — Estudio

## Tarjetas de repaso

P: ¿Por qué Fowler abre el libro con un ejemplo en lugar de con historia y principios?
R: Porque considera que es con ejemplos como se entiende realmente qué ocurre al refactorizar.

P: ¿Cuál es la paradoja del autor que reconoce Fowler?
R: Un programa grande sería demasiado complejo para seguirlo, y uno pequeño hace que la refactorización parezca innecesaria; pide imaginar el ejemplo como parte de un sistema mayor.

P: ¿Cuál es la tesis central del capítulo sobre el diseño pobre?
R: Un diseño pobre no molesta al compilador pero sí al humano al cambiar el sistema: cuesta localizar dónde modificar y es fácil introducir errores.

P: ¿Cuál es el ritmo esencial de la refactorización?
R: Probar, cambio pequeño, probar, cambio pequeño.

P: ¿Qué debe existir antes de empezar a refactorizar?
R: Un conjunto sólido y autoverificable de pruebas que dé la seguridad necesaria para cambiar el programa.

P: ¿Qué clases iniciales tiene el ejemplo del videoclub y qué representan?
R: `Movie` (datos: título y código de precio), `Rental` (alquiler de una película con días) y `Customer` (nombre, vector de alquileres y el método largo `statement()`).

P: ¿Qué dos cambios piden los usuarios y por qué son problemáticos con el diseño inicial?
R: Imprimir el recibo en HTML y modificar la clasificación de películas; obligarían a duplicar `statement()` por copiar y pegar y a mantener reglas consistentes en dos sitios.

P: ¿En qué consiste Extract Method aplicado al `switch` del cargo?
R: Se extrae el cálculo a `amountFor(Rental each)`, analizando antes las variables locales: `each` se pasa como parámetro y `thisAmount` se devuelve.

P: ¿Qué enseña el error de declarar el retorno como `int` en vez de `double`?
R: Como cada cambio es muy pequeño, los errores son fáciles de encontrar; las pruebas lo detectaron de inmediato.

P: ¿Qué principio justifica Move Method de `amountFor` a `Rental` como `getCharge()`?
R: Un método debe estar en el objeto cuyos datos usa.

P: ¿Qué es Replace Temp with Query y qué coste acepta Fowler al aplicarlo?
R: Eliminar temporales como `thisAmount` usando directamente `each.getCharge()`; acepta recalcular el cargo dos veces, coste que se optimiza mejor con el código bien factorizado.

P: ¿Por qué se reemplaza el `switch` del precio por polimorfismo?
R: Es mala idea hacer un `switch` basado en un atributo de otro objeto; si debe usarse, que sea sobre los datos propios.

P: ¿Por qué se usa el patrón State en vez de subclasear `Movie`?
R: Porque una película puede cambiar de clasificación durante su vida y un objeto no puede cambiar de clase; se delega a una jerarquía `Price`.

P: ¿Qué tres refactorizaciones encadenadas montan el patrón State?
R: Replace Type Code with State/Strategy, Move Method del `switch` a `Price` y Replace Conditional with Polymorphism.

P: ¿Por qué `getFrequentRenterPoints` no se declara abstracto en `Price`?
R: Se deja una implementación por defecto en `Price` (devuelve 1) y solo `NewReleasePrice` la sobreescribe.

## Preguntas de autoevaluación

P: ¿Qué recomienda Fowler cuando hay que añadir una función y el código no está estructurado de forma conveniente?
R: Refactorizar primero para hacer fácil el cambio y luego hacer el cambio. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué características tienen las pruebas que construye antes de refactorizar?
R: Comparan cadenas del recibo contra referencias verificadas a mano, se ejecutan con un solo comando Java, tardan pocos segundos y son autoverificables (dicen "OK" o listan las diferencias). (Sección: El primer paso: construir pruebas)

P: Al descomponer `statement()`, ¿cómo decide Fowler qué hacer con las variables locales `each` y `thisAmount`?
R: `each` no se modifica, así que se pasa como parámetro; `thisAmount` se modifica, así que se devuelve. (Sección: Descomponer y redistribuir statement())

P: ¿Por qué al extraer los puntos de cliente frecuente basta una asignación acumulativa (`+=`) sin pasar la temporal como parámetro?
R: Porque `frequentRenterPoints` tiene valor previo pero el cuerpo extraído no lo lee. (Sección: Extraer los puntos de cliente frecuente)

P: ¿Por qué reemplazar `totalAmount` y `frequentRenterPoints` por consultas no es el caso más simple de Replace Temp with Query?
R: Porque las temporales se asignaban dentro de un bucle, así que hay que copiar el bucle a la consulta. (Sección: Eliminar temporales con consultas (queries))

P: ¿Qué efecto tienen las consultas `getTotalCharge()` y `getTotalFrequentRenterPoints()` sobre el aumento de código y el rendimiento, y qué postura adopta Fowler?
R: Aumentan el código y ejecutan el bucle tres veces en vez de una, pero no hay que preocuparse por el rendimiento al refactorizar; se mide y optimiza después. (Sección: Eliminar temporales con consultas (queries))

P: ¿Por qué Fowler prefiere pasar la duración del alquiler a la película en lugar de pasar el tipo al alquiler?
R: Porque los cambios previstos añaden tipos: la información de tipo es más volátil y quiere minimizar el efecto dominó. (Sección: Reemplazar la lógica condicional del precio por polimorfismo)

P: ¿Cuál es la lección más importante del ejemplo según Fowler?
R: El ritmo de la refactorización: probar, cambio pequeño, probar, cambio pequeño. (Sección: Reflexiones finales)

## Puntos a dominar

- Refactoriza primero para hacer fácil el cambio, luego haz el cambio; el diseño pobre duele al modificar, no al compilador.
- Ten un conjunto de pruebas sólido y autoverificable antes de refactorizar.
- Interioriza el ritmo: probar, cambio pequeño, probar; con pasos pequeños los errores son fáciles de localizar.
- Aplica Move Method para que un método esté en el objeto cuyos datos usa, y cuida que los nombres de variables comuniquen su propósito.
- Elimina temporales con Replace Temp with Query y no optimices el rendimiento durante la refactorización.
- Reconoce que extraer cálculos a consultas permite reutilizarlos (p. ej. en `htmlStatement()`) sin copiar y pegar.
- Evita `switch` sobre datos de otro objeto y reemplaza la lógica condicional por polimorfismo.
- Usa el patrón State (jerarquía `Price`) cuando una entidad cambia de clasificación en vida, en vez de subclasear directamente.
