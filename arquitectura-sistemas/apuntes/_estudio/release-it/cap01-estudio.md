# Living in Production (Vivir en producción) — Estudio

## Tarjetas de repaso

P: ¿Qué significa que un sistema esté "feature complete" y por qué no basta? / R: Que tiene todas las funcionalidades (la mayoría con tests), pero eso no implica que esté "production ready": el diseño de software está incompleto porque ignora lo que el sistema no debe hacer.

P: ¿Cuáles son las cosas que un sistema "no debe hacer" según el capítulo? / R: No caer, no colgarse, no perder datos, no violar la privacidad, no perder dinero, no destruir la empresa ni matar clientes.

P: ¿Cuál es el objetivo correcto al que debe apuntar el diseño? / R: La vida real en producción (usuarios reales e impredecibles, tráfico global, agentes hostiles), no pasar las pruebas de QA.

P: ¿Puede el testing demostrar que el software está listo para el mundo real? / R: No; por muy ágil, pragmático y automatizado que sea, el testing no basta para demostrar que el software está listo para producción.

P: ¿Cuál es la meta frente a los eventos adversos? / R: No predecir y eliminar todos los eventos adversos, sino prevenir los que se puedan y asegurar que el sistema se recupere de traumas severos e inesperados.

P: ¿Qué es "design for production" y con qué se compara? / R: Diseñar los sistemas individuales y el ecosistema de sistemas interdependientes para operar a bajo costo y alta calidad; es el análogo del "design for manufacturability" de la industria.

P: ¿Con qué analogía ilustra Nygard el software diseñado solo para QA? / R: Con los automóviles de principios de los 90: diseñados cómodamente en el laboratorio, elegantes pero frágiles y de vida corta.

P: ¿Qué dice pasar QA sobre la idoneidad del sistema a largo plazo? / R: Muy poco; con días o semanas de pruebas no se sabe si será el Toyota Camry del software o el Chevy Vega / Ford Pinto en los próximos tres a diez años.

P: ¿Cómo ha cambiado el alcance del desafío respecto a los días cliente/servidor? / R: Antes se medían decenas o cientos de usuarios con pocas decenas concurrentes; hoy hay recuentos mayores que continentes enteros y ya existió una red social de mil millones de usuarios.

P: ¿Qué son los "cinco nueves" y quién los exige hoy? / R: Un uptime del 99,999 por ciento, antes dominio del mainframe, hoy esperado incluso de sitios de comercio corrientes disponibles 24x7x365.

P: ¿Por qué las decisiones de diseño son también decisiones financieras? / R: Porque los sistemas pasan mucho más de su vida en operación que en desarrollo; evitar un costo único de desarrollo para incurrir en un costo operativo recurrente no tiene sentido financiero.

P: ¿Cuál es el ejemplo numérico de ROI del capítulo? / R: Cinco minutos de downtime por release, vida de cinco años y releases mensuales dan ~300 minutos a 3.000 dólares/minuto = ~1.000.000 de dólares; invertir 50.000 en un pipeline sin downtime da un ROI de 2.000 por ciento.

P: ¿Por qué son críticas las decisiones tempranas de arquitectura? / R: Tienen el mayor impacto y son las más difíciles de revertir (cristalizan equipos, fondos, códigos de horas), pero son las menos informadas porque aún se ignora la estructura final.

P: ¿Qué caracteriza a un arquitecto de "torre de marfil"? / R: Busca abstracciones altas y portables desconectadas del hardware; emite decretos distantes, persigue un estado final perfecto cerrado a mejoras y, al no escuchar a los coders, tampoco escucha a los usuarios.

P: ¿Qué caracteriza a un arquitecto pragmático? / R: Es también programador; levanta la tapa de las abstracciones, discute memoria, CPU, ancho de banda y binding, piensa en la dinámica del cambio y construye componentes "suficientemente buenos" para las tensiones actuales.

## Preguntas de autoevaluación

P: ¿Por qué afirma Nygard que "el diseño de software, tal como se enseña hoy, está incompleto"? / R: Porque habla de lo que los sistemas deben hacer pero no de lo que no deben hacer (caer, perder datos, violar privacidad, etc.). (Lo que necesitas saber)

P: ¿En qué se parecen el "throwing over the wall" de la manufactura y la entrega de software a IT operations? / R: En ambos, diseñadores y operadores vivían en mundos distintos y los diseños arrojados por encima del muro generaban baja calidad y alto costo; el "design for production" lo corrige. (Apuntar al objetivo correcto)

P: ¿Por qué los diseños aptos para un pequeño sitio WordPress fracasan en sistemas grandes? / R: Porque con el mayor alcance y escala llegan nuevas formas de romperse, entornos más hostiles y menos tolerancia a los defectos. (El alcance del desafío)

P: ¿Por qué optimizar el costo de desarrollo a expensas del operativo suele ser un error? / R: Porque solo tiene sentido ante un presupuesto y fecha fijos; como los sistemas viven más en operación, cambiar un costo único por uno recurrente no tiene sentido financiero. (Un millón de dólares aquí, un millón allá)

P: ¿Por qué las decisiones tempranas son a la vez las más impactantes y las menos informadas? / R: Porque fijan límites, subsistemas y estructura de equipo de forma difícil de revertir, pero se toman cuando el equipo aún desconoce la estructura final del software. (Usa la Fuerza)

P: Siendo partidario de lo ágil, ¿por qué defiende Nygard tomar decisiones con previsión? / R: Porque las alternativas suelen tener costos de implementación similares pero costos de ciclo de vida radicalmente distintos, así que importa su efecto en disponibilidad, capacidad y flexibilidad. (Usa la Fuerza)

P: ¿En qué se diferencian la visión de cambio del arquitecto de torre de marfil y la del pragmático? / R: El de torre de marfil persigue un estado final perfecto cerrado a mejoras; el pragmático piensa en la dinámica del cambio: desplegar sin reiniciar el mundo, qué métricas recolectar y qué mejorar. (Arquitectura pragmática)

P: Según el cierre, ¿dónde entrega su valor el software y con qué caso arranca la Parte I? / R: El software entrega su valor en producción; la Parte I (Create Stability) arranca con el bug que dejó en tierra a una aerolínea. (Cierre)

## Puntos a dominar

- Distinguir "feature complete" de "production ready" y enumerar lo que un sistema no debe hacer.
- Explicar por qué el objetivo correcto es la vida en producción y no pasar QA, y por qué el testing no basta.
- Reformular la meta como prevención de lo evitable más recuperación ante traumas inesperados.
- Relacionar "design for production" con "design for manufacturability".
- Argumentar las decisiones de arquitectura en términos financieros, incluyendo el ejemplo del ROI de 2.000 por ciento.
- Reconocer que las decisiones tempranas son las más irreversibles y menos informadas, y sopesar su efecto en disponibilidad, capacidad y flexibilidad.
- Contrastar al arquitecto de torre de marfil con el pragmático y defender el enfoque "suficientemente bueno".
