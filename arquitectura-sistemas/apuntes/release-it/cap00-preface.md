# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Prólogo — Preface (Prefacio)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este prefacio presenta el propósito del libro: examinar cómo arquitectar, diseñar y construir software —en particular sistemas distribuidos— para el "lodo y el fango" del mundo real. El autor advierte que el software estará bajo ataque desde el momento en que se libera y debe resistir tanto los vientos de un flash mob como la presión de un ataque DDoS lanzado por hornos tostadores IoT mal asegurados. El objetivo es analizar software que no superó esa prueba y encontrar formas de asegurar que el tuyo sobreviva al contacto con la realidad.

La tesis central es que la estabilidad es un prerrequisito necesario para cualquier otra preocupación: sin ella no hay futuro viable para un sistema. A partir de ahí, el libro recorre la vida completa del software en producción —operación, entrega y evolución— con la idea de que hay dinero real en juego cuando los sistemas fallan.

Al terminar el prefacio sabrás a quién va dirigido el libro, cómo está organizado en cuatro partes, qué papel cumplen los casos de estudio y dónde encontrar los recursos en línea.

## A quién va dirigido

El libro está dirigido a arquitectos, diseñadores y desarrolladores de sistemas de software distribuido: sitios web, servicios web y proyectos de EAI, entre otros. Se trata de sistemas que deben estar disponibles o la empresa pierde dinero, ya sean sistemas de comercio que generan ingresos directamente por ventas o sistemas internos críticos que los empleados usan para su trabajo. La regla práctica que ofrece el autor: si alguien tiene que irse a casa porque tu software deja de funcionar, este libro es para ti.

## Cómo está organizado el libro

El libro se divide en cuatro partes, cada una introducida por un caso de estudio:

- **Parte I: Create Stability (Crear estabilidad).** Muestra cómo mantener vivos los sistemas y preservar el tiempo de actividad. Pese a las promesas de fiabilidad por redundancia, los sistemas distribuidos exhiben una disponibilidad más parecida a "dos ochos" que a los codiciados "cinco nueves". Si un sistema se cae y muere a diario, nada más importa y domina el pensamiento a corto plazo; por eso se empieza construyendo una base estable.
- **Parte II: Design for Production (Diseñar para producción).** Trata lo que significa vivir en producción, lidiando con la complejidad de los entornos modernos en todo su detalle virtualizado, contenerizado, con balanceo de carga y descubrimiento de servicios. Ilustra buenos patrones de control, transparencia y disponibilidad tanto en centros de datos físicos como en la nube.
- **Parte III: Deliver Your System (Entregar tu sistema).** Aborda los despliegues. Hoy existen buenas herramientas para "verter bits" en los servidores, pero esa es la parte fácil; lo difícil es empujar cambios frecuentes y pequeños sin romper a los consumidores. Se cubre el diseño para el despliegue, los despliegues sin tiempo de inactividad y el versionado entre servicios dispares —siempre un asunto delicado—.
- **Parte IV: Solve Systemic Problems (Resolver problemas sistémicos).** Examina la vida continua del sistema como parte del ecosistema de información global. Si la versión 1.0 es el nacimiento del sistema, hay que pensar en su crecimiento y desarrollo posterior: construir sistemas que crezcan, se flexibilicen y se adapten con el tiempo. Incluye la arquitectura evolutiva, el "conocimiento" compartido entre sistemas y, finalmente, cómo construir sistemas antifrágiles mediante la disciplina emergente de la *chaos engineering*, que usa aleatoriedad y estrés deliberado sobre un sistema para mejorarlo.

## Sobre los casos de estudio

El autor incluye varios casos de estudio extensos para ilustrar los temas principales. Están tomados de eventos y fallos de sistemas reales que él mismo observó, fallos muy costosos y embarazosos para los involucrados. Por eso ofuscó parte de la información —nombres de empresas, personas, sistemas, clases y métodos— pero solo esos detalles no esenciales. En cada caso se mantuvieron la misma industria, la secuencia de eventos, el modo de fallo, la propagación del error y el desenlace. Los costes no están exagerados: son empresas reales y dinero real, y esas cifras se conservaron para subrayar la seriedad del material. "Real money is on the line when systems fail" (PDF p. 14).

## Recursos en línea

El libro tiene su propia página web donde se pueden consultar detalles, descargar el código fuente, participar en los foros de discusión y reportar erratas como errores tipográficos y sugerencias de contenido. Los foros se presentan como el lugar ideal para conversar con otros lectores y compartir comentarios sobre el libro.

## Ideas clave

- El libro enseña a diseñar y desplegar sistemas distribuidos para las condiciones hostiles del mundo real, donde el software está bajo ataque desde su liberación.
- Va dirigido a arquitectos, diseñadores y desarrolladores de sistemas cuya indisponibilidad hace perder dinero a la empresa.
- La estabilidad es el prerrequisito fundamental: sin ella domina el pensamiento a corto plazo y no hay futuro viable.
- Cuatro partes recorren el ciclo completo: estabilidad, diseño para producción, entrega y problemas sistémicos.
- Los sistemas distribuidos suelen ofrecer "dos ochos" de disponibilidad en lugar de los "cinco nueves" prometidos por la redundancia.
- El reto del despliegue no es verter bits, sino empujar cambios frecuentes y pequeños sin romper a los consumidores ni sufrir caídas.
- La evolución a largo plazo incluye arquitectura evolutiva, conocimiento compartido y la *chaos engineering* para lograr sistemas antifrágiles.
- Los casos de estudio provienen de fallos reales observados por el autor, con cifras de coste conservadas para subrayar que hay dinero real en juego.
