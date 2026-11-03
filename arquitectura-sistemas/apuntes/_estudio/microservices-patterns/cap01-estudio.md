# Escaping monolithic hell (Escapando del infierno monolítico) — Estudio

## Tarjetas de repaso

P: ¿Qué es el "monolithic hell" (infierno monolítico)?
R: El estado al que llega una aplicación monolítica exitosa cuando supera su propia arquitectura y el desarrollo se vuelve lento, penoso y poco fiable.

P: ¿Cuál es la tesis central del capítulo?
R: Que la cura para una aplicación grande y compleja es migrar a la arquitectura de microservicios, entendida como la descomposición funcional de la aplicación en servicios con límites bien definidos.

P: ¿Cómo se define la arquitectura de microservicios?
R: Un estilo arquitectónico que descompone funcionalmente (eje Y del scale cube) la aplicación en un conjunto de servicios; no habla de tamaño, sino de responsabilidades cohesivas y enfocadas.

P: ¿Qué son los tres ejes del scale cube?
R: Eje X (duplicación horizontal: clonar instancias idénticas tras un balanceador), eje Z (partición de datos: instancias idénticas que atienden un subconjunto de datos) y eje Y (descomposición funcional en servicios).

P: ¿Por qué cada servicio tiene su propia base de datos?
R: Para lograr el acoplamiento débil: permite cambiar el esquema sin coordinar con otros y mantener los servicios aislados en ejecución. No obliga a un servidor de BD por servicio.

P: ¿Por qué los microservicios son una mejor forma de modularidad que los paquetes Java?
R: Porque la API de un servicio es una frontera impermeable, difícil de violar, lo que preserva la modularidad mejor que los paquetes.

P: ¿Qué es un "Big Ball of Mud" y cómo se relaciona con FTGO?
R: El patrón de gran bola de barro; FTGO, pese a ser lógicamente modular, se ha convertido en un ejemplo de ese patrón.

P: ¿En qué se diferencian SOA y microservicios en comunicación?
R: SOA usa tuberías inteligentes (ESB) y protocolos pesados (SOAP, WS*); los microservicios usan tuberías tontas (message broker o comunicación directa) y protocolos ligeros (REST, gRPC).

P: ¿En qué se diferencian SOA y microservicios en datos?
R: SOA usa un modelo de datos global y bases de datos compartidas; los microservicios usan modelo de datos y base de datos por servicio.

P: ¿Qué es un "distributed monolith" (monolito distribuido)?
R: El resultado de descomponer mal una aplicación en servicios, que acaba con las desventajas de ambos mundos (monolito y microservicios).

P: ¿Qué es un patrón y qué es un pattern language?
R: Un patrón es una solución reutilizable a un problema en un contexto dado (Christopher Alexander); un pattern language es una colección de patrones relacionados.

P: ¿Qué elementos valiosos incluye una estructura de patrón?
R: Forces (fuerzas, problemas a resolver que pueden estar en conflicto), resulting context (beneficios, drawbacks e issues nuevos) y related patterns (predecesor, sucesor, alternativa, generalización, especialización).

P: ¿Qué es el "reverse Conway maneuver"?
R: Aplicar la ley de Conway en reverso: diseñar la organización para que su estructura refleje la arquitectura de microservicios.

P: ¿Qué es un equipo "two-pizza" o cómo deben ser los equipos?
R: Equipos pequeños (8-12 personas), transfuncionales y con una misión orientada al negocio, dentro de un "team of teams".

P: ¿Cuáles son las tres etapas del modelo de transición de Bridges (Managing Transitions)?
R: Ending/Losing/Letting Go, The Neutral Zone y The New Beginning.

## Preguntas de autoevaluación

P: ¿Cuáles son los síntomas del infierno monolítico? (sección "El lento avance hacia el infierno monolítico")
R: Complejidad que intimida a los desarrolladores, desarrollo lento, camino largo del commit al despliegue, dificultad para escalar módulos con requisitos de recursos en conflicto, falta de aislamiento de fallos y bloqueo en una pila tecnológica obsoleta.

P: ¿Qué beneficios tenía inicialmente la arquitectura monolítica de FTGO? (sección "El lento avance hacia el infierno monolítico")
R: Era simple de desarrollar, fácil de hacer cambios radicales, sencilla de probar (tests de extremo a extremo con Selenium), sencilla de desplegar (copiar el WAR a Tomcat) y fácil de escalar (varias instancias tras un balanceador).

P: ¿Por qué importa la arquitectura según el capítulo? (sección "La arquitectura de microservicios al rescate")
R: Por los atributos de calidad o "ilities" (sobre todo mantenibilidad, extensibilidad y testabilidad), no por los requisitos funcionales, porque condicionan la velocidad de entrega.

P: ¿Cuáles son los principales inconvenientes de los microservicios? (sección "Beneficios e inconvenientes")
R: Es difícil encontrar el conjunto correcto de servicios (riesgo de monolito distribuido), los sistemas distribuidos son complejos (IPC, fallos parciales, transacciones y consultas entre servicios, mayor complejidad operativa), desplegar funcionalidades que abarcan varios servicios exige coordinación, y decidir cuándo adoptarlos es difícil.

P: ¿Qué debería hacer una startup respecto a los microservicios? (sección "Beneficios e inconvenientes")
R: Empezar casi siempre con un monolito y descomponer más tarde, cuando el problema sea la complejidad.

P: ¿Para qué sirve el Microservice architecture pattern language? (sección "El lenguaje de patrones de arquitectura de microservicios")
R: Primero ayuda a decidir entre arquitectura monolítica y de microservicios, y luego a aplicarla; se organiza en tres capas (infraestructura, infraestructura de aplicación y aplicación) y en grupos por área de problema.

P: ¿Por qué el formato de patrón es útil para discutir tecnología? (sección "El lenguaje de patrones de arquitectura de microservicios")
R: Porque es objetivo y obliga a describir los inconvenientes, evitando la dicotomía "suck/rock" y el hype cycle; no hay bala de plata (Fred Brooks).

P: ¿Por qué la arquitectura por sí sola no basta? (sección "Más allá de los microservicios: proceso y organización")
R: Porque la entrega rápida, frecuente y fiable requiere combinarla con una organización adecuada (equipos pequeños y autónomos), procesos ágiles y DevOps, y atención al lado humano de la transición.

## Puntos a dominar

- Reconocer los síntomas del infierno monolítico y por qué una aplicación monolítica exitosa acaba en ese estado.
- Distinguir qué es y qué no es la arquitectura de microservicios: eje Y del scale cube, responsabilidades cohesivas, no tamaño.
- Explicar los tres ejes del scale cube (X, Y, Z) y cómo un servicio puede escalarse en X y Z.
- Justificar por qué cada servicio tiene su propia base de datos y cómo eso logra acoplamiento débil.
- Comparar SOA y microservicios en comunicación, datos y tamaño del servicio típico.
- Enumerar beneficios e inconvenientes de los microservicios y saber cuándo conviene (o no) adoptarlos.
- Describir la estructura de un patrón (forces, resulting context, related patterns) y el propósito del pattern language.
- Entender que la adopción requiere también DevOps, equipos pequeños y autónomos (reverse Conway maneuver) y gestión del lado humano (modelo de Bridges).
