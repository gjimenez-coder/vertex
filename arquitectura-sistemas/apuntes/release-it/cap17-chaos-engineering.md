# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 17 — Chaos Engineering (Ingeniería del caos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

La ingeniería del caos es "la disciplina de experimentar sobre un sistema distribuido para construir confianza en su capacidad de resistir condiciones turbulentas en producción" (PDF p. 329). Es empírica, no formal: no modelamos lo que el sistema debería hacer, sino que ejecutamos experimentos para aprender lo que realmente hace. Matar instancias en producción parece una idea radical, pero no descabellada: es una de sus técnicas.

El énfasis está en el sistema completo, normalmente a gran escala. Los entornos de staging o QA no sirven de guía porque jamás serán réplicas a tamaño real de producción (nadie construye un segundo Facebook como staging), y distintas proporciones de instancias o de tráfico producen comportamientos cualitativamente diferentes. Muchos problemas solo aparecen en el sistema entero: reintentos excesivos que provocan timeouts, fallos en cascada, dogpiles, respuestas lentas y puntos únicos de fallo.

La tesis central es que la seguridad, como la concurrencia, no es una propiedad componible: dos servicios seguros por separado no garantizan un sistema seguro al combinarlos. Sales sabiendo cómo pensar en propiedades emergentes, cómo diseñar experimentos con una hipótesis, cómo inyectar y dirigir el caos, y cómo extenderlo al factor humano.

## El ejemplo que recorre el capítulo

Dos proveedores con un cliente que impone un timeout de 50 ms. Cada proveedor tiene una respuesta media de 20 ms y un percentil 99.9 de 30 ms, así que llamar a cualquiera por separado es fiable. Pero si el cliente debe llamar a ambos en secuencia, aunque la media siga dentro del presupuesto de 50 ms, un porcentaje considerable de llamadas lo rompe y el cliente parece poco fiable. Ilustra por qué el caos mira el sistema completo y no los componentes aislados.

## Breaking Things to Make Them Better

Carácter empírico y de escala: los fallos del sistema completo no se simulan en no-producción por el problema de escala, ni se ganan probando componentes aislados, por la no-componibilidad de la seguridad.

## Antecedentes

La disciplina bebe de la cibernética, los sistemas adaptativos complejos, las organizaciones de alta fiabilidad y, en especial, la *resilience engineering*. Ideas clave de las que parte:

- **Drift (Sidney Dekker, *Drift into Failure*)**: un sistema (personas, tecnología y procesos) vive entre tres límites: capacidad, economía y seguridad. La presión por mayor retorno económico y la tendencia humana a no trabajar al máximo empujan el sistema hacia la barrera de seguridad. Analogía del avión: al altitud económicamente óptima hay menos margen entre la velocidad de pérdida y la de turbulencia. Los sistemas muy eficientes gestionan mal las disrupciones y tienden a romperse de golpe. El caos es la fuerza compensadora que optimiza disponibilidad y tolerancia frente a throughput.
- **Paradoja fundamental del regulador (Gerald Weinberg)**: la tarea de un regulador es eliminar la variación, pero esa variación es la fuente de información sobre su desempeño; cuanto mejor trabaja, menos aprende. Parafraseada como "no sabes cuánto dependes de tu equipo de IT hasta que se van de vacaciones".
- **Paradoja del "microbús Volkswagen"**: aprendes a arreglar lo que se rompe a menudo; lo que rara vez falla, cuando falla, resulta más grave. Conviene un nivel continuo y bajo de rotura.
- **Antifragilidad (Nassim Taleb, *Antifragile*)**: usamos el caos como un pesista usa el hierro, creando niveles tolerables de estrés para fortalecer el sistema con el tiempo.

## The Simian Army

El ejemplo más conocido es el **Chaos Monkey** de Netflix: cada cierto tiempo elige un clúster de autoescalado y mata una instancia; el clúster debe recuperarse solo, y si no, el equipo propietario debe arreglarlo. Nació durante la migración a AWS y a microservicios: AWS termina instancias lo bastante a menudo como para ser un problema al escalar, pero no tanto como para probar cada despliegue, así que Netflix necesitaba que los fallos ocurrieran más seguido hasta volverse rutinarios ("si algo duele, hazlo más a menudo"). La elección no fue "o robustecer componentes o robustecer el sistema", sino "y": patrones de estabilidad en cada instancia *y* resiliencia global.

Siguieron otros monos (Latency Monkey, Janitor Monkey, Conformity Monkey, incluso Chaos Kong), liberados como open source en la "Simian Army". Cada nuevo mono mejoró la disponibilidad global.

## Opt In or Opt Out?

En Netflix el caos es **opt-out**: todo servicio en producción queda sujeto a Chaos Monkey; eximirse requiere aprobación, queda registrado en una base de datos y conlleva estigma. Otras empresas eligen **opt-in**, con tasas de adopción mucho menores pero quizá la única vía viable en arquitecturas maduras y frágiles. Recomendación: empezar en opt-in para reducir resistencia y publicitar éxitos antes de pasar a opt-out; con opt-out, la gente puede no entender de qué se exime ni la gravedad de no responder.

## Adopting Your Own Monkey

Al lanzarse, Chaos Monkey sorprendió por cuántas vulnerabilidades destapó incluso en servicios antiguos (configuraciones sutiles, rosters de clúster que crecían sin límite con IPs viejas).

