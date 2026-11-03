# Appendix B. Facts, Laws, Rules, and Definitions (Apéndice B. Hechos, leyes, reglas y definiciones) — Estudio

## Tarjetas de repaso

P: ¿Qué cuatro categorías de enunciados recopila el apéndice B? / R: Hechos (facts), leyes (laws), reglas (rules) y definiciones (definitions).

P: ¿Cuál es el propósito del software según la ley correspondiente? / R: El propósito del software es ayudar a las personas.

P: ¿Qué establece la Ecuación del Diseño de Software (Ley Primaria)? / R: La conveniencia de un cambio es directamente proporcional al valor presente más el valor futuro, e inversamente proporcional al esfuerzo de implementación más el esfuerzo de mantenimiento.

P: Con el tiempo, ¿qué pasa a importar más en la Ecuación del Diseño de Software? / R: Importa más reducir el esfuerzo de mantenimiento que el esfuerzo de implementación.

P: ¿Qué dice la Ley del Cambio (Law of Change)? / R: Cuanto más tiempo exista tu programa, más probable es que cualquier parte tenga que cambiar.

P: ¿Qué afirma la Ley de la Probabilidad de Defectos (Law of Defect Probability)? / R: La probabilidad de introducir un defecto es proporcional al tamaño de los cambios que haces.

P: ¿Qué sostiene la Ley de la Simplicidad (Law of Simplicity)? / R: La facilidad de mantenimiento es proporcional a la simplicidad de las piezas individuales.

P: ¿Qué establece la Ley de las Pruebas (Law of Testing)? / R: El grado en que conoces cómo se comporta tu software es el grado en que lo has probado con precisión.

P: ¿Cómo se define "programa" en el apéndice? / R: (1) Una secuencia de instrucciones dadas a la computadora; (2) las acciones que toma una computadora al recibir instrucciones.

P: ¿Cómo se define "diseño de software"? / R: Todo lo que involucra la arquitectura del sistema o las decisiones técnicas que se toman al crearlo.

P: ¿Cuáles son las tres fallas ("las tres fallas") frente a la Ley del Cambio? / R: Escribir código que no se necesita, no hacer el código fácil de cambiar y ser demasiado genérico.

P: ¿Qué es la sobreingeniería (overengineering) según los hechos del apéndice? / R: Cuando tu diseño hace las cosas más complejas en vez de simplificarlas.

P: ¿Cuáles son los tres objetivos del diseño de software? / R: Escribir software lo más útil posible, permitir que siga siéndolo y diseñar sistemas que se creen y mantengan con la mayor facilidad.

P: ¿Cuál es el error más común y desastroso de los programadores? / R: Predecir algo del futuro cuando en realidad no pueden conocerlo.

P: ¿Cuántas veces debería existir idealmente cualquier pieza de información en el sistema? / R: Una sola vez.

## Preguntas de autoevaluación

1. ¿Por qué el apéndice no introduce ideas nuevas y qué función cumple? / R: Es una recopilación literal de los hechos, leyes, reglas y definiciones del libro; funciona como índice de referencia rápida que condensa el cuerpo teórico. (Lo que necesitas saber)

2. Según las reglas, ¿sobre qué base deben tomarse las decisiones de diseño y por qué? / R: Según lo que sabes ahora, no según lo que crees que pasará, porque hay cosas del futuro que no puedes conocer y estás más seguro decidiendo con información del presente. (Reglas)

3. ¿Qué caracteriza al "mejor diseño" en cuanto a cambio y entorno? / R: El que permite el mayor cambio en el entorno con el menor cambio en el software. (Reglas)

4. ¿Cuándo es aceptable "arreglar" algo según las reglas del apéndice? / R: Nunca, salvo que sea un problema real y tengas evidencia de que existe. (Reglas)

5. ¿Cómo se recomienda manejar la complejidad cuando aparece? / R: Rediseñando las piezas individuales en pasos pequeños, y preguntando "¿Qué problema intentas resolver?"; si es inarreglable y externa, poniéndole un wrapper simple. (Reglas)

6. ¿Qué relación existe entre la calidad del diseño y el tiempo? / R: La calidad del diseño debe ser proporcional al tiempo futuro en que el sistema seguirá ayudando a las personas. (Reglas)

7. ¿Qué criterios sirven para juzgar si una tecnología es "mala"? / R: Su potencial de supervivencia, su interoperabilidad y su atención a la calidad. (Reglas)

8. ¿Qué significa que "la simplicidad es relativa" y cuál es la pregunta clave de toda simplificación? / R: Que no es absoluta; la pregunta clave es "¿Cómo podría esto ser más fácil de manejar o más comprensible?". (Hechos)

## Puntos a dominar

- Reconocer las cuatro categorías del apéndice: hechos, leyes, reglas y definiciones.
- Recordar las cinco leyes nombradas más la Ecuación del Diseño de Software como Ley Primaria.
- Dominar que el propósito del software —ayudar a las personas— es la base de todo el sistema de leyes.
- Entender que las decisiones de diseño se basan en el presente conocido, no en predicciones del futuro.
- Asumir que la simplicidad y el mantenimiento priman sobre la facilidad de implementación inicial.
- Identificar las tres fallas y las formas de crear complejidad descritas en las reglas.
- Interiorizar que nada se da por funcional hasta que se ha probado (Ley de las Pruebas).
