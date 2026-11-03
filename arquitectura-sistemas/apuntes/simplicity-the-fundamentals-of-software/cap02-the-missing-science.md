# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 2 — The Missing Science (La ciencia que falta)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo define con precisión qué es el "diseño de software" (software design) y plantea la tesis central del libro: el diseño de software puede y debe ser una ciencia, pero hoy todavía no lo es porque le falta la pieza más importante, un conjunto de leyes fundamentales claramente enunciadas. El libro se presenta como el registro del descubrimiento de esas leyes.

Sales sabiendo tres cosas. Primero, que "diseño" tiene tres sentidos (verbo: planificar; sustantivo: el plan que se hizo; y el plan que sigue el código ya existente), y que todo lo relativo a la arquitectura y a las decisiones técnicas del sistema entra en esa categoría. Segundo, que todo programador es un diseñador, con responsabilidad sobre su propio código. Tercero, el porqué histórico de que no existiera antes una ciencia del diseño de software, y la afirmación de que la falta de esa ciencia es la fuente principal de la complejidad.

## El diseño de software, definido

El autor parte de las definiciones de diccionario de "design" y las aplica al software:

- Como verbo: planificar el software (estructura del código, tecnologías, decisiones técnicas), ya sea mentalmente, por escrito o con diagramas.
- Como sustantivo (primer sentido): el plan que se hizo.
- Como sustantivo (segundo sentido): la estructura o plan que sigue el código que ya existe.

Entre "sin diseño" y "con un diseño" hay infinitos grises: un diseño parcial, varios diseños en conflicto en una misma pieza de código, un diseño casi completo, etc. También puede haber diseños activamente malos, peores que no tener diseño (por ejemplo, código hecho desorganizado o complejo a propósito).

La ciencia del diseño de software sirve para tomar decisiones como: ¿cuál debe ser la estructura del código?, ¿importa más la velocidad del programa o la legibilidad del código?, ¿qué lenguaje usar? No cubre decisiones sobre la organización o las personas (estructura de la empresa, horarios, reuniones, medición del desempeño); esas son importantes, pero son sobre ti o tu organización, no sobre el software.

> "Anything that involves the architecture of your software system or the technical decisions you make while creating the system falls under the category of 'software design.'" (PDF p. 16)

## Every Programmer Is a Designer (Todo programador es diseñador)

Todo el que participa en un proyecto de software hace diseño: el lead diseña la arquitectura global, los senior sus grandes áreas, y los junior sus partes, aunque sean una porción de un archivo. Incluso escribir una sola línea implica algo de diseño. Hasta programando en solitario hay un proceso de diseño, aunque la decisión se tome un instante antes de teclear.

Nadie que escriba código puede ignorar el diseño, a ningún nivel. Pero el diseño no es una democracia: no se diseña por comité, porque el resultado sería un diseño activamente malo. Cada desarrollador tiene autoridad para tomar buenas decisiones en su área; si toma decisiones pobres o mediocres, un senior o el lead las sobreescribe (tiene poder de veto). Un diseñador debe escuchar sugerencias y feedback, pero cada decisión concreta la toma un individuo, no un grupo. En nota al pie: al sobreescribir una decisión, conviene educar al otro programador mostrando por qué la decisión propia es mejor; con el tiempo habrá que corregirlo cada vez menos.

## The Science of Software Design (La ciencia del diseño de software)

Para que algo sea ciencia, según el autor, debe cumplir varios requisitos:

- Contener conocimiento recopilado, compuesto de hechos (no opiniones) y reunido en algún lugar (como un libro).
- Que ese conocimiento esté organizado y categorizado, con las piezas correctamente relacionadas por importancia.
- Contener verdades generales o leyes básicas.
- Decir cómo hacer algo en el universo físico, aplicable en el trabajo o la vida.
- Haberse descubierto y demostrado por el método científico (observar, teorizar, experimentar y mostrar que el experimento funciona en todas partes).

En el software hay mucho conocimiento recopilado y algo organizado, pero falta la pieza clave: leyes claramente enunciadas, verdades inquebrantables. Los desarrolladores con experiencia saben qué es lo correcto, pero no por qué lo es ni qué hace correcta o incorrecta una decisión.

El libro distingue cuatro categorías de información:

- Definiciones: dicen qué es algo y cómo se usa.
- Hechos (facts): afirmaciones verdaderas sobre algo.
- Reglas (rules): consejos verdaderos sobre algo específico que guían decisiones (suelen indicar si hacer o no una acción), pero no permiten predecir el futuro ni deducir otras verdades.
- Leyes (laws): hechos que siempre son verdaderos, cubren un área amplia, ayudan a deducir otras verdades y permiten predecir lo que pasará.

