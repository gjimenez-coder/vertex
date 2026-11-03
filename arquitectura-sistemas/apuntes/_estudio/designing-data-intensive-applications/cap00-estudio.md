# Prólogo — Preface (Prólogo) — Estudio

## Tarjetas de repaso

P: ¿Cuándo se considera que una aplicación es data-intensive? / R: Cuando su principal reto son los datos (su cantidad, su complejidad o la velocidad a la que cambian), no los ciclos de CPU.

P: ¿Qué es una aplicación compute-intensive frente a una data-intensive? / R: En una aplicación compute-intensive el cuello de botella son los ciclos de CPU; en una data-intensive el reto principal son los datos.

P: ¿Cuál es la tesis central del prólogo respecto a las buzzwords? / R: Que detrás del cambio tecnológico rápido existen principios perdurables; entenderlos permite elegir y usar bien cada herramienta y evitar sus trampas.

P: ¿Qué NO es este libro según el prólogo? / R: No es un tutorial de una herramienta concreta ni un libro de teoría árida; examina internals de sistemas de datos reales en producción.

P: ¿Cuál es el objetivo que el lector alcanza tras leer el libro? / R: Decidir qué tecnología es apropiada para cada propósito y combinar herramientas en una buena arquitectura, con intuición de lo que los sistemas hacen por debajo, sin construir un motor de almacenamiento desde cero.

P: ¿Qué fuerzas impulsan los desarrollos recientes en bases de datos y sistemas distribuidos? / R: Grandes volúmenes de datos y tráfico en empresas de internet, necesidad de agilidad de negocio, éxito del software libre, procesadores multinúcleo y redes rápidas, infraestructura como servicio (IaaS) y la expectativa de alta disponibilidad.

P: Además de las bases de datos "NoSQL", ¿qué otras piezas destaca el prólogo? / R: Colas de mensajes, cachés, índices de búsqueda y frameworks de procesamiento batch y stream, que muchas aplicaciones combinan.

P: ¿Para quién está escrito el libro? / R: Para ingenieros de software, arquitectos y managers técnicos a los que les gusta programar y que desarrollan aplicaciones con backend que almacena o procesa datos y usa internet.

P: ¿Qué experiencia previa se recomienda para leer el libro? / R: Experiencia construyendo aplicaciones web o servicios de red y familiaridad con bases de datos relacionales y SQL; conocer bases no relacionales y protocolos como TCP y HTTP es un plus.

P: ¿Qué postura toma el autor ante "no eres Google ni Amazon"? / R: Reconoce que construir para una escala innecesaria es optimización prematura, pero insiste en elegir la herramienta adecuada, pues las relacionales no son la última palabra para tratar con datos.

P: ¿Qué temas quedan deliberadamente fuera del alcance del libro? / R: El despliegue, las operaciones, la seguridad y la gestión, por ser temas complejos que merecen libros propios.

P: ¿Por qué el libro evita el término "Big Data"? / R: Por estar sobreusado y mal definido; prefiere términos menos ambiguos como nodo único vs. distribuido u online/interactivo vs. offline/batch.

P: ¿Por qué el libro tiene sesgo hacia el software libre (FOSS)? / R: Porque leer, modificar y ejecutar el código fuente ayuda a entender el detalle y reduce el riesgo de vendor lock-in, aunque también discute software propietario cuando procede.

P: ¿Cómo se estructura el libro? / R: En tres partes: Parte I fundamentos de los sistemas de datos, Parte II de una máquina a datos distribuidos en varias, y Parte III sistemas que derivan datasets de otros datasets (batch y stream).

## Preguntas de autoevaluación

P: ¿Qué distingue a una aplicación data-intensive de una compute-intensive y qué implica para el diseño? / R: En la data-intensive el reto son los datos (cantidad, complejidad o velocidad de cambio) y en la compute-intensive el cuello de botella es la CPU; por ello el libro se centra en tecnologías de datos. (Sección "Lo que necesitas saber")

P: ¿Por qué conviene entender los principios perdurables y no solo las herramientas de moda? / R: Porque los principios siguen siendo válidos aunque cambie la versión de la herramienta, y conocerlos permite saber dónde encaja cada una, aprovecharla y evitar sus trampas. (Sección "Lo que necesitas saber")

P: Enumera al menos tres fuerzas que han motivado los desarrollos recientes en sistemas de datos. / R: Entre otras: los enormes volúmenes de datos y tráfico de empresas de internet, la necesidad de agilidad del negocio, el éxito del software libre, los procesadores multinúcleo con redes más rápidas, la infraestructura como servicio y la expectativa de alta disponibilidad. (Sección "Fuerzas que impulsan el cambio")

P: ¿Qué objetivos del Capítulo 1 anticipa el prólogo? / R: Qué se intenta lograr —fiabilidad, escalabilidad y mantenibilidad—, cómo pensarlas y cómo alcanzarlas. (Sección "Estructura del libro")

P: ¿Qué cubren respectivamente las Partes II y III del libro? / R: La Parte II trata el paso de una máquina a datos distribuidos (replicación, particionado, transacciones, problemas de sistemas distribuidos, consistencia y consenso); la Parte III trata sistemas que derivan datasets de otros, con procesamiento batch y stream. (Sección "Estructura del libro")

P: ¿Qué requisitos deben cumplir en producción los sistemas de datos que el libro examina? / R: Requisitos de escalabilidad, rendimiento y fiabilidad cada día. (Sección "Lo que necesitas saber")

P: ¿Qué recurso ofrece el autor para acceder a la literatura original citada? / R: Más de 800 referencias, en su mayoría gratis en línea; recomienda buscar el título en Google Scholar y mantiene las referencias actualizadas en el repositorio ept/ddia-references de GitHub. (Sección "Referencias y agradecimientos")

## Puntos a dominar

- Diferenciar aplicaciones data-intensive (reto en los datos) de compute-intensive (reto en la CPU).
- Explicar por qué los principios perdurables importan más que las buzzwords al elegir tecnología.
- Recitar las fuerzas que impulsan el cambio en bases de datos y sistemas distribuidos.
- Reconocer que el libro estudia internals de sistemas reales, no tutoriales ni teoría abstracta.
- Entender que construir para una escala innecesaria es optimización prematura, pero hay que elegir la herramienta adecuada.
- Saber qué queda fuera del alcance (despliegue, operaciones, seguridad, gestión) y por qué se evita "Big Data".
- Justificar el sesgo hacia FOSS por el entendimiento del detalle y la reducción de vendor lock-in.
- Conocer la estructura en tres partes: fundamentos, datos distribuidos y datos derivados (batch y stream).
