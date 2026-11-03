# Chaos Engineering (Ingeniería del caos) — Estudio

## Tarjetas de repaso

P: ¿Qué es la ingeniería del caos?
R: La disciplina de experimentar sobre un sistema distribuido para construir confianza en su capacidad de resistir condiciones turbulentas en producción (PDF p. 329).

P: ¿Por qué la ingeniería del caos es empírica y no formal?
R: Porque no modela lo que el sistema debería hacer, sino que ejecuta experimentos para aprender lo que realmente hace.

P: ¿Por qué los entornos de staging o QA no sirven de guía?
R: Porque jamás serán réplicas a tamaño real de producción y distintas proporciones de instancias o de tráfico producen comportamientos cualitativamente diferentes.

P: ¿Cuál es la tesis central sobre la seguridad del sistema?
R: La seguridad, como la concurrencia, no es una propiedad componible: dos servicios seguros por separado no garantizan un sistema seguro al combinarlos.

P: ¿Qué ilustra el ejemplo de los dos proveedores con timeout de 50 ms?
R: Que aunque cada proveedor sea fiable por separado (media 20 ms, p99.9 30 ms), llamarlos en secuencia rompe el presupuesto en un porcentaje considerable de llamadas; por eso el caos mira el sistema completo.

P: ¿Qué es el *drift* según Sidney Dekker?
R: Un sistema vive entre tres límites (capacidad, economía y seguridad); la presión económica y la tendencia a no trabajar al máximo lo empujan hacia la barrera de seguridad, y los sistemas muy eficientes se rompen de golpe.

P: ¿Qué dice la paradoja fundamental del regulador (Weinberg)?
R: La tarea de un regulador es eliminar la variación, pero esa variación es la fuente de información sobre su desempeño; cuanto mejor trabaja, menos aprende.

P: ¿Qué es la antifragilidad (Taleb) aplicada al caos?
R: Usar el caos como un pesista usa el hierro, creando niveles tolerables de estrés para fortalecer el sistema con el tiempo.

P: ¿Qué hace el Chaos Monkey de Netflix?
R: Cada cierto tiempo elige un clúster de autoescalado y mata una instancia; el clúster debe recuperarse solo, y si no, el equipo propietario debe arreglarlo.

P: ¿Qué diferencia hay entre caos opt-out y opt-in?
R: Opt-out (Netflix) sujeta todo servicio en producción al caos y eximirse requiere aprobación y conlleva estigma; opt-in tiene menor adopción pero reduce resistencia y puede ser la única vía viable en arquitecturas maduras y frágiles.

P: ¿Qué es el *blast radius* y cómo se limita?
R: El número de clientes afectados y el grado de disrupción; se limita eligiendo víctimas por criterios, p. ej. "falla cada petición número 10.000".

P: ¿Cuáles son los prerrequisitos para adoptar el caos?
R: No matar la empresa ni a los clientes, limitar el blast radius, poder trazar usuarios y peticiones, saber qué es "sano" y desde qué perspectiva, y tener un plan de recuperación.

P: ¿Cómo debe formularse la hipótesis de un experimento de caos?
R: En términos de invariantes que el sistema debe mantener bajo turbulencia, centrada en el comportamiento observable externamente y no en internos, definiendo qué evidencia bastaría para rechazarla.

P: ¿Cuáles son los tres tipos de inyección de caos y qué es FIT?
R: Matar instancias (la más burda), añadir latencia (Latency Monkey) y hacer fallar llamadas servicio a servicio; FIT (failure injection testing) etiqueta la petición en el borde con una cookie que marca dónde fallará y la reporta como fallida sin hacer la petición.

P: ¿Por qué dirigir el caos es un problema de búsqueda y cómo se aborda?
R: Porque el espacio de fallos es escaso, no uniforme y de alta dimensionalidad (en el peor caso 2^(2x) fallos); humanos y la "cunning malevolent intelligence" de Peter Alvaro (trazas, grafos y algoritmos de grafos) acotan el espacio.

