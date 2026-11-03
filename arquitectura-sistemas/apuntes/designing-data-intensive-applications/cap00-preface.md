# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Prólogo — Preface (Prólogo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

El prólogo sitúa al lector ante la avalancha de buzzwords que rodean el almacenamiento y procesamiento de datos (NoSQL, Big Data, Web-scale, Sharding, consistencia eventual, ACID, teorema CAP, servicios cloud, MapReduce, tiempo real) y argumenta que, para construir buenas aplicaciones, hace falta ir más allá de esas palabras de moda hacia una comprensión técnica precisa de las tecnologías y sus trade-offs. La tesis central es que, detrás del cambio tecnológico rápido, existen principios perdurables que siguen siendo válidos sin importar qué versión de una herramienta se use; si entiendes esos principios, sabrás dónde encaja cada herramienta, cómo aprovecharla y cómo evitar sus trampas.

El libro se define por lo que no es: no es un tutorial de una herramienta concreta ni un libro de teoría árida. En su lugar, examina ejemplos de sistemas de datos exitosos, los que sostienen muchas aplicaciones populares y deben cumplir requisitos de escalabilidad, rendimiento y fiabilidad en producción cada día. Se profundiza en sus internals, se separan sus algoritmos clave y se discuten sus principios y los trade-offs que deben asumir, buscando no solo cómo funcionan, sino por qué funcionan así y qué preguntas hay que hacerse.

Kleppmann introduce la distinción clave entre aplicaciones data-intensive y compute-intensive: una aplicación es data-intensive cuando los datos son su principal reto (cantidad, complejidad o velocidad de cambio), frente a compute-intensive, donde el cuello de botella son los ciclos de CPU. Tras leer el libro, el lector podrá decidir qué tipo de tecnología es apropiada para cada propósito y entender cómo combinar herramientas para formar una buena arquitectura de aplicación, sin llegar a construir un motor de almacenamiento desde cero (algo que rara vez es necesario), pero sí con buena intuición sobre lo que sus sistemas hacen por debajo.

## Fuerzas que impulsan el cambio

El prólogo enumera las fuerzas que han motivado los desarrollos de la última década en bases de datos, sistemas distribuidos y la forma de construir aplicaciones sobre ellos:

- Empresas de internet (Google, Yahoo!, Amazon, Facebook, LinkedIn, Microsoft, Twitter) manejan volúmenes enormes de datos y tráfico, lo que las obliga a crear herramientas nuevas para esa escala.
- Los negocios necesitan ser ágiles, probar hipótesis de forma barata y responder rápido al mercado con ciclos de desarrollo cortos y modelos de datos flexibles.
- El software libre y de código abierto se ha vuelto muy exitoso y se prefiere al software comercial o a medida en muchos entornos.
- Las velocidades de reloj de CPU apenas aumentan, pero los procesadores multinúcleo son estándar y las redes son más rápidas: el paralelismo solo va a crecer.
- Incluso un equipo pequeño puede construir sistemas distribuidos en muchas máquinas y varias regiones geográficas gracias a la infraestructura como servicio (IaaS) como Amazon Web Services.
- Se espera que muchos servicios sean altamente disponibles; el tiempo de inactividad prolongado por caídas o mantenimiento es cada vez más inaceptable.

Además de las bases de datos "NoSQL", el prólogo subraya que las colas de mensajes, cachés, índices de búsqueda y frameworks de procesamiento batch y stream también son muy importantes, y que muchas aplicaciones usan una combinación de ellos.

## Quién debería leer este libro

Está dirigido a quien desarrolla aplicaciones con algún tipo de servidor/backend para almacenar o procesar datos y que usan internet (web, apps móviles o sensores conectados). Es para ingenieros de software, arquitectos y managers técnicos a los que les gusta programar, y resulta especialmente relevante para quien toma decisiones de arquitectura, como elegir herramientas para un problema. Se recomienda experiencia construyendo aplicaciones web o servicios de red y familiaridad con bases de datos relacionales y SQL; conocer bases de datos no relacionales y protocolos como TCP y HTTP es un plus. El lenguaje o framework de programación es indiferente.