Las leyes son lo más importante; el texto dirá explícitamente cuándo algo es una ley, y el Apéndice B etiqueta cada pieza mayor como ley, regla, definición o hecho. Ante una idea que parezca obvia, el autor invita a preguntarse: ¿sabía que era demostrablemente cierta?, ¿sabía su importancia?, ¿podría comunicarla con claridad?, ¿entendía cómo se relaciona con otros datos del campo? Pasar de "no/quizá" a "sí" en esas preguntas es parte de lo que diferencia una ciencia de una mera colección de ideas. La ciencia puede no ser perfecta aún y admitir correcciones, pero lo esencial es que el diseño de software *puede* ser una ciencia: hay leyes, pueden conocerse, son eternas, inmutables y funcionan.

## Why Has There Been No Science of Software Design? (¿Por qué no existía?)

Un repaso histórico explica el vacío. Los computadores nacieron como dispositivos abstractos en la mente de matemáticos, fundadores de la *computer science* (estudio matemático del procesamiento de información, no el estudio de la programación). Los primeros se construían a medida, operados por personal muy entrenado en entornos controlados (gobiernos, para apuntar misiles y descifrar códigos).

Con UNIVAC y los primeros computadores comerciales no había matemáticos suficientes para enviar uno con cada máquina. Así surgió el "working programmer": el autor lo personifica en "Bill de Contabilidad", que leía el manual y, a prueba y error, hacía funcionar la máquina bajo presión de la gerencia ("no nos importa cómo, hazlo"), aunque se cayera cada dos horas. A más computadores enviados, más "Bills" y menos operadores entrenados. El arte práctico de la programación creció de forma orgánica, "más como estudiantes universitarios aprendiendo a cocinar que como ingenieros de la NASA construyendo el transbordador espacial" (PDF p. 20).

Luego llegó *The Mythical Man-Month* (Addison-Wesley) de Fred Brooks, que observó un proyecto real y señaló hechos —el más famoso: añadir programadores a un proyecto de software atrasado lo atrasa más— sin crear una ciencia. Después vino una oleada de métodos: Rational Unified Process, Capability Maturity Model, Agile Software Development y otros. Ninguno afirmaba ser una ciencia; solo eran formas de gestionar la complejidad.

De ahí la situación actual: muchos métodos, ninguna ciencia real. Faltan de hecho dos ciencias:

- La ciencia de la gestión de software (cómo repartir el trabajo, planificar releases, estimar tiempos): recibe atención activa de los métodos citados, aunque la existencia de opiniones contradictorias e igualmente válidas indica que sus leyes fundamentales aún no se han formulado.
- La ciencia del diseño de software: recibe poca atención; en la escuela se enseña cómo funciona un lenguaje, no que pueda existir una ciencia para diseñar software. Este libro existe para llenar ese hueco.

Esta ciencia no es computer science (estudio matemático); es una ciencia para el working programmer, tan fiable como la física o la química para indicar cómo crear una aplicación. Se objeta que no es posible, que el diseño es demasiado variable y todo es cuestión de opinión; el autor responde que también se dijo que el universo físico era incognoscible y sí se descubrieron sus ciencias. Igualmente rebate el mito de que programar sea puro arte: hay arte al aplicar cualquier ciencia, pero primero tiene que existir la ciencia que aplicar, y hoy no existe.

> "The primary source of complexity in software is, in fact, the lack of this science." (PDF p. 21)

## Ideas clave

- "Diseño" tiene tres sentidos: planificar, el plan hecho y el plan que sigue el código existente; entre "sin diseño" y "con diseño" hay grises, e incluso diseños activamente malos.
- El diseño de software cubre la arquitectura y las decisiones técnicas del sistema; no cubre decisiones sobre la organización o las personas.
- Todo programador es diseñador y responde por su propio código; pero no se diseña por comité: cada decisión la toma un individuo, con veto de los senior.
- Para ser ciencia, un campo necesita conocimiento recopilado y organizado, verdades generales, aplicabilidad y el método científico; al software le faltan leyes claramente enunciadas.
- El libro distingue definiciones, hechos, reglas y leyes; las leyes son lo más importante y se marcan explícitamente (Apéndice B las cataloga).
- Históricamente, la programación práctica creció de forma orgánica (los "Bill") sin ciencia; *The Mythical Man-Month* aportó observaciones y luego llegaron métodos como RUP, CMM y Agile, pero ninguna ciencia.
- Faltan dos ciencias: la de la gestión (algo atendida) y la del diseño de software (desatendida); esta no es computer science, sino una ciencia para el working programmer.
- La falta de esta ciencia es la fuente principal de la complejidad del software.
