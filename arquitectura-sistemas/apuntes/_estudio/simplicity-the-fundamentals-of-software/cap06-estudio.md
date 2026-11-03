# Defects and Design (Defectos y diseño) — Estudio

## Tarjetas de repaso

P: ¿Cuántos defectos introducen aproximadamente los buenos programadores por líneas de código, y los mejores en las mejores circunstancias?
R: Los buenos, aproximadamente un defecto por cada 100 líneas; los mejores, uno por cada 1.000 líneas.

P: ¿Qué enuncia la Ley de la Probabilidad de Defectos?
R: La probabilidad de introducir un defecto en el programa es proporcional al tamaño de los cambios que le haces.

P: ¿Cuál es la versión informal de la Ley de la Probabilidad de Defectos?
R: "No puedes introducir nuevos bugs si no añades ni modificas código".

P: ¿Cuál es la cadena lógica que justifica hacer cambios pequeños?
R: Cambios pequeños = menos defectos = menos mantenimiento.

P: ¿Por qué existe el diseño de software según el capítulo?
R: Para resolver el conflicto entre la Ley del Cambio (el software debe cambiar) y el hecho de que todo cambio introduce defectos.

P: ¿Cómo define el autor el mejor diseño?
R: El que permite el mayor cambio en el entorno con el menor cambio en el software.

P: ¿Qué establece la regla "If It Ain't Broken..."?
R: Nunca "arregles" nada a menos que sea un problema y tengas evidencia de que el problema realmente existe.

P: ¿Qué pasa si arreglas problemas sin evidencia?
R: Sueles romper cosas: introduces cambios que traen defectos nuevos, desperdicias tiempo y añades complejidad sin motivo.

P: ¿Qué cuenta como evidencia de un problema real?
R: Por ejemplo, que cinco usuarios reporten la caída al pulsar el botón rojo, o comprobar tú mismo la caída.

P: Si muchos usuarios piden una función que el programa ya tiene, ¿cuál es el problema real?
R: Que los usuarios no encuentran fácilmente las funciones que necesitan; eso sí debe arreglarse.

P: ¿Cómo se decide si un reporte de bug es realmente un bug cuando el programa se comporta como se pretendía?
R: Manda la mayoría: si un número significativo de usuarios lo cree, es un bug; si solo una minoría ínfima (uno o dos), no lo es.

P: ¿Qué es la optimización prematura y por qué es un error?
R: Optimizar el código antes de saber que es lento; resuelve un problema que no existe.

P: Según el capítulo, ¿dónde debe preocuparte la velocidad?
R: Solo en las partes que puedas demostrar que causan un problema real de rendimiento a los usuarios; para el resto priman flexibilidad y simplicidad.

P: ¿Qué enuncia la regla "Don't Repeat Yourself"?
R: En cualquier sistema concreto, toda pieza de información debería existir, idealmente, una sola vez.

P: ¿Por qué DRY reduce defectos y mejora la flexibilidad?
R: Por la Ley de la Probabilidad de Defectos (reutilizar implica escribir/cambiar menos código) y porque permite modificar el comportamiento en un solo lugar.

## Preguntas de autoevaluación

P: ¿Por qué, sin importar el nivel del programador, escribir más código implica más defectos?
R: Porque ningún programador es perfecto y la tasa de defectos es proporcional a la cantidad de líneas; más código escrito introduce más defectos. (Lo que necesitas saber)

P: Explica el conflicto entre la Ley del Cambio y la Ley de la Probabilidad de Defectos.
R: El software tiene que cambiar, pero todo cambio introduce defectos; equilibrar ambas leyes exige la inteligencia del diseñador y justifica el diseño. (La Ley de la Probabilidad de Defectos)

P: ¿Cómo distingue el autor un reporte de usuario que es un problema real de uno que no lo es?
R: Un reporte no implica problema: el usuario puede pedir una función existente o reportar un comportamiento intencionado; se evalúa con evidencia y por mayoría de usuarios. (If It Ain't Broken...)

P: En el ejemplo del programa que ordena palabras, ¿por qué no hay un problema que arreglar?
R: Porque un programa que ordena palabras alfabéticamente ya puede ordenar letras; el usuario cree que hay un problema cuando no lo hay. (If It Ain't Broken...)

P: ¿Qué deben priorizar las partes del código que no demuestran un problema de rendimiento?
R: Flexibilidad y simplicidad, no la rapidez. (If It Ain't Broken...)

P: Con el ejemplo del campo "Password" en 100 pantallas, ¿qué ventaja aporta DRY?
R: Si el nombre está en un único lugar central, cambiarlo a "Passcode" es un cambio de una línea; si está escrito en las 100 pantallas, requiere 100 cambios. (Don't Repeat Yourself)

P: ¿Cómo aplica DRY a los bloques de código y por qué conviene?
R: En vez de copiar y pegar, se usan mecanismos que hacen que un fragmento use, llame o incluya a otro existente; así se escribe menos código (menos defectos) y se cambia en un solo lugar (más flexibilidad). (Don't Repeat Yourself)

## Puntos a dominar

- Enunciar la Ley de la Probabilidad de Defectos y su versión informal.
- Explicar la cadena: cambios pequeños = menos defectos = menos mantenimiento.
- Justificar por qué el diseño nace del conflicto entre la Ley del Cambio y los defectos.
- Recitar la definición del mejor diseño: mayor cambio en el entorno con el menor cambio en el software.
- Aplicar la regla "If It Ain't Broken...": exigir evidencia real antes de arreglar.
- Reconocer la optimización prematura y cuándo sí optimizar (problema de rendimiento demostrado).
- Aplicar DRY a información y a código: centralizar para reducir defectos y ganar flexibilidad.
