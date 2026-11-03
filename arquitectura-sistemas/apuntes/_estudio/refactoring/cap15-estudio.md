# Putting It All Together (Juntándolo todo) — Estudio

## Tarjetas de repaso

- P: ¿Cuál es la tesis central del capítulo 15? / R: Que las técnicas, el catálogo, las listas de verificación y el testing son solo el principio —"la puerta que debes atravesar"—; dominar el refactoring es saber cuándo usar las técnicas y cuándo no, cuándo empezar y cuándo parar.
- P: Según la cita de Beck, ¿qué hace el refactoring? / R: "Es el ritmo lo que hace el refactoring, no las notas individuales" (PDF p. 333): el ritmo, no las técnicas aisladas.
- P: ¿Cuáles son las dos señales de que se domina el refactoring? / R: La calma —confianza de que, por mal que esté el código, puedes mejorarlo lo suficiente para seguir— y la capacidad de parar con confianza.
- P: ¿Qué es "la jugada más fuerte del repertorio del refactorizador"? / R: Parar con confianza (PDF p. 333).
- P: ¿Qué significa "acostúmbrate a elegir una meta"? / R: Cuando el código huele mal, decidir eliminar el problema y marchar hacia esa meta; no refactorizas por verdad y belleza, sino para hacer tu mundo más fácil de entender y recuperar el control.
- P: ¿Cuándo debes parar al refactorizar? / R: Cuando no estés seguro, es decir, cuando no puedas demostrar que tus cambios preservan la semántica del programa.
- P: Si paras por inseguridad, ¿qué haces con los cambios? / R: Si el código ya está mejor, publicas el progreso; si no, descartas los cambios.
- P: ¿Qué es "volver atrás" (backtrack)? / R: Ante un fallo de test tras varios cambios, volver a la última configuración buena conocida y reproducir los cambios uno a uno, corriendo los tests después de cada uno.
- P: ¿Por qué no depurar cuando falla un test tras varios cambios? / R: Es un argumento de coste acotado frente a incierto: reproducir una hora de trabajo toma unos diez minutos y garantiza volver a la vía; depurar puede tardar cinco segundos o dos horas.
- P: ¿Qué cuatro ventajas tiene refactorizar en pareja (dúos)? / R: Trabajar con cuidado y método, ver consecuencias de largo alcance, saber cuándo parar y la confianza serena.
- P: En un dúo, ¿qué tres cosas conviene hablar? / R: Lo que crees que va a pasar (apuntar igual), lo que está pasando (detectar problemas pronto) y lo que acaba de pasar (aprender).
- P: ¿Por qué evitar los grandes refactorings? / R: Porque "un gran refactoring es una receta para el desastre" (PDF p. 335) y ningún jefe quiere parar meses para limpiar; es mejor ir mordisqueando el problema.
- P: ¿Por qué refactorizar primero es menos peligroso que añadir código nuevo? / R: Porque tocar el código te recuerda cómo funciona, terminas antes y la próxima vez que pases por ahí lucirá mejor.
- P: ¿Qué son "los dos sombreros"? / R: La separación entre refactorizar (dejar el código calculando exactamente las mismas respuestas) y cambiar el comportamiento; no mezclar ambas tareas.
- P: ¿Cómo gestiona Beck las ideas de cambios que surgen al refactorizar? / R: Mantiene una lista (una ficha/index card junto al ordenador) con tests, refactorizaciones no relacionadas, documentos y diagramas para hacer luego.

## Preguntas de autoevaluación

- P: ¿Por qué dice el capítulo que conocer todas las técnicas no basta para dominar el refactoring? / R: Porque las técnicas son solo el comienzo, "la puerta que debes atravesar"; dominar el refactoring es saber cuándo aplicarlas, cuándo empezar y cuándo parar —es el ritmo, no las notas individuales. (Sección "Lo que necesitas saber")
- P: ¿Qué debes hacer si, tras varios cambios, un test falla y no sabes cuál lo rompió? / R: No depurar; volver a la última configuración buena conocida y reproducir los cambios uno a uno, corriendo los tests tras cada uno. (Sección "El atajo tentador: no depures, vuelve atrás")
- P: ¿Cómo ayuda un compañero a saber cuándo parar? / R: Si tu compañero no entiende lo que haces, es señal segura de que tú tampoco; además te anima con suavidad cuando tú te detendrías (confianza serena). (Sección "Dúos (duets)")
- P: ¿Cuál es la estrategia recomendada frente a la tentación de limpiar todo el código de golpe? / R: Mordisquear el problema: cuando vayas a añadir funcionalidad a una zona, dedica unos minutos a limpiarla primero, añadiendo tests si hace falta para limpiar con confianza. (Sección "No a los grandes refactorings; sí al mordisqueo")
- P: Al refactorizar descubres un bug del que estás absolutamente seguro, ¿qué haces? / R: Resistir la tentación de arreglarlo ahí mismo; la meta es que el código calcule exactamente las mismas respuestas. Anótalo en la lista para cambiarlo después. (Sección "Los dos sombreros")
- P: ¿Qué ejemplo personal usa Beck para ilustrar que la intuición llega cuando llega? / R: Su récord de esperar nueve años para completar la segunda mitad de una refactorización; cuando llega la intuición, el siguiente paso es claro. (Sección "Lo que necesitas saber")
- P: ¿Qué cuantifica el coste de volver atrás frente a depurar en el ejemplo de Beck? / R: Reproducir una hora de refactoring toma unos diez minutos y garantiza volver a la vía; depurar puede tardar entre cinco segundos y dos horas. Su récord de no seguir el consejo fue cuatro horas y tres intentos. (Sección "El atajo tentador: no depures, vuelve atrás")

## Puntos a dominar

- Entender el refactoring como una habilidad aprendible cuyo valor está en el ritmo, no en técnicas aisladas.
- Reconocer las dos señales de dominio: la calma y la capacidad de parar con confianza.
- Elegir siempre una meta clara y avanzar en pasos pequeños y seguros respaldados por tests.
- Parar cuando no se pueda demostrar que los cambios preservan la semántica; publicar si hay mejora, descartar si no.
- Preferir volver atrás a la última configuración buena en lugar de depurar tras un fallo.
- Aprovechar los dúos: cuidado metódico, consecuencias de largo alcance, saber cuándo parar y hablar continuamente.
- Mordisquear el problema en vez de emprender grandes refactorings.
- Mantener separados los dos sombreros y anotar en una lista lo que se hará después.
