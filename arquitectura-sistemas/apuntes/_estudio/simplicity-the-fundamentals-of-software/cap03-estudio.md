# The Driving Forces of Software Design (Las fuerzas que impulsan el diseño de software) — Estudio

## Tarjetas de repaso

P: ¿Cuál es el propósito de todo el software según el capítulo? / R: Ayudar a las personas (to help people); el autor lo llama "el Propósito del Software".

P: ¿A quién ayuda siempre el software? / R: A personas; nunca a objetos inanimados ni a la computadora. Incluso una biblioteca ayuda a programadores, que son personas.

P: Si un software ayuda a animales o plantas, ¿a quién ayuda en realidad? / R: A personas, ayudándolas a ayudar a animales o plantas.

P: ¿Cómo define "ayudar" el diccionario que cita el autor (Webster's New World Dictionary)? / R: Hacer más fácil para una persona hacer algo; ayudar, asistir; hacer parte del trabajo de; aliviar o compartir la labor.

P: ¿Qué es libre y qué es invariable en el propósito del software? / R: Con qué se ayuda es libre (agenda, libro, dieta); lo invariable es que el propósito sea ayudar.

P: ¿Por qué "ganar dinero" o "lucirse" no deben ser el propósito del software? / R: Diseñar solo con esos fines viola el propósito del software y probablemente lleva a software de menor calidad; el ingreso suele estar ligado a cuánto ayuda el software.

P: ¿Qué hipótesis plantea el autor sobre quién escribe buen software? / R: Que la capacidad de escribir buen software está limitada por la capacidad de concebir cómo ayudar a otra persona.

P: ¿Cuál es la pregunta rectora para priorizar funciones y evaluar cambios? / R: "¿Cuánto ayuda esto a los usuarios?"; la función que más ayude recibe la mayor prioridad.

P: En el ejemplo del editor de texto, ¿qué propósito simple se define? / R: "Ayudar a los programadores a editar texto".

P: ¿Qué se hace con una función si al preguntar cómo ayuda la respuesta es "no ayudaría"? / R: Se descarta de inmediato.

P: ¿Cuál es la pregunta inversa que se plantea para los errores (bugs)? / R: "¿Cómo estorba este error la edición de texto de los programadores?".

P: ¿Cuáles son los tres objetivos del diseño de software? / R: 1) Escribir software lo más útil posible; 2) que siga siendo lo más útil posible; 3) que sea fácil de crear y mantener por sus programadores.

P: ¿Cuál de los tres objetivos se piensa tradicionalmente como "el objetivo" del diseño? / R: El tercero (facilidad de creación y mantenimiento), aunque no se enuncie explícitamente.

P: ¿Cuál es el mayor obstáculo actual para escribir y mantener software útil? / R: La dificultad real del diseño y la programación; cuando es difícil, los programadores gastan tiempo en que "simplemente funcione" en vez de ayudar al usuario.

P: ¿Por qué la facilidad de mantenimiento no es opcional? / R: Es la condición para que el software siga siendo útil en el tiempo (segundo objetivo); sin el tercer objetivo no se logran los dos primeros.

## Preguntas de autoevaluación

P: ¿Por qué el autor afirma que el software nunca ayuda a la computadora? / R: Porque el software siempre existe para ayudar a personas; incluso al escribir bibliotecas se ayuda a programadores, que son personas. (Sección: El propósito del software)

P: ¿Puede "ganar dinero" ser un fin legítimo en algún sentido según el texto? / R: Sí, como fin personal o de la organización no está mal, pero no debe ser el propósito del software; además, el ingreso suele estar ligado a cuánto ayuda el software. (Sección: El propósito del software)

P: Ante la petición de atajos de teclado en el editor, ¿cómo responde la pregunta "cómo ayuda" y qué implica para la implementación? / R: Ayuda a los programadores a interactuar con el programa más rápido sin dejar de escribir; por eso la implementación debe ser rápida, pues ahí está el valor. (Sección: Aplicación en el mundo real)

P: ¿Qué cuatro utilidades aporta hacerse la pregunta "cómo ayuda esta función"? / R: Resuelve dudas de descripción/implementación, ayuda al equipo a acordar el valor de la función, hace evidente qué funciones son más importantes para priorizar, y permite decidir cuáles eliminar si el programa está inflado. (Sección: Aplicación en el mundo real)

P: ¿Por qué el autor incluye los objetivos primero y segundo si el tercero es el tradicional? / R: Para recordar que ser útil ahora y en el futuro es la motivación del tercero. (Sección: Los objetivos del diseño de software)

P: ¿Qué significa la frase "tan fácilmente como sea posible" en el tercer objetivo? / R: Que la idea es hacer los programas fáciles de crear y mantener, no difíciles ni complejos; aunque no todo sea fácil de inmediato, a largo plazo las decisiones deben facilitar la creación y el mantenimiento. (Sección: Los objetivos del diseño de software)

P: ¿Cómo se relacionan el primer objetivo (ser útil) y el tercero (mantenibilidad) cuando entran en conflicto? / R: A veces hacer el software más útil complica su mantenimiento, pero han estado más en conflicto de lo necesario: es posible un sistema mantenible y a la vez muy útil; sin mantenibilidad es muy difícil seguir siendo útil. (Sección: Los objetivos del diseño de software)

## Puntos a dominar

- Enunciar el Propósito del Software: ayudar a las personas, y nunca a objetos ni a la computadora.
- Definir la palabra "ayudar" en el sentido del capítulo (hacer más fácil que alguien haga algo).
- Distinguir lo libre (con qué se ayuda) de lo invariable (el propósito de ayudar).
- Explicar por qué "ganar dinero" o "lucirse" no deben ser el propósito del software.
- Aplicar la pregunta rectora "¿cuánto ayuda esto a los usuarios?" para priorizar y evaluar cambios.
- Reproducir el método del ejemplo: definir un propósito simple y evaluar cada función (y cada bug con la pregunta inversa).
- Enumerar y relacionar los tres objetivos del diseño de software.
- Justificar por qué la facilidad de mantenimiento es inseparable de que el software siga siendo útil.
