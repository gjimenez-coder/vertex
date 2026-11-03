# Complexity (Complejidad) — Estudio

## Tarjetas de repaso

P: ¿Por qué la complejidad no crece de forma lineal? / R: Porque se acumula sobre sí misma: cada función nueva debe coordinarse con todas las existentes, así que el coste de añadir funciones aumenta con el tamaño del sistema.

P: ¿Cuáles son las vías habituales de introducir complejidad? / R: Expandir el propósito, añadir programadores, cambiar lo que no hace falta, quedar atado a tecnologías malas, el malentendido, el diseño pobre o ausente y reinventar la rueda.

P: ¿Qué efecto tiene añadir programadores a un proyecto? / R: Suma complejidad en vez de quitarla (referencia a *The Mythical Man-Month*); es más probable el éxito con un grupo pequeño de expertos que con uno grande de inexpertos.

P: ¿Qué costes conlleva cambiar algo que no necesita cambiarse? / R: Posibilidad de bugs y costes de decisión, implementación, validación, seguimiento y pruebas; por eso hay que decidir de forma informada, no por capricho.

P: ¿Cuándo es aceptable reinventar la rueda? / R: Cuando necesitas algo que aún no existe, cuando todas las ruedas existentes te encierran, cuando son incapaces de cubrir tus necesidades, o cuando no se mantienen y no puedes tomar su mantenimiento.

P: ¿Qué relación debe tener el propósito del programa con el del usuario? / R: Idealmente el propósito del programa debe coincidir casi con las mismas palabras que usaría el usuario para describir el suyo.

P: ¿Cuáles son los tres factores para detectar una tecnología mala? / R: El potencial de supervivencia (survival potential), la interoperabilidad (facilidad para abandonarla) y la atención a la calidad.

P: ¿Cómo se evalúa el potencial de supervivencia de una tecnología? / R: Por el historial reciente de versiones, la respuesta a reportes de bugs, la actividad de la comunidad y si hay un solo proveedor o adopción amplia.

P: ¿Qué distingue la popularidad válida de la que no lo es? / R: La popularidad válida tiene múltiples estándares e implementaciones (ejemplo: C); la no válida proviene de un monopolio o de la obligación con un solo proveedor.

P: ¿Qué suele indicar una complejidad irresoluble? / R: Un error de diseño en un nivel muy por debajo de donde aparece la complejidad; hay que retroceder y mirar qué subyace (analogía de las ruedas cuadradas).

P: ¿Qué pregunta clave hay que hacer ante una petición confusa? / R: "¿Qué problema intentas resolver?"; al entenderlo del todo aparece la solución simple, descartando suposiciones.

P: ¿Cómo se maneja la complejidad existente? / R: Rediseñando las piezas en pasos pequeños, cada arreglo lo más pequeño posible sin introducir más complejidad, avanzando hacia un sistema algo más simple y repitiendo.

P: ¿Qué es la Ley del Cambio (Law of Change) en este contexto? / R: Obliga a seguir adaptando la funcionalidad so pena de perder usuarios, por lo que no se puede dejar de escribir funciones para dedicarse solo a rediseñar.

P: ¿Qué hacer con la complejidad irreparable, como la del hardware? / R: Ocultarla tras un envoltorio simple de usar y entender.

P: ¿Por qué reescribir desde cero es casi siempre un error? / R: Es una admisión de fracaso como diseñador; un sistema bien diseñado y mantenido no tiene por qué reescribirse, igual que un rascacielos bien construido no tiene por qué caerse.

## Preguntas de autoevaluación

P: ¿Por qué un mal diseño hace que cada función multiplique la complejidad en vez de sumarla? / R: Porque el mal diseño equivale a "no planificar para el cambio"; sin esa planificación, incorporar cada función obliga a reajustar el resto en vez de añadir solo un poco. (Sección: Cómo se añade complejidad)

P: ¿Quién debe decidir qué hace un programa y por qué no marketing o gestión? / R: El diseñador o gestor técnico es responsable de que no se viole el propósito; marketing o gestión a veces persiguen metas ajenas ("ser lindo", "usar la última tecnología") que no deben decidir el qué. (Sección: Complejidad y propósito)

P: ¿Cómo ayuda la interoperabilidad a no quedar encerrado en una tecnología? / R: Si interactúas por una vía estándar (ejemplo: estándares para hablar con una base de datos), cambiar a otro sistema que siga el mismo estándar requiere cambios menores; si no, quedas encerrado y tendrás que reescribir. (Sección: Tecnologías malas)

P: ¿Son los problemas inherentemente complejos una excusa para soluciones complejas? / R: No; problemas como el corrector ortográfico o el ajedrez por computadora son complejos, pero no obligan a una solución compleja: exigen más esfuerzo para simplificar, y ayuda escribirlos o dibujarlos en papel. (Sección: Problemas complejos)

P: ¿Cuál fue la estrategia de rediseño de Bugzilla para soportar varias bases de datos? / R: En vez de llenar el código de `if`, rediseñaron en pasos: usar comandos estándar un archivo a la vez, crear funciones que devuelvan el comando correcto para los no estándar, dejar de usar funciones específicas de OldDB y rediseñar el instalador; cada paso probado, hasta soportar cuatro bases de datos. (Sección: Manejar la complejidad)

P: ¿Cuál es el mayor peligro al arreglar una parte compleja y por qué fracasan muchas reescrituras? / R: Que el propio arreglo añada complejidad; por eso fracasan tantas reescrituras, que intentan un salto grande en lugar de pasos pequeños hacia un sistema algo más simple. (Sección: Manejar la complejidad)

P: ¿Qué cinco condiciones deben cumplirse todas para que reescribir sea aceptable? / R: Una estimación precisa con experimentos reales de que reescribir es más eficiente; muchísimo tiempo; ser mejor diseñador que el original; diseñar en pasos simples con feedback de usuarios; y recursos para mantener lo existente y diseñar lo nuevo a la vez. (Sección: Reescribir)

## Puntos a dominar

- Explicar por qué la complejidad se acumula sobre sí misma y encarece cada función nueva.
- Enumerar las siete vías de introducir complejidad y reconocerlas en un proyecto propio.
- Mantener el software ceñido a su propósito básico y acercarlo al propósito del usuario.
- Evaluar una tecnología por su potencial de supervivencia, interoperabilidad y atención a la calidad antes de adoptarla.
- Ante complejidad irresoluble, retroceder a niveles más profundos y preguntar "¿qué problema intentas resolver?".
- Manejar la complejidad con rediseños en pasos pequeños que no introduzcan más complejidad, alternando rediseño y funciones.
- Ocultar la complejidad inevitable (hardware) tras un envoltorio simple.
- Verificar las cinco condiciones antes de plantear una reescritura y, si falta alguna, rediseñar en pasos en lugar de reescribir.
