# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 11 — Appendix B. Facts, Laws, Rules, and Definitions (Apéndice B. Hechos, leyes, reglas y definiciones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este apéndice es una recopilación literal de todos los hechos (facts), leyes (laws), reglas (rules) y definiciones (definitions) principales que aparecen a lo largo del libro. No introduce ideas nuevas: funciona como índice de referencia rápida que condensa el cuerpo teórico de *Code Simplicity*.

La tesis central que recorre toda la lista es que el diseño de software se rige por leyes conocibles, eternas y verdaderas, y que el objetivo del software es ayudar a las personas. A partir de ahí se derivan criterios prácticos para decidir cambios, controlar la complejidad y mantener la simplicidad.

Al terminar deberías poder reconocer las cuatro categorías de enunciados y recordar las leyes nombradas del libro: la Ecuación del Diseño de Software, la Ley del Cambio, la Ley de la Probabilidad de Defectos, la Ley de la Simplicidad y la Ley de las Pruebas.

## Definiciones

- **Programa**: (1) una secuencia de instrucciones dadas a la computadora; (2) las acciones que toma una computadora como resultado de recibir instrucciones.
- **Diseño de software (software design)**: todo lo que involucra la arquitectura del sistema o las decisiones técnicas que se toman al crearlo.

## Hechos (Facts)

- La diferencia entre un mal y un buen programador es la comprensión: los malos no entienden lo que hacen, los buenos sí.
- Todo el que escribe software es un diseñador.
- Existen leyes del diseño de software, son conocibles, eternas, inmutables, fundamentalmente verdaderas y funcionan.
- Los objetivos del diseño de software son: (1) escribir software lo más útil posible; (2) permitir que siga siendo lo más útil posible; (3) diseñar sistemas que se puedan crear y mantener con la mayor facilidad.
- El error más común y desastroso de los programadores es predecir algo del futuro cuando en realidad no pueden conocerlo.
- Los tres errores ("las tres fallas") al enfrentar la Ley del Cambio son: escribir código que no se necesita, no hacer el código fácil de cambiar, y ser demasiado genérico.
- Cuando tu diseño hace las cosas más complejas en vez de simplificarlas, estás haciendo sobreingeniería (overengineering).
- La simplicidad es relativa.
- La pregunta clave detrás de toda simplificación válida es: "¿Cómo podría esto ser más fácil de manejar o más comprensible?".

## Leyes (Laws)

- **Propósito del software**: el propósito del software es ayudar a las personas.
- **La Ecuación del Diseño de Software** (Ley Primaria): la conveniencia de un cambio es directamente proporcional al valor presente más el valor futuro, e inversamente proporcional al esfuerzo de implementación más el esfuerzo de mantenimiento. Con el tiempo la ecuación se reduce de modo que importa más reducir el esfuerzo de mantenimiento que el de implementación.
- **Ley del Cambio (Law of Change)**: cuanto más tiempo exista tu programa, más probable es que cualquier parte tenga que cambiar.
- **Ley de la Probabilidad de Defectos (Law of Defect Probability)**: la probabilidad de introducir un defecto es proporcional al tamaño de los cambios que haces.
- **Ley de la Simplicidad (Law of Simplicity)**: la facilidad de mantenimiento es proporcional a la simplicidad de las piezas individuales.
- **Ley de las Pruebas (Law of Testing)**: el grado en que conoces cómo se comporta tu software es el grado en que lo has probado con precisión.

## Reglas (Rules)

- Un "buen programador" debe hacer todo lo posible por que lo que escribe sea lo más simple posible para otros programadores.
- El diseño no es una democracia: las decisiones las toman individuos.
- La calidad del diseño debe ser proporcional al tiempo futuro en que el sistema seguirá ayudando a las personas.
- Hay cosas del futuro que no puedes conocer; estás más seguro si no intentas predecirlo y decides con información del presente.
- No escribas código hasta que lo necesites y elimina el que no se usa.
- Diseña según lo que sabes ahora, no según lo que crees que pasará.
- Sé solo tan genérico como sepas que necesitas ser ahora mismo; evita las tres fallas con desarrollo y diseño incrementales.
- El mejor diseño permite el mayor cambio en el entorno con el menor cambio en el software.
- Nunca "arregles" nada salvo que sea un problema y tengas evidencia de que existe realmente.
- Idealmente, cualquier pieza de información debe existir una sola vez en el sistema.
- Si de verdad quieres triunfar, conviene ser "tonto, simple hasta lo bobo" (stupid, dumb simple); sé consistente.
- La legibilidad depende sobre todo de cómo ocupan el espacio letras y símbolos; los nombres deben ser lo bastante largos para comunicar sin volverse difíciles de leer; los comentarios explican por qué, no qué.
- La simplicidad requiere diseño.
- Formas de crear complejidad: expandir el propósito del software, añadir programadores, cambiar lo que no hace falta, quedar atrapado en malas tecnologías, malentendidos, diseño pobre o nulo, reinventar la rueda, violar el propósito del software.
- Juzga si una tecnología es "mala" por su potencial de supervivencia, interoperabilidad y atención a la calidad.
- Si algo se vuelve muy complejo, suele haber un error de diseño por debajo del nivel donde aparece la complejidad; ante la complejidad pregunta "¿Qué problema intentas resolver?".
- La mayoría de los problemas difíciles de diseño se resuelven dibujándolos o escribiéndolos en papel.
- Maneja la complejidad rediseñando las piezas individuales en pasos pequeños.
- Si topas con una complejidad inarreglable fuera de tu programa, ponle un envoltorio (wrapper) simple para otros programadores.
- Reescribir solo es aceptable en un conjunto muy limitado de situaciones.
- A menos que lo hayas probado, no sabes que funciona.

## Ideas clave

- El apéndice es un catálogo de referencia de cuatro tipos de enunciados: hechos, leyes, reglas y definiciones.
- Hay cinco leyes nombradas más la Ecuación del Diseño de Software como Ley Primaria.
- El propósito del software —ayudar a las personas— es la base de todo el sistema de leyes.
- Las decisiones de diseño deben basarse en el presente conocido, no en predicciones del futuro.
- La simplicidad y el mantenimiento priman sobre la facilidad de implementación inicial.
- El desarrollo incremental y el diseño por piezas pequeñas son las defensas contra la complejidad y las tres fallas.
- Nada se da por funcional hasta que se ha probado.
