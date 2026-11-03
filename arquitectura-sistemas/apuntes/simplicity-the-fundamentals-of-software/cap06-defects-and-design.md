# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 6 — Defects and Design (Defectos y diseño)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo conecta la aparición de defectos con la necesidad del diseño de software. Parte de un hecho incómodo: ningún programador es perfecto. Los buenos programadores introducen aproximadamente un defecto por cada 100 líneas de código; los mejores, en las mejores circunstancias posibles, uno por cada 1.000 líneas. La consecuencia es directa: cuanto más código escribes, más defectos introduces, sin importar tu nivel.

A partir de ahí el autor formula la Ley de la Probabilidad de Defectos y la usa para justificar por qué conviene hacer cambios pequeños, por qué solo deben corregirse problemas con evidencia real, y por qué no hay que repetir información ni código. Sales sabiendo que el diseño existe precisamente para resolver el conflicto entre la necesidad de cambiar el software y el hecho de que todo cambio introduce defectos.

La tesis central es que el mejor diseño es el que permite el mayor cambio en el entorno con el menor cambio en el software. Según el autor, eso resume gran parte de lo que hoy se sabe sobre buen diseño de software.

## La Ley de la Probabilidad de Defectos

El enunciado formal es:

> La probabilidad de introducir un defecto en tu programa es proporcional al tamaño de los cambios que le haces (PDF p. 53).

De forma informal se expresa como "no puedes introducir nuevos bugs si no añades ni modificas código". Las implicaciones:

- Los defectos violan el propósito del software (ayudar a las personas), así que deben evitarse.
- Corregir defectos es una forma de mantenimiento; más defectos significan más esfuerzo de mantenimiento.
- La cadena lógica es: cambios pequeños = menos defectos = menos mantenimiento.

Esta ley entra en conflicto con la Ley del Cambio: el software tiene que cambiar, pero cambiarlo introduce defectos. Equilibrar ambas leyes es lo que exige la inteligencia del diseñador y lo que explica por qué necesitamos diseño. De ese conflicto surge la definición del diseño ideal:

> El mejor diseño es el que permite el mayor cambio en el entorno con el menor cambio en el software (PDF p. 53).

## If It Ain't Broken... (Si no está roto...)

La regla relacionada que muchos ingenieros olvidan:

> Nunca "arregles" nada a menos que sea un problema y tengas evidencia de que el problema realmente existe (PDF p. 54).

Arreglar problemas sin evidencia suele romper cosas: introduces cambios que traen defectos nuevos, desperdicias tiempo y añades complejidad sin motivo.

¿Qué cuenta como evidencia? Por ejemplo, que cinco usuarios reporten que el programa se cae al pulsar el botón rojo, o comprobar tú mismo la caída. Pero que un usuario reporte algo no significa que sea un problema:

- El usuario puede pedir una función que el programa ya tiene. Ejemplo: un programa que ordena palabras alfabéticamente ya puede ordenar letras; el usuario cree que hay un problema cuando no lo hay.
- Si recibes muchas peticiones así, significa que los usuarios no encuentran fácilmente las funciones que necesitan: eso sí es algo que debes arreglar.
- A veces un usuario reporta un bug cuando el programa se comporta como se pretendía. Aquí manda la mayoría: si un número significativo de usuarios cree que es un bug, es un bug; si solo lo cree una minoría ínfima (uno o dos), no lo es.

El error más famoso en esta área es la optimización prematura: algunos desarrolladores optimizan el código antes de saber que es lento. Es como una organización benéfica enviando comida a los ricos diciendo "solo queríamos ayudar". Resuelven un problema que no existe.

Las únicas partes donde debe preocuparte la velocidad son aquellas que puedas demostrar que causan un problema real de rendimiento a los usuarios. Para el resto del código, las prioridades son la flexibilidad y la simplicidad, no la rapidez. La forma de cumplir la regla es simple: consigue evidencia real de que un problema es válido antes de abordarlo.

## Don't Repeat Yourself (No te repitas)

Probablemente la regla más conocida del diseño de software, y aunque este libro no es su origen, es válida:

> En cualquier sistema concreto, toda pieza de información debería existir, idealmente, una sola vez (PDF p. 55).

Ejemplo: un campo "Password" que aparece en 100 pantallas de la interfaz. Si el nombre está almacenado en un único lugar central del código, cambiarlo a "Passcode" es un cambio de una línea. Si se escribió manualmente en las 100 pantallas, hacen falta 100 cambios.

La regla también aplica a bloques de código: no se debe copiar y pegar código, sino usar los mecanismos de programación que permiten que un fragmento "use", "llame" o "incluya" a otro fragmento existente. Razones:

- Por la Ley de la Probabilidad de Defectos: reutilizar código existente significa escribir o cambiar menos código al añadir funciones, y por tanto introducir menos defectos.
- Por flexibilidad: si hay que cambiar el funcionamiento, se modifica el código en un solo lugar en vez de en muchos.

Gran parte del buen diseño se basa en esta regla: cuanto más hábilmente logres que un código use otro y centralices la información, mejor será tu diseño. Es otra área donde la inteligencia del programador entra en juego.

## Ideas clave

- La probabilidad de introducir un defecto es proporcional al tamaño del cambio (Ley de la Probabilidad de Defectos).
- Cambios pequeños = menos defectos = menos mantenimiento.
- El conflicto entre la Ley del Cambio y la de los defectos es lo que justifica el diseño.
- El mejor diseño permite el mayor cambio en el entorno con el menor cambio en el software.
- Nunca arregles nada sin evidencia de que el problema existe realmente.
- Si muchos reportan una función ausente que ya existe, el problema es que no la encuentran: eso sí hay que arreglarlo.
- La optimización prematura resuelve problemas inexistentes; optimiza solo donde demuestres un problema real de rendimiento.
- Toda información debería existir una sola vez; centralizar código e información reduce defectos y mejora la flexibilidad.
