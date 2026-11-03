# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 10 — Appendix A. The Laws of Software Design (Apéndice A. Las leyes del diseño de software)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

Este apéndice es un resumen condensado que recopila todas las leyes del diseño de software tratadas a lo largo del libro. No introduce conceptos nuevos: reúne en un único lugar las seis leyes y señala cuáles son las más importantes para tener presentes al diseñar software.

La tesis es que, aunque el libro discute muchos hechos e ideas, solo estos seis puntos constituyen las leyes del diseño de software. De todas ellas, las tres que más conviene recordar son el propósito del software, la forma reducida de la Ecuación del Diseño de Software y la Ley de la Simplicidad.

Sales sabiendo enunciar las seis leyes y, sobre todo, las dos frases que resumen lo más importante del diseño de software: que reducir el esfuerzo de mantenimiento importa más que reducir el de implementación, y que ese esfuerzo de mantenimiento es proporcional a la complejidad del sistema.

## Las seis leyes del diseño de software

1. **El propósito del software**: el propósito del software es ayudar a las personas.

2. **La Ecuación del Diseño de Software**: es la ley principal del diseño de software. Relaciona la deseabilidad de un cambio (D) con el valor ahora (Vn), el valor futuro (Vf), el esfuerzo de implementación (Ei) y el esfuerzo de mantenimiento (Em). Con el paso del tiempo la ecuación se reduce a una forma que demuestra que es más importante reducir el esfuerzo de mantenimiento que reducir el esfuerzo de implementación.

   - D: deseabilidad del cambio.
   - Vn: valor ahora (value now).
   - Vf: valor futuro (future value).
   - Ei: esfuerzo de implementación (effort of implementation).
   - Em: esfuerzo de mantenimiento (effort of maintenance).

3. **La Ley del Cambio (Law of Change)**: cuanto más tiempo exista tu programa, más probable es que cualquier parte de él tenga que cambiar.

4. **La Ley de la Probabilidad de Defectos (Law of Defect Probability)**: la posibilidad de introducir un defecto en tu programa es proporcional al tamaño de los cambios que le haces.

5. **La Ley de la Simplicidad (Law of Simplicity)**: la facilidad de mantenimiento de cualquier pieza de software es proporcional a la simplicidad de sus piezas individuales.

6. **La Ley de las Pruebas (Law of Testing)**: el grado en que conoces cómo se comporta tu software es el grado en que lo has probado con precisión.

## Las leyes más importantes y el resumen en dos frases

De las seis leyes, las más importantes a tener en mente son el propósito del software, la forma reducida de la Ecuación del Diseño de Software y la Ley de la Simplicidad.

El autor afirma que los hechos más importantes sobre el diseño de software podrían resumirse en dos frases simples:

- Es más importante reducir el esfuerzo de mantenimiento que reducir el esfuerzo de implementación.
- El esfuerzo de mantenimiento es proporcional a la complejidad del sistema.

Según el texto, con solo esas dos afirmaciones y la comprensión del propósito del software, se podría "re-evolucionar" toda la ciencia del diseño de software, siempre que además se entienda que la complejidad del sistema proviene de la complejidad de sus piezas individuales.

## Ideas clave

- El apéndice reúne las seis leyes del diseño de software del libro; no añade material nuevo.
- Ley 1: el propósito del software es ayudar a las personas.
- Ley 2 (Ecuación del Diseño de Software): su forma reducida muestra que reducir el mantenimiento pesa más que reducir la implementación.
- Ley 3 (del Cambio): a más tiempo de vida del programa, más probable es que cualquier parte deba cambiar.
- Ley 4 (de la Probabilidad de Defectos): el riesgo de defecto es proporcional al tamaño del cambio.
- Ley 5 (de la Simplicidad): la facilidad de mantenimiento es proporcional a la simplicidad de las piezas individuales.
- Ley 6 (de las Pruebas): conoces el comportamiento de tu software en la medida en que lo has probado con precisión.
- Las tres leyes más importantes: propósito del software, forma reducida de la Ecuación del Diseño de Software y Ley de la Simplicidad.
- La complejidad del sistema proviene de la complejidad de sus piezas individuales.