**Prerequisites:** el caos no puede matar tu empresa ni a tus clientes; Netflix lo tenía fácil porque el cliente reintenta el play. Hay que:

- Limitar el **blast radius** (número de clientes afectados y grado de disrupción), eligiendo "víctimas" por criterios (p. ej., "falla cada petición número 10.000").
- Poder **trazar** un usuario y una petición por las capas y saber si tuvo éxito: si éxito, la traza revela dónde la redundancia salvó la petición; si falla, dónde falló.
- Saber qué es "sano" y desde qué perspectiva; cuidado con que el monitoreo falle cuando las cosas se tuercen, sobre todo si comparte red con producción. Charity Majors: "si tienes un muro de dashboards en verde, tus herramientas de monitoreo no son suficientemente buenas" (PDF p. 334).
- Tener un **plan de recuperación**: el sistema puede no volver solo a sano al apagar el caos.

**Designing the Experiment:** empezar con una **hipótesis** en términos de invariantes que el sistema debe mantener bajo turbulencia, centrada en el comportamiento observable externamente, no en internos (la de Chaos Monkey, "los servicios en clúster no deberían verse afectados por fallos de instancia", fue invalidada rápido). Verificar que se puede medir el estado estable actual y definir qué evidencia bastaría para rechazar la hipótesis (una tasa de fallo no nula puede no ser suficiente por condiciones de red externas).

**Injecting Chaos:** tres tipos de inyecciones: matar instancias (la más básica y burda, Chaos Monkey), añadir latencia (Latency Monkey: destapa timeouts sin fallback y condiciones de carrera ocultas) y hacer fallar llamadas servicio a servicio. Netflix usa **FIT** (failure injection testing, distinto del "framework for integrated testing" del cap. anterior): etiqueta la petición en el borde con una cookie que marca dónde fallará una llamada, y en el call site se reporta como fallida sin hacer la petición.

**Targeting Chaos:** la aleatoriedad (como Chaos Monkey) funciona al principio porque el espacio de fallos está densamente poblado. Al avanzar es un **problema de búsqueda** en un espacio escaso y no uniforme con alta dimensionalidad (en el peor caso, con x servicios podría haber 2^(2x) fallos a inyectar). Hace falta dirigir las inyecciones: los humanos aplican conocimiento del sistema, razonamiento abductivo y reconocimiento de patrones. Importa estudiar los fallos que *no* provocan caídas, porque algo evitó que el fault se volviera failure. Peter Alvaro propone una "cunning malevolent intelligence": recoge trazas de carga normal, infiere qué servicios necesita cada petición, modela un grafo y usa algoritmos de grafos para elegir enlaces que cortar, reduciendo drásticamente el espacio de búsqueda.

**Automate and Repeat:** en el mejor caso el caos es aburrido porque el sistema sigue funcionando. Al hallar una debilidad hay que arreglar ese caso concreto y buscar otras partes vulnerables a la misma clase de problema, luego automatizar las pruebas con moderación (no matar la última instancia de un clúster; no fallar a la vez todos los fallbacks). Las plataformas dedicadas deciden cuánto caos aplicar, cuándo, a quién y qué servicios quedan fuera; la de Netflix es **ChAP** (Chaos Automation Platform). La plataforma decide el qué y el cuándo, pero delega el cómo a herramientas existentes (Ansible es popular por no requerir agente), y reporta sus pruebas al monitoreo para correlacionar.

## Disaster Simulations

El caos no es solo software: las personas son mortales y falibles (enferman, renuncian, hay desastres naturales). ¿Qué pasa cuando tu punto único de fallo se va a casa cada noche? Las organizaciones de alta fiabilidad usan simulacros. A gran escala es un ejercicio de "business continuity"; a menor escala, se designa a cierta gente como "incapacitada" y se comprueba si se sigue operando. Versión divertida: la "simulación de apocalipsis zombi", con el 50 % del personal como zombis que no responden. Los primeros intentos revelan procesos que dependen de un único rol o persona; se registran como incidencias y, tras un *postmortem*, se corrigen con documentación, cambios de rol o automatización. No conviene combinar inyección de fallos con zombis en la primera ronda; después, subir estrés al 20 % de zombis. Nota de seguridad: tener forma de **abortar** el ejercicio con una palabra clave para distinguir "esto no es parte del simulacro".

## Ideas clave

- La ingeniería del caos es empírica: experimenta en producción sobre el sistema completo para ganar confianza ante condiciones turbulentas.
- La seguridad no es componible; muchos fallos solo emergen a escala en el sistema entero.
- El *drift* empuja los sistemas eficientes hacia la barrera de seguridad; el caos es la fuerza compensadora que prioriza disponibilidad.
- Chaos Monkey mata instancias de clústeres autoescalados; la Simian Army añadió latencia, limpieza, conformidad y Chaos Kong.
- Elegir entre opt-out (Netflix, mayor adopción, con estigma) y opt-in (menor resistencia, útil al empezar).
- Prerrequisitos: no matar la empresa, limitar el *blast radius*, trazar peticiones, saber qué es "sano" y tener plan de recuperación.
- El experimento parte de una hipótesis sobre invariantes observables externamente; definir qué evidencia rechaza la hipótesis.
- Tres inyecciones (matar instancia, latencia, fallo de llamada) y FIT; dirigir el caos es un problema de búsqueda que humanos y herramientas como la "cunning malevolent intelligence" acotan; automatizar con moderación (ChAP) y extender al factor humano con simulacros.
