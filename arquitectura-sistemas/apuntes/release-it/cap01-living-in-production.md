# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 1 — Living in Production (Vivir en producción)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo abre el libro planteando una pregunta incómoda: que un sistema esté "feature complete" (con todas las funcionalidades y la mayoría con tests) no significa que esté listo para producción. El diseño de software, tal como se enseña hoy, está incompleto: habla de lo que los sistemas deben hacer, pero no de lo que no deben hacer (no caer, no colgarse, no perder datos, no violar la privacidad, no perder dinero, no destruir la empresa ni matar clientes).

La tesis central es que hay que apuntar al objetivo correcto: la vida real en producción, no pasar las pruebas de QA. El testing, por muy ágil, pragmático y automatizado que sea, no basta para demostrar que el software está listo para el mundo real, con usuarios reales e impredecibles, tráfico global y agentes hostiles. Sales sabiendo que debes aceptar que, pese a los mejores planes, pasarán cosas malas; la meta no es predecir y eliminar todos los eventos adversos, sino prevenir los que se puedan y asegurar que el sistema en conjunto se recupere de traumas severos e inesperados.

El capítulo introduce además dos ideas que atraviesan todo el libro: que las decisiones de diseño y arquitectura son también decisiones financieras, y que conviene ser un arquitecto pragmático antes que uno de "torre de marfil".

## Apuntar al objetivo correcto (Aiming for the Right Target)

La mayoría del software se diseña para el laboratorio de desarrollo o para los testers de QA, buscando sobrevivir al reino artificial de QA y no al mundo real de producción. Nygard lo compara con el diseño de automóviles de principios de los 90: coches diseñados en la comodidad del laboratorio, elegantes y sofisticados, pero frágiles y de vida corta.

Pasar QA dice poco sobre la idoneidad del sistema para los próximos tres a diez años de vida. Podría ser el Toyota Camry del software (miles de horas de uptime) o el Chevy Vega o el Ford Pinto. No se puede saber con unos días o semanas de pruebas lo que traerán los años siguientes.

Trae el paralelo del "design for manufacturability" (diseño para la manufacturabilidad) de la industria: diseñar productos para fabricarse a bajo costo y alta calidad. Antes, diseñadores y fabricantes vivían en mundos distintos y los diseños "arrojados por encima del muro" generaban baja calidad y alto costo. Hoy ocurre algo similar: entregamos software terminado a IT operations. El análogo propuesto es el "design for production" (diseño para producción): diseñar tanto los sistemas individuales como el ecosistema de sistemas interdependientes para operar a bajo costo y alta calidad.

## El alcance del desafío (The Scope of the Challenge)

En los días relajados de los sistemas cliente/servidor, la base de usuarios se medía en decenas o cientos, con unas pocas decenas concurrentes. Hoy se ven recuentos de usuarios activos mayores que la población de continentes enteros; ya hubo una primera red social de mil millones de usuarios.

Las exigencias de uptime también crecieron: los famosos "cinco nueves" (99,999 por ciento), antes dominio del mainframe, hoy se esperan incluso de sitios de comercio corrientes, disponibles 24 por 7 por 365. Con el mayor alcance y escala llegan nuevas formas de romperse, entornos más hostiles y menos tolerancia a los defectos. Los diseños apropiados para un pequeño sitio WordPress fracasan estrepitosamente al aplicarse a sistemas grandes, transaccionales y distribuidos.

## Un millón de dólares aquí, un millón allá (A Million Dollars Here, a Million Dollars There)

Hay mucho en juego: el éxito del proyecto, las stock options, la supervivencia de la empresa y hasta tu empleo. Los sistemas construidos para QA suelen requerir tanto gasto continuo (costo de operación, downtime, mantenimiento) que nunca alcanzan la rentabilidad.

Durante la prisa del desarrollo es fácil tomar decisiones que optimizan el costo de desarrollo a expensas del costo operativo, lo cual solo tiene sentido ante un presupuesto y una fecha fijos. Los sistemas pasan mucho más de su vida en operación que en desarrollo, así que evitar un costo único de desarrollo para incurrir en un costo operativo recurrente no tiene sentido financiero.