Frente al comentario habitual de "no eres Google ni Amazon, deja de preocuparte por la escala y usa una base de datos relacional", Kleppmann reconoce que construir para una escala que no se necesita es esfuerzo desperdiciado y una forma de optimización prematura, pero insiste en elegir la herramienta adecuada: las bases de datos relacionales son importantes, pero no la última palabra para tratar con datos.

## Alcance del libro

El libro no da instrucciones detalladas de instalación o uso de paquetes o APIs concretos, sino que discute los principios y trade-offs fundamentales de los sistemas de datos y las distintas decisiones de diseño de cada producto. Deja fuera deliberadamente el despliegue, las operaciones, la seguridad y la gestión, por ser temas complejos que merecen libros propios. Evita el término "Big Data" por estar sobreusado y mal definido, y prefiere términos menos ambiguos: sistemas de un solo nodo frente a distribuidos, o procesamiento online/interactivo frente a offline/batch. Tiene un sesgo hacia el software libre y de código abierto (FOSS), porque leer, modificar y ejecutar el código fuente ayuda a entender el detalle y reduce el riesgo de vendor lock-in, aunque también discute software propietario cuando procede.

## Estructura del libro

El libro se organiza en tres partes:

- Parte I — Fundamentos de los sistemas de datos. Capítulo 1: qué se intenta lograr (fiabilidad, escalabilidad y mantenibilidad), cómo pensarlas y cómo alcanzarlas. Capítulo 2: modelos de datos y lenguajes de consulta y su adecuación a distintas situaciones. Capítulo 3: motores de almacenamiento, cómo las bases de datos disponen los datos en disco para encontrarlos eficientemente. Capítulo 4: formatos de codificación (serialización) y evolución de esquemas con el tiempo.
- Parte II — De una máquina a datos distribuidos en varias. Capítulo 5: replicación. Capítulo 6: particionado/sharding. Capítulo 7: transacciones. Capítulo 8: problemas de los sistemas distribuidos. Capítulo 9: consistencia y consenso en sistemas distribuidos.
- Parte III — Sistemas que derivan datasets de otros datasets. Los datos derivados aparecen en sistemas heterogéneos que integran varias bases de datos, cachés e índices. Capítulo 10: procesamiento batch. Capítulo 11: procesamiento stream. Capítulo 12: puesta en común y enfoques futuros para construir aplicaciones fiables, escalables y mantenibles.

## Referencias y agradecimientos

Kleppmann señala que gran parte del contenido ya se ha dicho en presentaciones, papers, blogs, código, bug trackers y listas de correo; el libro sintetiza las ideas más importantes y aporta punteros a la literatura original (más de 800 referencias, en su mayoría disponibles gratis en línea). Para papers académicos recomienda buscar el título en Google Scholar, y mantiene todas las referencias actualizadas en el repositorio ept/ddia-references de GitHub. Agradece a numerosas personas por conversaciones y revisiones de borradores, a sus editores de O'Reilly, y destaca a Shabbir Diwan y Edie Freedman por ilustrar con cuidado los mapas que acompañan los capítulos. El proyecto le tomó casi cuatro años.

## Ideas clave

- Una aplicación es data-intensive cuando el reto principal son los datos (cantidad, complejidad o velocidad de cambio), no los ciclos de CPU.
- Detrás de las buzzwords hay principios perdurables; entenderlos permite elegir y usar bien cada herramienta y evitar sus trampas.
- El libro estudia internals de sistemas de datos reales en producción, no tutoriales ni teoría abstracta.
- El objetivo es navegar el panorama de tecnologías de datos y tomar buenas decisiones de arquitectura, no construir un motor de almacenamiento desde cero.
- Construir para una escala innecesaria es optimización prematura; aun así, hay que elegir la herramienta adecuada, y las relacionales no son la última palabra.
- Quedan fuera despliegue, operaciones, seguridad y gestión; se evita "Big Data" en favor de términos precisos (nodo único vs. distribuido, online vs. batch).
- Sesgo hacia FOSS para entender el detalle y reducir el vendor lock-in, discutiendo software propietario cuando aporta.
- El libro se estructura en tres partes: fundamentos, datos distribuidos y datos derivados (batch y stream).
