# Capítulo 5 — Toward a Catalog of Refactorings (Hacia un catálogo de refactorizaciones) — Estudio

## Tarjetas de repaso

P: ¿Qué papel cumple el catálogo de refactorizaciones (caps. 5-12)?
R: Es un punto de partida de referencia, no una colección exhaustiva ni infalible; nació de las notas que Fowler tomó al refactorizar durante años.

P: ¿Cuáles son las cinco partes del formato de cada refactorización?
R: Nombre (name), resumen (summary), motivación (motivation), mecánica (mechanics) y ejemplos (examples).

P: ¿Para qué sirve el nombre (name) de una refactorización?
R: Para construir un vocabulario de refactorizaciones; es el nombre que se usa en el resto del libro.

P: ¿Qué contiene el resumen (summary)?
R: Una breve descripción de la situación en que se necesita y de lo que hace, con un enunciado corto del problema y un boceto de antes y después, en código o UML según lo que mejor transmita la esencia.

P: ¿Desde qué perspectiva se dibujan los diagramas UML del libro?
R: Desde la perspectiva de implementación.

P: ¿Cómo describe Fowler la mecánica (mechanics) y cuál es su regla de oro?
R: Es una descripción concisa, paso a paso, con pasos lo más pequeños posible; la regla de oro es probar después de cada paso, y sirve también como recordatorio y checklist.

P: ¿Qué naturaleza tienen los ejemplos del catálogo?
R: Son "de libro de texto", deliberadamente simples, pensados solo para ilustrar la refactorización en discusión; el código final suele seguir teniendo problemas y no son modelos de buen diseño de objetos de negocio.

P: ¿Por qué usa Fowler `double` para valores monetarios y qué recomienda en su lugar?
R: Lo usa solo por simplicidad; desaconseja firmemente usar `double` para dinero en software comercial y recomienda el patrón Quantity.

P: ¿En qué versión de Java están la mayoría de los ejemplos y cómo se gestionan las diferencias?
R: En Java 1.1 (la más usada comercialmente al escribir el libro); cuando una refactorización difiere en Java 2, como Encapsulate Collection, explica ambos casos.

P: ¿Para qué se usa el código en negrita en los ejemplos?
R: Para resaltar el código cambiado cuando queda oculto entre código sin cambios; no se aplica a todo el código modificado porque demasiada negrita anula el propósito.

P: Al encontrar referencias, ¿por qué conviene apoyarse en el ordenador?
R: Para reducir las posibilidades de pasar por alto una referencia y hacerlo más rápido que inspeccionando el código a ojo.

P: ¿Qué riesgos tiene usar el compilador para encontrar referencias en lenguajes fuertemente tipados?
R: Se confunde con características declaradas varias veces en una jerarquía de herencia, puede ser demasiado lento y no detecta usos de la API de reflexión.

P: ¿Qué parte del refactoring considera Fowler muy estable y por qué?
R: La técnica básica de pasos pequeños y pruebas frecuentes, bien probada durante años, especialmente en la comunidad Smalltalk.

P: ¿Para qué tipo de software están pensadas estas refactorizaciones?
R: Para software de un solo proceso; espera futuras refactorizaciones para programación concurrente y distribuida, que serán diferentes.

P: ¿Cuál es la relación entre patrones y refactorizaciones?
R: Los patrones son adonde se quiere llegar y las refactorizaciones son las maneras de llegar allí; como dice la Banda de los Cuatro, los patrones aportan objetivos para tus refactorizaciones.

## Preguntas de autoevaluación

P: ¿Qué dos objetivos persigue este capítulo como puerta de entrada al catálogo?
R: Presentar el formato estándar con que se describe cada refactorización (para que funcione como referencia) y dar contexto honesto sobre alcance, convenciones de código y madurez de las técnicas. (Lo que necesitas saber)

P: ¿Por qué la mecánica se escribe de forma deliberadamente escueta, sin explicar el porqué de cada paso?
R: Porque sirve como recordatorio y checklist cuando ya se conoce la técnica; las explicaciones más extensas se dejan para los ejemplos. (Formato de las refactorizaciones)

P: Si al aplicar la mecánica aparece un bug, ¿cómo recomienda proceder Fowler?
R: Aunque él suele dar pasos más grandes, si aparece un bug retrocede y vuelve a los pasos muy pequeños, probando tras cada uno. (Formato de las refactorizaciones)

P: ¿Por qué no se deben tomar los ejemplos como sugerencias de diseño de objetos de negocio?
R: Porque son casos simplificados para ilustrar una sola refactorización y el código suele seguir con problemas que exigirían otras refactorizaciones; cada entrada se mantiene autocontenida por su papel de referencia. (Formato de las refactorizaciones)

P: ¿Por qué no conviene hacer búsqueda y reemplazo a ciegas al encontrar referencias?
R: Porque hay que inspeccionar cada referencia para confirmar que se refiere a lo que se reemplaza; reusar el mismo nombre en distintas clases o firmas distintas en la misma clase aumenta el riesgo de error. (Encontrar referencias)

P: ¿Cuándo es útil usar el compilador para encontrar referencias y cuándo no?
R: Es útil cuando se piensa eliminar la característica, dejando que el compilador atrape las referencias colgantes; no sirve si solo se quieren ver todos los usos para decidir qué hacer, caso en que hay que usar búsqueda de texto. (Encontrar referencias)

P: ¿Por qué la reflexión es una razón para desconfiar al refactorizar?
R: Porque el compilador no detecta usos de la API de reflexión; con reflexión hay que buscar por texto y poner más peso en las pruebas. (Encontrar referencias)

P: ¿Qué dilema plantea Fowler sobre la madurez de las refactorizaciones?
R: El dilema de cuándo publicar: hacerlo pronto difunde antes las ideas, pero publicar ideas a medio cocer puede causar problemas a quienes las usen; aun así considera el catálogo útil como punto de partida. (¿Qué tan maduras son estas refactorizaciones?)

## Puntos a dominar

- Reconocer y nombrar las cinco partes del formato de una refactorización: nombre, resumen, motivación, mecánica y ejemplos.
- Entender que la mecánica se aplica con pasos muy pequeños, probando tras cada uno, y sirve como checklist.
- Interpretar los ejemplos como ilustraciones simplificadas, no como diseño de referencia.
- Conocer las convenciones de código: `double` solo por simplicidad (patrón Quantity en producción), Java 1.1 con notas para Java 2 y negrita para cambios.
- Distinguir las estrategias para encontrar referencias (búsqueda de texto frente a compilador) y sus limitaciones ante herencia, lentitud y reflexión.
- Asumir que las recetas están pensadas para software de un solo proceso y deben adaptarse a cada circunstancia.
- Relacionar patrones y refactorizaciones: los patrones son el destino, las refactorizaciones el camino.
