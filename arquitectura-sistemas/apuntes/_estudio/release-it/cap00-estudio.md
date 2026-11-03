# Prólogo — Preface (Prefacio) — Estudio

## Tarjetas de repaso

P: ¿Cuál es el propósito del libro según el prefacio?
R: Examinar cómo arquitectar, diseñar y construir software —en particular sistemas distribuidos— para el "lodo y el fango" del mundo real, de modo que sobreviva al contacto con la realidad.

P: ¿Desde cuándo está el software bajo ataque, según el autor?
R: Desde el momento en que se libera; debe resistir desde los vientos de un flash mob hasta un ataque DDoS lanzado por hornos tostadores IoT mal asegurados.

P: ¿Cuál es la tesis central del prefacio?
R: La estabilidad es el prerrequisito necesario para cualquier otra preocupación; sin ella no hay futuro viable para un sistema.

P: ¿A quién va dirigido el libro?
R: A arquitectos, diseñadores y desarrolladores de sistemas de software distribuido (sitios web, servicios web, proyectos de EAI) cuya indisponibilidad hace perder dinero a la empresa.

P: ¿Cuál es la regla práctica que ofrece el autor sobre su audiencia?
R: Si alguien tiene que irse a casa porque tu software deja de funcionar, el libro es para ti.

P: ¿En cuántas partes se divide el libro y cómo se introduce cada una?
R: En cuatro partes, cada una introducida por un caso de estudio.

P: ¿Qué cubre la Parte I: Create Stability (Crear estabilidad)?
R: Cómo mantener vivos los sistemas y preservar el tiempo de actividad, construyendo una base estable porque si el sistema cae a diario domina el pensamiento a corto plazo.

P: ¿Qué nivel de disponibilidad suelen exhibir los sistemas distribuidos según el prefacio?
R: Más parecido a "dos ochos" que a los codiciados "cinco nueves" prometidos por la redundancia.

P: ¿Qué aborda la Parte II: Design for Production (Diseñar para producción)?
R: Lo que significa vivir en producción con entornos virtualizados, contenerizados, con balanceo de carga y descubrimiento de servicios, y buenos patrones de control, transparencia y disponibilidad.

P: ¿Cuál es la parte fácil y la parte difícil del despliegue según la Parte III?
R: La parte fácil es "verter bits" en los servidores; lo difícil es empujar cambios frecuentes y pequeños sin romper a los consumidores (despliegues sin downtime y versionado entre servicios dispares).

P: ¿Qué examina la Parte IV: Solve Systemic Problems (Resolver problemas sistémicos)?
R: La vida continua del sistema: arquitectura evolutiva, conocimiento compartido entre sistemas y la chaos engineering para construir sistemas antifrágiles.

P: ¿Qué es la chaos engineering según el prefacio?
R: Una disciplina emergente que usa aleatoriedad y estrés deliberado sobre un sistema para mejorarlo y hacerlo antifrágil.

P: ¿Por qué el autor ofuscó información en los casos de estudio y qué conservó?
R: Ofuscó detalles no esenciales (nombres de empresas, personas, sistemas, clases y métodos), pero mantuvo la industria, la secuencia de eventos, el modo de fallo, la propagación del error y el desenlace.

P: ¿Por qué conservó las cifras de coste de los casos de estudio?
R: Para subrayar la seriedad del material: son empresas reales y dinero real. "Real money is on the line when systems fail" (PDF p. 14).

## Preguntas de autoevaluación

P: ¿Por qué afirma el autor que la estabilidad debe abordarse antes que cualquier otra preocupación?
R: Porque si un sistema se cae y muere a diario, nada más importa y domina el pensamiento a corto plazo; sin estabilidad no hay futuro viable. (Lo que necesitas saber / Cómo está organizado el libro)

P: ¿Qué tipo de sistemas y empresas tiene en mente el autor como lectores objetivo?
R: Sistemas distribuidos que deben estar disponibles o la empresa pierde dinero, ya sean sistemas de comercio que generan ingresos por ventas o sistemas internos críticos para el trabajo de los empleados. (A quién va dirigido)

P: ¿Qué recorrido sigue el libro a lo largo de la vida del software en producción?
R: El ciclo completo: crear estabilidad, diseñar para producción, entregar el sistema y resolver problemas sistémicos (operación, entrega y evolución). (Cómo está organizado el libro)

P: ¿Qué contraste plantea el prefacio entre la promesa de la redundancia y la realidad de la disponibilidad?
R: La redundancia promete "cinco nueves", pero los sistemas distribuidos exhiben en la práctica una disponibilidad más cercana a "dos ochos". (Cómo está organizado el libro — Parte I)

P: Según la Parte III, ¿por qué las buenas herramientas de despliegue no bastan?
R: Porque verter bits en los servidores es lo fácil; el reto real es empujar cambios frecuentes y pequeños sin romper a los consumidores ni provocar caídas, incluyendo el versionado entre servicios dispares. (Cómo está organizado el libro — Parte III)

P: ¿Qué significa pensar en el sistema más allá de su versión 1.0?
R: Si la 1.0 es el nacimiento del sistema, hay que pensar en su crecimiento y desarrollo: construir sistemas que crezcan, se flexibilicen y se adapten con el tiempo mediante arquitectura evolutiva, conocimiento compartido y chaos engineering. (Cómo está organizado el libro — Parte IV)

P: ¿Qué garantiza la fidelidad y el valor didáctico de los casos de estudio?
R: Que provienen de fallos reales observados por el autor y que, pese a ofuscar detalles no esenciales, conservan industria, secuencia, modo de fallo, propagación, desenlace y las cifras de coste reales. (Sobre los casos de estudio)

## Puntos a dominar

- El propósito del libro: diseñar y desplegar sistemas distribuidos para condiciones hostiles del mundo real.
- La tesis central: la estabilidad es el prerrequisito fundamental de todo lo demás.
- El perfil del lector: arquitectos, diseñadores y desarrolladores de sistemas cuya indisponibilidad cuesta dinero.
- La organización en cuatro partes (estabilidad, diseño para producción, entrega, problemas sistémicos) y el tema de cada una.
- El contraste "dos ochos" vs. "cinco nueves" en la disponibilidad real de sistemas distribuidos.
- El reto real del despliegue: cambios frecuentes y pequeños sin romper a los consumidores.
- La chaos engineering como vía hacia sistemas antifrágiles.
- El origen real de los casos de estudio y por qué se conservan las cifras de coste.