Ejemplo numérico del capítulo: un sistema que requiere cinco minutos de downtime en cada release, con vida útil de cinco años y releases mensuales, tiene un costo esperado de downtime del orden de 1.000.000 de dólares (300 minutos de downtime a un modesto costo de 3.000 dólares por minuto). Invertir 50.000 dólares en un build pipeline y un proceso de despliegue sin downtime evita esa pérdida: un ROI de 2.000 por ciento, además de permitir desplegar con más frecuencia y ganar cuota de mercado. La fusión de los puntos de vista técnico y financiero es uno de los temas recurrentes más importantes del libro.

## Usa la Fuerza (Use the Force)

Las decisiones tempranas tienen el mayor impacto en la forma eventual del sistema y son las más difíciles de revertir. Las decisiones iniciales sobre el límite del sistema y su descomposición en subsistemas se cristalizan en la estructura del equipo, la asignación de fondos y hasta los códigos de hoja de horas. Las asignaciones de equipo son el primer borrador de la arquitectura. La ironía es que estas decisiones tempranas e irrevocables son también las menos informadas, porque el equipo aún ignora la estructura final del software.

Nygard se declara partidario del desarrollo ágil: la entrega temprana y las mejoras incrementales llevan el software a producción rápido, y producción es el único lugar donde se aprende cómo responde el software ante estímulos del mundo real. Aun en proyectos ágiles las decisiones se toman mejor con previsión; como las alternativas suelen tener costos de implementación similares pero costos de ciclo de vida radicalmente distintos, importa considerar el efecto de cada decisión sobre disponibilidad, capacidad y flexibilidad.

## Arquitectura pragmática (Pragmatic Architecture)

Bajo el término "arquitectura" caen dos tipos de actividad divergentes. Uno busca niveles de abstracción más altos, portables y desconectados de los detalles de hardware, redes y electrones; su forma extrema es la "torre de marfil" (ivory tower), habitada por gurús distantes que emiten decretos ("el middleware será JBoss para siempre", "todas las UIs con Angular 1.0", "todo vive en Oracle", "no usarás Ruby"). Un arquitecto de torre de marfil que no escucha a los coders tampoco escucha a los usuarios.

El otro tipo, el arquitecto pragmático, no solo se codea con los programadores: es uno. No duda en levantar la tapa de una abstracción o descartarla si no encaja, y discute uso de memoria, requisitos de CPU, ancho de banda, hyperthreading y CPU binding. Mientras el de torre de marfil persigue una visión de estado final perfecto y cerrado a mejoras, el pragmático piensa en la dinámica del cambio: cómo desplegar sin reiniciar el mundo, qué métricas recolectar y analizar, qué parte del sistema necesita más mejora. En su creación, cada componente es "suficientemente bueno" para las tensiones actuales, y él sabe cuáles habrá que reemplazar según cambien los factores de estrés.

## Cierre (Wrapping Up)

El software entrega su valor en producción; todo lo anterior (desarrollo, testing, integración, planificación) es preludio. El libro trata la vida en producción, desde el release inicial hasta el crecimiento y la evolución del sistema. La primera parte se dedica a la estabilidad (Part I: Create Stability), y arranca con el caso del bug de software que dejó en tierra a una aerolínea.

## Ideas clave

- "Feature complete" no equivale a "production ready"; el diseño de software debe atender también lo que el sistema no debe hacer.
- La meta no es pasar QA, sino sobrevivir a la vida real en producción; el testing no basta para probarlo.
- Asume que pasarán cosas malas: prioriza la recuperación del sistema ante traumas inesperados, no solo la prevención.
- "Design for production" es el análogo del "design for manufacturability": diseñar sistemas y ecosistemas para operar a bajo costo y alta calidad.
- La escala actual (miles de millones de usuarios, uptime de cinco nueves, 24x7x365) impone entornos más hostiles y menor tolerancia a defectos.
- Las decisiones de diseño y arquitectura son decisiones financieras: los sistemas viven más en operación que en desarrollo; evitar downtime puede dar ROI de 2.000 por ciento.
- Las decisiones tempranas son las más irreversibles y las menos informadas; considera su efecto en disponibilidad, capacidad y flexibilidad.
- Sé un arquitecto pragmático (atento a la dinámica del cambio y al "suficientemente bueno"), no uno de torre de marfil.
