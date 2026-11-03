# Comments (Comentarios) — Estudio

## Tarjetas de repaso

P: ¿Cómo describe el autor los comentarios en el mejor de los casos? / R: Como un mal necesario; su uso adecuado compensa nuestra incapacidad de expresarnos en el código.

P: ¿Qué sentimiento debería acompañar la escritura de un comentario? / R: El sentimiento de fracaso de la propia capacidad de expresión, porque un lenguaje suficientemente expresivo casi no necesitaría comentarios.

P: ¿Por qué el autor desconfía de los comentarios? / R: Porque mienten: el código cambia y se mueve, pero los comentarios no siempre lo siguen y quedan huérfanos, con exactitud decreciente.

P: ¿Por qué un comentario inexacto es peor que ninguno? / R: Porque engaña y desinforma, creando expectativas que no se cumplen; la única verdad precisa está en el código.

P: ¿Cuál es el único comentario verdaderamente bueno? / R: El que encontraste la manera de no escribir, expresando la intención en el propio código.

P: ¿Qué son los comentarios legales y cómo deben tratarse? / R: Encabezados de copyright y autoría al inicio del archivo; no deben ser contratos y, cuando se pueda, deben referir a una licencia estándar externa.

P: ¿Qué documenta un comentario de explicación de intención? / R: La razón detrás de una decisión, de modo que aunque no compartas la solución entiendas qué pretendía el autor.

P: ¿Para qué sirve un comentario de aclaración y cuál es su riesgo? / R: Traduce un argumento o valor de retorno oscuro a algo legible, útil en librerías que no puedes alterar; su riesgo es ser incorrecto, así que debe ser exacto.

P: ¿Qué advierte un comentario de advertencia de consecuencias? / R: Avisa a otros programadores de un riesgo, como un test lento o que `SimpleDateFormat` no es thread-safe y hay que crear cada instancia aparte.

P: ¿Qué son los comentarios TODO y qué precaución exigen? / R: Notas de trabajo pendiente con su justificación; no son excusa para dejar código malo y deben revisarse y eliminarse periódicamente.

P: ¿Qué diferencia a un comentario redundante de uno engañoso? / R: El redundante dice lo mismo que el código y tarda más en leerse; el engañoso es sutilmente impreciso, como `waitForClose`, que espera un timeout ciego y lanza excepción en vez de retornar al cerrarse.

P: ¿Por qué deben eliminarse los comentarios de diario (journal)? / R: Porque son registros de cambios al inicio del módulo que hoy hace el control de versiones por nosotros.

P: ¿Qué debe hacerse con el código comentado y por qué? / R: Borrarlo; nadie se atreve a eliminarlo y se acumula como posos, y el control de versiones lo recuerda igualmente.

P: ¿Qué principio aplicar antes de escribir un comentario? / R: Buscar una función o variable que lo haga innecesario, por ejemplo `employee.isEligibleForFullBenefits()` en lugar de explicar la condición.

P: ¿A qué se redujeron los comentarios en la refactorización de `PrimeGenerator`? / R: A solo dos comentarios explicativos: uno que introduce la Criba de Eratóstenes y otro que justifica por qué el límite de iteración es la raíz cuadrada del tamaño del arreglo.

## Preguntas de autoevaluación

P: ¿Cuál es la tesis central del capítulo sobre los comentarios? / R: Que los comentarios son un mal necesario y que el mejor comentario es el que logras no escribir expresando la intención en el código. (Sección: Lo que necesitas saber)

P: ¿Qué hace que los comentarios tiendan a mentir con el tiempo? / R: Que el código evoluciona y se mueve mientras los comentarios quedan huérfanos y pierden exactitud, porque los programadores no pueden mantenerlos de forma realista. (Sección: Lo que necesitas saber)

P: Nombra al menos cuatro tipos de comentarios considerados buenos. / R: Legales, informativos, de explicación de intención, de aclaración, de advertencia de consecuencias, TODO, de amplificación y Javadocs en APIs públicas. (Sección: Comentarios buenos)

P: ¿Por qué los comentarios obligatorios (mandated) son contraproducentes? / R: Porque la regla de que toda función o variable lleve comentario solo genera ruido y mentiras. (Sección: Comentarios malos)

P: ¿Qué problema tienen los comentarios en las llaves de cierre de una función? / R: Son señal de que la función es demasiado larga; en lugar de comentar, conviene acortarla. (Sección: Comentarios malos)

P: ¿Qué caracteriza al ejemplo que recorre el capítulo y qué demuestra su refactorización? / R: `GeneratePrimes.java`, antes considerado "bien documentado", se refactoriza a `PrimeGenerator.java` y queda con solo dos comentarios explicativos, mostrando cuánto comentario era innecesario. (Sección: El ejemplo que recorre el capítulo)

P: ¿Por qué un comentario no debe contener información no local o demasiada información? / R: Porque debe describir el código cercano, no partes lejanas del sistema ni disquisiciones históricas o detalles irrelevantes. (Sección: Comentarios malos)

## Checklist

- Antes de escribir un comentario, intenta expresar la intención en el código mediante una función o variable con buen nombre.
- No comentes código malo: límpialo en lugar de explicarlo.
- Verifica que todo comentario de aclaración sea exacto para no engañar.
- Elimina el código comentado, los comentarios de diario y las atribuciones o firmas: confía en el control de versiones.
- Revisa y depura periódicamente los comentarios TODO.
- Comprueba que los comentarios en llaves de cierre no estén delatando funciones demasiado largas.
- Reserva los Javadocs para APIs públicas y evita el Javadoc en código no público.
- Asegura que la conexión entre comentario y código sea evidente y de ámbito local.
