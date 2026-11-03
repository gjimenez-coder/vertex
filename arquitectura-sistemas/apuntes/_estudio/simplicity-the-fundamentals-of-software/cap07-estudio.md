# Simplicity (Simplicidad) — Estudio

## Tarjetas de repaso

P: ¿Qué enuncia la Ley de la Simplicidad?
R: La facilidad de mantenimiento de cualquier pieza de software es proporcional a la simplicidad de sus piezas individuales; cuanto más simples sean las piezas, más fácil será cambiar las cosas en el futuro.

P: ¿Por qué la ley habla de las piezas individuales y no del sistema completo?
R: Porque un programa de tamaño medio es tan complejo que ningún humano puede comprenderlo todo de una vez; siempre hay una estructura grande y compleja, y lo que importa es que cada pieza se entienda al mirarla.

P: ¿Cuál es la meta de mantenimiento según el capítulo?
R: El mantenimiento perfecto: poder hacer cambio total o código nuevo infinito sin dificultad, aunque sea imposible, es la meta hacia la que se trabaja.

P: En la analogía de la arquitectura, ¿qué ventaja tienen las vigas pequeñas frente a tres piezas enormes?
R: Las vigas son fáciles de fabricar o comprar y, si una se rompe, se reemplaza por un repuesto idéntico; las piezas enormes se fabrican a medida, cuesta hallar sus defectos y no se pueden reemplazar sin que el edificio caiga.

P: ¿Por qué la gente elige los bloques grandes y complejos pese a sus desventajas?
R: Por un ahorro de tiempo percibido al inicio (encajan de golpe), pero la calidad es menor y el coste futuro mayor; a largo plazo lo eficiente es la simplicidad.

P: Según la Ecuación del Diseño de Software, ¿qué es lo más importante que se puede hacer ahora para reducir el mantenimiento?
R: Hacer el código más simple; no hace falta predecir el futuro, basta ver si el código es complejo y hacerlo menos complejo ya, logrando un esfuerzo de mantenimiento que decrece con el tiempo.

P: ¿Qué significa que "la simplicidad es relativa"?
R: Que lo que es simple depende de la audiencia objetivo y del contexto; algo puede parecer simple a quien lo entiende por dentro y muy complicado a quien lo ve por primera vez.

P: ¿Qué revela la guerra de editores vi vs Emacs sobre la simplicidad?
R: Que rara vez hay una herramienta fundamentalmente superior; la simplicidad percibida depende sobre todo de la familiaridad, y para los no programadores ambos editores parecerían complejos.

P: ¿Qué nivel de simplicidad hay que buscar para tener éxito de verdad?
R: "Stupid, dumb simple" (ridícula, tontamente simple); lo usable por gente normal también lo es por genios, ampliando el rango de usuarios posibles.

P: ¿Qué enseña el ejemplo del mapa del centro comercial?
R: Que el diseñador asume que el usuario dedicará mucho tiempo, pero el usuario solo quiere resolverlo rápido; por eso el mejor mapa tiene un gran "YOU ARE HERE" y el peor un diminuto triángulo difícil de encontrar.

P: ¿Por qué la consistencia es parte de la simplicidad?
R: Porque el código inconsistente es más difícil de leer, y la consistencia total facilita programar: si todos los objetos tienen un campo `name`, un solo trozo de código lo maneja en vez de requerir código especial para cada caso.

P: ¿De qué depende sobre todo la legibilidad del código?
R: De cómo el espacio es ocupado por letras y símbolos; demasiado espacio dificulta ver cómo se relacionan las cosas y muy poco dificulta ver que están separadas, por lo que el espaciado debe ser consistente e informar sobre la estructura.

P: ¿Cuál es el verdadero propósito de los comentarios?
R: Explicar por qué se hizo algo cuando la razón no es obvia, no qué hace el código; si el qué no es obvio, lo correcto es simplificar el código.

P: ¿Qué ocurre con un sistema si no se le presta atención al diseño?
R: Evoluciona hacia una bestia enorme y complicada; sin buen diseño el proyecto acaba hundido en complejidad y un día fallará.

## Preguntas de autoevaluación

P: ¿Por qué un código legible es también más fácil de arreglar? (sección "Legibilidad")
R: Porque al verlo con buen espaciado se detectan los bugs; en el ejemplo se ve que `z` nunca será mayor que `y + x` (siempre es igual), así que el bloque `if (z > y + x)` sobra. Ante código muy buggy y difícil de leer, el primer paso es hacerlo más legible.

P: ¿Cómo se aplica la Ley de la Simplicidad en la práctica? (sección "La analogía de la arquitectura")
R: Haciendo los componentes tan simples como sea posible y manteniéndolos así con el tiempo, por ejemplo con el desarrollo y diseño incremental, que incluye un paso de "rediseño" antes de añadir cada nueva función para simplificar.

P: ¿Por qué conviene documentación con secciones tipo "New to This Code?"? (sección "La simplicidad es relativa")
R: Porque ayuda a entender el punto de vista del recién llegado con explicaciones simples escritas como si el lector no supiera nada; muchos proyectos fallan mostrando una masa de enlaces sin dirección, y lo único peor que la documentación compleja es no tener documentación.

P: ¿Qué debe guiar la longitud de los nombres? (sección "Nombrar las cosas")
R: Deben ser lo bastante largos para comunicar qué es o qué hace algo, sin ser tan largos que cuesten de leer; depende de cómo se usan: una función llamada una vez en su línea admite nombre largo, una usada en expresiones complejas debe ser corta pero suficiente.

P: ¿Qué recomienda el autor cuando no se puede ser del todo simple? (sección "Sé consistente")
R: Al menos ser consistente; hay situaciones donde no importa cómo lo hagas mientras siempre lo hagas igual, y como tú mandas en el mundo de tu programa puedes hacerlo simple y consistente.

P: ¿Por qué diseñar bien suele dar poco crédito? (sección "La simplicidad requiere diseño")
R: Porque los fallos catastróficos son grandes y visibles mientras que los pequeños incrementos hacia un buen diseño son invisibles; manejar un gran fallo recibe agradecimiento, pero prevenirlo rara vez se nota.

P: ¿Cómo afecta simplificar a la deseabilidad de los cambios futuros? (sección "Simplicidad y la Ecuación del Diseño de Software")
R: Simplificar cuesta algo de trabajo ahora pero ahorra mucho tiempo después y, al reducir el esfuerzo de mantenimiento, aumenta la deseabilidad de todos los cambios posibles.

## Checklist

- [ ] Divide el sistema en piezas pequeñas, simples y autocontenidas en lugar de bloques grandes y complejos.
- [ ] Revisa el código actual, identifica lo que es complejo y hazlo menos complejo ahora, sin esperar a predecir el futuro.
- [ ] Aplica un paso de rediseño antes de añadir cada nueva función para simplificar las piezas.
- [ ] Añade documentación simple para recién llegados (tipo "New to This Code?"), escrita como si el lector no supiera nada.
- [ ] Busca que el código sea "stupid, dumb simple" de aprender, usando la tecnología avanzada que haga falta para lograr esa simplicidad.
- [ ] Mantén la consistencia: nombra y estructura todo igual en todas partes, incluido el comportamiento interno del programa.
- [ ] Usa un espaciado consistente que informe sobre la estructura, ni demasiado ni demasiado escaso.
- [ ] Elige nombres suficientes pero no excesivamente largos, ajustados a cómo se usa cada elemento.
- [ ] Reserva los comentarios para explicar el porqué; si necesitas explicar el qué, simplifica el código primero.
- [ ] Diseña deliberadamente para evitar que el sistema crezca hacia la complejidad.
