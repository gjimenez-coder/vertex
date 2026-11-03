# Stabilize Your System (Estabiliza tu sistema) — Estudio

## Tarjetas de repaso

- P: ¿Qué significa que el software empresarial deba ser "cínico"? / R: Que espera que ocurran cosas malas, se protege con barreras internas, no confía ni en sí mismo y se niega a intimar demasiado con otros sistemas para no salir dañado.
- P: ¿Cuáles son los costos de la mala estabilidad? / R: Pérdida de ingresos (el minorista pierde 1.000.000 de dólares por hora de caída) y pérdida de reputación, menos tangible pero igual de dolorosa.
- P: ¿Cuesta más la buena estabilidad que la inestable? / R: No; en arquitectura, diseño e implementación hay puntos de decisión donde el diseño estable suele costar lo mismo que el inestable.
- P: ¿Qué es una transacción en este contexto? / R: La unidad abstracta de trabajo que procesa el sistema (ej. "cliente realiza un pedido"); no es una transacción de base de datos, y una unidad de trabajo puede abarcar muchas de ellas.
- P: ¿Qué diferencia hay entre sistema dedicado y carga mixta (mixed workload)? / R: Un sistema dedicado procesa un solo tipo de transacción; la carga mixta combina distintos tipos de transacciones.
- P: ¿Qué es un sistema robusto? / R: El que sigue procesando transacciones pese a impulsos transitorios, estreses persistentes o fallos de componentes; no basta con que los servidores sigan en pie, el usuario debe poder seguir trabajando.
- P: ¿Qué diferencia hay entre impulso (impulse) y estrés (stress)? / R: El impulso es un choque rápido (como un martillazo); el estrés es una fuerza aplicada durante un periodo prolongado.
- P: ¿Qué es la deformación (strain)? / R: El efecto que produce el estrés: un componente estresado (ej. un procesador de tarjetas lento) propaga deformación a partes distantes (más RAM en servidores web, exceso de I/O en la base de datos).
- P: ¿Cómo se define la longevidad y "mucho tiempo"? / R: Es la capacidad de seguir procesando transacciones mucho tiempo; una definición útil de "mucho tiempo" es el tiempo entre despliegues de código.
- P: ¿Cuáles son los mayores enemigos de la longevidad? / R: Las fugas de memoria y el crecimiento de datos ("lodo"), que matan el sistema en producción y rara vez se detectan en pruebas.
- P: ¿Qué es un modo de fallo (failure mode)? / R: El conjunto del disparador original, la forma en que la grieta se extiende y el daño resultante.
- P: ¿Qué son los "crackstoppers" de Chiles? / R: Protecciones o modos de fallo seguros diseñados para contener el daño, análogos a las zonas de deformación que fallan primero para proteger a los pasajeros.
- P: ¿Qué distingue a fault, error y failure? / R: Fault (falla) es una condición que crea un estado interno incorrecto; error es comportamiento visiblemente incorrecto; failure (fallo) es un sistema que no responde.
- P: ¿Por qué una cadena de fallo no es tan improbable como parece? / R: Porque se supone erróneamente que los eventos son independientes; un fallo en una capa aumenta la probabilidad de fallos en otras.
- P: ¿En qué coinciden los enfoques de tolerancia a fallos y "let it crash"? / R: En que las fallas siempre ocurrirán y en que hay que impedir que se conviertan en errores.

## Preguntas de autoevaluación

- P: ¿Por qué el proyecto Core Facilities (CF) de la aerolínea no fue lo bastante cínico? / R: Porque el equipo se dejó deslumbrar por la nueva tecnología y la arquitectura avanzada y no vio la señal de alto; no planificó sus modos de fallo. (El ejemplo que recorre el capítulo)
- P: Con 5.000 visitantes únicos por hora, un 10% que se marcha para siempre y un costo de adquisición de hasta 150 dólares, ¿cuánto marketing se desperdicia? / R: 75.000 dólares. (Lo que necesitas saber)
- P: ¿Por qué QA y las pruebas de carga no detectan los bugs de longevidad, y cómo se cazan? / R: Porque las aplicaciones se reciclan a diario en QA y las pruebas de carga corren un tiempo acotado y caro; se cazan con pruebas de longevidad propias (JMeter, Marathon) que generan peticiones de forma continua y aflojan unas horas al día para simular la madrugada. (Alargar la vida útil)
- P: ¿Qué consecuencia tiene negar la inevitabilidad del fallo? / R: Te quita el poder de controlarlo; aceptarlo permite diseñar la reacción del sistema, y si no diseñas los modos de fallo obtendrás los impredecibles y peligrosos que emerjan solos. (Modos de fallo)
- P: En CF, ¿por qué los hilos de atención quedaban bloqueados y cómo pudo evitarse? / R: El pool de conexiones bloqueaba hilos indefinidamente al no haber recursos, y las llamadas RMI por defecto nunca expiran; pudo evitarse creando más conexiones, limitando el bloqueo, fijando un timeout en los sockets RMI (p. ej. `Socket.setSoTimeout()`) o descartando los hilos bloqueados. (Detener la propagación de la grieta)
- P: ¿Cómo influye el acoplamiento en la propagación de la grieta? / R: Cuanto más acoplada la arquitectura, más fácil se propaga el error; las arquitecturas poco acopladas (colas petición/respuesta, tuple space) actúan como amortiguadores. (Detener la propagación de la grieta / Cadena de fallo)
- P: ¿Qué pregunta ayuda a prepararse ante la cadena de fallo y cuándo es práctico el enfoque exhaustivo? / R: Preguntar en cada llamada externa, I/O y uso de recursos "¿de cuántas formas puede salir mal esto?"; el enfoque exhaustivo por fuerza bruta solo es práctico para sistemas de misión crítica o rovers de Marte. (Cadena de fallo)

## Puntos a dominar

- Explicar por qué el software debe ser cínico y relacionar la mala estabilidad con pérdida de ingresos y reputación, sabiendo que la buena estabilidad no cuesta más.
- Definir con precisión transacción, sistema, sistema dedicado, carga mixta y sistema robusto.
- Distinguir impulso, estrés, deformación y longevidad, con sus ejemplos (flash mob, tuit de celebridad, doce millones de mensajes en una cola).
- Reconocer fugas de memoria y crecimiento de datos como enemigos de la longevidad y justificar la necesidad de pruebas de longevidad propias.
- Describir el modo de fallo (disparador, propagación y daño) y la analogía de la grieta de Chiles, incluyendo zonas de deformación y "crackstoppers".
- Enumerar los niveles donde CF pudo detener la grieta: pool de conexiones, timeouts RMI/EJB, particionado en grupos de servicio y arquitecturas poco acopladas.
- Manejar la terminología fault → error → failure y explicar por qué los eventos de la cadena de fallo no son independientes.
- Contrastar los enfoques de tolerancia a fallos y "let it crash" y su punto de acuerdo.
