# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 15 — Putting It All Together (Juntándolo todo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo breve, escrito por Kent Beck, cierra el libro y cambia el registro: ya no enseña técnicas, sino el *ritmo* del refactoring. La tesis central es que conocer las refactorizaciones, el catálogo, las listas de verificación y el testing es solo el principio —"la puerta que debes atravesar"—. Dominar el refactoring no es saber ejecutar cada técnica, sino saber cuándo usarlas y cuándo no, cuándo empezar y cuándo parar. "Es el ritmo lo que hace el refactoring, no las notas individuales" (PDF p. 333).

Sales sabiendo que el refactoring es una habilidad aprendible, no mística, cuyos componentes ya has leído en el libro. Lo señalan dos señales: la calma —la confianza de que, por mal que esté el código, puedes mejorarlo lo suficiente para seguir avanzando— y, sobre todo, la capacidad de *parar con confianza*, que Beck llama "la jugada más fuerte del repertorio del refactorizador" (PDF p. 333).

El capítulo transmite una actitud: fijar una meta, avanzar en pasos pequeños y seguros respaldados por tests, y detenerse sin vergüenza cuando se agota la confianza. Beck ilustra con su propio récord de esperar nueve años para completar la segunda mitad de una refactorización: la intuición llega cuando llega, y entonces el siguiente paso es claro.

## Aprender la habilidad: las pautas

Beck presenta el refactoring como skill aprendible y da un conjunto de pautas prácticas:

- **Acostúmbrate a elegir una meta.** Cuando el código huele mal, decide eliminar el problema y marcha hacia esa meta. No refactorizas por verdad y belleza, sino para hacer tu mundo más fácil de entender y recuperar el control de un programa que se ha soltado.
- **Para cuando no estés seguro.** Si llega un momento en que no puedes demostrar que tus cambios preservan la semántica del programa, detente. Si el código ya está mejor, publica el progreso; si no, descarta los cambios.
- **Vuelve atrás (backtrack).** La disciplina es difícil de aprender y fácil de perder. Beck admite hacer dos, tres o cuatro refactorizaciones seguidas sin volver a correr los tests; entonces falla una prueba y no sabe cuál cambio la rompió.

## El atajo tentador: no depures, vuelve atrás

Cuando un test falla tras varios cambios, la tentación es depurar para salir del apuro. Beck insiste: detente, estás fuera de control. Vuelve a la última configuración buena conocida y reproduce los cambios uno a uno, corriendo los tests después de cada uno.

El argumento es de coste acotado frente a coste incierto: si has refactorizado una hora, reproducir lo hecho toma unos diez minutos y garantiza volver a la vía; si avanzas depurando, puedes tardar cinco segundos o dos horas. Beck reconoce lo brutalmente difícil que es seguir su propio consejo: su récord de no hacerlo fue de cuatro horas y tres intentos separados, perdiendo el control una y otra vez.

## Dúos (duets)

"Por el amor de Dios, refactoriza con alguien" (PDF p. 334). Las ventajas de trabajar en pareja se multiplican en el refactoring, donde hay una prima (un valor especial) sobre varias cosas:

- Trabajar con cuidado y metódicamente: tu compañero te mantiene avanzando paso a paso, y tú a él.
- Ver consecuencias de largo alcance: el compañero ve lo que tú no ves y sabe lo que tú no sabes.
- Saber cuándo parar: si tu compañero no entiende lo que haces, es señal segura de que tú tampoco.
- La confianza serena: el compañero te anima con suavidad cuando tú te detendrías.

Otro aspecto es *hablar*: hablar de lo que crees que va a pasar (para apuntar en la misma dirección), de lo que está pasando (para detectar problemas pronto) y de lo que acaba de pasar (para aprender). Esa conversación fija en tu mente dónde encaja cada refactorización individual dentro del ritmo del refactoring.

## No a los grandes refactorings; sí al mordisqueo

Al conocer los smells y las refactorizaciones que los eliminan, verás nuevas posibilidades incluso en código con el que llevas años trabajando, y querrás limpiarlo todo de golpe. No lo hagas. Ningún jefe quiere oír que el equipo debe parar tres meses para limpiar el desorden, y con razón: "un gran refactoring es una receta para el desastre" (PDF p. 335).

En su lugar, disciplínate para ir mordisqueando el problema. Cuando vayas a añadir funcionalidad a una zona, dedica unos minutos a limpiarla primero; si necesitas añadir tests para limpiar con confianza, añádelos. Refactorizar primero es menos peligroso que añadir código nuevo: tocar el código te recordará cómo funciona, terminarás antes y la próxima vez que pases por ahí lucirá mejor.

## Los dos sombreros

Al refactorizar inevitablemente descubrirás casos en que el código no funciona bien, y estarás absolutamente seguro de ello. Resiste la tentación de arreglarlo ahí mismo. Cuando refactorizas, tu meta es dejar el código calculando exactamente las mismas respuestas que daba cuando lo encontraste: nada más, nada menos. Beck recomienda mantener una lista —él siempre tiene una ficha (index card) junto al ordenador— de cosas a cambiar luego: tests que añadir o modificar, refactorizaciones no relacionadas, documentos que escribir, diagramas que dibujar. Así no pierdes esas ideas, pero tampoco dejas que estorben lo que haces ahora.

## Ideas clave

- Las técnicas son solo el comienzo: lo que hace el refactoring es el *ritmo*, no las notas individuales.
- Parar con confianza es la jugada más fuerte; si el código ya está mejor, intégralo y publícalo; si no, descártalo.
- Elige una meta clara y avanza en pasos pequeños y seguros respaldados por los tests.
- Cuando no estés seguro de preservar la semántica, detente.
- Ante un fallo tras varios cambios, no depures: vuelve a la última configuración buena y reproduce los cambios uno a uno.
- Refactoriza en pareja: cuidado metódico, consecuencias de largo alcance, saber cuándo parar y confianza serena; y habla continuamente.
- Evita los grandes refactorings; mordisquea el problema limpiando antes de añadir funcionalidad.
- Nunca olvides los dos sombreros: al refactorizar no cambies el comportamiento; anota en una lista lo que harás después.
