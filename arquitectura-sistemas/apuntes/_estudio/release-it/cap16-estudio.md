# Adaptation (Adaptación) — Estudio

## Tarjetas de repaso

P: ¿Qué distingue a las organizaciones que prosperan de las que se extinguen según el capítulo? / R: Su capacidad de absorber o crear cambio; la adaptación debe diseñarse en personas, procesos, herramientas y arquitectura, de forma paralela e incremental.

P: ¿Qué es el ciclo de decisión y cómo se formaliza? / R: El tiempo para observar, decidir, actuar y comprobar; se formaliza como ciclo Deming/Shewhart (PDCA) o bucle OODA (observe, orient, decide, act), y su velocidad es la restricción clave de la competitividad.

P: ¿Qué es el thrashing en el contexto organizativo? / R: Cambiar de rumbo sin dar tiempo a recibir y procesar el feedback; es análogo al "porpoising" en aviación cuando el ciclo de control va más rápido que el feedback del entorno.

P: ¿Cuál es el rol del Platform Team? / R: Tratar al desarrollo de aplicaciones como su cliente y proveer provisión vía API/CLI; implementa mecanismos (no reglas concretas) y responde por la disponibilidad de la plataforma, no de las aplicaciones.

P: ¿Por qué un "DevOps Team" intermediario es un antipatrón? / R: Porque crea dos interfaces donde había una; DevOps es una transformación cultural, no solo automatización de despliegues.

P: ¿Qué patrones de Continuous Delivery hacen las releases menos arriesgadas? / R: Canary Deploy, Blue/Green Deploy y despliegue en oleadas; actúan como gobernadores que limitan el ritmo de acciones peligrosas y el número de clientes expuestos a un bug.

P: ¿Qué significa Service Extinction y por qué importa? / R: Que la clave de la arquitectura evolutiva es matar servicios rezagados en grano fino; preserva la entidad mayor y reduce dependencias, haciendo a la organización antifrágil.

P: ¿De qué trata realmente la regla del two-pizza team de Bezos? / R: No solo de tener pocas personas, sino de reducir dependencias externas y ser autosuficiente hasta producción; cada dependencia es una cuerda que ata a Gulliver.

P: ¿Por qué la eficiencia como "utilización plena" es contraproducente? / R: Frena el flujo global del trabajo; además, cuanto más eficiente y especializado queda un flujo para las tareas de hoy, más difícil es cambiarlo mañana (velero frente a portacontenedores).

P: ¿Qué es la arquitectura evolutiva según Ford, Parsons y Kua? / R: La que soporta cambio incremental y guiado como primer principio en múltiples dimensiones.

P: ¿Por qué la arquitectura en capas dificulta la evolución y qué alternativa se propone? / R: Impone aislamiento vertical pero fomenta acoplamiento horizontal; girar las barreras 90 grados da una arquitectura de componentes donde cada uno posee su pila completa con interfaces estrechas.

P: ¿Qué problema resuelve Explicit Context en los identificadores? / R: Un identificador desnudo crea una dependencia implícita hacia un único proveedor; usar una URL (p. ej. itemID como URL) sirve como token opaco pero permite resolver contra múltiples autoridades y facilita el testing.

P: ¿Qué son los seis operadores modulares de Baldwin y Clark? / R: Splitting, Substituting, Augmenting, Excluding, Inversion y Porting; herramientas de pensamiento para crear opciones, cuyo valor económico crece con el número de fronteras donde aplicarlos.

P: ¿Qué es el "URL Dualism"? / R: Una URL es a la vez referencia (resoluble para obtener la representación) e identificador (token que se pasa sin resolver), igual que un puntero.

P: ¿Qué es la "dark matter" en la arquitectura de la información? / R: Lo que no cabe en el modelo del sistema de registro y, por tanto, no se representa.

## Preguntas de autoevaluación

P: ¿Cuándo compensa la adaptación rápida y qué excepción se cita? / R: Cuando hay una relación convexa entre esfuerzo y retorno (mercados competitivos); dominios como aviónica o dispositivos médicos tienen costes de transacción altísimos. Excepción: JPL desplegó un hotfix al rover Spirit en Marte y Curiosity cargó software tras aterrizar. (Sección: Convex Returns)

P: Si el desarrollo va más rápido que el feedback, ¿en qué conviene invertir el tiempo sobrante? / R: No en más herramientas de despliegue, sino en una plataforma de experimentación que acelere la observación y la decisión. (Sección: Process and Organization)

P: ¿Qué indica la necesidad de un despliegue coordinado entre proveedor y consumidor de una interfaz? / R: Es señal de acoplamiento fuerte; el proveedor es responsable de mantener compatibilidad hacia atrás o de añadir una nueva ruta y retirar la vieja después. (Sección: Process and Organization, recuadro No Coordinated Deployments)

P: ¿Qué evidencia señala un "Bad Layering"? / R: Commits con nombres como "Foo", "FooController", "FooMapper", "FooDTO"; cada capa debe expresar sus propios conceptos fundamentales, y lo que es una clase en una capa debe ser mero dato en las demás. (Sección: System Architecture, recuadro Bad Layering)

P: ¿Por qué conviene que los servicios controlen sus propios identificadores? / R: Asignar un "owner ID" acopla el servicio a una autoridad de usuarios concreta y limita a un catálogo por dueño; emitir sus propios identificadores (una URL) permite actuar como un SaaS con muchos clientes. (Sección: Services Control Their Identifiers)

P: ¿Qué distinciones hace Fowler sobre mensajes y eventos? / R: Event notification (anuncio unidireccional), event-carried state transfer (replica entidades), event sourcing (todos los cambios como eventos) y CQRS (lectura y escritura con estructuras distintas). (Sección: Messages, Events, and Commands)

P: ¿Qué enseña el caso del "price point" sobre la filtración de conceptos? / R: Era elegante upstream, pero propagarlo a todos los sistemas downstream (que solo necesitaban el precio) era un cambio masivo con efecto dominó; es complejidad incidental filtrándose y crea acoplamiento semántico que estorba el cambio. (Sección: Avoid Concept Leakage)

P: Según el cierre, ¿cuándo empieza la vida real del software? / R: Con la release; todo lo anterior es gestación. Los sistemas crecen adaptándose o decaen hasta que sus costes superan sus beneficios y mueren. (Sección: Wrapping Up)

## Puntos a dominar

- Explicar por qué la velocidad del ciclo de decisión (PDCA/OODA) determina la competitividad y reconocer el riesgo de thrashing.
- Distinguir un Platform Team legítimo del antipatrón "DevOps Team" intermediario.
- Describir los patrones de release de bajo riesgo (Canary, Blue/Green, oleadas) y por qué actúan como gobernadores.
- Argumentar la extinción de servicios en grano fino y las cinco opciones ante un servicio rezagado.
- Justificar la autonomía a escala de equipo (two-pizza) por reducción de dependencias, no por tamaño.
- Contrastar eficiencia como utilización plena frente a flujo de valor (velero frente a portacontenedores).
- Comparar estilos de arquitectura (capas, componentes, microservices, microkernel, event-based) y sus trade-offs evolutivos.
- Aplicar contexto explícito, loose clustering y los seis operadores modulares de Baldwin y Clark para crear opciones.
- Elegir el paradigma de datos deliberadamente, considerar eventos frente a estado y aprovechar la dualidad de las URLs.
- Evitar la filtración de conceptos internos y pensar en zonas de autoridad federadas en lugar de un único sistema de registro.