## Preguntas de autoevaluación

P: ¿Por qué matar instancias en producción no es una idea descabellada para Netflix?
R: Porque el cliente reintenta el play, así que el caos no mata la empresa ni a los clientes; eso hacía que a Netflix le resultara fácil cumplir el prerrequisito de no causar daño. (Sección: Adopting Your Own Monkey — Prerequisites)

P: ¿Qué clases de problemas solo aparecen en el sistema completo?
R: Reintentos excesivos que provocan timeouts, fallos en cascada, dogpiles, respuestas lentas y puntos únicos de fallo. (Sección: Lo que necesitas saber)

P: ¿Por qué Netflix necesitó introducir Chaos Monkey durante su migración a AWS y microservicios?
R: Porque AWS termina instancias lo bastante a menudo como para ser un problema al escalar, pero no tanto como para probar cada despliegue; necesitaban que los fallos ocurrieran más seguido hasta volverse rutinarios ("si algo duele, hazlo más a menudo"). (Sección: The Simian Army)

P: ¿Qué recomendación da el capítulo sobre el orden entre opt-in y opt-out?
R: Empezar en opt-in para reducir resistencia y publicitar éxitos antes de pasar a opt-out, ya que con opt-out la gente puede no entender de qué se exime ni la gravedad de no responder. (Sección: Opt In or Opt Out?)

P: ¿Por qué el monitoreo puede fallar justo cuando más se necesita?
R: Porque las cosas se tuercen y el monitoreo puede caer, sobre todo si comparte red con producción; Charity Majors advierte que un muro de dashboards en verde indica herramientas de monitoreo insuficientes (PDF p. 334). (Sección: Adopting Your Own Monkey — Prerequisites)

P: ¿Por qué importa estudiar los fallos que *no* provocan caídas?
R: Porque algo evitó que el fault se volviera failure, y entender ese mecanismo de redundancia o protección aporta información para dirigir mejor las inyecciones. (Sección: Adopting Your Own Monkey — Targeting Chaos)

P: ¿Qué moderación hay que aplicar al automatizar las pruebas de caos?
R: No matar la última instancia de un clúster ni fallar a la vez todos los fallbacks; la plataforma (ChAP en Netflix) decide cuánto caos aplicar, cuándo, a quién y qué servicios quedan fuera. (Sección: Adopting Your Own Monkey — Automate and Repeat)

P: ¿Para qué sirven los simulacros de desastre y la "simulación de apocalipsis zombi"?
R: Para probar el factor humano, comprobando si se sigue operando cuando ciertas personas quedan "incapacitadas"; revelan procesos que dependen de un único rol o persona, que se corrigen tras un postmortem con documentación, cambios de rol o automatización. (Sección: Disaster Simulations)

## Puntos a dominar

- Definir la ingeniería del caos como disciplina empírica que experimenta sobre el sistema completo en producción.
- Explicar por qué staging/QA no bastan y por qué la seguridad no es componible.
- Reconocer los antecedentes: drift (Dekker), paradoja del regulador (Weinberg), paradoja del microbús Volkswagen y antifragilidad (Taleb).
- Describir Chaos Monkey y la evolución de la Simian Army (Latency, Janitor, Conformity, Chaos Kong).
- Distinguir los modelos opt-out y opt-in y la recomendación de orden entre ambos.
- Enumerar los prerrequisitos: no matar la empresa, limitar blast radius, trazar peticiones, saber qué es "sano" y tener plan de recuperación.
- Formular una hipótesis sobre invariantes observables externamente y definir la evidencia que la rechaza.
- Diferenciar las tres inyecciones (matar, latencia, fallo de llamada), entender FIT y por qué dirigir el caos es un problema de búsqueda.
- Automatizar con moderación mediante una plataforma (ChAP) que delega el cómo a herramientas existentes (Ansible).
- Extender el caos al factor humano con simulacros de desastre, incluyendo una palabra clave para abortar el ejercicio.
